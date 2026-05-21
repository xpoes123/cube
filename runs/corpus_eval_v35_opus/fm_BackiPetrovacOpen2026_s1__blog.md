# FMC Retrospective: BackiPetrovacOpen2026 S1 — A DNF I Have to Own

**Scramble:** `R' U' F D' L2 R' U2 F2 R' F2 U2 B2 L2 U B D' R' D' U2 L2 B2 D2 R' U' F`
**My submission:** DNF (both drafts failed within the hour)
**WCA reference (Szántai):** 22 moves
**Nissy axis-locked (UD):** 32 moves

The gap is not a phase-execution gap. It's a strategy gap: Marcin skipped DR entirely and went 2c3+6e direct from EO, landing at 10-move DR-in-disguise and finishing with a clean HTR+slice. I committed to a UD EO→DR pipeline twice, got jammed in a 2C0E corner residual, and burned my hour trying to escape it instead of restarting on a different axis or running a direct EO→HTR probe.

---

## Initial scout

`inspect_state` on normal: UD=4 bad edges, FB=6, RL=6. The UD-4 split was clean — FR/FL on the F-face, UB/BR on the B-face — but no single quarter turn fixes it, so I knew UD EO-normal would cost 4–5 moves with a setup. I tried the NISS frame immediately:

Inverse scramble bad edges: UD=4 still, but the geometry was different and my pattern recognizer flagged a 3-mover. Specifically `D U B'` killed all four UD bad edges on inverse. That's the strongest EO seed on the cube — beats UD-normal (5), FB and RL on both frames (all 4). I committed to inverse-UD without hesitation.

This is also where my first strategic error lived: I never scouted whether the post-EO state was a good DR candidate. I just took the cheapest EO and walked forward, instead of probing 2c3+2e or direct-finish options the way Marcin did.

---

## Draft 1 — FAILED (wall_clock, 595s, 138 tool calls)

### Phase moves as actually played (inverse frame unless noted)

- **EO (3):** `D U B'` — UD-inverse, kills all 4 bad edges
- **DR attempt A (3):** `L' U' L` → lands at DR-2C2E
- **DR attempt A continuation (4):** `F2 D' F2 R` → DR-2C0E (4 moves, 7 total to DR-corner-residual)
- **Stuck.** Extended with `R2 F2 U' L2` (4 more, 11 total) chasing closure, still RL=4 bad edges. The brain kept routing me through 0-edge / 2-corner residuals that needed a 7–8 move corner commutator I couldn't compose under pressure.

### What I was thinking

After `D U B'` the state was DR-4C3E on UD. `dr_trigger_options` and intuition both highlighted three 3-move triggers landing at 2C2E. `L' U' L` was the first I committed to; it took me to 2C2E with what looked like a clean continuation. `F2 D' F2 R` then collapsed the slice-edge debt and dumped me at **DR-2C0E** in 7 moves total.

That's where the trap closed. 2C0E with two twisted corners and no edge debt is a JZP-eligible state, but the corner residual on this scramble needed an EO-breaking trigger (R or L, not a half-turn) and a long setup. My intuition kept proposing half-turn finishes (`R2`, `F2`, `U'`, `L2`), which can't repair corner twist inside ⟨U,D,R2,L2,F2,B2⟩. I burned ~4 moves on dead-end half-turn extensions before I noticed all I was doing was permuting edges while the corners stayed twisted.

I rewound and tried `R' D R2 U' R` as an alternate DR closure — landed at **DR-0C2E** instead (5-move DR, 8 total). Better residual class (edges-only) but the brain immediately led me into `L U2 D2` which kicked me back to 4C3E. I rewound again.

Then I reset entirely and tried a different post-EO continuation: `D U B' F2 D R`, then attempted `L' U' L F2 D' F2 R` (8 total). This actually landed at DR-2C0E **with FB-EO also coincidentally solved** — a strong state, both EO axes good, only corner twist remaining. `htr_classify` returned "could not compute HTR phases for this subset" — meaning my state wasn't reducible inside the toolset's HTR coset, which should have been a loud warning to abandon DR-on-UD entirely.

I didn't listen. I tried `R2 F2 U' L2` extending to 12 moves, still 4 bad RL-edges. Tried `B2 U F2 D` on FB axis (also 0C2E). NISS-flipped to normal frame to check (UD=6, FB=4, RL=8 — worse). Flipped back. Started running pure finish intuition on a state that wasn't in the finish coset.

### Where this draft fell short

Two layered errors:

1. **EO selection optimized cost, not downstream quality.** The 3-move `D U B'` was locally cheapest but landed me in a UD-DR coset where the corner residual was structurally hard. Marcin's 4-move EO `B U D B'` (inverse) cost 1 move more but set up a 2c3+6e direct solve that skipped DR.
2. **No abort criterion.** Once I was 8+ moves in on inverse with HTR classify failing, I should have hard-reset and tried RL or FB axis, or run a 2c3+2e probe. Instead I kept patching. Final move count when wall_clock fired: ~36 moves on the slot, not solved.

---

## Draft 2 — FAILED (unknown cause, 66s, 18 tool calls)

No narrative was captured for this draft. From the tool count and sim-time it looks like an aborted restart — possibly I tried a fresh axis scout, made one or two commitments, and the run terminated before composing a submission. With 18 tool calls there wasn't enough budget to reach DR even on the best EO seed, let alone finish.

This was effectively a wasted draft. Given draft 1 consumed 595s of sim time out of a ~660s budget, draft 2 was triage with no real chance.

---

## Winning-draft analysis

There is no winning draft. For accountability, here is what the submission *should* have looked like if I'd executed the path Marcin found.

Marcin's solution decomposed (normal frame, with his inverse-prefix `(B U D B')` shown as `B D' U' B'` on normal):

- **EO (4) on inverse:** `B U D B'` — UD axis
- **2c3+6e direct (6) on inverse, with `(R')` premove:** `U F2 U D' L` plus an `R'` premove on normal — this is the key insight: he didn't aim at DR. He aimed at a 2-corner-3-cycle + 6-edge state directly reachable from EO, which is a much richer target coset than DR-4C2E.
- **HTR reduction (8):** `B2 Uw B2 U' E2 F2 L2 R2 D' Dw` (notating his `U*`, `%`, `D'*` rewrites)
- **Slice finish (3):** `L2 F2 B2`

Total: 22.

The critical move was treating EO output as input to a **direct 2c3+ne search**, not a DR search. On this scramble the EO state happened to be 6 moves from a JZP-eligible 2c3+6e position, which is roughly the cost of a single DR trigger — except it skips the entire HTR-corner-coset bottleneck that ate my hour.

Nissy's 32-move UD-axis-locked path confirms this. Even with perfect EO (6mv), perfect DR (7mv), perfect HTR (10mv), perfect finish (9mv), the pipeline ceiling is 32 because the UD DR-coset for this scramble is structurally bad. The 10-move HTR phase is the tell — Nissy's HTR alone is longer than Marcin's entire HTR+slice (11 moves combined). The DR pipeline was the wrong tool.

---

## Three-way comparison

**vs Marcin (22):** I lost 14+ moves and a successful submission. He won by recognizing that EO-then-direct-2c3+6e was viable on this scramble and skipping DR entirely. His `(R'), U F2 U D' L` is a premove-aware 6-move direct solve to a JZP state — exactly the kind of probe I should have run after EO and didn't.

**vs nissy axis-locked (32):** Nissy proves the DR pipeline on UD caps at 32 even with optimal phase play. I got DNF, so my pipeline execution lost ∞ moves. But more usefully: **if I had executed UD-DR optimally I'd have been at 32, still 10 moves behind Marcin.** Axis choice and EO-output strategy were worth 10 moves on this scramble, dwarfing any phase-optimization gain. This is the single most important number in this retrospective.

**vs prior LLM versions:** Every prior version solved this scramble. v24_n4 and v26 both landed 28, v34 at 30, v25 at 29, v19 at 31, v27b at 32. The previous best (28) was already 6 moves behind Marcin but at least submitted. I regressed from "consistently 28–32 with submission" to DNF. The regression vector is clear from the transcript: too much time on a single DR branch, no abort-and-restart discipline, no direct-finish probe after EO. v24_n4's solution `U2 F2 R2 F2 R2 D2 L2 D2 B2 D' F2 U B2 L2 B2 R U2 R' L' D F2 U B2 R' U B U' D'` shows the prior version was finding a UD-pipeline solve and shipping it; I tried to do better and got nothing.

---

## What I'd change

1. **Add a hard 2c3+ne / direct-finish probe immediately after EO commitment, before any DR trigger.** On this scramble, a 6-move probe from EO would have surfaced Marcin's path. Specifically: after `D U B'` (or `B U D B'`), run a depth-6 search targeting JZP-eligible cosets, not DR-4C2E. If the probe returns anything ≤7 moves, take it over DR.

2. **Set a per-branch move budget and a phase-failure abort.** When `htr_classify` returns "could not compute HTR phases for this subset" — that's a structural signal the DR coset is bad, not a request to keep grinding intuition. Rule: if HTR classify fails on a DR state, abort the branch within 2 moves and switch axis.

3. **Reserve 30% of wall budget for draft 2.** I spent 595/660s on draft 1, leaving 66s for draft 2 — not enough to reach DR on a fresh axis. Cap draft 1 at ~400s with a hard timeout, even mid-branch, and use the remaining 250s for a clean axis-shopped second attempt.

---

DNFing a scramble that every prior LLM version solved is the worst possible outcome, and the lesson is procedural — know when to abandon a branch — not analytical.
