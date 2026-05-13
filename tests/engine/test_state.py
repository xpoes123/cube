"""Engine sanity tests: move tables and algorithm application.

If any of these fail, the move tables in state.py have a bug — most likely
a CO/EO delta direction or a cycle ordering.
"""

import random

import pytest

from cube.engine import SOLVED, Face, Move, Turn, parse_alg
from cube.engine.notation import invert


def apply(alg_str: str):
    return SOLVED.apply_alg(parse_alg(alg_str))


@pytest.mark.parametrize("face", list(Face))
def test_face_order_four(face):
    """Every quarter turn has order 4."""
    s = SOLVED
    move = Move(face, Turn.CW)
    for _ in range(4):
        s = s.apply(move)
    assert s == SOLVED, f"{face.name} CW not order 4"


@pytest.mark.parametrize("face", list(Face))
def test_half_turn_self_inverse(face):
    """Half turns are self-inverse."""
    move = Move(face, Turn.HALF)
    assert SOLVED.apply(move).apply(move) == SOLVED


@pytest.mark.parametrize("face", list(Face))
def test_quarter_inverse(face):
    """CW followed by CCW returns to solved."""
    cw = Move(face, Turn.CW)
    ccw = Move(face, Turn.CCW)
    assert SOLVED.apply(cw).apply(ccw) == SOLVED


def test_sexy_move_order_6():
    """(R U R' U')^6 = identity. Classic commutator identity."""
    alg = parse_alg("R U R' U'") * 6
    assert SOLVED.apply_alg(alg) == SOLVED


def test_sune_anti_sune_identity():
    """Sune + anti-Sune = identity."""
    alg = parse_alg("R U R' U R U2 R'") + parse_alg("R U2 R' U' R U' R'")
    assert SOLVED.apply_alg(alg) == SOLVED


def test_t_perm_order_2():
    """T-perm has order 2 (it's a 2-swap)."""
    t_perm = parse_alg("R U R' U' R' F R2 U' R' U' R U R' F'")
    s = SOLVED.apply_alg(t_perm)
    assert s != SOLVED
    assert s.apply_alg(t_perm) == SOLVED


def test_random_scramble_inverse_roundtrip():
    """For 100 random algs of length 25, alg + invert(alg) = identity."""
    rng = random.Random(0)
    moves_pool = [Move(f, t) for f in Face for t in Turn]
    for _ in range(100):
        alg = [rng.choice(moves_pool) for _ in range(25)]
        round_trip = SOLVED.apply_alg(alg).apply_alg(invert(alg))
        assert round_trip == SOLVED


def test_co_sum_invariant():
    """Total CO is always 0 mod 3 after any legal alg."""
    rng = random.Random(1)
    moves_pool = [Move(f, t) for f in Face for t in Turn]
    for _ in range(50):
        alg = [rng.choice(moves_pool) for _ in range(20)]
        s = SOLVED.apply_alg(alg)
        assert sum(s.co) % 3 == 0


def test_eo_sum_invariant():
    """Total EO is always 0 mod 2 after any legal alg."""
    rng = random.Random(2)
    moves_pool = [Move(f, t) for f in Face for t in Turn]
    for _ in range(50):
        alg = [rng.choice(moves_pool) for _ in range(20)]
        s = SOLVED.apply_alg(alg)
        assert sum(s.eo) % 2 == 0


def test_corner_permutation_parity_matches_edge():
    """In 3x3, corner permutation parity must equal edge permutation parity."""
    rng = random.Random(3)
    moves_pool = [Move(f, t) for f in Face for t in Turn]
    for _ in range(50):
        alg = [rng.choice(moves_pool) for _ in range(20)]
        s = SOLVED.apply_alg(alg)
        assert _parity(s.cp) == _parity(s.ep)


# --- Reference-validated CO/EO states ---
# These pin exact CO/EO values after each single quarter turn from solved.
# Values cross-checked against pycuber 0.2.2. Round-trip invariants alone
# (R^4=identity, sum_CO=0 mod 3) cannot catch chirality bugs in CO deltas;
# these can.

_EXPECTED_AFTER_QUARTER = {
    # face: (cp, co, ep, eo)
    "U": (
        (3, 0, 1, 2, 4, 5, 6, 7),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11),
        (0,) * 12,
    ),
    "D": (
        (0, 1, 2, 3, 5, 6, 7, 4),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11),
        (0,) * 12,
    ),
    "R": (
        (4, 1, 2, 0, 7, 5, 6, 3),
        (2, 0, 0, 1, 1, 0, 0, 2),
        (8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0),
        (0,) * 12,
    ),
    "L": (
        (0, 2, 6, 3, 4, 1, 5, 7),
        (0, 1, 2, 0, 0, 2, 1, 0),
        (0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11),
        (0,) * 12,
    ),
    "F": (
        (1, 5, 2, 3, 0, 4, 6, 7),
        (1, 2, 0, 0, 2, 1, 0, 0),
        (0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11),
        (0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0),
    ),
    "B": (
        (0, 1, 3, 7, 4, 5, 2, 6),
        (0, 0, 1, 2, 0, 0, 2, 1),
        (0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7),
        (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1),
    ),
}


@pytest.mark.parametrize("face_char", list(_EXPECTED_AFTER_QUARTER.keys()))
def test_quarter_turn_exact_state(face_char):
    expected_cp, expected_co, expected_ep, expected_eo = _EXPECTED_AFTER_QUARTER[face_char]
    s = SOLVED.apply_alg(parse_alg(face_char))
    assert s.cp == expected_cp, f"{face_char} cp mismatch"
    assert s.co == expected_co, f"{face_char} co mismatch (chirality?)"
    assert s.ep == expected_ep, f"{face_char} ep mismatch"
    assert s.eo == expected_eo, f"{face_char} eo mismatch"


def _parity(perm: tuple[int, ...]) -> int:
    """Permutation parity: number of transpositions mod 2."""
    p = list(perm)
    swaps = 0
    for i in range(len(p)):
        while p[i] != i:
            j = p[i]
            p[i], p[j] = p[j], p[i]
            swaps += 1
    return swaps % 2
