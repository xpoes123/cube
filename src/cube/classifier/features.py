"""State feature extractors for FMC analysis.

All detectors are *informational*: they label a state with properties but never
constrain search. The "findability" policy reads these as conditioning signal
and decides on its own whether breaking a partial structure is worth it.

Scope notes:
- Multi-axis EO is tracked in State (eo, eo_fb, eo_rl). Helpers below accept
  an axis argument (default UD).
- CO detection is UD-axis only; multi-axis CO is a future addition (less
  pressing because authors rarely vary CO axis independently of EO axis).
- HTR detection is stubbed (raises NotImplementedError). Will be implemented
  when corpus segmentation needs it.
"""

from __future__ import annotations

from enum import Enum

from cube.engine.facelet import CORNER_COLORS, CORNER_FACELETS, face_of
from cube.engine.state import SOLVED, State


class Axis(str, Enum):
    UD = "UD"
    FB = "FB"
    RL = "RL"


# Edge index ranges per slice
_E_SLICE_EDGES = (8, 9, 10, 11)   # E-slice: FR, FL, BL, BR (perp to UD axis)
_S_SLICE_EDGES = (0, 2, 4, 6)     # S-slice: UR, UL, DR, DL (perp to FB axis)
_M_SLICE_EDGES = (1, 3, 5, 7)     # M-slice: UF, UB, DF, DB (perp to RL axis)

_SLICE_BY_AXIS = {
    Axis.UD: _E_SLICE_EDGES,
    Axis.FB: _S_SLICE_EDGES,
    Axis.RL: _M_SLICE_EDGES,
}


# ---------- EO / CO ----------


def eo_count(state: State, axis: Axis = Axis.UD) -> int:
    """Number of bad edges under the given axis's EO convention."""
    if axis == Axis.UD:
        return sum(state.eo)
    if axis == Axis.FB:
        return sum(state.eo_fb)
    if axis == Axis.RL:
        return sum(state.eo_rl)
    raise ValueError(f"unknown axis: {axis}")


# Face index sets per axis (face indices match facelet.py: U=0 R=1 F=2 D=3 L=4 B=5).
_AXIS_FACES: dict[Axis, frozenset[int]] = {
    Axis.UD: frozenset({0, 3}),  # U, D
    Axis.FB: frozenset({2, 5}),  # F, B
    Axis.RL: frozenset({1, 4}),  # R, L
}


def _corner_axis_oriented(state: State, position: int, axis: Axis) -> bool:
    """Is the cubie at `position` oriented relative to `axis`?

    Definition: the cubie has 3 facelets, exactly one of which carries an
    axis-colored sticker (e.g., U or D for UD-axis). The corner is
    "axis-oriented" iff that sticker is currently on an axis-face.

    Computed directly from facelet positions — no extra state needed.
    """
    cubie = state.cp[position]
    orient = state.co[position]
    axis_faces = _AXIS_FACES[axis]
    cubie_colors = CORNER_COLORS[cubie]

    # The cubie's slot 0 is always its U/D facelet (UD-color). For other
    # axes, find which of the cubie's slots carries an axis-color.
    axis_slot_in_cubie = next(
        s for s in range(3) if cubie_colors[s] in axis_faces
    )
    # to_facelets places cubie_colors[(slot - orient) % 3] at facelet_slots[slot].
    # So cubie_colors[axis_slot_in_cubie] lands at position-slot
    # (axis_slot_in_cubie + orient) % 3.
    pos_slot = (axis_slot_in_cubie + orient) % 3
    facelet_idx = CORNER_FACELETS[position][pos_slot]
    return face_of(facelet_idx) in axis_faces


def co_count(state: State, axis: Axis = Axis.UD) -> int:
    """Number of corners NOT oriented relative to `axis`.

    UD-axis: equivalent to `sum(1 for o in state.co if o != 0)` — fast path.
    Other axes: derived from facelets.
    """
    if axis == Axis.UD:
        return sum(1 for o in state.co if o != 0)
    return sum(1 for p in range(8) if not _corner_axis_oriented(state, p, axis))


