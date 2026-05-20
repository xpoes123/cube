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


def _load_nissy_axis_locked(scramble: str) -> dict | None:
    """Run nissy's eoud→drud→htr-drud→htrfin pipeline (UD axis-locked).

    Useful as a "what's the DR-pipeline ceiling on this axis if every
    phase is optimal" anchor. Returns None if nissy isn't installed.
    """
    try:
        from cube.tools.nissy_oracle import full_pipeline
    except Exception:
        return None
    try:
        data = full_pipeline(scramble.split(), n_solutions=1, timeout_s=90.0)
    except Exception:
        return None
    if not data:
        return None
    phases = []
    total = 0
    for d in data:
        phases.append({
            "phase": d.step_name,
            "length": d.optimal_length,
            "moves": list(d.chosen_optimal),
        })
        total += d.optimal_length
    return {
        "axis": "UD",
        "total": total,
        "phases": phases,
    }


def _load_prior_versions(scramble_id: str, current_out_dir: Path) -> list[dict]:
    """Scan sibling runs/corpus_eval_v*/ dirs for prior best solutions.

    For each prior version dir, picks the lowest-move-count solved attempt
    for this scramble_id. Returns list sorted by version label.
    """
    runs_root = current_out_dir.parent
    if not runs_root.exists():
        return []
    prior: list[dict] = []
    for d in sorted(runs_root.glob("corpus_eval_v*")):
        if d == current_out_dir or not d.is_dir():
            continue
        best: dict | None = None
        for jpath in d.glob(f"{scramble_id}__attempt*.json"):
            try:
                data = json.loads(jpath.read_text())
            except json.JSONDecodeError:
                continue
            if not data.get("solves"):
                continue
            tm = data.get("total_moves") or 9999
            if best is None or tm < best["total_moves"]:
                best = {
                    "version": d.name.replace("corpus_eval_", ""),
                    "total_moves": tm,
                    "final_solution": data.get("final_solution") or [],
                    "tool_calls": data.get("tool_calls"),
                }
        if best is not None:
            prior.append(best)
    return prior


SYSTEM_PROMPT = """\
You are an FMC competitor writing a deep technical retrospective on a
single scramble. The audience is top-level FMC solvers — they should
be able to read your retrospective and reconstruct EXACTLY what the
solver was trying to do at every decision point. Use the vocabulary
(EO, DR, HTR, JZP, XCYE substates, NISS, etc.) without over-explaining;
this is for cubers, not a general audience.

You are writing in first person as the solver who produced the drafts
below. You have access to:
- The full session's drafts (each attempt is one draft within your
  1-hour budget on paper).
- The reference WCA solver's submitted solution and their commentary.
- Nissy's optimal axis-locked solution (the "DR-pipeline ceiling" if
  you had perfect EO/DR/HTR/finish phase optimization).
- Your prior LLM-version attempts on this same scramble (if any).

Required structure:

1. **Header** — scramble shown verbatim, your submitted move count,
   the WCA reference move count, and nissy's axis-locked total. One
   sentence framing where the move-count gap came from.

2. **Initial scout** — what you saw on inspect_state: bad-edge counts
   per axis, which axes looked promising, which you considered NISS-ing.

3. **Draft-by-draft walkthrough**. For EACH draft, in order, include:
   - **Draft header**: the result (`SOLVED in Xmv` or `FAILED reason`),
     sim-time spent.
   - **Phase-by-phase verbatim moves**, with running move counts and
     what each phase accomplished. Format like:
     - EO (4): `R2 D' B' F'` — UD axis, kills all 8 bad edges
     - DR (8): `U' R' L2 U F2 R U2 R'` — DR-4C2E trigger, lands at
       UD-DR with 4qt corners remaining
     - HTR reduction (10): `U F2 U' R2 U L2 U2 R2 F2 U'` — 0-swap
       long-cycle subset
     - Half-turn finish (8): `B2 F2 L2 B2 L2 U2 B2 R2`
   - **What I was thinking** during that draft: which axis I picked
     and WHY, which substate, why I rejected alternatives, which tools
     I called and what they told me. Quote specific tool outputs when
     they drove a decision (e.g. "dr_trigger_options returned 7C8E
     in 7 — I weighed it vs the 2C4E in 8 and picked..."). Cite
     turn-by-turn reasoning so a top solver can follow your logic.
   - **Where this draft fell short** (if it lost vs the winning draft):
     specifically which phase leaked moves vs the reference.

4. **Winning-draft analysis** — single dedicated section. Walk through
   the submitted solution one more time at the deepest level: what
   made each phase choice good, what alternatives existed in the
   neighborhood, what the cancellation savings were if any.

5. **Three-way comparison** at the end:
   - vs Marcin (WCA reference): where they won, why. Cite their
     specific phase decomposition from their commentary if available.
     If they used 2c3+2e direct solve, JZP, or skipped a phase, say so.
   - vs nissy axis-locked: how much was the LLM's axis/NISS choice
     worth on its own? If nissy on the same axis is 35mv and we got
     30, NISS+axis pick was worth 5. If we got 30 and nissy is 28,
     we leaked 2 moves to suboptimal phase execution.
   - vs prior LLM version (if listed): same scramble, prior version's
     best — did the changes since then help or hurt? Quote the prior
     submitted solution if it differs meaningfully.

6. **What I'd change** — 2-3 specific, actionable suggestions for the
   next iteration. E.g. "Need a 2c3+2e direct-solve probe after EO —
   on this scramble it would have saved 10 moves." Not generalities.

7. **One-sentence closer.**

Style notes:
- Be specific. "I called dr_trigger_options(axis='UD') and saw three
  candidates" beats "I scouted DR options."
- Quote moves verbatim. "The 4-move EO was R2 D' B' F'" beats "the
  EO was short."
- Use move counts in parens consistently: `R2 D' B' F'` (4 moves).
- Don't pad. If a draft was just a re-run of the same idea with a
  different commitment, say so in 2-3 sentences and move on.
- Write 1800-3000 words. Length serves depth — don't pad, but don't
  skimp on the per-draft walkthrough.
- Do NOT include preamble, JSON, or commentary outside the blog post.
- Do NOT use phrases like "interesting" or "fascinating." This is a
  technical retrospective, not marketing copy.

Output ONLY the markdown blog post.
"""


