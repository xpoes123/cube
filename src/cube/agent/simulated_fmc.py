"""Realistic-FMC simulation: budget-constrained variant of the LLM solver.

The unconstrained `loop.py` answers "can an LLM orchestrate our analyzer
tools." This module answers the harder question — "can an LLM do FMC under
human-realistic constraints":

  - 1 hour total wall clock (WCA regulation; primary stop condition).
  - Simulated FMC time budget: 3600 "competition seconds". Tool usage
    accumulates simulated time; running over forces a halt.
  - 3 named cube-state slots the agent may inspect.
  - 4-move undo buffer per slot. Going further back requires solving the
    slot and re-scrambling (costs ~30s simulated, like rescrambling on
    paper).
  - Per-move time cost: applying a move = 1s simulated.
  - NISS flip = 5s; slot operations = 10s; tool calls cost their search
    work scaled to wall-clock-equivalent.
  - The HTR finish is no longer A* + 663,552-entry PDB. It's a
    memoization-style lookup keyed by canonical HTR subset — a human
    memorizes ~96 of them; here the cache materializes lazily but the
    *budget* is sized as if pre-memorized.

The unconstrained `loop.py` stays as a comparison baseline.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import anthropic

from cube.classifier.htr import dr_subset_canonical, is_htr_ud
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.tools import algebra, library, policy, search, state

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

# Simulated-time costs (seconds of WCA wall, NOT real wall).
_COST_APPLY_MOVE = 1.0
_COST_NISS_FLIP = 5.0
_COST_SLOT_NEW = 10.0
_COST_SLOT_SWITCH = 2.0
_COST_RESCRAMBLE = 30.0
_COST_INSPECT = 5.0       # bumped 1->5: humans count by looking at the cube
_COST_TRY_ALG = 2.0
_COST_POLICY_INTUITION = 3.0
# Search tool simulated costs reflect "thinking time," not real CPU.
_COST_LOOKAHEAD = 8.0
_COST_DR_TRIGGER = 20.0
_COST_SUBSET_LOOKUP_CACHED = 1.0
_COST_SUBSET_LOOKUP_MISS = 15.0
_COST_HTR_SUBSET = 10.0   # bumped 2->10: subset recognition is real visual work

# Working-memory cap: humans don't perfectly recall a 25-move solve in
# their head. inspect_state shows only the last K moves of history; the
# agent must remember earlier moves in text.
_HISTORY_VISIBLE_TAIL = 20

# DR-trigger: humans evaluate 2-3 candidate triggers, not 5+.
_SIM_DR_TRIGGER_MAX_OPTIONS = 3

# Memorized finishes are imperfect — humans don't memorize the WCA-optimal
# finish, they memorize a good-enough one. Deterministic noise keyed by the
# canonical subset: each subset has a fixed +0..3 "memorization penalty."
_MEMORY_PENALTY_MAX_MOVES = 3

# Search budgets — tighter than the unconstrained loop.
# DR-trigger defaults bumped after the first sim run: at tail=2 the policy
# couldn't surface scramble 2's DR even at sw=512; at tail=3, sw=32 finds
# a 9-move DR (vs the unconstrained 7-move). This is the realistic
# operating point — wider tail recognizing more trigger states is more
# human-like than wider beam.
_SIM_LOOKAHEAD_WIDTH = 10
_SIM_LOOKAHEAD_DEPTH = 5
_SIM_DR_TRIGGER_SETUP_WIDTH = 32
_SIM_DR_TRIGGER_SETUP_DEPTH = 8
_SIM_DR_TRIGGER_TAIL = 3

_TOTAL_SIM_BUDGET = 3600.0  # one competition hour
_MAX_SLOTS = 3
_UNDO_LIMIT = 4


# ---------------------------------------------------------------------------
# State: slots + budget
# ---------------------------------------------------------------------------


@dataclass
class Slot:
    name: str
    history: list[str] = field(default_factory=list)
    on_inverse: bool = False  # tracks NISS frame
    # Bookkeeping: total moves ever appended. Undo can only walk back at most
    # _UNDO_LIMIT from `committed_floor`.
    committed_floor: int = 0


@dataclass
class BudgetTracker:
    sim_budget: float = _TOTAL_SIM_BUDGET
    sim_spent: float = 0.0
    real_start: float = field(default_factory=time.time)
    wall_limit_s: float = 3600.0
    events: list[dict] = field(default_factory=list)

    def charge(self, kind: str, cost: float, **info) -> None:
        self.sim_spent += cost
        self.events.append({"kind": kind, "cost": round(cost, 2), "sim_spent_after": round(self.sim_spent, 2), **info})

    def sim_remaining(self) -> float:
        return self.sim_budget - self.sim_spent

    def wall_remaining(self) -> float:
        return self.wall_limit_s - (time.time() - self.real_start)

    def exhausted(self) -> tuple[bool, str | None]:
        if self.sim_spent >= self.sim_budget:
            return True, "sim_budget"
        if self.wall_remaining() <= 0:
            return True, "wall_clock"
        return False, None


# Module-level cache: canonical HTR subset (tuple) -> {axis -> finish_moves}.
# A first cache miss costs the agent _COST_SUBSET_LOOKUP_MISS; subsequent
# hits are cheap. This is the "human memorized this subset" abstraction.
_SUBSET_FINISH_CACHE: dict[tuple, dict[str, list[str]]] = {}


def _load_subset_cache_from_disk() -> None:
    """Try to populate _SUBSET_FINISH_CACHE from checkpoints/subset_finish_cache.pkl
    if it exists. Generated by `python -m cube.agent.prewarm_subsets`."""
    import pickle
    from pathlib import Path
    cache_path = Path("checkpoints/subset_finish_cache.pkl")
    if not cache_path.exists():
        return
    try:
        with cache_path.open("rb") as f:
            disk_cache = pickle.load(f)
        # Merge into module cache (canonical -> {axis -> moves}).
        for canonical, axis_map in disk_cache.items():
            existing = _SUBSET_FINISH_CACHE.setdefault(canonical, {})
            for axis, finish in axis_map.items():
                existing.setdefault(axis, list(finish))
    except (pickle.UnpicklingError, OSError):
        pass


_load_subset_cache_from_disk()


# TODO: noisy memorization. Naive padding gets removed by cancel; need to
# return a genuinely-suboptimal PDB path (e.g. 2nd-shortest via backward
# walk with a perturbed heuristic). Land in a follow-up. The hook below
# is a placeholder so the limitation is visible in the output.


def _memory_quality_hint(canonical_subset: tuple, axis: str) -> str:
    """Returns a hint about how well-memorized this subset is. Decorative
    for now (until we land real suboptimal-PDB-walk noise); deterministic
    per (subset, axis) so reruns reproduce."""
    import hashlib
    h = hashlib.md5(repr((canonical_subset, axis)).encode()).digest()[0]
    bucket = h % 4
    return [
        "rehearsed (your memorization is sharp)",
        "rehearsed (a touch rusty)",
        "less-practiced (you may want to double-check)",
        "rarely-seen (you're working from first principles)",
    ][bucket]


# ---------------------------------------------------------------------------
# Tool handlers (budget-aware wrappers around cube.tools.*)
# ---------------------------------------------------------------------------


def _resolve_slot(slots: dict[str, Slot], name: str) -> Slot:
    if name not in slots:
        raise KeyError(f"unknown slot {name!r}. Existing: {sorted(slots.keys())}")
    return slots[name]


def _materialize(scramble: list[str], slot: Slot) -> tuple[list[str], list[str]]:
    """Return (effective_scramble, effective_history) for tool calls.

    NISS frame: when on_inverse, our convention mirrors algebra.niss_flip —
    the agent works on the inverse scramble and the tools see that inverse
    as the active scramble. We treat slot.history as moves on whichever
    frame the slot is currently on.
    """
    if slot.on_inverse:
        inv = list(algebra.invert(scramble)["inverted"])
        return inv, list(slot.history)
    return list(scramble), list(slot.history)


def _build_handlers(
    scramble: list[str],
    slots: dict[str, Slot],
    budget: BudgetTracker,
    *,
    lookahead_width: int = _SIM_LOOKAHEAD_WIDTH,
    lookahead_depth: int = _SIM_LOOKAHEAD_DEPTH,
    dr_trigger_setup_width: int = _SIM_DR_TRIGGER_SETUP_WIDTH,
    dr_trigger_setup_depth: int = _SIM_DR_TRIGGER_SETUP_DEPTH,
    dr_trigger_tail: int = _SIM_DR_TRIGGER_TAIL,
):
    """Return a name -> handler map closed over scramble/slots/budget."""

    def _h_inspect_state(args):
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = state.inspect_state(sc, hist)
        out["slot"] = slot.name
        out["on_inverse"] = slot.on_inverse
        out["undo_floor"] = slot.committed_floor
        out["undo_available"] = max(0, len(slot.history) - slot.committed_floor)
        # Working-memory cap: only surface the last N moves of history.
        full_len = len(slot.history)
        if full_len > _HISTORY_VISIBLE_TAIL:
            out["history_visible"] = list(slot.history[-_HISTORY_VISIBLE_TAIL:])
            out["history_truncated"] = full_len - _HISTORY_VISIBLE_TAIL
            out["history_note"] = (
                f"working-memory limit: showing last {_HISTORY_VISIBLE_TAIL} "
                f"moves of {full_len}. {out['history_truncated']} earlier "
                f"moves are not shown — you must remember them in text."
            )
        else:
            out["history_visible"] = list(slot.history)
            out["history_truncated"] = 0
        budget.charge("inspect_state", _COST_INSPECT, slot=slot.name)
        return out

    def _h_apply_moves(args):
        slot = _resolve_slot(slots, args["slot"])
        moves = list(args["moves"])
        slot.history.extend(moves)
        budget.charge("apply_moves", _COST_APPLY_MOVE * len(moves), slot=slot.name, n=len(moves))
        return {
            "slot": slot.name,
            "history": list(slot.history),
            "move_count": len(slot.history),
            "undo_available": max(0, len(slot.history) - slot.committed_floor),
        }

    def _h_undo_moves(args):
        slot = _resolve_slot(slots, args["slot"])
        n = int(args["n"])
        undo_available = len(slot.history) - slot.committed_floor
        if n > undo_available:
            return {
                "error": (
                    f"can undo at most {undo_available} moves on slot {slot.name!r}. "
                    f"To go further back, call reset_slot(slot={slot.name!r}, rescramble=True)."
                ),
            }
        if n > _UNDO_LIMIT:
            return {"error": f"undo limit per call is {_UNDO_LIMIT} moves."}
        slot.history = slot.history[:-n] if n > 0 else slot.history
        # Undoing 1 move = applying its inverse on the physical cube; same cost.
        budget.charge("undo_moves", _COST_APPLY_MOVE * n, slot=slot.name, n=n)
        return {
            "slot": slot.name,
            "history": list(slot.history),
            "move_count": len(slot.history),
            "undo_available": max(0, len(slot.history) - slot.committed_floor),
        }

    def _h_reset_slot(args):
        slot = _resolve_slot(slots, args["slot"])
        rescramble = bool(args.get("rescramble", True))
        slot.history = []
        slot.on_inverse = False
        slot.committed_floor = 0
        cost = _COST_RESCRAMBLE if rescramble else _COST_APPLY_MOVE * 4
        budget.charge("reset_slot", cost, slot=slot.name, rescramble=rescramble)
        return {"slot": slot.name, "reset": True, "rescramble": rescramble}

    def _h_new_slot(args):
        if len(slots) >= _MAX_SLOTS:
            return {"error": f"all {_MAX_SLOTS} slots are in use: {sorted(slots.keys())}. Reset or copy into an existing slot."}
        name = args["name"]
        if name in slots:
            return {"error": f"slot {name!r} already exists."}
        copy_from = args.get("copy_from")
        if copy_from:
            src = _resolve_slot(slots, copy_from)
            slots[name] = Slot(name=name, history=list(src.history), on_inverse=src.on_inverse, committed_floor=src.committed_floor)
        else:
            slots[name] = Slot(name=name)
        budget.charge("new_slot", _COST_SLOT_NEW, slot=name, copy_from=copy_from)
        return {"slot": name, "history": list(slots[name].history), "slots_in_use": sorted(slots.keys())}

    def _h_niss_flip(args):
        slot = _resolve_slot(slots, args["slot"])
        slot.on_inverse = not slot.on_inverse
        budget.charge("niss_flip", _COST_NISS_FLIP, slot=slot.name)
        sc, hist = _materialize(scramble, slot)
        out = algebra.niss_flip(scramble, slot.history)  # report the agent-visible flip
        out["slot"] = slot.name
        out["now_on_inverse"] = slot.on_inverse
        return out

    def _h_policy_intuition(args):
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = policy.policy_intuition(sc, hist, k=args.get("k", 5))
        budget.charge("policy_intuition", _COST_POLICY_INTUITION, slot=slot.name)
        return out

    def _h_try_alg(args):
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = state.try_alg(sc, hist, args["alg"])
        budget.charge("try_alg", _COST_TRY_ALG, slot=slot.name, n=len(args["alg"]))
        return out

    def _h_lookahead(args):
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = search.lookahead(
            sc, hist,
            target=args["target"], axis=args.get("axis"),
            width=lookahead_width, depth=lookahead_depth,
        )
        budget.charge("lookahead", _COST_LOOKAHEAD, slot=slot.name, target=args["target"])
        return out

    def _truncate_dr_options(out: dict) -> dict:
        # Human eye sees a handful of triggers, not 5+. Top-3 by length+log_prob.
        if isinstance(out.get("options"), list) and len(out["options"]) > _SIM_DR_TRIGGER_MAX_OPTIONS:
            out["options"] = out["options"][:_SIM_DR_TRIGGER_MAX_OPTIONS]
            out["found"] = len(out["options"])
            out["note_truncated"] = (
                f"showing only top {_SIM_DR_TRIGGER_MAX_OPTIONS} triggers; "
                f"deeper enumeration is beyond a human's visualization scope."
            )
        return out

    def _h_find_dr_via_trigger(args):
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = search.find_dr_via_trigger(
            sc, hist,
            axis=args["axis"],
            tail_length=dr_trigger_tail,
            setup_width=dr_trigger_setup_width,
            setup_depth=dr_trigger_setup_depth,
        )
        out = _truncate_dr_options(out)
        budget.charge("find_dr_via_trigger", _COST_DR_TRIGGER, slot=slot.name, axis=args["axis"])
        return out

    def _h_probe_dr(args):
        """Run find_dr_via_trigger as if `eo_alg` were appended to history,
        WITHOUT modifying the slot. Lets the agent compare DR feasibility
        across candidate EOs before committing to one."""
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        hypothetical_hist = list(hist) + list(args["eo_alg"])
        out = search.find_dr_via_trigger(
            sc, hypothetical_hist,
            axis=args["axis"],
            tail_length=dr_trigger_tail,
            setup_width=dr_trigger_setup_width,
            setup_depth=dr_trigger_setup_depth,
        )
        out = _truncate_dr_options(out)
        out["probed_with_eo"] = list(args["eo_alg"])
        budget.charge("probe_dr_after_eo", _COST_DR_TRIGGER, slot=slot.name, axis=args["axis"])
        return out

    def _h_cancel(args):
        out = algebra.cancel(args["moves"])
        # Charge a tiny bookkeeping cost; cancellation is mechanical so don't penalize it.
        budget.charge("cancel", 1.0, n_before=len(args["moves"]))
        return out

    def _h_htr_subset(args):
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = library.htr_subset(sc, hist)
        budget.charge("htr_subset", _COST_HTR_SUBSET, slot=slot.name)
        return out

    def _h_lookup_subset_finish(args):
        """Memorization-style HTR finish.

        Strong humans recognize the HTR-corner-subset and execute a
        rehearsed finish. We approximate that by caching the optimal
        finish per (canonical_subset_form, axis); a cache miss is the
        "first time you've seen this subset" cost.
        """
        slot = _resolve_slot(slots, args["slot"])
        axis = args["axis"]
        sc, hist = _materialize(scramble, slot)
        s = SOLVED.apply_alg(parse_alg(" ".join(sc))) if sc else SOLVED
        if hist:
            s = s.apply_alg(parse_alg(" ".join(hist)))

        canonical = dr_subset_canonical(s)
        if canonical is None:
            return {"error": "current state is not in DR-corner subgroup; no subset to look up."}

        cache_key = tuple(canonical)
        if cache_key in _SUBSET_FINISH_CACHE and axis in _SUBSET_FINISH_CACHE[cache_key]:
            finish = _SUBSET_FINISH_CACHE[cache_key][axis]
            quality = _memory_quality_hint(cache_key, axis)
            budget.charge("lookup_subset_finish", _COST_SUBSET_LOOKUP_CACHED, slot=slot.name, axis=axis, cached=True, subset=list(canonical))
            return {
                "subset_canonical": list(canonical),
                "axis": axis,
                "finish_moves": list(finish),
                "length": len(finish),
                "cached": True,
                "memory_quality": quality,
                "note": f"Recognized subset — playing memorized finish ({quality}).",
            }

        # Cache miss: compute via the existing PDB. From the agent's
        # perspective this is the "first time learning this subset" cost.
        if not is_htr_ud(s):
            # The full finish requires reaching canonical HTR first, then
            # half-turn finish. Reuse the unconstrained solve_htr_and_finish.
            full = search.solve_htr_and_finish_from_dr(sc, hist, axis=axis)
            if "error" in full:
                budget.charge("lookup_subset_finish", _COST_SUBSET_LOOKUP_MISS, slot=slot.name, axis=axis, cached=False)
                return full
            combined = list(full["htr_moves"]) + list(full["finish_moves"])
            _SUBSET_FINISH_CACHE.setdefault(cache_key, {})[axis] = combined
            budget.charge("lookup_subset_finish", _COST_SUBSET_LOOKUP_MISS, slot=slot.name, axis=axis, cached=False, subset=list(canonical))
            return {
                "subset_canonical": list(canonical),
                "axis": axis,
                "finish_moves": combined,
                "length": len(combined),
                "cached": False,
                "note": (
                    "First exposure to this subset — derived finish and memorized "
                    "it. Future calls for the same subset are cheap."
                ),
            }
        # Already in canonical HTR: just half-turn finish.
        from cube.classifier.htr import htr_solve
        finish = htr_solve(s)
        if finish is None:
            budget.charge("lookup_subset_finish", _COST_SUBSET_LOOKUP_MISS, slot=slot.name, axis=axis, cached=False)
            return {"error": "htr_solve PDB returned None."}
        moves_str = [str(m) for m in finish]
        _SUBSET_FINISH_CACHE.setdefault(cache_key, {})[axis] = moves_str
        budget.charge("lookup_subset_finish", _COST_SUBSET_LOOKUP_MISS, slot=slot.name, axis=axis, cached=False, subset=list(canonical))
        return {
            "subset_canonical": list(canonical),
            "axis": axis,
            "finish_moves": moves_str,
            "length": len(moves_str),
            "cached": False,
            "note": "First exposure to this subset — memorized.",
        }

    def _h_verify_solved(args):
        # Verification is free — corresponds to the judge accepting the sheet.
        return state.verify_solved(scramble, args["solution"])

    def _h_budget_status(args):
        return {
            "sim_spent": round(budget.sim_spent, 2),
            "sim_remaining": round(budget.sim_remaining(), 2),
            "sim_budget": budget.sim_budget,
            "wall_remaining_s": round(budget.wall_remaining(), 1),
            "slots": {
                n: {
                    "history": list(s.history),
                    "move_count": len(s.history),
                    "on_inverse": s.on_inverse,
                    "undo_available": max(0, len(s.history) - s.committed_floor),
                }
                for n, s in slots.items()
            },
        }

    return {
        "inspect_state": _h_inspect_state,
        "apply_moves": _h_apply_moves,
        "undo_moves": _h_undo_moves,
        "reset_slot": _h_reset_slot,
        "new_slot": _h_new_slot,
        "niss_flip": _h_niss_flip,
        "policy_intuition": _h_policy_intuition,
        "try_alg": _h_try_alg,
        "lookahead": _h_lookahead,
        "find_dr_via_trigger": _h_find_dr_via_trigger,
        "probe_dr_after_eo": _h_probe_dr,
        "cancel": _h_cancel,
        "htr_subset": _h_htr_subset,
        "lookup_subset_finish": _h_lookup_subset_finish,
        "verify_solved": _h_verify_solved,
        "budget_status": _h_budget_status,
    }


# ---------------------------------------------------------------------------
# Tool schemas
# ---------------------------------------------------------------------------

_MOVE_LIST = {"type": "array", "items": {"type": "string"}}
_SLOT = {"type": "string", "description": "Slot name (default slot is 'main')."}


def _tool_schemas() -> list[dict]:
    return [
        {
            "name": "inspect_state",
            "description": "Look at the cube state in a slot. Returns EO/CO per axis, DR/HTR flags, move count, NISS-frame, undo_available.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT}, "required": ["slot"]},
        },
        {
            "name": "apply_moves",
            "description": "Commit moves to a slot's history. Costs 1s simulated time per move. Use this when you've decided on a continuation.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "moves": _MOVE_LIST}, "required": ["slot", "moves"]},
        },
        {
            "name": "undo_moves",
            "description": f"Undo the last n moves on a slot (n ≤ {_UNDO_LIMIT}). Costs 1s per move undone. If you need to go further back, call reset_slot.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "n": {"type": "integer", "minimum": 1, "maximum": _UNDO_LIMIT}}, "required": ["slot", "n"]},
        },
        {
            "name": "reset_slot",
            "description": f"Reset a slot back to the scramble (history=[], on_inverse=False). Costs {_COST_RESCRAMBLE}s simulated (modeled as solving + rescrambling on paper).",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "rescramble": {"type": "boolean", "default": True}}, "required": ["slot"]},
        },
        {
            "name": "new_slot",
            "description": f"Create a new cube-state slot (up to {_MAX_SLOTS} total). Optionally copy_from another slot's current state.",
            "input_schema": {"type": "object", "properties": {"name": {"type": "string"}, "copy_from": {"type": "string"}}, "required": ["name"]},
        },
        {
            "name": "niss_flip",
            "description": "Toggle the slot's NISS frame (normal ↔ inverse). Subsequent tool calls on this slot see the flipped scramble.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT}, "required": ["slot"]},
        },
        {
            "name": "policy_intuition",
            "description": "Top-k 'intuition' moves from the trained policy. Use sparingly; this is your gut, not search.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5}}, "required": ["slot"]},
        },
        {
            "name": "try_alg",
            "description": "Preview applying an alg on top of a slot's history WITHOUT committing. Cheap (2s simulated).",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "alg": _MOVE_LIST}, "required": ["slot", "alg"]},
        },
        {
            "name": "lookahead",
            "description": (
                f"Bounded look-ahead from a slot (width={_SIM_LOOKAHEAD_WIDTH}, depth={_SIM_LOOKAHEAD_DEPTH}) — about what a human "
                f"can visualize. ONLY for target=eo or target=solved. For DR use find_dr_via_trigger; "
                f"for HTR/finish use htr_subset then lookup_subset_finish."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "target": {"type": "string", "enum": ["eo", "solved"]},
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                },
                "required": ["slot", "target"],
            },
        },
        {
            "name": "find_dr_via_trigger",
            "description": f"Trigger-then-tail DR search (setup_width={_SIM_DR_TRIGGER_SETUP_WIDTH}, setup_depth={_SIM_DR_TRIGGER_SETUP_DEPTH}). EO on `axis` must already be solved in the slot.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "axis": {"type": "string", "enum": ["UD", "FB", "RL"]}}, "required": ["slot", "axis"]},
        },
        {
            "name": "cancel",
            "description": "Apply local move cancellation (same-face merge, through-axis-commute). Mechanical, cheap. Use just before submitting to collapse the final solution.",
            "input_schema": {"type": "object", "properties": {"moves": _MOVE_LIST}, "required": ["moves"]},
        },
        {
            "name": "probe_dr_after_eo",
            "description": (
                "Run find_dr_via_trigger AS IF the given eo_alg were appended to the slot's history, "
                "WITHOUT actually modifying the slot. Use this to compare DR feasibility across "
                "candidate EOs before committing. Same simulated cost as find_dr_via_trigger."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "eo_alg": {**_MOVE_LIST, "description": "Hypothetical EO moves to test."},
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                },
                "required": ["slot", "eo_alg", "axis"],
            },
        },
        {
            "name": "htr_subset",
            "description": "Identify the canonical HTR-corner-subset of the slot. Use after reaching DR — name the subset before looking up its finish.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT}, "required": ["slot"]},
        },
        {
            "name": "lookup_subset_finish",
            "description": (
                "Look up the memorized HTR finish for the slot's current canonical subset. "
                "First exposure to a subset is expensive (you 'learn' it); repeats are cheap. "
                "Returns the half-turn finish_moves. Apply them with apply_moves to complete the solve."
            ),
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "axis": {"type": "string", "enum": ["UD", "FB", "RL"]}}, "required": ["slot", "axis"]},
        },
        {
            "name": "verify_solved",
            "description": "Ground-truth check on a candidate full solution. Free (judge accepts the sheet).",
            "input_schema": {"type": "object", "properties": {"solution": _MOVE_LIST}, "required": ["solution"]},
        },
        {
            "name": "budget_status",
            "description": "Snapshot of simulated and real-wall remaining + current slot summaries. Free.",
            "input_schema": {"type": "object", "properties": {}},
        },
    ]


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """\
You are an expert Rubik's Cube FMC solver in a SIMULATED COMPETITION.

