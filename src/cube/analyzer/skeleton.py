"""Staged skeleton search: scramble -> EO -> DR (-> HTR -> Finish).

Stops at DR (or EO if DR fails) when no model checkpoint reaches further.
The HTR + half-turn finish extension runs for the top-ranked (EO, DR)
candidates only.

Stage targets are state predicates from `cube.classifier.features`. Each
stage runs a fresh beam search seeded with the prior stage's history (so
the policy sees context).

NISS (Normal-Inverse Scramble Switch)
-------------------------------------
Each `Stage` records the `side` it was found on (`"normal"` or `"inverse"`).
Inverse-side moves are mathematically equivalent to premoves applied to the
normal scramble: if normal-side stages produced moves N_1..N_k and inverse-
side stages produced I_1..I_j (in stage order), the full solution applied
to the scrambled state is `concat(N_*) + invert_alg(concat(I_*))`.

`Skeleton.flat_moves` already performs that stitching, so downstream code
(cancellation, full-solve verification, CLI output) works transparently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import torch

from cube.analyzer.search import a_star_search, beam_search
from cube.analyzer.triggers import has_dr_within, tail_to_dr
from cube.classifier.features import Axis, best_eo_axis, is_dr, is_eo_solved
from cube.classifier.htr import (
    dr_group_moves,
    htr_lower_bound,
    htr_solve,
    is_htr,
    is_htr_ud,
)
from cube.engine.cancellation import cancel_moves
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import invert_alg
from cube.engine.state import SOLVED, State
from cube.training.encoding import encode_move
from cube.training.model import PolicyTransformer

Side = Literal["normal", "inverse"]


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
    # State AFTER applying `moves`, in the frame of `side`. For normal-side
    # stages this is the cumulative normal-side state; for inverse-side
    # stages it's the cumulative inverse-side state (i.e. the state of the
    # inverse scramble after the inverse-side moves so far).
    end_state: State
    # Quality signal for DR stages: corner-perm distance from this state
    # to any HTR state. None for non-DR stages or when not computable.
    htr_distance: int | None = None
    # Which side this stage was searched on. Mid-solve NISS produces
    # skeletons where successive stages may differ in `side`.
    side: Side = "normal"


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
        """Move sequence applied to the scrambled state to produce the
        final state (== SOLVED for a complete skeleton).

        NISS assembly: normal-side stages concatenated in order, then
        inverse-side stages concatenated in order and `invert_alg`'d.
        """
        normal: list[Move] = []
        inverse: list[Move] = []
        for s in self.stages:
            if s.side == "inverse":
                inverse.extend(s.moves)
            else:
                normal.extend(s.moves)
        return tuple(normal) + tuple(invert_alg(inverse))

    @property
    def cancelled_moves(self) -> tuple[Move, ...]:
        """The full move sequence with local cancellations applied."""
        return tuple(cancel_moves(self.flat_moves))

    @property
    def final_state(self) -> State:
        """Normal-side state after applying the scramble and all stages."""
        return SOLVED.apply_alg(list(self.scramble) + list(self.flat_moves))

    @property
    def is_solved(self) -> bool:
        return self.final_state == SOLVED


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
    scramble_t: tuple[Move, ...],
    start_state: State,
    seed_history: tuple[Move, ...],
    side: Side,
    axis: Axis,
    history_len: int,
    device: torch.device | str,
    eo_beam_width: int,
    eo_max_depth: int,
    dr_beam_width: int,
    dr_max_depth: int,
    eo_label: str | None = None,
    dr_label: str | None = None,
) -> list[Skeleton]:
    """Run EO -> DR on one axis from `start_state`. Returns all (EO, DR)
    candidate skeletons.

    `start_state` is the state the search begins from (the scrambled state
    on normal side, or the inverse-scrambled state on inverse side).
    `seed_history` is fed to the policy as conditioning context — for
    normal side this is the scramble, for inverse it's `invert_alg(scramble)`.
    `side` is recorded on the produced stages so cross-side stitching
    works downstream.

    `eo_label`/`dr_label` override the default `"EO (UD)"` / `"DR (UD)"`
    stage names — used by the CLI / NISS callers to mark inverse stages.
    Empty list if EO didn't fire.
    """
    eo_name = eo_label or f"EO ({axis.value})"
    dr_name = dr_label or f"DR ({axis.value})"

    eo_sols = beam_search(
        model,
        start_state=start_state,
        target_predicate=lambda s: is_eo_solved(s, axis),
        beam_width=eo_beam_width,
        max_depth=eo_max_depth,
        history_len=history_len,
        device=device,
        seed_history=seed_history,
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
        eo_end_state = start_state.apply_alg(list(eo_sol.moves))
        return [Skeleton(
            scramble=scramble_t,
            stages=(Stage(
                name=eo_name,
                moves=eo_sol.moves,
                log_prob=eo_sol.log_prob,
                end_state=eo_end_state,
                side=side,
            ),),
        )]

    # Collect ALL viable (EO, DR) candidates. Each gets its own Skeleton.
    # Caller's find_skeleton ranks the union across axes.
    skeletons: list[Skeleton] = []
    seen_dr_moves: set[tuple[Move, ...]] = set()
    # Direct-DR fallback (Stage 2c) is bounded but expensive at wide beam;
    # only run it on the shortest EO per axis to cap wall time.
    direct_dr_fallback_budget = 1 if dr_beam_width > 256 else 0

    for eo_sol in eo_sols:
        eo_end_state = start_state.apply_alg(list(eo_sol.moves))
        eo_stage = Stage(
            name=eo_name,
            moves=eo_sol.moves,
            log_prob=eo_sol.log_prob,
            end_state=eo_end_state,
            side=side,
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
            seed_history=seed_history + eo_sol.moves,
            allowed_move_indices=_EO_PRESERVING[axis],
            extra_depths_after_first_hit=2,
        )
        if not trigger_sols:
            # Stage 2c (direct-DR fallback): trigger beam whiffed. If the
            # caller dialed in a wide DR budget, try a single direct
            # is_dr beam at the configured width — this catches scrambles
            # where DR is reachable but no short-tail trigger exists.
            direct_dr_sols = []
            if direct_dr_fallback_budget > 0:
                direct_dr_fallback_budget -= 1
                direct_dr_sols = beam_search(
                    model,
                    start_state=eo_end_state,
                    target_predicate=lambda s, ax=axis: is_dr(s, ax),
                    beam_width=dr_beam_width,
                    max_depth=dr_max_depth,
                    history_len=history_len,
                    device=device,
                    seed_history=seed_history + eo_sol.moves,
                    allowed_move_indices=_EO_PRESERVING[axis],
                    extra_depths_after_first_hit=2,
                )
            if not direct_dr_sols:
                # Track EO-only as a fallback option.
                skeletons.append(Skeleton(scramble=scramble_t, stages=(eo_stage,)))
                continue
            for dr_sol in direct_dr_sols:
                if dr_sol.moves in seen_dr_moves:
                    continue
                seen_dr_moves.add(dr_sol.moves)
                dr_end = eo_end_state.apply_alg(list(dr_sol.moves))
                htr_dist = htr_lower_bound(dr_end, axis)
                dr_stage = Stage(
                    name=dr_name,
                    moves=dr_sol.moves,
                    log_prob=dr_sol.log_prob,
                    end_state=dr_end,
                    htr_distance=htr_dist,
                    side=side,
                )
                skeletons.append(Skeleton(
                    scramble=scramble_t, stages=(eo_stage, dr_stage),
                ))
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
            # Tight admissible lower bound on the HTR phase: max of the
            # corner-distance and edge-distance PDBs. The corner-only
            # bound systematically under-counts when the edge structure
            # is the harder side.
            htr_dist = htr_lower_bound(dr_end, axis)
            dr_stage = Stage(
                name=dr_name,
                moves=full_dr_moves,
                log_prob=trig_sol.log_prob,
                end_state=dr_end,
                htr_distance=htr_dist,
                side=side,
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
    side: Side = "normal",
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

    `side` is recorded on the emitted stages so cross-side stitching in
    `Skeleton.flat_moves` works correctly.

    Returns the additional stages, or None on search failure.
    """
    side_tag = " [inv]" if side == "inverse" else ""

    # Fast path: already in strict-HTR.
    if is_htr(dr_end_state):
        finish = htr_solve(dr_end_state)
        if finish is None:
            return None
        return (
            Stage(name=f"HTR ({axis.value}){side_tag}", moves=(), log_prob=0.0,
                  end_state=dr_end_state, side=side),
            Stage(name=f"Finish{side_tag}", moves=tuple(finish), log_prob=0.0,
                  end_state=dr_end_state.apply_alg(finish), side=side),
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
        name=f"HTR ({axis.value}){side_tag}",
        moves=best.moves,
        log_prob=best.log_prob,
        end_state=htr_state,
        side=side,
    )

    # Step 2: If we happened to land in strict-HTR, finish with the PDB.
    # Otherwise the canonical-HTR state needs leave-slice (Milestone 2)
    # to fully solve — return HTR stage only for now.
    if is_htr(htr_state):
        finish = htr_solve(htr_state)
        if finish is not None:
            return (
                htr_stage,
                Stage(name=f"Finish{side_tag}", moves=tuple(finish),
                      log_prob=0.0,
                      end_state=htr_state.apply_alg(finish), side=side),
            )

    return (htr_stage,)