def _build_user_message(
    scramble_id: str,
    scramble: str,
    attempts: list[dict],
    human_ref: dict | None,
    nissy_axis_locked: dict | None = None,
    prior_versions: list[dict] | None = None,
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
    if nissy_axis_locked:
        lines += [
            "## Nissy axis-locked optimal (UD pipeline, phase-by-phase)",
            f"- Total: {nissy_axis_locked['total']} moves",
        ]
        for ph in nissy_axis_locked["phases"]:
            lines.append(
                f"- {ph['phase']} ({ph['length']}): `{' '.join(ph['moves'])}`"
            )
        lines += [
            "",
            "Note: nissy is axis-locked (UD only, no NISS, no axis-shopping). "
            "It's the ceiling for a 'commit to UD and execute every phase "
            "optimally' strategy. The WCA-reference solver beats it by "
            "skipping DR entirely (direct solve from EO).",
            "",
        ]
    if prior_versions:
        lines += [
            "## Prior LLM-version best solutions on this scramble",
        ]
        for pv in prior_versions:
            lines.append(
                f"- **{pv['version']}**: {pv['total_moves']} moves "
                f"({pv['tool_calls']} tool calls) — "
                f"`{' '.join(pv['final_solution'])}`"
            )
        lines.append("")
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
            # Lift the cap to 20000 chars per attempt so the verbatim
            # walkthrough has enough source material. Most attempts fit.
            (a.get("narrative") or "(no narrative captured)")[:20000],
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
    max_tokens: int = 8000,
) -> Path:
    attempts = _load_attempts(out_dir, scramble_id)
    if not attempts:
        raise SystemExit(f"no attempts found for {scramble_id} in {out_dir}")
    human_ref = _load_human_reference(corpus_path, scramble_id) if corpus_path else None
    scramble = human_ref.get("scramble", "") if human_ref else ""
    if not scramble:
        first = json.loads(Path(attempts[0]["json_path"]).read_text())
        sc = first.get("scramble") or []
        scramble = " ".join(sc) if isinstance(sc, list) else str(sc)

    nissy_axis_locked = _load_nissy_axis_locked(scramble)
    prior_versions = _load_prior_versions(scramble_id, out_dir)

    user_msg = _build_user_message(
        scramble_id, scramble, attempts, human_ref,
        nissy_axis_locked=nissy_axis_locked,
        prior_versions=prior_versions,
    )
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
