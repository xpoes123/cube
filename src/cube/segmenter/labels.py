"""Map free-form author labels to canonical Phase values.

Authors write things like "EO", "DR, 4a1", "DR + 2c2", "M + S slice", "HTR",
"Insertion", "2x2x2", "F2L-1". This module normalizes them.

Strategy: lowercase, strip, then check substring patterns in priority order.
Priority matters: "DR finish" should be DR not FINISH; "EO + 1c" should be EO.
"""

from __future__ import annotations

import re

from cube.segmenter.types import Phase

# Patterns checked in order — first match wins.
_LABEL_PATTERNS: list[tuple[re.Pattern, Phase]] = [
    (re.compile(r"^eoline\b|^eo[\s\-]?line\b"), Phase.EOLINE),
    (re.compile(r"^eo\b|^edge[\s\-]?orient"), Phase.EO),
    (re.compile(r"^htr\b|half[\s\-]?turn"), Phase.HTR),
    # DR catches "DR", "DR+", "DR-", "DR finish", "domino"
    (re.compile(r"^dr\b|^domino"), Phase.DR),
    (re.compile(r"\binsert(ion)?\b|^insert\b"), Phase.INSERTION),
    (re.compile(r"^skeleton\b"), Phase.SKELETON),
    (re.compile(r"\bslice\b"), Phase.SLICE),
    (re.compile(r"^(finish|leave|last|all done|solve)\b"), Phase.FINISH),
    # Blocks: 2x2x2, 2x2x3, F2L (with optional minus-slot), 222, 223
    (re.compile(r"\b(2x2x2|2x2x3|222|223|f2l|block|pair)\b"), Phase.BLOCK),
]


def canonicalize(label: str) -> Phase:
    """Map a raw author phase label to a canonical Phase.

    Returns Phase.UNKNOWN if no pattern matches. Always preserve the raw label
    elsewhere — this function is lossy.
    """
    s = label.strip().lower()
    if not s:
        return Phase.UNKNOWN
    for pat, phase in _LABEL_PATTERNS:
        if pat.search(s):
            return phase
    return Phase.UNKNOWN
