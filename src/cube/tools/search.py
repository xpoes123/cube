"""Bounded look-ahead: the agent's "look 4-5 moves ahead" tool.

Human-scale search: depth ≤ 5, width ≤ 50. The transformer policy ranks
expansions so the search is realistic about "what a strong solver
considers." Wider/deeper budgets would be cheating compared to a
competition human.
"""

from __future__ import annotations

from cube.analyzer.search import beam_search
from cube.classifier.features import Axis, is_dr, is_eo_solved
from cube.classifier.htr import is_htr, is_htr_ud
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.tools import policy as _policy_mod

# Human-permissible upper bounds. The agent can request smaller, never larger.
_MAX_WIDTH = 50
_MAX_DEPTH = 5

_AXIS_LOOKUP = {a.value: a for a in Axis}


def _target_predicate(target: str, axis_name: str | None):
    if target == "solved":
        return lambda s: s == SOLVED, "solved"
    if axis_name is None:
        raise ValueError(
            f"target={target!r} requires axis (UD, FB, or RL)"
        )
    axis = _AXIS_LOOKUP[axis_name]
    if target == "eo":
        return lambda s: is_eo_solved(s, axis), f"EO ({axis.value})"
    if target == "dr":
        return lambda s: is_dr(s, axis), f"DR ({axis.value})"
    if target == "htr":
        return lambda s: is_htr_ud(s) or is_htr(s), f"HTR ({axis.value})"
    raise ValueError(f"unknown target: {target!r}")


def lookahead(
    scramble: list[str],
    history: list[str],
    *,
    target: str,
    axis: str | None = None,
    width: int = 20,
    depth: int = 4,
) -> dict:
    """Run a bounded forward search looking for `target` within `depth` moves.

    Budget: width ≤ 50, depth ≤ 5 — capped to keep the search "human-scale."
    Roughly equivalent to a strong solver thinking through several
    candidate setups before committing.

    Args:
      target: one of `eo`, `dr`, `htr`, `solved`.
      axis:   `UD` | `FB` | `RL`. Required for `eo`/`dr`/`htr`; ignored for `solved`.
      width:  beam width (≤ 50).
      depth:  max moves to look ahead (≤ 5).

    Returns the top-N (up to width) move sequences that hit the target,
    each with its log-prob score. Empty if the target isn't reachable
    within the budget.
    """
    if width > _MAX_WIDTH:
        return {
            "error": (
                f"width={width} exceeds human-scale limit of {_MAX_WIDTH}. "
                f"A competition solver wouldn't enumerate that many candidates."
            ),
        }
    if depth > _MAX_DEPTH:
        return {
            "error": (
                f"depth={depth} exceeds human-scale limit of {_MAX_DEPTH}. "
                f"Use a stage-by-stage approach for deeper reasoning."
            ),
        }

    _policy_mod._load_model()
    model = _policy_mod._MODEL
    device = _policy_mod._DEVICE
    history_len = _policy_mod._HISTORY_LEN
    assert model is not None and device is not None

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    seed_history = parse_alg(" ".join(scramble + history)) if (scramble or history) else []
    predicate, label = _target_predicate(target, axis)

    sols = beam_search(
        model,
        start_state=state,
        target_predicate=predicate,
        beam_width=width,
        max_depth=depth,
        history_len=history_len,
        device=device,
        seed_history=tuple(seed_history),
        stop_at_first_hit=False,
        extra_depths_after_first_hit=1,
    )

    if not sols:
        return {
            "target": label,
            "found": 0,
            "options": [],
            "note": (
                f"No {label} found within depth={depth}, width={width}. "
                f"Try a longer setup chain, NISS, or a different axis."
            ),
        }

    # Dedupe by move sequence + take top by log-prob.
    seen: set[tuple[str, ...]] = set()
    options = []
    for sol in sorted(sols, key=lambda s: (len(s), -s.log_prob)):
        key = tuple(str(m) for m in sol.moves)
        if key in seen:
            continue
        seen.add(key)
        options.append({
            "moves": list(key),
            "length": len(sol),
            "log_prob": round(sol.log_prob, 3),
        })
        if len(options) >= min(10, width):
            break

    return {
        "target": label,
        "found": len(options),
        "options": options,
    }
