"""DR/HTR closeness heuristics — the signals a human champion sees.

These are NOT distance oracles. They are the COUNTS and LABELS that humans
read directly off the cube: the "C" and "E" in DR-XCYE; the JZP eligibility
flag; pairs-tracing (Wen) for inverse-frame switch decisions; ARM (Axial
Reduction Minus) for the other-axis distance signal.

Grounded in:
- Hitchhiker's Guide to DR (data/hitchhiker_dr.txt)
- Hitchhiker's Guide to FMC (data/hitchhiker_fmc.txt)

The agent reads these and applies probabilistic FMC reasoning, NOT exact
move-distance reasoning.
"""

from __future__ import annotations

from cube.classifier.features import (
    Axis,
    _AXIS_FACES,
    co_count,
    slice_misplaced_count,
    _SLICE_BY_AXIS,
)
from cube.engine.facelet import CORNER_COLORS, CORNER_FACELETS, EDGE_COLORS, face_of
from cube.engine.state import State

# Slot indices that make up each face's edge-belt (M-slice etc.) — used for
# JZP condition #2.
_M_SLICE_POSITIONS = (1, 3, 5, 7)   # UF, UB, DF, DB — perpendicular to RL
_S_SLICE_POSITIONS = (0, 2, 4, 6)   # UR, UL, DR, DL — perpendicular to FB
_E_SLICE_POSITIONS = (8, 9, 10, 11)  # FR, FL, BL, BR — perpendicular to UD


def _ud_color_sticker_face(state: State, position: int) -> int:
    """Which face index (0-5) does this corner's U/D-color sticker currently
    sit on? Used for JZP condition #1.
    """
    cubie = state.cp[position]
    orient = state.co[position]
    # Slot 0 of every cubie is its UD-color (by convention).
    pos_slot = (0 + orient) % 3
    facelet_idx = CORNER_FACELETS[position][pos_slot]
    return face_of(facelet_idx)


def is_jzp_eligible(state: State) -> bool:
    """JZP on UD-axis: three conditions (Hitchhiker DR §JZP).

    1. No U/D corner stickers on R/L faces.
    2. No E-slice edges (8-11) currently sitting in M-slice positions (1,3,5,7).
    3. Even number of unoriented corners on UD-axis (co_count is even).
    """
    # Condition 1
    rl_faces = {1, 4}
    for p in range(8):
        if _ud_color_sticker_face(state, p) in rl_faces:
            return False
    # Condition 2
    e_slice = set(_E_SLICE_POSITIONS)
    for slot in _M_SLICE_POSITIONS:
        if state.ep[slot] in e_slice:
            return False
    # Condition 3
    if sum(1 for c in state.co if c != 0) % 2 != 0:
        return False
    return True


def trigger_label(c_count: int, e_count: int) -> str:
    """Human-readable trigger label from (C, E) signature: DR-XCYE.

    Special cases per Hitchhiker DR §triggers — e.g., (4,4) is the most
    common ("R" trigger), (4,2) is `R U2 R'`, (3,2) is `R U R'`/`R U' R'`.
    """
    return f"DR-{c_count}C{e_count}E"


def _ud_color_present(cubie_colors: tuple[int, int, int]) -> bool:
    return any(c in {0, 3} for c in cubie_colors)  # face indices: U=0, D=3


def _fb_color_present(cubie_colors: tuple[int, int, int]) -> bool:
    return any(c in {2, 5} for c in cubie_colors)


def arm_other_axis(state: State, dr_axis: Axis) -> dict[str, int]:
    """Axial Reduction Minus on the OTHER axis (Hitchhiker DR §ARM).

    From the doc: "misoriented corner stickers that don't have F/B color"
    + "E layer ... misoriented edges". This estimates how close we'd be to
    JZP after switching to inverse.

    For dr_axis=UD, the "other axis" is FB (the EO axis after switching).
    We count: corners not FB-axis-oriented that DON'T have an F/B-color
    sticker visible on F/B face, plus E-layer (top+bottom) edges that are
    misoriented on the FB-axis.
    """
    other = Axis.FB if dr_axis == Axis.UD else (Axis.UD if dr_axis == Axis.FB else Axis.FB)
    other_faces = _AXIS_FACES[other]
    # Corner count: corners NOT axis-oriented on the other-axis AND lacking
    # the axis-color on an axis face — approximated via co_count on the other
    # axis (a reasonable upper bound, refined later).
    c_count = co_count(state, other)
    # Edge count: misoriented edges on the perpendicular-to-other slice that
    # aren't in their slice.
    e_count = slice_misplaced_count(state, other)
    return {"C": c_count, "E": e_count}


