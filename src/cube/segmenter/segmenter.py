"""Main segmenter: take a Reconstruction, return a SegmentedReconstruction.

Strategy:
1. If the comment has parseable phase annotations, use those (comment-based).
2. Otherwise, walk the solution state-by-state and segment at milestone
   transitions (state-based fallback).
3. Cross-validate: when comment-based, also run state-based and flag
   discrepancies as issues.
"""

from __future__ import annotations

from cube.classifier import Axis, best_eo_axis, is_dr, is_eo_solved
from cube.corpus.types import Reconstruction
from cube.engine.notation import NissAlg
from cube.engine.state import SOLVED, State
from cube.segmenter.comment import RawPhase, parse_phase_comments
from cube.segmenter.labels import canonicalize
from cube.segmenter.types import (
    Method,
    Phase,
    PhaseSegment,
    SegmentedReconstruction,
)


def segment(reconstruction: Reconstruction) -> SegmentedReconstruction:
    """Segment a reconstruction into labeled phases."""
    raw = parse_phase_comments(reconstruction.commentary)
    if raw:
        segments, issues = _segments_from_comment(reconstruction, raw)
        source = "comment"
    else:
        segments = _segments_from_state(reconstruction)
        issues = ()
        source = "state"

    method = _infer_method(segments)
    return SegmentedReconstruction(
        reconstruction=reconstruction,
        segments=tuple(segments),
        method=method,
        source=source,
        issues=tuple(issues),
    )


# ---------- Comment-driven segmentation ----------


def _segments_from_comment(
    rec: Reconstruction, raw: list[RawPhase]
) -> tuple[list[PhaseSegment], list[str]]:
    """Build segments from author-labeled lines, applying moves and capturing
    state at each phase boundary."""
    segments: list[PhaseSegment] = []
    issues: list[str] = []
    state = SOLVED.apply_alg(rec.scramble)
    cumulative = 0

    for idx, rp in enumerate(raw):
        phase_moves = rp.moves.flat()
        new_state = state.apply_alg(phase_moves)
        cumulative += len(phase_moves)

        # Sanity: author's reported cumulative should match our actual.
        if rp.author_cumulative != cumulative:
            issues.append(
                f"phase {idx}: author cumulative={rp.author_cumulative} "
                f"but actual={cumulative}"
            )

        phase = canonicalize(rp.raw_label)
        # Multi-axis cross-validation: when the phase claims EO or DR, verify
        # the state actually reaches it on SOME axis. If author labeled EO but
        # no axis has all edges oriented, flag — the label may be a pseudo-EO
        # or a typo.
        if phase == Phase.EO:
            axis, count = best_eo_axis(new_state)
            if count > 0:
                issues.append(
                    f"phase {idx}: labeled EO but best axis ({axis.value}) "
                    f"has {count} bad edges"
                )
        elif phase == Phase.DR:
            if not any(is_dr(new_state, a) for a in Axis):
                # Couldn't confirm DR on any axis. CO might be on a non-UD
                # axis (which we don't yet detect), so this is informational.
                bad_eo = min(_eo_count_any(new_state, a) for a in Axis)
                if bad_eo > 0:
                    issues.append(
                        f"phase {idx}: labeled DR but no axis has EO solved "
                        f"(best has {bad_eo} bad edges)"
                    )

        segments.append(
            PhaseSegment(
                phase=phase,
                raw_label=rp.raw_label,
                moves=rp.moves,
                state_at_end=new_state,
                phase_move_count=len(phase_moves),
                cumulative_count=cumulative,
                author_cumulative=rp.author_cumulative,
                author_phase_count=rp.author_phase_count,
            )
        )
        state = new_state

    return segments, issues


# ---------- Helpers ----------


def _eo_count_any(state: State, axis: Axis) -> int:
    from cube.classifier import eo_count
    return eo_count(state, axis)


# ---------- State-driven segmentation (fallback) ----------


def _segments_from_state(rec: Reconstruction) -> list[PhaseSegment]:
    """When no comment exists, walk the flat solution and place phase
    boundaries at milestone transitions (EO/DR/SOLVED).

    Limitation (v0): milestone detection is UD-axis only. Non-UD solves
    will fall through to a single PRE_EO segment plus a FINISH segment
    when SOLVED is reached. Multi-axis detection is task #9.
    """
    from cube.classifier import is_dr, is_eo_solved

    flat_moves = rec.solution.flat()
    state = SOLVED.apply_alg(rec.scramble)

    # Run through every prefix, mark first index where each milestone holds.
    milestones: list[tuple[int, Phase]] = []
    reached_eo = False
    reached_dr = False
    cur = state
    for i, m in enumerate(flat_moves, start=1):
        cur = cur.apply(m)
        if not reached_eo and is_eo_solved(cur):
            milestones.append((i, Phase.EO))
            reached_eo = True
        if not reached_dr and is_dr(cur):
            milestones.append((i, Phase.DR))
            reached_dr = True
        if cur == SOLVED:
            milestones.append((i, Phase.FINISH))
            break

    # Build segments between milestones. Pre-EO moves get PRE_EO.
    segments: list[PhaseSegment] = []
    prev_idx = 0
    cur = state
    last_phase: Phase | None = None
    for idx, phase in milestones:
        sub = flat_moves[prev_idx:idx]
        sub_alg = NissAlg(normal=list(sub), inverse=[])
        cur = cur.apply_alg(sub)
        # The first segment (before EO) is PRE_EO if there are pre-EO moves.
        seg_phase = Phase.PRE_EO if last_phase is None and phase != Phase.EO else phase
        segments.append(
            PhaseSegment(
                phase=seg_phase if last_phase is None else phase,
                raw_label="",
                moves=sub_alg,
                state_at_end=cur,
                phase_move_count=len(sub),
                cumulative_count=idx,
            )
        )
        prev_idx = idx
        last_phase = phase

    return segments


# ---------- Method inference ----------


def _infer_method(segments: list[PhaseSegment]) -> Method:
    phases = [s.phase for s in segments]
    has_eo = Phase.EO in phases
    has_dr = Phase.DR in phases
    has_htr = Phase.HTR in phases
    has_block = Phase.BLOCK in phases
    has_eoline = Phase.EOLINE in phases

    if has_dr or has_htr:
        return Method.DR
    if has_eoline:
        return Method.ZZ
    if has_block:
        return Method.BLOCKBUILDING
    if has_eo:
        # EO without DR is most likely ZZ-style.
        return Method.ZZ
    return Method.UNKNOWN
