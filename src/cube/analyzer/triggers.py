"""DR trigger search: short tail-sequences from a state to DR.

The human FMC method recognizes a small library of named triggers (F R F,
R' F R F', B U' B' R, etc.) — fixed move sequences that complete DR from
specific intermediate patterns.

For an algorithm, hardcoding that library misses cases the policy can
find that humans don't have memorized templates for. Instead, we use a
generic "DR within K moves" check: at any candidate state, run a small
DFS to find the shortest tail-sequence (≤K moves) that reaches DR.

This subsumes all human templates AND any other short DR completion.
K is small (2-4 typically), so per-call cost is bounded (18^K).

Use case: as a beam-search target predicate. The beam searches for
states from which DR is K moves away. Total DR path = beam_depth + tail.
"""

from __future__ import annotations

from cube.classifier.features import Axis, is_dr
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import State

# Pre-build the list of all 18 moves once.
_ALL_MOVES: tuple[Move, ...] = tuple(
    Move(face, turn) for face in Face for turn in Turn
)


def tail_to_dr(
    state: State,
    axis: Axis,
    max_tail: int,
) -> tuple[Move, ...] | None:
    """Shortest tail-sequence (length ≤ max_tail) from `state` to DR.

    Returns the moves as a tuple (possibly empty if state already in DR),
    or None if no path of length ≤ max_tail reaches DR.

    Implementation: iterative-deepening DFS. Total work is O(18^max_tail)
    in the worst case but usually much smaller because hits cut off
    branches early.
    """
    if is_dr(state, axis):
        return ()
    for target_depth in range(1, max_tail + 1):
        path = _dfs(state, axis, target_depth)
        if path is not None:
            return path
    return None


def _dfs(state: State, axis: Axis, depth: int) -> tuple[Move, ...] | None:
    if depth == 0:
        return () if is_dr(state, axis) else None
    for m in _ALL_MOVES:
        child = state.apply(m)
        if depth == 1:
            if is_dr(child, axis):
                return (m,)
        else:
            rest = _dfs(child, axis, depth - 1)
            if rest is not None:
                return (m,) + rest
    return None


def has_dr_within(state: State, axis: Axis, max_tail: int) -> bool:
    """True iff DR is reachable from `state` within `max_tail` moves."""
    return tail_to_dr(state, axis, max_tail) is not None
