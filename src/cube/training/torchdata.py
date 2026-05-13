"""PyTorch Dataset / collate for the policy transformer.

The full corpus is small (~61k examples post-flatten), so we materialize
all tensors in memory once and serve them by index. No streaming, no
shuffling cost — the heavy work (parse JSONL → State → tensors) happens
at startup, then training iterates over a contiguous block of int8/int64
arrays.

Splits use `split_by_source_id` so all moves of a single solve stay
together in train/val/test.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset

from cube.training.dataset import TrainingExample
from cube.training.encoding import encode_move
from cube.training.loader import iter_examples_from_jsonl
from cube.training.model import PAD_MOVE
from cube.training.split import split_by_source_id


@dataclass
class TensorBundle:
    """All training-relevant tensors materialized for one split."""

    cp: torch.Tensor       # (N, 8)  uint8
    co: torch.Tensor       # (N, 8)  uint8
    ep: torch.Tensor       # (N, 12) uint8
    eo: torch.Tensor       # (N, 12) uint8
    eo_fb: torch.Tensor    # (N, 12) uint8
    eo_rl: torch.Tensor    # (N, 12) uint8
    history: torch.Tensor  # (N, K)  uint8 (PAD_MOVE for missing)
    target: torch.Tensor   # (N,)    int64

    def __len__(self) -> int:
        return self.target.size(0)


class CubeMovesDataset(Dataset):
    """Indexable view over a TensorBundle."""

    def __init__(self, bundle: TensorBundle) -> None:
        self.b = bundle

    def __len__(self) -> int:
        return len(self.b)

    def __getitem__(self, i: int) -> dict[str, torch.Tensor]:
        b = self.b
        return {
            "cp": b.cp[i].long(),
            "co": b.co[i].long(),
            "ep": b.ep[i].long(),
            "eo": b.eo[i].long(),
            "eo_fb": b.eo_fb[i].long(),
            "eo_rl": b.eo_rl[i].long(),
            "history": b.history[i].long(),
            "target": b.target[i],
        }


def _examples_to_bundle(
    examples: Iterable[TrainingExample],
    history_len: int,
) -> TensorBundle:
    """Stack a list of examples into typed numpy arrays then to torch tensors."""
    cp, co, ep, eo, eo_fb, eo_rl = [], [], [], [], [], []
    history, target = [], []
    for ex in examples:
        s = ex.state_before
        cp.append(s.cp)
        co.append(s.co)
        ep.append(s.ep)
        eo.append(s.eo)
        eo_fb.append(s.eo_fb)
        eo_rl.append(s.eo_rl)

        # Take last K moves, left-pad with PAD_MOVE. Output order: oldest → newest.
        recent = ex.history[-history_len:]
        pad_n = history_len - len(recent)
        encoded = [PAD_MOVE] * pad_n + [encode_move(m) for m in recent]
        history.append(encoded)

        target.append(encode_move(ex.target_move))

    def _to(arr, dtype):
        return torch.from_numpy(np.asarray(arr, dtype=dtype))

    return TensorBundle(
        cp=_to(cp, np.uint8),
        co=_to(co, np.uint8),
        ep=_to(ep, np.uint8),
        eo=_to(eo, np.uint8),
        eo_fb=_to(eo_fb, np.uint8),
        eo_rl=_to(eo_rl, np.uint8),
        history=_to(history, np.uint8),
        target=_to(target, np.int64),
    )


@dataclass
class SplitBundles:
    train: TensorBundle
    val: TensorBundle
    test: TensorBundle


def build_splits(
    jsonl_path: str | Path,
    history_len: int = 32,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
    limit: int | None = None,
) -> SplitBundles:
    """Load JSONL, materialize tensors per split, return all three bundles.

    `limit`: cap on number of source records (for quick experiments).
    """
    # First pass: bucket examples by source_id assignment.
    # We iterate once; iter_examples_from_jsonl yields all examples in source order.
    train_ex: list[TrainingExample] = []
    val_ex: list[TrainingExample] = []
    test_ex: list[TrainingExample] = []

    # We need source_ids known up front for the splitter, but the iterator
    # doesn't expose record order without a pre-pass. Simplest correct approach:
    # collect all examples, gather distinct source_ids, split, then partition.
    all_examples: list[TrainingExample] = []
    seen_sources: list[str] = []
    seen_set: set[str] = set()
    for ex in iter_examples_from_jsonl(jsonl_path):
        if ex.source_id not in seen_set:
            seen_set.add(ex.source_id)
            seen_sources.append(ex.source_id)
            if limit is not None and len(seen_sources) > limit:
                # We've already added this example; pop the source_id we just added
                # and stop iterating.
                seen_set.remove(ex.source_id)
                seen_sources.pop()
                break
        all_examples.append(ex)

    train_set, val_set, test_set = split_by_source_id(
        seen_sources, val_ratio=val_ratio, test_ratio=test_ratio, seed=seed
    )

    for ex in all_examples:
        if ex.source_id in train_set:
            train_ex.append(ex)
        elif ex.source_id in val_set:
            val_ex.append(ex)
        else:
            test_ex.append(ex)

    return SplitBundles(
        train=_examples_to_bundle(train_ex, history_len),
        val=_examples_to_bundle(val_ex, history_len),
        test=_examples_to_bundle(test_ex, history_len),
    )
