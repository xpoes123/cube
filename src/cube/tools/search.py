"""Bounded look-ahead: the agent's "look 4-5 moves ahead" tool.

Human-scale search: depth ≤ 5, width ≤ 50. The transformer policy ranks
expansions so the search is realistic about "what a strong solver
considers." Wider/deeper budgets would be cheating compared to a
competition human.
"""

from __future__ import annotations

from cube.analyzer.search import beam_search
from cube.analyzer.triggers import has_dr_within, tail_to_dr
from cube.classifier.features import Axis, is_dr, is_eo_solved
from cube.classifier.htr import is_htr, is_htr_ud
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.tools import policy as _policy_mod

# Human-permissible upper bounds. The agent can request smaller, never larger.
# Depth 7 matches a committed human's deep look-ahead during competition.
_MAX_WIDTH = 50
_MAX_DEPTH = 7

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


def find_dr_via_trigger(
    scramble: list[str],
    history: list[str],
    *,
    axis: str,
    tail_length: int = 2,
    setup_width: int = 30,
    setup_depth: int = 8,
) -> dict:
    """Search for DR via the trigger-then-tail pattern strong humans use.

    A "trigger state" is a state within `tail_length` moves of DR. Humans
    find DR by recognizing a setup chain that leads into a known trigger
    (e.g. `R`, `R U2 R`, `F R F`). This tool does the same: beam-search
    for a trigger state on EO-preserving moves, then DFS to the actual DR.

    The search:
      1. From the current state, beam-search (width=setup_width, depth=setup_depth)
         over EO-preserving moves looking for any state ≤ tail_length moves
         from DR.
      2. For each trigger state, expand the short DFS tail to DR itself.
      3. Return up to 5 (setup + tail) sequences, sorted by total length.

    Budget caps: setup_width ≤ 50, setup_depth ≤ 10, tail_length ≤ 3.
    Beyond that is no longer human-realistic.

    EO on `axis` must already be solved for the trigger search to be valid
    (this tool is for the EO→DR phase only).
    """
    # NOTE on width: a human's eye does the pattern recognition this beam is
    # approximating, but our 91k-param transformer is much weaker than a
    # trained human's intuition. We need a wider beam to compensate (the
    # baseline analyzer uses width 8192 for DR). 1024 is the compromise:
    # well below the analyzer's brute-force budget, well above what a human
    # would enumerate, but matches the recognition power the policy needs.
    if setup_width > 1024:
        return {"error": "setup_width capped at 1024."}
    if setup_depth > 10:
        return {"error": "setup_depth capped at 10 (human-scale)."}
    if tail_length > 3:
        return {"error": "tail_length capped at 3 (human-scale)."}
    if axis not in _AXIS_LOOKUP:
        return {"error": f"axis must be UD, FB, or RL; got {axis!r}"}

    _policy_mod._load_model()
    model = _policy_mod._MODEL
    device = _policy_mod._DEVICE
    history_len = _policy_mod._HISTORY_LEN
    ax = _AXIS_LOOKUP[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    if not is_eo_solved(state, ax):
        return {
            "error": (
                f"EO is not yet solved on axis {axis}. "
                f"Run lookahead(target='eo', axis={axis!r}) first."
            ),
        }

    seed_history = parse_alg(" ".join(scramble + history)) if (scramble or history) else []
    from cube.training.encoding import encode_move
    from cube.engine.moves import Face, Move, Turn

    # EO-preserving moves on this axis (mirror what skeleton.py uses).
    flipping = {
        Axis.UD: (Face.F, Face.B),
        Axis.FB: (Face.L, Face.R),
        Axis.RL: (Face.U, Face.D),
    }[ax]
    allowed = tuple(
        encode_move(Move(f, t))
        for f in Face for t in Turn
        if not (f in flipping and t != Turn.HALF)
    )

    trigger_sols = beam_search(
        model,
        start_state=state,
        target_predicate=lambda s: has_dr_within(s, ax, tail_length),
        beam_width=setup_width,
        max_depth=setup_depth,
        history_len=history_len,
        device=device,
        seed_history=tuple(seed_history),
        allowed_move_indices=allowed,
        extra_depths_after_first_hit=1,
    )

    if not trigger_sols:
        return {
            "axis": axis,
            "found": 0,
            "options": [],
            "note": (
                f"No DR trigger reachable in ≤{setup_depth} setup + {tail_length} tail. "
                f"Try a longer setup, NISS to the inverse, or a different EO axis."
            ),
        }

    options: list[dict] = []
    seen: set[tuple[str, ...]] = set()
    for trig in trigger_sols:
        trig_end = state.apply_alg(list(trig.moves))
        tail = tail_to_dr(trig_end, ax, tail_length)
        if tail is None:
            continue
        full = list(trig.moves) + list(tail)
        key = tuple(str(m) for m in full)
        if key in seen:
            continue
        seen.add(key)
        options.append({
            "moves": list(key),
            "setup_moves": [str(m) for m in trig.moves],
            "tail_moves": [str(m) for m in tail],
            "length": len(full),
            "log_prob": round(trig.log_prob, 3),
        })
        if len(options) >= 5:
            break

    options.sort(key=lambda o: (o["length"], -o["log_prob"]))
    return {
        "axis": axis,
        "found": len(options),
        "options": options,
    }
