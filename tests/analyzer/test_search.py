"""Smoke tests for staged search. No trained model required — we use a
tiny untrained PolicyTransformer and verify that beam_search returns
engine-valid sequences when given a reachable target.
"""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")

from cube.analyzer.search import beam_search
from cube.analyzer.skeleton import _EO_PRESERVING, _eo_preserving_moves
from cube.classifier.features import Axis, is_eo_solved
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED
from cube.training.encoding import encode_move
from cube.training.model import ModelConfig, PolicyTransformer


def _tiny_model() -> PolicyTransformer:
    torch.manual_seed(0)
    return PolicyTransformer(
        ModelConfig(d_model=32, n_layers=1, n_heads=2, history_len=8)
    )


def test_beam_search_returns_engine_valid_sequences():
    """Hit the cheapest possible target: 'state is SOLVED' from a 1-move scramble.

    Even with an untrained model, beam_search should explore far enough at
    width 64 / depth 3 to undo a single move.
    """
    model = _tiny_model()
    scramble = [Move(Face.U, Turn.CW)]  # one U; solution is U'
    scrambled = SOLVED.apply_alg(scramble)
    sols = beam_search(
        model,
        start_state=scrambled,
        target_predicate=lambda s: s == SOLVED,
        beam_width=64,
        max_depth=3,
        history_len=8,
        device="cpu",
        seed_history=tuple(scramble),
    )
    assert sols, "untrained model should still find a 1-move solve under beam"
    # Verify the engine actually agrees.
    for sol in sols:
        end = scrambled.apply_alg(list(sol.moves))
        assert end == SOLVED


def test_eo_preserving_move_set_excludes_correct_quarters():
    ud = _EO_PRESERVING[Axis.UD]
    # UD-axis EO is flipped by F/B quarters. Half turns are fine.
    forbidden = {encode_move(Move(Face.F, Turn.CW)), encode_move(Move(Face.F, Turn.CCW)),
                 encode_move(Move(Face.B, Turn.CW)), encode_move(Move(Face.B, Turn.CCW))}
    assert forbidden.isdisjoint(set(ud))
    assert encode_move(Move(Face.F, Turn.HALF)) in ud
    assert encode_move(Move(Face.B, Turn.HALF)) in ud
    # 14 = 18 - 4 forbidden quarters
    assert len(ud) == 14


def test_eo_preserving_axes_are_distinct():
    """Each axis excludes a different pair of faces."""
    s = {a: frozenset(_eo_preserving_moves(a)) for a in (Axis.UD, Axis.FB, Axis.RL)}
    assert s[Axis.UD] != s[Axis.FB]
    assert s[Axis.UD] != s[Axis.RL]
    assert s[Axis.FB] != s[Axis.RL]


def test_beam_search_respects_allowed_moves():
    """Only allow U/U'/U2; the only reachable states from SOLVED are 4 (U group).
    From a 3-move U scramble, SOLVED is reachable with a U move.
    """
    model = _tiny_model()
    scramble = [Move(Face.U, Turn.CW)]
    scrambled = SOLVED.apply_alg(scramble)
    u_only = tuple(
        encode_move(Move(Face.U, t)) for t in Turn
    )
    sols = beam_search(
        model,
        start_state=scrambled,
        target_predicate=lambda s: s == SOLVED,
        beam_width=8,
        max_depth=3,
        history_len=8,
        device="cpu",
        seed_history=tuple(scramble),
        allowed_move_indices=u_only,
    )
    assert sols
    # All moves in the solution must be U-face.
    for sol in sols:
        for m in sol.moves:
            assert m.face == Face.U


def test_beam_search_immediate_hit_returns_empty_sequence():
    model = _tiny_model()
    sols = beam_search(
        model,
        start_state=SOLVED,
        target_predicate=lambda s: is_eo_solved(s, Axis.UD),
        beam_width=4,
        max_depth=5,
        history_len=8,
        device="cpu",
    )
    assert len(sols) == 1
    assert sols[0].moves == ()
