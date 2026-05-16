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
from cube.tools import algebra, dr_pattern_lib, dr_trigger_options as dr_to_mod, dr_triggers, eo_bfs, eo_pattern_lib, insertion_tools, library, niss_scout as niss_scout_mod, policy, search, state

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

# Human-visualization limit: how many moves a champion can hold in their
# head at once when recalling a pattern or lookahead-searching. Real FMC
# solvers see ~3-5 moves ahead; longer sequences are composed by applying
# what they can see and re-evaluating. We force the same on the agent:
# every recall/search tool returns at most this many moves per call.
MAX_HUMAN_RECALL = 4

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
_SIM_LOOKAHEAD_WIDTH = 5  # narrowed in v11: only top-K policy candidates per node
_SIM_LOOKAHEAD_DEPTH = 4  # capped to MAX_HUMAN_RECALL: a human sees ~4 moves ahead
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

# Set of (canonical_subset, axis) we've already encountered — used ONLY for
# cost-tracking (first vs repeat exposure). We never reuse cached moves across
# states because two distinct full-states can share a canonical_subset (notably,
# all canonical-HTR states have canonical == identity). The "memorized finish"
# narrative is preserved at the cost layer; the moves themselves are always
# computed for the current state.
_SUBSET_SEEN: set[tuple[tuple, str]] = set()


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
    run_state: dict | None = None,
):
    """Return a name -> handler map closed over scramble/slots/budget.

    `run_state` is a mutable dict the caller updates per turn so handlers
    can introspect run-level state (tool_calls_remaining, rs_calls_used).
    """
    if run_state is None:
        run_state = {"tool_calls_remaining": 10_000, "rs_calls_used": 0}

    def _h_quick_check(args):
        """v17: FREE state classifier. Returns booleans only — is_solved,
        is_eo_solved per axis, is_dr per axis, is_htr per axis, on_inverse.
        Mirrors what a human FMC solver does in a fraction of a second:
        glance at the cube and recognize the state class. 0s sim cost.

        Use this instead of analyze_residual for mid-solve "am I in DR/HTR
        yet?" checks. Reserve analyze_residual for the rarer case of
        looking specifically for an insertable 3-cycle residual.
        """
        from cube.classifier.features import Axis, is_eo_solved, is_dr
        from cube.classifier.htr import is_htr_ud
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        s = SOLVED.apply_alg(parse_alg(" ".join(sc))) if sc else SOLVED
        if hist:
            s = s.apply_alg(parse_alg(" ".join(hist)))
        # eo / dr per axis
        eo = {ax.value: is_eo_solved(s, ax) for ax in Axis}
        dr = {ax.value: is_dr(s, ax) for ax in Axis}
        return {
            "is_solved": s == SOLVED,
            "is_eo_per_axis": eo,
            "is_dr_per_axis": dr,
            "is_htr_ud": is_htr_ud(s),
            "on_inverse": slot.on_inverse,
            "moves_in_history": len(hist),
            "note": "Free state class check — use this before reaching for analyze_residual.",
        }

    def _h_compose_niss_solution(args):
        """v17: assemble the normal-frame WCA-FMC solution sheet from a
        slot that may have been worked on the inverse side. Returns the
        canonical solution + verify_solved result. Do NOT hand-invert —
        the engine composes correctly per the NISS algebra.

        Convention: when slot.on_inverse is True, slot.history is moves
        applied on the inverse frame after niss_flip; their normal-frame
        equivalent is invert(history). The engine respects whatever
        cumulative state your slot reached.
        """
        slot = _resolve_slot(slots, args["slot"])
        # Construct the normal-frame solution.
        if slot.on_inverse:
            # On inverse: normal-frame solution = invert(history).
            inv_moves = algebra.invert(slot.history)["inverted"]
            solution = list(inv_moves)
        else:
            solution = list(slot.history)
        # Run a cancel pass — humans always do this before submitting.
        solution = algebra.cancel(solution)["cancelled_moves"]
        check = state.verify_solved(scramble, solution)
        budget.charge("compose_niss_solution", 1.0, slot=slot.name)

        # v23a (Phase A): no rs_recommend oracle. The LLM has to decide
        # whether the solve looks lumpy enough to justify a refinement
        # call. The replace_and_shorten tool still enforces its 1-call
        # cap and tool-calls-remaining gate, so it's not a free choice.
        return {
            "solution": solution,
            "length": len(solution),
            "solves": check["solves"],
            "frame_at_compose": "inverse" if slot.on_inverse else "normal",
            "note": (
                "Submit this as FINAL_SOLUTION if you're satisfied, OR "
                "call replace_and_shorten first to see if a sub-span "
                "can be shortened (1-call cap, gated). YOU decide."
                if check["solves"]
                else "Your slot state isn't solved yet — keep working."
            ),
        }

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

    def _h_brain_suggest(args):
        """v23 brain inference: state-conditioned per-step move predictor.

        Returns top-K (move, prob) pairs from the nissy-trained brain
        for the named step (eo/dr/htr/finish). Falls back to legacy
        policy_intuition if the brain checkpoint for that step is not
        present — caller sees `from_brain: false` to know which.
        """
        from cube.brain import infer as brain_infer
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        step = args["step"]
        k = args.get("k", 5)
        if not brain_infer.is_brain_available(step):
            # Fallback to legacy policy
            legacy = policy.policy_intuition(sc, hist, k=k)
            budget.charge("brain_suggest", _COST_POLICY_INTUITION, slot=slot.name)
            return {
                "from_brain": False,
                "step": step,
                "candidates": legacy.get("candidates", []),
                "note": f"no trained brain checkpoint for step={step}; fell back to legacy policy_intuition",
            }
        # Evaluate state from scramble + history
        s = SOLVED.apply_alg(parse_alg(" ".join(sc))) if sc else SOLVED
        if hist:
            s = s.apply_alg(parse_alg(" ".join(hist)))
        suggestions = brain_infer.policy_suggest(s, step, k=k)
        budget.charge("brain_suggest", _COST_POLICY_INTUITION, slot=slot.name, step=step)
        return {
            "from_brain": True,
            "step": step,
            "candidates": [{"move": m, "prob": p} for m, p in suggestions],
            "note": f"top-{k} from brain_{step} (nissy-trained state-conditioned)",
        }

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

    def _h_eo_pattern_lookup(args):
        """Recall a memorized EO sequence for the current bad-edge-slot pattern.

        Mirrors what a human FMC champion does: recognize the
        configuration, recall the fix. Returns at most MAX_HUMAN_RECALL
        moves per call — if the full optimal is longer, you see the first
        N moves toward the goal. Apply them, then re-query from the new
        state to see the next chunk (which may be a different, shorter
        path from there).
        """
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = eo_pattern_lib.eo_pattern_lookup(sc, hist, axis=args["axis"])
        if out.get("found") == 1 and out.get("options"):
            full = out["options"][0]["moves"]
            if len(full) > MAX_HUMAN_RECALL:
                chunk = full[:MAX_HUMAN_RECALL]
                out = {
                    **out,
                    "options": [{"moves": chunk, "length": len(chunk), "partial": True}],
                    "full_optimal_length": len(full),
                    "note": (
                        f"Full optimal EO is {len(full)} moves — beyond your "
                        f"{MAX_HUMAN_RECALL}-move visualization. You see the next "
                        f"{len(chunk)} moves toward EO. Apply them, then re-query "
                        f"from the new state for the next chunk."
                    ),
                }
        budget.charge("eo_pattern_lookup", 3.0, slot=slot.name, axis=args["axis"])
        return out

    # (Removed in v11: find_eo_algorithmic and lookahead_wide — those were
    # wide BFS / wide-beam searches not available to a human solver.)

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

    def _h_niss_scout(args):
        """v16: read-only 6-row scout of EO+DR on normal × inverse × 3 axes.

        Returns a comparison table sorted by expected_total_to_solved.
        The agent reads, picks the recommended row (or overrides with
        rationale), then proceeds with niss_flip + apply_moves as needed.
        """
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = niss_scout_mod.niss_scout(sc, hist)
        # Cost: 6 cells × ~5s each = 30s sim (6 eo_lookups + 6 dr BFS).
        budget.charge("niss_scout", 30.0, slot=slot.name)
        return out

    def _h_dr_trigger_options(args):
        """List named DR-trigger options from the current EO-solved state.

        Returns a ranked menu of trigger families (DR-4C4E, DR-3C2E, etc.)
        with their setup moves, total-to-DR, and JZP/pairs flags. The agent
        picks by family preference and structural flags, not just by
        shortest moves. Champion-shaped decision-making. v15: supports
        all 3 axes (UD/FB/RL) via per-axis trigger catalogs derived by
        cube symmetry from the UD reference.
        """
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = dr_to_mod.dr_trigger_options(
            sc, hist,
            axis=args.get("axis", "UD"),
            max_setup=args.get("max_setup", 5),
        )
        budget.charge("dr_trigger_options", 8.0, slot=slot.name, axis=args.get("axis", "UD"))
        return out

    def _h_dr_recognize(args):
        """Recognize the DR pattern. If the trigger is reachable within
        MAX_HUMAN_RECALL moves, return setup_moves + trigger_moves + named
        family. Otherwise return only the first MAX_HUMAN_RECALL moves of
        the optimal path as `setup_progress` — partial setup toward an
        eventual trigger. Apply, then re-query.

        This mirrors how a champion solves: see the trigger (R, R U2 R',
        etc.) when it's close; or, if the trigger isn't yet in view,
        apply a short setup chunk and look again.
        """
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = dr_pattern_lib.dr_pattern_lookup(sc, hist, axis=args["axis"])
        if out.get("found") == 1 and out.get("options") and out["options"][0]["moves"]:
            full_moves = out["options"][0]["moves"]
            if len(full_moves) <= MAX_HUMAN_RECALL:
                setup, trigger, trigger_name = dr_triggers.identify_trigger(full_moves)
                out = {
                    "found": 1,
                    "axis": args["axis"],
                    "trigger_family": trigger_name,
                    "setup_moves": setup,
                    "trigger_moves": trigger,
                    "total_length": len(full_moves),
                    "note": (
                        f"DR within visualization: {trigger_name}. "
                        f"{len(setup)}-move setup + {len(trigger)}-move trigger."
                    ),
                }
            else:
                chunk = full_moves[:MAX_HUMAN_RECALL]
                out = {
                    "found": 0,
                    "axis": args["axis"],
                    "setup_progress": chunk,
                    "full_optimal_length": len(full_moves),
                    "note": (
                        f"Trigger not yet in view — full optimal is "
                        f"{len(full_moves)} moves, beyond your "
                        f"{MAX_HUMAN_RECALL}-move visualization. You see "
                        f"{len(chunk)} moves of useful setup. Apply them, "
                        f"then re-query to see the trigger."
                    ),
                }
        budget.charge("dr_recognize", 3.0, slot=slot.name, axis=args["axis"])
        return out

    def _h_probe_dr_pattern(args):
        """Estimate DR feasibility after a hypothetical EO. Reports the
        TOTAL optimal DR length (for picking the best EO axis) and, if
        within MAX_HUMAN_RECALL moves, the trigger family. Use to compare
        EO options by DR total. Cost: 3s simulated.
        """
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        hypothetical_hist = list(hist) + list(args["eo_alg"])
        out = dr_pattern_lib.dr_pattern_lookup(sc, hypothetical_hist, axis=args["axis"])
        if out.get("found") == 1 and out.get("options") and out["options"][0]["moves"]:
            full_moves = out["options"][0]["moves"]
            res = {
                "found": 1,
                "axis": args["axis"],
                "total_dr_length": len(full_moves),
                "within_visualization": len(full_moves) <= MAX_HUMAN_RECALL,
            }
            if len(full_moves) <= MAX_HUMAN_RECALL:
                _, _, trigger_name = dr_triggers.identify_trigger(full_moves)
                res["trigger_family"] = trigger_name
            out = res
        out["probed_with_eo"] = list(args["eo_alg"])
        budget.charge("probe_dr_pattern", 3.0, slot=slot.name, axis=args["axis"])
        return out

    # (Removed in v11: find_dr_via_trigger and probe_dr_after_eo — those were
    # wide beam searches with width=32 not available to a human solver.)

    def _h_analyze_residual(args):
        """Classify what's left to solve on the current state.

        Use this whenever you want to see if you've landed on an
        insertable residual (pure 3-cycle, 2e2e, etc.). Cheap (2s).
        """
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = insertion_tools.analyze_current_residual(sc, hist)
        budget.charge("analyze_residual", 2.0, slot=slot.name)
        return out

    def _h_derive_corner_3cycle(args):
        """If the current state is a pure corner 3-cycle, return the
        canonical 8-move commutator that solves it. Closed-form table
        lookup, no search. Cost: 3s simulated."""
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = insertion_tools.derive_corner_3cycle(sc, hist)
        budget.charge("derive_corner_3cycle", 3.0, slot=slot.name)
        return out

    def _h_replace_and_shorten(args):
        """Tronto §3.10 'Replace and shorten': pick a sub-span of the
        current history, re-solve it as a micro-scramble via the existing
        DR/HTR pipeline, and return a shorter substitute if found.
        Recursive reuse of existing tools, not new search. Cost: 30s sim.

        v14a guardrails: capped at 1 call per run, and gated on having
        ≥30 tool calls remaining (since on a miss the agent may need to
        rebuild its solve, which can chew through 20+ tool calls)."""
        # Gate 1: per-run cap. Tronto explicitly recommends a single r&s pass.
        if run_state.get("rs_calls_used", 0) >= 1:
            return {
                "error": "replace_and_shorten already used this run (1-call cap, Tronto §3.10).",
                "rs_calls_used": run_state["rs_calls_used"],
            }
        # Gate 2: budget headroom. r&s consumes tool calls on the miss path.
        remaining = run_state.get("tool_calls_remaining", 0)
        if remaining < 30:
            return {
                "error": (
                    f"too few tool calls remaining ({remaining}) for replace_and_shorten; "
                    f"need ≥30 (the miss path can require 20+ recovery calls). "
                    f"Ship your current solve as FINAL_SOLUTION instead."
                ),
                "tool_calls_remaining": remaining,
            }
        slot = _resolve_slot(slots, args["slot"])
        sc, hist = _materialize(scramble, slot)
        out = insertion_tools.replace_and_shorten(
            sc, hist,
            start=args["start"], end=args["end"],
            axis=args.get("axis", "UD"),
        )
        run_state["rs_calls_used"] = run_state.get("rs_calls_used", 0) + 1
        out["rs_calls_used"] = run_state["rs_calls_used"]
        budget.charge("replace_and_shorten", 30.0, slot=slot.name)
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

    def _compute_subset_phases(s, sc, hist, axis: str, canonical: tuple) -> dict | None:
        """Compute fresh phases for the CURRENT state. Returns
        {"htr_moves": [...], "finish_moves": [...]} or None on error.
        Always recomputes — different states with the same canonical_subset
        can need different finish moves (canonical drops EP info), so caching
        the moves would silently give wrong answers."""
        if not is_htr_ud(s):
            full = search.solve_htr_and_finish_from_dr(sc, hist, axis=axis)
            if "error" in full:
                return None
            return {
                "htr_moves": list(full["htr_moves"]),
                "finish_moves": list(full["finish_moves"]),
            }
        from cube.classifier.htr import htr_solve
        finish = htr_solve(s)
        if finish is None:
            return None
        return {"htr_moves": [], "finish_moves": [str(m) for m in finish]}

    def _subset_describe(canonical: tuple) -> dict:
        """Human-friendly structural description of the corner subset."""
        from cube.classifier.features import (
            corner_swap_count, corner_axial_count,
            corner_perm_parity, corner_cycle_structure,
        )
        # Build a State view from the canonical cp tuple to query features.
        from cube.engine.state import SOLVED as _S
        from dataclasses import replace
        synthetic = replace(_S, cp=tuple(canonical))
        swap = corner_swap_count(synthetic)
        axial = corner_axial_count(synthetic)
        parity = corner_perm_parity(synthetic)
        cycles = corner_cycle_structure(synthetic)
        if axial == 8:
            family = "axial"
        elif axial >= 4:
            family = "mostly-axial"
        elif max(cycles) <= 2:
            family = "2-cycle"
        else:
            family = "long-cycle"
        return {
            "swap_count": swap,
            "axial_count": axial,
            "perm_parity": parity,
            "cycle_structure": list(cycles),
            "family": family,
            "name": f"{swap}-swap {family}",
        }

    def _h_htr_classify(args):
        """Classify the current HTR-corner-subset and report phase lengths.

        Returns the subset name (e.g. "4-swap axial"), the structural features
        (swap/axial counts, cycle structure, parity), and the lengths of the
        two finish phases:
          - htr_reduction: corner-orbit moves taking DR -> HTR subgroup
          - finish: half-turn-only moves taking HTR -> solved

        The agent should then apply each phase with apply_htr_phase and
        narrate which phase is doing what. First exposure to a subset costs
        more sim time ("learning"); subsequent exposures are cheap (recall).
        """
        slot = _resolve_slot(slots, args["slot"])
        axis = args["axis"]
        sc, hist = _materialize(scramble, slot)
        s = SOLVED.apply_alg(parse_alg(" ".join(sc))) if sc else SOLVED
        if hist:
            s = s.apply_alg(parse_alg(" ".join(hist)))

        canonical = dr_subset_canonical(s)
        if canonical is None:
            return {"error": "current state is not in DR-corner subgroup; reach DR first."}
        cache_key = tuple(canonical)
        seen_key = (cache_key, axis)
        cached_before = seen_key in _SUBSET_SEEN
        phases = _compute_subset_phases(s, sc, hist, axis, cache_key)
        if phases is None:
            budget.charge("htr_classify", _COST_SUBSET_LOOKUP_MISS, slot=slot.name, axis=axis, cached=False)
            return {"error": "could not compute HTR phases for this subset."}
        _SUBSET_SEEN.add(seen_key)

        cost = _COST_SUBSET_LOOKUP_CACHED if cached_before else _COST_SUBSET_LOOKUP_MISS
        budget.charge("htr_classify", cost, slot=slot.name, axis=axis, cached=cached_before, subset=list(canonical))
        info = _subset_describe(cache_key)
        return {
            "subset_canonical": list(canonical),
            "subset_name": info["name"],
            "subset_family": info["family"],
            "structural": {
                "swap_count": info["swap_count"],
                "axial_count": info["axial_count"],
                "perm_parity": info["perm_parity"],
                "cycle_structure": info["cycle_structure"],
            },
            "axis": axis,
            "phases": {
                "htr_reduction": {
                    "length": len(phases["htr_moves"]),
                    "description": (
                        "DR -> HTR-corner-subgroup; quarter-turn corners on the axis "
                        "(or empty if already in HTR)."
                    ),
                },
                "finish": {
                    "length": len(phases["finish_moves"]),
                    "description": "HTR -> solved; half-turn only.",
                },
            },
            "total_length": len(phases["htr_moves"]) + len(phases["finish_moves"]),
            "cached": cached_before,
            "note": (
                f"Subset is {info['name']} (cycles={info['cycle_structure']}). "
                f"Apply with apply_htr_phase(phase='htr_reduction') then "
                f"apply_htr_phase(phase='finish'). "
                + ("Recall (cached)." if cached_before else "First exposure — memorized.")
            ),
        }

    def _h_apply_htr_phase(args):
        """Return the moves for the named HTR phase. Phase must be either
        'htr_reduction' or 'finish'. Requires htr_classify to have been
        called first (otherwise lazily computes). Apply the returned moves
        with apply_moves and narrate what the phase is doing."""
        slot = _resolve_slot(slots, args["slot"])
        axis = args["axis"]
        phase = args["phase"]
        if phase not in ("htr_reduction", "finish"):
            return {"error": f"phase must be 'htr_reduction' or 'finish'; got {phase!r}"}
        sc, hist = _materialize(scramble, slot)
        s = SOLVED.apply_alg(parse_alg(" ".join(sc))) if sc else SOLVED
        if hist:
            s = s.apply_alg(parse_alg(" ".join(hist)))
        canonical = dr_subset_canonical(s)
        if canonical is None:
            return {"error": "not in DR-corner subgroup."}
        cache_key = tuple(canonical)
        phases = _compute_subset_phases(s, sc, hist, axis, cache_key)
        if phases is None:
            return {"error": "could not compute HTR phases."}
        full = phases["htr_moves"] if phase == "htr_reduction" else phases["finish_moves"]
        budget.charge("apply_htr_phase", 1.0, slot=slot.name, axis=axis, phase=phase)
        if len(full) <= MAX_HUMAN_RECALL:
            return {
                "phase": phase,
                "axis": axis,
                "moves": list(full),
                "length": len(full),
                "partial": False,
                "note": (
                    f"{phase}: {len(full)} moves, fully in view. Apply with apply_moves."
                    + (" (Already in HTR — empty phase.)" if not full else "")
                ),
            }
        chunk = full[:MAX_HUMAN_RECALL]
        return {
            "phase": phase,
            "axis": axis,
            "moves": list(chunk),
            "length": len(chunk),
            "full_phase_length": len(full),
            "partial": True,
            "note": (
                f"{phase}: {len(full)} moves total, but only {len(chunk)} "
                f"fit in your visualization. Apply this chunk, then re-query "
                f"to see the next {MAX_HUMAN_RECALL} moves from the new state."
            ),
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
        "quick_check": _h_quick_check,
        "compose_niss_solution": _h_compose_niss_solution,
        "niss_flip": _h_niss_flip,
        "policy_intuition": _h_policy_intuition,
        "brain_suggest": _h_brain_suggest,
        "try_alg": _h_try_alg,
        "lookahead": _h_lookahead,
        "eo_pattern_lookup": _h_eo_pattern_lookup,
        "niss_scout": _h_niss_scout,
        "dr_trigger_options": _h_dr_trigger_options,
        "dr_recognize": _h_dr_recognize,
        "probe_dr_pattern": _h_probe_dr_pattern,
        "analyze_residual": _h_analyze_residual,
        "derive_corner_3cycle": _h_derive_corner_3cycle,
        "replace_and_shorten": _h_replace_and_shorten,
        "cancel": _h_cancel,
        "htr_subset": _h_htr_subset,
        "htr_classify": _h_htr_classify,
        "apply_htr_phase": _h_apply_htr_phase,
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
            "name": "quick_check",
            "description": (
                "v17 FREE state classifier (0s sim). Returns is_solved + "
                "is_eo_per_axis + is_dr_per_axis + is_htr_ud + on_inverse + "
                "moves_in_history. Mirrors a human FMC solver's instant visual "
                "recognition of state class. Use this for inter-phase 'am I in "
                "DR/HTR/solved yet?' checks — reserve analyze_residual for the "
                "rarer case of explicitly looking for an insertable 3-cycle."
            ),
            "input_schema": {"type": "object", "properties": {"slot": _SLOT}, "required": ["slot"]},
        },
        {
            "name": "compose_niss_solution",
            "description": (
                "v17 — assemble the canonical normal-frame WCA-FMC solution "
                "sheet from a slot. If the slot is on_inverse, the engine "
                "correctly inverts the history; otherwise it returns history "
                "as-is. Runs cancel() and verify_solved internally. **Always "
                "call this before emitting FINAL_SOLUTION** rather than hand-"
                "constructing the inverted move list — the agent has a poor "
                "track record on NISS algebra in transcripts. Cost: 1s sim."
            ),
            "input_schema": {"type": "object", "properties": {"slot": _SLOT}, "required": ["slot"]},
        },
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
            "name": "brain_suggest",
            "description": (
                "v23 — state-conditioned per-step move predictor (the 'brain'). "
                "Specify which FMC step you're working on (eo/dr/htr/finish); the "
                "brain returns top-K (move, prob) candidates from a small "
                "transformer trained on optimal-move distributions from nissy. "
                "Unlike policy_intuition (history-sequence-conditioned), this "
                "directly conditions on the current cube state and outputs only "
                "moves that are legal for the named step. Falls back to "
                "policy_intuition if the brain checkpoint for that step is not "
                "trained yet (response includes `from_brain: false`)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "step": {"type": "string", "enum": ["eo", "dr", "htr", "finish"]},
                    "k": {"type": "integer", "minimum": 1, "maximum": 10, "default": 5},
                },
                "required": ["slot", "step"],
            },
        },
        {
            "name": "try_alg",
            "description": "Preview applying an alg on top of a slot's history WITHOUT committing. Cheap (2s simulated).",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT, "alg": _MOVE_LIST}, "required": ["slot", "alg"]},
        },
        {
            "name": "lookahead",
            "description": (
                f"Policy-pruned visualization (depth={_SIM_LOOKAHEAD_DEPTH}, "
                f"width={_SIM_LOOKAHEAD_WIDTH} — top-K candidates per node from "
                f"the trained transformer). This is your 'see ahead in your head' "
                f"tool: what looks closest to target within the {_SIM_LOOKAHEAD_DEPTH}-move "
                f"horizon. Targets: 'eo' or 'solved'. Not a deep search — a human visualization."
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
            "name": "eo_pattern_lookup",
            "description": (
                "Recognize a memorized EO pattern on `axis`. Returns at most "
                f"{MAX_HUMAN_RECALL} moves per call (your visualization limit). "
                "If the optimal full EO is ≤4 moves you see the full sequence; "
                "otherwise you see the first 4 moves of progress. Apply them, "
                "then re-query from the new state to see the next chunk. "
                "Cost: 3s simulated."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                },
                "required": ["slot", "axis"],
            },
        },
        {
            "name": "niss_scout",
            "description": (
                "v16 — 6-row read-only scout. Computes the best EO+DR option "
                "on BOTH normal AND inverse for all 3 axes (UD/FB/RL), returns "
                "a comparison table sorted by expected_total_to_solved. The "
                "table is the explicit branch-and-discard ledger elite WCA "
                "solvers keep in their head; the median elite solve has 8 "
                "NISS transitions and 50% START on inverse. Call this ONCE "
                "right after inspect_state on a fresh scramble — before any "
                "EO commit — and use the recommendation (or override with "
                "an explicit rationale). Does NOT modify any slot. Cost: 30s sim."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"slot": _SLOT},
                "required": ["slot"],
            },
        },
        {
            "name": "dr_trigger_options",
            "description": (
                "List named DR-trigger options from the current EO-solved state "
                "on ANY axis (UD/FB/RL — v15 supports all three). Returns a "
                "ranked menu: each entry is a NAMED trigger family (DR-4C4E 'R', "
                "DR-3C2E 'R U R'', DR-4C2E 'R U2 R'', DR-7C8E 'R U L', etc.) "
                "with its setup_moves, total_to_dr, expected_total_to_solved "
                "(DR + empirical HTR-finish), jzp_eligible flag, and "
                "top_pairs_on_inverse count. Per-axis trigger letters: "
                "UD uses R+U, FB uses U+F, RL uses F+L (cube-symmetry equivalents). "
                "Pick by expected_total_to_solved (already sorted lowest-first). "
                "Use this INSTEAD of dr_recognize when surveying any axis — it "
                "surfaces the decision a champion makes. Cost: 8s simulated."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                    "max_setup": {"type": "integer", "minimum": 1, "maximum": 6, "default": 5},
                },
                "required": ["slot", "axis"],
            },
        },
        {
            "name": "dr_recognize",
            "description": (
                "PRIMARY DR TOOL — recognize the DR pattern on `axis` and "
                "split the memorized completion into NAMED setup + trigger. "
                "Returns trigger_family (e.g. \"X-U2-X' (DR-4c4e)\"), "
                "setup_moves (may be empty), and trigger_moves. Like a "
                "champion: name what you're seeing, then apply the named "
                "pieces. Then apply setup_moves and trigger_moves with "
                "SEPARATE apply_moves calls so the narration shows each "
                "piece. EO on `axis` must already be solved. 3s simulated."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                },
                "required": ["slot", "axis"],
            },
        },
        {
            "name": "probe_dr_pattern",
            "description": (
                "Run dr_recognize AS IF the given eo_alg were applied, "
                "WITHOUT modifying the slot. Returns trigger_family + "
                "setup/trigger lengths + total. Use to compare DR options "
                "across candidate EOs by trigger family AND total. "
                "Cost: 3s simulated."
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
            "name": "analyze_residual",
            "description": (
                "Classify what's still unsolved on the current slot. Returns "
                "residual_class (e.g. 'corner_3cycle', 'edge_3cycle', 'mixed'), "
                "the actual perm cycles and twists/flips by slot name, "
                "is_pure_corner_3cycle / is_pure_edge_3cycle flags, and "
                "counts of unsolved pieces. Use this to detect when you've "
                "landed on an insertable residual (3c, 2e2e, etc.) so you "
                "can derive a commutator instead of grinding through HTR. 2s sim."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"slot": _SLOT},
                "required": ["slot"],
            },
        },
        {
            "name": "derive_corner_3cycle",
            "description": (
                "If your current state is a PURE corner 3-cycle (verify via "
                "analyze_residual.is_pure_corner_3cycle first), return the "
                "canonical 8-move commutator that solves it. Closed-form table "
                "lookup over the 112 reachable corner 3-cycles × 9 twist "
                "patterns. Mirrors a human FMC solver deriving the right "
                "commutator from the 3-cycle they see. NO SEARCH. 3s sim."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"slot": _SLOT},
                "required": ["slot"],
            },
        },
        {
            "name": "replace_and_shorten",
            "description": (
                "Tronto §3.10 'Replace and shorten'. Pick a sub-span of your "
                "current slot history (specify start/end indices). Apply that "
                "span to a solved cube as a fresh micro-scramble, re-solve it "
                "via the existing DR/HTR pipeline, and substitute the result "
                "back in. Returns the substitute and whether the new full "
                "history still solves. Use on suspicious lumpy sub-sequences "
                "of 8+ moves. NOT new search — recursive reuse of existing "
                "tools. 30s sim."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "start": {"type": "integer", "minimum": 0},
                    "end": {"type": "integer", "minimum": 1},
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"], "default": "UD"},
                },
                "required": ["slot", "start", "end"],
            },
        },
        {
            "name": "cancel",
            "description": "Apply local move cancellation (same-face merge, through-axis-commute). Mechanical, cheap. Use just before submitting to collapse the final solution.",
            "input_schema": {"type": "object", "properties": {"moves": _MOVE_LIST}, "required": ["moves"]},
        },
        {
            "name": "htr_subset",
            "description": "Identify the canonical HTR-corner-subset of the slot. Use after reaching DR — name the subset before classifying/finishing.",
            "input_schema": {"type": "object", "properties": {"slot": _SLOT}, "required": ["slot"]},
        },
        {
            "name": "htr_classify",
            "description": (
                "Classify the post-DR state into a named HTR subset and "
                "report the two finish-phase lengths: (1) htr_reduction "
                "(DR -> HTR-corner-subgroup via quarter-turn corners on the "
                "axis); (2) finish (HTR -> solved via half-turns only). "
                "Returns subset_name (e.g. '4-swap axial'), structural "
                "features (swap_count, axial_count, cycle_structure), and "
                "per-phase lengths. Narrate the subset by name, then call "
                "apply_htr_phase for each phase separately. First exposure "
                f"to a subset costs ~{int(_COST_SUBSET_LOOKUP_MISS)}s (learning); "
                f"repeats cost {int(_COST_SUBSET_LOOKUP_CACHED)}s (recall)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                },
                "required": ["slot", "axis"],
            },
        },
        {
            "name": "apply_htr_phase",
            "description": (
                "Return the moves for one HTR phase ('htr_reduction' or "
                "'finish'). Pair with apply_moves to commit them. Calling "
                "the two phases separately gives narration like 'reducing "
                "corners with U2 R2 U2 R2' then 'half-turn finish: F2 L2 "
                "U2…'. Cost: 1s simulated each."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "slot": _SLOT,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                    "phase": {"type": "string", "enum": ["htr_reduction", "finish"]},
                },
                "required": ["slot", "axis", "phase"],
            },
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

