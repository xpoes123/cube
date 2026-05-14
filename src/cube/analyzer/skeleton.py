"""Staged skeleton search: scramble -> EO -> DR.

Stops at DR (or EO if DR fails). Does not attempt the finish — per
project framing, the analyzer produces a human-style skeleton, not an
end-to-end solve. The cycle-reduction / 4e4c-finish step is intentionally
out of scope here.

Stage targets are state predicates from `cube.classifier.features`. Each
stage runs a fresh beam search seeded with the prior stage's history (so
the policy sees context).
"""

from __future__ import annotations

from dataclasses import dataclass

import torch

from cube.analyzer.search import Solution, a_star_search, beam_search
from cube.analyzer.triggers import has_dr_within, tail_to_dr
from cube.classifier.features import Axis, best_eo_axis, is_dr, is_eo_solved
from cube.engine.cancellation import cancel_moves
from cube.classifier.htr import (
    dr_distance_to_htr,
    dr_group_moves,
    htr_distance,
    htr_lower_bound,
    htr_solve,
    is_htr,
    is_htr_ud,
)
from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED, State
from cube.training.encoding import encode_move
from cube.training.model import PolicyTransformer


# EO-preserving move sets, one per axis. Each face whose quarter turns
# flip that axis's EO is EXCLUDED. Half-turns are always preserved (double
# flip cancels). For example, UD-axis EO is flipped by F/B quarters, so
# UD-preserving moves are everything except F/F'/B/B' (14 of 18 moves).
def _eo_preserving_moves(axis: Axis) -> tuple[int, ...]:
    if axis == Axis.UD:
        flipping_faces = (Face.F, Face.B)
    elif axis == Axis.FB:
        flipping_faces = (Face.L, Face.R)
    elif axis == Axis.RL:
        flipping_faces = (Face.U, Face.D)
    else:
        raise ValueError(f"unknown axis: {axis}")

    out: list[int] = []
    for face in Face:
        for turn in Turn:
            # Quarter turns on flipping faces break EO; half turns don't.
            if face in flipping_faces and turn != Turn.HALF:
                continue
            out.append(encode_move(Move(face, turn)))
    return tuple(out)


_EO_PRESERVING: dict[Axis, tuple[int, ...]] = {
    a: _eo_preserving_moves(a) for a in Axis
}


# DR-group move indices (axis-specific): the set of moves that preserve DR
# on that axis. UD axis = ⟨U, D, R², L², F², B²⟩ = 10 moves.
_DR_PRESERVING: dict[Axis, tuple[int, ...]] = {
    a: tuple(encode_move(m) for m in dr_group_moves(a)) for a in Axis
}


# How many moves the tail-search may use to reach DR from a beam state.
# Each predicate call is O(18^K). K=2 means ~324 ops per state which is
# fast enough for beam_width=256 at typical depths.
_TAIL_LEN = 2


@dataclass(frozen=True, slots=True)
class Stage:
    name: str           # human-readable: "EO (UD)", "DR (UD)", …
    moves: tuple[Move, ...]
    log_prob: float
    end_state: State    # state after applying these moves
    # Quality signal for DR stages: corner-perm distance from this state
    # to any HTR state. None for non-DR stages or when not computable.
    htr_distance: int | None = None


@dataclass(frozen=True, slots=True)
class Skeleton:
    scramble: tuple[Move, ...]
    stages: tuple[Stage, ...]

    @property
    def total_moves(self) -> int:
        """Move count AFTER stage-boundary cancellation."""
        return len(self.cancelled_moves)

    @property
    def total_moves_raw(self) -> int:
        """Raw move count, summed across stages without cancellation."""
        return sum(len(s.moves) for s in self.stages)

    @property
    def flat_moves(self) -> tuple[Move, ...]:
        out: list[Move] = []
        for s in self.stages:
            out.extend(s.moves)
        return tuple(out)

    @property
    def cancelled_moves(self) -> tuple[Move, ...]:
        """The full move sequence with local cancellations applied."""
        return tuple(cancel_moves(self.flat_moves))


# Stage parameter defaults. EO is shallow (humans usually find EO in <8
# moves) and cheap. DR is the expensive stage — the policy is too peaked
# to find DR with modest beams without a value function. Empirically,
# beam=8192/depth=14 finds 9-move DR in ~20s for typical scrambles.
_EO_MAX_DEPTH = 10
_EO_BEAM_WIDTH = 256
_DR_MAX_DEPTH = 14
_DR_BEAM_WIDTH = 8192

