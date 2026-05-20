# FMC Retrospective — fm_PSSSideDayGdansk2026_s1

**Scramble:** `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`

**Submitted:** 36 moves. **Marcin (WCA reference):** 20 moves. **Nissy axis-locked (UD):** 35 moves.

The 16-move gap to Marcin is almost entirely structural: he abandoned the EO→DR→HTR pipeline after EO and solved directly out of a 2c3+2e skeleton, while I committed to the full pipeline and paid every phase in full. I also leaked moves inside the pipeline relative to nissy because I never landed a clean DR trigger — every axis I tried ended in a DR-0C2E / DR-2C0E / DR-0C1E trap.

---

## Initial scout

`inspect_state` on the scramble: bad-edge counts **UD=8, FB=6, RL=6**. UD is all-bad (the classic "needs NISS or accept a longer EO" flag), FB and RL are tied at 6, which usually means 4-move EOs are plausible on at least one of them.

EO probes across all four (side, axis) pairs:

- normal-FB: 5 moves (`R2 B' L' U2 R'`)
- normal-RL: 5 moves (`L U L2 R D'`)
- inverse-FB: 5 moves (`R F D' U' R'`)
- inverse-RL: 5 moves (`B U B2 F D'`)
- normal-UD: **4 moves** (`R2 D' B' F'`) — this one I only found later, while desperately scouting in Draft 3
- inverse-UD: 5 moves (`B' D' L' R' …`)

The UD=8 case turning into a 4-move EO is the classic "all-bad collapses cleanly" outcome. I missed it in Draft 1 because I assumed UD=8 meant NISS-or-bust and skipped it during the initial scout. That oversight cost me — but as it turned out, normal-UD post-EO also leaked into a 0C2E trap, so the EO savings would not have rescued the run.

---

## Draft 1 — FAILED (max_tool_calls), 314s, 80 calls

No moves submitted. The transcript is a tour of every (side, axis) pair followed by a brain-suggest tailspin.

**What I was thinking.** Standard "scout four EOs, commit the cleanest joint EO+DR." I lined up:

- inverse-FB post-EO → `dr_progress_options` returned **DR-2C1E in 3** (`D2 B U`), no named trigger.
- inverse-RL post-EO → **DR-0C2E in 4** (`L F2 R' F`), no trigger.
- normal-FB post-EO → **DR-0C2E in 4** (`F2 R2 B' D`).
- normal-RL post-EO → **DR-0C2E in 4** (`R2 D2 L F`).

I committed inverse-RL's 4-move DR-0C2E setup, then re-queried and saw **DR-0C1E in 4** but nothing hitting a trigger. Committed that → still stuck at DR-0C1E. Depth-5 search returned the same family. The pattern was identical across every axis: the residual 2C0E / 0C2E / 0C1E states cannot be cleared by EO-preserving moves alone, because the misplaced E-slice edges or misoriented corners form a parity-style trap that requires a quarter-turn on the EO axis (which breaks EO) to resolve.

I verified this by `try_alg`-ing `R`, `L`, `R L'`, `L R` from inverse-FB DR-2C1E — all of them broke FB-EO. So the BFS wasn't bugged; the state was genuinely depth-≥6 from full DR and the search horizon couldn't see it.

At call ~50 I panicked and switched to **brain_suggest** as a last resort. The brain emitted `L U R D' L2 U2 B2 R2 L2 F2 L2 R2 F2 U2 R2 L2 F2 U2 D2 R2 F2` — a confident sequence that visibly was not converging on a solved state. It transitioned from "eo" predictions to "finish" predictions while the cube was still scrambled, which means it was hallucinating a phase boundary. By call 80 I had 23 moves applied, no solve, and no time to recover.

**Where Draft 1 fell short.** I burned the entire call budget on scouting. I should have committed to inverse-FB at call ~15 instead of pinballing across four axes for 30 calls, then 15 more on brain_suggest. Even a 38-move solve would have been the submitted result.

---

## Draft 2 — SOLVED 36mv, 145s, 40 calls

The winning draft. I restored the `inv-FB-post-EO` bookmark from Draft 1 and committed hard.