def _cumulative_normal_seq(
    scramble_t: tuple[Move, ...], stages_so_far: tuple[Stage, ...],
) -> tuple[Move, ...]:
    """Move sequence whose application to SOLVED produces the current
    NORMAL-frame cube state given the stages played so far.

    Premove formulation: `invert_alg(I_total) + scramble + N_total`, where
    I_total / N_total are the in-order concatenations of the inverse and
    normal stages' moves. The cube-state group action makes this the same
    state the user would be looking at on the normal cube during the solve.

    NOTE this is NOT the user-applied skeleton solution `Skeleton.flat_moves`
    (which is `N_total + invert_alg(I_total)`, a cyclic shift). For SOLVED
    target the two sequences are equivalent; for intermediate (DR, HTR) the
    cumulative-state formulation is required.
    """
    n_total: list[Move] = []
    i_total: list[Move] = []
    for s in stages_so_far:
        (i_total if s.side == "inverse" else n_total).extend(s.moves)
    return tuple(invert_alg(i_total)) + scramble_t + tuple(n_total)


def _cumulative_inverse_seq(
    scramble_t: tuple[Move, ...], stages_so_far: tuple[Stage, ...],
) -> tuple[Move, ...]:
    """Move sequence whose application to SOLVED produces the current
    INVERSE-frame cube state. This is the inverse of `_cumulative_normal_seq`.
    """
    return tuple(invert_alg(list(_cumulative_normal_seq(scramble_t, stages_so_far))))