def count_top_pairs(state: State) -> int:
    """Wen's pairs-tracing rule (Hitchhiker DR §pairs).

    "Look at one of the edges in the E slice that don't belong there, then
    look at a misoriented corner — if the 2 stickers on the corner that
    are touching the E slice match with that E slice edge, then that's a
    pair on inverse."

    Returns count of (misplaced-E-edge, misoriented-UD-corner) pairs whose
    side-stickers match colors.
    """
    pairs = 0
    e_slice = set(_E_SLICE_POSITIONS)

    # Find misplaced E-slice edges (E-slice edges currently in U/D layer).
    misplaced_edges: list[tuple[int, tuple[int, int]]] = []
    for pos in range(12):
        if pos in e_slice:
            continue
        ep_here = state.ep[pos]
        if ep_here in e_slice:
            # This edge belongs in E-slice but is here. Get its 2 colors.
            cubie_colors = EDGE_COLORS[ep_here]
            misplaced_edges.append((pos, cubie_colors))

    # Find misoriented UD-corners (co != 0).
    misoriented: list[tuple[int, frozenset[int]]] = []
    for pos in range(8):
        if state.co[pos] == 0:
            continue
        cubie = state.cp[pos]
        # Get the 2 side-stickers (non-UD-color stickers) of this cubie.
        cubie_colors = CORNER_COLORS[cubie]
        side_colors = frozenset(c for c in cubie_colors if c not in {0, 3})
        misoriented.append((pos, side_colors))

    # Match: an E-edge with colors {a, b} pairs with a corner whose side
    # colors are {a, b}.
    for _, edge_cols in misplaced_edges:
        edge_set = frozenset(edge_cols)
        for _, corner_sides in misoriented:
            if edge_set == corner_sides:
                pairs += 1
                break  # one pair per edge
    return pairs


def solved_corner_count(state: State) -> int:
    """Number of corners home AND oriented (cp[i]==i and co[i]==0)."""
    return sum(1 for i in range(8) if state.cp[i] == i and state.co[i] == 0)


def solved_edge_count(state: State) -> int:
    """Number of edges home AND oriented under UD-EO convention."""
    return sum(1 for i in range(12) if state.ep[i] == i and state.eo[i] == 0)


# ---------------------------------------------------------------------------
# HTR closeness (post-DR)
# ---------------------------------------------------------------------------


def qt_corner_count(state: State) -> int:
    """Quarter-turn-corner count: how many of the 8 corners require a
    quarter turn to reach HTR (per Hitchhiker FMC §HTR).

    Operational definition: count corners NOT in the "axial position"
    (cp[i] % 4 != i % 4). This is the same as 8 - corner_axial_count.
    """
    return sum(1 for p in range(8) if (state.cp[p] % 4) != (p % 4))


def solved_corner_columns(state: State) -> int:
    """Count of (U-corner, D-corner) column pairs that are both home AND
    oriented. Used for floppy-reduction reasoning (Hitchhiker FMC §floppy)."""
    count = 0
    for col in range(4):
        u_pos = col
        d_pos = col + 4
        if (state.cp[u_pos] == u_pos and state.co[u_pos] == 0
                and state.cp[d_pos] == d_pos and state.co[d_pos] == 0):
            count += 1
    return count


# ---------------------------------------------------------------------------
# Single-call summary for inspect_state
# ---------------------------------------------------------------------------


def dr_closeness_for_axis(state: State, axis: Axis) -> dict:
    """Heuristic closeness signals for DR on `axis`, as a champion would read."""
    c = co_count(state, axis)
    e = slice_misplaced_count(state, axis)
    out = {
        "axis": axis.value,
        "misoriented_corners": c,
        "misplaced_slice_edges": e,
        "trigger_label": trigger_label(c, e),
    }
    if axis == Axis.UD:
        out["jzp_eligible"] = is_jzp_eligible(state)
        out["top_pairs_on_inverse"] = count_top_pairs(state)
    out["arm_other_axis"] = arm_other_axis(state, axis)
    return out


def htr_closeness(state: State) -> dict:
    """Post-DR structural signals for HTR reasoning."""
    return {
        "qt_corners": qt_corner_count(state),
        "solved_corner_columns": solved_corner_columns(state),
    }