# Multi-axis CO is now implemented (classifier.features._corner_axis_oriented),
# so DR is genuinely axis-aware. We try all three axes by default.
_DR_AXES = (Axis.UD, Axis.FB, Axis.RL)


def _try_axis(
    model: PolicyTransformer,
    scrambled: State,
    scramble_t: tuple[Move, ...],
    axis: Axis,
    history_len: int,
    device: torch.device | str,
    eo_beam_width: int,
    eo_max_depth: int,
    dr_beam_width: int,
    dr_max_depth: int,
) -> list[Skeleton]:
    """Run EO -> DR on one axis. Returns all (EO, DR) candidate skeletons.

    Empty list if EO didn't fire. Multiple skeletons enable downstream
    ranking and shortlist presentation — the human practice of
    considering several DR candidates before committing.
    """
    eo_sols = beam_search(
        model,
        start_state=scrambled,
        target_predicate=lambda s: is_eo_solved(s, axis),
        beam_width=eo_beam_width,
        max_depth=eo_max_depth,
        history_len=history_len,
        device=device,
        seed_history=scramble_t,
        extra_depths_after_first_hit=2,
    )
    if not eo_sols:
        return []
    # Cap how many EOs we explore — each one triggers a costly DR search.
    # Per spec, we want diversity in the shortlist; for now just take the
    # K shortest unique EO move sequences.
    EO_CANDIDATES = 5
    eo_sols = sorted(eo_sols, key=lambda s: (len(s), -s.log_prob))[:EO_CANDIDATES]

    # If we can't do DR on this axis, return a single EO-only skeleton.
    if axis not in _DR_AXES:
        eo_sol = eo_sols[0]
        eo_end_state = scrambled.apply_alg(list(eo_sol.moves))
        return [Skeleton(
            scramble=scramble_t,
            stages=(Stage(
                name=f"EO ({axis.value})",
                moves=eo_sol.moves,
                log_prob=eo_sol.log_prob,
                end_state=eo_end_state,
            ),),
        )]

    # Collect ALL viable (EO, DR) candidates. Each gets its own Skeleton.
    # Caller's find_skeleton ranks the union across axes.
    skeletons: list[Skeleton] = []
    seen_dr_moves: set[tuple[Move, ...]] = set()

    for eo_sol in eo_sols:
        eo_end_state = scrambled.apply_alg(list(eo_sol.moves))
        eo_stage = Stage(
            name=f"EO ({axis.value})",
            moves=eo_sol.moves,
            log_prob=eo_sol.log_prob,
            end_state=eo_end_state,
        )

        # Stage 2a: search for trigger states (≤_TAIL_LEN from DR).
        trigger_sols = beam_search(
            model,
            start_state=eo_end_state,
            target_predicate=lambda s, ax=axis: has_dr_within(s, ax, _TAIL_LEN),
            beam_width=256,
            max_depth=10,
            history_len=history_len,
            device=device,
            seed_history=scramble_t + eo_sol.moves,
            allowed_move_indices=_EO_PRESERVING[axis],
            extra_depths_after_first_hit=2,
        )
        if not trigger_sols:
            # Track EO-only as a fallback option.
            skeletons.append(Skeleton(scramble=scramble_t, stages=(eo_stage,)))
            continue

        # Stage 2b: for each trigger-state, compute the shortest tail.
        for trig_sol in trigger_sols:
            trigger_end = eo_end_state.apply_alg(list(trig_sol.moves))
            tail = tail_to_dr(trigger_end, axis, _TAIL_LEN)
            if tail is None:
                continue

            full_dr_moves = trig_sol.moves + tail
            full_path = eo_sol.moves + full_dr_moves
            if full_path in seen_dr_moves:
                continue
            seen_dr_moves.add(full_path)

            dr_end = trigger_end
            for m in tail:
                dr_end = dr_end.apply(m)
            htr_dist = dr_distance_to_htr(dr_end, axis)
            dr_stage = Stage(
                name=f"DR ({axis.value})",
                moves=full_dr_moves,
                log_prob=trig_sol.log_prob,
                end_state=dr_end,
                htr_distance=htr_dist,
            )
            # Note: HTR + Finish extension is run later in find_skeleton
            # for only the top-N (EO, DR) candidates by expected total —
            # too expensive to run per (EO, DR) here.
            skeletons.append(Skeleton(
                scramble=scramble_t, stages=(eo_stage, dr_stage),
            ))

    return skeletons


