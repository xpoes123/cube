"""Train a per-step brain model.

Reads `data/brain_training/{step}.jsonl`, builds a Dataset of
(state_tokens, target_distribution) pairs, trains a BrainStepModel
with KL divergence against the soft (or hard one-hot) target.

One step is trained at a time:
    python -m cube.brain.train --step eo --epochs 30
    python -m cube.brain.train --step dr --epochs 30
    python -m cube.brain.train --step htr --epochs 30
    python -m cube.brain.train --step finish --epochs 30

Checkpoints saved to `checkpoints/brain_{step}.pt`.

We use KL divergence (soft cross-entropy) as the loss — same loss
works for hard one-hot targets (KL collapses to standard CE) and soft
distribution targets. This is the "humanlike" formulation: multiple
moves can be equally optimal; the model learns that distribution.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset

from cube.brain.model import BrainStepModel, STEP_ALPHABETS
from cube.engine.state import State


@dataclass(slots=True)
class StateRecord:
    """One on-disk JSONL training record, parsed."""
    state: State
    target_distribution: dict[str, float]  # move → probability


class BrainDataset(Dataset):
    """Lazy in-memory dataset over a JSONL file.

    Each item is converted to fixed-size tensors at __getitem__ time.
    The dataset is small enough (~50K records per step) that we just
    parse the whole file into memory once.
    """

    def __init__(self, jsonl_path: Path, step: str) -> None:
        self.step = step
        self.alphabet = STEP_ALPHABETS[step]
        self.move_to_idx = {m: i for i, m in enumerate(self.alphabet)}
        self.records: list[StateRecord] = []
        with jsonl_path.open() as f:
            for line in f:
                d = json.loads(line)
                if d["step"] != step:
                    continue  # safety filter
                state = State(
                    cp=tuple(d["state"]["cp"]),
                    co=tuple(d["state"]["co"]),
                    ep=tuple(d["state"]["ep"]),
                    eo=tuple(d["state"]["eo"]),
                )
                # Filter target distribution to legal moves for this step's
                # alphabet. If any optimal move is OUT-of-alphabet, the
                # record is a domain mismatch (e.g. EO target needs the
                # 18-move alphabet, but if a DR-targeting record's move
                # isn't EO-preserving it'd be filtered here).
                dist = {m: p for m, p in d["distribution"].items() if m in self.move_to_idx}
                if not dist:
                    continue  # skip records whose moves are all out-of-alphabet
                # Renormalize after filtering.
                tot = sum(dist.values())
                dist = {m: p / tot for m, p in dist.items()}
                self.records.append(StateRecord(state=state, target_distribution=dist))

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, i: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        r = self.records[i]
        slot_idx = torch.arange(20, dtype=torch.long)
        cubie_idx = torch.tensor(list(r.state.cp) + list(r.state.ep), dtype=torch.long)
        orientation = torch.tensor(list(r.state.co) + list(r.state.eo), dtype=torch.long)
        target = torch.zeros(len(self.alphabet), dtype=torch.float32)
        for move, prob in r.target_distribution.items():
            target[self.move_to_idx[move]] = prob
        return slot_idx, cubie_idx, orientation, target


def kl_loss(logits: torch.Tensor, target_dist: torch.Tensor) -> torch.Tensor:
    """KL(target || softmax(logits)).

    Both soft and one-hot targets work; for one-hot this reduces to
    standard cross-entropy with the single nonzero class.
    """
    log_pred = F.log_softmax(logits, dim=-1)
    # KL(target || pred) = sum target * (log target - log pred).
    # We drop the log-target term (constant w.r.t. params) and use
    # negative log-likelihood weighted by target probabilities.
    return -(target_dist * log_pred).sum(dim=-1).mean()


def train_one_step(
    step: str,
    jsonl_path: Path,
    *,
    out_path: Path,
    epochs: int = 30,
    batch_size: int = 256,
    lr: float = 3e-4,
    val_frac: float = 0.05,
    seed: int = 42,
    device: str | None = None,
) -> dict:
    """Train a single-step model. Returns final train/val losses."""
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[train] step={step} device={device}", file=sys.stderr)

    ds = BrainDataset(jsonl_path, step)
    if len(ds) == 0:
        raise RuntimeError(f"no training records for step {step!r} in {jsonl_path}")
    print(f"[train] dataset size: {len(ds)}", file=sys.stderr)

    # Split train/val
    rng = random.Random(seed)
    indices = list(range(len(ds)))
    rng.shuffle(indices)
    n_val = max(1, int(len(ds) * val_frac))
    val_idx = set(indices[:n_val])
    train_idx = [i for i in indices if i not in val_idx]
    val_idx = list(val_idx)

    train_loader = DataLoader(
        torch.utils.data.Subset(ds, train_idx),
        batch_size=batch_size, shuffle=True, num_workers=0,
    )
    val_loader = DataLoader(
        torch.utils.data.Subset(ds, val_idx),
        batch_size=batch_size, shuffle=False, num_workers=0,
    )

    model = BrainStepModel(step=step).to(device)
    print(f"[train] model params: {model.param_count()}", file=sys.stderr)

    opt = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    sched = optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)

    best_val = float("inf")
    history: list[dict] = []
    t0 = time.time()
    for ep in range(1, epochs + 1):
        model.train()
        ep_train_loss = 0.0
        ep_train_n = 0
        for slot_idx, cubie_idx, orient, target in train_loader:
            slot_idx = slot_idx.to(device)
            cubie_idx = cubie_idx.to(device)
            orient = orient.to(device)
            target = target.to(device)
            logits = model(slot_idx, cubie_idx, orient)
            loss = kl_loss(logits, target)
            opt.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            opt.step()
            ep_train_loss += loss.item() * slot_idx.size(0)
            ep_train_n += slot_idx.size(0)
        sched.step()
        train_loss = ep_train_loss / max(1, ep_train_n)

        # validation
        model.eval()
        ep_val_loss = 0.0
        ep_val_n = 0
        ep_val_acc = 0
        with torch.no_grad():
            for slot_idx, cubie_idx, orient, target in val_loader:
                slot_idx = slot_idx.to(device)
                cubie_idx = cubie_idx.to(device)
                orient = orient.to(device)
                target = target.to(device)
                logits = model(slot_idx, cubie_idx, orient)
                ep_val_loss += kl_loss(logits, target).item() * slot_idx.size(0)
                ep_val_n += slot_idx.size(0)
                pred = logits.argmax(dim=-1)
                tgt = target.argmax(dim=-1)
                ep_val_acc += (pred == tgt).sum().item()
        val_loss = ep_val_loss / max(1, ep_val_n)
        val_acc = ep_val_acc / max(1, ep_val_n)
        elapsed = time.time() - t0
        history.append({"epoch": ep, "train_loss": train_loss, "val_loss": val_loss, "val_acc": val_acc, "elapsed_s": elapsed})
        print(f"  ep={ep:2d}  train={train_loss:.4f}  val={val_loss:.4f}  val_top1_acc={val_acc:.3f}  "
              f"[{elapsed:.0f}s]", file=sys.stderr)

        if val_loss < best_val:
            best_val = val_loss
            out_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save({
                "step": step,
                "state_dict": model.state_dict(),
                "config": model.cfg.__dict__,
                "epoch": ep,
                "val_loss": val_loss,
                "val_acc": val_acc,
                "history": history,
            }, out_path)

    return {"best_val_loss": best_val, "history": history}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--step", choices=sorted(STEP_ALPHABETS), required=True)
    parser.add_argument("--data-dir", type=Path, default=Path("data/brain_training"))
    parser.add_argument("--out-dir", type=Path, default=Path("checkpoints"))
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--val-frac", type=float, default=0.05)
    parser.add_argument("--device", default=None)
    args = parser.parse_args(argv)

    jsonl = args.data_dir / f"{args.step}.jsonl"
    if not jsonl.exists():
        print(f"error: {jsonl} not found. Run gen_training_data first.", file=sys.stderr)
        return 2

    out_path = args.out_dir / f"brain_{args.step}.pt"
    summary = train_one_step(
        args.step, jsonl,
        out_path=out_path,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        val_frac=args.val_frac,
        seed=args.seed,
        device=args.device,
    )
    print(f"\n[done] best val_loss = {summary['best_val_loss']:.4f}, saved to {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
