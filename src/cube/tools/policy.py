"""Policy tool: single-pass transformer query for "intuition" suggestions.

Wraps the trained policy model. The agent calls this to ask "what move
does a strong-solver-like prior recommend next?" — analogous to a human's
trained eye instantly suggesting candidates. Always a single forward pass,
no beam search.
"""

from __future__ import annotations

import math
from pathlib import Path

import torch
import torch.nn.functional as F

from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.training.encoding import decode_move, encode_move
from cube.training.model import PAD_MOVE, ModelConfig, PolicyTransformer

_MODEL: PolicyTransformer | None = None
_HISTORY_LEN: int = 32
_DEVICE: torch.device | None = None


def _load_model(ckpt_path: str = "checkpoints/policy_best.pt") -> None:
    """Lazy-load the policy model once per process."""
    global _MODEL, _HISTORY_LEN, _DEVICE
    if _MODEL is not None:
        return
    if not Path(ckpt_path).exists():
        raise FileNotFoundError(
            f"Policy checkpoint not found: {ckpt_path}. "
            f"Tools requiring the policy will fail until it exists."
        )
    _DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(ckpt_path, map_location=_DEVICE, weights_only=False)
    cfg = ModelConfig(**ckpt["model_cfg"])
    model = PolicyTransformer(cfg).to(_DEVICE)
    model.load_state_dict(ckpt["model"])
    model.eval()
    _MODEL = model
    _HISTORY_LEN = cfg.history_len


def policy_intuition(
    scramble: list[str], history: list[str], k: int = 8,
) -> dict:
    """Return the policy's top-k move suggestions at the current state.

    This is the agent's "human intuition" tool: one forward pass over the
    transformer trained on real WCA reconstructions. Use it when you want
    to know "what would a competition solver instinctively try here?"

    Returns:
      - `top_k`: list of {move, log_prob, prob} dicts, sorted by probability descending
      - `entropy`: distribution entropy in nats (higher = model is less sure)
    """
    _load_model()
    assert _MODEL is not None and _DEVICE is not None

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    # The model conditions on (state, recent history). For our purposes
    # the "history" the model sees is the full move-sequence-so-far on the
    # normal side: scramble + history, left-padded to history_len.
    full_history = parse_alg(" ".join(scramble + history)) if (scramble or history) else []
    recent = full_history[-_HISTORY_LEN:]

    device = _DEVICE
    cp = torch.tensor(state.cp, dtype=torch.long, device=device).unsqueeze(0)
    co = torch.tensor(state.co, dtype=torch.long, device=device).unsqueeze(0)
    ep = torch.tensor(state.ep, dtype=torch.long, device=device).unsqueeze(0)
    eo = torch.tensor(state.eo, dtype=torch.long, device=device).unsqueeze(0)
    eo_fb = torch.tensor(state.eo_fb, dtype=torch.long, device=device).unsqueeze(0)
    eo_rl = torch.tensor(state.eo_rl, dtype=torch.long, device=device).unsqueeze(0)
    hist = torch.full(
        (1, _HISTORY_LEN), PAD_MOVE, dtype=torch.long, device=device,
    )
    for j, m in enumerate(recent):
        hist[0, _HISTORY_LEN - len(recent) + j] = encode_move(m)

    with torch.no_grad():
        logits = _MODEL(
            cp=cp, co=co, ep=ep, eo=eo, eo_fb=eo_fb, eo_rl=eo_rl, history=hist,
        )
    log_probs = F.log_softmax(logits[0], dim=-1).cpu().tolist()

    indexed = sorted(enumerate(log_probs), key=lambda kv: -kv[1])
    top = []
    for idx, lp in indexed[:k]:
        move = decode_move(idx)
        top.append({
            "move": str(move),
            "log_prob": round(lp, 3),
            "prob": round(math.exp(lp), 4),
        })

    probs = [math.exp(lp) for lp in log_probs]
    entropy = -sum(p * lp for p, lp in zip(probs, log_probs) if p > 0)
    return {
        "top_k": top,
        "entropy": round(entropy, 3),
    }
