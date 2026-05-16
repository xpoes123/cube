"""Human-style narrative renderer for sim transcripts.

Translates the raw tool-call stream into natural language that reads
like a human FMC solver thinking out loud. Each tool gets a hand-
written translator that converts (input, result) into a sentence or
two of observation + commentary.

The output is for the video deliverable: viewers should be able to
follow the solve without reading JSON. The structured
`render_narrative.py` stays as the detailed-trace alternative.

Usage:
    python -m cube.agent.human_narrative path/to/transcript.json -o solve.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Per-tool translators
# ---------------------------------------------------------------------------


def _fmt_moves(moves: list[str] | None) -> str:
    if not moves:
        return "(empty)"
    return "`" + " ".join(moves) + "`"


def _t_inspect_state(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return ["I glance at the cube."]
    parts = ["I look over the cube."]
    bad = res.get("bad_edges_per_axis")
    if bad:
        ud = bad.get("UD", "?")
        fb = bad.get("FB", "?")
        rl = bad.get("RL", "?")
        parts.append(f"Bad-edge counts: UD={ud}, FB={fb}, RL={rl}.")
    co = res.get("co_count_per_axis")
    if co:
        parts.append(f"Corner-orientation off: UD={co.get('UD')}, FB={co.get('FB')}, RL={co.get('RL')}.")
    if res.get("on_inverse"):
        parts.append("I'm currently working on the inverse scramble.")
    if res.get("history_visible"):
        h = res["history_visible"]
        if h:
            parts.append(f"Last applied: {_fmt_moves(h[-6:])}.")
    return parts


def _t_quick_check(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    if res.get("is_solved"):
        return ["A quick glance — the cube is solved."]
    pieces = []
    eo = res.get("is_eo_per_axis", {})
    dr = res.get("is_dr_per_axis", {})
    htr = res.get("is_htr_ud")
    eo_axes = [a for a, v in eo.items() if v]
    dr_axes = [a for a, v in dr.items() if v]
    if htr:
        pieces.append("Quick check: in HTR.")
    elif dr_axes:
        pieces.append(f"Quick check: DR-locked on {','.join(dr_axes)}, not yet HTR.")
    elif eo_axes:
        pieces.append(f"Quick check: EO solved on {','.join(eo_axes)}, working toward DR.")
    else:
        pieces.append("Quick check: still scrambled.")
    return pieces


def _t_niss_scout(inp: dict, res: dict) -> list[str]:
    rows = res.get("rows", []) if isinstance(res, dict) else []
    if not rows:
        return ["I scout — nothing came back."]
    valid = [r for r in rows if r.get("eo_plus_dr_length") is not None]
    pieces = [f"I scout EO+DR on both normal and inverse, all three axes — {len(valid)} viable rows."]
    for r in valid[:3]:
        side = r.get("side", "?")
        axis = r.get("axis", "?")
        eo_len = r.get("eo_length", "?")
        dr_opt = r.get("dr_option") or {}
        fam = dr_opt.get("trigger_family", "?")
        total_to_dr = dr_opt.get("total_to_dr", "?")
        jzp = " [JZP]" if r.get("jzp_eligible") else ""
        pieces.append(f"  • {side}-{axis}: EO {eo_len}mv → {fam} DR ({total_to_dr}mv){jzp}")
    pieces.append("I'll weigh the substate quality (trigger family) against raw length and pick.")
    return pieces


def _t_eo_pattern_lookup(inp: dict, res: dict) -> list[str]:
    axis = inp.get("axis", "?")
    if not isinstance(res, dict) or res.get("found") == 0:
        return [f"On the {axis} axis, I don't recognize the EO pattern from memory."]
    options = res.get("options", [])
    if not options:
        return [f"EO on {axis}: already solved." ]
    moves = options[0].get("moves", [])
    note = res.get("note", "")
    if not moves:
        return [f"EO on {axis}: already solved."]
    if "partial" in note.lower() or options[0].get("partial"):
        full_len = options[0].get("full_optimal_length", len(moves))
        return [f"On {axis} axis I recognize the EO pattern — the first chunk is {_fmt_moves(moves)} (full fix is {full_len} moves)."]
    return [f"On {axis} axis I recognize the EO pattern — {_fmt_moves(moves)} fixes it."]


def _t_apply_moves(inp: dict, res: dict) -> list[str]:
    moves = inp.get("moves", [])
    if not moves:
        return []
    return [f"I turn {_fmt_moves(moves)}."]


def _t_undo_moves(inp: dict, res: dict) -> list[str]:
    n = inp.get("n", 1)
    return [f"I rewind {n} move{'s' if n != 1 else ''}."]


def _t_reset_slot(inp: dict, res: dict) -> list[str]:
    return ["I reset the cube back to the scramble — fresh start, dropping the branch I was on."]


def _t_new_slot(inp: dict, res: dict) -> list[str]:
    name = inp.get("name", "?")
    src = inp.get("copy_from")
    if src:
        return [f"I bookmark the current state as slot `{name}` so I can explore an alternative without losing this one."]
    return [f"I create a fresh slot `{name}` for an alternate branch."]


def _t_niss_flip(inp: dict, res: dict) -> list[str]:
    if isinstance(res, dict) and res.get("now_on_inverse"):
        return ["NISS flip — switching to the inverse scramble."]
    return ["NISS flip — switching back to the normal scramble."]


def _t_dr_trigger_options(inp: dict, res: dict) -> list[str]:
    axis = inp.get("axis", "?")
    opts = res.get("options", []) if isinstance(res, dict) else []
    if "error" in (res or {}):
        return [f"DR trigger menu on {axis}: {res['error']}"]
    if not opts:
        return [f"DR trigger menu on {axis}: no named trigger fits within 5 setup moves."]
    pieces = [f"I survey the named DR triggers on {axis}:"]
    for o in opts[:3]:
        fam = o.get("trigger_family", "?")
        setup = o.get("setup_length", "?")
        trig = o.get("trigger_length", "?")
        jzp = " [JZP]" if o.get("jzp_eligible") else ""
        pieces.append(f"  • {fam}: {setup}-mv setup + {trig}-mv trigger ({setup + trig if isinstance(setup, int) and isinstance(trig, int) else '?'} total){jzp}")
    return pieces


def _t_htr_classify(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict) or "error" in res:
        return [f"HTR classify: {(res or {}).get('error', 'not in DR yet')}"]
    name = res.get("subset_name", "?")
    phases = res.get("phases", {})
    red = phases.get("htr_reduction", {}).get("length", "?")
    fin = phases.get("finish", {}).get("length", "?")
    cached = res.get("cached")
    cache_note = " (recall)" if cached else " (first exposure — learning)"
    return [f"I recognize the HTR subset: **{name}**. Reduction is {red} moves, finish is {fin} moves{cache_note}."]


def _t_htr_subset(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    cs = res.get("canonical_subset", [])
    return [f"HTR canonical subset: `{cs}`."]


def _t_apply_htr_phase(inp: dict, res: dict) -> list[str]:
    phase = inp.get("phase", "?")
    if not isinstance(res, dict) or "error" in res:
        return [f"apply_htr_phase {phase}: {(res or {}).get('error', 'failed')}."]
    moves = res.get("moves", [])
    partial = res.get("partial")
    label = "corner reduction" if phase == "htr_reduction" else "half-turn finish"
    if partial:
        full = res.get("full_phase_length", "?")
        return [f"For the {label}, I see {_fmt_moves(moves)} (chunk of a {full}-move phase) — apply and re-check."]
    if not moves:
        return [f"The {label} is empty — already done."]
    return [f"For the {label}: {_fmt_moves(moves)}."]


def _t_analyze_residual(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    cls = res.get("residual_class", "?")
    if res.get("is_pure_corner_3cycle"):
        return [f"The residual is a **pure corner 3-cycle**. An 8-move commutator could close it."]
    if res.get("is_pure_edge_3cycle"):
        return [f"The residual is a **pure edge 3-cycle**. Inserting a comm could close it."]
    if cls == "solved":
        return ["Residual: cube is solved."]
    return [f"Residual class: {cls}."]


def _t_derive_corner_3cycle(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict) or "error" in res:
        return [f"derive_corner_3cycle: {(res or {}).get('error', 'not applicable')}."]
    moves = res.get("moves", [])
    return [f"I derive the corner 3-cycle commutator: {_fmt_moves(moves)}."]


def _t_replace_and_shorten(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict) or "error" in res:
        return [f"r&s: {(res or {}).get('error', 'failed')}"]
    delta = res.get("delta", 0)
    if delta < 0:
        return [f"replace_and_shorten on the tail span: substitute is {abs(delta)} move{'s' if abs(delta) != 1 else ''} shorter. Accepted."]
    elif delta == 0:
        return ["replace_and_shorten: same length, no improvement."]
    else:
        return [f"replace_and_shorten: substitute is {delta} moves longer; reject."]


def _t_cancel(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    saved = res.get("saved", 0)
    if saved > 0:
        before = res.get("input_length", "?")
        after = res.get("cancelled_length", "?")
        return [f"I run cancellation: {before} → {after} moves (saved {saved})."]
    return ["I check for cancellations — no savings."]


def _t_compose_niss_solution(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    solves = res.get("solves")
    length = res.get("length", "?")
    frame = res.get("frame_at_compose", "?")
    if solves:
        return [f"I assemble the canonical {frame}-frame solution: **{length} moves**, verified."]
    return [f"compose_niss_solution: not yet solved ({length} moves on slot)."]


def _t_verify_solved(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    if res.get("solves"):
        return [f"verify_solved: ✓ — {res.get('total_moves')} moves."]
    return [f"verify_solved: ✗ — proposed solution does NOT solve. Back to work."]


def _t_budget_status(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    sim_left = res.get("sim_remaining")
    tool_left = res.get("tool_calls_remaining")
    return [f"Budget check: {sim_left}s sim, {tool_left} tool calls remaining."]


def _t_try_alg(inp: dict, res: dict) -> list[str]:
    alg = inp.get("alg", [])
    return [f"I try {_fmt_moves(alg)} on top to see the after-state (without committing)."]


def _t_lookahead(inp: dict, res: dict) -> list[str]:
    return ["I look 4 moves ahead with a small beam."]


def _t_policy_intuition(inp: dict, res: dict) -> list[str]:
    return ["I check my gut for plausible next moves."]


def _t_brain_suggest(inp: dict, res: dict) -> list[str]:
    if not isinstance(res, dict):
        return []
    step = inp.get("step", "?")
    if res.get("from_brain"):
        cands = res.get("candidates", [])[:3]
        if not cands:
            return [f"brain ({step}): no candidates."]
        cand_str = ", ".join(f"{c['move']} ({c['prob']:.0%})" for c in cands)
        return [f"My trained intuition for {step}: top candidates are {cand_str}."]
    return [f"brain ({step}): no checkpoint trained yet; falling back to legacy policy."]


def _t_probe_dr_pattern(inp: dict, res: dict) -> list[str]:
    return ["I probe what DR would look like if I applied this EO (without committing)."]


def _t_dr_recognize(inp: dict, res: dict) -> list[str]:
    return ["I check whether the DR is recognizable from this state via the library."]


def _t_eo_pattern_set_bias(inp: dict, res: dict) -> list[str]:
    return []  # internal — skip


_TRANSLATORS = {
    "inspect_state": _t_inspect_state,
    "quick_check": _t_quick_check,
    "niss_scout": _t_niss_scout,
    "eo_pattern_lookup": _t_eo_pattern_lookup,
    "apply_moves": _t_apply_moves,
    "undo_moves": _t_undo_moves,
    "reset_slot": _t_reset_slot,
    "new_slot": _t_new_slot,
    "niss_flip": _t_niss_flip,
    "dr_trigger_options": _t_dr_trigger_options,
    "htr_classify": _t_htr_classify,
    "htr_subset": _t_htr_subset,
    "apply_htr_phase": _t_apply_htr_phase,
    "analyze_residual": _t_analyze_residual,
    "derive_corner_3cycle": _t_derive_corner_3cycle,
    "replace_and_shorten": _t_replace_and_shorten,
    "cancel": _t_cancel,
    "compose_niss_solution": _t_compose_niss_solution,
    "verify_solved": _t_verify_solved,
    "budget_status": _t_budget_status,
    "try_alg": _t_try_alg,
    "lookahead": _t_lookahead,
    "policy_intuition": _t_policy_intuition,
    "brain_suggest": _t_brain_suggest,
    "probe_dr_pattern": _t_probe_dr_pattern,
    "dr_recognize": _t_dr_recognize,
}


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------


def _is_meaningful_text(text: str) -> bool:
    """Filter trivial / boilerplate model text from the narration stream."""
    if not text or len(text) < 8:
        return False
    return True


def _clean_thinking(text: str) -> str:
    """Trim thinking output for readability. Keep the substantive bits."""
    text = text.strip()
    # Collapse multiple blank lines
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text


def render(transcript_json_path: Path, *, include_thinking: bool = True) -> str:
    with transcript_json_path.open() as f:
        data = json.load(f)

    scramble = data.get("scramble") or []
    model = data.get("model", "?")
    solves = data.get("solves", False)
    total_moves = data.get("total_moves", 0)
    halt = data.get("halt_reason")

    lines: list[str] = []
    lines.append(f"# Solve — {transcript_json_path.stem}")
    lines.append("")
    lines.append(f"**Scramble**: `{' '.join(scramble)}`  ")
    lines.append(f"**Model**: `{model}`  ")
    status = f"**Result**: SOLVED in {total_moves} moves" if solves else f"**Result**: failed ({halt})"
    lines.append(status)
    if solves and data.get("final_solution"):
        lines.append(f"**Solution**: `{' '.join(data['final_solution'])}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Walk the transcript. We surface each turn's text/thinking, then the
    # human-translation of each tool call.
    turn_idx = 0
    for entry in data.get("transcript", []):
        kind = entry.get("type")
        if kind == "assistant":
            turn_idx += 1
            blocks = entry.get("content", [])
            for block in blocks:
                btype = block.get("type")
                if btype == "thinking" and include_thinking:
                    text = _clean_thinking(block.get("thinking", "") or "")
                    if _is_meaningful_text(text):
                        lines.append(f"*Thinking ({turn_idx}):*")
                        lines.append("")
                        # Use blockquote for readability
                        for ln in text.split("\n"):
                            lines.append(f"> {ln}")
                        lines.append("")
                elif btype == "text":
                    text = (block.get("text", "") or "").strip()
                    if _is_meaningful_text(text):
                        lines.append(text)
                        lines.append("")
        elif kind == "tool_call":
            name = entry.get("name", "?")
            inp = entry.get("input", {})
            res = entry.get("result", {})
            translator = _TRANSLATORS.get(name)
            if translator is None:
                continue
            sentences = translator(inp, res)
            for s in sentences:
                lines.append(s)
            if sentences:
                lines.append("")
        elif kind == "verify":
            sol = entry.get("solution", [])
            r = entry.get("result", {})
            if r.get("solves"):
                lines.append(f"**Verified solution ({r.get('total_moves')} moves):** `{' '.join(sol)}`")
                lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", help="Path to runs/*.json")
    parser.add_argument("-o", "--output", help="Output .md path (default: same name, .human.md)")
    parser.add_argument("--no-thinking", action="store_true", help="Suppress thinking blocks")
    args = parser.parse_args(argv)

    src = Path(args.transcript)
    if not src.exists():
        print(f"error: not found: {src}", file=sys.stderr)
        return 1
    md = render(src, include_thinking=not args.no_thinking)
    if args.output:
        dst = Path(args.output)
    else:
        dst = src.with_suffix(".human.md")
    dst.write_text(md)
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
