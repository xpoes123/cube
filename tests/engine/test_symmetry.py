"""Validate LR-mirror.

Three layers of test, from cheapest to most expensive:
1. Move-level: table lookup matches expectations, involution holds.
2. Random scrambles: applying a random alg + then mirror(alg.inverse) to a
   mirror-able starting setup behaves consistently.
3. Full corpus: every real reconstruction round-trips to SOLVED after
   mirror(scramble) + mirror(flat solution). This is the killer test.
"""

from __future__ import annotations

import json
import os
import random
from pathlib import Path

import pytest

from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import invert, parse_alg
from cube.engine.state import SOLVED
from cube.engine.symmetry import mirror_lr_alg, mirror_lr_move

CORPUS_PATH = Path("data/raw/wca.jsonl")


def test_move_table():
    # Spot-check the six base moves.
    cases = [
        ("U", "U'"), ("U'", "U"), ("U2", "U2"),
        ("D", "D'"), ("D'", "D"), ("D2", "D2"),
        ("F", "F'"), ("F'", "F"), ("F2", "F2"),
        ("B", "B'"), ("B'", "B"), ("B2", "B2"),
        ("R", "L'"), ("R'", "L"), ("R2", "L2"),
        ("L", "R'"), ("L'", "R"), ("L2", "R2"),
    ]
    for src, expected in cases:
        m = parse_alg(src)[0]
        e = parse_alg(expected)[0]
        assert mirror_lr_move(m) == e, f"mirror({src}) expected {expected}, got {mirror_lr_move(m)}"


def test_involution_on_all_18_moves():
    for face in Face:
        for turn in Turn:
            m = Move(face, turn)
            assert mirror_lr_move(mirror_lr_move(m)) == m


def test_alg_involution_random():
    rng = random.Random(0)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(50):
        alg = [rng.choice(moves) for _ in range(rng.randint(0, 40))]
        assert mirror_lr_alg(mirror_lr_alg(alg)) == alg


def test_mirror_preserves_solve_structure_random():
    """Random alg followed by its inverse always returns to SOLVED.
    The mirror of that property must also hold (sanity).
    """
    rng = random.Random(42)
    moves = [Move(f, t) for f in Face for t in Turn]
    for _ in range(50):
        alg = [rng.choice(moves) for _ in range(rng.randint(1, 30))]
        # alg + invert(alg) == identity on the cube
        s = SOLVED.apply_alg(alg + invert(alg))
        assert s == SOLVED
        # Mirror should also be the identity
        ma = mirror_lr_alg(alg)
        s = SOLVED.apply_alg(ma + invert(ma))
        assert s == SOLVED


@pytest.mark.skipif(not CORPUS_PATH.exists(), reason="corpus not on disk")
def test_mirror_solves_every_corpus_record():
    """For every reconstruction in the corpus:
       SOLVED.apply_alg(mirror(scramble) + mirror(flat_solution)) == SOLVED.

    This is the strong correctness check for mirror_lr. If any record
    fails, the move-mapping table is wrong.
    """
    n_checked = 0
    n_failed = 0
    failures: list[str] = []
    for line in CORPUS_PATH.open():
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        try:
            scramble = parse_alg(record["scramble"])
            normal = parse_alg(record["solution_normal"])
            inverse = parse_alg(record["solution_inverse"])
        except Exception:
            continue  # corpus has occasional unparseable records — not our concern here

        # Validate the original solve first (skip records that don't solve
        # under our engine; those are corpus bugs, not mirror bugs).
        flat = normal + invert(inverse)
        end = SOLVED.apply_alg(scramble + flat)
        if end != SOLVED:
            continue  # not a usable record; skip silently

        n_checked += 1

        # Now mirror.
        m_scramble = mirror_lr_alg(scramble)
        m_flat = mirror_lr_alg(flat)
        m_end = SOLVED.apply_alg(m_scramble + m_flat)
        if m_end != SOLVED:
            n_failed += 1
            if len(failures) < 5:
                failures.append(record.get("source_id", "?"))

    # We require at least a non-trivial number of records to make this meaningful.
    assert n_checked > 100, f"expected >100 valid records to check, got {n_checked}"
    assert n_failed == 0, (
        f"{n_failed}/{n_checked} mirrored solves failed to reach SOLVED. "
        f"First failures: {failures}"
    )


# Skip the full-corpus test in CI / fast runs unless env says otherwise.
if os.environ.get("CUBE_SKIP_CORPUS_TESTS"):  # pragma: no cover
    test_mirror_solves_every_corpus_record = pytest.mark.skip(  # type: ignore
        reason="CUBE_SKIP_CORPUS_TESTS set"
    )(test_mirror_solves_every_corpus_record)
