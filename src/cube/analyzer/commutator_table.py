"""Pre-built table of pure 3-cycle commutators for corners and edges.

This is the FMC-champion's "derived in their head" library: for any pure
3-cycle of corners or edges, the table maps the cycle to a short
commutator that performs exactly that cycle when applied to a solved cube.

Build is offline (one-time enumeration of ~70k commutator candidates,
~1 minute). Runtime queries are O(1) dict lookups — never a search.

Per Tronto §2.3.1, every pure 3-cycle of corners is solvable by an
8-move `[setup, interchange]` commutator. We enumerate all (setup ∈ {1-3
moves}, interchange ∈ {12 quarter turns}) pairs, identify the resulting
3-cycle when applied to SOLVED, and record the shortest commutator per
cycle.

Mirror/inverse variants are folded in: the inverse of an `(a b c)` cycle
is `(a c b)`, found by inverting the commutator's moves.
"""

from __future__ import annotations

import pickle
from collections import deque
from pathlib import Path

from cube.engine.cancellation import cancel_moves
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State

CORNER_TABLE_PATH = Path("checkpoints/corner_3cycle_table.pkl")
EDGE_TABLE_PATH = Path("checkpoints/edge_3cycle_table.pkl")


# A 3-cycle key: 3 piece indices in cycle order, canonicalized.
# Convention: sort the cycle so its smallest index is first, the direction
# is preserved. So cycle (3, 7, 1) -> (1, 3, 7) canonical. The reverse
# cycle (1, 7, 3) is stored separately as (1, 7, 3).
Cycle3 = tuple[int, int, int]


def _canonicalize_cycle(cycle: tuple[int, ...]) -> Cycle3:
    """Rotate cycle so smallest index is first. Direction preserved."""
    n = len(cycle)
    min_idx = cycle.index(min(cycle))
    return tuple(cycle[(min_idx + i) % n] for i in range(n))  # type: ignore


def _extract_pure_3cycle_corners(state: State) -> Cycle3 | None:
    """Return the corner 3-cycle if state is a pure corner 3-cycle
    (all edges solved, all non-cycled corners home AND oriented, exactly
    3 corners cycled — twists on the cycled corners are allowed since
    they're an inherent part of the cycle).
    """
    if state.ep != SOLVED.ep or state.eo != SOLVED.eo:
        return None
    moved = [i for i in range(8) if state.cp[i] != i]
    if len(moved) != 3:
        return None
    for i in range(8):
        if i not in moved and state.co[i] != 0:
            return None
    a = moved[0]
    b = state.cp[a]
    if b not in moved:
        return None
    c = state.cp[b]
    if c not in moved or c == a:
        return None
    if state.cp[c] != a:
        return None
    return _canonicalize_cycle((a, b, c))


# Full corner residual key: cycle + twists in cycle order.
# Different comms that perform the same 3-cycle of cubies can leave
# different twist patterns on the cycled corners. We need to key on both.
CornerResidualKey = tuple[int, int, int, int, int, int]  # (a, b, c, ta, tb, tc)


def _extract_corner_residual_key(state: State) -> CornerResidualKey | None:
    """Return (cycle + twists) key if state is a pure corner 3-cycle, else None.
    Canonicalized to start at the smallest slot index."""
    cycle = _extract_pure_3cycle_corners(state)
    if cycle is None:
        return None
    a, b, c = cycle
    return (a, b, c, state.co[a], state.co[b], state.co[c])


def _extract_pure_3cycle_edges(state: State) -> Cycle3 | None:
    """Same but for edges."""
    if state.cp != SOLVED.cp or state.co != SOLVED.co:
        return None
    if state.eo != SOLVED.eo:
        return None
    moved = [i for i in range(12) if state.ep[i] != i]
    if len(moved) != 3:
        return None
    a = moved[0]
    b = state.ep[a]
    if b not in moved:
        return None
    c = state.ep[b]
    if c not in moved or c == a:
        return None
    if state.ep[c] != a:
        return None
    return _canonicalize_cycle((a, b, c))


def _invert_moves(moves: list[Move]) -> list[Move]:
    return [m.inverse() for m in reversed(moves)]


def _enumerate_paths(max_len: int) -> list[list[Move]]:
    """All move sequences up to length max_len (no consecutive same-face)."""
    all_moves = [Move(f, t) for f in Face for t in Turn]
    out: list[list[Move]] = [[]]
    frontier: deque[tuple[list[Move], Face | None]] = deque([([], None)])
    while frontier:
        path, last_face = frontier.popleft()
        if len(path) >= max_len:
            continue
        for m in all_moves:
            if last_face is not None and m.face == last_face:
                continue
            new_path = path + [m]
            out.append(new_path)
            frontier.append((new_path, m.face))
    return out


