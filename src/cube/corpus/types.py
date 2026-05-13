"""Canonical reconstruction record shape, source-agnostic.

Every ingest source (cubesolv.es, reddit, speedsolving, FB) feeds raw text
into the parser and produces a `Reconstruction`. Downstream consumers
(validator, segmenter, training data builder) work only against this type.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from cube.engine.notation import NissAlg


@dataclass(frozen=True, slots=True)
class Reconstruction:
    scramble: list  # list[Move] — the scramble applied to SOLVED
    solution: NissAlg  # the solver's solution (may include NISS)
    source: str  # e.g. "cubesolv.es", "reddit", "speedsolving.com"
    source_id: str  # source-specific id (URL slug, post id, etc.)

    # Optional metadata — populated when available, never required.
    author: str | None = None
    date_solved: date | None = None
    competition: str | None = None  # WCA comp name if applicable
    commentary: str | None = None  # author's thought-process notes
    raw_text: str | None = None  # original raw form, for debugging
    tags: tuple[str, ...] = field(default_factory=tuple)

    @property
    def length(self) -> int:
        return len(self.solution.flat())
