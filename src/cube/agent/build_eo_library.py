"""Build the EO pattern library by sweeping random scrambles.

Generates N random scrambles, extracts bad-edge-slot patterns across
all 3 axes, BFS the optimal EO for each newly-seen pattern, save to
disk. Dedupes by pattern so each unique pattern gets BFS'd once.

Usage:
  uv run python -m cube.agent.build_eo_library --n-scrambles 2000 --max-depth 6
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cube.agent.scramble_gen import make_scramble
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.tools.eo_pattern_lib import (
    LIBRARY_PATH,
    build_full_library_via_eo_bfs,
    build_library_from_states,
    load_library,
    save_library,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build EO pattern library.")
    p.add_argument("--n-scrambles", type=int, default=2000,
                   help="Number of random scrambles to sample states from.")
    p.add_argument("--max-depth", type=int, default=6,
                   help="BFS depth cap for finding EO sequences.")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", type=Path, default=LIBRARY_PATH)
    p.add_argument("--append", action="store_true",
                   help="Merge into existing library instead of overwriting.")
    p.add_argument("--full", action="store_true",
                   help="Use the fast complete EO-state-space BFS (recommended). "
                        "Covers every reachable EO pattern via single forward BFS "
                        "per axis. Ignores --n-scrambles.")
    args = p.parse_args(argv)

    if args.full:
        print(f"Building full EO library via forward BFS (max_depth={args.max_depth})...")
        new_lib = build_full_library_via_eo_bfs(max_depth=args.max_depth, verbose=True)
        save_library(new_lib, args.out)
        # Quick stats.
        sizes_per_axis: dict[str, list[int]] = {"UD": [], "FB": [], "RL": []}
        pattern_sizes: dict[int, int] = {}
        for (axis, slots), moves in new_lib.items():
            sizes_per_axis.setdefault(axis, []).append(len(moves))
            pattern_sizes[len(slots)] = pattern_sizes.get(len(slots), 0) + 1
        print(f"\nWrote {args.out} ({len(new_lib)} entries)")
        for axis, lens in sizes_per_axis.items():
            if lens:
                print(f"  {axis}: {len(lens)} patterns, avg EO len = {sum(lens) / len(lens):.2f}, max = {max(lens)}")
        for k in sorted(pattern_sizes):
            print(f"  {k} bad edges: {pattern_sizes[k]} patterns")
        return 0

    print(f"Generating {args.n_scrambles} states from random scrambles...")
    states = []
    for i in range(args.n_scrambles):
        moves = make_scramble(seed=args.seed + i)
        state = SOLVED.apply_alg(parse_alg(" ".join(moves)))
        states.append(state)
    print(f"Have {len(states)} states. Building library (max_depth={args.max_depth})...")

    new_lib = build_library_from_states(states, max_depth=args.max_depth, verbose=True)

    if args.append:
        existing = load_library(args.out)
        if existing:
            print(f"Existing library: {len(existing)} entries; merging.")
            for k, v in existing.items():
                # Prefer shorter sequences if collision.
                if k not in new_lib or len(v) < len(new_lib[k]):
                    new_lib[k] = v

    save_library(new_lib, args.out)
    # Quick stats.
    sizes_per_axis: dict[str, list[int]] = {"UD": [], "FB": [], "RL": []}
    pattern_sizes: dict[int, int] = {}
    for (axis, slots), moves in new_lib.items():
        sizes_per_axis.setdefault(axis, []).append(len(moves))
        pattern_sizes[len(slots)] = pattern_sizes.get(len(slots), 0) + 1
    print(f"\nWrote {args.out} ({len(new_lib)} entries)")
    print("By axis:")
    for axis, lens in sizes_per_axis.items():
        if lens:
            print(f"  {axis}: {len(lens)} patterns, avg EO len = {sum(lens) / len(lens):.2f}, max = {max(lens)}")
    print("By pattern size (number of bad edges):")
    for k in sorted(pattern_sizes):
        print(f"  {k} bad edges: {pattern_sizes[k]} patterns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