# What you SEE in inspect_state (the champion's view)

For each axis, inspect_state reports a `dr_closeness_per_axis` block:
- `misoriented_corners` ("C") and `misplaced_slice_edges` ("E"): these are
  the DR-XCYE label that champions recite. (4, 4) = DR-4C4E (R trigger),
  (4, 2) = DR-4C2E (R U2 R'), (3, 2) = DR-3C2E (R U R' / R U' R'),
  (7, 8) = DR-7C8E (R U L), etc.
- `jzp_eligible` (UD only): boolean — a JZP state has dramatically shorter
  DR; even normally-bad cases like 2C6E/4C6E become viable. JZP requires:
  no U/D corner stickers on R/L, no E-slice edges in M-slice, even
  unoriented corners. If JZP-eligible, lean toward this axis.
- `top_pairs_on_inverse` (UD only): Wen's pairs-tracing count. 2+ pairs
  preserved on inverse = strong NISS-switch signal.
- `arm_other_axis`: distance from JZP on the OTHER axis after NISS.
  Lower numbers predict better post-switch DR.

For HTR (post-DR), `htr_closeness`:
- `qt_corners` (0-5): primary HTR-distance signal. 0qt = already at HTR
  corners; 4qt+ = expect longer finish.
- `solved_corner_columns` (0-4): for floppy/slice-finish reasoning.