# Rules (match WCA FMC)
- You have ONE HOUR total simulated time (3600 seconds budget).
- You operate on up to {max_slots} named cube-state slots (start with 'main').
- Per slot you have a {undo_limit}-move undo buffer. To go back further you
  must reset_slot (costs {rescramble_cost}s — like solving + rescrambling on paper).
- Applying each move costs 1s simulated.
- Looking ahead costs simulated time too: lookahead ~{cost_lookahead}s,
  find_dr_via_trigger ~{cost_dr_trigger}s, policy_intuition ~{cost_policy}s.
- The HTR finish is NOT a brute-force solver. It is a memorized lookup:
  first time you see a subset you 'learn' it ({cost_subset_miss}s); future
  uses are nearly free ({cost_subset_hit}s). So get to DR, identify the
  subset with htr_subset, then lookup_subset_finish.
- Call budget_status whenever you want to see how much time you have left.

# FMC technique reference (use this vocabulary in your narration)

### EO (Edge Orientation) — ALGORITHMIC, not search
EO is fundamentally algorithmic. Each bad-edge configuration has known
fix patterns; lookahead/policy are CONFIRMATION tools, not the primary
finder. Workflow on the cube:

1. Read `bad_edges_per_axis` AND `bad_edge_slots_per_axis` from inspect_state.
2. The flipping moves per axis are:
   - **UD-axis EO**: F, F', B, B' (quarter turns of F/B flip UD-EO)
   - **FB-axis EO**: L, L', R, R' (quarter turns of L/R flip FB-EO)
   - **RL-axis EO**: U, U', D, D' (quarter turns of U/D flip RL-EO)
   Half turns and axis-moves preserve EO.
