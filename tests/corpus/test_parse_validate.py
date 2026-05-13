"""Corpus parser and validator end-to-end tests.

Uses a synthetic-but-valid reconstruction (scramble + its inverse) so we
don't depend on memorized real-world FMC solves.
"""

import pytest

from cube.corpus import parse_reconstruction, validate
from cube.engine.notation import format_alg, invert, parse_alg


def synthetic_reconstruction_text(scramble_str: str, solution_str: str) -> str:
    return f"Scramble: {scramble_str}\nSolution: {solution_str}\n"


def test_parses_basic_reconstruction():
    scramble = "R U R' F2 L2 D B"
    solution_alg = invert(parse_alg(scramble))
    text = synthetic_reconstruction_text(scramble, format_alg(solution_alg))
    rec = parse_reconstruction(text, source="test", source_id="r1")
    assert rec.scramble == parse_alg(scramble)
    assert rec.solution.flat() == solution_alg


def test_validates_correct_solution():
    scramble = "R U R' F2 L2 D B"
    solution = format_alg(invert(parse_alg(scramble)))
    text = synthetic_reconstruction_text(scramble, solution)
    rec = parse_reconstruction(text, source="test", source_id="r1")
    result = validate(rec)
    assert result.ok, f"expected valid: {result.reason}"


def test_catches_wrong_solution():
    scramble = "R U R' F2 L2 D B"
    # Truncate the inverse so it doesn't solve.
    wrong_solution = "R U"  # nowhere near correct
    text = synthetic_reconstruction_text(scramble, wrong_solution)
    rec = parse_reconstruction(text, source="test", source_id="r1")
    result = validate(rec)
    assert not result.ok
    assert "bad" in (result.reason or "")


def test_parses_niss_in_solution():
    """Reconstruction with NISS notation should parse and validate.
    Construct: scramble = R U; if we apply scramble then U' R', we're solved.
    Equivalent NISS form: solution = (R U) — applies R U on inverse, which
    means the flat sequence applied to the scramble is invert("R U") = U' R'.
    """
    text = synthetic_reconstruction_text("R U", "(R U)")
    rec = parse_reconstruction(text, source="test", source_id="r1")
    assert rec.solution.normal == []
    assert rec.solution.inverse == parse_alg("R U")
    assert validate(rec).ok


def test_strips_inline_comments():
    text = (
        "Scramble: R U R' // some prep notes\n"
        "Solution: R U' R U' R' // EO\n"
    )
    rec = parse_reconstruction(text, source="test", source_id="r1")
    assert rec.scramble == parse_alg("R U R'")
    assert rec.solution.normal == parse_alg("R U' R U' R'")


def test_multiline_solution_block():
    text = (
        "Scramble: R U R' F2 L2 D B\n"
        "Solution: B' D' L2\n"
        "          F2 R U' R'\n"
        "Final: 7 moves\n"
    )
    rec = parse_reconstruction(text, source="test", source_id="r1")
    assert rec.solution.normal == parse_alg("B' D' L2 F2 R U' R'")
    assert validate(rec).ok


def test_missing_scramble_raises():
    with pytest.raises(ValueError, match="scramble"):
        parse_reconstruction("Solution: R U R'\n", source="test", source_id="r1")


def test_missing_solution_raises():
    with pytest.raises(ValueError, match="solution"):
        parse_reconstruction("Scramble: R U R'\n", source="test", source_id="r1")


def test_reconstruction_length_property():
    text = synthetic_reconstruction_text("R U R'", "R U' R'")
    rec = parse_reconstruction(text, source="test", source_id="r1")
    assert rec.length == 3
