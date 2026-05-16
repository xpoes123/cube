"""State-inspection tools for the LLM FMC agent.

All functions take a scramble + move-history pair (both lists of move
strings in WCA notation) and return JSON-serializable summaries. The
agent never sees raw `State` objects — it gets human-readable dicts.
"""

from __future__ import annotations

from cube.classifier.features import (
    Axis,
    co_count,
    eo_count,
    is_dr,
    is_eo_solved,
)
from cube.classifier.htr import is_htr, is_htr_ud
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State


def _state_after(scramble: list[str], history: list[str]) -> State:
    """Apply scramble + history to SOLVED. Centralized for consistency."""
    s = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        s = s.apply_alg(parse_alg(" ".join(history)))
    return s


from cube.engine.state import EDGE_NAMES


def _bad_edge_slots(state, axis: Axis) -> list[str]:
    """Slot names of edges that are mis-oriented on the given axis."""
    if axis == Axis.UD:
        arr = state.eo
    elif axis == Axis.FB:
        arr = state.eo_fb
    elif axis == Axis.RL:
        arr = state.eo_rl
    else:
        return []
    return [EDGE_NAMES[i] for i, v in enumerate(arr) if v]


# Which slots sit on each face (used to organize bad edges by face).
# An edge sits on a face iff its name contains that face letter.
_FACE_SLOTS: dict[str, list[str]] = {
    "U": ["UR", "UF", "UL", "UB"],
    "D": ["DR", "DF", "DL", "DB"],
    "F": ["UF", "DF", "FR", "FL"],
    "B": ["UB", "DB", "BL", "BR"],
    "R": ["UR", "DR", "FR", "BR"],
    "L": ["UL", "DL", "FL", "BL"],
}

# Which faces flip EO when turned a QUARTER, per axis. Quoting from
# the EO theory: UD-EO is flipped by F/B quarters, FB-EO by L/R, RL-EO by U/D.
_FLIPPING_FACES_PER_AXIS: dict[str, list[str]] = {
    "UD": ["F", "B"],
    "FB": ["L", "R"],
    "RL": ["U", "D"],
}


def _bad_edges_by_flipping_face(
    bad_slots: list[str], axis: Axis,
) -> dict[str, list[str]]:
    """For the EO axis's flipping faces, list which bad edges sit on each.
    A quarter turn of that face flips exactly its 4 edges; the bad edges
    among them tell the agent which face turns help vs. hurt."""
    out: dict[str, list[str]] = {}
    bad_set = set(bad_slots)
    for face in _FLIPPING_FACES_PER_AXIS[axis.value]:
        on_face = [s for s in _FACE_SLOTS[face] if s in bad_set]
        out[face] = on_face
    return out


def inspect_state(scramble: list[str], history: list[str]) -> dict:
    """Classify the current cube state. The agent's primary 'look at the cube' tool.

    Returns a dict with:
      - `bad_edges_per_axis`: how many edges are misoriented on each EO axis
        (UD, FB, RL). Lower is better; 0 means EO is solved on that axis.
      - `bad_corners_per_axis`: corner orientation count per axis.
      - `eo_solved_axes`: list of axes where EO is fully solved.
      - `dr_solved_axes`: list of axes where DR is solved (EO + corner-CO + cp/ep in DR set).
      - `in_strict_htr`: True iff the state is in the strict HTR subgroup
        (cp + ep in HTR subgroups AND all-axis EO/CO == 0).
      - `in_canonical_htr_ud`: True iff is_htr_ud (single-axis canonical HTR).
      - `is_solved`: True iff the state == SOLVED.
      - `move_count`: how many moves have been played (length of history).
    """
    s = _state_after(scramble, history)
    eo_axes = [a for a in Axis if is_eo_solved(s, a)]
    dr_axes = [a for a in Axis if is_dr(s, a)]
    bad_slots = {a.value: _bad_edge_slots(s, a) for a in Axis}
    # For each EO axis, group its bad edges by the flipping face that would
    # affect them. This lets the LLM SEE "F has 3 bad edges on UD-axis, so F
    # quarter-turn fixes 3 (and breaks 1)" directly from the output, instead
    # of having to mentally map slot names → faces.
    bad_by_face = {
        ax.value: _bad_edges_by_flipping_face(bad_slots[ax.value], ax)
        for ax in Axis
    }
    return {
        "bad_edges_per_axis": {a.value: eo_count(s, a) for a in Axis},
        "bad_edge_slots_per_axis": bad_slots,
        "bad_edges_by_flipping_face": bad_by_face,
        "bad_corners_per_axis": {a.value: co_count(s, a) for a in Axis},
        "eo_solved_axes": [a.value for a in eo_axes],
        "dr_solved_axes": [a.value for a in dr_axes],
        "in_strict_htr": bool(is_htr(s)),
        "in_canonical_htr_ud": bool(is_htr_ud(s)),
        "is_solved": s == SOLVED,
        "move_count": len(history),
    }


def try_alg(
    scramble: list[str], history: list[str], alg: list[str],
) -> dict:
    """Hypothetically apply `alg` after `history` and report the deltas.

    The agent uses this to preview a continuation without committing.

    Returns:
      - `before`: inspect_state(scramble, history) summary
      - `after`: inspect_state(scramble, history + alg) summary
      - `deltas`: which counts changed and by how much
      - `solved`: True iff the resulting state is SOLVED
    """
    before = inspect_state(scramble, history)
    after = inspect_state(scramble, history + alg)
    deltas: dict[str, dict[str, int]] = {}
    for key in ("bad_edges_per_axis", "bad_corners_per_axis"):
        dk: dict[str, int] = {}
        for ax in before[key]:
            d = after[key][ax] - before[key][ax]
            if d != 0:
                dk[ax] = d
        if dk:
            deltas[key] = dk
    # Surface which specific edge slots became fixed / broken per axis, so the
    # LLM can SEE "this alg flipped UF and DF on UD-axis, breaking 1 edge and
    # fixing 2" instead of just a count delta.
    edge_changes: dict[str, dict[str, list[str]]] = {}
    for ax in ("UD", "FB", "RL"):
        before_set = set(before["bad_edge_slots_per_axis"][ax])
        after_set = set(after["bad_edge_slots_per_axis"][ax])
        newly_oriented = sorted(before_set - after_set)
        newly_misoriented = sorted(after_set - before_set)
        if newly_oriented or newly_misoriented:
            edge_changes[ax] = {
                "newly_oriented": newly_oriented,
                "newly_misoriented": newly_misoriented,
            }
    return {
        "before": before,
        "after": after,
        "deltas": deltas,
        "edge_changes_per_axis": edge_changes,
        "solved": after["is_solved"],
    }


def verify_solved(scramble: list[str], solution: list[str]) -> dict:
    """Ground-truth check: apply scramble + solution to SOLVED, return whether
    the cube is solved. Use this as the final acceptance test.
    """
    final = _state_after(scramble, solution)
    return {
        "solves": final == SOLVED,
        "total_moves": len(solution),
    }
