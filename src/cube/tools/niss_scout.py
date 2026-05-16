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


def _eo_then_dr(
    scramble: list[str], history: list[str], *, axis: str, dr_per_cell: int = 2
) -> list[dict]:
    """Return EO length + top-N DR options for one (side, axis) cell.

    Returns a list of dicts (one per DR option, up to dr_per_cell). v22:
    surface multiple DR candidates per (side, axis) so the agent can
    compare JOINT paths, not just (side, axis) winners.
    """
    eo = eo_pattern_lookup(scramble, history, axis=axis)
    if eo.get("found", 0) == 0:
        return [{
            "axis": axis,
            "eo_length": None,
            "eo_moves": [],
            "dr_option": None,
            "expected_total_to_solved": None,
            "jzp_eligible": False,
            "note": "EO pattern not memorized for this axis",
        }]
    eo_moves = list(eo["options"][0]["moves"])
    eo_len = len(eo_moves)

    extended_history = list(history) + eo_moves
    dr = dr_trigger_options(scramble, extended_history, axis=axis, max_setup=5)
    if "error" in dr or not dr.get("options"):
        return [{
            "axis": axis,
            "eo_length": eo_len,
            "eo_moves": eo_moves,
            "dr_option": None,
            "expected_total_to_solved": eo_len + 99,
            "jzp_eligible": False,
            "note": dr.get("error", "no DR triggers within max_setup=5"),
        }]
    rows = []
    for opt in dr["options"][:dr_per_cell]:
        rows.append({
            "axis": axis,
            "eo_length": eo_len,
            "eo_moves": eo_moves,
            "dr_option": {
                "trigger_family": opt["trigger_family"],
                "setup_length": opt["setup_length"],
                "trigger_length": opt["trigger_length"],
                "total_to_dr": opt["total_to_dr"],
                "expected_htr_moves": opt["expected_htr_moves"],
            },
            "expected_total_to_solved": eo_len + opt["expected_total_to_solved"],
            "jzp_eligible": opt["jzp_eligible"],
            "note": (
                f"EO {eo_len}mv + {opt['trigger_family']} "
                f"(DR {opt['total_to_dr']}mv) -> expected ~{eo_len + opt['expected_total_to_solved']} total"
            ),
        })
    return rows


def niss_scout(scramble: list[str], history: list[str], *, dr_per_cell: int = 2) -> dict:
    """Scout EO + top-N DR options on both normal AND inverse, all 3 axes.

    v22: returns up to 12 rows (2 sides × 3 axes × dr_per_cell DR options).
    Surfaces the JOINT EO+DR comparison: a 4-move EO with a great DR
    substate can beat a 2-move EO with a worse DR substate. The agent
    reads the menu and picks the lowest-expected_total row.

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
        for cell in _eo_then_dr(scramble, history, axis=axis, dr_per_cell=dr_per_cell):
            cell["side"] = "normal"
            rows.append(cell)

    # Inverse side: invert the scramble; history is reset (mid-solve
    # scouting is not the use case for this tool).
    inv_moves = invert_alg(parse_alg(" ".join(scramble))) if scramble else []
    inv_scramble = [str(m) for m in inv_moves]
    for axis in _AXES:
        for cell in _eo_then_dr(inv_scramble, [], axis=axis, dr_per_cell=dr_per_cell):
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
            "v22 joint scout: up to 12 rows (2 sides × 3 axes × top-N DR triggers). "
            "Surfaces the COMPLETE EO+DR joint comparison. A longer EO with a better "
            "DR substate often beats a shorter EO with a 4C4E DR. "
            "Pick the recommendation OR override with rationale (write the rejection "
            "reasoning per [[exemplar-c-branch-journal]]). "
            "If you take the inverse side, call niss_flip BEFORE applying "
            "the EO moves; otherwise apply them on normal."
        ),
    }
