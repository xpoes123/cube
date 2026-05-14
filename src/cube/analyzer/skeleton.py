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
from cube.classifier.features import Axis, best_eo_axis, is_dr, is_eo_solved
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


@dataclass(frozen=True, slots=True)
class Stage:
    name: str           # human-readable: "EO (UD)", "DR (UD)", …
    moves: tuple[Move, ...]
    log_prob: float
    end_state: State    # state after applying these moves


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

# DR predicate is currently UD-axis-CO-strict, so only attempt DR on UD
# axis. FB/RL stages return EO-only. Multi-axis CO is a follow-up.
_DR_AXES = (Axis.UD,)


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
) -> Skeleton | None:
    """Run EO -> DR on one axis. Returns None if EO didn't fire."""
    eo_sols = beam_search(
        model,
        start_state=scrambled,
        target_predicate=lambda s: is_eo_solved(s, axis),
        beam_width=eo_beam_width,
        max_depth=eo_max_depth,
        history_len=history_len,
        device=device,
        seed_history=scramble_t,
    )
    if not eo_sols:
        return None

    eo_sol = eo_sols[0]
    eo_end_state = scrambled.apply_alg(list(eo_sol.moves))
    eo_stage = Stage(
        name=f"EO ({axis.value})",
        moves=eo_sol.moves,
        log_prob=eo_sol.log_prob,
        end_state=eo_end_state,
    )

    if axis not in _DR_AXES:
        # DR predicate is too strict on this axis (UD-CO required); skip.
        return Skeleton(scramble=scramble_t, stages=(eo_stage,))

    # DR stage: mask to EO-preserving moves so the search doesn't undo Stage 1.
    dr_sols = beam_search(
        model,
        start_state=eo_end_state,
        target_predicate=lambda s: is_dr(s, axis),
        beam_width=dr_beam_width,
        max_depth=dr_max_depth,
        history_len=history_len,
        device=device,
        seed_history=scramble_t + eo_sol.moves,
        allowed_move_indices=_EO_PRESERVING[axis],
    )
    if not dr_sols:
        return Skeleton(scramble=scramble_t, stages=(eo_stage,))

    dr_sol = dr_sols[0]
    dr_end_state = eo_end_state.apply_alg(list(dr_sol.moves))
    dr_stage = Stage(
        name=f"DR ({axis.value})",
        moves=dr_sol.moves,
        log_prob=dr_sol.log_prob,
        end_state=dr_end_state,
    )
    return Skeleton(scramble=scramble_t, stages=(eo_stage, dr_stage))


def find_skeleton(
    model: PolicyTransformer,
    scramble: list[Move],
    history_len: int = 32,
    device: torch.device | str = "cuda",
    eo_beam_width: int = _EO_BEAM_WIDTH,
    eo_max_depth: int = _EO_MAX_DEPTH,
    dr_beam_width: int = _DR_BEAM_WIDTH,
    dr_max_depth: int = _DR_MAX_DEPTH,
) -> Skeleton:
    """Try (EO -> DR) on each axis; return the best skeleton.

    "Best" = most stages reached (prefer EO+DR over EO-only), then fewest
    total moves, then highest log-prob.

    DR detection is currently UD-axis-CO-strict (see classifier.features
    docstring). In practice this means UD-axis usually wins for any
    scramble where DR is reachable at all; the FB/RL pathways still try
    but only get to EO.
    """
    scrambled = SOLVED.apply_alg(scramble)
    scramble_t = tuple(scramble)

    candidates: list[Skeleton] = []
    for axis in (Axis.UD, Axis.FB, Axis.RL):
        sk = _try_axis(
            model, scrambled, scramble_t, axis,
            history_len, device,
            eo_beam_width, eo_max_depth,
            dr_beam_width, dr_max_depth,
        )
        if sk is not None and sk.stages:
            candidates.append(sk)

    if not candidates:
        return Skeleton(scramble=scramble_t, stages=())

    # Prefer the most-complete skeleton; tiebreak by total moves then log-prob.
    def _rank(sk: Skeleton) -> tuple[int, int, float]:
        return (
            -len(sk.stages),           # more stages first (negate for ascending sort)
            sk.total_moves,            # then fewer total moves
            -sum(s.log_prob for s in sk.stages),  # then higher cumulative log-prob
        )

    return min(candidates, key=_rank)


def format_skeleton(skeleton: Skeleton) -> str:
    """Pretty-print a skeleton for the CLI."""
    lines: list[str] = []
    lines.append(f"scramble: {' '.join(str(m) for m in skeleton.scramble)}")
    if not skeleton.stages:
        lines.append("  (no stages found)")
        return "\n".join(lines)

    for st in skeleton.stages:
        moves_str = " ".join(str(m) for m in st.moves)
        lines.append(
            f"  [{st.name:>9}] {len(st.moves):>2} moves  "
            f"log-prob={st.log_prob:>6.2f}  →  {moves_str}"
        )
    lines.append(f"  skeleton total: {skeleton.total_moves} moves")

    # Sanity: best EO/DR fact about the final state.
    final = skeleton.stages[-1].end_state
    axis, count = best_eo_axis(final)
    lines.append(f"  final state: best EO axis = {axis.value} ({count} bad edges)")
    return "\n".join(lines)
