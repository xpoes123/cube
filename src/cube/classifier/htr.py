"""HTR (Half-Turn Reduction) predicate and subgroup enumeration.

A state is in HTR iff it is reachable from SOLVED using only half-turn moves
(group ⟨U², D², R², L², F², B²⟩). Equivalently, the state can be solved
using only half-turns.

This is a STRUCTURAL property of the state's (cp, ep) tuples — CO and EO
are necessarily zero in HTR, and slices are necessarily in slice.

Strategy: precompute the set of HTR-reachable corner permutations and edge
permutations via BFS from SOLVED. Both are small (corner subgroup ≤ ~200,
edge subgroup ≤ ~5000), so lookup is O(1).

The HTR subgroup also drives DR subset classification (each HTR coset of
the post-DR corner state is one canonical subset like 4a1 / 2c3 / 4b2).
"""

from __future__ import annotations

from collections import deque
from functools import lru_cache

from cube.classifier.features import Axis, co_count, eo_count
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED, State


_HALF_TURN_MOVES = tuple(Move(f, Turn.HALF) for f in Face)
_HALF_TURN_FACES_AXIS_AWARE = {
    Axis.UD: (Face.U, Face.D),
    Axis.FB: (Face.F, Face.B),
    Axis.RL: (Face.R, Face.L),
}


@lru_cache(maxsize=1)
def htr_corner_perms() -> frozenset[tuple[int, ...]]:
    """All corner permutations reachable from SOLVED via half-turn moves.

    Computed via BFS in the corner-permutation projection: only cp changes
    are tracked. Cached after the first call.
    """
    seen: set[tuple[int, ...]] = {SOLVED.cp}
    frontier: deque[State] = deque([SOLVED])
    while frontier:
        s = frontier.popleft()
        for m in _HALF_TURN_MOVES:
            child = s.apply(m)
            if child.cp not in seen:
                seen.add(child.cp)
                frontier.append(child)
    return frozenset(seen)


@lru_cache(maxsize=1)
def htr_edge_perms() -> frozenset[tuple[int, ...]]:
    """All edge permutations reachable from SOLVED via half-turn moves.

    Computed via BFS in the edge-permutation projection: only ep changes
    are tracked. Cached after the first call.
    """
    seen: set[tuple[int, ...]] = {SOLVED.ep}
    frontier: deque[State] = deque([SOLVED])
    while frontier:
        s = frontier.popleft()
        for m in _HALF_TURN_MOVES:
            child = s.apply(m)
            if child.ep not in seen:
                seen.add(child.ep)
                frontier.append(child)
    return frozenset(seen)


def is_htr(state: State) -> bool:
    """True iff `state` is in the HTR subgroup.

    Five conditions, all derived from "reachable from SOLVED via half turns":
      1. EO solved on all 3 axes (half turns preserve EO).
      2. CO solved on all 3 axes (half turns preserve CO).
      3. Corner permutation in HTR-reachable corner-perm set.
      4. Edge permutation in HTR-reachable edge-perm set.

    Slice-in-slice on all axes is implied by (4) — half turns preserve
    slice-membership for every slice axis, so any edge perm reachable
    from SOLVED via half turns has every slice in its own slice.
    """
    # Cheap rejections first.
    if eo_count(state, Axis.UD) != 0:
        return False
    if eo_count(state, Axis.FB) != 0:
        return False
    if eo_count(state, Axis.RL) != 0:
        return False
    if co_count(state, Axis.UD) != 0:
        return False
    if co_count(state, Axis.FB) != 0:
        return False
    if co_count(state, Axis.RL) != 0:
        return False
    if state.cp not in htr_corner_perms():
        return False
    if state.ep not in htr_edge_perms():
        return False
    return True