# NISS-FIRST RULE

After your initial EO scan, ALWAYS also check the inverse frame for each
axis you might use. Use niss_flip + eo_pattern_lookup on the inverse to
compare. If `top_pairs_on_inverse ≥ 2` OR EO is ≥1 move shorter on
inverse, the inverse frame is the better solving direction. NISS is
cheap (~5s); always check it.

# Human Tools (v11 — strict constraints)
You are NOT a brute-force search engine. You have a HUMAN solver's tools:

- **Vision**: inspect_state shows the cube and per-axis bad-edge counts.
- **Trained intuition** (transformer policy): policy_intuition returns
  top-K candidate moves. This is your "gut feeling" — the same kind of
  trained pattern recognition a champion has after years of practice.
- **Visualization** (depth 4): lookahead does policy-pruned beam search
  to depth {MAX_HUMAN_RECALL}, width K. This is what a human can hold
  in their head — 3-4 moves of mental visualization, not a deep search.
- **Pattern memory** (4-move recall): eo_pattern_lookup, dr_recognize,
  apply_htr_phase return AT MOST {MAX_HUMAN_RECALL} moves per call. If
  the optimal solution is longer, you see only the first 4 moves of
  progress toward it. APPLY THEM, then RE-QUERY from the new state to
  see the next chunk. This is the real human workflow: a champion sees
  "OK these 3 moves get me much closer", commits, re-evaluates.
