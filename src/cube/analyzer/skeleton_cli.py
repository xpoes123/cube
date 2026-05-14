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

from cube.analyzer.skeleton import find_skeleton, format_skeleton, Skeleton
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
    p.add_argument("--top", type=int, default=5, help="Show top-N skeletons.")
    p.add_argument("--no-niss", action="store_true",
                   help="Disable inverse-side & NISS hybrid search (~3x faster, lower quality).")
    p.add_argument("--fast", action="store_true",
                   help="Preset: --no-niss, dr-beam=2048, dr-depth=10. Use for quick triage.")
    args = p.parse_args()

    if args.fast:
        args.no_niss = True
        args.dr_beam = 2048
        args.dr_depth = 10

    if not Path(args.ckpt).exists():
        raise SystemExit(f"checkpoint not found: {args.ckpt}")

    dev = torch.device(args.device if torch.cuda.is_available() else "cpu")
    model, ckpt = _load_model(args.ckpt, dev)
    history_len = ckpt["model_cfg"]["history_len"]
    print(f"loaded {args.ckpt}")
    print(f"  val: top1={ckpt['val']['top1']:.4f} top5={ckpt['val']['top5']:.4f} "
          f"(epoch {ckpt['epoch']})")

    # Pre-warm the per-axis HTR distance tables so the first search call
    # doesn't pay the ~50s build cost mid-A*.
    from cube.classifier.features import Axis
    from cube.classifier.htr import (
        _dr_corner_to_htr_distance_table,
        _dr_edge_to_htr_distance_table,
    )
    print("  warming HTR distance tables (corners + edges × 3 axes)...")
    _t0 = time.time()
    for ax in (Axis.UD, Axis.FB, Axis.RL):
        _dr_corner_to_htr_distance_table(ax)
        _dr_edge_to_htr_distance_table(ax)
    print(f"  HTR tables ready ({time.time()-_t0:.1f}s)")
    print()

    scramble = parse_alg(args.scramble)

    t0 = time.time()
    skeletons = find_skeleton(
        model,
        scramble,
        history_len=history_len,
        device=dev,
        eo_beam_width=args.eo_beam,
        eo_max_depth=args.eo_depth,
        dr_beam_width=args.dr_beam,
        dr_max_depth=args.dr_depth,
        use_niss=not args.no_niss,
    )
    elapsed = time.time() - t0

    print(f"found {len(skeletons)} skeleton candidates; showing top {min(args.top, len(skeletons))}:")
    print()
    for i, sk in enumerate(skeletons[: args.top]):
        print(f"  --- #{i + 1} ---")
        print(format_skeleton(sk))
        print()
    print(f"  search time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
