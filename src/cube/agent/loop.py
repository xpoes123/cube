"""Anthropic API agent loop for solving FMC scrambles.

The agent uses Claude's native tool-use API. We expose the existing tools
in `cube.tools.*` via a dispatch table so adding tools later is trivial.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import anthropic

from cube.tools import algebra, library, policy, search, state

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

# Each entry: name -> (handler, anthropic-tool-schema). The handler takes a
# kwargs dict (the tool_input) and returns a JSON-serializable dict. Adding a
# new tool is one entry here plus the schema.

ToolHandler = Callable[[dict[str, Any]], dict]


def _h_inspect_state(args: dict[str, Any]) -> dict:
    return state.inspect_state(args["scramble"], args["history"])


def _h_try_alg(args: dict[str, Any]) -> dict:
    return state.try_alg(args["scramble"], args["history"], args["alg"])


def _h_verify_solved(args: dict[str, Any]) -> dict:
    return state.verify_solved(args["scramble"], args["solution"])


def _h_policy_intuition(args: dict[str, Any]) -> dict:
    return policy.policy_intuition(
        args["scramble"], args["history"], k=args.get("k", 8),
    )


def _h_cancel(args: dict[str, Any]) -> dict:
    return algebra.cancel(args["moves"])


def _h_niss_flip(args: dict[str, Any]) -> dict:
    return algebra.niss_flip(args["scramble"], args["history"])


def _h_invert(args: dict[str, Any]) -> dict:
    return algebra.invert(args["moves"])


def _h_lookup_commutator(args: dict[str, Any]) -> dict:
    return library.lookup_commutator(args.get("cycle_type"))


def _h_htr_subset(args: dict[str, Any]) -> dict:
    return library.htr_subset(args["scramble"], args["history"])


def _h_residual_cycles(args: dict[str, Any]) -> dict:
    return library.residual_cycles(args["scramble"], args["history"])


def _h_lookahead(args: dict[str, Any]) -> dict:
    return search.lookahead(
        args["scramble"], args["history"],
        target=args["target"], axis=args.get("axis"),
        width=args.get("width", 20), depth=args.get("depth", 4),
    )


def _h_find_dr_via_trigger(args: dict[str, Any]) -> dict:
    return search.find_dr_via_trigger(
        args["scramble"], args["history"],
        axis=args["axis"],
        tail_length=args.get("tail_length", 2),
        setup_width=args.get("setup_width", 30),
        setup_depth=args.get("setup_depth", 8),
    )


def _h_solve_htr_and_finish_from_dr(args: dict[str, Any]) -> dict:
    return search.solve_htr_and_finish_from_dr(
        args["scramble"], args["history"], axis=args["axis"],
    )


_MOVE_LIST_SCHEMA = {
    "type": "array",
    "items": {"type": "string"},
    "description": "Sequence of WCA-notation moves, e.g. ['R', \"U'\", 'F2'].",
}


TOOL_REGISTRY: dict[str, tuple[ToolHandler, dict]] = {
    "inspect_state": (
        _h_inspect_state,
        {
            "name": "inspect_state",
            "description": (
                "Classify the current cube state after applying scramble + history. "
                "Returns EO/CO counts per axis, which axes have EO or DR solved, "
                "whether the state is in HTR, and whether it's solved."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                },
                "required": ["scramble", "history"],
            },
        },
    ),
    "policy_intuition": (
        _h_policy_intuition,
        {
            "name": "policy_intuition",
            "description": (
                "Ask the trained policy for top-k 'intuitive' next-move suggestions. "
                "One forward pass; analogous to a human's trained eye. Use sparingly."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                    "k": {"type": "integer", "minimum": 1, "maximum": 20, "default": 8},
                },
                "required": ["scramble", "history"],
            },
        },
    ),
    "try_alg": (
        _h_try_alg,
        {
            "name": "try_alg",
            "description": (
                "Hypothetically apply `alg` on top of `history` and report before/"
                "after summaries plus deltas. Use to preview a continuation without "
                "committing to it."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                    "alg": _MOVE_LIST_SCHEMA,
                },
                "required": ["scramble", "history", "alg"],
            },
        },
    ),
    "cancel": (
        _h_cancel,
        {
            "name": "cancel",
            "description": (
                "Apply local cancellation rules to a move sequence (same-face combine, "
                "through-commute). Returns the cancelled sequence and savings."
            ),
            "input_schema": {
                "type": "object",
                "properties": {"moves": _MOVE_LIST_SCHEMA},
                "required": ["moves"],
            },
        },
    ),
    "niss_flip": (
        _h_niss_flip,
        {
            "name": "niss_flip",
            "description": (
                "Switch to the NISS inverse frame. Returns the inverted scramble and "
                "the cumulative state expressed on the inverse side so search can continue there."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                },
                "required": ["scramble", "history"],
            },
        },
    ),
    "invert": (
        _h_invert,
        {
            "name": "invert",
            "description": "Invert a move sequence (mechanical).",
            "input_schema": {
                "type": "object",
                "properties": {"moves": _MOVE_LIST_SCHEMA},
                "required": ["moves"],
            },
        },
    ),
    "verify_solved": (
        _h_verify_solved,
        {
            "name": "verify_solved",
            "description": (
                "Ground-truth check: apply scramble + solution and report whether the "
                "cube is fully solved. The acceptance criterion."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "solution": _MOVE_LIST_SCHEMA,
                },
                "required": ["scramble", "solution"],
            },
        },
    ),
    "lookup_commutator": (
        _h_lookup_commutator,
        {
            "name": "lookup_commutator",
            "description": (
                "Look up known commutators a strong human has memorized. Filter by "
                "cycle_type (corner_3cycle, edge_3cycle, corner_twist_2, edge_flip_2) "
                "or omit for the whole library."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "cycle_type": {
                        "type": "string",
                        "enum": [
                            "corner_3cycle", "edge_3cycle",
                            "corner_twist_2", "edge_flip_2",
                        ],
                    },
                },
                "required": [],
            },
        },
    ),
    "htr_subset": (
        _h_htr_subset,
        {
            "name": "htr_subset",
            "description": (
                "Identify the HTR corner subset of the current state. Strong solvers "
                "recognize subsets by their canonical cp form; states with the same "
                "form have similar finish difficulty."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                },
                "required": ["scramble", "history"],
            },
        },
    ),
    "residual_cycles": (
        _h_residual_cycles,
        {
            "name": "residual_cycles",
            "description": (
                "Decompose what's still unsolved into permutation cycles + orientation "
                "errors. Use this when looking for an insertion: it tells you the "
                "cycle structure and recommends a commutator type to look up."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                },
                "required": ["scramble", "history"],
            },
        },
    ),
    "lookahead": (
        _h_lookahead,
        {
            "name": "lookahead",
            "description": (
                "Bounded forward search (human-scale: depth ≤ 7, width ≤ 50). "
                "Find sequences that reach a target stage. target=eo|dr|htr|solved; "
                "axis=UD|FB|RL (required for eo/dr/htr). For DR specifically, "
                "prefer `find_dr_via_trigger` once EO is solved."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                    "target": {
                        "type": "string",
                        "enum": ["eo", "dr", "htr", "solved"],
                    },
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                    "width": {"type": "integer", "minimum": 1, "maximum": 50, "default": 20},
                    "depth": {"type": "integer", "minimum": 1, "maximum": 7, "default": 5},
                },
                "required": ["scramble", "history", "target"],
            },
        },
    ),
    "solve_htr_and_finish_from_dr": (
        _h_solve_htr_and_finish_from_dr,
        {
            "name": "solve_htr_and_finish_from_dr",
            "description": (
                "From a DR-solved state, produce the full HTR + half-turn "
                "finish. Strong humans recognize the HTR subset and execute "
                "a memorized finish; this tool does the same via A* + PDB "
                "walk-back. Returns htr_moves + finish_moves + total_moves. "
                "ONLY use after the state is in DR on `axis` (call inspect_state "
                "to verify). This is the cleanest way to complete the solve "
                "once you've found a DR."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                },
                "required": ["scramble", "history", "axis"],
            },
        },
    ),
    "find_dr_via_trigger": (
        _h_find_dr_via_trigger,
        {
            "name": "find_dr_via_trigger",
            "description": (
                "Find DR by searching for a 'trigger state' that's ≤ tail_length "
                "moves from DR, then completing via DFS. This mirrors how strong "
                "humans actually find DR: spot a setup chain ending in a known "
                "pattern (R, R U2 R, F R F, etc.), then the trigger lands the DR. "
                "EO on `axis` must already be solved. Returns up to 5 (setup + tail) "
                "sequences sorted by total length."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "scramble": _MOVE_LIST_SCHEMA,
                    "history": _MOVE_LIST_SCHEMA,
                    "axis": {"type": "string", "enum": ["UD", "FB", "RL"]},
                    "tail_length": {"type": "integer", "minimum": 1, "maximum": 3, "default": 2},
                    "setup_width": {"type": "integer", "minimum": 1, "maximum": 1024, "default": 512},
                    "setup_depth": {"type": "integer", "minimum": 1, "maximum": 10, "default": 8},
                },
                "required": ["scramble", "history", "axis"],
            },
        },
    ),
}


def _tool_schemas() -> list[dict]:
    return [schema for _, schema in TOOL_REGISTRY.values()]


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """\
You are an expert Rubik's Cube FMC (Fewest Moves Challenge) solver.

