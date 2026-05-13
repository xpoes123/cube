"""Train/val/test split utilities.

Splits are by reconstruction (source_id), not by individual examples — so
all moves from one solve stay together in the same split. This prevents
information leakage from later moves of a solve appearing in train while
earlier moves appear in val.

Deterministic given a seed.
"""

from __future__ import annotations

import hashlib


def split_by_source_id(
    source_ids: list[str],
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[set[str], set[str], set[str]]:
    """Partition source IDs into (train, val, test) sets.

    Uses a hash of (seed, source_id) for stable, content-addressed splitting.
    Adding new source IDs later won't shuffle existing assignments.
    """
    train: set[str] = set()
    val: set[str] = set()
    test: set[str] = set()
    for sid in source_ids:
        bucket = _bucket(sid, seed)
        if bucket < test_ratio:
            test.add(sid)
        elif bucket < test_ratio + val_ratio:
            val.add(sid)
        else:
            train.add(sid)
    return train, val, test


def _bucket(source_id: str, seed: int) -> float:
    """Hash source_id to a deterministic value in [0, 1)."""
    h = hashlib.sha1(f"{seed}:{source_id}".encode()).hexdigest()
    # Use first 8 hex chars as a 32-bit int, normalize.
    return int(h[:8], 16) / 0xFFFFFFFF
