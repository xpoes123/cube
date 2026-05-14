"""Load JSONL corpus records and yield TrainingExamples.

Operates directly on JSONL (without rehydrating SegmentedReconstruction)
since the JSONL is the canonical training input — what's on disk is what
the model trains on. Reconstructing the segmented object would be redundant.
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.engine.symmetry import mirror_lr_alg
from cube.segmenter.types import Method, Phase
from cube.training.dataset import TrainingExample


def iter_records_from_jsonl(path: str | Path) -> Iterator[dict[str, Any]]:
    """Yield raw JSONL records one at a time. Skips blank lines."""
    p = Path(path)
    with p.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def record_to_examples(
    record: dict[str, Any],
    mirror_lr: bool = False,
) -> list[TrainingExample]:
    """Convert a single JSONL record into per-move TrainingExamples.

    Walks the flat solution (`normal + invert(inverse)`), attaches phase
    labels from the record's `phases` list (using cumulative_count ranges).

    When `mirror_lr=True`, the scramble and solution are reflected across
    the U-D-F-B plane before walking — yields the LR-mirror solve. Phase
    labels and counts are preserved (mirroring doesn't change the EO/DR/
    HTR/block enum or its move index). source_id gets "_M" appended so
    callers can tell mirrored examples apart.
    """
    scramble = parse_alg(record["scramble"])
    normal = parse_alg(record["solution_normal"])
    inverse = parse_alg(record["solution_inverse"])

    # Flatten: normal + invert(inverse).
    from cube.engine.notation import invert
    flat = normal + invert(inverse)

    if mirror_lr:
        scramble = mirror_lr_alg(scramble)
        flat = mirror_lr_alg(flat)
    source_id = record["source_id"] + ("_M" if mirror_lr else "")

    # Phase lookup by move index.
    move_to_phase: dict[int, tuple[Phase, str]] = {}
    for phase_dict in record.get("phases", []):
        cum = phase_dict["cumulative_count"]
        phase_count = phase_dict["phase_move_count"]
        start = cum - phase_count
        try:
            phase_enum = Phase(phase_dict["phase"])
        except ValueError:
            phase_enum = Phase.UNKNOWN
        for i in range(start, cum):
            move_to_phase[i] = (phase_enum, phase_dict.get("raw_label", "") or "")

    try:
        method_enum = Method(record["method"])
    except (KeyError, ValueError):
        method_enum = Method.UNKNOWN

    state = SOLVED.apply_alg(scramble)
    examples: list[TrainingExample] = []
    for i, move in enumerate(flat):
        phase_label = move_to_phase.get(i)
        phase = phase_label[0] if phase_label else None
        raw_label = phase_label[1] if phase_label else None
        examples.append(
            TrainingExample(
                source_id=source_id,
                move_index=i,
                state_before=state,
                target_move=move,
                history=tuple(flat[:i]),
                phase=phase,
                raw_label=raw_label,
                method=method_enum,
            )
        )
        state = state.apply(move)
    return examples


def iter_examples_from_jsonl(path: str | Path) -> Iterator[TrainingExample]:
    """Convenience: stream TrainingExamples across an entire JSONL corpus."""
    for record in iter_records_from_jsonl(path):
        yield from record_to_examples(record)
