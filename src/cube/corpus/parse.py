"""Parse raw reconstruction text into a Reconstruction record.

Reconstructions in the wild look roughly like:

    Scramble: R' U' F D2 R2 U L2 ...
    Solution: R U R' U (D F) R2 // EO + DR setup
              ...
    Final: 24 moves

Inputs vary by source. The parser is permissive: it scans for a scramble
line and a solution block, parses the solution via NISS notation, and stores
the rest as raw_text. Source adapters are responsible for extracting the
scramble/solution strings cleanly; this function does the cube-aware bits.
"""

from __future__ import annotations

import re

from cube.corpus.types import Reconstruction
from cube.engine.notation import parse_alg, parse_niss

_SCRAMBLE_RE = re.compile(r"(?:scramble|scr)\s*[:\-]\s*(.+)", re.IGNORECASE)
_SOLUTION_RE = re.compile(r"(?:solution|sol|reconstruction)\s*[:\-]\s*(.+)", re.IGNORECASE)
# Strip trailing "// comment" or "(NN moves)" style annotations from a single move-line.
_LINE_COMMENT_RE = re.compile(r"//.*$|#.*$")


def parse_reconstruction(
    raw_text: str,
    *,
    source: str,
    source_id: str,
    **metadata,
) -> Reconstruction:
    """Parse one reconstruction from raw text. Raises ValueError if essential
    fields (scramble, solution) cannot be recovered."""
    scramble_str = _find_field(raw_text, _SCRAMBLE_RE)
    if scramble_str is None:
        raise ValueError("no scramble line found")

    solution_str = _find_solution_block(raw_text)
    if not solution_str:
        raise ValueError("no solution found")

    scramble = parse_alg(_strip_comments(scramble_str))
    solution = parse_niss(_strip_comments(solution_str))

    return Reconstruction(
        scramble=scramble,
        solution=solution,
        source=source,
        source_id=source_id,
        raw_text=raw_text,
        **metadata,
    )


def _find_field(text: str, pattern: re.Pattern) -> str | None:
    for line in text.splitlines():
        m = pattern.search(line)
        if m:
            return m.group(1).strip()
    return None


def _find_solution_block(text: str) -> str:
    """Solution may span multiple lines. Capture from 'Solution:' until a blank
    line or 'Final:' / '=' summary line."""
    lines = text.splitlines()
    collected: list[str] = []
    capturing = False
    for line in lines:
        m = _SOLUTION_RE.search(line)
        if m:
            capturing = True
            tail = m.group(1).strip()
            if tail:
                collected.append(tail)
            continue
        if capturing:
            stripped = line.strip()
            if not stripped:
                break
            # Stop at summary/result lines.
            if re.match(r"^(final|total|result|=|--)", stripped, re.IGNORECASE):
                break
            collected.append(stripped)
    return " ".join(_strip_comments(line) for line in collected).strip()


def _strip_comments(s: str) -> str:
    return _LINE_COMMENT_RE.sub("", s).strip()
