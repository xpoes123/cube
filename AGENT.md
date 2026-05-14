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

---

# Human FMC Theory (from Hitchhiker's Guide to FMC, Yurii Riabov, 2024)

Distilled for agent reasoning. Three families coexist in the guide:
**CFOP** (sub-40), **blockbuilding + insertions** (sub-30), **DR + HTR** (sub-22,
what top solvers use).

## 1. Pipeline as a human plays it

Top-level order for the DR+HTR branch:
**EO -> RZP -> DR -> HTR -> Finish**, with NISS available at every stage.

One-hour time budget (per the guide):
- 5-10 min: enumerate all short EOs (write them down)
- up to 30-35 min: check each EO and search for DR
- remainder: solve the best DR through HTR and finish

NISS is *not* a separate stage - it's a frame switch (`A B'` final) used
opportunistically at specific decision points (see section 7).

For blockbuilding branch: 2x2x1 -> 2x2x2 -> 2x2x3 -> F2L-1 + EO, then
skeleton-based corner insertions instead of OLL/PLL.

## 2. EO recognition

EO = orient all 12 edges so finish needs no F/B quarter turns (per axis).

- Humans target EO in **<=5 moves**, preferring 3-4. The guide recommends
  writing out *all* EOs up to 5 moves across both axes (and inverse via NISS)
  before committing.
- Recognition: count "bad" edges per axis (FB stickers on U/D/L/R sides for
  F/B axis EO). Parity must be even.
- The 4-move EO case set, the 6-bad-edges 5-move-optimal set, the 8-bad-edges
  5-move-optimal set, and all sub-6 EOs are catalogued - top solvers have
  effectively memorized them via the EO trainer.
- NISS triggers during EO: if the side has reduction to 4 bad edges in 1
  move, check the inverse via NISS tracing.

## 3. DR axis pick + move count

DR = `<U, D, R2, L2, F2, B2>` reachable. Built on top of an EO.

- After EO, do **RZP** (1-3, max 6 quarter moves) to land on a **trigger**:
  - `R` -> DR-4E4C
  - `R U2 R'` -> DR-2E4C
  - `R U/U' R'` -> DR-2E3C
- Always check **both perpendicular axes**.
- Picking axis: ARM (axial-reduction-minus) scoring on each axis. ARM
  switches between axes after NISS, so if normal has bad DR-4E4C but the
  other axis ARM is e.g. AR-1C1E, NISS gives a 34%-ish chance of sub-7 DR.
- JZP (axial reduction without quarter turns on the DR axis) gives much
  shorter expected DR finishes; worth pursuing even at length 6.
- Typical full EO+RZP+DR = 9-13 moves for strong solvers.

## 4. HTR for humans

HTR = `<U2, D2, R2, L2, F2, B2>` reachable. Distance from DR = 0-5 leftover
**quarter turns** (qt) of U/D.

- Workflow: count qt on corners, reduce/raise to 1-2 qt, setup to canonical
  triggers `R`, `R U2 R'`, or `R U2 F2 R`.
- Yes, humans recognize **HTR subsets by name** (4b2, variation hell, etc.).
  Subset identification drives expected finish length and which corner method
  to use. "Hyperparity" is the advanced corner method for 3+ qt cases.
- Resources cite "Corner Case Funnel" and HTR subset stats tables; subset
  recognition is a learnable visual skill.

## 5. Finish structure

After HTR, every state solves in **<=14 moves**. Options in increasing
sophistication:

1. **Direct finish**: solve corners + as many edges as possible, then known
   edge commutators. Brute trial.
2. **Floppy Reduction (FR)**: reduce along DR axis to `<R2, L2, F2, B2>`,
   then solve domino layers ignoring middle E-slice edges. Not universally
   loved at the top but useful in many cases.
3. **Leave-slice / VR**: solve everything but the middle E-slice, then insert
   slice moves with cancellations across NISS. `VR` is the systematic framework;
   `rNISS` is the heuristic.
4. **Double-slice reduction**: leave DR slice + another slice that cancels
   across NISS.

Old CFOP-style finish (F2L+OLL+PLL on top of EO) is workable but rarely
optimal.

## 6. Insertions (blockbuilding branch)

Workflow:
1. Build F2L-1 + EO.
2. Solve the **edges** (often via the last F2L edge cleverly placed to
   solve LL edges too).
3. Classify remaining corner state.
4. Insert corner commutators where they cancel best.

"Pure" 3-corner commutators are 8 moves and affect only 3 corners; they can
be slotted anywhere in the skeleton. Solubility:

- 1 comm: `3c`
- 2 comms: `3c1t, 2c2c, 5c, 3c3c, 2t, 3t`
- Worse (`4c1t, 3c2t, 4t, 5t`, ...): redo edges; not worth pursuing.

Insertion search happens **after** the skeleton is complete, not during.

## 7. NISS - when to switch frames

