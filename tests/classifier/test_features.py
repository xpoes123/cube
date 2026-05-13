"""Classifier validation: feature detectors over known states."""

from cube.classifier import (
    Axis,
    best_eo_axis,
    co_count,
    e_slice_in_slice,
    eo_count,
    find_2x2x2,
    is_2x2x2_at,
    is_co_solved,
    is_dr,
    is_eo_solved,
    slice_in_slice,
    slice_misplaced_count,
    solved_corners,
    solved_edges,
)
from cube.engine import SOLVED, parse_alg


def apply(s: str):
    return SOLVED.apply_alg(parse_alg(s))


# ---------- EO ----------


def test_solved_has_no_bad_edges():
    assert eo_count(SOLVED) == 0
    assert is_eo_solved(SOLVED)


def test_f_flips_4_edges():
    """An F quarter turn flips the 4 F-face edges under UD-axis EO."""
    assert eo_count(apply("F")) == 4


def test_b_flips_4_edges():
    assert eo_count(apply("B")) == 4


def test_f_b_each_flip_independent_edges():
    """F + B touches 8 distinct edges, so 8 bad edges."""
    assert eo_count(apply("F B")) == 8


def test_u_quarter_does_not_flip_edges():
    assert eo_count(apply("U")) == 0


def test_r_quarter_does_not_flip_edges():
    """R quarter does not flip edges under UD-axis EO."""
    assert eo_count(apply("R")) == 0


def test_f2_preserves_eo():
    """F2 (half turn) is in <U,D,L,R,F2,B2> so preserves EO."""
    assert eo_count(apply("F2")) == 0


# ---------- CO ----------


def test_solved_has_no_bad_corners():
    assert co_count(SOLVED) == 0
    assert is_co_solved(SOLVED)


def test_r_twists_corners():
    """R CW twists the 4 R-face corners."""
    assert co_count(apply("R")) == 4


def test_u_preserves_co():
    """U quarter does not twist corners under UD-axis CO."""
    assert co_count(apply("U")) == 0


def test_r2_preserves_co():
    """Half turns preserve CO."""
    assert co_count(apply("R2")) == 0


# ---------- DR ----------


def test_solved_is_dr():
    assert is_dr(SOLVED)


def test_dr_preserving_moves_keep_dr():
    """Moves in <U, D, R2, L2, F2, B2> preserve DR."""
    for alg in ["U", "D", "R2", "L2", "F2", "B2", "U D R2 L2 F2 B2 U2"]:
        s = SOLVED.apply_alg(parse_alg(alg))
        assert is_dr(s), f"{alg!r} should be DR-preserving"


def test_single_quarter_breaks_dr():
    """A single R or F quarter turn breaks DR."""
    assert not is_dr(apply("R"))
    assert not is_dr(apply("F"))


def test_e_slice_stays_in_slice_after_dr_moves():
    s = apply("U D R2 L2 F2 B2")
    assert e_slice_in_slice(s)


def test_r_takes_e_slice_edge_out():
    """R moves the FR edge to UR position, leaving E-slice."""
    s = apply("R")
    assert not e_slice_in_slice(s)


# ---------- Solved-piece sets ----------


def test_solved_has_all_pieces_solved():
    assert len(solved_corners(SOLVED)) == 8
    assert len(solved_edges(SOLVED)) == 12


def test_r_breaks_r_face_pieces():
    """R turn unsolves 4 corners + 4 edges (the R face pieces)."""
    s = apply("R")
    assert len(solved_corners(s)) == 4  # the 4 L-face corners remain
    assert len(solved_edges(s)) == 8     # 12 - 4 R-face edges


# ---------- 2x2x2 blocks ----------


def test_solved_has_2x2x2_at_every_corner():
    for c in range(8):
        assert is_2x2x2_at(SOLVED, c)


def test_r_destroys_urf_2x2x2():
    s = apply("R")
    assert not is_2x2x2_at(s, 0)  # URF block broken


