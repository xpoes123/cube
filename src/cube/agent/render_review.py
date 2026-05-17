"""Reviewer-friendly per-phase renderer for sim transcripts.

Walks the agent's final solution move-by-move, computing the cube state
at each prefix and tagging phase transitions (EO → DR → HTR → solved).
Emits clean FMC notation segmented by phase with structural metadata,
so a top-level FMC solver can read the solve and critique it without
having to parse the raw tool stream.

Output format:

    # Solve — scramble_id
    Scramble: ...
    Solution: ... (27 moves)

    ## Phase 1 — EO (UD axis, 4 moves)
    `R2 D' B' F'`

    ## Phase 2 — DR (UD axis, 8 moves)
    Setup: `U' R' L2 U F2` (5 moves)
    Trigger: `R U2 R'` — DR-4C2E family
    Resulting substate: (1,0,3,2,4,6,7,5), JZP-eligible: False

    ## Phase 3 — HTR (5 moves)
    `U F2 U' R2 ...`
    Subset: 0-swap long-bar

    ## Phase 4 — Finish (10 moves)
    `...`

    ## Reasoning callouts
    Turn 5: "Picked DR-4C2E over DR-4C4E for the cleaner substate."
    Turn 12: "..."

Usage:
    python -m cube.agent.render_review path/to/transcript.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cube.classifier.features import Axis, is_eo_solved, is_dr
from cube.classifier.htr import is_htr_ud, dr_subset_canonical
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED


_AXES = (Axis.UD, Axis.FB, Axis.RL)
_AXIS_NAMES = {Axis.UD: "UD", Axis.FB: "FB", Axis.RL: "RL"}


def _state_after(scramble: list[str], moves: list[str]):
    s = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if moves:
        s = s.apply_alg(parse_alg(" ".join(moves)))
    return s


def _classify(state) -> dict:
    """Return a dict of structural flags for this state."""
    eo = {ax: is_eo_solved(state, ax) for ax in _AXES}
    dr = {ax: is_dr(state, ax) for ax in _AXES}
    htr_ud = is_htr_ud(state)
    solved = state.is_solved()
    return {
        "eo": eo,
        "dr": dr,
        "htr_ud": htr_ud,
        "solved": solved,
        "subset": dr_subset_canonical(state) if dr[Axis.UD] else None,
    }


def _segment(scramble: list[str], solution: list[str]) -> list[dict]:
    """Walk the solution and identify phase-boundary indices.

    Returns a list of phase dicts: {phase, axis, start, end, moves, ...}.
    Phase tags: 'EO', 'DR', 'HTR', 'finish'.
    """
    # Compute classification at each prefix (length 0 .. N).
    n = len(solution)
    classifications = []
    for i in range(n + 1):
        s = _state_after(scramble, solution[:i])
        classifications.append(_classify(s))

    # Walk and find transitions:
    # 1) first index where ANY axis has EO solved that wasn't solved before → EO end
    # 2) first index where ANY axis has DR solved that didn't have DR before → DR end
    # 3) first index where HTR-UD solved → HTR end
    # 4) solved → finish end (== n)
    #
    # The agent may pick UD / FB / RL — track which axis each phase ends on.

    def _first_true_axis(classifs, key, prev_axes_done) -> tuple[int, Axis] | None:
        for i in range(1, len(classifs)):
            for ax in _AXES:
                if classifs[i][key][ax] and not classifs[i - 1][key].get(ax, False):
                    if ax not in prev_axes_done:
                        return i, ax
        return None

    phases: list[dict] = []
    eo_done_at_axis = _first_true_axis(classifications, "eo", set())
    if eo_done_at_axis is None:
        # Never reached EO — emit a single "premature" phase covering all moves.
        phases.append({"phase": "EO?", "axis": "?", "start": 0, "end": n, "moves": solution[:]})
        return phases

    eo_end, eo_axis = eo_done_at_axis
    phases.append({
        "phase": "EO",
        "axis": _AXIS_NAMES[eo_axis],
        "start": 0,
        "end": eo_end,
        "moves": solution[:eo_end],
    })

    # DR must be on the same axis as EO (or another axis that already had EO).
    dr_done_at_axis = _first_true_axis(
        classifications[eo_end:], "dr", set()
    )
    if dr_done_at_axis is None:
        phases.append({
            "phase": "post-EO (DR never reached)",
            "axis": _AXIS_NAMES[eo_axis],
            "start": eo_end,
            "end": n,
            "moves": solution[eo_end:],
        })
        return phases

    dr_end_rel, dr_axis = dr_done_at_axis
    dr_end = eo_end + dr_end_rel
    phases.append({
        "phase": "DR",
        "axis": _AXIS_NAMES[dr_axis],
        "start": eo_end,
        "end": dr_end,
        "moves": solution[eo_end:dr_end],
        "substate": classifications[dr_end]["subset"],
    })

    # HTR: walk forward until is_htr_ud=True (we only support UD-DR HTR
    # classification right now; if dr_axis != UD it's an approximation).
    htr_end = None
    for i in range(dr_end + 1, n + 1):
        if classifications[i]["htr_ud"]:
            htr_end = i
            break
    if htr_end is None:
        phases.append({
            "phase": "post-DR (HTR never reached)",
            "axis": _AXIS_NAMES[dr_axis],
            "start": dr_end,
            "end": n,
            "moves": solution[dr_end:],
        })
        return phases
    phases.append({
        "phase": "HTR",
        "axis": _AXIS_NAMES[dr_axis],
        "start": dr_end,
        "end": htr_end,
        "moves": solution[dr_end:htr_end],
    })

    # Finish: HTR-end to solved.
    if classifications[n]["solved"]:
        phases.append({
            "phase": "finish",
            "axis": _AXIS_NAMES[dr_axis],
            "start": htr_end,
            "end": n,
            "moves": solution[htr_end:],
        })
    else:
        phases.append({
            "phase": "post-HTR (not solved)",
            "axis": _AXIS_NAMES[dr_axis],
            "start": htr_end,
            "end": n,
            "moves": solution[htr_end:],
        })
    return phases


def _extract_reasoning(transcript: list[dict]) -> list[tuple[int, str]]:
    """Pull short reasoning callouts from the agent's assistant turns."""
    out: list[tuple[int, str]] = []
    for ev in transcript:
        if ev.get("type") != "assistant":
            continue
        turn = ev.get("turn", 0)
        for block in ev.get("content", []) or []:
            btype = block.get("type")
            if btype == "text":
                txt = (block.get("text", "") or "").strip()
                if 20 < len(txt) < 400:
                    out.append((turn, txt))
            elif btype == "thinking":
                txt = (block.get("thinking", "") or "").strip()
                # Heuristic: skip super-short thinking (boilerplate)
                if 60 < len(txt) < 600:
                    out.append((turn, "(internal) " + txt[:400]))
    return out