def is_eo_solved(state: State, axis: Axis = Axis.UD) -> bool:
    return eo_count(state, axis) == 0


def is_co_solved(state: State, axis: Axis = Axis.UD) -> bool:
    """True iff all 8 corners are oriented relative to `axis`."""
    if axis == Axis.UD:
        return all(o == 0 for o in state.co)
    return all(_corner_axis_oriented(state, p, axis) for p in range(8))


def best_eo_axis(state: State) -> tuple[Axis, int]:
    """Return the axis with the fewest bad edges, and that count.

    Ties broken in UD > FB > RL order. Useful when ingesting an unlabeled
    solve to guess which axis the solver was on.
    """
    counts = {a: eo_count(state, a) for a in Axis}
    best = min(counts, key=lambda a: (counts[a], list(Axis).index(a)))
    return best, counts[best]


# ---------- Slices ----------


def slice_in_slice(state: State, axis: Axis = Axis.UD) -> bool:
    """True iff the slice perpendicular to `axis` has all its edges in slice."""
    slice_set = _SLICE_BY_AXIS[axis]
    return all(state.ep[i] in slice_set for i in slice_set)


def slice_misplaced_count(state: State, axis: Axis = Axis.UD) -> int:
    """How many slice edges are outside the slice (0-4)."""
    slice_set = _SLICE_BY_AXIS[axis]
    return sum(1 for i in slice_set if state.ep[i] not in slice_set)


# Back-compat aliases for the UD-axis helpers used elsewhere.
def e_slice_in_slice(state: State) -> bool:
    return slice_in_slice(state, Axis.UD)


def e_slice_misplaced_count(state: State) -> int:
    return slice_misplaced_count(state, Axis.UD)


# ---------- DR (domino reduction) ----------


def is_dr(state: State, axis: Axis = Axis.UD) -> bool:
    """Domino Reduction on the given axis.

    Conditions:
      1. EO solved on `axis`.
      2. CO solved on `axis` (corner's axis-color facelet on an axis-face).
      3. The axis-perpendicular slice edges all in their slice.
    """
    return (
        is_eo_solved(state, axis)
        and is_co_solved(state, axis)
        and slice_in_slice(state, axis)
    )


def dr_distance_lowerbound(state: State) -> int:
    """Cheap "how bad is this state for DR" score (UD axis).

    NOTE: This is bad-piece-count, NOT an admissible move-count lower bound.
    For an A*-admissible heuristic use `dr_heuristic` below.

    Cheap heuristic = max(bad_edges, misoriented_corners). Used for ordering /
    triage, not for proof of optimality.
    """
    return max(eo_count(state), co_count(state, Axis.UD), e_slice_misplaced_count(state))


# ---------- Admissible heuristics (for A* search) ----------
#
# Each face quarter turn affects at most 4 pieces of any one feature
# (4 edges flipped, 4 corners twisted, 4 slice edges cycled). So the
# minimum number of moves to fix N misplaced pieces is `ceil(N / 4)`.
# That gives a true lower bound on remaining moves to the target — the
# admissibility condition for A*.
#
# These are conservative (under-estimate true distance), which is exactly
# what A* needs. Stronger heuristics would speed up search further but
# must still under-estimate to preserve optimality.


def _ceil_div_4(n: int) -> int:
    return (n + 3) // 4


def eo_heuristic(state: State, axis: Axis = Axis.UD) -> int:
    """Admissible lower bound on moves to reach EO solved on `axis`."""
    return _ceil_div_4(eo_count(state, axis))


