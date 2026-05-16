"""Name the trigger family of a DR-completing move sequence.

The DR library returns a flat optimal move sequence. Champions verbalize
it as `<setup> + <named trigger>`. This module recognizes which trigger
family a sequence ends with (`R`, `R U2 R'`, `R U' R'`, etc.) and splits
the sequence accordingly so the agent can narrate "I'll apply this 2-move
setup then the R-U2-R' trigger" instead of dumping 8 moves at once.

Matching is shape-based: faces are renamed A, B, C... in order of first
appearance so `R U2 R'` and `L D2 L'` both match the shape `(A, B2, A')`.
"""

from __future__ import annotations

# Shape pattern -> human-readable name.
# Each shape is a tuple of move-strings normalized to abstract letters:
# the first new face becomes A, the second new face becomes B, etc.
# Turn modifiers ('', '2', "'") are preserved.
_TRIGGER_SHAPES: dict[tuple[str, ...], str] = {
    ("A",): "single (1-move trigger)",
    ("A2",): "single half-turn (1-move trigger)",
    ("A'",): "single inverse (1-move trigger)",
    ("A", "B2", "A'"): "X-U2-X' (DR-4c4e)",
    ("A'", "B2", "A"): "X'-U2-X (DR-4c4e mirror)",
    ("A", "B", "A'"): "X-U-X' (DR-3c2e)",
    ("A'", "B", "A"): "X'-U-X (DR-3c2e mirror)",
    ("A", "B'", "A'"): "X-U'-X' (DR-3c2e)",
    ("A'", "B'", "A"): "X'-U'-X (DR-3c2e mirror)",
    ("A", "B2", "C2", "A"): "X-U2-F2-X (DR-4c4e variant)",
    ("A", "B2", "C2", "A'"): "X-U2-F2-X' (DR-4c4e variant)",
    ("A", "B", "C"): "X-Y-Z (DR-7c8e setup)",
    ("A", "B"): "X-Y (2-move trigger)",
    ("A2", "B2"): "X2-Y2 (2-move half-turn trigger)",
}


def _shape(moves: list[str]) -> tuple[str, ...]:
    if not moves:
        return ()
    face_letter: dict[str, str] = {}
    out = []
    for m in moves:
        face = m[0]
        if face not in face_letter:
            face_letter[face] = chr(ord("A") + len(face_letter))
        letter = face_letter[face]
        suffix = m[1:]  # '', '2', or "'"
        out.append(f"{letter}{suffix}")
    return tuple(out)


def identify_trigger(moves: list[str]) -> tuple[list[str], list[str], str]:
    """Split a DR-completing sequence into (setup, trigger, trigger_name).

    Strategy: try matching the longest known trigger shape as a suffix.
    If nothing matches, treat the last 3 moves as an unnamed trigger
    (or the whole sequence if shorter than 3).
    """
    moves = list(moves)
    for k in (5, 4, 3, 2, 1):
        if len(moves) >= k:
            suffix_shape = _shape(moves[-k:])
            if suffix_shape in _TRIGGER_SHAPES:
                return (
                    moves[:-k],
                    moves[-k:],
                    _TRIGGER_SHAPES[suffix_shape],
                )
    if len(moves) <= 3:
        return [], moves, f"{len(moves)}-move trigger (unnamed)"
    return moves[:-3], moves[-3:], "3-move trigger (unnamed)"
