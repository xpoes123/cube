"""DR trigger-options menu — the human champion's "trigger picker".

For an EO-solved state on the UD axis, returns a ranked list of NAMED
trigger families that reach DR within a short setup. Each entry tells
the LLM: which trigger family, the actual setup moves, total-to-DR,
and structural flags (JZP, pairs).

Implemented via reduced-state BFS in the (co_tuple, slice_marker) space
(same trick as the DR pattern library — proven faithful quotient under
EO-preserving moves), so we can search to depth 5 in milliseconds.

Currently supports UD axis. FB/RL axes fall back to dr_recognize.

Ranking (Hitchhiker DR §triggers + §JZP):
  1. total_to_dr ascending
  2. JZP-eligible first within ties
  3. Family preference: 4C4E > 3C2E > 4C2E > 7C8E > rare
"""

from __future__ import annotations

from collections import deque

from cube.classifier.dr_heuristics import (
    count_top_pairs,
    is_jzp_eligible,
    trigger_label,
)
from cube.classifier.features import Axis, co_count, is_eo_solved, slice_misplaced_count
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State
from cube.tools.dr_pattern_lib import (
    _EO_PRESERVING_BY_AXIS,
    _SOLVED_MARKER,
    _apply_to_reduced,
    _axis_co_from_state,
    _slice_marker_from_state,
)

# Trigger catalog — name + canonical alg string.
_TRIGGER_CATALOG: list[tuple[str, str]] = [
    ("DR-4C4E (R)", "R"),
    ("DR-4C4E (R')", "R'"),
    ("DR-3C2E (R U R')", "R U R'"),
    ("DR-3C2E (R U' R')", "R U' R'"),
    ("DR-4C2E (R U2 R')", "R U2 R'"),
    ("DR-4C4E (R U2 F2 R)", "R U2 F2 R"),
    ("DR-7C8E (R U L)", "R U L"),
    ("DR-7C8E (R' U L)", "R' U L"),
    ("DR-2C4E (R F2 R)", "R F2 R"),
    ("DR-8C8E (R L)", "R L"),
]

_FAMILY_RANK = {
    "DR-4C4E": 0, "DR-3C2E": 1, "DR-4C2E": 2,
    "DR-7C8E": 3, "DR-2C4E": 4, "DR-8C8E": 5,
}


def _family_of(label: str) -> str:
    return label.split(" ", 1)[0]


def _apply_trigger_reduced(co, marker, trigger_moves, axis):
    """Apply a trigger move sequence to the reduced state representation."""
    for m in trigger_moves:
        co, marker = _apply_to_reduced(co, marker, m, axis)
    return co, marker


def dr_trigger_options(
    scramble: list[str], history: list[str],
    *, axis: str = "UD", max_setup: int = 5,
) -> dict:
    """Return a ranked menu of named DR triggers reachable from the current
    EO-solved state with at most `max_setup` EO-preserving setup moves."""
    if axis != "UD":
        return {
            "error": f"dr_trigger_options currently supports UD axis only "
                     f"(got {axis!r}). Use dr_recognize for FB/RL."
        }
    ax = Axis.UD

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))
    if not is_eo_solved(state, ax):
        return {
            "error": f"EO not yet solved on axis {axis}; run eo_pattern_lookup "
                     f"and apply EO moves first."
        }

    # Reduced state for BFS (CO + slice membership)
    start_co = _axis_co_from_state(state, ax)
    start_marker = _slice_marker_from_state(state, ax)
    solved_co = (0,) * 8
    solved_marker = _SOLVED_MARKER[ax]
    eo_preserving = _EO_PRESERVING_BY_AXIS[ax]

    # Precompute reduced-state trigger effects relative to the starting state:
    # we'll apply each trigger from each visited (co, marker) and check if
    # it lands on (solved_co, solved_marker).
    trigger_parsed = [(label, alg_str, parse_alg(alg_str))
                      for label, alg_str in _TRIGGER_CATALOG]

    # BFS in reduced-state space, tracking the move PATH so we can reconstruct
    # the setup as actual Move objects.
    frontier: deque = deque()
    frontier.append((start_co, start_marker, (), None))
    visited = {(start_co, start_marker): 0}

    # Find shortest setup per trigger family.
    best: dict[str, dict] = {}

    while frontier:
        co, marker, path, last_face = frontier.popleft()
        plen = len(path)
        # Test all triggers from this state.
        for label, alg_str, moves in trigger_parsed:
            if label in best:
                continue
            t_co, t_marker = _apply_trigger_reduced(co, marker, moves, ax)
            if t_co == solved_co and t_marker == solved_marker:
                # Found a setup for this trigger.
                # Compute structural flags on the actual State (the agent
                # cares about JZP and pairs at the pre-trigger moment).
                pre_state = state.apply_alg(list(path)) if path else state
                pre_c = co_count(pre_state, ax)
                pre_e = slice_misplaced_count(pre_state, ax)
                best[label] = {
                    "trigger_family": label,
                    "canonical_alg": alg_str,
                    "setup_moves": [str(m) for m in path],
                    "setup_length": plen,
                    "trigger_length": len(moves),
                    "total_to_dr": plen + len(moves),
                    "pre_trigger_signature": trigger_label(pre_c, pre_e),
                    "jzp_eligible": is_jzp_eligible(pre_state),
                    "top_pairs_on_inverse": count_top_pairs(pre_state),
                }
        if plen >= max_setup:
            continue
        for m in eo_preserving:
            if last_face is not None and m.face == last_face:
                continue
            child_co, child_marker = _apply_to_reduced(co, marker, m, ax)
            if (child_co, child_marker) in visited:
                continue
            visited[(child_co, child_marker)] = plen + 1
            frontier.append((child_co, child_marker, path + (m,), m.face))

    options = list(best.values())

    def rank_key(o: dict):
        family = _family_of(o["trigger_family"])
        return (
            o["total_to_dr"],
            0 if o["jzp_eligible"] else 1,
            _FAMILY_RANK.get(family, 99),
            o["setup_length"],
        )

    options.sort(key=rank_key)
    return {
        "axis": axis,
        "options": options[:6],
        "max_setup_searched": max_setup,
        "note": (
            f"Ranked by: shortest total → JZP first → family preference "
            f"(4C4E > 3C2E > 4C2E > 7C8E). Setup limit: {max_setup} moves. "
            f"If no options returned, the named-trigger DR is beyond {max_setup} "
            f"setup moves; fall back to dr_recognize for the optimal sequence."
        ),
    }
