from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class Face(IntEnum):
    U = 0
    D = 1
    R = 2
    L = 3
    F = 4
    B = 5


class Turn(IntEnum):
    CW = 1
    HALF = 2
    CCW = 3


_FACE_CHAR = {Face.U: "U", Face.D: "D", Face.R: "R", Face.L: "L", Face.F: "F", Face.B: "B"}
_TURN_SUFFIX = {Turn.CW: "", Turn.HALF: "2", Turn.CCW: "'"}


@dataclass(frozen=True, slots=True, order=True)
class Move:
    face: Face
    turn: Turn

    def inverse(self) -> Move:
        return Move(self.face, Turn(4 - self.turn))

    def __str__(self) -> str:
        return _FACE_CHAR[self.face] + _TURN_SUFFIX[self.turn]


ALL_MOVES: tuple[Move, ...] = tuple(Move(f, t) for f in Face for t in Turn)
