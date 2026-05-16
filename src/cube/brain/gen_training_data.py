"""Generate per-step training data via the nissy oracle.

Pipeline (per scramble):
  1. Generate a random WCA-style scramble (or accept one as input).
  2. Walk it through nissy: eoud → drud → htr-drud → htrfin.
  3. At each step's STARTING state, query nissy for up to N optimal
     solutions. Compute the first-move distribution. Save as a SOFT
     training datum.
  4. For each intermediate state along the chosen optimal path,
     emit a HARD training datum: the next move in the optimal path
     is the target.

Soft datums (per scramble × 4 steps): the optimal-first-move
distribution from up to N enumerated optimal solutions.
Hard datums (per scramble × ~5-9 per step × 4 steps): one-hot from
the chosen optimal solution's suffix at each step.

Output: one JSONL per step in `data/brain_training/{step}.jsonl`.

Each line:
  {
    "step": "eo",
    "state": {"cp": [...], "co": [...], "ep": [...], "eo": [...]},
    "target_kind": "soft" | "hard",
    "distribution": {"D": 0.66, "D'": 0.33},   # for soft
    "target_move": "D",                          # for hard (single move)
    "optimal_remaining": 5,                       # moves left to step-solved
  }

To run:
    python -m cube.brain.gen_training_data --n 1000 --out data/brain_training
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State
from cube.tools.nissy_oracle import solve_step, full_pipeline


_STEP_TO_NISSY = {
    "eo": "eoud",
    "dr": "drud",
    "htr": "htr-drud",
    "finish": "htrfin",
}


def _state_to_dict(s: State) -> dict:
    """Compact serializable form of a State (just the 4 cube fields)."""
    return {
        "cp": list(s.cp),
        "co": list(s.co),
        "ep": list(s.ep),
        "eo": list(s.eo),
    }


def _apply(moves: list[str], from_state: State | None = None) -> State:
    """Apply moves to a starting state (SOLVED if None)."""
    s = from_state if from_state is not None else SOLVED
    if moves:
        s = s.apply_alg(parse_alg(" ".join(moves)))
    return s


def _random_scramble(rng: random.Random, length: int = 25) -> list[str]:
    """Generate a length-N WCA-style scramble (no consecutive same-face).

    Quality is roughly equivalent to nissy's `scramble`; we use python
    so the generation is fast and reproducible by seed.
    """
    faces = ["U", "D", "R", "L", "F", "B"]
    suffixes = ["", "'", "2"]
    axes = {"U": 0, "D": 0, "R": 1, "L": 1, "F": 2, "B": 2}
    out: list[str] = []
    last_face = None
    last_axis = None
    for _ in range(length):
        while True:
            f = rng.choice(faces)
            if f == last_face:
                continue
            # avoid two consecutive same-axis (e.g. R L R) — WCA rule
            if axes[f] == last_axis and last_face is not None:
                # allowed if the last_face is in same axis pair — but to keep
                # the scrambles random and unambiguous we just disallow.
                continue
            break
        out.append(f + rng.choice(suffixes))
        last_face = f
        last_axis = axes[f]
    return out


@dataclass(slots=True)
class TrainingDatum:
    step: str
    state: State
    target_kind: str  # 'soft' or 'hard'
    distribution: dict[str, float]
    target_move: str
    optimal_remaining: int

    def to_json(self) -> dict:
        out = {
            "step": self.step,
            "state": _state_to_dict(self.state),
            "target_kind": self.target_kind,
            "distribution": self.distribution,
            "target_move": self.target_move,
            "optimal_remaining": self.optimal_remaining,
        }
        return out


def datums_from_scramble(
    scramble: list[str],
    *,
    n_optimal: int = 50,
    timeout_s: float = 60.0,
) -> list[TrainingDatum]:
    """Walk one scramble through the 4-step pipeline and emit training data.

    For each step:
      - Query nissy for up to n_optimal solutions from the step's start state.
      - Emit ONE soft datum from the start state with the move distribution.
      - Emit HARD datums for each intermediate state along the chosen
        optimal path (the optimal-suffix at each prefix).
    """
    out: list[TrainingDatum] = []
    cumulative: list[str] = []  # moves so far on the scramble
    # Walk through nissy pipeline to get optimal solutions
    pipeline = full_pipeline(scramble, n_solutions=n_optimal, timeout_s=timeout_s)
    for datum in pipeline:
        step_name = datum.step_name
        # State at the START of this step
        start_state = _apply(scramble + datum.prior_moves)
        if datum.move_distribution:
            # SOFT target only at the step's starting state.
            target_move = max(datum.move_distribution.items(), key=lambda kv: kv[1])[0]
            out.append(TrainingDatum(
                step=step_name,
                state=start_state,
                target_kind="soft",
                distribution=dict(datum.move_distribution),
                target_move=target_move,
                optimal_remaining=datum.optimal_length,
            ))
        # HARD targets for intermediate states along the optimal path.
        # Skip index 0 because it duplicates the soft datum's state.
        running_state = start_state
        chosen = datum.chosen_optimal
        for i, m in enumerate(chosen):
            if i == 0:
                running_state = _apply([m], running_state)
                continue
            out.append(TrainingDatum(
                step=step_name,
                state=running_state,
                target_kind="hard",
                distribution={m: 1.0},
                target_move=m,
                optimal_remaining=len(chosen) - i,
            ))
            running_state = _apply([m], running_state)
        # The first datum is duplicative with the soft datum's state but
        # carries the chosen-optimal hard target — kept for completeness.
        cumulative.extend(chosen)
    return out


def _open_writers(out_dir: Path) -> dict[str, "object"]:
    out_dir.mkdir(parents=True, exist_ok=True)
    return {step: (out_dir / f"{step}.jsonl").open("a") for step in _STEP_TO_NISSY}


def _close_writers(writers: dict) -> None:
    for w in writers.values():
        w.close()


def _worker_one(args: tuple[list[str], int]) -> list[dict]:
    """Multiprocessing worker — solves one scramble, returns serializable datums."""
    scramble, n_optimal = args
    try:
        datums = datums_from_scramble(scramble, n_optimal=n_optimal)
    except Exception:
        return []
    return [d.to_json() for d in datums]


def generate_corpus(
    n_scrambles: int,
    out_dir: Path,
    *,
    seed: int = 42,
    n_optimal: int = 50,
    verbose: bool = True,
    progress_every: int = 100,
    workers: int = 1,
) -> dict[str, int]:
    """Generate a per-step JSONL corpus of training data.

    Returns counts of records written per step.
    """
    rng = random.Random(seed)
    writers = _open_writers(out_dir)
    counts = {step: 0 for step in _STEP_TO_NISSY}
    t0 = time.time()
    scrambles = [_random_scramble(rng) for _ in range(n_scrambles)]
    try:
        if workers > 1:
            # Parallel path. Pool unordered for max throughput.
            args = [(s, n_optimal) for s in scrambles]
            with mp.Pool(workers) as pool:
                for i, datums_json in enumerate(pool.imap_unordered(_worker_one, args, chunksize=4)):
                    for d_json in datums_json:
                        writers[d_json["step"]].write(json.dumps(d_json) + "\n")
                        counts[d_json["step"]] += 1
                    if verbose and (i + 1) % progress_every == 0:
                        elapsed = time.time() - t0
                        rate = (i + 1) / elapsed
                        print(f"  {i + 1}/{n_scrambles} scrambles "
                              f"({rate:.1f}/s, ~{(n_scrambles - i - 1) / max(rate, 0.01):.0f}s remaining); "
                              f"records: {counts}", file=sys.stderr, flush=True)
            return counts
        # Serial path
        for i in range(n_scrambles):
            scramble = scrambles[i]
            try:
                datums = datums_from_scramble(scramble, n_optimal=n_optimal)
            except Exception as e:
                if verbose:
                    print(f"  scramble {i}: failed ({type(e).__name__}: {e})", file=sys.stderr)
                continue
            for d in datums:
                line = json.dumps(d.to_json())
                writers[d.step].write(line + "\n")
                counts[d.step] += 1
            if verbose and (i + 1) % progress_every == 0:
                elapsed = time.time() - t0
                rate = (i + 1) / elapsed
                print(f"  {i + 1}/{n_scrambles} scrambles "
                      f"({rate:.1f}/s, ~{(n_scrambles - i - 1) / max(rate, 0.01):.0f}s remaining); "
                      f"records: {counts}", file=sys.stderr, flush=True)
    finally:
        _close_writers(writers)
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=100, help="Number of scrambles.")
    parser.add_argument("--out", type=Path, default=Path("data/brain_training"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-optimal", type=int, default=50,
                        help="Cap on optimal-solutions to enumerate per soft target.")
    parser.add_argument("--workers", type=int, default=1,
                        help="Parallel worker processes (uses multiprocessing.Pool).")
    args = parser.parse_args(argv)

    print(f"Generating brain training data: n={args.n} workers={args.workers} → {args.out}", file=sys.stderr)
    t0 = time.time()
    counts = generate_corpus(
        args.n, args.out, seed=args.seed,
        n_optimal=args.n_optimal, verbose=True, workers=args.workers,
    )
    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s. Records per step:", file=sys.stderr)
    for step, c in counts.items():
        print(f"  {step}: {c}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
