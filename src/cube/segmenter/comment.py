"""Parse author phase annotations from a reconstruction's comment field.

The 333.fm convention (modern FMC reconstructions) is:

    <moves>//<label> (<phase_count>/<cumulative_count>)

per line. The moves may contain NISS parens. Labels are free-form prose
("EO", "DR, 4a1", "M + S slice", "HTR + EP"). Lines that don't match
the pattern are prose and are skipped.

Example input (Wong's FMC2024 attempt 1):

    U F L R' U//EO (5/5)
    (B) F2 D2 L2 B//DR, 4a1 (5/10)
    (D2 R2 U2 B2 R)//HTR (5/15)
    (U2 F2 U2 L2)//M + S slice (4/19)

Output: 4 raw phase entries.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from cube.engine.notation import NissAlg, parse_niss

# Capture: moves (anything except '/'), label (anything except parens),
# phase count, cumulative count. Trailing prose on the same line is ignored.
_PHASE_LINE_RE = re.compile(
    r"^\s*(?P<moves>[^/]+?)\s*//\s*(?P<label>[^()]*?)\s*"
    r"\(\s*(?P<phase_count>\d+)\s*/\s*(?P<cumulative>\d+)\s*\)\s*$"
)


@dataclass(frozen=True, slots=True)
class RawPhase:
    """One author-annotated phase line, pre-segmenter."""

    raw_label: str
    moves: NissAlg
    author_phase_count: int
    author_cumulative: int


def parse_phase_comments(comment: str | None) -> list[RawPhase]:
    """Extract author-annotated phases from a comment. Empty list if none."""
    if not comment:
        return []
    out: list[RawPhase] = []
    for line in comment.splitlines():
        m = _PHASE_LINE_RE.match(line)
        if not m:
            continue
        moves_str = m.group("moves").strip()
        label = m.group("label").strip()
        try:
            moves = parse_niss(moves_str)
        except ValueError:
            # Malformed move sequence in this line; skip it.
            continue
        out.append(
            RawPhase(
                raw_label=label,
                moves=moves,
                author_phase_count=int(m.group("phase_count")),
                author_cumulative=int(m.group("cumulative")),
            )
        )
    return out
