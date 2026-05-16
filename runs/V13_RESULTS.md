# v13 corpus eval — skeleton + insertion tools (partial landing)

The "human-shaped insertions" version. Mixed result: replace_and_shorten
delivered a big win on one scramble but increased per-scramble tool
usage enough to DNF another. Honest reporting.

## TL;DR

**v13: 4/5 solved, avg 28.2 vs human 20.5 (gap +7.7) on solved.**
v12 was 5/5 solved, avg 29.4 (gap +8.6).

Net: improved move count on the 4 that solved (-1.2 avg) but introduced
a 1-scramble regression in solve rate. Per-scramble cost went up
(more tool calls + r&s sim time).

## Per-scramble

| Scramble | v13 | v12 | Human | Δ v12 | Notes |
|---|---:|---:|---:|---:|---|
| **PSSS_s1** | **25** | 30 | 20 | **−5** | replace_and_shorten ×3, big win |
| PSSS_s2 | 30 | 30 | 20 | 0 | r&s didn't help |
| PSSS_s3 | 30 | 27 | 23 | +3 | regression — agent's path diverged |
| **BackiPetrovac** | **DNF** | 32 | 22 | — | hit 80-tool-call cap during recovery |
| WesternSicily | 28 | 28 | 19 | 0 | r&s gave no shortening |

## What v13 added

### New tools (3, plus the commutator table)
1. **analyze_residual** — classify what's left to solve (residual_class,
   perm cycles by slot name, twists/flips, is_pure_corner_3cycle flag).
2. **derive_corner_3cycle** — closed-form 8-move commutator lookup from a
   precomputed 432-entry table (covers all 112 corner 3-cycles × valid
   twist patterns).
3. **replace_and_shorten** — Tronto §3.10: re-solve a sub-span via the
   existing EO+DR+HTR pipeline; substitute back if shorter. Recursive
   reuse of v9-v12 tools, NOT new search.

### Tool was shipped but didn't activate
- **derive_corner_3cycle** — 0 calls across the corpus. The agent's
  natural pipeline goes straight from DR to SOLVED via HTR; it never
  lands on a 3c residual unless it stops short intentionally. The
  prompt suggests this but the agent picked the path of least resistance.
- **find_skeleton_greedy** — written but not exposed to the agent;
  greedy hill-climbing in DR group with beam 15 depth 15 produced 0
  insertable skeletons in testing (local maxima trap on mixed
  residuals).

### What DID work
**replace_and_shorten** carried v13. PSSS_s1: agent used it 3× to
substitute longer sub-spans with shorter pipeline-fresh re-solves,
dropping 30 → 25.

## What the honest gap-closer turned out to be

Pre-v13 hypothesis: closing the +9.4 gap requires commutator insertions
(named cycles, derived comms, AB3c-style skeletons). That's what FMC
literature emphasizes.

What v13 reveals: **the elite 20-25 move WCA solves are MOSTLY clean
DR-HTR pipelines, not insertions**. Looking at the 5-solver YouTube
transcript (yod7OCvJPI8), 4 of 5 elite solvers (Marcin's PSSS,
Alexandros, Cyprian, Tomi) finish in 20-25 moves with **zero
insertions** — they just have better DR/HTR-finish quality + judicious
NISS. Only Marcin's PSSS_s2 23-move PB uses an insertion (a 2e2e with
cancellation).

So the gap is really:
- ~5-7 moves: better DR/HTR quality (NISS, axis selection, etc.)
- ~1-3 moves: opportunistic insertions when the residual cooperates

replace_and_shorten captures the second category implicitly — it finds
shorter sub-solves via the same DR/HTR tools, equivalent to "redo this
chunk with fresh eyes." That's why r&s gave the big PSSS_s1 win and
nothing on the others — most spans were already near-optimal.

## What's missing for the remaining gap

1. **Slice insertions** (Levi WR technique, Tronto §3.8). M-move
   insertions on edge residuals; the "leave-slice skeleton" approach.
   Requires slice-move support in our move set. Defer to v14.

2. **NISS-aggressive solving**. Multi-flip workflows where the agent
   spends substantial effort on inverse-frame setups. We have niss_flip
   but the agent uses it 1-2× per solve; champions use it 3-4×.

3. **Skeleton recognition during HTR-reduction** (Pattern 1 from my
   analysis): between every apply_htr_phase chunk, call
   analyze_residual. If a 3c emerges, branch to derive_corner_3cycle.
   This is a PROMPT-only fix that requires no new code. Could deliver
   the remaining 2-3 moves on a subset of scrambles.

4. **Budget-aware r&s**: cap r&s calls at 1 per scramble OR don't
   trigger if tool-calls remaining < 30. Would have prevented the
   BackiPetrovac DNF.

## Cost

Session total: ~$77.50 of $100. v13 cost $1.07 for 5 scrambles. Tool
calls per scramble jumped from v12's 27-35 to v13's 43-80.

## File map

- `src/cube/analyzer/commutator_table.py` — 432-entry corner 3-cycle table
- `src/cube/tools/insertion_tools.py` — analyze_residual, derive_corner_3cycle,
  replace_and_shorten
- `src/cube/tools/skeleton_greedy.py` — greedy hill-climb (not exposed)
- `checkpoints/corner_3cycle_table.pkl`, `edge_3cycle_table.pkl`
