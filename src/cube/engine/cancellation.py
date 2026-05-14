"""Local move-sequence cancellation.

When concatenating stage outputs (EO + DR + HTR + Finish), adjacent moves
on the same face can often combine or cancel. This module applies those
local rules.

Rules:
- Same face, both turns sum to identity (e.g., U + U', U2 + U2, etc.) →
  remove both.
- Same face, turns combine to a single non-identity turn
  (e.g., U + U → U2, U2 + U' → U) → replace pair with the combined move.
- We also handle the "same-axis pair" case: U and D commute. If we see
  `U Dx U` we can move things around to combine the U's: `Dx U U = Dx U2`.
  This is a one-shot lookahead — we look for the nearest same-face move
  through any commuting moves and combine if possible.
"""

from __future__ import annotations

from collections.abc import Sequence

from cube.engine.moves import Face, Move, Turn

# Faces that commute with each other (opposite faces on the same axis).
_COMMUTING_AXIS: dict[Face, Face] = {
    Face.U: Face.D, Face.D: Face.U,
    Face.R: Face.L, Face.L: Face.R,
    Face.F: Face.B, Face.B: Face.F,
}


def _combine(m1: Move, m2: Move) -> Move | None:
    """Combine two same-face moves. Returns None if they cancel to identity."""
    assert m1.face == m2.face
    total = (int(m1.turn) + int(m2.turn)) % 4
    if total == 0:
        return None
    return Move(m1.face, Turn(total))


def cancel_moves(moves: Sequence[Move]) -> list[Move]:
    """Apply local cancellation rules to a move sequence.

    Two passes:
      1. Combine adjacent same-face moves (direct cancellation).
      2. Combine same-face moves separated only by opposite-face commuting
         moves (e.g., `U D U` → `D U2`).
    """
    # Pass 1: direct adjacent same-face combination.
    result = _combine_adjacent(list(moves))
    # Pass 2: through-commute combination. Repeat until stable.
    while True:
        new_result = _combine_through_commute(result)
        if new_result == result:
            break
        result = _combine_adjacent(new_result)
    return result


def _combine_adjacent(moves: list[Move]) -> list[Move]:
    out: list[Move] = []
    for m in moves:
        if out and out[-1].face == m.face:
            combined = _combine(out[-1], m)
            if combined is None:
                out.pop()
            else:
                out[-1] = combined
        else:
            out.append(m)
    return out


def _combine_through_commute(moves: list[Move]) -> list[Move]:
    """If moves[i] and moves[i+2] are same face AND moves[i+1] is on the
    opposite (commuting) face, swap and combine: `A B A → B AA`."""
    out: list[Move] = list(moves)
    i = 0
    while i + 2 < len(out):
        a, b, c = out[i], out[i + 1], out[i + 2]
        if (
            a.face == c.face
            and b.face == _COMMUTING_AXIS.get(a.face)
        ):
            combined = _combine(a, c)
            if combined is None:
                # a and c cancel; result is just b.
                out = out[:i] + [b] + out[i + 3:]
            else:
                out = out[:i] + [b, combined] + out[i + 3:]
        i += 1
    return out
