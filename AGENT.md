# cube — agent direction

This document tracks the pivot from "FMC analyzer / solver" to "LLM agent equipped with FMC tools."

## Why we pivoted

Cubelib + mallard already do classical FMC analysis very well. Speed (Rust + SIMD), pipeline richness (RZP / FR / HTR subsets / leave-slice / FINLS), and per-stage NISS configurability all exceed what we'd ship in pure Python in any reasonable timeframe. Competing on move-count or speed is a losing fight.

Where cubelib has nothing: **a learned policy calibrated to real human solvers**, and **a model that can reason about state in natural language**. That intersection is the wedge.

## Goal

Build an LLM agent that solves FMC scrambles using **only tools a strong human FMC solver has access to**. Target:

- **20-25 move average**: stretch. Beats most humans in competition.
- **25-30 move average**: realistic. Matches strong human practitioners.
- **30+**: tools or prompting need work.

The 25-move target is competitive with top human FMC averages on official 3-attempt means. Anything below that is a real result.

## Narrative for the video

> "Can an LLM solve a Rubik's cube as well as a human FMC champion? I gave Claude the same tools a human uses — pattern recognition, trigger libraries, NISS, insertions — and watched it reason its way to a solve."

The plot beats:
1. **Baseline failure**: LLM with no tools cannot solve a Rubik's cube. (Establishes the difficulty.)
2. **Progress with state-inspection tools**: LLM can describe the cube but produces nonsense moves.
3. **Progress with policy-as-intuition**: LLM picks plausible moves but doesn't have a strategy.
4. **Progress with stage-targeted tools**: LLM produces real solves, with reasoning. (The payoff.)

Each beat shows visible improvement. Failure modes are part of the content.

## What "human-permissible tool" means

A tool is fair iff a competition FMC solver could plausibly use the same operation in their head or on paper.

### Fair tools

- **State inspection**: classify EO / DR / HTR per axis, count residual cycles, name HTR subsets. (Human looks at the cube.)
- **Move application**: apply an alg, return the resulting state and what changed. (Human mentally previews.)
- **Cancellation**: collapse adjacent same-face moves + through-commute. (Humans do this routinely on paper.)
- **NISS frame switching**: invert frame, get the inverse-scramble state. (NISS by hand.)
- **Commutator library**: look up known commutators for 3-cycles. (Humans memorize ~10-30 commonly.)
- **Subset finishes**: published optimal finishes per HTR subset. (Humans memorize.)
- **Single-pass policy intuition**: one forward pass of the transformer, top-k move suggestions. This stands in for **what a trained human's eye instantly suggests** when looking at a position.
- **Shallow lookahead**: depth ≤ 5, width ≤ 50. ("Humans look 4-5 moves ahead.")

### Not fair (cheating)

- Wide beam search (width 8192).
- A\* with admissible PDB heuristic — humans don't have a 663,552-entry table memorized.
- Full PDB walk-back as a single "solve from HTR" call.
- Direct cycle search across the full cube group.

### Edge case: subset finish lookup

A human champion does memorize HTR subset finishes. So `lookup_subset_finish(subset_name) → moves` is fair. The line we draw: **the LLM has to identify which subset it's in, then look it up.** It can't ask for "the optimal finish from any state" without naming the subset first.

## Architecture

```
┌──────────────────┐         ┌──────────────────────┐
│ Claude (Sonnet/  │  tools  │ tools/ (this repo)   │
│  Opus) via API   │ ───────▶│   inspect_state      │
│                  │         │   policy_intuition   │
│                  │ ◀─────  │   try_alg            │
│                  │ results │   cancel             │
└──────────────────┘         │   niss_flip          │
        │                    │   lookup_commutator  │
        │                    │   htr_subset         │
        │                    │   subset_finish      │
        │                    │   lookahead          │
        │                    │   verify_solved      │
        ▼                    └──────────────────────┘
┌──────────────────────┐
│ agent.py             │
│   conversation loop  │
│   tool dispatch      │
│   transcript logger  │
└──────────────────────┘
```

### Implementation

- **`src/cube/tools/`** — one Python module per tool. Each function: type-annotated signature, structured dict return, fully unit-tested. Tools are pure functions where possible; the policy tool wraps `model.forward()` and caches the loaded model.
- **`src/cube/agent/`** — Anthropic API client + conversation loop. Uses the native tool-use API. ~150 lines.
- **`scripts/run_agent.py`** — CLI entry: takes a scramble, runs the agent, returns annotated solve + full transcript.

### Why Anthropic tool-use, not MCP

MCP is for portable long-running tool services. We're building one demo for one model. Native tool-use in the Anthropic API is simpler, more direct, easier to log, easier to iterate on.

## Eval methodology

Two test sets:
1. **Hand-picked 3 scrambles** (the ones we've been using all along). Used during development.
2. **10 random WCA corpus scrambles** (seed=0, same as `benchmarks/baseline_*.md`). For final video comparison.

For each scramble:
- Log every tool call + reasoning step in a transcript.
- Verify the final move sequence solves on the engine.
- Record total moves + time-to-solve.
- Compare against:
  - Our own `--fast` analyzer: 31.0 mean.
  - Our own NISS-on analyzer: 32.7 mean.
  - The human reconstruction (corpus-recorded).
  - (Optional) mallard's output on the same scrambles.

## Scope honestly

- **Day 1 (today)**: design doc + core tool module + agent loop skeleton + first end-to-end attempt.
- **Day 2-3**: iterate on tool surface based on failure modes; tune prompts.
- **Day 4-5**: run eval harness on 10 scrambles; record session for video.
- **Day 6-7**: edit video, write companion blog.

Total: ~1 week of focused work, or 2-3 weekends of casual.

## What we keep from existing code

- `cube/engine/` — unchanged. `State`, `Move`, NISS frame helpers, cancellation.
- `cube/classifier/features.py` — used by `inspect_state` tool.
- `cube/classifier/htr.py` — used by `htr_subset` tool. **PDB lookups stay internal** (testing only).
- `cube/training/model.py` — wrapped by `policy_intuition` tool.
- `cube/analyzer/insertions.py` — used by `lookup_commutator` and `find_insertions` tools.
- `cube/analyzer/triggers.py` — used by `lookahead` tool.

## What we drop / hide

- `cube/analyzer/skeleton.py`'s `find_skeleton` becomes internal — it's the baseline reference, not a public tool.
- `--fast` / `--no-niss` CLI flags remain for benchmarking but aren't surfaced to the agent.
- Beam search at width 8192 stays for the analyzer baseline benchmark only.

## Open design questions

- **Lookahead budget**: depth 4 vs depth 5? Width 30 vs 50? Pick by what feels human; document the budget in the video.
- **Multiple policy calls per state**: is calling `policy_intuition` 100 times on the same state cheating? Probably yes if the LLM does it to enumerate. Maybe rate-limit per state.
- **How much hand-holding in the system prompt**: do we explain FMC concepts, or trust the LLM's training data? Probably explain — most LLMs know EO/DR/HTR vaguely but not crisply.

## Status

- [x] Design doc
- [ ] Tool module skeleton
- [ ] Anthropic agent loop
- [ ] First end-to-end attempt
- [ ] Iterate on failure modes
- [ ] 10-scramble eval
- [ ] Video recording
