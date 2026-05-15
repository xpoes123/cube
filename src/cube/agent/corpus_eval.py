"""Run sim mode on a list of scrambles sequentially.

Sequential, not parallel, on purpose: a single process shares the
_SUBSET_FINISH_CACHE across runs, so the second time we see the same
HTR subset the agent recalls instead of learning. This is the
"strong solver who has played a few competitions" warm-up.

Outputs:
  - runs/corpus_eval/<scramble_id>.json    raw transcript per scramble
  - runs/corpus_eval/<scramble_id>.md      rendered narrative per scramble
  - runs/corpus_eval/SUMMARY.md            aggregate results table
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from cube.agent import build_index, render_narrative, simulated_fmc

# 4 hand-picked scrambles from benchmarks/test_scrambles.md.
DEFAULT_CORPUS = [
    ("scramble1", "R' U' F L' R U2 F2 L2 R U2 L B2 R' U' L2 F L' U2 R F2 R B' R' U' F"),
    ("scramble2", "R' U' F B' U2 F' U2 R2 B' R2 B' R2 U2 R2 F' L U2 B D R F L2 F D' R' U' F"),
    ("scramble3", "R' U' F R2 B2 D2 R F2 L D2 B2 R B2 U2 R F' L D' B U B' R' F' D' R' U' F"),
    ("scramble5", "R' U' F R D' B2 R2 D' L2 D2 L2 B2 U2 F U' L B R' F U F D2 R' U' F"),
]

# Reference: heavy-compute analyzer's best on each (from test_scrambles.md).
ANALYZER_BASELINE = {
    "scramble1": 30,
    "scramble2": 25,
    "scramble3": 31,
    "scramble5": 33,
}


def run_one(scramble_id: str, scramble: str, *, model: str, out_dir: Path,
            wall_limit_s: float, max_tool_calls: int) -> dict:
    print(f"\n{'=' * 60}\n  {scramble_id}: {scramble}\n{'=' * 60}", flush=True)
    moves = scramble.split()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_path = out_dir / f"{scramble_id}_{ts}.json"
    t0 = time.time()
    result = simulated_fmc.solve(
        moves,
        model=model,
        max_tool_calls=max_tool_calls,
        verbose=False,
        thinking_budget=3000,
        transcript_path=transcript_path,
        wall_limit_s=wall_limit_s,
        sim_budget=3600.0,
    )
    elapsed = time.time() - t0

    with transcript_path.open("w") as f:
        json.dump(result, f, indent=2, default=str)

    # Render narrative alongside.
    narrative_path = transcript_path.with_suffix(".md")
    narrative_path.write_text(render_narrative.render(transcript_path))

    summary = {
        "id": scramble_id,
        "scramble": scramble,
        "solves": result["solves"],
        "total_moves": result["total_moves"],
        "tool_calls": result["tool_calls"],
        "sim_spent": result["sim_spent"],
        "wall_s": round(elapsed, 1),
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
        "halt_reason": result["halt_reason"],
        "solution": result["final_solution"],
        "transcript_path": str(transcript_path.relative_to(out_dir.parent.parent)),
        "narrative_path": str(narrative_path.relative_to(out_dir.parent.parent)),
    }
    print(f"\n  -> {summary['solves'] and f'SOLVED in {summary['total_moves']}m' or 'FAILED'} "
          f"({summary['tool_calls']} tool calls, {summary['sim_spent']:.0f}s sim, {elapsed:.0f}s wall)", flush=True)
    return summary


def write_summary(out_dir: Path, summaries: list[dict], model: str) -> Path:
    rows: list[str] = []
    rows.append("# Corpus eval — sim mode on 4 scrambles")
    rows.append("")
    rows.append(f"Model: `{model}`")
    rows.append(f"Run: {datetime.now().isoformat(timespec='seconds')}")
    rows.append("")
    rows.append("| ID | Result | Sim moves | Analyzer baseline | Gap | Tool calls | Sim time | Wall | Cost |")
    rows.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    total_in = total_out = 0
    solved = 0
    move_sum = 0
    base_sum = 0
    for s in summaries:
        baseline = ANALYZER_BASELINE.get(s["id"], "?")
        if s["solves"]:
            gap = s["total_moves"] - baseline if isinstance(baseline, int) else "?"
            move_sum += s["total_moves"]
            if isinstance(baseline, int):
                base_sum += baseline
            solved += 1
            status = "✓"
        else:
            gap = "—"
            status = "✗"
        total_in += s["input_tokens"]
        total_out += s["output_tokens"]
        # Sonnet pricing rough: $3/M in (cached close to $0.30), $15/M out.
        cost_est = s["input_tokens"] * 3 / 1_000_000 + s["output_tokens"] * 15 / 1_000_000
        rows.append(
            f"| {s['id']} | {status} | {s['total_moves'] if s['solves'] else '—'} | "
            f"{baseline} | {gap} | {s['tool_calls']} | {s['sim_spent']:.0f}s | "
            f"{s['wall_s']:.0f}s | ${cost_est:.2f} |"
        )
    rows.append("")
    rows.append(f"**Solved**: {solved}/{len(summaries)}")
    if solved:
        rows.append(f"**Avg sim moves (solved)**: {move_sum / solved:.1f}")
        rows.append(f"**Avg analyzer baseline (solved)**: {base_sum / solved:.1f}")
        rows.append(f"**Avg gap (solved)**: {(move_sum - base_sum) / solved:.1f}")
    total_cost = total_in * 3 / 1_000_000 + total_out * 15 / 1_000_000
    rows.append(f"**Total API cost (rough, no cache discount)**: ${total_cost:.2f}")
    rows.append("")
    rows.append("## Per-scramble narratives")
    for s in summaries:
        rows.append(f"- [{s['id']}]({Path(s['narrative_path']).name})")
    summary_path = out_dir / "SUMMARY.md"
    summary_path.write_text("\n".join(rows) + "\n")
    return summary_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run sim mode on a scramble corpus.")
    parser.add_argument("--model", default=simulated_fmc.DEFAULT_MODEL)
    parser.add_argument("--wall-limit-s", type=float, default=900.0)
    parser.add_argument("--max-tool-calls", type=int, default=50)
    parser.add_argument("--out-dir", type=Path, default=Path("runs/corpus_eval"))
    args = parser.parse_args(argv)

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict] = []
    for scramble_id, scramble in DEFAULT_CORPUS:
        try:
            summaries.append(run_one(
                scramble_id, scramble,
                model=args.model, out_dir=args.out_dir,
                wall_limit_s=args.wall_limit_s,
                max_tool_calls=args.max_tool_calls,
            ))
        except Exception as e:
            print(f"  !! {scramble_id} crashed: {type(e).__name__}: {e}", flush=True)
            summaries.append({
                "id": scramble_id, "scramble": scramble,
                "solves": False, "total_moves": 0, "tool_calls": 0,
                "sim_spent": 0, "wall_s": 0,
                "input_tokens": 0, "output_tokens": 0,
                "halt_reason": f"crash: {type(e).__name__}", "solution": [],
                "transcript_path": "", "narrative_path": "",
            })

    summary_path = write_summary(args.out_dir, summaries, args.model)
    print(f"\nwrote {summary_path}")
    # Regenerate the top-level runs index so new transcripts surface immediately.
    try:
        runs_root = args.out_dir if args.out_dir.parent.name == "runs" else args.out_dir.parent
        if runs_root.name == "runs":
            idx_md = build_index.build(runs_root)
            (runs_root / "INDEX.md").write_text(idx_md)
            print(f"refreshed {runs_root / 'INDEX.md'}")
    except Exception as e:
        print(f"warn: could not regenerate INDEX.md ({e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
