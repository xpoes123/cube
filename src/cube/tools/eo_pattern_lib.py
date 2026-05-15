"""Memorized EO pattern library.

For every distinct bad-edge-slot pattern we've encountered (per axis),
the library stores an optimal-length move sequence to reach EO. At
runtime, the agent calls `eo_pattern_lookup(state, axis)` — O(1) dict
lookup, no search. Mirrors what a human FMC champion does: recognize
the configuration, recall the fix.

Pattern key: (axis_name, frozenset of bad-edge slot names like "UF"/"DR").
Value: list of WCA-notation moves.

Correctness: the EO update rule is `eo'[s] = eo[s] XOR flip_mask[face][s]`,
which depends only on the eo array, not on cp/ep/co. So two states with
the same eo array (i.e., same bad-edge-slot pattern) yield identical
move sequences from any BFS that targets EO.
"""

from __future__ import annotations

import pickle
from pathlib import Path

from cube.classifier.features import Axis, eo_count, is_eo_solved
from cube.engine.notation import parse_alg
from cube.engine.state import EDGE_NAMES, SOLVED, State
from cube.tools.eo_bfs import find_eo_bfs

_AXIS_LOOKUP = {a.value: a for a in Axis}
LIBRARY_PATH = Path("checkpoints/eo_pattern_library.pkl")

# (axis_name, frozenset_of_slot_names) -> optimal_moves
EOLibrary = dict[tuple[str, frozenset[str]], list[str]]

_LIBRARY: EOLibrary | None = None


def _bad_edge_slots(state: State, axis: Axis) -> frozenset[str]:
    if axis == Axis.UD:
        arr = state.eo
    elif axis == Axis.FB:
        arr = state.eo_fb
    elif axis == Axis.RL:
        arr = state.eo_rl
    else:
        return frozenset()
    return frozenset(EDGE_NAMES[i] for i, v in enumerate(arr) if v)


def _ensure_loaded() -> EOLibrary:
    global _LIBRARY
    if _LIBRARY is not None:
        return _LIBRARY
    if LIBRARY_PATH.exists():
        try:
            with LIBRARY_PATH.open("rb") as f:
                _LIBRARY = pickle.load(f)
        except (pickle.UnpicklingError, OSError):
            _LIBRARY = {}
    else:
        _LIBRARY = {}
    return _LIBRARY