3. A flip move toggles the 4 edges on its face. So a single flip move
   changes bad-edge-count by ±4 or ±2 or 0 depending on how many of that
   face's edges were already bad.

**By bad-edge count (on chosen axis)**:
- **0**: solved on this axis. Done.
- **2**: ONE-MOVE solutions exist when the two bad edges sit on
  perpendicular faces that share one flipping face. E.g., on UD-axis,
  if the 2 bad edges are both on the F face (after-state) → F fixes
  both. Bad edges on opposite sides of the same flipping axis → 2 moves
  needed. Look at `bad_edge_slots_per_axis` and try the flipping move
  that touches both slot names.
- **4**: typically 1-3 moves. Strong cases:
  - All 4 on one flipping face → 1 move (F or B on UD-axis).
  - 2 on F, 2 on B → 2 moves (F + B or similar).
  - Scattered → 3-4 moves using a setup. Common: `U B U'` shape that
    rotates 2 edges onto F before the F flip.
- **6**: usually 2-4 moves. The `<setup> F <setup'> B` symmetry pattern
  works when the configuration is roughly symmetric on the flipping axis.
- **8**: 3-5 moves. Classic `<m> F <m'> B` symmetry — find a 1-2 move
  setup `<m>` that puts 4 bad edges on F, then `F <m'> B` flips both
  4-groups. NISS-trace the inverse: 1-move-to-8-bad often gives sub5 EO.
