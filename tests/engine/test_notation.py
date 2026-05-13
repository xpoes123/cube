import pytest

from cube.engine import Face, Move, Turn, format_alg, parse_alg
from cube.engine.notation import NissAlg, invert, parse_niss


def test_parse_simple():
    alg = parse_alg("R U R' U2")
    assert alg == [
        Move(Face.R, Turn.CW),
        Move(Face.U, Turn.CW),
        Move(Face.R, Turn.CCW),
        Move(Face.U, Turn.HALF),
    ]


def test_format_roundtrip():
    s = "R U R' U2 F2 B'"
    assert format_alg(parse_alg(s)) == s


def test_parse_ignores_punctuation():
    """Reconstructions sometimes have commas, dots, slashes."""
    assert parse_alg("R, U/R'.U2") == parse_alg("R U R' U2")


def test_invert_correctness():
    alg = parse_alg("R U R' U'")
    inv = invert(alg)
    assert format_alg(inv) == "U R U' R'"


def test_invalid_alg_raises():
    with pytest.raises(ValueError):
        parse_alg("R X U")


def test_niss_simple():
    """`R U (D F) R'` means: normal=R U R', inverse=D F.
    Flat: R U R' + invert(D F) = R U R' F' D'.
    """
    n = parse_niss("R U (D F) R'")
    assert format_alg(n.normal) == "R U R'"
    assert format_alg(n.inverse) == "D F"
    assert format_alg(n.flat()) == "R U R' F' D'"


def test_niss_multiple_groups():
    """Multiple paren groups concatenate in order."""
    n = parse_niss("R (U) F (D2)")
    assert format_alg(n.normal) == "R F"
    assert format_alg(n.inverse) == "U D2"


def test_niss_empty_inverse():
    n = parse_niss("R U R'")
    assert isinstance(n, NissAlg)
    assert n.inverse == []
