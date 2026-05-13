"""End-to-end segmenter tests using a real 333.fm reconstruction."""

from cube.corpus.sources.api333fm import submission_to_reconstruction
from cube.segmenter import Method, Phase, segment

# Real submission with author phase annotations (Wong's FMC 2024 attempt 1).
# The phase moves describe the SKELETON; the `solution` field is the
# post-insertion final. State-at-end for the last phase will NOT be SOLVED,
# because insertions are applied separately.
_REAL_SUBMISSION = {
    "id": 45821,
    "solution": "U F L R' U B' F' L2 U2 F R2 D2 B2 U2 L' D2 B2 L R D2 B'",
    "inverse": False,
    "comment": (
        "U F L R' U//EO (5/5)\n"
        "(B) F2 D2 L2 B//DR, 4a1 (5/10)\n"
        "(D2 R2 U2 B2 R)//HTR (5/15)\n"
        "(U2 F2 U2 L2)//M + S slice (4/19)\n"
    ),
    "competitionId": 3006,
    "userId": 635,
    "scramble": {
        "scramble": "R' U' F D R F2 D L F D2 F2 L' U R' L2 D' R2 F2 R2 D L2 U2 R' U' F",
    },
}
_REAL_RECON = {"user": {"id": 635, "name": "Wong"}}


def make_reconstruction():
    return submission_to_reconstruction(
        _REAL_SUBMISSION, recon=_REAL_RECON, competition_name="FMC 2024"
    )


def test_segments_wong_solve():
    seg = segment(make_reconstruction())
    assert seg.source == "comment"
    assert len(seg.segments) == 4
    assert [s.phase for s in seg.segments] == [Phase.EO, Phase.DR, Phase.HTR, Phase.SLICE]
    assert [s.raw_label for s in seg.segments] == ["EO", "DR, 4a1", "HTR", "M + S slice"]


def test_cumulative_counts_match_author():
    seg = segment(make_reconstruction())
    for s in seg.segments:
        assert s.cumulative_count == s.author_cumulative


def test_eo_phase_state_captured():
    """We capture state at phase boundary; can't yet verify EO axis (UD-only
    classifier doesn't handle Wong's FB-axis EO). Just verify state is recorded."""
    seg = segment(make_reconstruction())
    eo_segment = seg.segments[0]
    assert eo_segment.state_at_end is not None
    assert eo_segment.phase_move_count == 5


def test_method_inferred_as_dr():
    seg = segment(make_reconstruction())
    assert seg.method == Method.DR


def test_no_issues_for_clean_solve():
    seg = segment(make_reconstruction())
    assert seg.issues == ()


def test_state_fallback_when_no_comment():
    """Reconstruction with no comment uses state-based segmentation."""
    sub = {**_REAL_SUBMISSION, "comment": None}
    rec = submission_to_reconstruction(sub, recon=_REAL_RECON, competition_name="FMC 2024")
    seg = segment(rec)
    assert seg.source == "state"
    # Should still detect at least EO and DR milestones (state-based) since the
    # solution physically passes through those milestones in this solve.
    phases = [s.phase for s in seg.segments]
    assert Phase.EO in phases or Phase.DR in phases
