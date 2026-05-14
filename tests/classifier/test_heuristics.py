"""Admissibility tests for EO and DR heuristics.

A heuristic is admissible iff h(state) <= true_distance(state) for every
state. We can't enumerate all states, but we can spot-check:
1. The heuristic is 0 at the target state.
2. After one move from a target state, the heuristic returns at most 1.
3. After K moves, the heuristic returns at most K (by induction).

We test (1) and (2) exhaustively, then sample-test (3).
"""

from __future__ import annotations

import random

import pytest

from cube.classifier.features import Axis, dr_heuristic, eo_heuristic, is_dr, is_eo_solved
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED


def test_eo_heuristic_zero_at_target():
    for axis in Axis:
        assert eo_heuristic(SOLVED, axis) == 0


def test_dr_heuristic_zero_at_target():
    # DR(UD) on SOLVED state: eo=0, co=0, slice in slice. So h=0.
    assert dr_heuristic(SOLVED, Axis.UD) == 0


def test_eo_heuristic_at_most_1_after_one_move():
    for face in Face:
        for turn in Turn:
            after = SOLVED.apply(Move(face, turn))
            for axis in Axis:
                h = eo_heuristic(after, axis)
                assert h <= 1, (
                    f"after {face}{turn}, eo_heuristic({axis})={h} > 1 — "
                    f"not admissible"
                )


def test_dr_heuristic_at_most_1_after_one_move():
    for face in Face:
        for turn in Turn:
            after = SOLVED.apply(Move(face, turn))
            h = dr_heuristic(after, Axis.UD)
            assert h <= 1, f"after {face}{turn}, dr_heuristic={h} > 1"


def test_eo_heuristic_admissible_on_random_walks():
    """For random move sequences of length K, the heuristic must be <= K
    (the sequence itself is a valid undoing-path; the heuristic is a lower
    bound on optimal, and optimal <= K).
    """
    rng = random.Random(0)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(200):
        k = rng.randint(0, 8)
        seq = [rng.choice(moves) for _ in range(k)]
        s = SOLVED.apply_alg(seq)
        for axis in Axis:
            h = eo_heuristic(s, axis)
            assert h <= k, (
                f"eo_heuristic({axis})={h} exceeds path length {k} on "
                f"seq={[str(m) for m in seq]}"
            )


def test_dr_heuristic_admissible_on_random_walks():
    rng = random.Random(0)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(200):
        k = rng.randint(0, 10)
        seq = [rng.choice(moves) for _ in range(k)]
        s = SOLVED.apply_alg(seq)
        h = dr_heuristic(s, Axis.UD)
        assert h <= k, (
            f"dr_heuristic={h} exceeds path length {k} on "
            f"seq={[str(m) for m in seq]}"
        )


def test_heuristic_predicate_consistency():
    """When a predicate fires, the heuristic must be 0 (we're at target)."""
    rng = random.Random(0)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(500):
        seq = [rng.choice(moves) for _ in range(rng.randint(0, 10))]
        s = SOLVED.apply_alg(seq)
        if is_eo_solved(s, Axis.UD):
            assert eo_heuristic(s, Axis.UD) == 0
        if is_dr(s, Axis.UD):
            assert dr_heuristic(s, Axis.UD) == 0
