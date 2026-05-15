"""Pre-compute the 96 HTR subset finishes and persist them.

Sim mode's `_SUBSET_FINISH_CACHE` is in-memory per-process. Without
pre-warming, every fresh run pays the 15s "learning" cost the first
time it encounters a subset. A champion-level FMC solver has these
memorized.

Strategy: for each canonical HTR-corner-subset (96 of them), construct
a representative DR state in that subset and compute its optimal
finish via the unconstrained solve_htr_and_finish_from_dr. Pickle the
{canonical_subset_tuple -> {axis -> finish_moves}} dict to
`checkpoints/subset_finish_cache.pkl`.

Sim mode loads this on import. The cache is then "warm" before any
run starts.
"""

from __future__ import annotations

import argparse
import pickle
import sys
import time
from pathlib import Path

from cube.classifier.features import Axis, is_dr
from cube.classifier.htr import (
    _htr_corner_subset_orbits,
    dr_subset_canonical,
    htr_corner_perms,
)
from cube.engine.state import SOLVED, State
from cube.tools.search import solve_htr_and_finish_from_dr

CACHE_PATH = Path("checkpoints/subset_finish_cache.pkl")


def _state_with_cp(cp: tuple[int, ...]) -> State:
    """Build a state with the given cp + everything else solved."""
    return State(
        cp=cp, co=SOLVED.co, ep=SOLVED.ep, eo=SOLVED.eo,
        eo_fb=SOLVED.eo_fb, eo_rl=SOLVED.eo_rl,
    )


def enumerate_subset_representatives() -> list[tuple[tuple[int, ...], State]]:
    """For each HTR subset (canonical_cp), build a representative State
    in that subset that's also a valid DR-UD state."""
    orbits = _htr_corner_subset_orbits()
    representatives: list[tuple[tuple[int, ...], State]] = []
    for canonical_cp in sorted(orbits):
        # Use the canonical cp itself as the representative; we just need a
        # state with this cp + all edges + CO solved (so it's in DR-UD).
        rep = _state_with_cp(canonical_cp)
        # Sanity check: must be in DR-UD.
        if is_dr(rep, Axis.UD):
            representatives.append((canonical_cp, rep))
    return representatives


def build_cache(axes: tuple[str, ...] = ("UD",)) -> dict[tuple, dict[str, list[str]]]:
    cache: dict[tuple, dict[str, list[str]]] = {}
    reps = enumerate_subset_representatives()
    print(f"Found {len(reps)} canonical HTR subsets reachable from DR-UD.")
    t0 = time.time()
    for i, (canonical, rep) in enumerate(reps, 1):
        for axis in axes:
            # solve_htr_and_finish_from_dr wants scramble+history; we synthesize
            # an empty scramble + a "history" that recreates the state. Simpler:
            # pass scramble=[] and a tool-specific entry point.
            # But solve_htr_and_finish_from_dr starts from scramble + history.
            # We bypass by computing finish on the rep state directly.
            from cube.classifier.htr import htr_lower_bound, htr_solve, is_htr_ud
            from cube.analyzer.search import a_star_search
            from cube.analyzer.skeleton import _DR_PRESERVING

            def h(s):
                bound = htr_lower_bound(s, Axis[axis])
                return bound if bound is not None else 0

            htr_sols = a_star_search(
                None,
                start_state=rep,
                target_predicate=is_htr_ud,
                heuristic=h,
                max_depth=16,
                max_nodes=200_000,
                history_len=32,
                device=None,
                seed_history=(),
                allowed_move_indices=_DR_PRESERVING[Axis[axis]],
                policy_weight=0.0,
            )
            if not htr_sols:
                continue
            htr_moves = htr_sols[0].moves
            htr_state = rep.apply_alg(list(htr_moves))
            finish = htr_solve(htr_state)
            if finish is None:
                continue
            combined = [str(m) for m in htr_moves] + [str(m) for m in finish]
            cache.setdefault(canonical, {})[axis] = combined
        if i % 10 == 0:
            print(f"  {i}/{len(reps)} subsets, {time.time() - t0:.1f}s elapsed")
    print(f"Cache built: {sum(len(v) for v in cache.values())} entries in {time.time() - t0:.1f}s")
    return cache


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=CACHE_PATH)
    p.add_argument("--axes", nargs="+", default=["UD"], help="Axes to compute (UD/FB/RL).")
    args = p.parse_args(argv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    cache = build_cache(axes=tuple(args.axes))
    with args.out.open("wb") as f:
        pickle.dump(cache, f)
    sizes = [len(moves) for axis_map in cache.values() for moves in axis_map.values()]
    if sizes:
        print(f"finish lengths: min={min(sizes)} max={max(sizes)} avg={sum(sizes) / len(sizes):.1f}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
