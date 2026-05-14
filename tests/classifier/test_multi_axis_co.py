"""Validate multi-axis CO predicates.

The chirality silent-fail risk (per project memory) is exactly this:
get the axis-orientation convention subtly wrong, and most checks still
pass but some specific multi-axis EO/DR/CO interaction fails silently.

Invariants we verify exhaustively:

1. SOLVED has axis-CO solved on all 3 axes.
2. **Axis-preservation:** quarter turns on a face whose axis matches X
   never change X-axis CO. (U/D don't change UD-CO; F/B don't change
   FB-CO; R/L don't change RL-CO.)
3. **Non-degeneracy:** quarter turns on a face whose axis is NOT X
   DO change X-axis CO for at least one corner.
4. **Consistency with engine UD-CO:** for any state, `co_count(s, UD)`
   matches the existing UD-only count.
5. **Random-walk admissibility:** `dr_heuristic(s, axis) <= path_length`
   for sequences of random moves applied to SOLVED.
"""

from __future__ import annotations

import random

import pytest

from cube.classifier.features import (
    Axis,
    co_count,
    dr_heuristic,
    is_co_solved,
    is_dr,
)
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED


def test_solved_is_co_solved_all_axes():
    for axis in Axis:
        assert is_co_solved(SOLVED, axis)
        assert co_count(SOLVED, axis) == 0


# Faces on each axis. UD-axis = {U, D}, etc.
_AXIS_TO_FACES = {
    Axis.UD: (Face.U, Face.D),
    Axis.FB: (Face.F, Face.B),
    Axis.RL: (Face.R, Face.L),
}


def test_axis_preservation_quarter_turns():
    """Quarter turns on axis-X faces never change X-axis CO from SOLVED."""
    for axis, faces in _AXIS_TO_FACES.items():
        for face in faces:
            for turn in (Turn.CW, Turn.CCW, Turn.HALF):
                after = SOLVED.apply(Move(face, turn))
                assert is_co_solved(after, axis), (
                    f"{face}{turn} broke {axis} CO from SOLVED — axis "
                    f"preservation violated"
                )


def test_axis_preservation_random_walks():
    """A random sequence of axis-X moves leaves X-axis CO unchanged."""
    rng = random.Random(0)
    for axis, faces in _AXIS_TO_FACES.items():
        for _ in range(50):
            length = rng.randint(1, 12)
            moves = [
                Move(rng.choice(faces), rng.choice([Turn.CW, Turn.CCW, Turn.HALF]))
                for _ in range(length)
            ]
            after = SOLVED.apply_alg(moves)
            assert is_co_solved(after, axis), (
                f"axis-{axis} sequence {[str(m) for m in moves]} broke "
                f"{axis} CO — axis preservation violated"
            )


def test_non_degeneracy_off_axis_quarters_change_co():
    """A quarter turn on an off-axis face DOES change axis-CO."""
    for axis, faces in _AXIS_TO_FACES.items():
        for face in Face:
            if face in faces:
                continue
            # Quarter turn (not half) on a face off the axis must twist some corners.
            after = SOLVED.apply(Move(face, Turn.CW))
            assert not is_co_solved(after, axis), (
                f"{face} CW should have changed {axis}-CO but didn't"
            )
            assert co_count(after, axis) > 0


def test_ud_co_consistency_with_legacy():
    """co_count(state, UD) must match the legacy `sum(o != 0 for o in co)`."""
    rng = random.Random(1)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(200):
        seq = [rng.choice(moves) for _ in range(rng.randint(0, 12))]
        s = SOLVED.apply_alg(seq)
        legacy = sum(1 for o in s.co if o != 0)
        assert co_count(s, Axis.UD) == legacy


def test_dr_heuristic_admissible_all_axes():
    """For random move sequences of length K, dr_heuristic(axis) <= K."""
    rng = random.Random(2)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(200):
        k = rng.randint(0, 10)
        seq = [rng.choice(moves) for _ in range(k)]
        s = SOLVED.apply_alg(seq)
        for axis in Axis:
            h = dr_heuristic(s, axis)
            assert h <= k, (
                f"dr_heuristic({axis})={h} > path length {k} on "
                f"seq={[str(m) for m in seq]}"
            )


def test_is_dr_solved_on_solved_all_axes():
    for axis in Axis:
        assert is_dr(SOLVED, axis)


def test_is_dr_after_axis_only_moves():
    """After ONLY on-axis moves, the state is still DR on that axis.

    Modern DR is the group <U, D, R2, L2, F2, B2>. Stay inside the DR-UD
    move group from SOLVED → must remain in DR.
    """
    rng = random.Random(3)
    dr_ud_moves = [
        Move(Face.U, t) for t in Turn
    ] + [
        Move(Face.D, t) for t in Turn
    ] + [
        Move(f, Turn.HALF) for f in (Face.R, Face.L, Face.F, Face.B)
    ]
    for _ in range(100):
        seq = [rng.choice(dr_ud_moves) for _ in range(rng.randint(0, 10))]
        s = SOLVED.apply_alg(seq)
        assert is_dr(s, Axis.UD), (
            f"DR-UD-group sequence {[str(m) for m in seq]} left DR — "
            f"is_dr or DR-UD move set is wrong"
        )
