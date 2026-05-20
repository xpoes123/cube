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
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from cube.agent import build_index, human_narrative, render_narrative, scramble_gen, simulated_fmc


def _git_push_scramble(scramble_id: str, summary: dict, out_dir: Path) -> None:
    """v34: commit + push after each scramble so the user can follow live.

    Soft-failing: any git error just prints a warning. Skipped when not
    in a git repo or when no remote is configured.
    """
    repo_root = Path(__file__).resolve().parents[3]
    if not (repo_root / ".git").exists():
        return
    # out_dir may be relative (from CLI) or absolute. Resolve, then make
    # it relative to repo_root so `git add` works from cwd=repo_root.
    try:
        out_rel = str(out_dir.resolve().relative_to(repo_root))
    except ValueError:
        return  # out_dir is outside the repo; don't try to commit it
    moves_str = "FAIL" if not summary.get("solves") else f"{summary.get('total_moves')}mv"
    tag = out_dir.name
    msg_lines = [
        f"{tag} live: {scramble_id} → {moves_str}",
        "",
        f"sim_spent: {summary.get('sim_spent', 0):.0f}s",
        f"tool_calls: {summary.get('tool_calls', 0)}",
        f"halt_reason: {summary.get('halt_reason') or 'completed'}",
    ]
    msg = "\n".join(msg_lines)

    def _run(args: list[str]) -> tuple[int, str]:
        proc = subprocess.run(
            args, cwd=repo_root,
            capture_output=True, text=True, check=False,
        )
        return proc.returncode, (proc.stdout + proc.stderr).strip()

    rc, _ = _run(["git", "add", out_rel])
    if rc != 0:
        return
    rc, out = _run(["git", "diff", "--cached", "--quiet"])
    if rc == 0:
        return  # nothing staged
    rc, out = _run(["git", "commit", "-m", msg])
    if rc != 0:
        print(f"  warn: git commit failed: {out[:200]}", flush=True)
        return
    rc, out = _run(["git", "push"])
    if rc != 0:
        print(f"  warn: git push failed: {out[:200]}", flush=True)
        return
    print(f"  [pushed] {scramble_id} → {moves_str}", flush=True)

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


def build_corpus(extra: int = 0, seed: int = 100) -> list[tuple[str, str]]:
    """Default 4 + optional N freshly-generated WCA-style scrambles."""
    out = list(DEFAULT_CORPUS)
    for i in range(extra):
        gen = scramble_gen.make_scramble(seed=seed + i)
        out.append((f"random{i+1}", " ".join(gen)))
    return out


def load_333fm_corpus(path: Path) -> tuple[list[tuple[str, str]], dict[str, dict]]:
    """Load a 333.fm corpus JSON (produced by `cube.agent.fetch_333fm_corpus`).

    Returns (corpus, metadata) where corpus is the list of (id, scramble) pairs
    and metadata maps id → {human_solution, human_moves, human_comment, solver,
    competition} for the per-scramble summary.
    """
    data = json.loads(path.read_text())
    corpus = [(entry["id"], entry["scramble"]) for entry in data]
    metadata = {entry["id"]: {
        "human_solution": entry["human_solution"],
        "human_moves": entry["human_moves"],
        "human_comment": entry["human_comment"],
        "solver": entry["solver"],
        "competition": entry["competition"],
    } for entry in data}
    return corpus, metadata


