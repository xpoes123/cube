"""v35: progress-based DR scout.

Replaces the hit/miss cliff of `dr_trigger_options` with a local
"which direction is closer to DR" heuristic. BFS up to `max_depth`
over EO-preserving moves; for every leaf state, evaluate proximity
to DR using `co_count + slice_misplaced_count` (state-readable
counts, not future-knowledge). Returns top-k continuations sorted
by proximity.

This is NOT an oracle. The LLM still doesn't know whether a given
continuation leads to a shorter SOLVE — it only sees "this 4-move
setup leaves me at distance 5 from DR" vs "this 5-move setup leaves
me at distance 3." A human at the table makes the same kind of
judgment by eyeballing the cube ("hmm, those 2 bad corners would
clear if I U2-flipped them").

When a named trigger DOES happen to land in the BFS, the option is
flagged. Otherwise the LLM commits the setup it likes best, then
re-queries from the new state to look another `max_depth` moves
deep. That's the search-and-commit loop a real cuber uses.
"""

from __future__ import annotations

from collections import deque

from cube.classifier.dr_heuristics import trigger_label
from cube.classifier.features import Axis, co_count, is_eo_solved, slice_misplaced_count
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.tools.dr_pattern_lib import (
    _EO_PRESERVING_BY_AXIS,
    _SOLVED_MARKER,
    _apply_to_reduced,
    _axis_co_from_state,
    _slice_marker_from_state,
)
from cube.tools.dr_trigger_options import (
    _TRIGGER_CATALOG_BY_AXIS,
    _apply_trigger_reduced,
)


def dr_progress_options(
    scramble: list[str], history: list[str],
    *, axis: str = "UD", max_depth: int = 5, k: int = 5,
) -> dict:
    """BFS depth ≤ max_depth, return top-k continuations by DR-proximity.

    Args:
      scramble, history: the cube state
      axis: UD/FB/RL
      max_depth: how deep to look (capped at 5 — human visualization)
      k: how many options to return (top-k by DR distance)

    Returns:
      {
        axis, max_depth, states_explored,
        starting_dr_dist: the dr_dist at depth 0,
        options: [
          {
            setup_moves, setup_length,
            dr_dist: co_count + slice_misplaced_count at this state,
            substate_label: e.g. "DR-3C2E" if this IS a DR state,
                            otherwise "{co_count}c{slice_misplaced}e",
            hits_named_trigger: bool,
            trigger_family: present if hits_named_trigger,
            trigger_moves: present if hits_named_trigger,
            total_to_dr: present if hits_named_trigger,
          },
          ...
        ],
        note: explainer for the LLM.
      }
    """
    max_depth = min(max(max_depth, 1), 5)
    k = min(max(k, 1), 10)
    if axis not in _TRIGGER_CATALOG_BY_AXIS:
        return {"error": f"axis must be UD/FB/RL; got {axis!r}"}

    ax = {"UD": Axis.UD, "FB": Axis.FB, "RL": Axis.RL}[axis]
    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))
    if not is_eo_solved(state, ax):
        return {
            "error": (
                f"EO not yet solved on axis {axis}; run eo_pattern_lookup "
                f"and apply EO moves first."
            ),
        }

    start_co = _axis_co_from_state(state, ax)
    start_marker = _slice_marker_from_state(state, ax)
    solved_co = (0,) * 8
    solved_marker = _SOLVED_MARKER[ax]
    eo_preserving = _EO_PRESERVING_BY_AXIS[ax]
    trigger_parsed = [(label, alg_str, parse_alg(alg_str))
                      for label, alg_str in _TRIGGER_CATALOG_BY_AXIS[axis]]

    def _counts_from_reduced(co: tuple[int, ...], marker: tuple[int, ...]) -> tuple[int, int]:
        """O(1) state-readable counts (no future knowledge). Returns
        (bad_corners, bad_slice_edges):
          - bad_corners: how many corners are misoriented for this axis
            (i.e. their U/D sticker isn't on U or D).
          - bad_slice_edges: how many E-slice edges are currently in
            the wrong slice for this axis.
        A human counts both directly off the cube.
        """
        bad_c = sum(1 for c in co if c != 0)
        bad_e = sum(
            1 for i in range(12)
            if marker[i] == 1 and solved_marker[i] == 0
        )
        return bad_c, bad_e

    starting_bad_corners, starting_bad_slice = _counts_from_reduced(start_co, start_marker)

    seen: dict[tuple, int] = {(start_co, start_marker): 0}
    candidates: list[dict] = []

    def _evaluate(co, marker, path):
        bad_c, bad_e = _counts_from_reduced(co, marker)
        bad_total = bad_c + bad_e
        substate = trigger_label(bad_c, bad_e) if bad_total > 0 else "DR (solved)"
        entry = {
            "setup_moves": [str(m) for m in path],
            "setup_length": len(path),
            "bad_corners": bad_c,
            "bad_slice_edges": bad_e,
            "substate_label": substate,
            "hits_named_trigger": False,
        }
        for label, alg_str, moves in trigger_parsed:
            t_co, t_marker = _apply_trigger_reduced(co, marker, moves, ax)
            if t_co == solved_co and t_marker == solved_marker:
                entry["hits_named_trigger"] = True
                entry["trigger_family"] = label
                entry["trigger_moves"] = [str(m) for m in moves]
                entry["total_to_dr"] = len(path) + len(moves)
                break
        candidates.append(entry)

    _evaluate(start_co, start_marker, ())

    # BFS expansion.
    frontier: deque = deque()
    frontier.append((start_co, start_marker, (), None))
    states_visited = 1
    while frontier:
        co, marker, path, last_face = frontier.popleft()
        if len(path) >= max_depth:
            continue
        for m in eo_preserving:
            if last_face is not None and m.face == last_face:
                continue
            child_co, child_marker = _apply_to_reduced(co, marker, m, ax)
            key = (child_co, child_marker)
            if key in seen:
                continue
            seen[key] = len(path) + 1
            states_visited += 1
            new_path = path + (m,)
            _evaluate(child_co, child_marker, new_path)
            frontier.append((child_co, child_marker, new_path, m.face))

    # Rank: primary key = total bad pieces asc; secondary = setup
    # length asc; tiebreaker = prefer hits_named_trigger.
    candidates.sort(
        key=lambda c: (
            c["bad_corners"] + c["bad_slice_edges"],
            c["setup_length"],
            not c["hits_named_trigger"],
        ),
    )
    options = candidates[:k]

    return {
        "axis": axis,
        "max_depth": max_depth,
        "states_explored": states_visited,
        "starting_bad_corners": starting_bad_corners,
        "starting_bad_slice_edges": starting_bad_slice,
        "options": options,
        "note": (
            f"BFS depth ≤{max_depth} over EO-preserving moves on axis "
            f"{axis}; explored {states_visited} unique states. Each "
            f"option reports `bad_corners` (corners with U/D sticker on "
            f"the wrong face) and `bad_slice_edges` (E-slice edges in "
            f"the wrong slice). These are state-readable counts — what "
            f"you'd count yourself off the cube — NOT a distance-to-DR "
            f"oracle. Sorted by total bad pieces ascending (ties: "
            f"shorter setup first). Two states with the same bad-piece "
            f"count can have very different actual move-to-DR distance; "
            f"use the substate_label to judge which one you'd rather "
            f"land in. If hits_named_trigger=true, applying "
            f"trigger_moves from this state reaches DR. Otherwise: "
            f"apply your chosen setup via apply_moves, then call "
            f"dr_progress_options again from the new state."
        ),
    }
