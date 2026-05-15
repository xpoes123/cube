"""WCA-style scramble generator.

Produces 25-move scrambles obeying standard WCA constraints:
- No consecutive moves on the same face.
- No three consecutive moves on the same axis pair (e.g., U then D then U).

Deterministic given a seed so runs reproduce.
"""

from __future__ import annotations

import argparse
import random
import sys

_FACES = ["U", "D", "F", "B", "R", "L"]
_AXIS = {"U": 0, "D": 0, "F": 1, "B": 1, "R": 2, "L": 2}
_MODS = ["", "'", "2"]


def make_scramble(n_moves: int = 25, seed: int | None = None) -> list[str]:
    rng = random.Random(seed)
    moves: list[str] = []
    last_face: str | None = None
    last2_axis: int | None = None
    while len(moves) < n_moves:
        f = rng.choice(_FACES)
        if f == last_face:
            continue
        # No three consecutive same-axis: if the two prior moves' axis equals
        # this candidate's axis (and last is on the OTHER face of that axis),
        # disallow.
        if last_face is not None and last2_axis == _AXIS[f] and _AXIS[last_face] == _AXIS[f]:
            continue
        m = rng.choice(_MODS)
        moves.append(f + m)
        last2_axis = _AXIS[last_face] if last_face else None
        last_face = f
    return moves


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate WCA-style scrambles.")
    p.add_argument("-n", "--count", type=int, default=10, help="Number of scrambles to generate.")
    p.add_argument("--seed", type=int, default=0, help="Base seed (each scramble uses seed+i).")
    args = p.parse_args(argv)
    for i in range(args.count):
        s = make_scramble(seed=args.seed + i)
        print(f"# scramble{i+1} (seed={args.seed + i})")
        print(" ".join(s))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