# DR-group move set (for online BFS from DR → HTR). DR on UD axis = the
# group ⟨U, D, R², L², F², B²⟩. By the axis-CO closure proved by multi-axis
# tests, applying these moves to a DR-UD state keeps it in DR.
def dr_group_moves(axis: Axis) -> tuple[Move, ...]:
    """Move set that preserves DR on the given axis."""
    if axis == Axis.UD:
        on_axis = (Face.U, Face.D)
        off_axis = (Face.R, Face.L, Face.F, Face.B)
    elif axis == Axis.FB:
        on_axis = (Face.F, Face.B)
        off_axis = (Face.U, Face.D, Face.R, Face.L)
    elif axis == Axis.RL:
        on_axis = (Face.R, Face.L)
        off_axis = (Face.U, Face.D, Face.F, Face.B)
    else:
        raise ValueError(f"unknown axis: {axis}")
    moves: list[Move] = []
    for face in on_axis:
        for turn in Turn:
            moves.append(Move(face, turn))
    for face in off_axis:
        moves.append(Move(face, Turn.HALF))
    return tuple(moves)


@lru_cache(maxsize=1)
def dr_corner_perms_ud() -> frozenset[tuple[int, ...]]:
    """All corner permutations reachable from SOLVED via UD-axis DR moves.

    DR moves on UD = ⟨U, D, R², L², F², B²⟩. The corner-perm projection of
    this group's action on SOLVED.
    """
    moves = dr_group_moves(Axis.UD)
    seen: set[tuple[int, ...]] = {SOLVED.cp}
    frontier: deque[State] = deque([SOLVED])
    while frontier:
        s = frontier.popleft()
        for m in moves:
            child = s.apply(m)
            if child.cp not in seen:
                seen.add(child.cp)
                frontier.append(child)
    return frozenset(seen)


@lru_cache(maxsize=1)
def _htr_corner_subset_orbits() -> dict[tuple[int, ...], frozenset[tuple[int, ...]]]:
    """Partition DR-reachable corner perms into HTR-coset equivalence classes.

    Each coset is one canonical "DR subset" (4a1, 4b2, 2c3, ...). Returns a
    mapping from canonical representative (lex-min in coset) → set of all
    members of that coset.

    Computed by left-multiplying each DR-corner-perm by every HTR-corner-perm
    and grouping members of the same orbit.
    """
    htr_cps = htr_corner_perms()
    dr_cps = dr_corner_perms_ud()

    # For each DR-reachable cp, build its HTR-orbit (the set of cps you get
    # by composing with any HTR-corner-perm). The orbit's lex-min is the
    # canonical representative.
    cp_to_canonical: dict[tuple[int, ...], tuple[int, ...]] = {}
    canonical_to_orbit: dict[tuple[int, ...], set[tuple[int, ...]]] = {}

    for cp in dr_cps:
        if cp in cp_to_canonical:
            continue
        # Build orbit: apply each htr corner perm h to cp (composition cp ∘ h).
        # Permutation composition: (cp ∘ h)[i] = cp[h[i]].
        orbit: set[tuple[int, ...]] = set()
        for h in htr_cps:
            composed = tuple(cp[h[i]] for i in range(8))
            orbit.add(composed)
        canonical = min(orbit)
        for member in orbit:
            cp_to_canonical[member] = canonical
        canonical_to_orbit[canonical] = orbit

    return {k: frozenset(v) for k, v in canonical_to_orbit.items()}


def dr_subset_canonical(state: State) -> tuple[int, ...] | None:
    """Canonical representative of the state's HTR-coset (post-DR corner perm).

    Returns None if `state.cp` is not in the DR-reachable corner-perm set
    (e.g. state is not actually in a DR position on the UD axis).

    Two states have the same canonical iff they're in the same DR subset
    (= the canonical FMC notion of 4a1 vs 4b2 vs 2c3 etc.).
    """
    orbits = _htr_corner_subset_orbits()
    htr_cps = htr_corner_perms()
    cp = state.cp
    # Walk the orbit to find canonical (avoids dict lookup if not pre-cached).
    orbit_min = cp
    for h in htr_cps:
        composed = tuple(cp[h[i]] for i in range(8))
        if composed < orbit_min:
            orbit_min = composed
    return orbit_min if orbit_min in orbits else None


