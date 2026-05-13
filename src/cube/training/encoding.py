"""Convert cube states and moves to numerical encodings for ML models.

Two encodings provided:
- `encode_state_flat`: one-hot concat, suitable for MLP input.
- `encode_state_indices`: index arrays, suitable for embedding layers.

Move encoding is a single int in [0, 18). Move index = face * 3 + (turn - 1).

Architecture choice (transformer vs MLP vs GNN) is deferred — these encoders
are the boundary between model-agnostic TrainingExample and model-specific
tensors.
"""

from __future__ import annotations

from cube.engine.moves import Face, Move, Turn
from cube.engine.state import State

# Move encoding: 18 face-quarter moves.
N_MOVES = 18


def encode_move(move: Move) -> int:
    """Encode Move as index in [0, 18). face * 3 + (turn - 1)."""
    return int(move.face) * 3 + (int(move.turn) - 1)


def decode_move(idx: int) -> Move:
    """Inverse of encode_move."""
    face = Face(idx // 3)
    turn = Turn(idx % 3 + 1)
    return Move(face, turn)


# State encoding sizes for one-hot flat representation.
# Layout (concatenated, in this order):
#   cp:    8 positions × 8 corner types = 64
#   co:    8 positions × 3 orientations = 24
#   ep:   12 positions × 12 edge types  = 144
#   eo:   12 bits (UD-axis EO)          = 12
#   eo_fb:12 bits (FB-axis EO)          = 12
#   eo_rl:12 bits (RL-axis EO)          = 12
# Total: 268
STATE_FLAT_SIZE = 8 * 8 + 8 * 3 + 12 * 12 + 12 + 12 + 12  # = 268


def encode_state_flat(state: State) -> list[int]:
    """One-hot concat encoding of a state. Returns list of length STATE_FLAT_SIZE.

    Use this for MLP-style models. For embedding-based models, prefer
    `encode_state_indices` which avoids the one-hot blowup.
    """
    out: list[int] = []
    # cp: 8 × 8
    for cubie in state.cp:
        block = [0] * 8
        block[cubie] = 1
        out.extend(block)
    # co: 8 × 3
    for orient in state.co:
        block = [0] * 3
        block[orient] = 1
        out.extend(block)
    # ep: 12 × 12
    for cubie in state.ep:
        block = [0] * 12
        block[cubie] = 1
        out.extend(block)
    # eo (UD), eo_fb, eo_rl: 12 bits each
    out.extend(state.eo)
    out.extend(state.eo_fb)
    out.extend(state.eo_rl)
    return out


def encode_state_indices(state: State) -> dict[str, tuple[int, ...]]:
    """Encode a state as index arrays. Use with embedding layers.

    Returns a dict mapping feature name to tuple of indices. All values are
    plain Python ints (not numpy) — the caller decides framework conversion.
    """
    return {
        "cp": state.cp,
        "co": state.co,
        "ep": state.ep,
        "eo": state.eo,
        "eo_fb": state.eo_fb,
        "eo_rl": state.eo_rl,
    }


def encode_history(history: tuple[Move, ...]) -> tuple[int, ...]:
    """Encode a move sequence as a tuple of move indices."""
    return tuple(encode_move(m) for m in history)