- **What you DON'T have**: no wide BFS, no deep search, no oracle that
  spits out the full solution. You compose by iterating.

Your job is to narrate the FMC theory and reasoning as you go. The
transcript is the product. Show your work.

# Elite-solver exemplars (v21 — read these before scouting)

Three condensed reasoning patterns from elite WCA-FMC champions. They
illustrate the *texture* of the solve narration you should imitate.
Match the voice: tool calls + terse rationale + explicit rejection of
inferior branches.

### Exemplar A — Multi-side EO scouting before committing
> Scramble loaded. niss_scout returns the 12-row joint table. UD-normal
> top row: EO 4mv + DR-4C4E expected_total 18. But inverse-FB row 2 has
> EO 5mv + DR-3C2E expected_total 17 (better HTR substate). Picking the
> inverse branch: cost saved is 1 expected move, more importantly the
> 3C2E substate finishes in ~5 vs ~9 for 4C4E. niss_flip, then apply EO
> on the inverse frame. I did NOT take the row that gave a "free pseudo-
> slot" — EO blocks are a trap, they constrain DR axis choice. Keep EO
> clean, let DR do the structural work.

### Exemplar B — Picking the longer DR for a cleaner substate
> Post-EO on the inverse-FB axis. dr_trigger_options(axis='FB') returns
> three candidates:
> - DR-4C4E (U): 1mv setup, expected_total 11. Tempting but the
>   substate is the worst case.
> - DR-3C2E (U F U'): 3mv setup, expected_total 9 — 2 moves CHEAPER
>   net despite 2 extra DR-setup moves.
> - DR-2C4E (U L2 U): 3mv setup, expected_total 10.
> Taking DR-3C2E. Length of DR is a red herring; what matters is
> dr_moves + htr_moves + finish_moves, and the 3C2E substate is worth
> ~3 moves of credit against any longer-DR comparison. A 4C2E DR
> substate at zero-setup-to-HTR is similarly worth that credit.

### Exemplar C — Branch journal with explicit rejection rationale
> Logging branches as I scout.
> **Branch 1 — UD axis DR (Branch I'm bookmarking):** dr_trigger_options
> finds a 4-move setup to RZP, then a 3-move trigger gives DR in 11
> total. Substate: 1 quarter-turn corner. HTR estimate 5 moves. Finish
> leaves 2e2e (potential 1-move insertion via replace_and_shorten).
> Projected total: 20-21. **Bookmarking.**
> **Branch 2 — RL axis DR (scouted from same EO):** holding Branch 1
> aside. dr_trigger_options(axis='RL') returns nothing under 7 moves —
> corner orientation is wrong-parity for this axis. **Reject:** 7+ move
> DR with a bad substate dominates Branch 1.
> **Branch 3 — FB axis DR:** would require redoing EO from scratch.
> **Reject** without scouting; the cost of re-EO is not recoverable.
> Committing to Branch 1. **Lesson:** when a branch is rejected, write
> *why* (parity, length, substate quality), not just "it lost." This
> is the elite-FMC compare-before-commit pattern.

# Branch journal (v14b, elite-solver behavior)

Elite solvers literally log their rejected branches: "tried 4b2 on FB,
saw 4c4e in 7 — took the 2c3 on UD in 5 instead." This is **comparison
before commitment**. Before committing to an EO axis or a DR trigger,
state out loud the candidates you considered and WHY you rejected the
others, e.g.:

  "EO axes considered: UD=2bad/1mv, FB=4bad/3mv, RL=8bad/4mv → UD wins."
  "DR triggers on UD: 4C4E (1mv, expected_total=11), 3C2E (4mv, JZP,
   expected_total=9) → take 3C2E, it's 2 moves cheaper TOTAL despite
   3 extra DR setup moves."

This is BOTH the deliverable (the transcript reads like a champion's
walkthrough) AND a forcing function — verbalizing alternatives prevents
the default "take the shortest DR" trap that produced our 28-30 move
solves in v11-v13.

# Pipeline (the realistic-human version)

1. **Inspect + NISS-scout** (v16):
   a) inspect_state(main).
   b) **niss_scout(slot='main')**. ONE call returns a 6-row table
      (normal × inverse × {{UD, FB, RL}}) sorted by
      expected_total_to_solved. The first row is the recommendation.
      Median elite WCA solve has 8 NISS transitions and 50% start on
      inverse — scouting is mandatory, not optional. Verbalize the
      rejected rows: "Picked normal-UD with expected 18 (EO 4 + DR
      8 + HTR 6); rejected inverse-FB at 19 because the EO is 5
      moves and the DR substate's worse."
   c) If the recommendation picks the INVERSE side, call niss_flip
      BEFORE applying the EO. Otherwise continue on normal.
   d) For the chosen (side, axis), call eo_pattern_lookup(axis=X) to
      get the actual EO move list to apply (the scout reports
      lengths; this returns the moves themselves, possibly chunked
      4 at a time if partial).