def eo_pattern_lookup(
    scramble: list[str],
    history: list[str],
    *,
    axis: str,
) -> dict:
    """Recall a memorized EO sequence for the current bad-edge-slot pattern.

    Returns:
      - if hit: {'found': 1, 'options': [{'moves': [...], 'length': N}],
                 'pattern_size': K, 'cached': True}
      - if miss: {'found': 0, 'options': [], 'pattern_size': K, 'cached': False,
                  'note': 'pattern not memorized; try find_eo_algorithmic'}
    """
    if axis not in _AXIS_LOOKUP:
        return {"error": f"axis must be UD/FB/RL; got {axis!r}"}
    ax = _AXIS_LOOKUP[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    if is_eo_solved(state, ax):
        return {
            "found": 1,
            "options": [{"moves": [], "length": 0}],
            "pattern_size": 0,
            "cached": True,
            "note": "EO already solved on this axis.",
        }

    slot_pattern = _bad_edge_slots(state, ax)
    key = (axis, slot_pattern)
    library = _ensure_loaded()

    if key in library:
        moves = library[key]
        return {
            "found": 1,
            "options": [{"moves": list(moves), "length": len(moves)}],
            "pattern_size": len(slot_pattern),
            "cached": True,
            "note": f"Recognized pattern ({len(slot_pattern)} bad edges) — playing memorized {len(moves)}-move EO.",
        }
    return {
        "found": 0,
        "options": [],
        "pattern_size": len(slot_pattern),
        "cached": False,
        "note": (
            f"Pattern not in memorized library ({len(slot_pattern)} bad edges "
            f"on axis {axis}). Fall back to find_eo_algorithmic."
        ),
    }


# ---------------------------------------------------------------------------
# Library builder
# ---------------------------------------------------------------------------


def build_library_from_states(
    states: list[State],
    *,
    max_depth: int = 6,
    verbose: bool = True,
) -> EOLibrary:
    """For each (state, axis) pair, find the optimal EO and add to library.

    Dedupes by (axis, bad_slot_pattern) so a pattern seen via multiple
    states gets BFS'd only once.
    """
    import time
    library: EOLibrary = {}
    n_seen = 0
    n_added = 0
    n_skipped_solved = 0
    t0 = time.time()
    for i, state in enumerate(states, 1):
        for axis_name in ("UD", "FB", "RL"):
            ax = _AXIS_LOOKUP[axis_name]
            if is_eo_solved(state, ax):
                n_skipped_solved += 1
                continue
            slots = _bad_edge_slots(state, ax)
            key = (axis_name, slots)
            n_seen += 1
            if key in library:
                continue
            # BFS to find optimal EO. We don't have the scramble that
            # produced this state, so we directly feed the state via a
            # tiny inline BFS that mirrors find_eo_bfs.
            res = _bfs_eo_from_state(state, ax, max_depth=max_depth)
            if res is not None:
                library[key] = res
                n_added += 1
        if verbose and i % 100 == 0:
            print(
                f"  scramble {i}/{len(states)}: lib={len(library)}, "
                f"seen={n_seen}, added={n_added}, "
                f"elapsed={time.time() - t0:.1f}s"
            )
    if verbose:
        print(
            f"Done: lib={len(library)}, seen={n_seen}, added={n_added}, "
            f"skipped_solved={n_skipped_solved}, elapsed={time.time() - t0:.1f}s"
        )
    return library


def _bfs_eo_from_state(state: State, axis: Axis, *, max_depth: int = 6) -> list[str] | None:
    """Tight BFS for EO on `axis` from `state`. Returns shortest move
    sequence as strings, or None if unreachable in max_depth."""
    from collections import deque
    from cube.engine.moves import Face, Move, Turn

    ALL_MOVES = tuple(Move(f, t) for f in Face for t in Turn)

    if is_eo_solved(state, axis):
        return []
    frontier: deque[tuple[State, tuple[Move, ...], Face | None]] = deque()
    frontier.append((state, (), None))
    seen: set[State] = {state}
    while frontier:
        s, path, last_face = frontier.popleft()
        if len(path) >= max_depth:
            continue
        for m in ALL_MOVES:
            if last_face is not None and m.face == last_face:
                continue
            child = s.apply(m)
            if child in seen:
                continue
            new_path = path + (m,)
            if is_eo_solved(child, axis):
                return [str(mm) for mm in new_path]
            if len(new_path) < max_depth:
                seen.add(child)
                frontier.append((child, new_path, m.face))
    return None


def save_library(library: EOLibrary, path: Path = LIBRARY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(library, f)


def load_library(path: Path = LIBRARY_PATH) -> EOLibrary:
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return pickle.load(f)


# ---------------------------------------------------------------------------
# Fast complete builder via EO-state-space forward BFS
# ---------------------------------------------------------------------------


def _seed_state_with_eo(axis: Axis, eo_tuple: tuple[int, ...]) -> State:
    """Build a synthetic state where the chosen axis's eo array equals
    `eo_tuple` and the others are SOLVED. EO transitions depend only on
    the relevant eo array, so the resulting state behaves correctly
    under any move sequence's effect on that axis's EO."""
    if axis == Axis.UD:
        return State(cp=SOLVED.cp, co=SOLVED.co, ep=SOLVED.ep,
                     eo=eo_tuple, eo_fb=SOLVED.eo_fb, eo_rl=SOLVED.eo_rl)
    if axis == Axis.FB:
        return State(cp=SOLVED.cp, co=SOLVED.co, ep=SOLVED.ep,
                     eo=SOLVED.eo, eo_fb=eo_tuple, eo_rl=SOLVED.eo_rl)
    return State(cp=SOLVED.cp, co=SOLVED.co, ep=SOLVED.ep,
                 eo=SOLVED.eo, eo_fb=SOLVED.eo_fb, eo_rl=eo_tuple)


def _get_eo_array(state: State, axis: Axis) -> tuple[int, ...]:
    if axis == Axis.UD:
        return state.eo
    if axis == Axis.FB:
        return state.eo_fb
    return state.eo_rl


def build_full_library_via_eo_bfs(*, max_depth: int = 8, verbose: bool = True) -> EOLibrary:
    """Complete EO library via per-axis forward BFS over the 2048-state
    EO-array space. Linear in number of reachable patterns × moves per
    state; should finish in well under a minute.

    Strategy: from SOLVED (eo=0), explore all reachable eo arrays via
    moves. Record the path of moves taken to reach each eo state. The
    inverse of that path is the optimal solver from that state.
    """
    from collections import deque
    from cube.engine.moves import Face, Move, Turn
    import time

    ALL_MOVES = tuple(Move(f, t) for f in Face for t in Turn)
    library: EOLibrary = {}
    t0 = time.time()

    for axis in [Axis.UD, Axis.FB, Axis.RL]:
        axis_name = axis.value
        zero_state = SOLVED
        zero_eo = _get_eo_array(zero_state, axis)
        # eo_array_tuple -> path of Move objects from SOLVED to that array
        path_to_state: dict[tuple[int, ...], tuple[Move, ...]] = {zero_eo: ()}
        # parallel: for the synthetic state at each eo array
        state_for_eo: dict[tuple[int, ...], State] = {zero_eo: zero_state}
        frontier: deque[tuple[int, ...]] = deque([zero_eo])
        # The library key for SOLVED is the empty frozenset — already-solved.
        library[(axis_name, frozenset())] = []

        explored = 0
        while frontier:
            cur_eo = frontier.popleft()
            cur_path = path_to_state[cur_eo]
            if len(cur_path) >= max_depth:
                continue
            cur_state = state_for_eo[cur_eo]
            last_face = cur_path[-1].face if cur_path else None
            for m in ALL_MOVES:
                if last_face is not None and m.face == last_face:
                    continue
                child = cur_state.apply(m)
                child_eo = _get_eo_array(child, axis)
                if child_eo in path_to_state:
                    continue
                new_path = cur_path + (m,)
                path_to_state[child_eo] = new_path
                state_for_eo[child_eo] = child
                # The solver for THIS eo is the inverse of the forward path.
                solver = tuple(reversed([_inverse_move(mm) for mm in new_path]))
                slots = frozenset(EDGE_NAMES[i] for i, v in enumerate(child_eo) if v)
                library[(axis_name, slots)] = [str(mm) for mm in solver]
                frontier.append(child_eo)
                explored += 1
        if verbose:
            print(f"  axis {axis_name}: {explored} reachable EO states, "
                  f"library now {len(library)} entries, {time.time() - t0:.1f}s")
    return library


def _inverse_move(move):
    from cube.engine.moves import Move, Turn
    inv_turn = {Turn.CW: Turn.CCW, Turn.HALF: Turn.HALF, Turn.CCW: Turn.CW}[move.turn]
    return Move(move.face, inv_turn)
