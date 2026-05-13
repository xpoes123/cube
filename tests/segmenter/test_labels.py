from cube.segmenter import Phase, canonicalize


def test_eo_variants():
    assert canonicalize("EO") == Phase.EO
    assert canonicalize("eo") == Phase.EO
    assert canonicalize("EO + 1c") == Phase.EO
    assert canonicalize("Edge orientation") == Phase.EO


def test_dr_variants():
    assert canonicalize("DR") == Phase.DR
    assert canonicalize("DR, 4a1") == Phase.DR
    assert canonicalize("DR + 2c2") == Phase.DR
    assert canonicalize("DR finish") == Phase.DR
    assert canonicalize("Domino reduction") == Phase.DR


def test_htr_variants():
    assert canonicalize("HTR") == Phase.HTR
    assert canonicalize("Half-turn reduction") == Phase.HTR


def test_slice_variants():
    assert canonicalize("M slice") == Phase.SLICE
    assert canonicalize("M + S slice") == Phase.SLICE


def test_block_variants():
    assert canonicalize("2x2x2") == Phase.BLOCK
    assert canonicalize("2x2x3") == Phase.BLOCK
    assert canonicalize("F2L-1") == Phase.BLOCK
    assert canonicalize("F2L") == Phase.BLOCK


def test_insertion():
    assert canonicalize("Insertion") == Phase.INSERTION
    assert canonicalize("Insert here") == Phase.INSERTION


def test_unknown():
    assert canonicalize("") == Phase.UNKNOWN
    assert canonicalize("something weird") == Phase.UNKNOWN


def test_dr_takes_priority_over_finish():
    """'DR finish' should canonicalize to DR, not FINISH."""
    assert canonicalize("DR finish") == Phase.DR
