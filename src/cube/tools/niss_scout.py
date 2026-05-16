"""niss_scout — v16: auto-compare EO + DR on normal AND inverse, all 3 axes.

The 333.fm corpus research showed that 50% of elite WCA-FMC solves START
on the inverse scramble. The median elite solve has 8 NISS transitions —
they branch in and out of inverse aggressively to scout for better EO/DR.

Our pre-v16 agent could do this via niss_flip + eo_pattern_lookup +
dr_trigger_options, but in practice it almost never did — the prompt
nudges (v14b step 1b) were too soft. v16 makes scouting a single tool
call that returns a structured comparison table, so the model HAS to
read the alternatives before committing.

Read-only: this tool does NOT modify any slot. It only computes "what
would EO + DR look like if I were on the {normal, inverse} side, doing
DR on the {UD, FB, RL} axis." Six rows total, sorted by
expected_total_to_solved.
"""

from __future__ import annotations

from cube.engine.notation import parse_alg, invert_alg
from cube.engine.state import SOLVED, State
from cube.tools.dr_trigger_options import dr_trigger_options
from cube.tools.eo_pattern_lib import eo_pattern_lookup


_AXES = ("UD", "FB", "RL")


def _apply(scramble: list[str], history: list[str]) -> State:
    s = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        s = s.apply_alg(parse_alg(" ".join(history)))
    return s


def _eo_then_dr(scramble: list[str], history: list[str], *, axis: str) -> dict:
    """Return EO length + best DR option for one (side, axis) cell.

    Returns dict with: eo_length, eo_moves, dr_option (best entry from
    dr_trigger_options or None), expected_total_to_solved, jzp_eligible,
    notes if any step failed.
    """
    eo = eo_pattern_lookup(scramble, history, axis=axis)
    if eo.get("found", 0) == 0:
        return {
            "axis": axis,
            "eo_length": None,
            "eo_moves": [],
            "dr_option": None,
            "expected_total_to_solved": None,
            "jzp_eligible": False,
            "note": "EO pattern not memorized for this axis",
        }
    eo_moves = list(eo["options"][0]["moves"])
    eo_len = len(eo_moves)

    # Simulate applying EO and see what DR options open up. We pass
    # eo_moves as an extension of history to dr_trigger_options.
    extended_history = list(history) + eo_moves
    dr = dr_trigger_options(scramble, extended_history, axis=axis, max_setup=5)
    if "error" in dr or not dr.get("options"):
        return {
            "axis": axis,
            "eo_length": eo_len,
            "eo_moves": eo_moves,
            "dr_option": None,
            "expected_total_to_solved": eo_len + 99,  # large sentinel so it sorts last
            "jzp_eligible": False,
            "note": dr.get("error", "no DR triggers within max_setup=5"),
        }
    best = dr["options"][0]
    return {
        "axis": axis,
        "eo_length": eo_len,
        "eo_moves": eo_moves,
        "dr_option": {
            "trigger_family": best["trigger_family"],
            "setup_length": best["setup_length"],
            "trigger_length": best["trigger_length"],
            "total_to_dr": best["total_to_dr"],
            "expected_htr_moves": best["expected_htr_moves"],
        },
        "expected_total_to_solved": eo_len + best["expected_total_to_solved"],
        "jzp_eligible": best["jzp_eligible"],
        "note": (
            f"EO {eo_len}mv + {best['trigger_family']} "
            f"(DR {best['total_to_dr']}mv) -> expected ~{eo_len + best['expected_total_to_solved']} total"
        ),
    }


def niss_scout(scramble: list[str], history: list[str]) -> dict:
    """Scout EO + DR feasibility on both normal AND inverse, all 3 axes.

    Returns a comparison table of 6 rows (side × axis), each with EO
    length, best DR option, and expected_total_to_solved. The agent
    reads this menu and commits to the lowest-expected_total row.

    Read-only: does NOT modify any slot. The agent must still call
    niss_flip + apply_moves separately to commit to a row.

    Note on inverse scouting: we invert the scramble and clear history.
    This reports "what EO/DR would I see if I were on the inverse side
    with no moves applied yet?" The agent should be aware that any
    pre-existing history on the slot is NOT accounted for in the
    inverse columns — call niss_scout at scramble-time, not mid-solve.
    """
    rows: list[dict] = []

    # Normal side: use current scramble + history as-is.
    for axis in _AXES:
        cell = _eo_then_dr(scramble, history, axis=axis)
        cell["side"] = "normal"
        rows.append(cell)

    # Inverse side: invert the scramble; history is reset (mid-solve
    # scouting is not the use case for this tool).
    inv_moves = invert_alg(parse_alg(" ".join(scramble))) if scramble else []
    inv_scramble = [str(m) for m in inv_moves]
    for axis in _AXES:
        cell = _eo_then_dr(inv_scramble, [], axis=axis)
        cell["side"] = "inverse"
        rows.append(cell)

    # Sort by expected_total_to_solved. Rows that couldn't compute a DR
    # option get a large sentinel and sort last.
    rows.sort(key=lambda r: (r.get("expected_total_to_solved") or 999, r.get("eo_length") or 99))

    # Surface a recommendation in the response — the agent can override
    # but the default points at the row with lowest expected total.
    top = rows[0] if rows else None
    return {
        "rows": rows,
        "recommendation": (
            {
                "side": top["side"],
                "axis": top["axis"],
                "rationale": top.get("note", ""),
                "expected_total_to_solved": top.get("expected_total_to_solved"),
            }
            if top and top.get("expected_total_to_solved") is not None
            else None
        ),
        "note": (
            "Six-row scout (normal × {UD,FB,RL}, inverse × {UD,FB,RL}). "
            "Pick the recommendation OR override with rationale. "
            "If you take the inverse side, call niss_flip BEFORE applying "
            "the EO moves; otherwise apply them on normal."
        ),
    }