def dr_heuristic(state: State, axis: Axis = Axis.UD) -> int:
    """Admissible lower bound on moves to reach DR on `axis`.

    Takes the max of three independent admissible bounds:
      - moves to fix EO on this axis
      - moves to fix CO on this axis
      - moves to get axis-perpendicular slice edges in slice

    Each is the floor on its own subproblem; the max is therefore a valid
    lower bound on the combined problem.
    """
    return max(
        _ceil_div_4(eo_count(state, axis)),
        _ceil_div_4(co_count(state, axis)),
        _ceil_div_4(slice_misplaced_count(state, axis)),
    )


# ---------- DR corner structural features ----------
#
# After DR is reached on an axis, the corner permutation lies in the
# DR-stabilizer (group <U, D, R², L², F², B²>). FMC solvers classify
# the resulting corner state into "subsets" (4a1, 4b2, 2c3, …) that
# predict optimal HTR-finish length.
#
# Implementing the full canonical 96-case classifier requires a
# published lookup table or a BFS over the HTR subgroup (Milestone 3
# work). Until then, the structural features below capture most of the
# discriminative signal:
#   - `swap_count`: corners that left their home U/D layer
#   - `axial_count`: corners at column-correct positions
#   - `perm_parity`: even/odd corner permutation
#   - `max_cycle_len`: longest cycle in the corner permutation
#
# Corner column layout (matches CORNER_NAMES order):
#   index % 4 = 0: RF column (URF, DFR)
#   index % 4 = 1: FL column (UFL, DLF)
#   index % 4 = 2: LB column (ULB, DBL)
#   index % 4 = 3: RB column (UBR, DRB)
# A corner is "axial" iff it's at a position in its home column
# (cp[pos] % 4 == pos % 4).


