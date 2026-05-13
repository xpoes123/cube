"""Training loop for the policy transformer.

Cross-entropy on next-move targets. Evaluates top-1 / top-5 on val each
epoch; checkpoints best-val to `checkpoints/policy_best.pt`.

CLI:
    uv run python -m cube.training.train --epochs 30
"""

from __future__ import annotations

import argparse
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader

from cube.training.model import ModelConfig, PolicyTransformer, count_params
from cube.training.torchdata import (
    CubeMovesDataset,
    TensorBundle,
    build_splits,
)


@dataclass
class TrainConfig:
    jsonl_path: str = "data/raw/wca.jsonl"
    history_len: int = 32
    epochs: int = 30
    batch_size: int = 512
    lr: float = 3e-4
    weight_decay: float = 0.01
    warmup_frac: float = 0.05
    seed: int = 42
    device: str = "cuda"
    num_workers: int = 0
    ckpt_dir: str = "checkpoints"
    log_every: int = 50
    limit: int | None = None


def _accuracy(logits: torch.Tensor, target: torch.Tensor, k: int = 1) -> float:
    """Top-k accuracy on a single batch."""
    if k == 1:
        pred = logits.argmax(dim=-1)
        return (pred == target).float().mean().item()
    topk = logits.topk(k, dim=-1).indices
    hit = (topk == target.unsqueeze(-1)).any(dim=-1)
    return hit.float().mean().item()


def _evaluate(
    model: PolicyTransformer,
    bundle: TensorBundle,
    device: torch.device,
    batch_size: int,
) -> dict[str, float]:
    """Run full pass over a bundle, return top-1/top-5 + loss."""
    model.eval()
    loss_fn = nn.CrossEntropyLoss(reduction="sum")
    n_total = 0
    loss_sum = 0.0
    top1_sum = 0
    top5_sum = 0
    with torch.no_grad():
        for i in range(0, len(bundle), batch_size):
            sl = slice(i, i + batch_size)
            cp = bundle.cp[sl].long().to(device)
            co = bundle.co[sl].long().to(device)
            ep = bundle.ep[sl].long().to(device)
            eo = bundle.eo[sl].long().to(device)
            eo_fb = bundle.eo_fb[sl].long().to(device)
            eo_rl = bundle.eo_rl[sl].long().to(device)
            history = bundle.history[sl].long().to(device)
            target = bundle.target[sl].to(device)

            logits = model(cp, co, ep, eo, eo_fb, eo_rl, history)
            loss_sum += loss_fn(logits, target).item()
            top1_sum += int((logits.argmax(-1) == target).sum().item())
            top5_hits = (logits.topk(5, dim=-1).indices == target.unsqueeze(-1)).any(dim=-1)
            top5_sum += int(top5_hits.sum().item())
            n_total += target.size(0)

    return {
        "loss": loss_sum / max(n_total, 1),
        "top1": top1_sum / max(n_total, 1),
        "top5": top5_sum / max(n_total, 1),
        "n": n_total,
    }


