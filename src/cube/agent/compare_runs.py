"""Compare two run transcripts side-by-side.

Useful for showing "same scramble, different version: here's what changed."
Renders a markdown table of key stats + a turn-by-turn diff of tool calls.

Usage:
  python -m cube.agent.compare_runs <left.json> <right.json> [-o out.md]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _load(p: Path) -> dict:
    with p.open() as f:
        return json.load(f)


def _stats(d: dict) -> dict:
    return {
        "solves": d.get("solves", False),
        "total_moves": d.get("total_moves", 0),
        "tool_calls": d.get("tool_calls", 0),
        "sim_spent": d.get("sim_spent"),
        "wall": d.get("wall_elapsed_s"),
        "in_tok": d.get("input_tokens", 0),
        "out_tok": d.get("output_tokens", 0),
        "cache": d.get("cache_read_tokens", 0),
        "cost": d.get("cost_estimate_usd"),
        "halt": d.get("halt_reason") or "—",
        "solution": " ".join(d.get("final_solution", []) or []),
    }


def _tool_call_seq(d: dict) -> list[tuple[str, str]]:
    """Return [(tool_name, input_repr), ...] for the run."""
    out = []
    for entry in d.get("transcript", []):
        if entry.get("type") == "tool_call":
            inp = json.dumps(entry.get("input", {}), separators=(",", ":"))
            if len(inp) > 80:
                inp = inp[:77] + "..."
            out.append((entry.get("name", "?"), inp))
    return out


def render(left_path: Path, right_path: Path) -> str:
    left = _load(left_path)
    right = _load(right_path)
    ls = _stats(left)
    rs = _stats(right)

    lines: list[str] = []
    lines.append(f"# Compare — `{left_path.name}` vs `{right_path.name}`")
    lines.append("")
    lines.append("**Scramble**:")
    lines.append(f"`{' '.join(left.get('scramble', []))}`")
    lines.append("")
    lines.append("| Metric | Left | Right |")
    lines.append("|---|---|---|")
    lines.append(f"| Result | {'✓' if ls['solves'] else '✗'} | {'✓' if rs['solves'] else '✗'} |")
    lines.append(f"| Moves | {ls['total_moves'] or '—'} | {rs['total_moves'] or '—'} |")
    lines.append(f"| Tool calls | {ls['tool_calls']} | {rs['tool_calls']} |")
    if ls["sim_spent"] is not None or rs["sim_spent"] is not None:
        lines.append(f"| Sim time | {ls['sim_spent']:.0f}s | {rs['sim_spent']:.0f}s |"
                     if ls['sim_spent'] is not None and rs['sim_spent'] is not None else
                     f"| Sim time | {ls['sim_spent']} | {rs['sim_spent']} |")
    if ls["wall"] is not None or rs["wall"] is not None:
        lines.append(f"| Wall | {ls['wall']:.0f}s | {rs['wall']:.0f}s |"
                     if ls['wall'] is not None and rs['wall'] is not None else
                     f"| Wall | {ls['wall']} | {rs['wall']} |")
    lines.append(f"| Input tokens | {ls['in_tok']:,} | {rs['in_tok']:,} |")
    lines.append(f"| Cached tokens | {ls['cache']:,} | {rs['cache']:,} |")
    lines.append(f"| Output tokens | {ls['out_tok']:,} | {rs['out_tok']:,} |")
    if ls["cost"] is not None or rs["cost"] is not None:
        lc = f"${ls['cost']:.3f}" if ls['cost'] is not None else "—"
        rc = f"${rs['cost']:.3f}" if rs['cost'] is not None else "—"
        lines.append(f"| Cost (est.) | {lc} | {rc} |")
    lines.append(f"| Halt | {ls['halt']} | {rs['halt']} |")
    lines.append("")
    if ls["solution"]:
        lines.append(f"**Left solution** ({ls['total_moves']}m): `{ls['solution']}`  ")
    if rs["solution"]:
        lines.append(f"**Right solution** ({rs['total_moves']}m): `{rs['solution']}`")
    lines.append("")

    # Tool call sequence diff.
    lts = _tool_call_seq(left)
    rts = _tool_call_seq(right)
    lines.append("## Tool-call sequences")
    lines.append("")
    lines.append(f"Left: {len(lts)} calls — `{', '.join(t[0] for t in lts[:30])}`{'...' if len(lts) > 30 else ''}")
    lines.append("")
    lines.append(f"Right: {len(rts)} calls — `{', '.join(t[0] for t in rts[:30])}`{'...' if len(rts) > 30 else ''}")
    lines.append("")

    # First divergence point (in the sequence of tool names).
    div = None
    for i, (lt, rt) in enumerate(zip(lts, rts)):
        if lt[0] != rt[0]:
            div = i
            break
    if div is None:
        if len(lts) != len(rts):
            div = min(len(lts), len(rts))
    if div is not None:
        lines.append(f"**Divergence at tool #{div + 1}** (1-indexed):")
        if div < len(lts):
            lines.append(f"- Left:  `{lts[div][0]}({lts[div][1]})`")
        if div < len(rts):
            lines.append(f"- Right: `{rts[div][0]}({rts[div][1]})`")
    else:
        lines.append("**Tool-call sequences identical (by name).**")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("left")
    p.add_argument("right")
    p.add_argument("-o", "--output")
    args = p.parse_args(argv)
    md = render(Path(args.left), Path(args.right))
    if args.output:
        Path(args.output).write_text(md)
        print(f"wrote {args.output}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
