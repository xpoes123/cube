"""Transformer policy model for FMC next-move prediction.

Tokens (one stream per example):
  [CLS] [corner_0 .. corner_7] [edge_0 .. edge_11] [hist_{K-1} .. hist_0]

State piece tokens carry cubie identity + orientation as summed embeddings.
History tokens carry move identity + distance-from-current positional code,
padded with a sentinel for moves before the start.

Readout: project the CLS hidden state to 18 move logits.

Sized for ~60k training examples: small, no dropout-heavy, trains in seconds
per epoch on a 4060.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn

# Match training.encoding: 18 face-quarter moves.
N_MOVES = 18
# Sentinel index for "no move here" (padding before solve start).
PAD_MOVE = N_MOVES  # → vocab size = 19


@dataclass(frozen=True)
class ModelConfig:
    d_model: int = 96
    n_heads: int = 4
    n_layers: int = 3
    ffn_mult: int = 3
    dropout: float = 0.1
    history_len: int = 32


class PolicyTransformer(nn.Module):
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        self.cfg = cfg
        d = cfg.d_model

        # Per-token-kind position embedding (CLS, corner_0..7, edge_0..11, hist_0..K-1).
        n_state_tokens = 1 + 8 + 12  # cls + corners + edges
        self.n_state_tokens = n_state_tokens
        self.token_pos = nn.Embedding(n_state_tokens + cfg.history_len, d)

        # Content embeddings.
        self.cls = nn.Parameter(torch.zeros(d))
        self.cp_emb = nn.Embedding(8, d)         # corner permutation id
        self.co_emb = nn.Embedding(3, d)         # corner orientation
        self.ep_emb = nn.Embedding(12, d)        # edge permutation id
        self.eo_emb = nn.Embedding(2, d)         # UD-axis EO
        self.eo_fb_emb = nn.Embedding(2, d)      # FB-axis EO
        self.eo_rl_emb = nn.Embedding(2, d)      # RL-axis EO
        self.move_emb = nn.Embedding(N_MOVES + 1, d)  # +1 for PAD

        nn.init.normal_(self.cls, std=0.02)
        for emb in [
            self.token_pos, self.cp_emb, self.co_emb, self.ep_emb,
            self.eo_emb, self.eo_fb_emb, self.eo_rl_emb, self.move_emb,
        ]:
            nn.init.normal_(emb.weight, std=0.02)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d,
            nhead=cfg.n_heads,
            dim_feedforward=d * cfg.ffn_mult,
            dropout=cfg.dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=cfg.n_layers)
        self.norm = nn.LayerNorm(d)
        self.head = nn.Linear(d, N_MOVES)

    def forward(
        self,
        cp: torch.Tensor,       # (B, 8)  int64
        co: torch.Tensor,       # (B, 8)  int64
        ep: torch.Tensor,       # (B, 12) int64
        eo: torch.Tensor,       # (B, 12) int64
        eo_fb: torch.Tensor,    # (B, 12) int64
        eo_rl: torch.Tensor,    # (B, 12) int64
        history: torch.Tensor,  # (B, K)  int64, PAD_MOVE for missing
    ) -> torch.Tensor:
        b = cp.size(0)
        d = self.cfg.d_model
        device = cp.device

        # CLS token.
        cls_tok = self.cls.expand(b, 1, d)

        # Corner tokens.
        corner_tok = self.cp_emb(cp) + self.co_emb(co)        # (B, 8, d)
        # Edge tokens.
        edge_tok = (
            self.ep_emb(ep)
            + self.eo_emb(eo)
            + self.eo_fb_emb(eo_fb)
            + self.eo_rl_emb(eo_rl)
        )                                                      # (B, 12, d)
        # History tokens.
        hist_tok = self.move_emb(history)                      # (B, K, d)

        x = torch.cat([cls_tok, corner_tok, edge_tok, hist_tok], dim=1)  # (B, 1+8+12+K, d)

        # Add learned positional encoding shared across batch.
        positions = torch.arange(x.size(1), device=device)
        x = x + self.token_pos(positions)

        x = self.encoder(x)
        cls_out = self.norm(x[:, 0])
        return self.head(cls_out)  # (B, N_MOVES) logits


def count_params(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
