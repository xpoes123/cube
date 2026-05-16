"""Agent-facing brain inference.

Loads a trained BrainStepModel from checkpoint, exposes `policy_suggest`
that takes a state + step and returns top-K (move, probability) pairs.
Replaces the legacy `tools/policy.py` for the FMC agent.

Usage at solve time:
    from cube.brain.infer import policy_suggest
    cands = policy_suggest(state, step="dr", k=5)
    # → [(move_str, prob), ...] sorted by prob desc.

Models are lazy-loaded from `checkpoints/brain_{step}.pt`. Missing
checkpoints fall back to None — callers should check and decide
whether to use the legacy policy.
"""

from __future__ import annotations

import functools
from pathlib import Path

import torch
import torch.nn.functional as F

from cube.brain.model import BrainStepModel, BrainConfig, STEP_ALPHABETS
from cube.brain.state_encoder import encode_state
from cube.engine.state import State


_CKPT_DIR = Path("checkpoints")


@functools.lru_cache(maxsize=8)
def _load_model(step: str, device: str = "cpu") -> BrainStepModel | None:
    """Load a trained model from checkpoint. Returns None if not present."""
    if step not in STEP_ALPHABETS:
        return None
    ckpt_path = _CKPT_DIR / f"brain_{step}.pt"
    if not ckpt_path.exists():
        return None
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = BrainConfig(**ckpt["config"]) if isinstance(ckpt.get("config"), dict) else BrainConfig()
    model = BrainStepModel(step=step, cfg=cfg)
    model.load_state_dict(ckpt["state_dict"])
    model.to(device)
    model.eval()
    return model


def is_brain_available(step: str) -> bool:
    """Quick check without loading: does a trained checkpoint exist?"""
    return (_CKPT_DIR / f"brain_{step}.pt").exists() and step in STEP_ALPHABETS


def policy_suggest(
    state: State,
    step: str,
    *,
    k: int = 5,
    device: str = "cpu",
) -> list[tuple[str, float]]:
    """Top-K move suggestions for the given state + step.

    Returns a list of (move, probability) sorted by probability descending.
    Probabilities are softmax-normalized over the step's legal-move alphabet.
    Returns [] if no model is loaded for this step.
    """
    model = _load_model(step, device=device)
    if model is None:
        return []
    tok = encode_state(state).to(device)
    # Add batch dim
    slot_idx = tok.slot_idx.unsqueeze(0)
    cubie_idx = tok.cubie_idx.unsqueeze(0)
    orientation = tok.orientation.unsqueeze(0)
    with torch.no_grad():
        logits = model(slot_idx, cubie_idx, orientation).squeeze(0)
        probs = F.softmax(logits, dim=-1)
    alphabet = STEP_ALPHABETS[step]
    top_k_idx = torch.topk(probs, min(k, len(alphabet))).indices.tolist()
    return [(alphabet[i], float(probs[i])) for i in top_k_idx]


def full_distribution(
    state: State,
    step: str,
    *,
    device: str = "cpu",
) -> dict[str, float]:
    """Return the full softmax distribution over the step's alphabet."""
    model = _load_model(step, device=device)
    if model is None:
        return {}
    tok = encode_state(state).to(device)
    with torch.no_grad():
        logits = model(
            tok.slot_idx.unsqueeze(0),
            tok.cubie_idx.unsqueeze(0),
            tok.orientation.unsqueeze(0),
        ).squeeze(0)
        probs = F.softmax(logits, dim=-1)
    return {move: float(probs[i]) for i, move in enumerate(STEP_ALPHABETS[step])}