def test_r_preserves_ulb_2x2x2():
    """R doesn't touch ULB or its neighbors."""
    s = apply("R")
    assert is_2x2x2_at(s, 2)


def test_find_2x2x2_returns_some_corner_after_one_move():
    """After a single R, multiple 2x2x2 blocks survive — find_2x2x2 returns one."""
    s = apply("R")
    found = find_2x2x2(s)
    assert found is not None
    assert is_2x2x2_at(s, found)


# ---------- Multi-axis EO ----------


def test_solved_has_no_bad_edges_on_any_axis():
    for axis in Axis:
        assert eo_count(SOLVED, axis) == 0
        assert is_eo_solved(SOLVED, axis)


def test_f_only_flips_ud_axis_eo():
    """F quarter flips 4 edges under UD-axis EO, none under FB or RL."""
    s = apply("F")
    assert eo_count(s, Axis.UD) == 4
    assert eo_count(s, Axis.FB) == 0
    assert eo_count(s, Axis.RL) == 0


def test_r_only_flips_fb_axis_eo():
    """R quarter flips 4 edges under FB-axis EO (LR-flip convention)."""
    s = apply("R")
    assert eo_count(s, Axis.UD) == 0
    assert eo_count(s, Axis.FB) == 4
    assert eo_count(s, Axis.RL) == 0


def test_u_only_flips_rl_axis_eo():
    """U quarter flips 4 edges under RL-axis EO (UD-flip convention)."""
    s = apply("U")
    assert eo_count(s, Axis.UD) == 0
    assert eo_count(s, Axis.FB) == 0
    assert eo_count(s, Axis.RL) == 4


def test_wong_eo_solved_on_rl_axis():
    """Wong's FMC2024 attempt 1 EO line solves RL-axis EO (not UD or FB)."""
    s = apply("R' U' F D R F2 D L F D2 F2 L' U R' L2 D' R2 F2 R2 D L2 U2 R' U' F")
    s = s.apply_alg(parse_alg("U F L R' U"))
    # Should be solved on RL axis (since Wong used RL-axis EO)
    axis, count = best_eo_axis(s)
    assert count == 0, f"expected some axis fully solved, best was {axis} with {count} bad"
    assert axis == Axis.RL


def test_half_turns_preserve_all_axis_eo():
    """Half turns preserve EO under all axis conventions."""
    for half in ["U2", "D2", "R2", "L2", "F2", "B2"]:
        s = apply(half)
        for axis in Axis:
            assert is_eo_solved(s, axis), f"{half} broke EO on {axis.value}"


# ---------- Multi-axis slice ----------


def test_e_slice_perpendicular_to_ud():
    """E-slice edges (FR/FL/BL/BR) are perpendicular to UD axis."""
    assert slice_in_slice(SOLVED, Axis.UD)


def test_r_displaces_e_slice():
    """R turn moves an E-slice edge (FR) out of E-slice."""
    s = apply("R")
    assert not slice_in_slice(s, Axis.UD)


def test_u_does_not_displace_e_slice():
    """U turn only moves U-layer edges; E-slice untouched."""
    s = apply("U")
    assert slice_in_slice(s, Axis.UD)


def test_u_displaces_s_slice():
    """U turn moves S-slice edges (UR moves to UF, which is M-slice)."""
    s = apply("U")
    assert not slice_in_slice(s, Axis.FB)


def test_f_displaces_m_slice():
    """F turn moves M-slice edges (UF moves to FR, which is E-slice)."""
    s = apply("F")
    assert not slice_in_slice(s, Axis.RL)


# ---------- end multi-axis ----------


def test_scrambled_no_2x2x2():
    """Sufficient scramble destroys all 2x2x2 blocks."""
    s = apply("R U R' U' R' F R2 U' R' U' R U R' F'")  # T-perm
    # T-perm only permutes 3 corners and 3 edges. Most 2x2x2 blocks survive.
    # Use a more disruptive scramble.
    s = apply("R U F D L B R U F D")
    assert find_2x2x2(s) is None