def train(cfg: TrainConfig, model_cfg: ModelConfig | None = None) -> dict:
    torch.manual_seed(cfg.seed)
    device = torch.device(cfg.device if torch.cuda.is_available() else "cpu")

    print(f"loading corpus from {cfg.jsonl_path} ...")
    t0 = time.time()
    splits = build_splits(
        cfg.jsonl_path,
        history_len=cfg.history_len,
        seed=cfg.seed,
        limit=cfg.limit,
    )
    print(
        f"  loaded in {time.time() - t0:.1f}s "
        f"(train={len(splits.train)} val={len(splits.val)} test={len(splits.test)})"
    )

    train_ds = CubeMovesDataset(splits.train)
    loader = DataLoader(
        train_ds,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
        pin_memory=device.type == "cuda",
        drop_last=False,
    )

    model_cfg = model_cfg or ModelConfig(history_len=cfg.history_len)
    model = PolicyTransformer(model_cfg).to(device)
    print(f"model: {count_params(model):,} params, cfg={asdict(model_cfg)}")

    optim = torch.optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
    total_steps = max(1, cfg.epochs * len(loader))
    warmup_steps = max(1, int(total_steps * cfg.warmup_frac))

    def lr_at(step: int) -> float:
        if step < warmup_steps:
            return step / warmup_steps
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return 0.5 * (1.0 + math.cos(math.pi * progress))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optim, lr_lambda=lr_at)
    loss_fn = nn.CrossEntropyLoss()

    ckpt_dir = Path(cfg.ckpt_dir)
    ckpt_dir.mkdir(exist_ok=True)
    best_val_top1 = -1.0
    best_metrics: dict[str, float] = {}

    step = 0
    for epoch in range(cfg.epochs):
        model.train()
        epoch_t0 = time.time()
        running_loss = 0.0
        running_n = 0
        running_top1 = 0
        for batch in loader:
            for k, v in batch.items():
                batch[k] = v.to(device, non_blocking=True)

            logits = model(
                batch["cp"], batch["co"], batch["ep"],
                batch["eo"], batch["eo_fb"], batch["eo_rl"],
                batch["history"],
            )
            loss = loss_fn(logits, batch["target"])

            optim.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optim.step()
            scheduler.step()

            bs = batch["target"].size(0)
            running_loss += loss.item() * bs
            running_n += bs
            running_top1 += int((logits.argmax(-1) == batch["target"]).sum().item())
            step += 1

            if step % cfg.log_every == 0:
                print(
                    f"  step {step:>6}  "
                    f"train_loss={running_loss / running_n:.4f}  "
                    f"train_top1={running_top1 / running_n:.4f}  "
                    f"lr={optim.param_groups[0]['lr']:.2e}"
                )

        # End-of-epoch val.
        val_metrics = _evaluate(model, splits.val, device, cfg.batch_size)
        epoch_time = time.time() - epoch_t0
        print(
            f"epoch {epoch + 1:>3}/{cfg.epochs}  "
            f"train_loss={running_loss / running_n:.4f}  "
            f"val_loss={val_metrics['loss']:.4f}  "
            f"val_top1={val_metrics['top1']:.4f}  "
            f"val_top5={val_metrics['top5']:.4f}  "
            f"({epoch_time:.1f}s)"
        )

        if val_metrics["top1"] > best_val_top1:
            best_val_top1 = val_metrics["top1"]
            best_metrics = val_metrics
            torch.save(
                {
                    "model": model.state_dict(),
                    "model_cfg": asdict(model_cfg),
                    "train_cfg": asdict(cfg),
                    "val": val_metrics,
                    "epoch": epoch + 1,
                },
                ckpt_dir / "policy_best.pt",
            )

    # Final test eval using best checkpoint.
    ckpt = torch.load(ckpt_dir / "policy_best.pt", map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    test_metrics = _evaluate(model, splits.test, device, cfg.batch_size)
    print(
        f"BEST val_top1={best_metrics['top1']:.4f} val_top5={best_metrics['top5']:.4f} "
        f"@ epoch {ckpt['epoch']}"
    )
    print(
        f"TEST top1={test_metrics['top1']:.4f} top5={test_metrics['top5']:.4f} "
        f"loss={test_metrics['loss']:.4f}"
    )
    return {"best_val": best_metrics, "test": test_metrics}


def _parse_args() -> tuple[TrainConfig, ModelConfig]:
    p = argparse.ArgumentParser()
    p.add_argument("--jsonl-path", default="data/raw/wca.jsonl")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--batch-size", type=int, default=512)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--history-len", type=int, default=32)
    p.add_argument("--d-model", type=int, default=96)
    p.add_argument("--n-layers", type=int, default=3)
    p.add_argument("--n-heads", type=int, default=4)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--device", default="cuda")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()
    train_cfg = TrainConfig(
        jsonl_path=args.jsonl_path,
        history_len=args.history_len,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
        seed=args.seed,
        limit=args.limit,
    )
    model_cfg = ModelConfig(
        d_model=args.d_model,
        n_heads=args.n_heads,
        n_layers=args.n_layers,
        dropout=args.dropout,
        history_len=args.history_len,
    )
    return train_cfg, model_cfg


def main() -> None:
    train_cfg, model_cfg = _parse_args()
    train(train_cfg, model_cfg)


if __name__ == "__main__":
    main()
