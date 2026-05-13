"""Training example schema: one (state, move) pair per move in a reconstruction.

Model architecture is deliberately not committed yet — TrainingExample stays
model-agnostic. Concrete encoders (state → tensor, history → tensor, etc.)
live in a separate module once the model is chosen.

Walking strategy (v1): flatten the NissAlg into a single move sequence
(`normal + invert(inverse)`) and emit one example per move on the flat
sequence. This is the simplest BC formulation — the model sees the
post-insertion final solution. It doesn't separate skeleton from insertion;
that's a v2 refinement.

Phase labels are attached per move using the segmenter's cumulative_count
ranges. Moves past the last labeled phase (e.g., insertion-extension moves
in solves where author labeled only the skeleton) get phase=None.
"""

from __future__ import annotations

from dataclasses import dataclass

from cube.engine.moves import Move
from cube.engine.state import SOLVED, State
from cube.segmenter.types import Method, Phase, SegmentedReconstruction


@dataclass(frozen=True, slots=True)
class TrainingExample:
    """One supervised example: predict `target_move` given context.

    Carries enough to reconstruct the cube position via engine application
    without needing to store the State directly (which is large). Concrete
    encoders use `state_before` if they want the cubie tuples directly.
    """

    source_id: str            # reconstruction's source_id, for traceability + grouping
    move_index: int           # position in the flat solution (0-indexed)
    state_before: State       # cube state before this move (post-scramble + prior moves)
    target_move: Move         # the move actually taken
    history: tuple[Move, ...] # moves made so far (length = move_index)
    phase: Phase | None       # phase this move belongs to (None if past skeleton)
    raw_label: str | None     # author's exact label, if available
    method: Method            # overall method of the solve


def examples_from_segmented(segmented: SegmentedReconstruction) -> list[TrainingExample]:
    """Build per-move TrainingExamples for one segmented reconstruction."""
    rec = segmented.reconstruction
    flat = rec.solution.flat()

    # Map move index → (phase, raw_label) using segment cumulative counts.
    move_to_phase: dict[int, tuple[Phase, str]] = {}
    prev_cum = 0
    for seg in segmented.segments:
        for i in range(prev_cum, seg.cumulative_count):
            move_to_phase[i] = (seg.phase, seg.raw_label)
        prev_cum = seg.cumulative_count

    state = SOLVED.apply_alg(rec.scramble)
    examples: list[TrainingExample] = []
    for i, move in enumerate(flat):
        phase_label = move_to_phase.get(i)
        phase = phase_label[0] if phase_label else None
        raw_label = phase_label[1] if phase_label else None
        examples.append(
            TrainingExample(
                source_id=rec.source_id,
                move_index=i,
                state_before=state,
                target_move=move,
                history=tuple(flat[:i]),
                phase=phase,
                raw_label=raw_label,
                method=segmented.method,
            )
        )
        state = state.apply(move)
    return examples
