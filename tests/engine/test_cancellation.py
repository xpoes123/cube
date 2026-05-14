"""Tests for move-sequence cancellation."""

from __future__ import annotations

from cube.engine.cancellation import cancel_moves
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED


def test_identity_pair_cancels():
    moves = parse_alg("U U'")
    assert cancel_moves(moves) == []


def test_double_turn_combines():
    moves = parse_alg("U U")
    assert cancel_moves(moves) == [Move(Face.U, Turn.HALF)]


def test_quarter_then_half_combines():
    moves = parse_alg("U U2")
    assert cancel_moves(moves) == [Move(Face.U, Turn.CCW)]


def test_half_then_half_cancels():
    moves = parse_alg("U2 U2")
    assert cancel_moves(moves) == []


def test_through_commute():
    """U D U → D U2 (U and D commute, so the two U's combine)."""
    moves = parse_alg("U D U")
    out = cancel_moves(moves)
    # Result should have 2 moves: D + U2 (in some order)
    assert len(out) == 2
    assert Move(Face.U, Turn.HALF) in out
    assert Move(Face.D, Turn.CW) in out


def test_no_false_cancellation():
    moves = parse_alg("R U R'")
    assert cancel_moves(moves) == list(moves)


def test_engine_equivalence():
    """The cancelled sequence must produce the same final state."""
    import random
    rng = random.Random(0)
    all_moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(50):
        n = rng.randint(0, 20)
        seq = [rng.choice(all_moves) for _ in range(n)]
        cancelled = cancel_moves(seq)
        # Both should reach the same state from SOLVED.
        s1 = SOLVED.apply_alg(seq)
        s2 = SOLVED.apply_alg(cancelled)
        assert s1 == s2, f"cancellation changed state: {seq} → {cancelled}"


def test_savings_on_realistic_skeleton():
    """A typical skeleton with boundary moves likely to cancel."""
    # EO ending in D, DR starting with D' — should cancel.
    seq = parse_alg("U' B L' F' D D'")
    out = cancel_moves(seq)
    assert out == parse_alg("U' B L' F'")


def test_solves_test_scramble_reduces():
    """Real example: the 31-move solve from the M1 test should not get
    longer; ideally it shrinks via boundary cancellation."""
    seq = parse_alg(
        "U B L' F' R' D' U L U' B2 L "
        "U' R2 U F2 U F2 U' B2 D "
        "U2 R2 D2 F2 R2 B2 U2 F2 R2 D2 U2"
    )
    out = cancel_moves(seq)
    assert len(out) <= len(seq)
