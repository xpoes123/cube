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

from cube.analyzer.search import Solution, beam_search
from cube.analyzer.triggers import has_dr_within, tail_to_dr
from cube.classifier.features import Axis, best_eo_axis, is_dr, is_eo_solved
from cube.classifier.htr import dr_distance_to_htr
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
        return sum(len(s.moves) for s in self.stages)

    @property
    def flat_moves(self) -> tuple[Move, ...]:
        out: list[Move] = []
        for s in self.stages:
            out.extend(s.moves)
        return tuple(out)


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
            skeletons.append(Skeleton(scramble=scramble_t, stages=(eo_stage, dr_stage)))

    return skeletons


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
        last = sk.stages[-1]
        htr_d = last.htr_distance if last.htr_distance is not None else 99
        expected_total = sk.total_moves + htr_d
        return (
            -len(sk.stages),
            expected_total,
            sk.total_moves,
            -sum(s.log_prob for s in sk.stages),
        )

    return sorted(candidates, key=_rank)


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
            f"  [{st.name:>9}] {len(st.moves):>2} moves  "
            f"log-prob={st.log_prob:>6.2f}{htr_tag}  →  {moves_str}"
        )
    lines.append(f"  skeleton total: {skeleton.total_moves} moves")
    last = skeleton.stages[-1]
    if last.htr_distance is not None:
        expected = skeleton.total_moves + last.htr_distance
        lines.append(
            f"  expected to HTR: {expected} moves "
            f"(skeleton {skeleton.total_moves} + corner-distance {last.htr_distance})"
        )

    # Sanity: best EO/DR fact about the final state.
    final = skeleton.stages[-1].end_state
    axis, count = best_eo_axis(final)
    lines.append(f"  final state: best EO axis = {axis.value} ({count} bad edges)")
    return "\n".join(lines)
