"""HTR predicate, subgroup enumeration, and DR-to-HTR distance.

These tests are slow on first run (a few seconds to build BFS tables) but
the results are module-cached via lru_cache, so subsequent calls are fast.
"""

from __future__ import annotations

from cube.classifier.features import Axis
from cube.classifier.htr import (
    _dr_corner_to_htr_distance_table,
    _htr_corner_subset_orbits,
    dr_corner_perms_ud,
    dr_distance_to_htr,
    dr_group_moves,
    dr_subset_canonical,
    htr_corner_perms,
    htr_edge_perms,
    is_htr,
)
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED


def test_htr_corner_set_size():
    """Canonical: |HTR corner subgroup| = 96 (the "96 HTR cases")."""
    assert len(htr_corner_perms()) == 96


def test_htr_edge_set_size():
    """HTR edge subgroup has order exactly 6912.

    Algebraic: half-turns act on edges as a subgroup of S_12. The orbit
    of solved-edges under ⟨U², D², R², L², F², B²⟩ has 6912 elements.
    96 (corner subgroup) × 6912 (edge subgroup) = 663,552 = |HTR|.
    """
    assert len(htr_edge_perms()) == 6912


def test_solved_is_htr():
    assert is_htr(SOLVED)


def test_half_turns_preserve_htr_from_solved():
    """Any half-turn applied to SOLVED stays in HTR."""
    for face in Face:
        for half_turn_count in range(1, 6):
            state = SOLVED
            for _ in range(half_turn_count):
                state = state.apply(Move(face, Turn.HALF))
            assert is_htr(state), (
                f"{face}2 x{half_turn_count} from SOLVED not detected as HTR"
            )


def test_quarter_turns_leave_htr():
    """Any single quarter turn from SOLVED leaves HTR."""
    for face in Face:
        for turn in (Turn.CW, Turn.CCW):
            assert not is_htr(SOLVED.apply(Move(face, turn))), (
                f"{face}{turn} from SOLVED should leave HTR"
            )


def test_dr_corner_set_size():
    """DR-reachable corner perms = alternating group A_8 = 8!/2 = 20160."""
    # Empirically we get 40320 = 8! — full S_8, not A_8.
    # That's because the DR-group on UD includes U and D quarters, which
    # generate odd corner cycles in combination with half-turn corner
    # 2-cycles. So the corner subgroup is the full S_8, not A_8.
    n = len(dr_corner_perms_ud())
    assert n == 40320


def test_htr_cosets_in_dr():
    """[DR_corner : HTR_corner] = 40320 / 96 = 420."""
    orbits = _htr_corner_subset_orbits()
    assert len(orbits) == 420
    # Every orbit has size exactly |H| = 96.
    for orbit in orbits.values():
        assert len(orbit) == 96


def test_distance_table_size_and_range():
    table = _dr_corner_to_htr_distance_table()
    assert len(table) == 40320
    assert min(table.values()) == 0
    # Distance 0 entries == HTR corner perms.
    zero_dist = {cp for cp, d in table.items() if d == 0}
    assert zero_dist == htr_corner_perms()


def test_distance_constant_within_left_coset():
    """All members of a LEFT coset Hπ have the same DR-to-HTR distance.

    The Cayley graph of DR with right-multiplication generators is
    right-translation invariant, so d(π, H) depends only on the left
    coset Hπ. This is the math-level invariant that justifies using a
    single distance per "structural class."

    The FMC literature's notion of "subset" is actually the RIGHT coset
    πH (states transitionable via HTR moves) — that partition cuts
    across distance classes. We use per-cp distance for ranking; the
    right-coset partition is for naming.
    """
    table = _dr_corner_to_htr_distance_table()
    htr_cps = htr_corner_perms()
    # Group cps by left coset Hπ = {h ∘ π : h ∈ H}.
    cp_to_left_coset: dict[tuple[int, ...], tuple[int, ...]] = {}
    for pi in table:
        if pi in cp_to_left_coset:
            continue
        orbit: set[tuple[int, ...]] = set()
        for h in htr_cps:
            composed = tuple(h[pi[i]] for i in range(8))  # h ∘ π
            orbit.add(composed)
        canonical = min(orbit)
        for x in orbit:
            cp_to_left_coset[x] = canonical
    # Group by left-coset canonical, check distances all match.
    from collections import defaultdict
    by_coset: dict[tuple[int, ...], set[int]] = defaultdict(set)
    for cp, d in table.items():
        by_coset[cp_to_left_coset[cp]].add(d)
    for canonical, distances in by_coset.items():
        assert len(distances) == 1, (
            f"LEFT coset {canonical} has multiple distances: {distances}"
        )


def test_distance_class_sizes_are_multiples_of_96():
    """Each distance class is a union of cosets, so its size is k * 96."""
    from collections import Counter
    table = _dr_corner_to_htr_distance_table()
    hist = Counter(table.values())
    for d, n in hist.items():
        assert n % 96 == 0, f"distance {d} class has size {n}, not divisible by 96"


