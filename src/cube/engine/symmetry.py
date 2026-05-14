"""Cube symmetries used for data augmentation.

Currently: LR-mirror (reflection across the U-D-F-B plane).

Under LR-mirror:
- L ↔ R faces swap
- U, D, F, B faces unchanged
- Quarter-turn direction inverts on all faces (chirality flips in a mirror)
- 180° turns are direction-invariant

Effect on move tokens:
    U  ↔ U'    D  ↔ D'    F  ↔ F'    B  ↔ B'    R  ↔ L'    L  ↔ R'
    U2 = U2    D2 = D2    F2 = F2    B2 = B2    R2 = L2    L2 = R2

The transformation is an involution: mirror_lr(mirror_lr(m)) == m.

Validation policy: this module is correct iff for every reconstruction in
the corpus, `mirror(scramble) + mirror(flat_solution)` produces a SOLVED
state. See tests/training/test_symmetry.py and the corpus-level check in
the augmentation pipeline. Per the chirality feedback in project memory,
mirror-style transforms have a silent-fail pattern — do not skip this.
"""

from __future__ import annotations

from cube.engine.moves import Face, Move, Turn

# Face swap under LR mirror. U/D/F/B fixed; L↔R.
_MIRRORED_FACE: dict[Face, Face] = {
    Face.U: Face.U,
    Face.D: Face.D,
    Face.F: Face.F,
    Face.B: Face.B,
    Face.R: Face.L,
    Face.L: Face.R,
}

# Turn flip under chirality reversal. CW ↔ CCW, HALF unchanged.
_MIRRORED_TURN: dict[Turn, Turn] = {
    Turn.CW: Turn.CCW,
    Turn.CCW: Turn.CW,
    Turn.HALF: Turn.HALF,
}


def mirror_lr_move(move: Move) -> Move:
    """Return the LR-mirror of a single move."""
    return Move(_MIRRORED_FACE[move.face], _MIRRORED_TURN[move.turn])


def mirror_lr_alg(alg: list[Move]) -> list[Move]:
    """Return the LR-mirror of an algorithm (preserves move order)."""
    return [mirror_lr_move(m) for m in alg]
