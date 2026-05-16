"""Cube state → tensor inputs for the brain model.

Each cube state is encoded as 20 cubie tokens (8 corners + 12 edges).
Per token we feed three small ints:
    - slot index           (0..19) — which physical slot this token represents
    - cubie identity       (0..7 for corners, 0..11 for edges)
    - orientation          (0..2 for corners, 0..1 for edges)

The model's embedding layers combine these into a per-token vector;
the encoder mixes information across tokens via attention. The state
encoder here is pure data-shaping — no learnable parameters.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch

from cube.engine.state import State


# Slot index conventions matching cube.engine.state:
#   Corner slots 0..7 are URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB
#   Edge slots   0..11 are UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR
N_CORNER_SLOTS = 8
N_EDGE_SLOTS = 12
N_TOKENS = N_CORNER_SLOTS + N_EDGE_SLOTS


@dataclass(frozen=True, slots=True)
class StateTokens:
    """Per-token int features for one cube state.

    Shapes are (N_TOKENS,) — one row per slot. Concatenation order is
    corners (8) then edges (12).
    """

    slot_idx: torch.Tensor       # (20,) int64; identity 0..19
    cubie_idx: torch.Tensor      # (20,) int64; corner ids 0..7 in first 8 rows, edge ids 0..11 in next 12
    orientation: torch.Tensor    # (20,) int64; co 0..2 for corners (first 8 rows), eo 0..1 for edges (next 12)

    def to(self, device) -> "StateTokens":
        return StateTokens(
            slot_idx=self.slot_idx.to(device),
            cubie_idx=self.cubie_idx.to(device),
            orientation=self.orientation.to(device),
        )


def encode_state(state: State) -> StateTokens:
    """Encode a single State as (slot_idx, cubie_idx, orientation) tensors.

    Conventions:
    - Slot indices: 0..7 corners, 8..19 edges.
    - cubie_idx: which cubie is currently in each slot (state.cp / state.ep).
      The corner and edge cubie ID spaces are disjoint; we keep them
      separate via slot_idx so the model can disambiguate.
    - orientation: state.co (mod 3) for corners; state.eo (mod 2) for edges.
      We use the UD-axis EO array; non-UD-axis training requires rotating
      the state into canonical UD frame first (see canonical_axis.py).
    """
    slot_idx = torch.arange(N_TOKENS, dtype=torch.long)
    cubie_idx = torch.tensor(list(state.cp) + list(state.ep), dtype=torch.long)
    orientation = torch.tensor(list(state.co) + list(state.eo), dtype=torch.long)
    return StateTokens(slot_idx=slot_idx, cubie_idx=cubie_idx, orientation=orientation)


def encode_batch(states: list[State]) -> StateTokens:
    """Encode a list of States as a single batched StateTokens.

    Returned tensors have shape (B, N_TOKENS).
    """
    if not states:
        raise ValueError("encode_batch requires at least one state")
    per = [encode_state(s) for s in states]
    return StateTokens(
        slot_idx=torch.stack([p.slot_idx for p in per], dim=0),
        cubie_idx=torch.stack([p.cubie_idx for p in per], dim=0),
        orientation=torch.stack([p.orientation for p in per], dim=0),
    )