2. **Commit EO incrementally**:
   - If the lookup returned the full sequence (≤4 moves): apply_moves
     the whole thing in one call. Narrate the move purpose.
   - If partial: apply_moves the visible chunk, narrate "this gets me
     closer to EO on FB", then re-query eo_pattern_lookup(axis=X) on
     the new state. Repeat until found=1 with no partial flag.

3. **DR feasibility probe (before each EO axis decision is final)**:
   For each plausible EO candidate, call probe_dr_pattern. It reports
   total_dr_length and trigger_family (if within visualization). USE
   this to pick the joint-shortest EO+DR axis. Note: total_dr_length
   may be 5-10 moves — even though you can only SEE 4 moves at a time,
   you know the TOTAL.

4. **DR compose** (UD axis: use dr_trigger_options; other axes: dr_recognize):

   **DR-LENGTH HARD RULE (v14b, from 333.fm corpus research)**: elite
   solves get DR in ≤6 moves with 85.7% probability. **DR ≥10 moves NEVER
   appears in sub-22 solves.** If your shortlist's best `expected_total_to_solved`
   is >15, treat it as a SIGNAL that the EO axis or DR axis choice was wrong —
   probe another axis (or NISS-flip and try again) before committing.

   **The 4C4E TRAP**: DR-4C4E (single-R trigger) is the shortest-DR but
   HTR-finishes in ~9 moves (vs ~5 for DR-3C2E). The new rank_key
   accounts for this via `expected_total_to_solved`. Prefer a 4-move
   3C2E DR over a 1-move 4C4E DR — the savings come from the HTR side.

   a) **v15: dr_trigger_options is now your PRIMARY tool on ALL 3 axes.**
      Call dr_trigger_options(axis=X) for X in your candidate axes. Returns
      a ranked MENU of named triggers with `expected_total_to_solved`.
      Read the menu, pick by `expected_total_to_solved` (already ranked
      lowest-first). JZP-eligible cases are gold; top_pairs_on_inverse ≥ 2
      signals a NISS-switch opportunity. Narrate your pick by NAME ("I'll
      take the R-U2-R' DR-4C2E option because it's JZP-eligible with
      expected_total_to_solved=10 — beats the 1-move 4C4E whose
      expected_total is 11").
   b) dr_recognize is a FALLBACK only — use it only if dr_trigger_options
      returns no options within max_setup=5. Per-axis trigger letters:
      UD uses R+U, FB uses U+F, RL uses F+L. The expected_total ranking
      lets you compare apples-to-apples across axes.
   c) If `found=0` with `setup_progress`: trigger isn't in view yet.
      Apply the {MAX_HUMAN_RECALL} setup_progress moves with narration,
      then dr_recognize again on the new state.