def _cumulative_state(
    scramble_t: tuple[Move, ...], stages_so_far: tuple[Stage, ...], side: Side,
) -> State:
    """Current cube state on the given side after the given stages."""
    if side == "normal":
        return SOLVED.apply_alg(list(_cumulative_normal_seq(scramble_t, stages_so_far)))
    return SOLVED.apply_alg(list(_cumulative_inverse_seq(scramble_t, stages_so_far)))


def _stage_seed_history(
    scramble_t: tuple[Move, ...], stages_so_far: tuple[Stage, ...], side: Side,
) -> tuple[Move, ...]:
    """Policy-conditioning history for a NEW stage on `side`, given the
    scramble and the stages already produced.

    The policy was trained on forward sequences ending at the current
    state; the most natural seed is the cumulative side-frame sequence
    that produces the current state from SOLVED.
    """
    if side == "normal":
        return _cumulative_normal_seq(scramble_t, stages_so_far)
    return _cumulative_inverse_seq(scramble_t, stages_so_far)


def _rank_skeleton(sk: Skeleton) -> tuple[int, int, int, float]:
    """Sort key for skeleton candidates. Lower is better.

    Order:
      1. Solved skeletons (full pipeline through Finish) beat partial.
      2. More stages beat fewer.
      3. Lower expected total length (moves + htr_distance) wins.
      4. Tiebreak: fewer total moves, then higher policy log-prob.
    """
    is_solved = sk.is_solved
    if is_solved:
        expected_total = sk.total_moves
    else:
        htr_d = 99
        for st in reversed(sk.stages):
            if st.htr_distance is not None:
                htr_d = st.htr_distance
                break
        expected_total = sk.total_moves + htr_d
    return (
        0 if is_solved else 1,
        -len(sk.stages),
        expected_total,
        sk.total_moves,
        -sum(s.log_prob for s in sk.stages),
    )


