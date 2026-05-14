"""Validation / benchmark harness for the staged FMC skeleton analyzer.

Loads N random scrambles from the WCA corpus, runs `find_skeleton` on each
under a configurable wall-clock budget, and reports per-scramble and
aggregate stats (success rate, stages reached, move counts, human-delta).

Each scramble runs in its own subprocess so we can enforce a hard time
budget by terminating the worker. Workers default to CPU (the policy is
91K params, so CPU is fast and we can parallelize beyond a single GPU).

Example:
    uv run python -m cube.analyzer.validate \\
        --corpus data/raw/wca.jsonl \\
        --n 10 --seed 0 --time-budget 300 --workers 4 \\
        --report benchmarks/baseline.md
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import random
import statistics
import sys
import time
import traceback
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


# Per-scramble worker: imports are inside the function so the parent process
# doesn't pay torch's import cost when spawning workers via "spawn".
def _worker_entry(
    scramble_str: str,
    ckpt_path: str,
    device: str,
    eo_beam: int,
    eo_depth: int,
    dr_beam: int,
    dr_depth: int,
    result_q: mp.Queue,
    use_niss: bool = True,
) -> None:
    """Run find_skeleton on one scramble, push result onto queue.

    Result is a dict with: best_total_moves, stages_reached, full_solve,
    timing, error (if any). The parent reads from the queue and falls back
    to a timeout sentinel if the worker is killed.
    """
    try:
        import torch  # noqa: F401  (heavy import inside the worker)

        from cube.analyzer.skeleton import find_skeleton
        from cube.engine.notation import parse_alg
        from cube.engine.state import SOLVED
        from cube.training.model import ModelConfig, PolicyTransformer

        t_start = time.time()

        dev = torch.device(device)
        ckpt = torch.load(ckpt_path, map_location=dev, weights_only=False)
        cfg = ModelConfig(**ckpt["model_cfg"])
        model = PolicyTransformer(cfg).to(dev)
        model.load_state_dict(ckpt["model"])
        model.eval()
        history_len = ckpt["model_cfg"]["history_len"]

        scramble = parse_alg(scramble_str)

        t_search = time.time()
        skeletons = find_skeleton(
            model,
            scramble,
            history_len=history_len,
            device=dev,
            eo_beam_width=eo_beam,
            eo_max_depth=eo_depth,
            dr_beam_width=dr_beam,
            dr_max_depth=dr_depth,
            use_niss=use_niss,
        )
        search_elapsed = time.time() - t_search
        total_elapsed = time.time() - t_start

        # The first skeleton is the top-ranked one (see find_skeleton's rank).
        best = skeletons[0] if skeletons else None
        if best is None or not best.stages:
            stages_reached = 0
            best_total = None
            full_solve = False
            stage_names: list[str] = []
        else:
            stages_reached = len(best.stages)
            best_total = best.total_moves
            full_solve = best.stages[-1].end_state == SOLVED
            stage_names = [s.name for s in best.stages]

        # Also report: shortest full-solve skeleton among all candidates
        # (the top-ranked one is usually best, but verify).
        shortest_full = None
        any_full = False
        for sk in skeletons:
            if sk.stages and sk.stages[-1].end_state == SOLVED:
                any_full = True
                ln = sk.total_moves
                if shortest_full is None or ln < shortest_full:
                    shortest_full = ln

        result_q.put({
            "ok": True,
            "stages_reached": stages_reached,
            "stage_names": stage_names,
            "best_total_moves": best_total,
            "full_solve": full_solve,
            "any_full_solve": any_full,
            "shortest_full_solve": shortest_full,
            "n_candidates": len(skeletons),
            "search_elapsed": search_elapsed,
            "total_elapsed": total_elapsed,
        })
    except Exception as e:
        import contextlib
        with contextlib.suppress(Exception):
            result_q.put({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
            })


@dataclass
class ScrambleResult:
    index: int
    scramble: str
    source_id: str
    human_length: int | None
    # Worker outputs:
    ok: bool = False
    timed_out: bool = False
    error: str | None = None
    stages_reached: int = 0
    stage_names: list[str] = field(default_factory=list)
    best_total_moves: int | None = None
    full_solve: bool = False
    any_full_solve: bool = False
    shortest_full_solve: int | None = None
    n_candidates: int = 0
    search_elapsed: float | None = None
    total_elapsed: float | None = None
    wall_elapsed: float | None = None


def _load_corpus(path: Path, n: int, seed: int) -> list[dict]:
    """Read all corpus rows, return a seeded random sample of size n."""
    rows: list[dict] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    # Filter to entries with usable scrambles.
    rows = [r for r in rows if r.get("scramble")]
    rng = random.Random(seed)
    return rng.sample(rows, min(n, len(rows)))


def _run_one(
    scramble_str: str,
    ckpt_path: str,
    device: str,
    eo_beam: int,
    eo_depth: int,
    dr_beam: int,
    dr_depth: int,
    time_budget: float,
    use_niss: bool = True,
) -> tuple[dict | None, bool, float]:
    """Run find_skeleton in a subprocess with a hard wall-clock budget.

    Returns (result_dict or None, timed_out, wall_elapsed). If timed_out,
    the worker was terminated; result is None.
    """
    ctx = mp.get_context("spawn")
    q: mp.Queue = ctx.Queue()
    p = ctx.Process(
        target=_worker_entry,
        args=(scramble_str, ckpt_path, device, eo_beam, eo_depth,
              dr_beam, dr_depth, q, use_niss),
        daemon=True,
    )
    t0 = time.time()
    p.start()
    p.join(time_budget)
    wall = time.time() - t0

    if p.is_alive():
        p.terminate()
        p.join(5)
        if p.is_alive():
            p.kill()
            p.join()
        return None, True, wall

    # Process exited; try to pull a result (it may have errored before push).
    try:
        result = q.get_nowait()
    except Exception:
        return None, False, wall
    return result, False, wall


def _format_human_length(length: int | None) -> str:
    return str(length) if length is not None else "—"


def _fmt(v: float | None, spec: str = ".1f") -> str:
    if v is None:
        return "—"
    return f"{v:{spec}}"


def _stage_summary(name: str) -> str:
    """Compact label, e.g. 'EO (UD)' -> 'EO', 'DR (FB)' -> 'DR', 'Finish' -> 'F'."""
    if name.startswith("EO"):
        return "EO"
    if name.startswith("DR"):
        return "DR"
    if name.startswith("HTR"):
        return "HTR"
    if name.startswith("Finish"):
        return "F"
    return name


def aggregate(results: list[ScrambleResult]) -> dict[str, Any]:
    n = len(results)
    n_ok = sum(1 for r in results if r.ok and not r.timed_out)
    n_timeout = sum(1 for r in results if r.timed_out)
    n_error = sum(1 for r in results if r.error and not r.timed_out)
    n_full = sum(1 for r in results if r.full_solve)
    n_any_full = sum(1 for r in results if r.any_full_solve)

    solve_lens = [r.best_total_moves for r in results
                  if r.full_solve and r.best_total_moves is not None]
    shortest_lens = [r.shortest_full_solve for r in results
                     if r.shortest_full_solve is not None]

    # Stage distribution among non-timeout results.
    stage_hist: dict[int, int] = {}
    for r in results:
        if r.timed_out:
            continue
        stage_hist[r.stages_reached] = stage_hist.get(r.stages_reached, 0) + 1

    # Human-delta: only for full-solve scrambles where corpus had a length.
    deltas = []
    beats_human = 0
    for r in results:
        if r.full_solve and r.best_total_moves is not None \
                and r.human_length is not None:
            d = r.best_total_moves - r.human_length
            deltas.append(d)
            if d < 0:
                beats_human += 1

    times = [r.wall_elapsed for r in results if r.wall_elapsed is not None]

    def _safe_mean(xs: list[float | int]) -> float | None:
        return statistics.mean(xs) if xs else None

    def _safe_median(xs: list[float | int]) -> float | None:
        return statistics.median(xs) if xs else None

    return {
        "n": n,
        "n_ok": n_ok,
        "n_timeout": n_timeout,
        "n_error": n_error,
        "n_full_solve": n_full,
        "n_any_full_solve": n_any_full,
        "full_solve_rate": n_full / n if n else 0.0,
        "any_full_solve_rate": n_any_full / n if n else 0.0,
        "solve_mean": _safe_mean(solve_lens),
        "solve_median": _safe_median(solve_lens),
        "solve_min": min(solve_lens) if solve_lens else None,
        "solve_max": max(solve_lens) if solve_lens else None,
        "shortest_mean": _safe_mean(shortest_lens),
        "stage_histogram": stage_hist,
        "human_delta_mean": _safe_mean(deltas),
        "human_delta_median": _safe_median(deltas),
        "n_beats_human": beats_human,
        "n_with_delta": len(deltas),
        "wall_mean": _safe_mean(times),
        "wall_median": _safe_median(times),
        "wall_max": max(times) if times else None,
    }


def render_report(
    results: list[ScrambleResult],
    agg: dict[str, Any],
    config: dict[str, Any],
) -> str:
    """Render a markdown report from results + aggregates."""
    lines: list[str] = []
    lines.append("# FMC Analyzer Baseline Benchmark")
    lines.append("")
    lines.append("## Config")
    lines.append("")
    for k, v in config.items():
        lines.append(f"- **{k}**: `{v}`")
    lines.append("")

    lines.append("## Aggregate Results")
    lines.append("")
    n = agg["n"]
    lines.append(f"- **scrambles run**: {n}")
    lines.append(
        f"- **completed (no timeout/error)**: {agg['n_ok']} "
        f"({agg['n_ok'] / n:.1%})"
    )
    lines.append(f"- **timed out**: {agg['n_timeout']}")
    lines.append(f"- **errored**: {agg['n_error']}")
    lines.append("")
    lines.append(
        f"- **full-solve rate (top-1)**: {agg['n_full_solve']}/{n} "
        f"= **{agg['full_solve_rate']:.1%}**"
    )
    lines.append(
        f"- **full-solve rate (any candidate)**: {agg['n_any_full_solve']}/{n} "
        f"= **{agg['any_full_solve_rate']:.1%}**"
    )
    lines.append("")

    if agg["solve_mean"] is not None:
        lines.append("### Move counts on successful solves (top-1)")
        lines.append("")
        lines.append(f"- **mean**: {_fmt(agg['solve_mean'], '.1f')}")
        lines.append(f"- **median**: {_fmt(agg['solve_median'], '.1f')}")
        lines.append(f"- **min / max**: {agg['solve_min']} / {agg['solve_max']}")
        if agg["shortest_mean"] is not None:
            lines.append(
                f"- **shortest-among-candidates mean**: "
                f"{_fmt(agg['shortest_mean'], '.1f')}"
            )
        lines.append("")

    lines.append("### Stages reached (count of scrambles)")
    lines.append("")
    lines.append("| stages | n |")
    lines.append("|---|---|")
    for k in sorted(agg["stage_histogram"].keys()):
        lines.append(f"| {k} | {agg['stage_histogram'][k]} |")
    lines.append("")

    if agg["n_with_delta"]:
        lines.append("### Comparison to human reconstructions")
        lines.append("")
        lines.append(
            f"- **scrambles with full solve + human length**: "
            f"{agg['n_with_delta']}"
        )
        lines.append(
            f"- **beats human**: {agg['n_beats_human']}/{agg['n_with_delta']} "
            f"({agg['n_beats_human'] / agg['n_with_delta']:.1%})"
        )
        lines.append(
            f"- **mean delta (analyzer − human)**: "
            f"{_fmt(agg['human_delta_mean'], '+.1f')}"
        )
        lines.append(
            f"- **median delta**: {_fmt(agg['human_delta_median'], '+.1f')}"
        )
        lines.append("")

    lines.append("### Wall time")
    lines.append("")
    lines.append(f"- **mean**: {_fmt(agg['wall_mean'], '.1f')}s")
    lines.append(f"- **median**: {_fmt(agg['wall_median'], '.1f')}s")
    lines.append(f"- **max**: {_fmt(agg['wall_max'], '.1f')}s")
    lines.append("")

    lines.append("## Per-scramble Results")
    lines.append("")
    lines.append(
        "| # | id | human | stages | top-1 | shortest | full? | wall (s) | notes |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in results:
        stages_str = "→".join(_stage_summary(s) for s in r.stage_names) or "—"
        notes = ""
        if r.timed_out:
            notes = "TIMEOUT"
        elif r.error:
            notes = f"ERROR: {r.error[:60]}"
        lines.append(
            "| {idx} | `{sid}` | {hum} | {st} | {b1} | {sh} | {fs} | {wall} | {n} |".format(
                idx=r.index,
                sid=r.source_id[:24],
                hum=_format_human_length(r.human_length),
                st=stages_str,
                b1=_format_human_length(r.best_total_moves),
                sh=_format_human_length(r.shortest_full_solve),
                fs="✓" if r.full_solve else "✗",
                wall=f"{r.wall_elapsed:.1f}" if r.wall_elapsed else "—",
                n=notes,
            )
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/raw/wca.jsonl")
    ap.add_argument("--ckpt", default="checkpoints/policy_best.pt")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--time-budget", type=float, default=300.0,
                    help="Wall-clock budget per scramble in seconds.")
    ap.add_argument("--workers", type=int, default=1,
                    help="Number of parallel worker processes.")
    ap.add_argument("--device", default="cpu",
                    help="torch device for workers (cpu recommended for parallel).")
    ap.add_argument("--eo-beam", type=int, default=256)
    ap.add_argument("--eo-depth", type=int, default=10)
    ap.add_argument("--dr-beam", type=int, default=8192)
    ap.add_argument("--dr-depth", type=int, default=14)
    ap.add_argument("--no-niss", action="store_true",
                    help="Disable inverse-side & NISS hybrid search.")
    ap.add_argument("--report", default=None,
                    help="Optional path to write the markdown report.")
    ap.add_argument("--json-out", default=None,
                    help="Optional path to write raw per-scramble JSON.")
    args = ap.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        print(f"corpus not found: {corpus_path}", file=sys.stderr)
        return 2
    ckpt_path = Path(args.ckpt)
    if not ckpt_path.exists():
        print(f"checkpoint not found: {ckpt_path}", file=sys.stderr)
        return 2

    rows = _load_corpus(corpus_path, args.n, args.seed)
    print(f"loaded {len(rows)} scrambles from {corpus_path}")
    print(f"running with time_budget={args.time_budget}s, workers={args.workers}, "
          f"device={args.device}")
    print()

    jobs: list[tuple[int, dict]] = list(enumerate(rows))

    results: list[ScrambleResult] = [None] * len(jobs)  # type: ignore[list-item]

    # Bounded thread pool to drive subprocesses concurrently. Each "slot"
    # owns one subprocess at a time. Using threads in the parent to wait on
    # processes is fine because the heavy work happens in the children.
    from concurrent.futures import ThreadPoolExecutor, as_completed

    def _run_idx(idx: int, row: dict) -> ScrambleResult:
        scr = row["scramble"]
        sid = row.get("source_id", "?")
        human_len = row.get("length") or row.get("move_count")
        try:
            human_len = int(human_len) if human_len is not None else None
        except (TypeError, ValueError):
            human_len = None

        out, timed_out, wall = _run_one(
            scr, str(ckpt_path), args.device,
            args.eo_beam, args.eo_depth,
            args.dr_beam, args.dr_depth,
            args.time_budget,
            use_niss=not args.no_niss,
        )
        res = ScrambleResult(
            index=idx,
            scramble=scr,
            source_id=str(sid),
            human_length=human_len,
            wall_elapsed=wall,
        )
        if timed_out:
            res.timed_out = True
            print(f"[{idx:>3}] TIMEOUT after {wall:.1f}s  ({sid})")
        elif out is None:
            res.error = "worker exited without producing a result"
            print(f"[{idx:>3}] ERROR no result ({sid})")
        elif not out.get("ok"):
            res.error = out.get("error", "unknown")
            print(f"[{idx:>3}] ERROR {res.error}  ({sid})")
        else:
            res.ok = True
            res.stages_reached = out["stages_reached"]
            res.stage_names = out["stage_names"]
            res.best_total_moves = out["best_total_moves"]
            res.full_solve = out["full_solve"]
            res.any_full_solve = out["any_full_solve"]
            res.shortest_full_solve = out["shortest_full_solve"]
            res.n_candidates = out["n_candidates"]
            res.search_elapsed = out["search_elapsed"]
            res.total_elapsed = out["total_elapsed"]
            stages = "→".join(_stage_summary(s) for s in res.stage_names) or "—"
            full = "SOLVE" if res.full_solve else "partial"
            print(
                f"[{idx:>3}] {full:>7}  stages={stages:<14} "
                f"top1={str(res.best_total_moves):>4}  "
                f"human={str(res.human_length):>4}  "
                f"wall={wall:.1f}s  ({sid})"
            )
        return res

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {pool.submit(_run_idx, idx, row): idx for idx, row in jobs}
        for fut in as_completed(futs):
            idx = futs[fut]
            results[idx] = fut.result()

    print()
    agg = aggregate(results)
    config = {
        "corpus": str(corpus_path),
        "ckpt": str(ckpt_path),
        "n": args.n,
        "seed": args.seed,
        "time_budget_s": args.time_budget,
        "workers": args.workers,
        "device": args.device,
        "eo_beam": args.eo_beam,
        "eo_depth": args.eo_depth,
        "dr_beam": args.dr_beam,
        "dr_depth": args.dr_depth,
    }
    report = render_report(results, agg, config)
    print(report)

    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(report)
        print(f"\nwrote report -> {args.report}", file=sys.stderr)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps({
            "config": config,
            "aggregate": agg,
            "results": [asdict(r) for r in results],
        }, indent=2))
        print(f"wrote json -> {args.json_out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
