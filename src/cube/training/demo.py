"""Inference demo: load a trained policy and play moves on a scramble.

Usage:
    uv run python -m cube.training.demo \\
        --scramble "R U R' U' R' F R F'" \\
        --rollout 30

Shows top-5 next moves with probabilities at each step. With --rollout N,
greedily plays N moves and prints the cube's solved-ness at the end.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
import torch.nn.functional as F

from cube.engine.moves import Move
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State
from cube.training.encoding import decode_move, encode_move
from cube.training.model import PAD_MOVE, ModelConfig, PolicyTransformer


def _state_to_batch(state: State, history: list[Move], history_len: int, device: torch.device):
    """Encode a single (state, history) into model-input tensors of batch size 1."""
    def t(values, dtype=torch.long):
        return torch.tensor(values, dtype=dtype, device=device).unsqueeze(0)

    recent = history[-history_len:]
    pad_n = history_len - len(recent)
    hist_ids = [PAD_MOVE] * pad_n + [encode_move(m) for m in recent]
    return {
        "cp": t(state.cp),
        "co": t(state.co),
        "ep": t(state.ep),
        "eo": t(state.eo),
        "eo_fb": t(state.eo_fb),
        "eo_rl": t(state.eo_rl),
        "history": t(hist_ids),
    }


def _format_distance(state: State) -> str:
    """A cheap 'how solved is this' signal — count of correctly placed pieces."""
    correct_cp = sum(1 for i, v in enumerate(state.cp) if v == i)
    correct_co = sum(1 for v in state.co if v == 0)
    correct_ep = sum(1 for i, v in enumerate(state.ep) if v == i)
    correct_eo = sum(1 for v in state.eo if v == 0)
    return f"cp={correct_cp}/8 co={correct_co}/8 ep={correct_ep}/12 eo={correct_eo}/12"


def run_demo(
    ckpt_path: str,
    scramble_str: str,
    rollout: int,
    topk: int = 5,
    device: str = "cuda",
) -> None:
    dev = torch.device(device if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(ckpt_path, map_location=dev, weights_only=False)
    model_cfg_dict = ckpt["model_cfg"]
    model = PolicyTransformer(ModelConfig(**model_cfg_dict)).to(dev)
    model.load_state_dict(ckpt["model"])
    model.eval()

    print(f"loaded {ckpt_path}")
    print(f"  val: top1={ckpt['val']['top1']:.4f} top5={ckpt['val']['top5']:.4f} "
          f"(epoch {ckpt['epoch']})")
    print(f"  history_len={model_cfg_dict['history_len']}")
    print()

    scramble = parse_alg(scramble_str)
    state = SOLVED.apply_alg(scramble)
    history: list[Move] = []

    print(f"scramble: {scramble_str}")
    print(f"  after scramble: {_format_distance(state)}")
    print()

    print(f"top-{topk} predictions at each step:")
    for step in range(rollout):
        batch = _state_to_batch(state, history, model_cfg_dict["history_len"], dev)
        with torch.no_grad():
            logits = model(**batch).squeeze(0)
        probs = F.softmax(logits, dim=-1)
        top = probs.topk(topk)

        line_top = "  ".join(
            f"{decode_move(int(idx)).__str__():>3}({float(p):.2f})"
            for p, idx in zip(top.values, top.indices, strict=True)
        )
        chosen = decode_move(int(top.indices[0]))
        print(f"  step {step + 1:>2}: {chosen}  |  top-{topk}: {line_top}")

        state = state.apply(chosen)
        history.append(chosen)
        if state.is_solved():
            print(f"  SOLVED in {step + 1} moves.")
            break

    print()
    print(f"final state: {_format_distance(state)}")
    print(f"final history: {' '.join(str(m) for m in history)}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default="checkpoints/policy_best.pt")
    p.add_argument(
        "--scramble",
        default="R' U' F D2 L2 B U2 B' U2 R2 F D2 R2 F D U' R' B' U' R F U2 R' U' F",
        help="WCA-notation scramble (default is a real TNoodle-style FMC scramble).",
    )
    p.add_argument("--rollout", type=int, default=25)
    p.add_argument("--topk", type=int, default=5)
    p.add_argument("--device", default="cuda")
    args = p.parse_args()

    if not Path(args.ckpt).exists():
        raise SystemExit(f"checkpoint not found: {args.ckpt}")
    run_demo(args.ckpt, args.scramble, args.rollout, args.topk, args.device)


if __name__ == "__main__":
    main()