def _niss_eo_dr_hybrids(
    model: PolicyTransformer,
    scramble_t: tuple[Move, ...],
    eo_skeletons: list[Skeleton],
    eo_side: Side,
    history_len: int,
    device: torch.device | str,
    dr_beam_width: int,
    dr_max_depth: int,
    max_eo_candidates: int = 2,
) -> list[Skeleton]:
    """For each EO-only skeleton produced on `eo_side`, try DR on the
    OTHER side. Returns the resulting hybrid (EO + DR) skeletons.

    Limited to `max_eo_candidates` of the shortest EOs to keep cost
    bounded — DR search dominates runtime.
    """
    other_side: Side = "inverse" if eo_side == "normal" else "normal"

    # Group skeletons by their EO stage (first stage). Many same-side
    # results share an EO and differ only in DR; we only need one base
    # per distinct EO.
    by_eo: dict[tuple[Move, ...], Skeleton] = {}
    for sk in eo_skeletons:
        if not sk.stages:
            continue
        eo_moves = sk.stages[0].moves
        prior = by_eo.get(eo_moves)
        # Prefer the EO-only variant (cleanest base) over EO+DR.
        if prior is None or len(prior.stages) > len(sk.stages):
            by_eo[eo_moves] = sk
    eo_bases = sorted(
        by_eo.values(),
        key=lambda sk: (len(sk.stages[0].moves), -sk.stages[0].log_prob),
    )[:max_eo_candidates]

    hybrids: list[Skeleton] = []
    for sk_full in eo_bases:
        # Strip everything after the EO stage — we want to switch sides
        # for the DR phase.
        sk = Skeleton(scramble=sk_full.scramble, stages=(sk_full.stages[0],))
        eo_stage = sk.stages[0]
        # Parse axis from EO stage name. EO stage was produced by
        # _try_axis so name is "EO (UD)" / "EO (FB)" / "EO (RL)" possibly
        # suffixed with " [inv]" when produced on inverse side.
        axis_str = eo_stage.name.split("(")[-1].rstrip(")")
        try:
            axis = Axis(axis_str)
        except ValueError:
            continue
        if axis not in _DR_AXES:
            continue

        # Compute starting state for the OTHER side, given the EO stage
        # already played on `eo_side`. Premove formulation: the cumulative
        # side-frame sequence reflects all moves played so far across both
        # sides.
        seed = _stage_seed_history(scramble_t, sk.stages, other_side)
        start_state = _cumulative_state(scramble_t, sk.stages, other_side)

        # Run DR-only on `other_side`. We reuse _try_axis's EO+DR pipeline
        # but skip the EO phase: the start state is already EO-solved on
        # this axis (because EO is a property of the cube, axis-symmetric
        # under inverse — see test_niss for verification).
        dr_skeletons = _dr_only_from_eo_state(
            model,
            scramble_t=scramble_t,
            stages_before=sk.stages,
            eo_axis=axis,
            start_state=start_state,
            seed_history=seed,
            side=other_side,
            history_len=history_len,
            device=device,
            dr_beam_width=dr_beam_width,
            dr_max_depth=dr_max_depth,
        )
        hybrids.extend(dr_skeletons)
    return hybrids


