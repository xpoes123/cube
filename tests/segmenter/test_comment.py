"""Comment parser tests using real 333.fm reconstruction commentary."""

from cube.engine.notation import format_alg
from cube.segmenter import parse_phase_comments

WONG_COMMENT = """U F L R' U//EO (5/5)
(B) F2 D2 L2 B//DR, 4a1 (5/10)
(D2 R2 U2 B2 R)//HTR (5/15)
(U2 F2 U2 L2)//M + S slice (4/19)

...U [F2 D2 L2 B L2 U2 F2] U2 {R' B2 U2 R2} D2 B'

[]->B' F' L2 U2 F R2 D2 B2 (20)
"""


def test_extracts_wong_phase_lines():
    phases = parse_phase_comments(WONG_COMMENT)
    assert len(phases) == 4
    labels = [p.raw_label for p in phases]
    assert labels == ["EO", "DR, 4a1", "HTR", "M + S slice"]


def test_extracts_phase_counts():
    phases = parse_phase_comments(WONG_COMMENT)
    counts = [(p.author_phase_count, p.author_cumulative) for p in phases]
    assert counts == [(5, 5), (5, 10), (5, 15), (4, 19)]


def test_extracts_niss_moves():
    """Second phase has NISS notation: (B) F2 D2 L2 B."""
    phases = parse_phase_comments(WONG_COMMENT)
    dr_phase = phases[1]
    assert format_alg(dr_phase.moves.normal) == "F2 D2 L2 B"
    assert format_alg(dr_phase.moves.inverse) == "B"


def test_ignores_prose_and_insertions():
    """The [] insertion definition and prose lines must be skipped."""
    phases = parse_phase_comments(WONG_COMMENT)
    # 4 phase lines, not more (the [] -> line and prose should be ignored).
    assert len(phases) == 4


def test_empty_comment_returns_empty():
    assert parse_phase_comments("") == []
    assert parse_phase_comments(None) == []


def test_descriptive_label_preserved():
    comment = "R U R' U2 //slice + EP (4/4)\n"
    phases = parse_phase_comments(comment)
    assert phases[0].raw_label == "slice + EP"


def test_malformed_moves_line_skipped():
    """A phase line with bad notation is skipped, not raising."""
    comment = "R U BADXYZ//EO (3/3)\nR U R'//finish (3/6)\n"
    phases = parse_phase_comments(comment)
    assert len(phases) == 1
    assert phases[0].raw_label == "finish"
