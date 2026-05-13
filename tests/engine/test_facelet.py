"""Facelet representation tests.

Round-trip: to_facelets(from_facelets(f)) == f and from_facelets(to_facelets(s)) == s.
Solved state matches the canonical Kociemba facelet string.
Cross-checks against pycuber happen in the smoke script (not pinned here
because we don't want pycuber as a test dep).
"""

import random

from cube.engine import SOLVED, parse_alg
from cube.engine.facelet import (
    FACE_NAMES,
    U, R, F, D, L, B,
    from_facelets,
    to_facelets,
)


def test_solved_facelets():
    f = to_facelets(SOLVED)
    expected = (
        [U] * 9
        + [R] * 9
        + [F] * 9
        + [D] * 9
        + [L] * 9
        + [B] * 9
    )
    assert list(f) == expected


def test_centers_invariant_under_moves():
    """Face centers never move on 3x3 — they're at indices 4, 13, 22, 31, 40, 49."""
    for alg in ["U R F D L B", "R U R' U R U2 R'", "F2 D2 L2 B2"]:
        f = to_facelets(SOLVED.apply_alg(parse_alg(alg)))
        for face_idx in range(6):
            assert f[face_idx * 9 + 4] == face_idx, f"center moved on {FACE_NAMES[face_idx]} after {alg}"


def test_state_to_facelet_round_trip():
    """from_facelets recovers cp/co/ep/eo. Multi-axis EO arrays (eo_fb, eo_rl)
    are auxiliary state and not part of the facelet snapshot — they require
    history to compute, so they aren't recovered."""
    rng = random.Random(0)
    moves_pool = ["U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2", "L", "L'", "L2",
                  "F", "F'", "F2", "B", "B'", "B2"]
    for _ in range(100):
        alg = " ".join(rng.choice(moves_pool) for _ in range(25))
        state = SOLVED.apply_alg(parse_alg(alg))
        recovered = from_facelets(to_facelets(state))
        assert recovered.cp == state.cp
        assert recovered.co == state.co
        assert recovered.ep == state.ep
        assert recovered.eo == state.eo


def test_facelet_to_state_round_trip():
    """to_facelets(from_facelets(f)) == f. Facelet representation is bijective
    with the UD-axis-relevant part of State (cp/co/ep/eo)."""
    rng = random.Random(1)
    moves_pool = ["U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2", "L", "L'", "L2",
                  "F", "F'", "F2", "B", "B'", "B2"]
    for _ in range(100):
        alg = " ".join(rng.choice(moves_pool) for _ in range(25))
        f1 = to_facelets(SOLVED.apply_alg(parse_alg(alg)))
        f2 = to_facelets(from_facelets(f1))
        assert f1 == f2


def test_eo_recovery_matches_engine():
    """Recovered eo matches engine eo (key correctness signal for axis-EO work)."""
    rng = random.Random(2)
    moves_pool = ["U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2", "L", "L'", "L2",
                  "F", "F'", "F2", "B", "B'", "B2"]
    for _ in range(100):
        alg = " ".join(rng.choice(moves_pool) for _ in range(20))
        state = SOLVED.apply_alg(parse_alg(alg))
        recovered = from_facelets(to_facelets(state))
        assert recovered.eo == state.eo
        assert recovered.co == state.co


def test_total_color_count():
    """Every face color appears exactly 9 times in any valid state."""
    rng = random.Random(3)
    moves_pool = ["U", "U'", "R", "F", "D", "L", "B"]
    for _ in range(20):
        alg = " ".join(rng.choice(moves_pool) for _ in range(30))
        f = to_facelets(SOLVED.apply_alg(parse_alg(alg)))
        for color in range(6):
            assert f.count(color) == 9