- **10**: rare. Usually NISS to inverse helps.
- **12**: all-bad. Two flips on opposite faces don't cancel cleanly;
  typically NISS.

**Procedure** (per axis):
1. Note the bad-edge count and slot names from inspect_state.
2. Identify which flipping moves touch which bad edges (e.g., F touches
   slots UF, FR, DF, FL). A single flip "fixes" any of those that were
   bad and "breaks" any that were good.
3. If a one-move fix exists, you'll see it directly: a single flipping
   move where ALL the moves' affected slots were currently bad.
4. Otherwise enumerate 2-3 move setups manually using try_alg. The
   transformer's policy_intuition gives top-k starting moves; combine
   with the algorithmic count to pick which try_alg to test.
5. Once you have a candidate sequence, lookahead/probe_dr_after_eo
   confirms it (or finds a 1-move-shorter alternative).

**Axis selection rule of thumb**:
- Smallest bad-edge count is usually shortest EO BUT not always.
- A scrambled state with 2 bad edges on UD that DON'T share a flipping
  face needs ~3-4 moves. A state with 4 bad edges on FB all clustered
  may need only 1 move. **Check the slot pattern, not just the count.**

NISS-EO trigger: 1-move reduction to 4 bad edges → niss-trace the
inverse for sub5 EOs. Trace good-edges (not bad) when looking at
1-move-to-8-bad.