def _extend_to_htr_and_finish(
    model: PolicyTransformer,
    dr_end_state: State,
    axis: Axis,
    history_len: int,
    device: torch.device | str,
    seed_history: tuple[Move, ...],
) -> tuple[Stage, ...] | None:
    """Search DR → canonical HTR (M1) and finish via PDB when possible.

    Two-step:
      1. A* in the DR-group (`dr_group_moves`) from `dr_end_state` to
         any state satisfying `is_htr_ud` (single-axis HTR). Heuristic
         is `htr_lower_bound` = max(corner_dist, edge_dist), admissible
         because each DR move affects at most 4 corners and 4 edges.
      2. If the landed canonical-HTR state is ALSO strict-HTR (multi-
         axis EO/CO all zero), apply `htr_solve` PDB for the optimal
         half-turn finish. Otherwise emit the HTR stage and stop here —
         the leave-slice finish is Milestone 2 work.

    Returns the additional stages, or None on search failure.
    """
    # Fast path: already in strict-HTR.
    if is_htr(dr_end_state):
        finish = htr_solve(dr_end_state)
        if finish is None:
            return None
        return (
            Stage(name=f"HTR ({axis.value})", moves=(), log_prob=0.0,
                  end_state=dr_end_state),
            Stage(name="Finish", moves=tuple(finish), log_prob=0.0,
                  end_state=dr_end_state.apply_alg(finish)),
        )

    # Step 1: A* DR → canonical HTR with DR-group action mask.
    def h(state: State) -> int:
        bound = htr_lower_bound(state, axis)
        return bound if bound is not None else 0

    # Pure A* (policy_weight=0) — the corner+edge heuristic is tight
    # enough that the policy was just adding model-eval overhead without
    # meaningfully improving the search. Empirically 9-move DR→HTR in
    # <0.1s on the test scramble.
    htr_sols = a_star_search(
        None,  # no model needed when policy_weight=0
        start_state=dr_end_state,
        target_predicate=is_htr_ud,
        heuristic=h,
        max_depth=16,
        max_nodes=200_000,
        history_len=history_len,
        device=device,
        seed_history=seed_history,
        allowed_move_indices=_DR_PRESERVING[axis],
        policy_weight=0.0,
    )
    if not htr_sols:
        return None

    best = htr_sols[0]
    htr_state = dr_end_state.apply_alg(list(best.moves))
    htr_stage = Stage(
        name=f"HTR ({axis.value})",
        moves=best.moves,
        log_prob=best.log_prob,
        end_state=htr_state,
    )

    # Step 2: If we happened to land in strict-HTR, finish with the PDB.
    # Otherwise the canonical-HTR state needs leave-slice (Milestone 2)
    # to fully solve — return HTR stage only for now.
    if is_htr(htr_state):
        finish = htr_solve(htr_state)
        if finish is not None:
            return (
                htr_stage,
                Stage(name="Finish", moves=tuple(finish), log_prob=0.0,
                      end_state=htr_state.apply_alg(finish)),
            )

    return (htr_stage,)