@lru_cache(maxsize=1)
def _dr_corner_to_htr_distance_table() -> dict[tuple[int, ...], int]:
    """For every UD-DR-reachable corner perm, the minimum corner-perm moves
    to reach any HTR corner perm.

    Built via single reverse-BFS from all HTR-corner-perms expanding by the
    DR-group corner-perm action. All 40320 entries computed in one pass.

    Subset distance is identical across the whole HTR-coset of a corner
    state (since every member of a coset is 0 moves from its own HTR-coset
    representative under HTR action — but we measure DR-group distance, not
    HTR-group distance). So all 96 cps within one coset get the same
    distance.
    """
    moves = dr_group_moves(Axis.UD)
    # We need an apply function that operates on cp alone, so we cache one
    # forward-application per move starting from each cp.
    distance: dict[tuple[int, ...], int] = {cp: 0 for cp in htr_corner_perms()}
    frontier: deque[tuple[tuple[int, ...], int]] = deque(
        (cp, 0) for cp in htr_corner_perms()
    )

    # We need to apply move m to a state whose cp is `cp` and get the
    # resulting cp. Since cp+ep are independent under cube moves on
    # corners only when state is "cp-only" we synthesize a state.
    # Cache (cp, move) -> new_cp.
    cp_move_cache: dict[tuple[tuple[int, ...], Move], tuple[int, ...]] = {}
    solved_eo = (0,) * 12

    def apply_cp(cp: tuple[int, ...], m: Move) -> tuple[int, ...]:
        key = (cp, m)
        cached = cp_move_cache.get(key)
        if cached is not None:
            return cached
        s = State(
            cp=cp, co=(0,) * 8, ep=SOLVED.ep,
            eo=solved_eo, eo_fb=solved_eo, eo_rl=solved_eo,
        )
        new_cp = s.apply(m).cp
        cp_move_cache[key] = new_cp
        return new_cp

    while frontier:
        cp, d = frontier.popleft()
        for m in moves:
            new_cp = apply_cp(cp, m)
            if new_cp in distance:
                continue
            distance[new_cp] = d + 1
            frontier.append((new_cp, d + 1))
    return distance


def dr_distance_to_htr(state: State, axis: Axis = Axis.UD) -> int | None:
    """Minimum DR-group corner-permutation moves to reach any HTR corner perm.

    Returns None if `state.cp` is not in the DR-reachable corner-perm set
    (e.g., state is not actually post-DR on the requested axis).

    Implementation: O(1) lookup against the precomputed distance table.
    First call materializes the table (~1-2s for UD axis).

    Caveat: this measures *corner-perm* distance only. The full state may
    require more moves to actually reach HTR (e.g., edges still need
    arranging). But corner distance is the dominant signal for DR subset
    quality, and that's what FMC solvers use.
    """
    if axis != Axis.UD:
        # Multi-axis subset tables are a follow-up; for now, only UD.
        return None
    return _dr_corner_to_htr_distance_table().get(state.cp)


# ---------- HTR pattern database (full HTR-group enumeration) ----------


@lru_cache(maxsize=1)
def htr_pdb() -> dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[int, Move | None]]:
    """Pattern database: for every HTR-reachable state, store
    (distance_to_SOLVED, parent_move).

    Key: (cp, ep) tuple. CO and EO are always zero in HTR.
    Value: (distance, move). `move` is the half-turn applied at the
    parent that produced this state in the BFS expansion.

    First call BFS's the full HTR subgroup (663,552 states). ~20s.
    Cached after that.
    """
    pdb: dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[int, Move | None]] = {}
    pdb[(SOLVED.cp, SOLVED.ep)] = (0, None)
    frontier: deque[tuple[State, int]] = deque([(SOLVED, 0)])
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


def htr_distance(state: State) -> int | None:
    """Exact moves to SOLVED for an HTR-state, or None if not in HTR."""
    if not is_htr(state):
        return None
    pdb = htr_pdb()
    entry = pdb.get((state.cp, state.ep))
    return entry[0] if entry else None


def htr_solve(state: State) -> list[Move] | None:
    """Optimal half-turn solve from an HTR-state to SOLVED.

    Returns None if state is not in HTR.

    Algorithm: from `state`, repeatedly find the parent move that brought
    BFS to this state, apply it (self-inverse for half-turns), until
    SOLVED is reached.
    """
    if not is_htr(state):
        return None
    pdb = htr_pdb()
    solution: list[Move] = []
    cur = state
    while cur != SOLVED:
        entry = pdb.get((cur.cp, cur.ep))
        if entry is None or entry[1] is None:
            return None
        _, m = entry
        solution.append(m)
        cur = cur.apply(m)  # half turns are self-inverse
    return solution