def _dr_only_from_eo_state(
    model: PolicyTransformer,
    scramble_t: tuple[Move, ...],
    stages_before: tuple[Stage, ...],
    eo_axis: Axis,
    start_state: State,
    seed_history: tuple[Move, ...],
    side: Side,
    history_len: int,
    device: torch.device | str,
    dr_beam_width: int,
    dr_max_depth: int,
) -> list[Skeleton]:
    """Run only the DR portion of the pipeline from an already-EO-solved
    state, on the given `side`. Appends a DR stage to `stages_before`."""
    side_tag = " [inv]" if side == "inverse" else ""
    trigger_sols = beam_search(
        model,
        start_state=start_state,
        target_predicate=lambda s, ax=eo_axis: has_dr_within(s, ax, _TAIL_LEN),
        beam_width=min(256, dr_beam_width),
        max_depth=10,
        history_len=history_len,
        device=device,
        seed_history=seed_history,
        allowed_move_indices=_EO_PRESERVING[eo_axis],
        extra_depths_after_first_hit=2,
    )
    out: list[Skeleton] = []
    seen: set[tuple[Move, ...]] = set()
    for trig in trigger_sols:
        trig_end = start_state.apply_alg(list(trig.moves))
        tail = tail_to_dr(trig_end, eo_axis, _TAIL_LEN)
        if tail is None:
            continue
        full = trig.moves + tail
        if full in seen:
            continue
        seen.add(full)
        dr_end = trig_end
        for m in tail:
            dr_end = dr_end.apply(m)
        # Use tight admissible lower bound (max of corner + edge PDBs),
        # consistent with _try_axis. Corner-only would under-rank DRs that
        # land in a hard edge structure.
        htr_d = htr_lower_bound(dr_end, eo_axis)
        dr_stage = Stage(
            name=f"DR ({eo_axis.value}){side_tag}",
            moves=full,
            log_prob=trig.log_prob,
            end_state=dr_end,
            htr_distance=htr_d,
            side=side,
        )
        out.append(Skeleton(
            scramble=scramble_t, stages=stages_before + (dr_stage,),
        ))
    return out