def run_one(scramble_id: str, scramble: str, *, model: str, out_dir: Path,
            wall_limit_s: float, max_tool_calls: int, n_best: int = 1,
            scramble_sim_budget: float = 3600.0,
            min_attempt_budget_s: float = 120.0) -> dict:
    """v34: --n-best N attempts SHARE the WCA 1-hour budget.

    Prior versions gave each attempt a fresh 3600s, so n_best=8 meant
    8 hours of simulated thinking per scramble — not WCA-realistic.
    Now: every attempt deducts from a single `scramble_sim_budget`
    pool (default 3600s). The next attempt starts with whatever's left.
    We stop launching new attempts when remaining < min_attempt_budget_s.
    """
    if n_best > 1:
        best: dict | None = None
        prior_attempts: list[dict] = []
        cumulative_sim_spent = 0.0
        for attempt in range(n_best):
            remaining_budget = scramble_sim_budget - cumulative_sim_spent
            if remaining_budget < min_attempt_budget_s:
                print(
                    f"\n  [budget exhausted] {cumulative_sim_spent:.0f}s "
                    f"of {scramble_sim_budget:.0f}s used after {attempt} "
                    f"attempts; remaining {remaining_budget:.0f}s < "
                    f"{min_attempt_budget_s:.0f}s — stopping early.",
                    flush=True,
                )
                break
            single = _run_single(
                f"{scramble_id}__attempt{attempt+1}",
                scramble,
                model=model, out_dir=out_dir,
                wall_limit_s=wall_limit_s,
                max_tool_calls=max_tool_calls,
                prior_attempts=prior_attempts if prior_attempts else None,
                sim_budget=remaining_budget,
            )
            cumulative_sim_spent += float(single.get("sim_spent") or 0.0)
            prior_attempts.append({
                "solves": single["solves"],
                "total_moves": single.get("total_moves"),
                "final_solution": (single.get("solution") or "").split() if isinstance(single.get("solution"), str) else single.get("solution") or [],
                "halt_reason": single.get("halt_reason"),
            })
            if best is None:
                best = single
            elif single["solves"] and not best["solves"]:
                best = single
            elif single["solves"] and best["solves"] and single["total_moves"] < best["total_moves"]:
                best = single
        assert best is not None
        best["id"] = scramble_id
        best["n_best_attempts"] = n_best
        best["scramble_sim_spent_total"] = round(cumulative_sim_spent, 1)
        best["scramble_sim_budget"] = scramble_sim_budget
        status_str = (
            f"SOLVED in {best['total_moves']}m" if best["solves"] else "all attempts FAILED"
        )
        print(
            f"\n  -> [n_best={n_best}, shared {scramble_sim_budget:.0f}s] "
            f"BEST: {status_str}  (used {cumulative_sim_spent:.0f}s across "
            f"{len(prior_attempts)} attempts)",
            flush=True,
        )
        return best
    return _run_single(scramble_id, scramble, model=model, out_dir=out_dir,
                       wall_limit_s=wall_limit_s, max_tool_calls=max_tool_calls,
                       sim_budget=scramble_sim_budget)


def _run_single(scramble_id: str, scramble: str, *, model: str, out_dir: Path,
                wall_limit_s: float, max_tool_calls: int,
                prior_attempts: list[dict] | None = None,
                sim_budget: float = 3600.0) -> dict:
    print(f"\n{'=' * 60}\n  {scramble_id}: {scramble}  (sim_budget={sim_budget:.0f}s)\n{'=' * 60}", flush=True)
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
        sim_budget=sim_budget,
        prior_attempts=prior_attempts,
    )
    elapsed = time.time() - t0

    with transcript_path.open("w") as f:
        json.dump(result, f, indent=2, default=str)

    # Render narrative alongside.
    narrative_path = transcript_path.with_suffix(".md")
    narrative_path.write_text(render_narrative.render(transcript_path))
    # v23c: also emit the human-narrative version (NLP translation of tool calls).
    human_path = transcript_path.with_suffix(".human.md")
    try:
        human_path.write_text(human_narrative.render(transcript_path))
    except Exception:
        pass  # human narrative is best-effort; fall back silently

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


