"""Brain model: small transformer over 20 cubie tokens.

One instance per step (eo / dr / htr / finish). Each step has its own
output-head dimension matching the step's legal-move alphabet (after
canonical-axis collapse to UD).

Architecture:
  20 cubie tokens → 3-token embedding sum (slot + cubie + orient)
  → 2 transformer encoder layers (d_model=64, 4 heads)
  → mean-pool over tokens
  → step-specific linear head over the step's move alphabet

Params per step model: ~50-100k. Four models total: ~200-400k.
Training data: per-step (state, optimal-move-distribution) from nissy.
Loss: KL divergence vs the soft target.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


# Legal-move alphabets per step (canonical UD-axis frame).
# Order matters: defines the index → move mapping for the output head.
#
# EO model: all 18 face moves. The model picks ANY move that helps EO;
# no a-priori filtering.
ALPHABET_EO: tuple[str, ...] = (
    "U", "U'", "U2", "D", "D'", "D2",
    "R", "R'", "R2", "L", "L'", "L2",
    "F", "F'", "F2", "B", "B'", "B2",
)

# DR model: 14 moves EO-preserving on UD axis (no F/B quarter turns; F2/B2 OK).
ALPHABET_DR: tuple[str, ...] = (
    "U", "U'", "U2", "D", "D'", "D2",
    "R", "R'", "R2", "L", "L'", "L2",
    "F2", "B2",
)

# HTR model: 10 moves DR-preserving on UD axis.
# (DR-on-UD-corner-subgroup is preserved by U, D quarter turns + all half-turns.)
ALPHABET_HTR: tuple[str, ...] = (
    "U", "U'", "U2", "D", "D'", "D2",
    "R2", "L2", "F2", "B2",
)

# Finish model: 6 moves (half-turns only).
ALPHABET_FINISH: tuple[str, ...] = ("U2", "D2", "R2", "L2", "F2", "B2")

STEP_ALPHABETS = {
    "eo": ALPHABET_EO,
    "dr": ALPHABET_DR,
    "htr": ALPHABET_HTR,
    "finish": ALPHABET_FINISH,
}


@dataclass(frozen=True)
class BrainConfig:
    """Per-step model config. Small by design — these are cheap to train."""
    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    ffn_mult: int = 3
    dropout: float = 0.1


N_CORNER_SLOTS = 8
N_EDGE_SLOTS = 12
N_TOKENS = N_CORNER_SLOTS + N_EDGE_SLOTS

# Embedding vocab sizes
N_SLOTS = N_TOKENS  # 20 distinct slot identities
N_CUBIES = max(N_CORNER_SLOTS, N_EDGE_SLOTS)  # 12 — disambiguated by slot
N_ORIENT = 3  # max(corner orient = 3, edge orient = 2)


class BrainStepModel(nn.Module):
    """Single-step state-conditioned move predictor.

    Inputs are int64 tensors of shape (B, 20):
      slot_idx     — 0..19, identifies which slot the token represents
      cubie_idx    — which cubie ID is currently in that slot
      orientation  — 0..2 (corners) or 0..1 (edges)

    Output: (B, |alphabet|) logits over the step's legal moves.
    """

    def __init__(self, step: str, cfg: BrainConfig | None = None) -> None:
        super().__init__()
        if step not in STEP_ALPHABETS:
            raise ValueError(f"unknown step {step!r}; expected one of {sorted(STEP_ALPHABETS)}")
        self.step = step
        self.alphabet = STEP_ALPHABETS[step]
        self.cfg = cfg or BrainConfig()
        d = self.cfg.d_model

        # Embedding tables. Sum of (slot, cubie, orient) embeddings per token.
        self.slot_emb = nn.Embedding(N_SLOTS, d)
        self.cubie_emb = nn.Embedding(N_CUBIES, d)
        self.orient_emb = nn.Embedding(N_ORIENT, d)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d,
            nhead=self.cfg.n_heads,
            dim_feedforward=d * self.cfg.ffn_mult,
            dropout=self.cfg.dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=self.cfg.n_layers)
        self.norm = nn.LayerNorm(d)
        self.head = nn.Linear(d, len(self.alphabet))

        for emb in (self.slot_emb, self.cubie_emb, self.orient_emb):
            nn.init.normal_(emb.weight, std=0.02)

    def forward(
        self,
        slot_idx: torch.Tensor,    # (B, 20) int64
        cubie_idx: torch.Tensor,   # (B, 20) int64
        orientation: torch.Tensor, # (B, 20) int64
    ) -> torch.Tensor:
        """Returns (B, |alphabet|) move logits."""
        x = (
            self.slot_emb(slot_idx)
            + self.cubie_emb(cubie_idx)
            + self.orient_emb(orientation)
        )
        x = self.encoder(x)
        x = self.norm(x)
        x = x.mean(dim=1)  # mean-pool over 20 tokens → (B, d_model)
        return self.head(x)

    def param_count(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
