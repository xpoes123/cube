# v11 corpus eval — human-tools-only mode

The honest-human version of the agent. v10 still let the libraries
return 8-19 move blobs in single calls; v11 caps EVERY recall and
search tool at 4 moves per call, removes all wide-search tools, and
prompts the agent to compose multi-step plans by iterating.

Run against 5 real WCA-FMC scrambles pulled from api.333.fm with the
human champions' reconstructions for direct comparison.

## TL;DR

**5/5 solved, sim avg 30.2 vs WCA-champion avg 20.8 = +9.4 gap, $0.56.**

The agent is now doing real human-shaped composition (49→27→33 tool
calls per scramble, iterating in 4-move chunks). The remaining +9.4
move gap to top WCA solvers is almost entirely the **skeleton +
insertions** technique the agent doesn't have yet.

## Results

| Scramble | Sim | Human | Gap | Solver | Tools | Cost |
|---|---:|---:|---:|---|---:|---:|
| PSSSideDayGdansk2026 s1 | 31 | 20 | +11 | Marcin Chmielewski | 30 | $0.14 |
| PSSSideDayGdansk2026 s2 | 30 | 20 | +10 | Marcin Chmielewski | 27 | $0.10 |
| **PSSSideDayGdansk2026 s3** | **27** | 23 | **+4** | Marcin Chmielewski | 27 | $0.10 |
| BackiPetrovacOpen2026 s1 | 31 | 22 | +9 | Szabolcs Szántai | 33 | $0.12 |
| WesternSicilyOpen2026 s1 | 32 | 19 | +13 | Chiara Marcucci | 29 | $0.10 |

## What v11 changed (the "honest human" constraints)

| Tool | v10 (oracle-shaped) | v11 (human-shaped) |
|---|---|---|
| eo_pattern_lookup | Returns full 4-7 move EO | Cap 4 moves; partial reveal forces re-query |
| dr_recognize | Returns full 6-10 move DR + named trigger | If ≤4 moves: full + trigger family. Else: 4-move setup chunk, no trigger seen yet |
| apply_htr_phase | Returns full 9-13 move phase blob | Cap 4 moves; agent re-queries 2-3× per phase |
| lookahead | width=10, depth=5 | width=5 (policy-top-K), depth=4 |
| find_eo_algorithmic | Raw BFS up to depth 7 | **REMOVED** |
| find_dr_via_trigger | width=32, depth=8 beam | **REMOVED** |
| probe_dr_after_eo | Same wide beam | **REMOVED** |
| lookahead_wide | width=30, depth=6 | **REMOVED** |

Tool count: 22 → 18. Of the 18, only `lookahead`, `try_alg`, and the
three "pattern recall" tools do any search at all — and all of them
are capped at 4 moves of horizon.

Additionally, `inspect_state` was enriched with
`bad_edges_by_flipping_face` — for each EO axis, groups bad edges by
which flipping face they sit on. The LLM can SEE "F has 3 bad edges
on UD-axis → quarter-turn fixes 3, breaks 1" without mentally
mapping slot names to faces.

## What the LLM is actually doing now

From the v11 scramble1 transcript (49 tool calls, 30 moves):

**Turn 2**: "FB-axis: 8 bad edges — classic 'all-but-4' case which often has nice NISS solutions. For 6 bad edges, I expect 2-4 move EO solutions, potentially with nice symmetry patterns."

**Turn 4**: "Ah, I can't include the unknown 5th move in the probe. Since the EO patterns only gave me the first 4 moves of a 5-move sequence, I need to apply those 4 moves first, then get the final move, THEN I can probe DR. Let me try a different approach."

**Mid-solve**: Tries UD axis → applies 4 EO moves → re-queries → applies last move → tries `dr_recognize` → realizes the path is too long → **undoes 5 moves, resets the slot, tries FB axis instead**. Falls back, tries RL axis, resets again. Finally commits to FB, composes EO in chunks, then DR in chunks (3× `dr_recognize` calls), then HTR reduction in 3 chunks of 4, then finish in 3 chunks of 4.

This is **real iterative human-shaped reasoning visible in the
transcript** — every solve has 25-50 tool calls of trial, retreat,
re-evaluate, advance.

## What's STILL computer-like (the leakage)

Even with the caps, three things still leak omniscience:

1. **Each 4-move chunk is optimal toward the goal.** A real human
   visualizes 3-4 moves and picks what *looks* promising; the agent
   gets the truly-best 4 moves. Within each chunk, it's still oracle.
2. **`probe_dr_pattern` returns total_dr_length.** A human probes by
   trying triggers and seeing if DR appears; they don't know the
   optimal DR length without searching.
3. **`htr_classify` returns exact phase lengths.** Humans estimate
   from subset family — they don't know the precise PDB-optimal.

These three are the remaining "trained pattern library" residue. They
could be tightened further (return only a quality estimate, not exact
length) but it's a diminishing-returns refactor.

## What's genuinely human-shaped

- **4-move visualization horizon** for both lookahead and recall —
  matches a real solver's working memory
- **Composition by iteration** — apply chunk, re-evaluate, repeat
- **All strategic decisions** — axis choice, NISS, reset, ship — made
  by the LLM via narration
- **Trial-and-error visible** — undos and resets when paths don't work
- **Narration in FMC vocabulary** — the agent talks like a champion

## What explains the +9.4 gap

The agent currently runs EO → DR → HTR → finish as a raw optimal
pipeline. Real WCA champions use **skeletons + insertions**:

> Marcin's PSSS_s2 (20-move solve):
> ```
> (U2 R)                         // EO
> (B U' B2 U F D B)              // 4b2 2e (9)
> U F2 U'                        // HTR (12)
> L2 U2 B2 L2 B2 U2 L2           // slice (19), +1
> ```
> *"Missed a fairly easy 18 from extending different 9+2 into 10+2"*

Marcin found a 9-move skeleton (block + 4b2 2e setup), HTR at 12,
slice finish to 19. The "+1" is one corner left, fixed by a clever
1-move insertion. The whole thing is composed of recognized
sub-patterns and one well-placed insertion that cancels heavily into
the surrounding moves.

The agent doesn't have skeletons OR insertions. The analyzer module
has the code (`insertions.py`, `skeleton.py`) — exposing them is the
next iteration.

## File map

- `data/corpus_333fm.json` — 5 WCA scrambles + human solutions
- `src/cube/agent/fetch_333fm_corpus.py` — fetcher CLI
- `src/cube/agent/corpus_eval.py` — `--corpus-333fm` flag added
- `runs/corpus_eval_v11/` — 5 transcripts with rich narration

## Cost summary

Session total so far: ~$75 of $100. v11 cost $0.56 for 5 scrambles,
about 2-3× v10 due to longer transcripts (more tool calls per scramble).

## Next: V12

Add skeleton + insertion tools. Expose the analyzer's `find_skeleton`
and `find_insertions` as agent tools, but constrain them: the agent
must pick the skeleton TARGET ("leave 3 corners", "leave 3c1t",
"2e2e") and the LLM searches a small set of candidate insertion
points using the policy as a guide. The narration becomes "I see 3
corners off — let me look for a commutator that cancels into my
last 6 moves" — true champion texture.

That refactor closes most of the +9.4 gap.