- **EO (5)** [inverse]: `R F D' U' R'` — inverse-FB axis, kills all 6 bad edges
- **DR setup (3)**: `D2 B U` — lands at DR-2C1E
- **DR extension (5)**: `D' F' U2 F D` — pushed depth to 5 to escape the DR-2C1E trap, lands at DR-0C1E
- **DR finish (5)**: `U' F2 R2 B2 D` — depth-5 again, completes DR. **Total DR: 13 moves.**
- **HTR reduction (7)**: `F L2 F2 D2 F' U2 B` — 2-swap long-cycle subset, cycle (5,2,1)
- **HTR finish (11)**: `F2 R2 B2 D2 L2 D2 R2 F2 U2 R2 U2`

Total on the inverse: **5 + 13 + 7 + 11 = 36**. `compose_niss_solution` inverted to:

`U2 R2 U2 F2 R2 D2 L2 D2 B2 R2 F2 B' U2 F D2 F2 L2 F' D' B2 R2 F2 U D' F' U2 F D U' B' D2 R U D F' R'`

**What I was thinking.** The bookmark told me Draft 1 had identified inverse-FB DR-2C1E in 3 as the cleanest substate, even though no named trigger fired. I committed `D2 B U` and re-queried — same family of "all options return DR-2C1E, no trigger." Instead of bailing like Draft 1, I **raised max_depth to 5** on `dr_progress_options`. That cracked it: `D' F' U2 F D → DR-0C1E`. Re-queried at depth 5 again: `U' F2 R2 B2 D → DR`. So the trap was real but the horizon was the fix — depth-4 BFS couldn't see through it.

After DR, `htr_classify` returned subset **2-swap long-cycle**, structure (5,2,1), 7-move reduction + 11-move finish. The classifier emitted the phases in chunks (`F L2 F2 D2` then `F' U2 B`; finish in three chunks of 4+4+3) and I applied them straight through.

I tried `replace_and_shorten` on the tail `[16:36]` (HTR-reduction + finish), but it returned "could not solve micro-scramble: no DR found" — the tail spans HTR which has no DR on the spanned substate, so r&s couldn't help. That used my 1-call cap.

**Where this draft was leaky.** The 13-move DR is the bleed. Elite DR on a 5-move EO is supposed to land in ≤7-8 moves; I spent 13 because the inverse-FB substate forced two depth-5 expansions instead of a clean trigger hit. The 11-move HTR finish is also long for HTR (typical is 8-10), reflecting the 2-swap long-cycle (5,2,1) being a worst-case subset.

---

## Draft 3 — SOLVED 36mv (resubmitted Draft 2's solution), 266s, 35 calls

I tried to optimize Draft 2's path. I restored `inv-FB-post-EO` and this time noticed `dr_progress_options` had a **DR-0C2E in 5** option (`F U R2 B' D`) — strictly better bad-piece count than the DR-2C1E that Draft 2 took.

Committed it, re-queried → stuck at DR-0C2E, same trap I knew from Draft 1. Tested `R`, `L` manually: both broke FB-EO. Rolled back, tried the **DR-2C0E in 5** sibling (`B' U' L2 F D`) — also trapped, also broke EO on any quarter.

I then reset and scouted **normal-UD's 4-move EO** (`R2 D' B' F'`) — the one I'd missed in Draft 1. Probed DR: `R → DR-2C2E`, committed, then `R2 L U L → DR-2C1E`, committed (8 total), then `R D L2 D' R → DR-0C1E` (13 total). Tested `R2` and `L2` to fix the last edge — neither worked. Same trap.

At that point I had burned 30+ calls confirming that **every axis on this scramble routes through a 0C2E / 2C0E / 0C1E parity trap that requires depth-5+ BFS to escape**. I gave up on improving and resubmitted Draft 2's 36-move solution verbatim.

---

## Winning-draft analysis

The 36-move submission breaks down cleanly:

| Phase | Moves | Count | Cumulative |
|---|---|---|---|
| EO (inv-FB) | `R F D' U' R'` | 5 | 5 |
| DR-2C1E setup | `D2 B U` | 3 | 8 |
| DR-0C1E push | `D' F' U2 F D` | 5 | 13 |
| DR finish | `U' F2 R2 B2 D` | 5 | 18 |
| HTR reduction | `F L2 F2 D2 F' U2 B` | 7 | 25 |
| HTR finish | `F2 R2 B2 D2 L2 D2 R2 F2 U2 R2 U2` | 11 | 36 |

Cancellation savings: zero. Every phase boundary was a clean half-turn or quarter-turn handoff with no overlap.