Your task: produce a move sequence that solves the given scramble. You have \
access to tools that mirror what a strong human FMC solver uses on paper.

# The scramble
{scramble_str}

That is exactly {scramble_length} moves. **Always pass the scramble to tools
as the following JSON array — DO NOT retype it move-by-move, you will drop
moves**:

  scramble = {scramble_json}

# Tools you have
- `inspect_state(scramble, history)`: look at the cube. Tells you EO/CO per axis, \
which axes have EO/DR/HTR, and whether it's solved.
- `policy_intuition(scramble, history, k)`: ask a trained policy network for top-k \
"intuitive" next moves. Use it like a human consulting their gut. Don't spam it.
- `try_alg(scramble, history, alg)`: preview applying `alg` without committing. \
Use this constantly to test candidate continuations.
- `cancel(moves)`: apply local move-cancellation (e.g. `U U'` -> nothing).
- `niss_flip(scramble, history)`: switch to NISS inverse frame.
- `invert(moves)`: invert a move sequence.
- `verify_solved(scramble, solution)`: THE acceptance criterion. Your final \
solution is accepted iff this returns `solves: true`.

# FMC concepts (brief reminders)
- **EO** (edge orientation): an edge is "good" iff it can be solved with only \
<U,D,L,R,F2,B2> moves on a chosen axis. Three axes: UD, FB, RL. Goal: 0 bad edges \
on one axis.
- **DR** (domino reduction): EO solved on an axis AND corner orientation matches \
that axis AND E-slice edges in E-slice. From DR, the cube is solvable in only \
<U,D,L2,R2,F2,B2>. Powerful reduction.
- **HTR** (half-turn reduction): from DR, get to a state solvable with only \
half-turns. ~40 distinct HTR subsets, each has known optimal finishes.
- **NISS** (Normal-Inverse Scramble Switch): solve some moves on the inverse \
scramble, then concatenate `normal_moves + invert(inverse_moves)`. Lets you find \
shorter paths by attacking from both ends.