NISS is always legal, never mandatory. The guide's explicit switch triggers:

- During EO search: switch to find a 3-move EO on inverse when normal is 4.
- After EO: switch only if multiple equally-short EOs exist on this axis.
- After RZP-5 (or RZP-6 for `2e3c` or JZP cases).
- ARM-based: if other-axis ARM stats imply higher sub-7 DR probability.

Mechanically: final solution is `A B'` where `A` was the normal sequence and
`B` the inverse sequence. `A' S' B` rejoins normal; `A B'` is the answer.

## 8. Blockbuilding

The guide treats blockbuilding as the entry technique above CFOP:
2x2x1 -> 2x2x2 -> 2x2x3 -> F2L-1, optionally with **pseudo blocks** (blocks
that are off by a single U-face turn, exploited via NISS).

Still used inside DR pipelines opportunistically when the scramble offers
short partial structure that survives EO.

## 9. Move-count budget (strong solver)

| Stage | Moves |
|------|-------|
| EO | 3-5 |
| RZP | 1-3 (max 6) |
| DR finish | 3-7 |
| HTR | 4-8 |
| Finish (HTR -> solved) | 6-12 |
| **Total** | **21-24** (typical sub-22 mean) |

Blockbuilding alternative: F2L-1+EO ~18-22, then skeleton + 1-2 insertions
= ~28-30 total.

## 10. Implications for our agent's tools

We already have: state inspection per axis, policy transformer, cancellation,
NISS frame switch, commutator lookup, residual cycle classifier, HTR subset id.

Gaps to add (or expose more sharply) based on the guide:

- **EO enumerator** that returns *every* EO of length <=5 across all 3 axes,
  both normal and inverse - this is the gate to everything.
- **RZP / trigger search** restricted to the trigger family
  (`R`, `R U2 R'`, `R U/U' R'`) with axis tagging and DRM/ARM tags on output.
- **ARM/JZP classifier** evaluating both axes simultaneously and returning
  predicted sub-7 DR probability (statistical table lookup).
- **DR finish solver** restricted to `<U, D, R2, L2, F2, B2>`.
- **HTR qt counter + subset namer**; HTR finish solver to canonical setups
  (`R`, `R U2 R'`, `R U2 F2 R`).
- **Leave-slice / VR slice-insertion finder** (333.fm/sf-equivalent).
- **Insertion finder** with cancellation scoring (333.fm/if-equivalent),
  invoked only after a complete skeleton is in hand.
- **Move-budget tracker**: warn when a stage exceeds budget so the agent
  considers abandoning a branch.
- **Targeted NISS-switch helper** that fires only on the specific triggers
  in section 7, not at every node.

The agent shouldn't have a "solve from arbitrary state" tool - that's the
PDB heuristic line. Subset-finish lookup *after* subset identification is
fair (the human memorizes those).

## 11. System prompt content (8-15 lines, for `src/cube/agent/loop.py`)

```
You are an FMC (Fewest Moves Challenge) agent. Goal: produce the shortest
move sequence solving a given scramble. Strong human target is 21-24 moves;
acceptable target is <=30.

Default to the DR+HTR pipeline:
1) EO: enumerate every <=5-move edge orientation on all 3 axes, normal and
   inverse via NISS. Prefer 3-4 move EOs.
2) RZP: from each promising EO, search <=6 quarter moves to land on a DR
   trigger (R, R U2 R', R U R'). Check both perpendicular DR axes; use ARM
   stats to pick.
3) DR finish: stay in <U, D, R2, L2, F2, B2>.
4) HTR: count quarter-turns after DR, reduce to 1-2 qt, setup to R / R U2 R'
   / R U2 F2 R. Identify HTR subset by name when possible.
5) Finish: <=14 moves from HTR. Try direct corners+edge-comms first, then
   leave-slice (VR) or floppy reduction if direct is long.

NISS is always legal. Switch frames when: an axis has a 1-move route to
4-bad-edges, multiple equal-length EOs tie, RZP hits 5 moves, or the other
axis has strong ARM. Final answer format: A B' where A is normal-side
sequence and B is inverse-side sequence.

Stage move budgets: EO 3-5, RZP 1-3, DR finish 3-7, HTR 4-8, post-HTR finish
6-12. If a stage exceeds budget, abandon the branch and try another EO/DR.

Fall back to blockbuilding (2x2x2 -> 2x2x3 -> F2L-1 + EO, then skeleton +
corner-comm insertions) if DR+HTR yields nothing under 28 moves. Insertion
solubility: 3c=1 comm; 3c1t / 2c2c / 5c / 3c3c / 2t / 3t = 2 comms; worse
cases mean redo edges.

Treat preservation of partial structure (blocks, EO, DR) as a soft cost
balanced against total length, never as a hard constraint. Prefer
cancellations across stage boundaries over locally optimal stages.
```