def find_skeleton(
    model: PolicyTransformer,
    scramble: list[Move],
    history_len: int = 32,
    device: torch.device | str = "cuda",
    eo_beam_width: int = _EO_BEAM_WIDTH,
    eo_max_depth: int = _EO_MAX_DEPTH,
    dr_beam_width: int = _DR_BEAM_WIDTH,
    dr_max_depth: int = _DR_MAX_DEPTH,
    use_niss: bool = True,
) -> list[Skeleton]:
    """Try (EO -> DR) on each axis, on both normal and inverse scrambles,
    plus NISS hybrids at the EO→DR boundary. Returns a ranked shortlist.

    NISS (Normal-Inverse Scramble Switch): EO is found on whichever side
    is easier; DR can then be found on either side. Every <22-move FMC
    solution uses NISS at some boundary.

    Set `use_niss=False` for the pre-NISS behavior (normal side only).

    "Best" = most stages reached (prefer EO+DR over EO-only), then lower
    `total_moves + htr_distance`, then fewer total moves, then higher
    policy log-prob.
    """
    scramble_t = tuple(scramble)
    scrambled = SOLVED.apply_alg(scramble)
    inv_scramble = invert_alg(list(scramble))
    inv_scrambled = SOLVED.apply_alg(inv_scramble)

    candidates: list[Skeleton] = []

    # Pass 1: normal-side pipeline on each axis.
    normal_per_axis: dict[Axis, list[Skeleton]] = {}
    for axis in (Axis.UD, Axis.FB, Axis.RL):
        skels = _try_axis(
            model, scramble_t, scrambled, scramble_t, "normal", axis,
            history_len, device,
            eo_beam_width, eo_max_depth,
            dr_beam_width, dr_max_depth,
        )
        normal_per_axis[axis] = skels
        candidates.extend(skels)

    if use_niss:
        # Pass 2: inverse-side pipeline on each axis.
        inverse_per_axis: dict[Axis, list[Skeleton]] = {}
        for axis in (Axis.UD, Axis.FB, Axis.RL):
            skels = _try_axis(
                model, scramble_t, inv_scrambled, tuple(inv_scramble),
                "inverse", axis,
                history_len, device,
                eo_beam_width, eo_max_depth,
                dr_beam_width, dr_max_depth,
                eo_label=f"EO ({axis.value}) [inv]",
                dr_label=f"DR ({axis.value}) [inv]",
            )
            inverse_per_axis[axis] = skels
            candidates.extend(skels)

        # Pass 3: NISS at EO→DR boundary. For each side that found EO but
        # not DR (or even for those that did, since the inverse side's DR
        # may be shorter), try the OTHER side for DR.
        for axis in (Axis.UD, Axis.FB, Axis.RL):
            candidates.extend(_niss_eo_dr_hybrids(
                model, scramble_t, normal_per_axis[axis],
                eo_side="normal",
                history_len=history_len, device=device,
                dr_beam_width=dr_beam_width, dr_max_depth=dr_max_depth,
            ))
            candidates.extend(_niss_eo_dr_hybrids(
                model, scramble_t, inverse_per_axis[axis],
                eo_side="inverse",
                history_len=history_len, device=device,
                dr_beam_width=dr_beam_width, dr_max_depth=dr_max_depth,
            ))

    if not candidates:
        return [Skeleton(scramble=scramble_t, stages=())]

    candidates = sorted(candidates, key=_rank_skeleton)

    # Extend the top (EO, DR) candidates with HTR + Finish stages. The A*
    # DR → HTR with the tight htr_lower_bound heuristic is fast (~0.1s),
    # so we can afford a larger N. More candidates → better odds the
    # shortest cancelled-total solution is reached.
    #
    # NISS at DR→HTR boundary: for each candidate, we try the HTR/Finish
    # extension on BOTH the DR's own side AND the opposite side. EO=0
    # and CO=0 are subgroups of G (closed under inverse), so a DR-on-UD
    # state in one frame is also DR-on-UD in the other. The two
    # extensions produce different skeletons that may cancel better
    # with the EO/DR boundary; ranking picks the shortest.
    _EXTEND_TOP_N = 12
    extended: list[Skeleton] = []
    for sk in candidates[:_EXTEND_TOP_N]:
        if len(sk.stages) < 2:
            extended.append(sk)
            continue
        dr_stage = sk.stages[-1]
        # Parse axis from DR stage name "DR (XX)" or "DR (XX) [inv]".
        axis_str = dr_stage.name.split("(")[-1].split(")")[0]
        try:
            axis = Axis(axis_str)
        except ValueError:
            extended.append(sk)
            continue

        # Sides to try for the HTR extension: the DR's own side always,
        # plus the opposite side when NISS is enabled.
        same_side: Side = dr_stage.side
        try_sides: list[Side] = [same_side]
        if use_niss:
            other_side: Side = "inverse" if same_side == "normal" else "normal"
            try_sides.append(other_side)

        found_ext_for_sk = False
        for htr_side in try_sides:
            if htr_side == same_side:
                start = dr_stage.end_state
            else:
                start = _cumulative_state(sk.scramble, sk.stages, htr_side)
            seed = _stage_seed_history(sk.scramble, sk.stages, htr_side)
            ext = _extend_to_htr_and_finish(
                model, start, axis, history_len, device, seed,
                side=htr_side,
            )
            if ext is not None:
                extended.append(Skeleton(
                    scramble=sk.scramble, stages=sk.stages + ext,
                ))
                found_ext_for_sk = True
        if not found_ext_for_sk:
            extended.append(sk)

    # Rest of candidates unchanged.
    extended.extend(candidates[_EXTEND_TOP_N:])
    # Re-sort: extended (full-solve) candidates float to top.
    return sorted(extended, key=_rank_skeleton)