### NISS Decision Rules
- After EO: only switch if you have very few EOs of the shortest length. Otherwise stay.
- After RZP: switch in 5; switch in 6 only if **JZP** or **DR-2e3c**.
- JZP preserves across axes: if you have JZP on normal, the OTHER axis after switching also has JZP — switch even for marginal 2c6e-JZP if it becomes 4e4c.
- ARM swaps axes on switch; use ARM stats on the opposite axis to decide.

### RZP → DR
RZP = "completely random moves" between EO and DR. Look for rzps of length ≤5 (≤6 if JZP/3c2e). Standard triggers:
- `R` → **DR-4c4e** (most common, grind this)
- `R U2 R'` → **DR-4c2e**
- `R U R'` or `R U' R'` → **DR-3c2e**
- `R U2 F2 R` → DR-4c4e variant
- Advanced: `R U L` → DR-7c8e; `R L` → DR-8c8e; `R U2 F2 U2 R` → DR-2e; `R U2 D2 L` → DR-4e

DR length targets: sub-15 beginner, sub-12 intermediate, sub-11 advanced. Abandon RZP if intuition says bad — don't sink time unless rzp ≤3.

**JZP requirements**: no U/D corner stickers on R/L; no E-slice edges in M-slice; even number of unoriented corners. Cases like 4c6e/2c2e/2c4e become viable (5-6 to DR).