def render(transcript_path: Path) -> str:
    with transcript_path.open() as f:
        data = json.load(f)

    scramble: list[str] = data.get("scramble") or []
    solution: list[str] = data.get("final_solution") or []
    solves = data.get("solves", False)
    total_moves = data.get("total_moves", 0)
    model = data.get("model", "?")
    halt = data.get("halt_reason")

    lines: list[str] = []
    lines.append(f"# Solve — `{transcript_path.stem}`")
    lines.append("")
    lines.append(f"- **Scramble**: `{' '.join(scramble)}`")
    lines.append(f"- **Model**: `{model}`")
    if solves:
        lines.append(f"- **Result**: SOLVED in **{total_moves} moves**")
        lines.append(f"- **Solution**: `{' '.join(solution)}`")
    else:
        lines.append(f"- **Result**: FAILED (`{halt}`)")
    lines.append("")
    lines.append("---")
    lines.append("")

    if not solves or not solution:
        return "\n".join(lines).rstrip() + "\n"

    phases = _segment(scramble, solution)
    lines.append("## Phase-by-phase")
    lines.append("")
    for i, ph in enumerate(phases, 1):
        moves = ph["moves"]
        title = f"### Phase {i} — {ph['phase']}"
        if ph.get("axis") and ph["axis"] != "?":
            title += f" ({ph['axis']} axis, {len(moves)} moves)"
        else:
            title += f" ({len(moves)} moves)"
        lines.append(title)
        lines.append("")
        if moves:
            lines.append(f"`{' '.join(moves)}`")
        else:
            lines.append("_(no moves)_")
        # Substate detail for DR phase
        if ph["phase"] == "DR" and ph.get("substate"):
            lines.append("")
            lines.append(f"Resulting HTR subset (UD canonical): `{ph['substate']}`")
        lines.append("")

    # Phase length summary table.
    lines.append("## Length summary")
    lines.append("")
    lines.append("| Phase | Axis | Moves |")
    lines.append("|---|---|---:|")
    for ph in phases:
        lines.append(f"| {ph['phase']} | {ph.get('axis','?')} | {len(ph['moves'])} |")
    lines.append(f"| **Total** | — | **{total_moves}** |")
    lines.append("")

    # Reasoning callouts (short).
    callouts = _extract_reasoning(data.get("transcript", []))
    if callouts:
        lines.append("## Reasoning callouts (agent's own words)")
        lines.append("")
        for turn, text in callouts[:20]:  # cap to avoid sprawl
            # Single-line summary per callout.
            one_line = " ".join(text.split())[:300]
            lines.append(f"- **Turn {turn}**: {one_line}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", help="Path to runs/*.json")
    parser.add_argument("-o", "--output", help="Output path (default: <name>.review.md)")
    args = parser.parse_args(argv)
    src = Path(args.transcript)
    if not src.exists():
        print(f"error: not found: {src}", file=sys.stderr)
        return 1
    md = render(src)
    dst = Path(args.output) if args.output else src.with_suffix(".review.md")
    dst.write_text(md)
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
