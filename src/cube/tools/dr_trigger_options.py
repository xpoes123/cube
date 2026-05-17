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
    *, axis: str = "UD", max_setup: int = 4,
) -> dict:
    """Return named DR triggers reachable via short setup, DFS-style.

    v31: switched from BFS (computer-shape, finds guaranteed shortest)
    to bounded DFS with dedup at depth ≤4 (human-shape: try moves,
    look 4 deep, backtrack, don't re-try same state). Returns the
    first viable trigger PER FAMILY in DFS discovery order. Stops
    early once 3 families are found. Hard caps depth at 4 — a human's
    working visualization scope. If 0 triggers fit in 4 moves, the
    agent must commit a setup move or two by hand and re-call from
    the new state.
    """
    if axis not in _TRIGGER_CATALOG_BY_AXIS:
        return {"error": f"axis must be one of UD/FB/RL; got {axis!r}"}
    # v31b: hard-cap depth at 5 (was 4 in v31). 4 was too tight —
    # some scrambles genuinely need a 5-move setup. Elite cubers
    # do sometimes see 5 deep when they have a strong intuition
    # about the path.
    max_setup = min(max_setup, 5)
    ax = {"UD": Axis.UD, "FB": Axis.FB, "RL": Axis.RL}[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))
    if not is_eo_solved(state, ax):
        return {
            "error": f"EO not yet solved on axis {axis}; run eo_pattern_lookup "
                     f"and apply EO moves first."
        }

    start_co = _axis_co_from_state(state, ax)
    start_marker = _slice_marker_from_state(state, ax)
    solved_co = (0,) * 8
    solved_marker = _SOLVED_MARKER[ax]
    eo_preserving = _EO_PRESERVING_BY_AXIS[ax]

    trigger_parsed = [(label, alg_str, parse_alg(alg_str))
                      for label, alg_str in _TRIGGER_CATALOG_BY_AXIS[axis]]

    found: dict[str, dict] = {}
    states_visited = [0]
    EARLY_STOP_N_FAMILIES = 3
    # v31b: NO hard state cap. The per-state cost penalty (0.003s/state
    # charged in the handler) is what bounds wasteful search. A depth-5
    # BFS explores ~100K states ≈ 300s sim cost — significant (8% of
    # budget) but not crippling. Agent learns to do at most ~10 deep
    # DR scouts per attempt. Early-stop at 3 families found.
    MAX_STATES = 10**9  # effectively unbounded

    def _check_triggers_here(co, marker, path):
        for label, alg_str, moves in trigger_parsed:
            if label in found:
                continue
            t_co, t_marker = _apply_trigger_reduced(co, marker, moves, ax)
            if t_co == solved_co and t_marker == solved_marker:
                pre_state = state.apply_alg(list(path)) if path else state
                pre_c = co_count(pre_state, ax)
                pre_e = slice_misplaced_count(pre_state, ax)
                found[label] = {
                    "trigger_family": label,
                    "canonical_alg": alg_str,
                    "setup_moves": [str(m) for m in path],
                    "setup_length": len(path),
                    "trigger_length": len(moves),
                    "total_to_dr": len(path) + len(moves),
                    "pre_trigger_signature": trigger_label(pre_c, pre_e),
                    "jzp_eligible": is_jzp_eligible(pre_state),
                    "top_pairs_on_inverse": count_top_pairs(pre_state),
                }

    # v31b: BFS with global dedup, depth cap, state cap, family early-stop.
    # BFS-discovery-order IS the natural human "shortest setups first"
    # pattern — a human checks depth 0 (direct triggers) before depth 1
    # (1-move setups), etc. The state cap reflects "I gave up after
    # thinking about ~5K setups." Within those bounds, BFS finds the
    # SHORTEST setup per family — which is what a human reports.
    visited: dict[tuple, int] = {(start_co, start_marker): 0}
    frontier: deque = deque()
    frontier.append((start_co, start_marker, (), None))
    states_visited[0] = 1
    _check_triggers_here(start_co, start_marker, ())
    while frontier and len(found) < EARLY_STOP_N_FAMILIES and states_visited[0] < MAX_STATES:
        co, marker, path, last_face = frontier.popleft()
        if len(path) >= max_setup:
            continue
        for m in eo_preserving:
            if last_face is not None and m.face == last_face:
                continue
            child_co, child_marker = _apply_to_reduced(co, marker, m, ax)
            key = (child_co, child_marker)
            if key in visited:
                continue
            visited[key] = len(path) + 1
            states_visited[0] += 1
            _check_triggers_here(child_co, child_marker, path + (m,))
            if len(found) >= EARLY_STOP_N_FAMILIES:
                break
            if states_visited[0] >= MAX_STATES:
                break
            frontier.append((child_co, child_marker, path + (m,), m.face))

    options = list(found.values())

    return {
        "axis": axis,
        "options": options,
        "max_setup_searched": max_setup,
        "states_explored": states_visited[0],
        "note": (
            f"DFS depth ≤{max_setup} (hard-capped — human visualization scope). "
            f"Explored {states_visited[0]} unique states, stopped after "
            f"{len(options)} trigger families found (early-bail at "
            f"{EARLY_STOP_N_FAMILIES}). Options in DFS-discovery order — NOT a "
            f"ranked oracle. If 0 options: commit a setup move you think looks "
            f"promising via apply_moves, then re-call from the new state. "
            f"Read jzp_eligible and pre_trigger_signature for substate quality."
        ),
    }
