"""Validate the skeleton analyzer against real WCA reconstructions.

Pulls scrambles from the corpus that have human-labeled EO + DR phases,
runs our analyzer on each, prints side-by-side comparison.

Output columns:
  - scramble (truncated)
  - human EO len / DR len / DR subset label
  - our top skeleton: EO len / DR len / HTR distance / expected total

The point is NOT to match move-for-move — humans find any of dozens of
equivalent skeletons. The point is to check that our analyzer's expected
total is in the same ballpark (within 1-3 moves) of what humans find.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import time
from pathlib import Path

import torch

from cube.analyzer.skeleton import find_skeleton
from cube.engine.notation import parse_alg
from cube.training.model import ModelConfig, PolicyTransformer

_SUBSET_RE = re.compile(
    r"\b(4a[12]|4b[1-5]|4c[1-4]|2c[1-5]|0c[1-4])\b"
)


def _extract_human_dr(record: dict) -> dict | None:
    """Find the EO and DR phases in a corpus record. Return None if missing."""
    phases = record.get("phases") or []
    eo_phase = next((p for p in phases if p.get("phase") == "eo"), None)
    dr_phase = next((p for p in phases if p.get("phase") == "dr"), None)
    if eo_phase is None or dr_phase is None:
        return None
    label = dr_phase.get("raw_label", "") or ""
    subset_match = _SUBSET_RE.search(label)
    return {
        "eo_moves": eo_phase.get("phase_move_count", 0),
        "dr_moves": dr_phase.get("phase_move_count", 0),
        "dr_subset": subset_match.group(0) if subset_match else None,
        "dr_label": label,
    }


def _load_corpus_samples(path: Path, n: int, seed: int = 0) -> list[dict]:
    """Pick n random records with EO + DR labels."""
    candidates: list[dict] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            human = _extract_human_dr(rec)
            if human is None:
                continue
            rec["_human"] = human
            candidates.append(rec)
    rng = random.Random(seed)
    rng.shuffle(candidates)
    return candidates[:n]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", default="data/raw/wca.jsonl")
    p.add_argument("--ckpt", default="checkpoints/policy_best.pt")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--device", default="cuda")
    p.add_argument("--eo-beam", type=int, default=256)
    p.add_argument("--dr-beam", type=int, default=256)
    args = p.parse_args()

    samples = _load_corpus_samples(Path(args.corpus), args.n, args.seed)
    if not samples:
        raise SystemExit("no corpus samples with EO+DR labels found")

    dev = torch.device(args.device if torch.cuda.is_available() else "cpu")
    ckpt = torch.load(args.ckpt, map_location=dev, weights_only=False)
    model = PolicyTransformer(ModelConfig(**ckpt["model_cfg"])).to(dev)
    model.load_state_dict(ckpt["model"])
    model.eval()
    history_len = ckpt["model_cfg"]["history_len"]

    print(f"Running analyzer on {len(samples)} corpus reconstructions")
    print(f"Model: val_top1={ckpt['val']['top1']:.3f}  val_top5={ckpt['val']['top5']:.3f}")
    print()

    headers = (
        "  | scramble".ljust(34)
        + "| human EO/DR".ljust(20)
        + "| subset".ljust(10)
        + "| our EO/DR".ljust(16)
        + "| our +HTR".ljust(12)
        + "| total".ljust(8)
        + "| delta"
    )
    print(headers)
    print("-" * len(headers))

    deltas: list[int] = []
    for i, rec in enumerate(samples):
        scramble_str = rec["scramble"]
        scramble = parse_alg(scramble_str)
        human = rec["_human"]
        scramble_display = scramble_str[:28] + ("…" if len(scramble_str) > 28 else "")

        t0 = time.time()
        skeletons = find_skeleton(
            model, scramble,
            history_len=history_len, device=dev,
            eo_beam_width=args.eo_beam, eo_max_depth=10,
            dr_beam_width=args.dr_beam, dr_max_depth=14,
        )
        elapsed = time.time() - t0
        best = skeletons[0]

        our_eo = our_dr = our_htr = our_total = None
        if len(best.stages) >= 1:
            our_eo = len(best.stages[0].moves)
        if len(best.stages) >= 2:
            our_dr = len(best.stages[1].moves)
            our_htr = best.stages[1].htr_distance
            our_total = best.total_moves + (our_htr if our_htr is not None else 99)

        human_total = human["eo_moves"] + human["dr_moves"]
        delta = (our_total - human_total) if our_total is not None else None
        if delta is not None:
            deltas.append(delta)

        print(
            f"  | {scramble_display:<28}"
            f"| {human['eo_moves']:>2}/{human['dr_moves']:>2}            "
            f"| {(human['dr_subset'] or '-'):<8} "
            f"| {our_eo or '-':>2}/{our_dr or '-':>2}          "
            f"| +{our_htr if our_htr is not None else '?':<3}      "
            f"| {our_total or '-':>3}    "
            f"| {f'{delta:+d}' if delta is not None else '-'}    [{elapsed:.0f}s]"
        )

    if deltas:
        print()
        print(f"deltas (our_total_to_HTR vs human EO+DR length):")
        print(f"  mean = {sum(deltas) / len(deltas):+.1f}")
        print(f"  median = {sorted(deltas)[len(deltas) // 2]:+d}")
        print(f"  range = [{min(deltas):+d}, {max(deltas):+d}]")


if __name__ == "__main__":
    main()