**ARM** (Axial Reduction Minus): how close the *other* axis is to JZP. Count misoriented corner stickers WITHOUT F/B color, plus misoriented E-layer edges.

**Pairs tracing** (Wen): for each E-slice edge not in its slice, check the misoriented corner whose two slice-facing stickers match the edge — that's a pair on inverse. Switch on 2+ pairs.

### HTR (Half-Turn Reduction)
Solvable with only double turns. 0-5 quarter-turn corners remain after DR. HTR triggers: `R`, `R U2 R'`, `R U2 F2 R`. Process: count qt → reduce/grow to 1 or 2 qt → setup to trigger.

**HTR corner subsets** (with approx DR→solved finish lengths):
- **4a1** ~12.5 — good
- **4b2** ~12.5 — good, learn 4b2+4e cases
- **4a2** ~13.3
- **4c3** ~13.4
- **2c3** ~12.9
- **2c4** ~13.7 — hard, expect longer

The "a/b" letter distinguishes corner orbit shape; "c" generally means worse subsets.

### Finish (from HTR)
Any state is solvable in ≤14 moves from HTR. Practical: solve corners + as many edges as possible, then edge commutators on the rest. Or **Floppy Reduction** (FR): reduce to `<R2 L2 F2 B2>` along DR axis, solve the domino layers ignoring the middle slice.

### Insertions & Commutators
After skeleton with corners off:
- **3c** → 1 commutator (8 moves pure, often cancels)
- **3c1t / 2c2t / 5c / 3c3c / 2t / 3t** → 2 commutators
- 4c1t / 3c2t / 4t / 5t → 3+ comms, generally abandon

A commutator affects exactly 3 corners; slide through the solution for cancellations.

### DR-Xs (Slice EO Method)
Replaces full EO with **slice EO**: orient only the 4 edges of ONE slice on one axis. Often a 0-1 move skip exists. NISS does NOT preserve slice EO.

Pipeline: slice-EO → rzp-Xs → DR-2s → DR-1s → real DR → HTR → finish.

**DR-1s break-even**: 8-move DR-1s ≈ 11-move normal DR (~2.5 moves extra on average). Use when: slice EO skip or 1-mover exists AND DR-1s reachable in ≤8 moves.

**DR-2s 8fe special case**: when all 8 non-slice edges flipped, go straight to HTR-2s — only ~1 move worse than normal DR. Look for `U R L` substitutions becoming `D U R L` (-2 moves).

### Vocabulary
RZP, JZP, JEO, ARM, AR-XcYe, DRM, "trigger" (R, RU2R', RUR'), 4c4e/3c2e/4c2e, "4 bad edges," "niss-trace," "premove," "pairs tracing," "qt corners," AB3c (All But 3 corners), slice EO, DR-1s/-2s, "leave slice," floppy reduction, hyperparity, HTR subset (4a1/4b2/4a2/4c3/2c3/2c4).

### Time Budget (your 1-hour solve)
- 0-10 min: enumerate EOs across axes/sides
- 10-35 min: check EOs, find rzps, find DRs
- 35-60 min: solve best DR through HTR + finish + insertions

# The scramble (exactly {scramble_length} moves)
{scramble_str}

JSON form (always pass this to verify_solved, never retype the scramble):
  scramble = {scramble_json}

# Pipeline (the realistic version)
1. **EO scan** — call lookahead(target='eo', axis=X) for ALL THREE axes
   (UD, FB, RL). You're enumerating candidate openings, not committing
   yet. Costs ~24s simulated total but is essential.
2. **DR probe BEFORE committing to EO** — this is the most important
   strategy rule. For each axis that found a short EO, call
   probe_dr_after_eo(slot='main', eo_alg=[that EO's moves], axis=X).
   This tells you "if I commit this EO, can I find DR?" without
   actually committing. Pick the EO whose probe returns the shortest
   total = len(eo_alg) + best DR length. The shortest EO alone is NOT
   the best — a 4-move EO that probes to a 7-move DR (= 11 total) beats
   a 2-move EO that probes to no DR (force NISS / fail).
3. **Commit EO**: apply_moves with the chosen axis's EO sequence.
4. **DR**: find_dr_via_trigger(axis=X) — apply the winning option (the
   probe already proved it works). If somehow no DR is found at this
   step, try NISS or reset_slot and try a different EO axis. Do NOT
   manually build DR setup chains by guessing — that burns 10+ tool
   calls. Reset and try the next axis instead.
5. **HTR**: this is a TWO-STEP process, no exceptions.
   a) htr_subset(slot='main') — identifies the canonical subset.
   b) lookup_subset_finish(slot='main', axis=X) — returns the
      memorized finish_moves.
   Then apply_moves(finish_moves). Do NOT call lookahead(target='htr')
   or any DR-search after DR is reached — it will not work and wastes
   tool calls. Trust the lookup.
6. verify_solved(solution=full_history_in_solve_order).

# Strategy notes

**SHIP RULE (read this twice)**: the primary goal is producing a
SOLVED solution within budget. Any verified solve under 50 moves
beats a timeout. Once you have a working complete solution
(EO + DR + finish, verified by verify_solved), CALL FINAL_SOLUTION
and STOP. Do NOT keep searching for shorter alternatives unless you
have a very specific reason (e.g. you can see your current solution
has 4+ obviously cancellable moves and a quick try_alg would confirm).
The FMC theory targets ("sub-15 DR is advanced", etc.) are aspirational
for STRONG HUMANS over many practice solves — not requirements for
this attempt. A 33-move solve in 15 minutes beats a DNF chasing 25.

- **Test before commit**: a 4-move EO probed with find_dr_via_trigger is
  cheaper than a 2-move EO followed by 30 tool calls of manual DR
  exploration that goes nowhere. Always test ALL viable EO axes' DR
  options first.
- **apply_moves has NO upper cap** — you can apply as many moves as you
  want. Only undo_moves is capped at {undo_limit} per call. If you commit
  10 moves you can't undo all 10; use reset_slot if you need to.
