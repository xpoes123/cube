"""CLI: produce a human-style skeleton (scramble -> EO -> DR) from a scramble.

Example:
    uv run python -m cube.analyzer.skeleton_cli \\
        "R' U' F D2 L2 B U2 B' U2 R2 F D2 R2 F D U' R' B' U' R F U2 R' U' F"

Output is the skeleton broken down by phase. Each phase's moves are
verified by the cube engine to actually reach the target state (EO solved
on the chosen axis, then DR).
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import torch

from cube.analyzer.skeleton import find_skeleton, format_skeleton
from cube.engine.notation import parse_alg
from cube.training.model import ModelConfig, PolicyTransformer


def _load_model(ckpt_path: str, device: torch.device) -> tuple[PolicyTransformer, dict]:
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ModelConfig(**ckpt["model_cfg"])
    model = PolicyTransformer(cfg).to(device)
    model.load_state_dict(ckpt["model"])
    model.eval()
    return model, ckpt


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("scramble", help="WCA-notation scramble.")
    p.add_argument("--ckpt", default="checkpoints/policy_best.pt")
    p.add_argument("--eo-beam", type=int, default=256)
    p.add_argument("--eo-depth", type=int, default=10)
    p.add_argument("--dr-beam", type=int, default=8192)
    p.add_argument("--dr-depth", type=int, default=14)
    p.add_argument("--device", default="cuda")
    args = p.parse_args()

    if not Path(args.ckpt).exists():
        raise SystemExit(f"checkpoint not found: {args.ckpt}")

    dev = torch.device(args.device if torch.cuda.is_available() else "cpu")
    model, ckpt = _load_model(args.ckpt, dev)
    history_len = ckpt["model_cfg"]["history_len"]
    print(f"loaded {args.ckpt}")
    print(f"  val: top1={ckpt['val']['top1']:.4f} top5={ckpt['val']['top5']:.4f} "
          f"(epoch {ckpt['epoch']})")
    print()

    scramble = parse_alg(args.scramble)

    t0 = time.time()
    skeleton = find_skeleton(
        model,
        scramble,
        history_len=history_len,
        device=dev,
        eo_beam_width=args.eo_beam,
        eo_max_depth=args.eo_depth,
        dr_beam_width=args.dr_beam,
        dr_max_depth=args.dr_depth,
    )
    elapsed = time.time() - t0

    print(format_skeleton(skeleton))
    print(f"\n  search time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
