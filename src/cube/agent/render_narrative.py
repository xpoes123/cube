"""Render a sim/loop transcript JSON into clean readable markdown.

Strips out tool RESULTS (which are giant) and surfaces only:
  - the system prompt (one collapsed block)
  - per-turn: the model's thinking blocks, text narration, tool names + inputs
  - per-tool: a one-line summary of the result (length, found, error, etc.)
  - final solution + verification + cost/budget stats

The goal is "what was Claude actually thinking" — the video-ready trace.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _block_text(block: dict) -> str:
    """Pull plain text out of an assistant content block dict."""
    if block.get("type") == "text":
        return block.get("text", "")
    if block.get("type") == "thinking":
        return block.get("thinking", "") or ""
    return ""


def _summarize_tool_result(name: str, result: dict) -> str:
    """One-line summary of a tool result. Lists are collapsed to counts."""
    if not isinstance(result, dict):
        return repr(result)[:200]
    if "error" in result:
        return f"ERROR: {result['error']}"
    pieces: list[str] = []
    if "is_solved" in result and result["is_solved"]:
        pieces.append("SOLVED")
    if "eo_solved_axes" in result:
        pieces.append(f"EO: {result['eo_solved_axes']}")
    if "dr_solved_axes" in result:
        pieces.append(f"DR: {result['dr_solved_axes']}")
    if "bad_edges_per_axis" in result:
        pieces.append(f"bad_edges {result['bad_edges_per_axis']}")
    if "found" in result:
        pieces.append(f"found={result['found']}")
        if result.get("options"):
            best = result["options"][0]
            pieces.append(f"best={best.get('length')}m")
    if "subset_canonical" in result:
        pieces.append(f"subset={result['subset_canonical']}")
    if "finish_moves" in result:
        pieces.append(f"finish={len(result['finish_moves'])}m")
        if "memory_quality" in result:
            pieces.append(f"({result['memory_quality']})")
    if "history" in result and isinstance(result["history"], list):
        pieces.append(f"hist={len(result['history'])}m")
    if "sim_spent" in result:
        pieces.append(f"sim={result['sim_spent']:.0f}s")
    if "solves" in result:
        pieces.append(f"solves={result['solves']}")
    if "total_moves" in result:
        pieces.append(f"moves={result['total_moves']}")
    if "cancelled_length" in result:
        pieces.append(f"cancelled {result['input_length']}->{result['cancelled_length']}")
    return ", ".join(pieces) if pieces else "(empty result)"


def render(transcript_json_path: Path, *, include_system: bool = False) -> str:
    with transcript_json_path.open() as f:
        data = json.load(f)

    lines: list[str] = []
    scramble = data.get("scramble") or []
    model = data.get("model", "?")
    solves = data.get("solves", False)
    total_moves = data.get("total_moves", 0)
    tool_calls = data.get("tool_calls", 0)
    sim_spent = data.get("sim_spent")
    sim_budget = data.get("sim_budget")
    halt = data.get("halt_reason")
    in_tok = data.get("input_tokens", 0)
    out_tok = data.get("output_tokens", 0)

    lines.append(f"# Run — {transcript_json_path.name}")
    lines.append("")
    lines.append(f"**Scramble**: `{' '.join(scramble)}`  ")
    lines.append(f"**Model**: `{model}`  ")
    status = "✓ SOLVED" if solves else "✗ failed"
    lines.append(f"**Result**: {status} ({total_moves} moves, {tool_calls} tool calls)  ")
    if sim_spent is not None:
        lines.append(f"**Sim budget**: {sim_spent:.0f}s / {sim_budget:.0f}s  ")
    if halt:
        lines.append(f"**Halt**: {halt}  ")
    lines.append(f"**Tokens**: {in_tok:,} in, {out_tok:,} out  ")
    if data.get("final_solution"):
        lines.append(f"**Solution**: `{' '.join(data['final_solution'])}`  ")
    lines.append("")
    lines.append("---")
    lines.append("")

    if include_system and data.get("transcript"):
        for entry in data["transcript"]:
            if entry.get("type") == "system":
                lines.append("<details><summary>System prompt</summary>\n")
                lines.append("```\n" + entry["content"] + "\n```\n")
                lines.append("</details>\n")
                break

    # Walk the transcript. Two interleaved patterns:
    #   assistant entries hold lists of content blocks
    #   tool_call entries hold one tool invocation each
    turn_idx = 0
    tool_counter = 0
    for entry in data.get("transcript", []):
        kind = entry.get("type")
        if kind == "user" and isinstance(entry.get("content"), str):
            txt = entry["content"]
            if txt.startswith("Solve this scramble"):
                continue  # first user message — already in header
            lines.append(f"> **user**: {txt[:200]}")
            lines.append("")
        elif kind == "assistant":
            turn_idx += 1
            blocks = entry.get("content", [])
            for block in blocks:
                btype = block.get("type")
                if btype == "thinking":
                    text = block.get("thinking", "") or ""
                    if text.strip():
                        lines.append(f"### Turn {turn_idx} — thinking")
                        lines.append("")
                        lines.append("> " + text.replace("\n", "\n> "))
                        lines.append("")
                elif btype == "text":
                    text = block.get("text", "")
                    if text.strip():
                        lines.append(f"**Turn {turn_idx} narration**:")
                        lines.append("")
                        lines.append(text.strip())
                        lines.append("")
                elif btype == "tool_use":
                    # Tool name + input shown here; the matching tool_call entry
                    # later carries the result, so wait to print until then.
                    pass
        elif kind == "tool_call":
            tool_counter += 1
            name = entry.get("name", "?")
            tool_input = entry.get("input", {})
            input_repr = json.dumps(tool_input, separators=(",", ":"))
            if len(input_repr) > 120:
                input_repr = input_repr[:117] + "..."
            summary = _summarize_tool_result(name, entry.get("result", {}))
            sim = entry.get("sim_spent")
            sim_str = f" [sim={sim:.0f}s]" if sim is not None else ""
            lines.append(f"- `tool#{tool_counter}` **{name}**({input_repr}){sim_str}")
            lines.append(f"  → {summary}")
        elif kind == "verify":
            sol = entry.get("solution", [])
            res = entry.get("result", {})
            ok = "✓" if res.get("solves") else "✗"
            lines.append("")
            lines.append(f"**verify_solved** {ok} — {res.get('total_moves')} moves: `{' '.join(sol)}`")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a sim/loop transcript JSON to readable markdown.")
    parser.add_argument("transcript", help="Path to runs/*_NNNN.json")
    parser.add_argument("-o", "--output", help="Output .md path (default: same name, .md extension)")
    parser.add_argument("--system", action="store_true", help="Include system prompt collapsed")
    args = parser.parse_args(argv)

    src = Path(args.transcript)
    if not src.exists():
        print(f"error: not found: {src}", file=sys.stderr)
        return 1
    md = render(src, include_system=args.system)
    if args.output:
        dst = Path(args.output)
    else:
        dst = src.with_suffix(".narrative.md")
    dst.write_text(md)
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
