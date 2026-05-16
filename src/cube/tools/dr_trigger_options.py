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

# Trigger catalog — name + canonical alg string per axis. For UD-DR the
# trigger face is R (or L) and the EO-preserving non-CO-twisting setup
# face is U (or D). By cube symmetry, the FB-DR catalog uses U as
# trigger and F as setup; the RL-DR catalog uses F as trigger and L as
# setup. Half-turns of the EO-flipping axis (F2/B2 for UD; L2/R2 for FB;
# U2/D2 for RL) appear inside the trigger pattern.
#
# v15: extended from UD-only to all 3 axes by symmetric substitution.
_TRIGGER_CATALOG_BY_AXIS: dict[str, list[tuple[str, str]]] = {
    "UD": [
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
    ],
    # FB-DR: trigger=U, setup=F, half-turn-EO-flip-axis=L2/R2
    "FB": [
        ("DR-4C4E (U)", "U"),
        ("DR-4C4E (U')", "U'"),
        ("DR-3C2E (U F U')", "U F U'"),
        ("DR-3C2E (U F' U')", "U F' U'"),
        ("DR-4C2E (U F2 U')", "U F2 U'"),
        ("DR-4C4E (U F2 L2 U)", "U F2 L2 U"),
        ("DR-7C8E (U F D)", "U F D"),
        ("DR-7C8E (U' F D)", "U' F D"),
        ("DR-2C4E (U L2 U)", "U L2 U"),
        ("DR-8C8E (U D)", "U D"),
    ],
    # RL-DR: trigger=F, setup=L, half-turn-EO-flip-axis=U2/D2
    "RL": [
        ("DR-4C4E (F)", "F"),
        ("DR-4C4E (F')", "F'"),
        ("DR-3C2E (F L F')", "F L F'"),
        ("DR-3C2E (F L' F')", "F L' F'"),
        ("DR-4C2E (F L2 F')", "F L2 F'"),
        ("DR-4C4E (F L2 U2 F)", "F L2 U2 F"),
        ("DR-7C8E (F L B)", "F L B"),
        ("DR-7C8E (F' L B)", "F' L B"),
        ("DR-2C4E (F U2 F)", "F U2 F"),
        ("DR-8C8E (F B)", "F B"),
    ],
}

# Backward-compat alias (some downstream tooling may import the UD list).
_TRIGGER_CATALOG = _TRIGGER_CATALOG_BY_AXIS["UD"]

_FAMILY_RANK = {
    # v14b: inverted from the original Hitchhiker ordering. The 333.fm
    # corpus shows 4C4E is the WORST family (overrepresented in long
    # solves: 26 long vs 33 elite, vs 7 long / 160 elite for 4C2E).
    # 3C2E ("2c3") and 4C2E ("4b2") dominate elite solves.
    "DR-3C2E": 0, "DR-4C2E": 1, "DR-2C4E": 2,
    "DR-7C8E": 3, "DR-4C4E": 4, "DR-8C8E": 5,
}

# Empirical HTR-finish length by DR-substate, from the 333.fm corpus
# research (runs/333fm_research_2026-05-16.md). The key insight: a short
# DR landing in 4C4E is far worse than a longer DR landing in 3C2E, because
# the HTR-finish length differs by 4 moves on average. Used by the
# total-to-solved estimator in rank_key.
#
# Mapping (our trigger naming -> 333.fm tier):
#   DR-3C2E = "2c3"     -> ~5 HTR moves (elite-tier substate)
#   DR-4C2E = "4b2"     -> ~6 HTR moves (elite-tier substate)
#   DR-2C4E = "2c4"     -> ~6 HTR moves
#   DR-7C8E = mixed     -> ~7 HTR moves (uncommon)
#   DR-4C4E = "4c4e"    -> ~9 HTR moves (the "settled-for-worst" trigger)
#   DR-8C8E = degenerate -> ~10 HTR moves
_FAMILY_EXPECTED_HTR = {
    "DR-3C2E": 5,
    "DR-4C2E": 6,
    "DR-2C4E": 6,
    "DR-7C8E": 7,
    "DR-4C4E": 9,
    "DR-8C8E": 10,
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
    EO-solved state with at most `max_setup` EO-preserving setup moves.

    v15: now supports all 3 axes (UD/FB/RL). Each axis uses its own
    trigger catalog by symmetric substitution from the UD reference.
    """
    if axis not in _TRIGGER_CATALOG_BY_AXIS:
        return {
            "error": f"axis must be one of UD/FB/RL; got {axis!r}",
        }
    ax = {"UD": Axis.UD, "FB": Axis.FB, "RL": Axis.RL}[axis]

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
                      for label, alg_str in _TRIGGER_CATALOG_BY_AXIS[axis]]

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
                total_to_dr = plen + len(moves)
                # v23a (Phase A): drop expected_htr_moves and
                # expected_total_to_solved. These were oracle judgments
                # derived from empirical corpus stats — not something a
                # human solver would have. The LLM should weigh the
                # tradeoff (longer DR vs better substate) itself.
                best[label] = {
                    "trigger_family": label,
                    "canonical_alg": alg_str,
                    "setup_moves": [str(m) for m in path],
                    "setup_length": plen,
                    "trigger_length": len(moves),
                    "total_to_dr": total_to_dr,
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

    # v23a (Phase A): sort by total_to_dr only (raw length). The agent
    # has to weigh substate quality (4c4e vs 3c2e) itself, like a human
    # solver. JZP and pre_trigger_signature flags are visible structural
    # properties a human would notice; they're NOT a ranked oracle.
    def rank_key(o: dict):
        return (o["total_to_dr"], o["setup_length"])

    options.sort(key=rank_key)
    return {
        "axis": axis,
        "options": options[:6],
        "max_setup_searched": max_setup,
        "note": (
            f"Up to 6 named-trigger options on axis {axis}, sorted by "
            f"total_to_dr. JZP-eligible flag and pre_trigger_signature "
            f"(corner/edge counts) are structural properties a human can "
            f"see — use them to judge substate quality vs DR length. "
            f"There is NO expected_total_to_solved oracle; weigh the "
            f"tradeoffs yourself."
        ),
    }
