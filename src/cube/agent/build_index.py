"""Build runs/INDEX.md from every transcript JSON in runs/.

Lists every sim and unconstrained run with: result, moves, tool calls,
sim time, real wall, token / cost breakdown, and links to the narrative
markdown alongside.

Run after each new transcript drops; called by corpus_eval too.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _safe_load(p: Path) -> dict | None:
    try:
        with p.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _cost(data: dict) -> float:
    # Prefer the recorded estimate if present; else compute.
    if "cost_estimate_usd" in data:
        return float(data["cost_estimate_usd"])
    cached = data.get("cache_read_tokens", 0)
    inp = data.get("input_tokens", 0)
    out = data.get("output_tokens", 0)
    fresh = inp - cached
    return (cached * 0.30 + fresh * 3.0 + out * 15.0) / 1_000_000


def _scramble_id(p: Path, data: dict) -> str:
    # Look for a parent dir like corpus_eval_v4 and a name like scramble1_...
    stem = p.stem
    if stem.startswith("scramble"):
        sid = stem.split("_")[0]
    else:
        sid = stem
    return sid


def _row(p: Path) -> str | None:
    data = _safe_load(p)
    if data is None or "scramble" not in data:
        return None
    solves = data.get("solves", False)
    moves = data.get("total_moves", 0)
    tool_calls = data.get("tool_calls", 0)
    sim_spent = data.get("sim_spent")
    wall_s = data.get("wall_elapsed_s")
    halt = data.get("halt_reason") or ""
    in_tok = data.get("input_tokens", 0)
    out_tok = data.get("output_tokens", 0)
    cache_read = data.get("cache_read_tokens", 0)
    cost = _cost(data)
    rel = p.relative_to(p.parents[1] if p.parents[1].name == "runs" else p.parent.parent)
    narrative = p.with_suffix(".md")
    narrative_link = narrative.name if narrative.exists() else "—"
    sid = _scramble_id(p, data)
    parent = p.parent.name
    status = "✓" if solves else "✗"
    return (
        f"| {parent} | {sid} | {status} | {moves if solves else '—'} | {tool_calls} | "
        f"{f'{sim_spent:.0f}s' if sim_spent is not None else '—'} | "
        f"{f'{wall_s:.0f}s' if wall_s is not None else '—'} | "
        f"{in_tok:,} | {out_tok:,} | {cache_read:,} | ${cost:.3f} | "
        f"{halt} | [json]({rel}) [md]({rel.parent / narrative_link if narrative_link != '—' else '—'}) |"
    )


def build(runs_dir: Path) -> str:
    rows: list[str] = []
    json_paths = sorted(runs_dir.rglob("*.json"))
    # Exclude any non-transcript-looking files
    json_paths = [p for p in json_paths if "scramble" in p.name or "sim_" in p.name or "agent_" in p.name]
    for p in json_paths:
        r = _row(p)
        if r:
            rows.append(r)

    lines: list[str] = []
    lines.append("# Runs index")
    lines.append("")
    lines.append("Every transcript in `runs/` with key stats. Auto-generated.")
    lines.append("")
    lines.append("| Dir | Scramble | Result | Moves | Tools | Sim time | Wall | In-tok | Out-tok | Cache | Cost (est.) | Halt | Links |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    lines.extend(rows)
    lines.append("")
    lines.append(f"**Total transcripts**: {len(rows)}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate runs/INDEX.md from transcript JSONs.")
    parser.add_argument("--runs-dir", type=Path, default=Path("runs"))
    parser.add_argument("--output", type=Path, default=Path("runs/INDEX.md"))
    args = parser.parse_args(argv)
    md = build(args.runs_dir)
    args.output.write_text(md)
    print(f"wrote {args.output} with {md.count(chr(10))} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