def corner_swap_count(state: State) -> int:
    """Number of corners NOT in their home U/D layer.

    Always even (parity-preserving under the DR-group). Values: 0, 2, 4, 6, 8.
    Maps to the leading digit of the subset notation (0c…, 2c…, 4a/b/c, …).
    """
    return sum(
        1 for p in range(8)
        if (state.cp[p] // 4) != (p // 4)
    )


def corner_axial_count(state: State) -> int:
    """Number of corners at column-correct positions (cp[p] % 4 == p % 4).

    Values: 0, 2, 4, 6, 8 (parity-preserving in DR-group).
    """
    return sum(
        1 for p in range(8)
        if (state.cp[p] % 4) == (p % 4)
    )


def corner_perm_parity(state: State) -> int:
    """Sign of the corner permutation: 0 = even, 1 = odd.

    HTR group is a subgroup of the alternating group on corners, so after
    DR + corner-only moves, parity is always even. This is a sanity check
    and helps distinguish subsets that differ by orbit structure.
    """
    cp = list(state.cp)
    seen = [False] * 8
    sign = 0
    for i in range(8):
        if seen[i]:
            continue
        # Walk the cycle starting at i.
        j = i
        cycle_len = 0
        while not seen[j]:
            seen[j] = True
            j = cp[j]
            cycle_len += 1
        if cycle_len % 2 == 0:  # even-length cycles are odd permutations
            sign ^= 1
    return sign


def corner_cycle_structure(state: State) -> tuple[int, ...]:
    """Cycle lengths of the corner permutation, sorted descending.

    e.g. (3, 3, 2) means two 3-cycles and a 2-cycle. (1,1,1,1,1,1,1,1) =
    identity. Useful for distinguishing 4a (no permutation, just orbit
    swap) from 4b (2-cycles) from 4c (longer cycles).
    """
    cp = list(state.cp)
    seen = [False] * 8
    lengths: list[int] = []
    for i in range(8):
        if seen[i]:
            continue
        j = i
        cycle_len = 0
        while not seen[j]:
            seen[j] = True
            j = cp[j]
            cycle_len += 1
        lengths.append(cycle_len)
    return tuple(sorted(lengths, reverse=True))


def dr_corner_features(state: State) -> dict[str, int | tuple[int, ...]]:
    """Structural feature snapshot for a (presumed post-DR) state.

    Useful as inputs to a learned subset classifier or as auxiliary
    information alongside the canonical subset label. Not a substitute
    for the canonical 96-case classification — see `htr` module.
    """
    return {
        "swap_count": corner_swap_count(state),
        "axial_count": corner_axial_count(state),
        "perm_parity": corner_perm_parity(state),
        "cycle_structure": corner_cycle_structure(state),
    }


# ---------- HTR (half-turn reduction) ----------


def is_htr(state: State) -> bool:
    """Half-Turn Reduction: state solvable in <U2, D2, L2, R2, F2, B2>.

    Deferred. Will implement when corpus segmentation requires distinguishing
    DR-to-HTR transitions. Characterization: DR satisfied AND corners in HTR
    subset (one of 96 corner cases) AND edges in correct half-turn orbits.
    """
    raise NotImplementedError("HTR detection — deferred until needed for segmentation")


# ---------- Solved-piece detection (for blocks) ----------


def solved_corners(state: State) -> frozenset[int]:
    """Indices of corners that are home AND oriented."""
    return frozenset(i for i in range(8) if state.cp[i] == i and state.co[i] == 0)


def solved_edges(state: State) -> frozenset[int]:
    """Indices of edges that are home AND oriented."""
    return frozenset(i for i in range(12) if state.ep[i] == i and state.eo[i] == 0)


def pieces_solved(state: State, *, corners: tuple[int, ...], edges: tuple[int, ...]) -> bool:
    """Generic check: are the specified corner and edge positions all solved?"""
    return all(state.cp[c] == c and state.co[c] == 0 for c in corners) and all(
        state.ep[e] == e and state.eo[e] == 0 for e in edges
    )


# ---------- Blocks ----------

# 2x2x2 block at each corner index: the corner itself + its 3 adjacent edges.
# Edge indices follow EDGE_NAMES order: UR=0 UF=1 UL=2 UB=3 DR=4 DF=5 DL=6 DB=7
# FR=8 FL=9 BL=10 BR=11.
_2X2X2_EDGES: dict[int, tuple[int, int, int]] = {
    0: (0, 1, 8),    # URF: UR, UF, FR
    1: (1, 2, 9),    # UFL: UF, UL, FL
    2: (2, 3, 10),   # ULB: UL, UB, BL
    3: (3, 0, 11),   # UBR: UB, UR, BR
    4: (4, 5, 8),    # DFR: DR, DF, FR
    5: (5, 6, 9),    # DLF: DF, DL, FL
    6: (6, 7, 10),   # DBL: DL, DB, BL
    7: (7, 4, 11),   # DRB: DB, DR, BR
}


def is_2x2x2_at(state: State, corner: int) -> bool:
    """Is there a 2x2x2 block solved at the given corner (0-7)?"""
    return pieces_solved(state, corners=(corner,), edges=_2X2X2_EDGES[corner])


def find_2x2x2(state: State) -> int | None:
    """Return any corner with a solved 2x2x2 block, or None."""
    for c in range(8):
        if is_2x2x2_at(state, c):
            return c
    return None


# ---------- Summary feature vector ----------


def features(state: State) -> dict[str, int | bool]:
    """Cheap feature snapshot for logging / debugging / segmenter input.

    Not the final policy input — that will be a learned encoding. This is a
    human-readable view for analysis output.
    """
    return {
        "solved": state == SOLVED,
        "bad_edges": eo_count(state),
        "bad_corners": co_count(state),
        "e_slice_misplaced": e_slice_misplaced_count(state),
        "eo_solved": is_eo_solved(state),
        "co_solved": is_co_solved(state),
        "dr": is_dr(state),
        "solved_corner_count": len(solved_corners(state)),
        "solved_edge_count": len(solved_edges(state)),
        "has_2x2x2": find_2x2x2(state) is not None,
    }