The 13-move DR is the entire pipeline cost of "this scramble has no clean trigger on any axis." The 7+11 HTR phases are nissy-optimal for the (5,2,1) subset I landed in. Nissy on UD axis-locked spent 10+10+10 = 30 post-EO; I spent 13+7+11 = 31 post-EO. So my pipeline execution **after the axis choice** was within 1 move of optimal.

The 4-move gap to nissy's 35 is mostly the EO: nissy spent 5 on UD (`L U R L2 D`), I spent 5 on inverse-FB. But nissy's 10-10-10 distribution vs my 13-7-11 shows I traded DR moves for HTR moves — net loss of 1.

---

## Three-way comparison

**vs Marcin (20 moves) — he won by 16.** His commentary:
```
R2 D F B'           // EO (4)
L B2 R D2 L' D'     // 2c3 2e (10)
(B2 L' U2 R2 U2 R F2 B2 D2 L')  // solve directly (20)
```
He found a 4-move EO on UD (which I missed in Draft 1 and only found in Draft 3), then went **straight to 2c3+2e** in 6 more moves — no DR phase at all. From a 2c3+2e skeleton he direct-solved the residual on the inverse in 10 moves. This is the classic "skip DR when 2c3+2e is reachable from EO" play that the WCA pipeline rewards. My pipeline has no probe for it. Even if I had found the 4-move UD EO, my DR-first heuristic would have walked me into the same 0C2E trap (which it did, in Draft 3).

**vs nissy axis-locked (35 moves) — I lost by 1.** Nissy committed UD, spent 5 EO + 10 DR + 10 HTR + 10 finish. I went inverse-FB, spent 5 EO + 13 DR + 7 HTR-reduction + 11 finish. My axis pick was effectively equivalent to nissy's UD on EO length (5 vs 5), but my DR leaked 3 moves to the trap and HTR-finish leaked 1; HTR-reduction recovered 3. Net: -1 to nissy. So the NISS+axis-choice was worth roughly nothing on its own, and I leaked 1 move via execution.

**vs prior LLM versions.** The interesting comparators are v24/v25/v26/v29/v30, all of which converged on the same 25-move solution: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`. Decomposing: `R2 D' F' B` (4mv EO on UD — same as Marcin's first 4), then `R2 F2 R2 U2 F2 D2 R2 D2 L2` (9mv DR/HTR-skeleton), then `U' B2 U' F2 U` (5mv) + `R U L2 D L D' L'` (7mv). That's a 25-move full pipeline with a much tighter DR.

v31/v32 hit 28 via what looks like a related 2c3+2e route. v34 reproduced v19's 30-move solution exactly: `R2 D' B' F' U' R' L2 U F2 R U2 R'` (12mv to DR) + `U F2 U' R2 U L2 U2 R2 F2 U'` (HTR reduction) + `B2 F2 L2 B2 L2 U2 B2 R2` (8mv finish). **This v** got 36, regressing 6 moves against v34 and 11 against v24-30's plateau.

The regression vs v24/v25/v26/v29/v30 is the headline failure: prior versions found the **normal-UD 4-move EO** on the first scout and committed to it cleanly. This version missed normal-UD entirely in Draft 1, then in Draft 3 finally found it but couldn't escape the DR-0C1E trap that the prior versions evidently solved through depth-5+ search (or via a different DR trigger I didn't probe).

---

## What I'd change

1. **On the EO scout, never skip an axis just because bad-edge count is high.** UD=8 looked like an all-bad-needs-NISS case to Draft 1, but it had a 4-move EO. The scout should `eo_recognize` all six (side, axis) pairs unconditionally before committing — that costs 6 cheap calls, not 30.

2. **When `dr_progress_options` returns no named trigger at depth 4 across all top options, immediately raise max_depth to 5 instead of probing siblings.** Draft 1 burned 20+ calls testing 4 different (side, axis) substates that all gave depth-4 no-trigger results; the actual unblock (Draft 2) was just `max_depth=5` on the first substate. Make the depth-bump the **first** retry, not the last.

3. **Add a post-EO 2c3+2e probe.** Marcin's 20-move solve and the v24-v30 25-move plateau both depend on this: after EO, before committing to DR, scan for a short 2c3+2e skeleton + direct finish. On scrambles where DR has structural traps (like this one), the 2c3+2e route is dramatically better. The cost is one extra tool family; the savings on trap-scrambles like PSSSideDayGdansk-s1 are 10-16 moves.

A 36-move solve on a scramble where Marcin found 20 and prior LLM versions found 25 is a regression I want to never repeat.
