"""3x3 cube state, cubie-coordinate representation.

Corners (0-7): URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB
Edges (0-11):  UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR

Orientation conventions:
- Corner orientation (CO): twist of the U/D facelet relative to its "home"
  slot at each corner position, in {0, 1, 2}. U and D quarter turns do not
  change CO. F/B/R/L quarter turns twist the 4 affected corners with deltas
  summing to 0 mod 3.

Edge orientation is tracked under THREE axis conventions in parallel. The
"flip sets" are disjoint by design — each face quarter flips exactly one of
the three eo arrays:

- `eo` = UD-axis EO under FB-flip convention. F/B quarters flip 4 edges
  each. Standard for DR on UD axis (group <U, D, R2, L2, F2, B2>).
- `eo_fb` = FB-axis EO under LR-flip convention. L/R quarters flip 4 each.
  Standard for DR on FB axis (group <F, B, U2, D2, L2, R2>).
- `eo_rl` = RL-axis EO under UD-flip convention. U/D quarters flip 4 each.
  Standard for DR on RL axis (group <R, L, U2, D2, F2, B2>).

All three eo arrays are zero at solved. They can flip independently because
the 3 flip-axes are distinct.
"""

from __future__ import annotations

from dataclasses import dataclass

from cube.engine.moves import Face, Move, Turn

CORNER_NAMES = ("URF", "UFL", "ULB", "UBR", "DFR", "DLF", "DBL", "DRB")
EDGE_NAMES = ("UR", "UF", "UL", "UB", "DR", "DF", "DL", "DB", "FR", "FL", "BL", "BR")

# For each face's CW turn: (corner_cycle, co_deltas, edge_cycle, eo_deltas).
# A cycle (a, b, c, d) means: piece at a goes to b, b->c, c->d, d->a.
# co_deltas[i] is added (mod 3) to the piece moving from cycle[i] to cycle[(i+1)%4].
# eo_deltas[i] is added (mod 2) similarly.
# Per face's CW turn:
#   (corner_cycle, co_deltas, edge_cycle,
#    eo_ud_deltas, eo_fb_deltas, eo_rl_deltas)
# Flip-axis assignments: UD-axis EO flips on F/B; FB-axis EO flips on L/R;
# RL-axis EO flips on U/D. Each face's edge cycle flips exactly one of the
# three eo arrays.
_FACE_TURN_CW: dict[Face, tuple] = {
    Face.U: ((0, 1, 2, 3), (0, 0, 0, 0), (0, 1, 2, 3),
             (0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1)),
    Face.D: ((4, 7, 6, 5), (0, 0, 0, 0), (4, 7, 6, 5),
             (0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1)),
    Face.R: ((0, 3, 7, 4), (1, 2, 1, 2), (0, 11, 4, 8),
             (0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0)),
    Face.L: ((1, 5, 6, 2), (2, 1, 2, 1), (2, 9, 6, 10),
             (0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0)),
    Face.F: ((0, 4, 5, 1), (2, 1, 2, 1), (1, 8, 5, 9),
             (1, 1, 1, 1), (0, 0, 0, 0), (0, 0, 0, 0)),
    Face.B: ((3, 2, 6, 7), (1, 2, 1, 2), (3, 10, 7, 11),
             (1, 1, 1, 1), (0, 0, 0, 0), (0, 0, 0, 0)),
}


_DEFAULT_EO: tuple[int, ...] = (0,) * 12


@dataclass(frozen=True, slots=True)
class State:
    cp: tuple[int, ...]  # corner permutation, length 8
    co: tuple[int, ...]  # corner orientation, length 8
    ep: tuple[int, ...]  # edge permutation, length 12
    eo: tuple[int, ...]  # UD-axis edge orientation, length 12 (FB-flip)
    eo_fb: tuple[int, ...] = _DEFAULT_EO  # FB-axis EO (LR-flip)
    eo_rl: tuple[int, ...] = _DEFAULT_EO  # RL-axis EO (UD-flip)

    def apply(self, move: Move) -> State:
        cycle_c, dco, cycle_e, deo_ud, deo_fb, deo_rl = _FACE_TURN_CW[move.face]
        cp = list(self.cp)
        co = list(self.co)
        ep = list(self.ep)
        eo_arrays = [list(self.eo), list(self.eo_fb), list(self.eo_rl)]
        delta_arrays = (deo_ud, deo_fb, deo_rl)
        for _ in range(move.turn):
            cp, co = _apply_cycle(cp, co, cycle_c, dco, 3)
            ep, eo_arrays = _apply_edge_cycle(ep, eo_arrays, cycle_e, delta_arrays)
        return State(
            cp=tuple(cp),
            co=tuple(co),
            ep=tuple(ep),
            eo=tuple(eo_arrays[0]),
            eo_fb=tuple(eo_arrays[1]),
            eo_rl=tuple(eo_arrays[2]),
        )

    def apply_alg(self, alg: list[Move]) -> State:
        s = self
        for m in alg:
            s = s.apply(m)
        return s

    def is_solved(self) -> bool:
        return self == SOLVED


def _apply_cycle(
    perm: list[int],
    orient: list[int],
    cycle: tuple[int, int, int, int],
    deltas: tuple[int, int, int, int],
    mod: int,
) -> tuple[list[int], list[int]]:
    """Apply a 4-cycle to a (perm, single-orient) pair. Used for corners."""
    new_perm = perm.copy()
    new_orient = orient.copy()
    for i in range(4):
        src = cycle[i]
        dst = cycle[(i + 1) % 4]
        new_perm[dst] = perm[src]
        new_orient[dst] = (orient[src] + deltas[i]) % mod
    return new_perm, new_orient


def _apply_edge_cycle(
    perm: list[int],
    orient_arrays: list[list[int]],
    cycle: tuple[int, int, int, int],
    delta_arrays: tuple[tuple[int, int, int, int], ...],
) -> tuple[list[int], list[list[int]]]:
    """Apply a 4-cycle to edges, updating perm and N parallel orient arrays."""
    new_perm = perm.copy()
    new_orients = [o.copy() for o in orient_arrays]
    for i in range(4):
        src = cycle[i]
        dst = cycle[(i + 1) % 4]
        new_perm[dst] = perm[src]
        for j in range(len(orient_arrays)):
            new_orients[j][dst] = (orient_arrays[j][src] + delta_arrays[j][i]) % 2
    return new_perm, new_orients


SOLVED = State(
    cp=tuple(range(8)),
    co=(0,) * 8,
    ep=tuple(range(12)),
    eo=(0,) * 12,
    eo_fb=(0,) * 12,
    eo_rl=(0,) * 12,
)


def apply_alg(alg: list[Move], start: State = SOLVED) -> State:
    return start.apply_alg(alg)