def find_skeleton_inverse(
    model: PolicyTransformer,
    scramble: list[Move],
    history_len: int = 32,
    device: torch.device | str = "cuda",
    eo_beam_width: int = _EO_BEAM_WIDTH,
    eo_max_depth: int = _EO_MAX_DEPTH,
    dr_beam_width: int = _DR_BEAM_WIDTH,
    dr_max_depth: int = _DR_MAX_DEPTH,
) -> list[Skeleton]:
    """Inverse-only pipeline: run the full search on the inverse scramble.

    Returns skeletons whose stages are all `side="inverse"`. Their
    `flat_moves` are correctly remapped to solve the NORMAL scramble
    (i.e. `inverted-stage-concat-then-applied-as-premoves`).

    Useful as a diagnostic and as an entry point when you specifically
    want to ignore the normal side. `find_skeleton` already tries the
    inverse side as part of its full sweep.
    """
    scramble_t = tuple(scramble)
    inv_scramble = invert_alg(list(scramble))
    inv_scrambled = SOLVED.apply_alg(inv_scramble)

    candidates: list[Skeleton] = []
    for axis in (Axis.UD, Axis.FB, Axis.RL):
        candidates.extend(_try_axis(
            model, scramble_t, inv_scrambled, tuple(inv_scramble),
            "inverse", axis,
            history_len, device,
            eo_beam_width, eo_max_depth,
            dr_beam_width, dr_max_depth,
            eo_label=f"EO ({axis.value}) [inv]",
            dr_label=f"DR ({axis.value}) [inv]",
        ))
    if not candidates:
        return [Skeleton(scramble=scramble_t, stages=())]
    candidates = sorted(candidates, key=_rank_skeleton)

    # HTR + finish extension on top-N, same as find_skeleton.
    _EXTEND_TOP_N = 3
    extended: list[Skeleton] = []
    for sk in candidates[:_EXTEND_TOP_N]:
        if len(sk.stages) < 2:
            extended.append(sk)
            continue
        dr_stage = sk.stages[-1]
        axis_str = dr_stage.name.split("(")[-1].split(")")[0]
        try:
            axis = Axis(axis_str)
        except ValueError:
            extended.append(sk)
            continue
        seed = _stage_seed_history(sk.scramble, sk.stages, "inverse")
        ext = _extend_to_htr_and_finish(
            model, dr_stage.end_state, axis, history_len, device, seed,
            side="inverse",
        )
        if ext is not None:
            extended.append(Skeleton(scramble=sk.scramble, stages=sk.stages + ext))
        else:
            extended.append(sk)
    extended.extend(candidates[_EXTEND_TOP_N:])
    return sorted(extended, key=_rank_skeleton)


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
        side_tag = "  [inv]" if st.side == "inverse" else ""
        lines.append(
            f"  [{st.name:>16}] {len(st.moves):>2} moves  "
            f"log-prob={st.log_prob:>6.2f}{htr_tag}{side_tag}  →  {moves_str}"
        )
    saved = skeleton.total_moves_raw - skeleton.total_moves
    saved_tag = f" (cancellation saved {saved})" if saved > 0 else ""
    lines.append(f"  total: {skeleton.total_moves} moves{saved_tag}")

    final = skeleton.final_state
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
