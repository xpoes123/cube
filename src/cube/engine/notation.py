"""WCA-style notation parser and formatter for 3x3 algorithms.

Accepts: U U' U2 R R' R2 ... and the lowercase / wide-prime forms (e.g. U'2
is normalized to U2'). Whitespace between moves is required or implied by
single-letter face tokens. Parens, dots, and commas are ignored (comments
in cubesolv.es-style reconstructions often use them).

NISS notation (Normal-Inverse Scramble Switch): parentheses around a
sub-algorithm indicate moves applied to the inverse scramble. Parse via
`parse_niss` which returns a NissAlg with separate normal and inverse
parts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from cube.engine.moves import Face, Move, Turn

_FACE_LOOKUP = {"U": Face.U, "D": Face.D, "R": Face.R, "L": Face.L, "F": Face.F, "B": Face.B}
_TOKEN_RE = re.compile(r"([UDRLFB])([2']?'?2?)")


def parse_alg(s: str) -> list[Move]:
    """Parse a flat algorithm (no NISS parens). Raises ValueError on bad input."""
    # Strip ignorable characters: commas, periods, slashes, single-quote-doubled comments.
    cleaned = re.sub(r"[.,/]", " ", s)
    tokens = _TOKEN_RE.findall(cleaned)
    # Detect characters that weren't consumed (besides whitespace) to surface errors.
    consumed = "".join(f + t for f, t in tokens)
    leftover = re.sub(r"\s+", "", cleaned).replace(consumed, "", 1)
    if leftover.strip():
        raise ValueError(f"unparseable tokens in alg: {leftover!r}")

    moves: list[Move] = []
    for face_char, suffix in tokens:
        face = _FACE_LOOKUP[face_char]
        turn = _parse_turn_suffix(suffix)
        moves.append(Move(face, turn))
    return moves


def _parse_turn_suffix(suffix: str) -> Turn:
    # Normalize: "" -> CW, "2" -> HALF, "'" -> CCW, "2'" / "'2" -> CCW (180 of inverse = 180, but
    # by convention '2 == 2 == HALF since rotation by 180 is self-inverse).
    s = suffix.replace("'2", "2'").replace("2'", "2'")
    if s == "":
        return Turn.CW
    if s == "2" or s == "2'":
        return Turn.HALF
    if s == "'":
        return Turn.CCW
    raise ValueError(f"bad turn suffix: {suffix!r}")


def format_alg(moves: list[Move]) -> str:
    return " ".join(str(m) for m in moves)


def invert(alg: list[Move]) -> list[Move]:
    return [m.inverse() for m in reversed(alg)]


# Alias — `invert_alg` reads better at NISS callsites where `invert` (the
# bare verb) can be ambiguous with `Move.inverse()`.
invert_alg = invert


# ---------- NISS support ----------


@dataclass(frozen=True, slots=True)
class NissAlg:
    """Algorithm with normal and inverse parts.

    The full move sequence applied to a scramble S is:
        S * normal      (apply to scramble normally)
        S' * inverse    (equivalent: apply inverse moves to inverse scramble)
    Equivalent flat algorithm (applied to scramble): normal + invert(inverse).
    """

    normal: list[Move]
    inverse: list[Move]

    def flat(self) -> list[Move]:
        return list(self.normal) + invert(self.inverse)


_NISS_PAREN_RE = re.compile(r"\(([^()]*)\)")


def parse_niss(s: str) -> NissAlg:
    """Parse a NISS-style algorithm.

    Tokens in parentheses are interpreted as moves applied on the inverse
    scramble; tokens outside parens are normal moves. Reconstructions on
    cubesolv.es commonly use multiple paren groups interleaved — they all
    concatenate into the inverse list in the order they appear.
    """
    normal_parts: list[str] = []
    inverse_parts: list[str] = []
    pos = 0
    for m in _NISS_PAREN_RE.finditer(s):
        normal_parts.append(s[pos : m.start()])
        inverse_parts.append(m.group(1))
        pos = m.end()
    normal_parts.append(s[pos:])

    normal = parse_alg(" ".join(normal_parts))
    inverse = parse_alg(" ".join(inverse_parts)) if inverse_parts else []
    return NissAlg(normal=normal, inverse=inverse)
