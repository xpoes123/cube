"""Build the DR pattern library.

Usage:
    uv run python -m cube.agent.build_dr_library [--max-depth N]

Forward BFS in (co_tuple, slice_marker_tuple) reduced space, per axis.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from cube.tools.dr_pattern_lib import (
    LIBRARY_PATH,
    build_dr_library,
    save_library,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=16)
    parser.add_argument(
        "--out", type=Path, default=LIBRARY_PATH,
        help="Output pickle path",
    )
    args = parser.parse_args()

    print(f"Building DR pattern library (max_depth={args.max_depth}) ...")
    t0 = time.time()
    library = build_dr_library(max_depth=args.max_depth, verbose=True)
    elapsed = time.time() - t0

    save_library(library, args.out)
    size_mb = args.out.stat().st_size / 1024 / 1024
    print(f"\nSaved {len(library)} entries to {args.out} ({size_mb:.1f} MB)")
    print(f"Total build time: {elapsed:.1f}s")

    # Per-axis stats
    by_axis: dict[str, list[int]] = {"UD": [], "FB": [], "RL": []}
    for (axis_name, _co, _marker), moves in library.items():
        by_axis[axis_name].append(len(moves))
    for axis_name, lengths in by_axis.items():
        if not lengths:
            continue
        avg = sum(lengths) / len(lengths)
        print(
            f"  {axis_name}: {len(lengths):,} entries, "
            f"avg len {avg:.2f}, max {max(lengths)}"
        )


if __name__ == "__main__":
    main()
