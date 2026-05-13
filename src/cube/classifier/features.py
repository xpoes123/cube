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


def co_count(state: State) -> int:
    """Number of misoriented corners under UD-axis CO convention."""
    return sum(1 for o in state.co if o != 0)


def is_eo_solved(state: State, axis: Axis = Axis.UD) -> bool:
    return eo_count(state, axis) == 0


def is_co_solved(state: State) -> bool:
    return co_count(state) == 0


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
      2. CO solved (currently UD-axis CO only — see scope notes).
      3. The axis-perpendicular slice edges all in their slice.

    Note: CO check is UD-axis only. For DR on FB or RL axis, this returns
    True only when CO happens to be solved under UD convention too, which
    is a stricter condition than DR-on-axis strictly requires. Multi-axis
    CO is a follow-up.
    """
    return (
        is_eo_solved(state, axis)
        and is_co_solved(state)
        and slice_in_slice(state, axis)
    )


def dr_distance_lowerbound(state: State) -> int:
    """Heuristic lower bound on moves to reach DR (UD axis).

    Cheap heuristic = max(bad_edges, misoriented_corners). Used for ordering /
    triage, not for proof of optimality. The policy/value model will replace
    this with a learned estimate later.
    """
    return max(eo_count(state), co_count(state), e_slice_misplaced_count(state))


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