def write_summary(
    out_dir: Path, summaries: list[dict], model: str,
    human_meta: dict[str, dict] | None = None,
    version_notes: str | None = None,
) -> Path:
    rows: list[str] = []
    version_label = out_dir.name.replace("corpus_eval_", "")
    rows.append(f"# Corpus eval — `{version_label}`")
    rows.append("")
    rows.append(f"- **Model**: `{model}`")
    rows.append(f"- **Run**: {datetime.now().isoformat(timespec='seconds')}")
    rows.append(f"- **Scrambles**: {len(summaries)}")
    rows.append("")
    if version_notes:
        rows.append("## What changed in this version")
        rows.append("")
        rows.append(version_notes.strip())
        rows.append("")
    if human_meta:
        rows.append("| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |")
        rows.append("|---|---|---:|---:|---:|---|---:|---:|---:|---:|")
    else:
        rows.append("| ID | Result | Sim moves | Analyzer baseline | Gap | Tool calls | Sim time | Wall | Cost |")
        rows.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    total_in = total_out = 0
    solved = 0
    move_sum = 0
    base_sum = 0
    for s in summaries:
        if human_meta and s["id"] in human_meta:
            baseline = human_meta[s["id"]]["human_moves"]
            solver = human_meta[s["id"]]["solver"]
        else:
            baseline = ANALYZER_BASELINE.get(s["id"], "?")
            solver = None
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
        cost_est = s["input_tokens"] * 3 / 1_000_000 + s["output_tokens"] * 15 / 1_000_000
        if human_meta:
            rows.append(
                f"| {s['id']} | {status} | {s['total_moves'] if s['solves'] else '—'} | "
                f"{baseline} | {gap} | {solver or '—'} | {s['tool_calls']} | {s['sim_spent']:.0f}s | "
                f"{s['wall_s']:.0f}s | ${cost_est:.2f} |"
            )
        else:
            rows.append(
                f"| {s['id']} | {status} | {s['total_moves'] if s['solves'] else '—'} | "
                f"{baseline} | {gap} | {s['tool_calls']} | {s['sim_spent']:.0f}s | "
                f"{s['wall_s']:.0f}s | ${cost_est:.2f} |"
            )
    rows.append("")
    rows.append(f"**Solved**: {solved}/{len(summaries)}")
    if solved:
        rows.append(f"**Avg sim moves (solved)**: {move_sum / solved:.1f}")
        label = "human (WCA)" if human_meta else "analyzer baseline"
        rows.append(f"**Avg {label} (solved)**: {base_sum / solved:.1f}")
        rows.append(f"**Avg gap (solved)**: {(move_sum - base_sum) / solved:+.1f}")
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
    parser.add_argument("--extra-random", type=int, default=0,
                        help="Append N freshly-generated WCA-style scrambles to the default 4.")
    parser.add_argument("--random-seed", type=int, default=100,
                        help="Base seed for generated scrambles (each uses seed+i).")
    parser.add_argument("--corpus-333fm", type=Path, default=None,
                        help="If set, load scrambles from this 333.fm JSON (produced "
                             "by cube.agent.fetch_333fm_corpus) instead of the default + random corpus. "
                             "Summary will include human-solver baselines per scramble.")
    parser.add_argument("--n-best", type=int, default=8,
                        help="v19: run each scramble N times and report the best solve. "
                             "Default 8 (bumped from 4 in v28). With cross-attempt memory, "
                             "attempts 5-8 see all prior failures and can refine. Cost scales linearly.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Cap number of scrambles evaluated (after corpus load). "
                             "Useful when n_best>1 already burns cycles per scramble.")
    parser.add_argument("--version-notes", type=str, default=None,
                        help="One-paragraph 'what changed in this version' for the SUMMARY.md header.")
    args = parser.parse_args(argv)

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    human_meta: dict[str, dict] | None = None
    if args.corpus_333fm:
        corpus, human_meta = load_333fm_corpus(args.corpus_333fm)
    else:
        corpus = build_corpus(extra=args.extra_random, seed=args.random_seed)
    if args.limit is not None:
        corpus = corpus[:args.limit]
    summaries: list[dict] = []
    for scramble_id, scramble in corpus:
        try:
            summaries.append(run_one(
                scramble_id, scramble,
                model=args.model, out_dir=args.out_dir,
                wall_limit_s=args.wall_limit_s,
                max_tool_calls=args.max_tool_calls,
                n_best=args.n_best,
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
        # Per-scramble live update: write incremental SUMMARY.md, then
        # commit + push so the user can watch progress in the repo.
        try:
            write_summary(
                args.out_dir, summaries, args.model,
                human_meta=human_meta, version_notes=args.version_notes,
            )
            _git_push_scramble(scramble_id, summaries[-1], args.out_dir)
        except Exception as e:
            print(f"  warn: live push failed for {scramble_id}: {type(e).__name__}: {e}", flush=True)

    summary_path = write_summary(
        args.out_dir, summaries, args.model,
        human_meta=human_meta, version_notes=args.version_notes,
    )
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