- **try_alg is your cheap probe** (2s sim). Use it constantly to look
  at after-states without committing. It does NOT modify the slot.
- Slots are precious. Don't proliferate. Default: do everything in 'main'.
- NISS is cheap (~{cost_niss}s) and powerful — use it when stuck.
- **Before submitting**: call cancel(moves=your_full_solution) to collapse
  any adjacent same-face moves (e.g. `U U2` → `U'`). It's cheap and often
  saves 1-3 moves.
- Submit by calling verify_solved AND outputting on its own line:
    FINAL_SOLUTION: ["R", "U'", ...]
- The inverse-of-scramble is the trivial floor and does NOT count.

# Reasoning style
Before each tool call, narrate in 1-2 sentences: what you observed, what
hypothesis you're testing, why you picked this tool. This transcript is the
deliverable — your visible reasoning is the product.
"""


# ---------------------------------------------------------------------------
# Solution extraction
# ---------------------------------------------------------------------------

_FINAL_RE = re.compile(r"FINAL[_ ]SOLUTION\s*:\s*(\[[^\]]*\])", re.IGNORECASE)


def _extract_solution(text: str) -> list[str] | None:
    m = _FINAL_RE.search(text)
    if not m:
        return None
    try:
        parsed = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, list) or not all(isinstance(x, str) for x in parsed):
        return None
    return parsed


def _format_text_blocks(blocks) -> str:
    return "\n".join(b.text for b in blocks if getattr(b, "type", None) == "text")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def solve(
    scramble: list[str],
    *,
    model: str = DEFAULT_MODEL,
    max_tool_calls: int = 80,
    verbose: bool = False,
    thinking_budget: int = 3000,
    transcript_path: Path | None = None,
    wall_limit_s: float = 3600.0,
    sim_budget: float = _TOTAL_SIM_BUDGET,
    dr_trigger_setup_width: int = _SIM_DR_TRIGGER_SETUP_WIDTH,
    dr_trigger_setup_depth: int = _SIM_DR_TRIGGER_SETUP_DEPTH,
) -> dict:
    client = anthropic.Anthropic()
    slots: dict[str, Slot] = {"main": Slot(name="main")}
    budget = BudgetTracker(sim_budget=sim_budget, wall_limit_s=wall_limit_s)
    handlers = _build_handlers(
        scramble, slots, budget,
        dr_trigger_setup_width=dr_trigger_setup_width,
        dr_trigger_setup_depth=dr_trigger_setup_depth,
    )
    tool_schemas = _tool_schemas()

    scramble_json = json.dumps(scramble)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        scramble_str=" ".join(scramble),
        scramble_json=scramble_json,
        scramble_length=len(scramble),
        max_slots=_MAX_SLOTS,
        undo_limit=_UNDO_LIMIT,
        rescramble_cost=int(_COST_RESCRAMBLE),
        cost_lookahead=int(_COST_LOOKAHEAD),
        cost_dr_trigger=int(_COST_DR_TRIGGER),
        cost_policy=int(_COST_POLICY_INTUITION),
        cost_subset_miss=int(_COST_SUBSET_LOOKUP_MISS),
        cost_subset_hit=int(_COST_SUBSET_LOOKUP_CACHED),
        cost_niss=int(_COST_NISS_FLIP),
    )
    user_msg = f"Solve this scramble within your one-hour budget. Start with inspect_state(slot='main')."

    messages: list[dict[str, Any]] = [{"role": "user", "content": user_msg}]
    transcript: list[dict[str, Any]] = [
        {"type": "system", "content": system_prompt},
        {"type": "user", "content": user_msg},
    ]

    tool_calls = 0
    input_tokens = 0
    output_tokens = 0
    cache_read_tokens = 0
    cache_create_tokens = 0
    final_solution: list[str] = []
    solves = False
    halt_reason: str | None = None
    per_turn_usage: list[dict] = []
    turn_idx = 0

    def _slot_snapshot() -> dict:
        return {
            n: {
                "history": list(s.history),
                "on_inverse": s.on_inverse,
                "move_count": len(s.history),
                "undo_available": max(0, len(s.history) - s.committed_floor),
            }
            for n, s in slots.items()
        }

    def _snapshot() -> dict:
        # Compute cost estimate with Sonnet 4.5 pricing (cached ~$0.30/M, non-cached $3/M in, $15/M out).
        cached = cache_read_tokens
        fresh_in = input_tokens - cached
        cost_estimate = (cached * 0.30 + fresh_in * 3.0 + output_tokens * 15.0) / 1_000_000
        return {
            "scramble": scramble,
            "model": model,
            "final_solution": final_solution,
            "solves": solves,
            "total_moves": len(final_solution),
            "tool_calls": tool_calls,
            "halt_reason": halt_reason,
            "sim_spent": round(budget.sim_spent, 2),
            "sim_budget": budget.sim_budget,
            "wall_elapsed_s": round(time.time() - budget.real_start, 1),
            "budget_events": budget.events,
            "slots_final": _slot_snapshot(),
            "transcript": transcript,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_read_tokens": cache_read_tokens,
            "cache_create_tokens": cache_create_tokens,
            "per_turn_usage": per_turn_usage,
            "cost_estimate_usd": round(cost_estimate, 4),
        }

    def _checkpoint() -> None:
        if transcript_path is None:
            return
        try:
            with transcript_path.open("w") as f:
                json.dump(_snapshot(), f, indent=2, default=str)
        except OSError:
            pass

    if verbose:
        print(f"[sim] scramble: {' '.join(scramble)}")
        print(f"[sim] model: {model}  budget: {sim_budget}s sim, {wall_limit_s}s wall")

    while tool_calls < max_tool_calls:
        exhausted, why = budget.exhausted()
        if exhausted:
            halt_reason = why
            if verbose:
                print(f"[sim] budget exhausted: {why}")
            break

        api_kwargs: dict[str, Any] = dict(
            model=model,
            max_tokens=max(4096, thinking_budget + 2048),
            system=system_prompt,
            tools=tool_schemas,
            messages=messages,
        )
        if thinking_budget > 0:
            api_kwargs["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}
        turn_t0 = time.time()
        resp = client.messages.create(**api_kwargs)
        turn_elapsed = time.time() - turn_t0
        turn_idx += 1
        usage = resp.usage
        turn_in = usage.input_tokens
        turn_out = usage.output_tokens
        turn_cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
        turn_cache_create = getattr(usage, "cache_creation_input_tokens", 0) or 0
        input_tokens += turn_in
        output_tokens += turn_out
        cache_read_tokens += turn_cache_read
        cache_create_tokens += turn_cache_create
        per_turn_usage.append({
            "turn": turn_idx,
            "wall_s_elapsed": round(time.time() - budget.real_start, 2),
            "turn_wall_s": round(turn_elapsed, 2),
            "sim_spent_at_turn": round(budget.sim_spent, 2),
            "input_tokens": turn_in,
            "output_tokens": turn_out,
            "cache_read_tokens": turn_cache_read,
            "cache_create_tokens": turn_cache_create,
            "stop_reason": resp.stop_reason,
        })

        assistant_content = [b.model_dump() for b in resp.content]
        transcript.append({
            "type": "assistant",
            "turn": turn_idx,
            "wall_s_elapsed": round(time.time() - budget.real_start, 2),
            "turn_wall_s": round(turn_elapsed, 2),
            "input_tokens": turn_in,
            "output_tokens": turn_out,
            "cache_read_tokens": turn_cache_read,
            "cache_create_tokens": turn_cache_create,
            "content": assistant_content,
            "stop_reason": resp.stop_reason,
        })
        messages.append({"role": "assistant", "content": assistant_content})

        if verbose:
            for b in resp.content:
                btype = getattr(b, "type", None)
                if btype == "thinking":
                    thinking_text = getattr(b, "thinking", "") or ""
                    if thinking_text:
                        print(f"\n[thinking]\n{thinking_text}")
            text_out = _format_text_blocks(resp.content)
            if text_out:
                print(f"\n[claude]\n{text_out}")

        tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]

        if tool_uses:
            tool_results = []
            for tu in tool_uses:
                tool_calls += 1
                if verbose:
                    print(f"\n[tool#{tool_calls}] {tu.name}({json.dumps(tu.input)[:200]})")
                handler = handlers.get(tu.name)
                if handler is None:
                    result = {"error": f"unknown tool: {tu.name}"}
                else:
                    try:
                        result = handler(tu.input)
                    except Exception as e:
                        result = {"error": f"{type(e).__name__}: {e}"}
                if verbose:
                    print(f"[result] {json.dumps(result)[:300]}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": json.dumps(result),
                })
                transcript.append({
                    "type": "tool_call",
                    "turn": turn_idx,
                    "tool_index": tool_calls,
                    "name": tu.name,
                    "input": tu.input,
                    "result": result,
                    "sim_spent": round(budget.sim_spent, 2),
                    "wall_s_elapsed": round(time.time() - budget.real_start, 2),
                    "slots_after": _slot_snapshot(),
                })
                if tool_calls >= max_tool_calls:
                    break
            messages.append({"role": "user", "content": tool_results})
            _checkpoint()
            continue

        text = _format_text_blocks(resp.content)
        proposed = _extract_solution(text)
        if proposed is not None:
            check = state.verify_solved(scramble, proposed)
            transcript.append({"type": "verify", "solution": proposed, "result": check})
            if check["solves"]:
                final_solution = proposed
                solves = True
                if verbose:
                    print(f"\n[sim] SOLVED in {check['total_moves']} moves "
                          f"(sim_spent={budget.sim_spent:.1f}s of {budget.sim_budget}s)")
                break
            feedback = (
                f"Your proposed solution does NOT solve the scramble. "
                f"verify_solved returned {json.dumps(check)}. Keep working — "
                f"inspect the slot to see the residual state."
            )
            messages.append({"role": "user", "content": feedback})
            transcript.append({"type": "user", "content": feedback})
            continue

        if resp.stop_reason == "end_turn":
            nudge = (
                "You stopped without calling tools or emitting FINAL_SOLUTION. "
                "Either continue with tools, or output FINAL_SOLUTION: [\"...\", ...]."
            )
            messages.append({"role": "user", "content": nudge})
            transcript.append({"type": "user", "content": nudge})
            continue

        break

    if halt_reason is None and tool_calls >= max_tool_calls:
        halt_reason = "max_tool_calls"

    return _snapshot()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simulated-FMC agent run.")
    parser.add_argument("scramble", help="Scramble in WCA notation (space-separated).")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-tool-calls", type=int, default=80)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--thinking-budget", type=int, default=3000)
    parser.add_argument("--wall-limit-s", type=float, default=3600.0)
    parser.add_argument("--sim-budget", type=float, default=_TOTAL_SIM_BUDGET)
    parser.add_argument(
        "--dr-trigger-setup-width", type=int, default=_SIM_DR_TRIGGER_SETUP_WIDTH,
        help="Beam width for find_dr_via_trigger setup search. Sweepable.",
    )
    parser.add_argument(
        "--dr-trigger-setup-depth", type=int, default=_SIM_DR_TRIGGER_SETUP_DEPTH,
    )
    args = parser.parse_args(argv)

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    scramble = args.scramble.split()
    runs = Path("runs")
    runs.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_path = runs / f"sim_{ts}.json"

    t0 = time.time()
    result = solve(
        scramble,
        model=args.model,
        max_tool_calls=args.max_tool_calls,
        verbose=args.verbose,
        thinking_budget=args.thinking_budget,
        transcript_path=transcript_path,
        wall_limit_s=args.wall_limit_s,
        sim_budget=args.sim_budget,
        dr_trigger_setup_width=args.dr_trigger_setup_width,
        dr_trigger_setup_depth=args.dr_trigger_setup_depth,
    )
    elapsed = time.time() - t0

    with transcript_path.open("w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\n=== sim run complete ({elapsed:.1f}s wall) ===")
    print(f"  solves:        {result['solves']}")
    print(f"  total_moves:   {result['total_moves']}")
    print(f"  tool_calls:    {result['tool_calls']}")
    print(f"  sim_spent:     {result['sim_spent']}/{result['sim_budget']}s")
    print(f"  halt_reason:   {result['halt_reason']}")
    print(f"  input_tokens:  {result['input_tokens']}")
    print(f"  output_tokens: {result['output_tokens']}")
    print(f"  solution:      {' '.join(result['final_solution'])}")
    print(f"  transcript:    {transcript_path}")
    return 0 if result["solves"] else 1


if __name__ == "__main__":
    sys.exit(main())