5. **POST-DR DECISION** (v14b — research-driven priority):

   **PRIMARY PATH (Option A — Standard HTR finish)**: 333.fm corpus shows
   elite solvers DO NOT use insertions. Elite insertion rate is 0.7%; long
   (30+) solves use them 15.8%. Insertions are a recovery tool, not the
   path to sub-25. **Default to the clean DR→HTR→finish pipeline.** Use
   the inter-phase analyze_residual checks (step 6) as opportunistic
   shortcuts, NOT primary tooling.

   **FALLBACK (Option B — derive_corner_3cycle)**: ONLY if analyze_residual
   returns `is_pure_corner_3cycle: true` between HTR-finish chunks — then
   the 8-move comm is genuinely shorter than the remaining finish. Don't
   force this; don't go searching for skeletons.

   **REFINEMENT (Option D — replace_and_shorten)**: 1-call cap; the tool
   enforces it. Use ONLY if your initial solve is ≥27 moves AND you have
   ≥30 tool calls remaining. The tool will refuse otherwise.

   **DEPRIORITIZED**: don't go looking for slice insertions or 3-cycle
   skeletons proactively. Per the 333.fm research, the path to sub-25
   is DR-quality, not insertion-skill.

5b. **REFINEMENT (MANDATORY when gates pass)**: after you have a
   verified solve, if total_moves ≥ 27 AND tool calls remaining ≥ 30
   AND you haven't already called replace_and_shorten this run, you
   **MUST** call replace_and_shorten ONCE on a large tail span
   (e.g., start=4, end=N where N is your total move count). The tool
   enforces the gates and will refuse otherwise — DO NOT try to call
   it more than once. If it returns `solves_scramble: true` AND
   `delta < 0`, accept the substitute as your new history (replace
   history starting from `start` with `substitute_moves`). v13
   evidence: this saved 3-5 moves on PSSS_s1 (30 → 25). If r&s
   would fall outside the gates, submit your current solve.

   After r&s succeeds, you may submit immediately — don't try to
   chain a second r&s; the tool enforces a 1-call cap.

