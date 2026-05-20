"""Per-scramble synthesis blog post.

Aggregates all attempts on a single scramble into one narrative .md
written like an FMC competitor's tournament report blog post: walks
through each draft, what was tried, where it went wrong, why the
chosen solution is what it is, what could have been done differently,
and how the result compares to the human-reference WCA solver.

Usage:
    python -m cube.agent.synthesize_scramble fm_PSSSideDayGdansk2026_s1 \\
        --out-dir runs/corpus_eval_v34 \\
        --corpus-333fm data/corpus_333fm.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import anthropic

DEFAULT_MODEL = "claude-opus-4-7"


def _load_attempts(out_dir: Path, scramble_id: str) -> list[dict]:
    """Return per-attempt records, sorted by attempt index."""
    attempts: list[dict] = []
    pattern = re.compile(rf"{re.escape(scramble_id)}__attempt(\d+)_\d+_\d+\.json$")
    for jpath in sorted(out_dir.glob(f"{scramble_id}__attempt*.json")):
        m = pattern.search(jpath.name)
        if not m:
            continue
        idx = int(m.group(1))
        try:
            data = json.loads(jpath.read_text())
        except json.JSONDecodeError:
            continue
        human_path = jpath.with_suffix(".human.md")
        narrative = human_path.read_text() if human_path.exists() else ""
        attempts.append({
            "index": idx,
            "json_path": str(jpath),
            "solves": data.get("solves"),
            "total_moves": data.get("total_moves"),
            "final_solution": data.get("final_solution") or [],
            "tool_calls": data.get("tool_calls"),
            "sim_spent": data.get("sim_spent"),
            "halt_reason": data.get("halt_reason"),
            "narrative": narrative,
        })
    attempts.sort(key=lambda a: a["index"])
    return attempts


def _load_human_reference(corpus_path: Path, scramble_id: str) -> dict | None:
    if not corpus_path or not corpus_path.exists():
        return None
    data = json.loads(corpus_path.read_text())
    for entry in data:
        if entry.get("id") == scramble_id:
            return entry
    return None


SYSTEM_PROMPT = """\
You are an FMC (Fewest Moves Challenge) competitor writing a tournament
report blog post about a single scramble. You attempted this scramble
multiple times within the WCA 1-hour budget; each attempt was its own
draft on paper.

Your job: write a coherent, readable blog post (~1200-2000 words) that
walks the reader through what happened across all your drafts. The
audience is other FMC competitors and serious cubers — use the
vocabulary (EO, DR, HTR, JZP, 3C2E, etc.) without over-explaining.

Structure:
1. Opening paragraph: scramble shown, the result you submitted, and the
   reference WCA solver's result for comparison.
2. Per-attempt section: one short section per attempt (no more than 4-5
   sentences each). What you tried (EO axis, DR family), what worked,
   what went wrong, why you abandoned it or moved on. Use actual moves
   from the transcripts when they illustrate the point.
3. "Why I chose attempt X" — explain what made the final solution win
   over the other drafts.
4. The winning solution walked through phase-by-phase: EO / DR / HTR /
   finish, with move groupings.
5. "What I'd do differently" — honest analysis of where the moves were
   lost relative to the reference solver. Cite the specific phase
   (probably DR or finish) and the specific call that cost moves.
6. A 1-sentence closer.

Tone: a real competitor's tournament report — analytical, self-critical,
specific. Not breathless, not robotic. Refer to yourself in first person.
Do not flatter the solve or use phrases like "interesting solution."
Don't repeat the scramble in every section. Don't include URLs.
Output ONLY the blog post markdown — no preamble, no JSON, no commentary.
"""


def _build_user_message(
    scramble_id: str,
    scramble: str,
    attempts: list[dict],
    human_ref: dict | None,
) -> str:
    lines = [
        f"## Scramble ID: {scramble_id}",
        f"## Scramble: {scramble}",
        f"## Scramble length: {len(scramble.split())} moves",
        "",
    ]
    if human_ref:
        lines += [
            "## Reference WCA solver",
            f"- Solver: {human_ref.get('solver', 'unknown')}",
            f"- Competition: {human_ref.get('competition', 'unknown')}",
            f"- Their solution ({human_ref.get('human_moves')} moves): "
            f"`{human_ref.get('human_solution', '')}`",
            f"- Their commentary:",
            "```",
            human_ref.get("human_comment", ""),
            "```",
            "",
        ]
    solved_attempts = [a for a in attempts if a.get("solves")]
    best = min(solved_attempts, key=lambda a: a["total_moves"], default=None)
    lines += [
        f"## Your attempts ({len(attempts)} drafts within 1-hour budget)",
        f"- Solved: {len(solved_attempts)} / {len(attempts)}",
        f"- Submitted solution (best of drafts): "
        + (f"attempt {best['index']}, {best['total_moves']} moves" if best else "all drafts failed"),
        "",
    ]
    if best and best.get("final_solution"):
        lines += [
            f"## Submitted solution: `{' '.join(best['final_solution'])}`",
            "",
        ]
    for a in attempts:
        outcome = (
            f"SOLVED in {a['total_moves']} moves"
            if a.get("solves") else f"FAILED ({a.get('halt_reason') or 'unknown'})"
        )
        lines += [
            f"---",
            f"### Attempt {a['index']}: {outcome}",
            f"- Tool calls: {a.get('tool_calls')}",
            f"- Sim time spent: {a.get('sim_spent')}s",
            f"- Final solution: `{' '.join(a.get('final_solution') or [])}`"
            if a.get("final_solution") else "- Final solution: (none — did not submit)",
            "",
            "Narrative transcript (human-style first-person from the solver):",
            "```",
            (a.get("narrative") or "(no narrative captured)")[:8000],
            "```",
            "",
        ]
    lines += [
        "---",
        "Now write the tournament-report blog post per the system prompt.",
    ]
    return "\n".join(lines)


def synthesize(
    scramble_id: str,
    out_dir: Path,
    *,
    corpus_path: Path | None = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 6000,
) -> Path:
    attempts = _load_attempts(out_dir, scramble_id)
    if not attempts:
        raise SystemExit(f"no attempts found for {scramble_id} in {out_dir}")
    human_ref = _load_human_reference(corpus_path, scramble_id) if corpus_path else None
    scramble = human_ref.get("scramble", "") if human_ref else ""
    if not scramble:
        # Fallback: pull from first attempt JSON.
        first = json.loads(Path(attempts[0]["json_path"]).read_text())
        sc = first.get("scramble") or []
        scramble = " ".join(sc) if isinstance(sc, list) else str(sc)

    user_msg = _build_user_message(scramble_id, scramble, attempts, human_ref)
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "\n".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    blog_path = out_dir / f"{scramble_id}__blog.md"
    blog_path.write_text(text + "\n")
    print(
        f"  [blog] {scramble_id} → {blog_path.name} "
        f"({len(text.split())} words, "
        f"{resp.usage.input_tokens}+{resp.usage.output_tokens} tokens)",
        flush=True,
    )
    return blog_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Synthesize a per-scramble blog post from all attempt narratives.",
    )
    parser.add_argument("scramble_id", help="e.g. fm_PSSSideDayGdansk2026_s1")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--corpus-333fm", type=Path, default=None,
                        help="JSON corpus with human reference solutions.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args(argv)

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2
    synthesize(
        args.scramble_id, args.out_dir,
        corpus_path=args.corpus_333fm, model=args.model,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
