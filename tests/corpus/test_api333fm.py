"""Adapter tests for 333.fm API → Reconstruction.

Network test (live API hit) is gated by env var so the offline test suite
stays hermetic. Run with: `CUBE_RUN_NETWORK_TESTS=1 uv run pytest -k network`.
"""

import os

import pytest

from cube.corpus import validate
from cube.corpus.sources.api333fm import (
    Api333fmClient,
    FetchStats,
    submission_to_reconstruction,
)


# Real submission shape captured from /wca/reconstruction/FMC2024/user/635
# (Wong Chong Wen's winning solve, 21 moves). Solution validated independently.
_REAL_SUBMISSION = {
    "id": 45821,
    "mode": 0,
    "solution": "U F L R' U B' F' L2 U2 F R2 D2 B2 U2 L' D2 B2 L R D2 B'",
    "insertions": None,
    "inverse": False,
    "phase": 0,
    "comment": "U F L R' U//EO (5/5)\n(B) F2 D2 L2 B//DR, 4a1 (5/10)\n...",
    "moves": 2100,
    "wcaMoves": 2100,
    "competitionId": 3006,
    "scrambleId": 8056,
    "userId": 635,
    "createdAt": "2026-03-02T14:18:48.993Z",
    "scramble": {
        "scramble": "R' U' F D R F2 D L F D2 F2 L' U R' L2 D' R2 F2 R2 D L2 U2 R' U' F",
    },
}

_REAL_RECON = {
    "user": {"id": 635, "name": "Wong Chong Wen", "wcaId": "2014WENW01"},
}


def test_maps_submission_fields():
    rec = submission_to_reconstruction(
        _REAL_SUBMISSION, recon=_REAL_RECON, competition_name="FMC 2024"
    )
    assert rec is not None
    assert rec.source == "333.fm"
    assert rec.source_id == "wca:3006:635:45821"
    assert rec.author == "Wong Chong Wen"
    assert rec.competition == "FMC 2024"
    assert rec.commentary is not None and "EO (5/5)" in rec.commentary
    assert rec.length == 21


def test_real_submission_validates():
    """The mapped Reconstruction must round-trip through the cube engine."""
    rec = submission_to_reconstruction(
        _REAL_SUBMISSION, recon=_REAL_RECON, competition_name="FMC 2024"
    )
    result = validate(rec)
    assert result.ok, f"validation failed: {result.reason}"


def test_skips_inverse_submission():
    stats = FetchStats()
    inverse_sub = {**_REAL_SUBMISSION, "inverse": True}
    rec = submission_to_reconstruction(
        inverse_sub, recon=_REAL_RECON, competition_name="FMC 2024", stats=stats
    )
    assert rec is None
    assert stats.inverse_skipped == 1


def test_skips_empty_solution():
    sub = {**_REAL_SUBMISSION, "solution": ""}
    rec = submission_to_reconstruction(sub, recon=_REAL_RECON, competition_name="FMC 2024")
    assert rec is None


def test_counts_parse_failures():
    stats = FetchStats()
    sub = {**_REAL_SUBMISSION, "solution": "R UX F"}  # bad token
    rec = submission_to_reconstruction(
        sub, recon=_REAL_RECON, competition_name="FMC 2024", stats=stats
    )
    assert rec is None
    assert stats.parse_failures == 1


def test_missing_scramble_returns_none():
    sub = {**_REAL_SUBMISSION, "scramble": {}}
    rec = submission_to_reconstruction(sub, recon=_REAL_RECON, competition_name="FMC 2024")
    assert rec is None


@pytest.mark.skipif(
    not os.environ.get("CUBE_RUN_NETWORK_TESTS"),
    reason="network test gated by CUBE_RUN_NETWORK_TESTS=1",
)
def test_network_fetch_and_validate_one(tmp_path):
    """Smoke test: hit live API, parse one record, validate."""
    client = Api333fmClient(cache_dir=tmp_path)
    comp = client.get_competition("FMC2024")
    assert "recons" in comp
    assert "scrambles" in comp
    recon = comp["recons"][0]
    user_data = client.get_user_submissions("FMC2024", recon["userId"])
    sub = user_data["submissions"][0]
    rec = submission_to_reconstruction(
        sub, recon=user_data["recon"], competition_name=comp["competition"]["name"]
    )
    assert rec is not None
    assert validate(rec).ok
    client.close()