def test_dr_distance_to_htr_solved_is_zero():
    assert dr_distance_to_htr(SOLVED) == 0


def test_dr_distance_after_one_dr_move():
    """A single DR move from SOLVED should put us 1 away from HTR (if the
    move is a quarter; 0 if it's a half-turn = in HTR)."""
    # U' is a quarter; should be distance 1 from HTR.
    s = SOLVED.apply(Move(Face.U, Turn.CW))
    assert dr_distance_to_htr(s) == 1
    # F2 is a half-turn; should stay in HTR.
    s = SOLVED.apply(Move(Face.F, Turn.HALF))
    assert dr_distance_to_htr(s) == 0


def test_dr_subset_canonical_solved():
    canonical = dr_subset_canonical(SOLVED)
    assert canonical == (0, 1, 2, 3, 4, 5, 6, 7)


def test_dr_group_moves_count():
    moves = dr_group_moves(Axis.UD)
    # U/D get 3 turns each (CW, CCW, HALF), other 4 faces get 1 (HALF).
    assert len(moves) == 2 * 3 + 4 * 1 == 10


def test_htr_pdb_size():
    """HTR group order is 663,552."""
    from cube.classifier.htr import htr_pdb
    pdb = htr_pdb()
    assert len(pdb) == 663_552


def test_htr_pdb_diameter():
    """HTR diameter is finite and reasonable (literature: ~15 moves)."""
    from cube.classifier.htr import htr_pdb
    pdb = htr_pdb()
    max_d = max(d for d, _ in pdb.values())
    # Match cube literature: HTR diameter is exactly 15 half-turns.
    assert max_d == 15


def test_htr_solve_on_random_walks():
    """Apply k random half-turns to SOLVED; htr_solve should return ≤k moves."""
    import random
    from cube.classifier.htr import htr_solve
    rng = random.Random(0)
    half_turns = [Move(f, Turn.HALF) for f in Face]
    for _ in range(50):
        k = rng.randint(0, 10)
        seq = [rng.choice(half_turns) for _ in range(k)]
        state = SOLVED.apply_alg(seq)
        sol = htr_solve(state)
        assert sol is not None, f"htr_solve returned None for HTR-reachable state"
        assert len(sol) <= k
        # Verify solution actually solves.
        verify = state.apply_alg(sol)
        assert verify == SOLVED


def test_htr_solve_returns_only_half_turns():
    """The solve sequence must use only half turns (HTR group)."""
    import random
    from cube.classifier.htr import htr_solve
    rng = random.Random(1)
    half_turns = [Move(f, Turn.HALF) for f in Face]
    for _ in range(20):
        k = rng.randint(1, 12)
        seq = [rng.choice(half_turns) for _ in range(k)]
        state = SOLVED.apply_alg(seq)
        sol = htr_solve(state)
        assert sol is not None
        for m in sol:
            assert m.turn == Turn.HALF, f"non-half-turn in HTR solve: {m}"


def test_htr_solve_on_non_htr_returns_none():
    """A single quarter turn leaves HTR — solver should refuse."""
    from cube.classifier.htr import htr_solve
    for face in Face:
        state = SOLVED.apply(Move(face, Turn.CW))
        assert htr_solve(state) is None


def test_is_htr_ud_solved():
    from cube.classifier.htr import is_htr_ud
    assert is_htr_ud(SOLVED)


def test_is_htr_ud_is_strictly_looser_than_is_htr():
    """is_htr ⊆ is_htr_ud (strict implies single-axis).

    Random half-turn walks from SOLVED stay in is_htr; they should
    also stay in is_htr_ud trivially since the conditions are weaker.
    """
    import random
    from cube.classifier.htr import is_htr, is_htr_ud
    rng = random.Random(7)
    half_turns = [Move(f, Turn.HALF) for f in Face]
    for _ in range(40):
        k = rng.randint(0, 8)
        seq = [rng.choice(half_turns) for _ in range(k)]
        s = SOLVED.apply_alg(seq)
        if is_htr(s):
            assert is_htr_ud(s)


def test_is_htr_ud_after_dr_group_moves_can_be_true():
    """Apply DR-group moves to SOLVED → result is in is_htr_ud iff cp/ep
    in the HTR subgroups AND UD-EO/CO stay zero. Quarter U/D moves
    typically break this; half turns preserve it."""
    from cube.classifier.htr import is_htr_ud
    # SOLVED + U2 stays in HTR_ud (half turn preserves cp/ep within HTR).
    s = SOLVED.apply(Move(Face.U, Turn.HALF))
    assert is_htr_ud(s)
    # SOLVED + U breaks cp/ep out of HTR-corner/edge sets in general.
    s = SOLVED.apply(Move(Face.U, Turn.CW))
    # cp after U: (3, 0, 1, 2, 4, 5, 6, 7) — is this in HTR-corner-set?
    # Probably not — HTR is half-turn-generated, U is a quarter.
    assert not is_htr_ud(s)