def _build_corner_3cycle_table(
    max_setup_len: int = 3,
    max_interchange_len: int = 2,
    verbose: bool = True,
) -> dict[CornerResidualKey, list[str]]:
    """Build the corner 3-cycle table keyed by (cycle + twists)."""
    table: dict[CornerResidualKey, list[str]] = {}
    setups = _enumerate_paths(max_setup_len)
    interchanges = _enumerate_paths(max_interchange_len)
    interchanges = [p for p in interchanges if p]

    if verbose:
        print(f"Enumerating {len(setups)} setups × {len(interchanges)} interchanges "
              f"= {len(setups) * len(interchanges)} candidates...")

    count = 0
    for setup in setups:
        for inter in interchanges:
            comm = setup + inter + _invert_moves(setup) + _invert_moves(inter)
            comm = cancel_moves(comm)
            if not comm:
                continue
            state = SOLVED.apply_alg(comm)
            key = _extract_corner_residual_key(state)
            if key is None:
                continue
            count += 1
            comm_str = [str(m) for m in comm]
            existing = table.get(key)
            if existing is None or len(comm_str) < len(existing):
                table[key] = comm_str

    if verbose:
        print(f"  Found {count} candidates -> {len(table)} unique (cycle+twist) keys")
        if table:
            lengths = [len(v) for v in table.values()]
            print(f"  Lengths: min={min(lengths)}, max={max(lengths)}, "
                  f"avg={sum(lengths)/len(lengths):.1f}")
    return table


def _build_edge_3cycle_table(
    max_setup_len: int = 3,
    max_interchange_len: int = 2,
    verbose: bool = True,
) -> dict[Cycle3, list[str]]:
    """Edge 3-cycle table — keyed by cycle only (face-turn-only edge comms
    that produce pure 3-cycles don't introduce flip ambiguity in the same
    way; flips on cycled edges are well-determined by the cycle direction
    under our move set)."""
    table: dict[Cycle3, list[str]] = {}
    setups = _enumerate_paths(max_setup_len)
    interchanges = _enumerate_paths(max_interchange_len)
    interchanges = [p for p in interchanges if p]

    if verbose:
        print(f"Enumerating {len(setups)} setups × {len(interchanges)} interchanges "
              f"= {len(setups) * len(interchanges)} candidates...")

    count = 0
    for setup in setups:
        for inter in interchanges:
            comm = setup + inter + _invert_moves(setup) + _invert_moves(inter)
            comm = cancel_moves(comm)
            if not comm:
                continue
            state = SOLVED.apply_alg(comm)
            cycle = _extract_pure_3cycle_edges(state)
            if cycle is None:
                continue
            count += 1
            comm_str = [str(m) for m in comm]
            existing = table.get(cycle)
            if existing is None or len(comm_str) < len(existing):
                table[cycle] = comm_str

    if verbose:
        print(f"  Found {count} pure-3-cycle candidates -> {len(table)} unique cycles")
        if table:
            lengths = [len(v) for v in table.values()]
            print(f"  Lengths: min={min(lengths)}, max={max(lengths)}, "
                  f"avg={sum(lengths)/len(lengths):.1f}")
    return table


def build_and_save() -> None:
    """Build both tables and save to disk."""
    import time
    t0 = time.time()
    print("Building corner 3-cycle table...")
    corner_table = _build_corner_3cycle_table()
    print(f"  Corner table: {len(corner_table)} entries in {time.time() - t0:.1f}s")

    t0 = time.time()
    print("Building edge 3-cycle table...")
    edge_table = _build_edge_3cycle_table()
    print(f"  Edge table: {len(edge_table)} entries in {time.time() - t0:.1f}s")

    CORNER_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CORNER_TABLE_PATH.open("wb") as f:
        pickle.dump(corner_table, f)
    with EDGE_TABLE_PATH.open("wb") as f:
        pickle.dump(edge_table, f)
    print(f"Saved {CORNER_TABLE_PATH} and {EDGE_TABLE_PATH}")


# ---------------------------------------------------------------------------
# Runtime lookup API
# ---------------------------------------------------------------------------


_CORNER_TABLE: dict[Cycle3, list[str]] | None = None
_EDGE_TABLE: dict[Cycle3, list[str]] | None = None


def _ensure_loaded() -> tuple[dict[Cycle3, list[str]], dict[Cycle3, list[str]]]:
    global _CORNER_TABLE, _EDGE_TABLE
    if _CORNER_TABLE is None:
        if CORNER_TABLE_PATH.exists():
            with CORNER_TABLE_PATH.open("rb") as f:
                _CORNER_TABLE = pickle.load(f)
        else:
            _CORNER_TABLE = {}
    if _EDGE_TABLE is None:
        if EDGE_TABLE_PATH.exists():
            with EDGE_TABLE_PATH.open("rb") as f:
                _EDGE_TABLE = pickle.load(f)
        else:
            _EDGE_TABLE = {}
    return _CORNER_TABLE, _EDGE_TABLE


def lookup_corner_3cycle(key: CornerResidualKey) -> list[str] | None:
    """Lookup a corner 3-cycle commutator by full residual key (cycle+twists)."""
    corner_tab, _ = _ensure_loaded()
    return corner_tab.get(key)


def lookup_edge_3cycle(cycle: tuple[int, int, int]) -> list[str] | None:
    """Lookup an edge 3-cycle commutator by cycle key."""
    _, edge_tab = _ensure_loaded()
    key = _canonicalize_cycle(cycle)
    return edge_tab.get(key)


if __name__ == "__main__":
    build_and_save()