6. **HTR classify + phase compose** (running Option A) — with **free
   inter-phase state checks** (v17: quick_check replaces analyze_residual
   for the common case):
   a) htr_classify(axis=X). Narrate the subset by name: "this is a
      4-swap axial subset with cycle structure (2,2,2,2)."
   b) apply_htr_phase(phase='htr_reduction'). If `partial: true`, the
      reduction is longer than 4 moves; apply the visible chunk,
      narrate ("4 moves of corner orbit reduction"), then **CALL
      quick_check BEFORE re-querying apply_htr_phase**. quick_check is
      FREE (0s) and returns is_solved/is_htr_ud/etc. If is_solved=true
      → submit; if is_htr_ud=false → continue HTR-reduction. Only call
      analyze_residual when you specifically suspect a pure 3-cycle
      residual (rare; quick_check tells you when this is plausible).
   c) Same for apply_htr_phase(phase='finish'): quick_check between
      chunks. If is_solved emerges before the finish ends, ship it.

   Why: a "clean" subset finish often produces a 3c residual one or two
   chunks before fully solved — landing there earlier and inserting the
   commutator saves 2-4 moves vs running the full finish. This is the
   real human FMC pattern: see the residual, derive the comm, submit.

6. **cancel + verify_solved**. Narrate the cancellations you spot.