def find_skeleton(
    model: PolicyTransformer,
    scramble: list[Move],
    history_len: int = 32,
    device: torch.device | str = "cuda",
    eo_beam_width: int = _EO_BEAM_WIDTH,
    eo_max_depth: int = _EO_MAX_DEPTH,
    dr_beam_width: int = _DR_BEAM_WIDTH,
    dr_max_depth: int = _DR_MAX_DEPTH,
) -> list[Skeleton]:
    """Try (EO -> DR) on each axis; return a ranked shortlist of skeletons.

    Returns all viable (EO, DR) candidates sorted by expected total
    length to HTR. The caller picks the top-K to display.

    "Best" = most stages reached (prefer EO+DR over EO-only), then lower
    `total_moves + htr_distance`, then fewer total moves, then higher
    policy log-prob.
    """
    scrambled = SOLVED.apply_alg(scramble)
    scramble_t = tuple(scramble)

    candidates: list[Skeleton] = []
    for axis in (Axis.UD, Axis.FB, Axis.RL):
        candidates.extend(_try_axis(
            model, scrambled, scramble_t, axis,
            history_len, device,
            eo_beam_width, eo_max_depth,
            dr_beam_width, dr_max_depth,
        ))

    if not candidates:
        return [Skeleton(scramble=scramble_t, stages=())]

    # Rank candidates:
    # 1. Prefer more stages (EO+DR over EO-only).
    # 2. Among full skeletons with known htr_distance, prefer lower total
    #    "expected length" = dr_length + htr_distance. This is the key
    #    "good subset beats short DR" criterion from the FMC method docs.
    # 3. Tiebreak by total moves, then policy log-prob.
    def _rank(sk: Skeleton) -> tuple[int, int, int, float]:
        # Skeletons that include a full Finish stage have known actual
        # length. Skeletons stopping at DR estimate via htr_distance.
        is_solved = (
            len(sk.stages) >= 1 and sk.stages[-1].end_state == SOLVED
        )
        if is_solved:
            expected_total = sk.total_moves
        else:
            # Find DR stage's htr_distance (last stage with htr_distance set).
            htr_d = 99
            for st in reversed(sk.stages):
                if st.htr_distance is not None:
                    htr_d = st.htr_distance
                    break
            expected_total = sk.total_moves + htr_d
        return (
            # Prefer solved skeletons over partial.
            0 if is_solved else 1,
            # Prefer more stages.
            -len(sk.stages),
            # Prefer lower expected total.
            expected_total,
            sk.total_moves,
            -sum(s.log_prob for s in sk.stages),
        )

    candidates = sorted(candidates, key=_rank)

    # Extend the top few (EO, DR) candidates with HTR + Finish stages.
    # We only do this for the top-N because each call is expensive
    # (~30s for the DR → HTR beam search). The HTR PDB ensures finish
    # is O(1) once HTR is reached.
    _EXTEND_TOP_N = 3
    extended: list[Skeleton] = []
    for sk in candidates[:_EXTEND_TOP_N]:
        if len(sk.stages) < 2:
            extended.append(sk)
            continue
        # Last stage is the DR. Get axis from its name "DR (XX)".
        dr_stage = sk.stages[-1]
        dr_end = dr_stage.end_state
        axis_str = dr_stage.name.split("(")[-1].rstrip(")")
        try:
            axis = Axis(axis_str)
        except ValueError:
            extended.append(sk)
            continue
        seed = sk.scramble + tuple(
            m for st in sk.stages for m in st.moves
        )
        ext = _extend_to_htr_and_finish(
            model, dr_end, axis, history_len, device, seed,
        )
        if ext is not None:
            extended.append(Skeleton(
                scramble=sk.scramble, stages=sk.stages + ext,
            ))
        else:
            extended.append(sk)

    # Rest of candidates unchanged.
    extended.extend(candidates[_EXTEND_TOP_N:])
    # Re-sort: extended (full-solve) candidates float to top.
    return sorted(extended, key=_rank)


def find_best_skeleton(*args, **kwargs) -> Skeleton:
    """Convenience: just the top-ranked skeleton."""
    ranked = find_skeleton(*args, **kwargs)
    return ranked[0]


def format_skeleton(skeleton: Skeleton) -> str:
    """Pretty-print a skeleton for the CLI."""
    lines: list[str] = []
    lines.append(f"scramble: {' '.join(str(m) for m in skeleton.scramble)}")
    if not skeleton.stages:
        lines.append("  (no stages found)")
        return "\n".join(lines)

    for st in skeleton.stages:
        moves_str = " ".join(str(m) for m in st.moves)
        htr_tag = ""
        if st.htr_distance is not None:
            htr_tag = f"  +{st.htr_distance}→HTR"
        lines.append(
            f"  [{st.name:>12}] {len(st.moves):>2} moves  "
            f"log-prob={st.log_prob:>6.2f}{htr_tag}  →  {moves_str}"
        )
    saved = skeleton.total_moves_raw - skeleton.total_moves
    saved_tag = f" (cancellation saved {saved})" if saved > 0 else ""
    lines.append(f"  total: {skeleton.total_moves} moves{saved_tag}")

    final = skeleton.stages[-1].end_state
    if final == SOLVED:
        lines.append(f"  ✓ SOLVES the scramble in {skeleton.total_moves} moves")
        # Full solution (with cancellation applied) for copy/paste.
        all_moves = " ".join(str(m) for m in skeleton.cancelled_moves)
        lines.append(f"  full solution: {all_moves}")
    else:
        last = skeleton.stages[-1]
        if last.htr_distance is not None:
            expected = skeleton.total_moves + last.htr_distance
            lines.append(
                f"  expected to HTR: {expected} moves "
                f"(partial: {skeleton.total_moves} + corner-distance {last.htr_distance})"
            )
        axis, count = best_eo_axis(final)
        lines.append(f"  final state: best EO axis = {axis.value} ({count} bad edges)")
    return "\n".join(lines)
