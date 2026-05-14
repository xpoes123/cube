"""Move and algorithm inversion — foundational for NISS.

Verifies:
  * `Move.inverse()` swaps CW/CCW and leaves HALF unchanged.
  * `invert_alg(seq)` is a true group inverse: applying seq then its
    inverse from any state returns to that state.
  * `invert_alg` is involutive: invert(invert(seq)) == seq.
"""

from __future__ import annotations

import random

from cube.engine.moves import ALL_MOVES, Face, Move, Turn
from cube.engine.notation import invert, invert_alg
from cube.engine.state import SOLVED


def test_move_inverse_quarter_turns():
    assert Move(Face.U, Turn.CW).inverse() == Move(Face.U, Turn.CCW)
    assert Move(Face.U, Turn.CCW).inverse() == Move(Face.U, Turn.CW)
    assert Move(Face.R, Turn.CW).inverse() == Move(Face.R, Turn.CCW)


def test_move_inverse_half_turn_is_self_inverse():
    for face in Face:
        m = Move(face, Turn.HALF)
        assert m.inverse() == m


def test_move_inverse_double_inverse_is_identity():
    for m in ALL_MOVES:
        assert m.inverse().inverse() == m


def test_invert_alg_alias_matches_invert():
    assert invert_alg is invert


def test_invert_alg_reverses_order_and_inverts():
    seq = [Move(Face.R, Turn.CW), Move(Face.U, Turn.HALF), Move(Face.F, Turn.CCW)]
    assert invert_alg(seq) == [
        Move(Face.F, Turn.CW),
        Move(Face.U, Turn.HALF),
        Move(Face.R, Turn.CCW),
    ]


def test_invert_alg_involutive():
    rng = random.Random(0)
    for _ in range(20):
        n = rng.randint(0, 25)
        seq = [rng.choice(ALL_MOVES) for _ in range(n)]
        assert invert_alg(invert_alg(seq)) == seq


def test_apply_then_invert_returns_to_start():
    """state.apply_alg(seq).apply_alg(invert_alg(seq)) == state."""
    rng = random.Random(42)
    for _ in range(20):
        n = rng.randint(1, 20)
        seq = [rng.choice(ALL_MOVES) for _ in range(n)]
        # Start from a random scrambled state, not just SOLVED.
        scramble = [rng.choice(ALL_MOVES) for _ in range(15)]
        start = SOLVED.apply_alg(scramble)
        after = start.apply_alg(seq).apply_alg(invert_alg(seq))
        assert after == start
