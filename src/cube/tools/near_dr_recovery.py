"""v35: near-DR recovery tool.

The v34/v35 corpus eval and the v35 inverse-of-scramble cheat incident
both surfaced the same failure mode: the agent reaches a near-DR state
(DR-0C1E, DR-2C0E, DR-2C1E — 1-3 bad pieces shy of full DR), and
`dr_progress_options` returns no path forward because every EO-preserving
move from there cycles between near-DR states without closing the last
edge or corner. The agent's standard tools then offer no way out, it
brain-walks, and (in v35) considered the inverse-of-scramble cheat as
a "better than DNF" fallback.

This tool handles that specific case: from a state with `bad_corners +
bad_slice_edges ≤ 3`, run an A*-pruned BFS over **all 18 face moves**
(EO-breaking allowed) and return short solutions to SOLVED or to a
canonical HTR-UD state. A human cuber doing this on paper is using the
"slice insertion" or "M-slice cleanup" technique — recognize the near-DR
pattern as something a few EO-breaking moves can finish through HTR.

Not an oracle: the search is bounded (max_depth ≤ 10, max_nodes ≤ 50k)
and returns nothing if the state really is far from solved/HTR.
"""

from __future__ import annotations

from cube.analyzer.search import a_star_search
from cube.classifier.features import (
    Axis,
    co_count,
    is_eo_solved,
    slice_misplaced_count,
)
from cube.classifier.htr import htr_lower_bound, is_htr_ud
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.training.encoding import encode_move
from cube.engine.moves import Face, Move, Turn


_AXIS_LOOKUP = {a.value: a for a in Axis}

# All 18 face moves (EO-breaking moves are explicitly allowed here).
_ALL_FACE_MOVES = tuple(
    encode_move(Move(f, t)) for f in Face for t in Turn
)


def near_dr_recovery(
    scramble: list[str], history: list[str],
    *, axis: str = "UD", max_depth: int = 8, target: str = "solved", k: int = 3,
) -> dict:
    """A* search from a near-DR state for short solutions allowing
    EO-breaking moves.

    Args:
      scramble, history: current cube position
      axis: which DR axis the agent is targeting. Used for the
            near-DR precondition check and HTR-distance heuristic.
      max_depth: bound on search depth. ≤ 10. Realistic for human-
                 scale "I'll try breaking EO for a couple moves to
                 close the cycle" reasoning.
      target: 'solved' or 'htr_ud'. The latter is useful when the
              search to fully-solved is too deep; landing in HTR is
              still a clean continuation for apply_htr_phase.
      k: how many shortest solutions to return.

    Returns:
      {
        axis, target, near_dr_signature (e.g. "DR-2C0E"),
        starting_bad_corners, starting_bad_slice_edges,
        options: [{moves, length}, ...]   (up to k, sorted by length asc)
        note: explainer.
      }

    Preconditions:
      - bad_corners + bad_slice_edges ≤ 3 (the "near-DR" precondition).
        Outside this range, the agent should use dr_progress_options
        or commit setup moves manually. The tool refuses if the state
        isn't actually near-DR — it's not a general-purpose solver.
    """
    max_depth = min(max(max_depth, 1), 10)
    if axis not in _AXIS_LOOKUP:
        return {"error": f"axis must be UD/FB/RL; got {axis!r}"}
    if target not in ("solved", "htr_ud"):
        return {"error": f"target must be 'solved' or 'htr_ud'; got {target!r}"}
    ax = _AXIS_LOOKUP[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    bad_c = co_count(state, ax) if is_eo_solved(state, ax) else co_count(state, ax)
    bad_e = slice_misplaced_count(state, ax)
    bad_total = bad_c + bad_e

    near_dr_signature = (
        "DR (already solved on axis)" if bad_total == 0
        else f"DR-{bad_c}C{bad_e}E"
    )

    if bad_total > 3:
        return {
            "axis": axis,
            "starting_bad_corners": bad_c,
            "starting_bad_slice_edges": bad_e,
            "near_dr_signature": near_dr_signature,
            "options": [],
            "error": (
                f"This tool is for near-DR states only (bad_corners + "
                f"bad_slice_edges ≤ 3). Current state has {bad_total} bad "
                f"pieces; use dr_progress_options to navigate from here "
                f"and call near_dr_recovery again once you're within 3."
            ),
        }

    if target == "solved":
        predicate = lambda s: s == SOLVED
    else:
        predicate = is_htr_ud

    # Admissible heuristic: distance-to-HTR for the heuristic floor.
    # When target is HTR-UD this is exactly the right heuristic. When
    # target is SOLVED, HTR-distance is still admissible (HTR is a
    # waypoint on every solve path), giving us A* pruning power.
    def h(s):
        bound = htr_lower_bound(s, ax)
        return bound if bound is not None else 0

    sols = a_star_search(
        None,  # no policy model — pure A*
        start_state=state,
        target_predicate=predicate,
        heuristic=h,
        max_depth=max_depth,
        # Generous cap: at depth 8 over 18 moves the state space is
        # large; we want the cap to be the depth, not the node count.
        max_nodes=500_000,
        history_len=0,
        device="cpu",
        seed_history=(),
        allowed_move_indices=_ALL_FACE_MOVES,
        policy_weight=0.0,
    )

    if not sols:
        return {
            "axis": axis,
            "target": target,
            "starting_bad_corners": bad_c,
            "starting_bad_slice_edges": bad_e,
            "near_dr_signature": near_dr_signature,
            "max_depth_searched": max_depth,
            "options": [],
            "note": (
                f"No path to {target} found within depth ≤ {max_depth} (all "
                f"18 face moves explored). State may still be too far from "
                f"the target despite being labeled near-DR. Try a larger "
                f"max_depth (cap is 10), or commit a setup move via "
                f"apply_moves and re-call."
            ),
        }

    # Dedupe + take shortest.
    seen: set[tuple[str, ...]] = set()
    options: list[dict] = []
    for sol in sorted(sols, key=lambda s: len(s)):
        key = tuple(str(m) for m in sol.moves)
        if key in seen:
            continue
        seen.add(key)
        options.append({
            "moves": list(key),
            "length": len(sol),
        })
        if len(options) >= k:
            break

    return {
        "axis": axis,
        "target": target,
        "starting_bad_corners": bad_c,
        "starting_bad_slice_edges": bad_e,
        "near_dr_signature": near_dr_signature,
        "max_depth_searched": max_depth,
        "options": options,
        "note": (
            f"From {near_dr_signature}, A* over all 18 face moves to "
            f"depth ≤ {max_depth}. {len(options)} short {target} sequences "
            f"found. EO-breaking moves ARE allowed — this is the slice-"
            f"cleanup / 'break EO briefly to close the cycle' technique "
            f"humans use when DR-preserving moves leave a 1-2 piece "
            f"residual. Pick the shortest, apply_moves, you should be "
            f"at {target} (verify with quick_check)."
        ),
    }