# Strategy guidance
- Aim for short solutions (target: 25-30 moves). Anything under 40 is a real result.
- Typical pipeline: EO -> DR -> HTR -> finish. But feel free to deviate.
- **Important**: the inverse of the scramble is always a valid solution of
  the same length as the scramble itself — but this is the TRIVIAL "undo
  the scramble" solution and doesn't count as FMC. Your solution should
  be SHORTER than the scramble (typically 25-30 moves for a 25-27 move
  scramble). Don't pass the inverse-scramble as `history` to inspect_state
  and claim it as a solution.

# CRITICAL: each stage needs the right tool. Pipeline:

  1. **EO** (1-5 moves):
     `lookahead(target="eo", axis=X, depth=5)` from the scramble. Pick the
     shortest hit. Apply those moves (add to history).
  2. **DR** (5-10 more moves, total EO+DR ~10-12):
     After EO is solved on axis X, call `find_dr_via_trigger(axis=X, tail_length=2)`.
     This is the right tool for DR — it searches for a "trigger" state ≤2 moves
     from DR (the way humans do it: spot a setup, recognize a trigger pattern,
     finish). Do NOT use plain `lookahead(target="dr")` from EO — DR is usually
     7-10 moves away, beyond lookahead's depth cap of 7.
  3. **HTR + Finish** (10-15 more moves, combined):
     Once DR is solved, call `solve_htr_and_finish_from_dr(axis=X)`. This
     produces both the HTR moves and the half-turn finish in one call —
     equivalent to a strong human recognizing the HTR subset and executing
     a memorized finish. Do NOT use `lookahead(target="htr")` for this —
     it doesn't constrain to DR-group moves and wanders.
  5. **NISS**: at any boundary, try `niss_flip` and run the same pipeline on the
     inverse scramble. Inverse moves get concatenated as
     `normal_moves + invert(inverse_moves)` — `verify_solved` handles this
     automatically when you pass the full solution.