# Reasoning style — the deliverable

Before EACH tool call, narrate in 2-4 sentences:
- What you SEE (state of cube, what's left, what theory applies).
- What you EXPECT to happen (which moves should help and why).
- WHY this tool is the right next step.

The whole transcript is the video. Verbalize FMC vocabulary: "bad
edges on UF and DB share the F flipping face", "RZP setup of 2 moves
into the R-U2-R' DR-4c4e trigger", "this is a 4-swap axial subset —
3-cycle finish with one extra pair". This is the texture viewers want.

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
- Backtracking tools (`reset_slot`, `undo_moves`, `new_slot`) exist but
  use them sparingly. Empirically (v23b corpus eval), prompting the
  agent to use backtracking proactively REGRESSED move count by 1.2
  moves — same pattern as v14b's branch-journal thrash. Stick with
  the committed branch unless something is *clearly* wrong.
- NISS is cheap (~{cost_niss}s) and powerful — use it when stuck.
- **Before submitting**: call cancel(moves=your_full_solution) to collapse
  any adjacent same-face moves (e.g. `U U2` → `U'`). It's cheap and often
  saves 1-3 moves.
- **Submission (v17)**: ALWAYS call `compose_niss_solution(slot='main')`
  BEFORE emitting FINAL_SOLUTION. It assembles the canonical normal-frame
  solution from your slot history, runs cancel(), and verifies the solve.
  If it returns solves=True, output the returned `solution` field as the
  FINAL_SOLUTION list — do NOT hand-construct it from invert() calls
  (WesternSicily v16 wasted 25 tool calls + 1 extra move because the
  agent tried to invert mentally and got it wrong 3 times).
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
    run_state: dict = {
        "tool_calls_remaining": max_tool_calls,
        "rs_calls_used": 0,
    }
    handlers = _build_handlers(
        scramble, slots, budget,
        dr_trigger_setup_width=dr_trigger_setup_width,
        dr_trigger_setup_depth=dr_trigger_setup_depth,
        run_state=run_state,
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
        MAX_HUMAN_RECALL=MAX_HUMAN_RECALL,
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
        # Anthropic reports usage as:
        #   input_tokens     = uncached input tokens (fresh)
        #   cache_read_input_tokens   = read from prompt cache (charged ~$0.30/M)
        #   cache_creation_input_tokens = created cache (charged ~1.25x normal input)
        # So total input volume = input + cache_read + cache_create.
        # NOTE: these are NOT summed in input_tokens — they're independent counters.
        cost_estimate = (
            input_tokens * 3.0
            + cache_read_tokens * 0.30
            + cache_create_tokens * 3.75
            + output_tokens * 15.0
        ) / 1_000_000
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

        # Prompt caching: the system prompt is ~3k tokens of static FMC
        # theory + rules and doesn't change turn-to-turn. Marking it as
        # ephemeral-cacheable means turn 2+ reads it at ~10% of normal cost
        # (Anthropic's 5-min TTL prompt cache).
        api_kwargs: dict[str, Any] = dict(
            model=model,
            max_tokens=max(4096, thinking_budget + 2048),
            system=[{
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            tools=tool_schemas,
            messages=messages,
        )
        if thinking_budget > 0:
            # Opus 4.x uses adaptive thinking instead of explicit budget_tokens.
            if "opus" in model.lower():
                api_kwargs["thinking"] = {"type": "adaptive"}
            else:
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
                run_state["tool_calls_remaining"] = max(0, max_tool_calls - tool_calls)
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
