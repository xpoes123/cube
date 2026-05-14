"""Leave-slice finish: solve everything except the DR slice via half-turns.

The leave-slice technique is the canonical FMC HTR-finish: instead of
solving everything via half-turns only (often 9-15 moves), solve
*everything except the DR slice* in fewer moves (5-9 typically), then
patch the resulting slice residual with a slice quarter (M / E / S),
which can often be cancelled into the surrounding skeleton.

For UD-axis DR, the "DR slice" is the E-slice (edges FR, FL, BL, BR at
positions 8-11). A leave-slice-solved state has:
  - cp = identity (all corners home)
  - ep[0..7] = identity (U-layer and D-layer edges home)
  - ep[8..11] = some permutation of {8,9,10,11} (E-slice edges anywhere
    within E-slice positions)

The PDB is built via multi-source BFS from all such target states,
expanding via the 6 half-turn moves.
"""

from __future__ import annotations

from collections import deque
from functools import lru_cache

from cube.classifier.htr import htr_corner_perms, htr_edge_perms
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED, State


_HALF_TURN_MOVES = tuple(Move(f, Turn.HALF) for f in Face)


def _leave_slice_targets_ud() -> list[tuple[int, ...]]:
    """All HTR-reachable edge permutations with ep[0..7] = identity.

    These are the 'leave-slice solved' (UD-axis) edge perms — the U/D
    layer edges are home, the E-slice edges are anywhere in E-slice.
    """
    identity_prefix = tuple(range(8))
    return [
        ep for ep in htr_edge_perms()
        if ep[:8] == identity_prefix
    ]


@lru_cache(maxsize=1)
def leave_slice_pdb_ud() -> dict[
    tuple[tuple[int, ...], tuple[int, ...]],
    tuple[int, Move | None],
]:
    """Multi-source BFS PDB: distance to nearest leave-slice-solved state.

    Key: (cp, ep) tuple. Value: (distance, parent_move_to_get_here).
    Search expands by 6 half-turn moves.

    Build time ~10s; cached afterward.
    """
    targets = _leave_slice_targets_ud()
    # Identity corner perm.
    target_cp = SOLVED.cp

    pdb: dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[int, Move | None]] = {}
    frontier: deque[tuple[State, int]] = deque()

    # Multi-source: every (target_cp, target_ep) starts at distance 0.
    for target_ep in targets:
        target_state = State(
            cp=target_cp, co=SOLVED.co,
            ep=target_ep, eo=SOLVED.eo,
            eo_fb=SOLVED.eo_fb, eo_rl=SOLVED.eo_rl,
        )
        key = (target_state.cp, target_state.ep)
        if key not in pdb:
            pdb[key] = (0, None)
            frontier.append((target_state, 0))

    while frontier:
        s, d = frontier.popleft()
        for m in _HALF_TURN_MOVES:
            child = s.apply(m)
            key = (child.cp, child.ep)
            if key in pdb:
                continue
            pdb[key] = (d + 1, m)
            frontier.append((child, d + 1))

    return pdb


def leave_slice_distance(state: State) -> int | None:
    """Min half-turn moves to leave-slice-solved, or None if unreachable."""
    pdb = leave_slice_pdb_ud()
    entry = pdb.get((state.cp, state.ep))
    return entry[0] if entry else None


def leave_slice_solve(state: State) -> list[Move] | None:
    """Return shortest half-turn sequence taking `state` to leave-slice-solved.

    Returns None if state.cp/ep aren't in HTR subgroups (not reachable
    via half-turns from a leave-slice target).
    """
    pdb = leave_slice_pdb_ud()
    if (state.cp, state.ep) not in pdb:
        return None
    solution: list[Move] = []
    cur = state
    # Walk parent-pointers until distance is 0 (we're at a target).
    while True:
        entry = pdb.get((cur.cp, cur.ep))
        if entry is None:
            return None
        d, m = entry
        if d == 0:
            return solution
        if m is None:
            return None
        # m is the move that brought us here from the parent.
        # Apply m to undo (half-turns are self-inverse), reaching the parent.
        solution.append(m)
        cur = cur.apply(m)


# E-slice positions for UD axis.
_E_SLICE_POSITIONS = (8, 9, 10, 11)


def slice_residual_ud(state: State) -> tuple[int, ...]:
    """The current E-slice permutation, as a 4-tuple over positions 8-11.

    Returns the cubies at positions 8..11 in order. If the result is
    (8, 9, 10, 11), the slice is solved.
    """
    return tuple(state.ep[i] for i in _E_SLICE_POSITIONS)


# Slice-quarter equivalents in the 18-move alphabet.
# M = R L' (in face moves). M slice goes "down" (away from R-axis CW).
# Standard convention: M follows the L face direction.
_M_QUARTER: tuple[Move, ...] = (
    Move(Face.R, Turn.CCW), Move(Face.L, Turn.CW),
)
_M_PRIME_QUARTER: tuple[Move, ...] = (
    Move(Face.R, Turn.CW), Move(Face.L, Turn.CCW),
)
_M_HALF: tuple[Move, ...] = (
    Move(Face.R, Turn.HALF), Move(Face.L, Turn.HALF),
)


def slice_fix_for_residual(state: State) -> tuple[Move, ...] | None:
    """Given a leave-slice-solved state with E-slice residual, return
    the shortest slice quarter/half sequence that solves the slice.

    Returns None if no single M / M' / M2 fixes it (other cases need
    insertion, handled in Milestone 3).
    """
    if slice_residual_ud(state) == _E_SLICE_POSITIONS:
        return ()
    for fix in (_M_QUARTER, _M_PRIME_QUARTER, _M_HALF):
        after = state
        for m in fix:
            after = after.apply(m)
        if slice_residual_ud(after) == _E_SLICE_POSITIONS and after.cp == SOLVED.cp:
            # Also need to verify the rest is preserved — cp shouldn't be disturbed.
            if after == SOLVED:
                return fix
    return None
