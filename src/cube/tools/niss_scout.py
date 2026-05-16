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

import pickle
from pathlib import Path

from cube.classifier.htr import dr_subset_canonical
from cube.engine.notation import parse_alg, invert_alg
from cube.engine.state import SOLVED, State
from cube.tools.dr_trigger_options import dr_trigger_options
from cube.tools.eo_pattern_lib import eo_pattern_lookup


_AXES = ("UD", "FB", "RL")

# v24: warm subset-finish cache (built by cube.agent.prewarm_subsets).
# Each entry maps a canonical HTR subset → {axis: finish_move_list}.
# We use this at scout time to compute the *actual* finish length for
# each candidate DR's post-state, replacing the family-average prior.
_FINISH_CACHE: dict[tuple, dict[str, list[str]]] | None = None


def _load_finish_cache() -> dict[tuple, dict[str, list[str]]]:
    global _FINISH_CACHE
    if _FINISH_CACHE is not None:
        return _FINISH_CACHE
    cache_path = Path("checkpoints/subset_finish_cache.pkl")
    if not cache_path.exists():
        _FINISH_CACHE = {}
        return _FINISH_CACHE
    try:
        with cache_path.open("rb") as f:
            data = pickle.load(f)
        _FINISH_CACHE = data if isinstance(data, dict) else {}
    except Exception:
        _FINISH_CACHE = {}
    return _FINISH_CACHE


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
            "eo_plus_dr_length": None,
            "jzp_eligible": False,
            "note": dr.get("error", "no DR triggers within max_setup=5"),
        }]
    rows = []
    cache = _load_finish_cache()
    for opt in dr["options"][:dr_per_cell]:
        # v24: compute the post-DR state and look up the actual HTR
        # subset + finish length from the warm cache. Replaces the
        # corpus-prior expected_htr_moves with ground truth (when
        # the subset is cached) or None (uncached fallback).
        setup_moves = opt.get("setup_moves", [])
        canonical_alg = opt.get("canonical_alg", "")
        try:
            full_path = list(history) + eo_moves + list(setup_moves) + parse_alg(canonical_alg) if canonical_alg else list(history) + eo_moves + list(setup_moves)
            # parse_alg returns Move objects; mix-and-match needs care.
            # Rebuild from strings.
            move_strs = list(history) + eo_moves + list(setup_moves)
            if canonical_alg:
                move_strs += [str(m) for m in parse_alg(canonical_alg)]
            post_dr_state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
            if move_strs:
                post_dr_state = post_dr_state.apply_alg(parse_alg(" ".join(move_strs)))
            subset = dr_subset_canonical(post_dr_state)
        except Exception:
            subset = None
            post_dr_state = None
        # Look up finish length for this subset on this axis.
        finish_length: int | None = None
        subset_label: str | None = None
        if subset is not None:
            subset_label = str(subset)
            axis_finish = cache.get(tuple(subset), {})
            # Prefer the matching axis (UD/FB/RL); fall back to any cached axis.
            finish_moves = axis_finish.get(axis) or next(iter(axis_finish.values()), None)
            if finish_moves is not None:
                finish_length = len(finish_moves)
        total_to_solved = (
            eo_len + opt["total_to_dr"] + finish_length
            if finish_length is not None else None
        )
        rows.append({
            "axis": axis,
            "eo_length": eo_len,
            "eo_moves": eo_moves,
            "dr_option": {
                "trigger_family": opt["trigger_family"],
                "setup_length": opt["setup_length"],
                "trigger_length": opt["trigger_length"],
                "total_to_dr": opt["total_to_dr"],
            },
            "eo_plus_dr_length": eo_len + opt["total_to_dr"],
            "post_dr_subset": subset_label,
            "finish_length_actual": finish_length,
            "total_to_solved_actual": total_to_solved,
            "jzp_eligible": opt["jzp_eligible"],
            "note": (
                f"EO {eo_len}mv + {opt['trigger_family']} (DR {opt['total_to_dr']}mv) "
                + (
                    f"→ subset cached, finish {finish_length}mv "
                    f"→ total {total_to_solved}mv to solved"
                    if finish_length is not None
                    else "→ subset not in cache; judge by trigger family"
                )
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

    # v24: sort by total_to_solved_actual when available (real ground
    # truth from the warm subset cache), else fall back to
    # eo_plus_dr_length. Still no "recommendation" field — the LLM
    # picks. The sort is just to put the most-informative rows first.
    def _sort_key(r: dict):
        actual = r.get("total_to_solved_actual")
        if actual is not None:
            return (0, actual, r.get("eo_length") or 99)
        # Rows without actual total sort after, by raw EO+DR
        return (1, r.get("eo_plus_dr_length") or 999, r.get("eo_length") or 99)

    rows.sort(key=_sort_key)

    return {
        "rows": rows,
        "note": (
            "Up to 12 rows (2 sides × 3 axes × top-2 DR triggers). "
            "Each row carries: eo_length, dr_option, post_dr_subset, "
            "finish_length_actual (from the warm 176-entry HTR-subset cache), "
            "and total_to_solved_actual (= EO + DR + finish, real ground truth). "
            "Rows without a cached subset show total_to_solved_actual=null; "
            "judge those by trigger family. Sort is informational; you choose."
        ),
    }
