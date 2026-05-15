"""BFS-based DR finder — algorithmic, no policy ranking.

Sibling to eo_bfs. Some scrambles' DR is policy-weak too (the trigger
search fails because the policy beam doesn't rank the right setup
moves high enough). Plain BFS over EO-preserving moves to a trigger
state, then short DFS to actual DR.
"""

from __future__ import annotations

from collections import deque

from cube.analyzer.triggers import has_dr_within, tail_to_dr
from cube.classifier.features import Axis, is_eo_solved
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State

_AXIS_LOOKUP = {a.value: a for a in Axis}
_FLIPPING_PER_AXIS = {
    Axis.UD: (Face.F, Face.B),
    Axis.FB: (Face.L, Face.R),
    Axis.RL: (Face.U, Face.D),
}


def _eo_preserving_moves(axis: Axis) -> tuple[Move, ...]:
    """All moves that preserve EO on the given axis."""
    flipping = _FLIPPING_PER_AXIS[axis]
    out: list[Move] = []
    for f in Face:
        for t in Turn:
            if f in flipping and t != Turn.HALF:
                continue  # flipping quarter turn breaks EO
            out.append(Move(f, t))
    return tuple(out)


def find_dr_bfs(
    scramble: list[str],
    history: list[str],
    *,
    axis: str,
    max_setup_depth: int = 6,
    tail_length: int = 3,
    max_options: int = 3,
) -> dict:
    """BFS over EO-preserving moves for a trigger state, then DFS tail to DR.

    Plain BFS — no policy. Mirrors a human grinding through setups when
    intuition is empty. EO on `axis` must already be solved.
    """
    if axis not in _AXIS_LOOKUP:
        return {"error": f"axis must be UD/FB/RL; got {axis!r}"}
    ax = _AXIS_LOOKUP[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    if not is_eo_solved(state, ax):
        return {
            "error": f"EO is not yet solved on axis {axis}. "
                     f"Run find_eo_algorithmic(axis='{axis}') first."
        }

    moves = _eo_preserving_moves(ax)
    frontier: deque[tuple[State, tuple[Move, ...], Face | None]] = deque()
    frontier.append((state, (), None))
    seen: set[State] = {state}
    options: list[dict] = []

    if has_dr_within(state, ax, tail_length):
        tail = tail_to_dr(state, ax, tail_length)
        if tail is not None:
            return {
                "axis": axis,
                "found": 1,
                "options": [{
                    "moves": [str(m) for m in tail],
                    "setup_moves": [],
                    "tail_moves": [str(m) for m in tail],
                    "length": len(tail),
                }],
            }

    while frontier and len(options) < max_options:
        s, path, last_face = frontier.popleft()
        if len(path) >= max_setup_depth:
            continue
        for m in moves:
            if last_face is not None and m.face == last_face:
                continue
            child = s.apply(m)
            if child in seen:
                continue
            new_path = path + (m,)
            if has_dr_within(child, ax, tail_length):
                tail = tail_to_dr(child, ax, tail_length)
                if tail is not None:
                    full = list(new_path) + list(tail)
                    options.append({
                        "moves": [str(mm) for mm in full],
                        "setup_moves": [str(mm) for mm in new_path],
                        "tail_moves": [str(mm) for mm in tail],
                        "length": len(full),
                    })
                    if len(options) >= max_options:
                        break
                    continue
            if len(new_path) < max_setup_depth:
                seen.add(child)
                frontier.append((child, new_path, m.face))

    options.sort(key=lambda o: o["length"])
    if not options:
        return {
            "axis": axis,
            "found": 0,
            "options": [],
            "note": (
                f"No DR reachable in ≤{max_setup_depth} setup + {tail_length} tail "
                f"via BFS. Try NISS or a different EO axis."
            ),
        }
    return {"axis": axis, "found": len(options), "options": options}
