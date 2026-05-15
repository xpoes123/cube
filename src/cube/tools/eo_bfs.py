"""BFS-based EO finder — algorithmic, no policy.

Humans find EO algorithmically by looking at bad edge positions and
trying setups → flip moves. This tool does the same via plain BFS over
all moves to a given depth. No transformer policy used.

Justified as "human" because humans really do this when their intuition
is empty — they slow down and methodically try sequences. The 30s+
simulated cost reflects that.
"""

from __future__ import annotations

from collections import deque

from cube.classifier.features import Axis, is_eo_solved
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State

_AXIS_LOOKUP = {a.value: a for a in Axis}
_ALL_MOVES: tuple[Move, ...] = tuple(Move(f, t) for f in Face for t in Turn)


def _move_str(m: Move) -> str:
    return str(m)


def find_eo_bfs(
    scramble: list[str],
    history: list[str],
    *,
    axis: str,
    max_depth: int = 6,
    max_options: int = 5,
) -> dict:
    """BFS for short EO sequences on `axis` from scramble+history state.

    Returns up to `max_options` shortest move sequences that reach EO.
    Plain breadth-first; no policy ranking.

    Practical depth cap: 6 (about 1-3 sec wall on CPU). Branching is
    pruned via same-face suppression so effective branching is ~14.
    """
    if axis not in _AXIS_LOOKUP:
        return {"error": f"axis must be UD/FB/RL; got {axis!r}"}
    ax = _AXIS_LOOKUP[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    if is_eo_solved(state, ax):
        return {"axis": axis, "found": 1, "options": [{"moves": [], "length": 0}]}

    # BFS with (state, path, last_face). Track best-known move count per state
    # to avoid revisiting.
    frontier: deque[tuple[State, tuple[Move, ...], Face | None]] = deque()
    frontier.append((state, (), None))
    seen: set[State] = {state}
    found: list[list[str]] = []
    best_len = max_depth + 1

    while frontier:
        s, path, last_face = frontier.popleft()
        if len(path) >= best_len:
            break
        for m in _ALL_MOVES:
            if last_face is not None and m.face == last_face:
                continue
            child = s.apply(m)
            if child in seen:
                continue
            new_path = path + (m,)
            if is_eo_solved(child, ax):
                found.append([_move_str(mm) for mm in new_path])
                best_len = len(new_path)
                if len(found) >= max_options:
                    return {
                        "axis": axis,
                        "found": len(found),
                        "options": [{"moves": p, "length": len(p)} for p in found],
                    }
                continue
            if len(new_path) < max_depth:
                seen.add(child)
                frontier.append((child, new_path, m.face))

    if not found:
        return {
            "axis": axis,
            "found": 0,
            "options": [],
            "note": f"No EO ({axis}) found within depth={max_depth}. Try NISS.",
        }
    return {
        "axis": axis,
        "found": len(found),
        "options": [{"moves": p, "length": len(p)} for p in found],
    }
