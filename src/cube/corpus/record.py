"""Serialize Reconstruction + SegmentedReconstruction to JSONL records.

Stored fields are strings (move sequences) and primitives — no cubie state.
The engine can rehydrate state by re-applying the scramble/solution on demand.
We keep both author labels and canonical phases so the record is self-describing.
"""

from __future__ import annotations

import json
from typing import Any

from cube.corpus.types import Reconstruction
from cube.engine.notation import format_alg
from cube.segmenter.types import SegmentedReconstruction


def reconstruction_to_dict(rec: Reconstruction) -> dict[str, Any]:
    return {
        "source": rec.source,
        "source_id": rec.source_id,
        "author": rec.author,
        "competition": rec.competition,
        "date_solved": rec.date_solved.isoformat() if rec.date_solved else None,
        "scramble": format_alg(rec.scramble),
        "solution_normal": format_alg(rec.solution.normal),
        "solution_inverse": format_alg(rec.solution.inverse),
        "length": rec.length,
        "commentary": rec.commentary,
    }


def segmented_to_dict(seg: SegmentedReconstruction) -> dict[str, Any]:
    base = reconstruction_to_dict(seg.reconstruction)
    base["method"] = seg.method.value
    base["segment_source"] = seg.source
    base["issues"] = list(seg.issues)
    base["phases"] = [
        {
            "phase": s.phase.value,
            "raw_label": s.raw_label,
            "moves_normal": format_alg(s.moves.normal),
            "moves_inverse": format_alg(s.moves.inverse),
            "phase_move_count": s.phase_move_count,
            "cumulative_count": s.cumulative_count,
            "author_phase_count": s.author_phase_count,
            "author_cumulative": s.author_cumulative,
        }
        for s in seg.segments
    ]
    return base


def write_jsonl(records: list[dict[str, Any]], path: str) -> None:
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