- Use `lookup_commutator` + `residual_cycles` when you have a near-solved state with \
a small cycle remaining — insert a commutator at the cheapest position.
- Use `cancel(moves)` to collapse adjacent same-face moves before submitting.

# Submitting
When you believe you have a solution, FIRST call `verify_solved` to confirm. \
Then output the final solution as a JSON array on its own line in this format:

  FINAL_SOLUTION: ["R", "U", "R'", ...]

The runner parses that line and re-verifies. If verification fails, you'll \
be told why and can keep working.

Be concise in your reasoning. Use tools liberally. Don't get stuck explaining \
yourself when you could be testing moves.
"""


# ---------------------------------------------------------------------------
# Solution extraction
# ---------------------------------------------------------------------------

# Matches `FINAL_SOLUTION: [...]` (case-insensitive, optional whitespace).
_FINAL_RE = re.compile(r"FINAL[_ ]SOLUTION\s*:\s*(\[[^\]]*\])", re.IGNORECASE)


def _extract_solution(text: str) -> list[str] | None:
    """Pull a FINAL_SOLUTION JSON array out of an assistant text block."""
    m = _FINAL_RE.search(text)
    if not m:
        return None
    try:
        parsed = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, list) or not all(isinstance(x, str) for x in parsed):
        return None
    return parsed


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------


def _dispatch_tool(name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """Run a tool by name. Errors are returned as a dict so the model can recover."""
    handler = TOOL_REGISTRY.get(name)
    if handler is None:
        return {"error": f"unknown tool: {name}"}
    try:
        return handler[0](tool_input)
    except Exception as e:  # surface error to the model rather than crash the loop
        return {"error": f"{type(e).__name__}: {e}"}


def _format_text_blocks(blocks: list[Any]) -> str:
    return "\n".join(b.text for b in blocks if getattr(b, "type", None) == "text")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------


def solve(
    scramble: list[str],
    *,
    model: str = DEFAULT_MODEL,
    max_tool_calls: int = 50,
    verbose: bool = False,
) -> dict:
    """Run the Anthropic agent loop on a scramble; return solution + stats.

    See module docstring for the return-dict shape.
    """
    client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY from env

    scramble_json = json.dumps(scramble)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        scramble_str=" ".join(scramble),
        scramble_json=scramble_json,
        scramble_length=len(scramble),
    )
    user_msg = f"Solve this scramble: {' '.join(scramble)}"

    messages: list[dict[str, Any]] = [{"role": "user", "content": user_msg}]
    transcript: list[dict[str, Any]] = [
        {"type": "system", "content": system_prompt},
        {"type": "user", "content": user_msg},
    ]

    tool_calls = 0
    input_tokens = 0
    output_tokens = 0
    final_solution: list[str] = []
    solves = False

    if verbose:
        print(f"[agent] scramble: {' '.join(scramble)}")
        print(f"[agent] model: {model}")

    while tool_calls < max_tool_calls:
        resp = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            tools=_tool_schemas(),
            messages=messages,
        )
        input_tokens += resp.usage.input_tokens
        output_tokens += resp.usage.output_tokens

        # Record assistant content for transcript and conversation continuation.
        assistant_content = [b.model_dump() for b in resp.content]
        transcript.append({"type": "assistant", "content": assistant_content, "stop_reason": resp.stop_reason})
        messages.append({"role": "assistant", "content": assistant_content})

        if verbose:
            text_out = _format_text_blocks(resp.content)
            if text_out:
                print(f"\n[claude]\n{text_out}")

        tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]

        if tool_uses:
            tool_results = []
            for tu in tool_uses:
                tool_calls += 1
                if verbose:
                    print(f"\n[tool#{tool_calls}] {tu.name}({json.dumps(tu.input)[:200]})")
                result = _dispatch_tool(tu.name, tu.input)
                if verbose:
                    print(f"[result] {json.dumps(result)[:300]}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": json.dumps(result),
                })
                transcript.append({
                    "type": "tool_call",
                    "name": tu.name,
                    "input": tu.input,
                    "result": result,
                })
                if tool_calls >= max_tool_calls:
                    break
            messages.append({"role": "user", "content": tool_results})
            continue

        # No tool calls — look for a final solution in the text output.
        text = _format_text_blocks(resp.content)
        proposed = _extract_solution(text)
        if proposed is not None:
            check = state.verify_solved(scramble, proposed)
            transcript.append({"type": "verify", "solution": proposed, "result": check})
            if check["solves"]:
                final_solution = proposed
                solves = True
                if verbose:
                    print(f"\n[agent] SOLVED in {check['total_moves']} moves")
                break
            # Feed back the failure and let the agent try again.
            feedback = (
                f"Your proposed solution does NOT solve the scramble. "
                f"verify_solved returned {json.dumps(check)}. "
                f"Keep working — inspect the resulting state and fix it."
            )
            if verbose:
                print("\n[agent] proposed solution failed; continuing")
            messages.append({"role": "user", "content": feedback})
            transcript.append({"type": "user", "content": feedback})
            continue

        # No tool calls and no FINAL_SOLUTION — nudge the agent.
        if resp.stop_reason == "end_turn":
            nudge = (
                "You stopped without calling tools or emitting a FINAL_SOLUTION line. "
                "Either continue working with tools, or output your solution as "
                "`FINAL_SOLUTION: [\"...\", \"...\"]` on its own line."
            )
            messages.append({"role": "user", "content": nudge})
            transcript.append({"type": "user", "content": nudge})
            continue

        break  # unknown stop reason; bail

    return {
        "scramble": scramble,
        "final_solution": final_solution,
        "solves": solves,
        "total_moves": len(final_solution),
        "tool_calls": tool_calls,
        "transcript": transcript,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _save_transcript(result: dict) -> Path:
    runs = Path("runs")
    runs.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = runs / f"agent_{ts}.json"
    with path.open("w") as f:
        json.dump(result, f, indent=2, default=str)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Claude FMC agent on a scramble.")
    parser.add_argument("scramble", help="Scramble in WCA notation (space-separated).")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Anthropic model name.")
    parser.add_argument("--max-tool-calls", type=int, default=50)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("error: ANTHROPIC_API_KEY not set in environment", file=sys.stderr)
        return 2

    scramble = args.scramble.split()
    t0 = time.time()
    result = solve(
        scramble,
        model=args.model,
        max_tool_calls=args.max_tool_calls,
        verbose=args.verbose,
    )
    elapsed = time.time() - t0

    path = _save_transcript(result)
    print(f"\n=== run complete ({elapsed:.1f}s) ===")
    print(f"  solves:        {result['solves']}")
    print(f"  total_moves:   {result['total_moves']}")
    print(f"  tool_calls:    {result['tool_calls']}")
    print(f"  input_tokens:  {result['input_tokens']}")
    print(f"  output_tokens: {result['output_tokens']}")
    print(f"  solution:      {' '.join(result['final_solution'])}")
    print(f"  transcript:    {path}")
    return 0 if result["solves"] else 1


if __name__ == "__main__":
    sys.exit(main())
