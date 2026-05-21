# fm_PSSSideDayGdansk2026_s1 — Retrospective

**Scramble:** `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`
**Submitted:** 31 moves. **Marcin (WCA reference):** 20 moves. **Nissy axis-locked (UD):** 35 moves.

The 11-move gap to Marcin is almost entirely a structural miss: he skipped DR and solved 2c3+2e directly from a 4-move EO, while I committed to a full EO→DR→HTR→finish pipeline and only clawed back moves via `replace_and_shorten` on the tail.

---

## Initial scout

`inspect_state` gave me bad-edge counts UD=8, FB=6, RL=6. UD is the worst axis for EO (8 bad edges almost always means a 4–5mv fix is hard to find, but here a clean one exists), and FB/RL are tied as the natural candidates. I queried EO patterns on every (frame, axis) pair:

- Normal FB: `R2 B' L' U2 R'` (5)
- Normal RL: `L U L2 R …` (5)
- Normal UD: `R2 D' B' F'` (4) — best on paper
- Inverse FB: `R F D' U' R'` (5)
- Inverse RL: `B U B2 F …` (5)
- Inverse UD: `B' D' L' R' …` (5)

UD-normal at 4 moves was tempting and is exactly the EO that v19/v31/v32/v34 latched onto. I should have known from the prior-version history that UD here pipes into a 0-swap long-cycle subset with no good direct-solve, but in the moment I treated FB-normal as the workhorse and UD as a backup. That choice cascaded.

---

## Draft 1 — 39 moves, FAILED to compete (used as fallback only)

**Phases (verified):**
- EO (5): `R F D' U' R'` — inverse-FB
- DR (12, after running through 2C1E → 2C0E → DR closures): `D2 B U U2 B' D F D U B D2 B' U` collapses on the inverse frame to a 12-mv block; total to DR = 17.
- HTR reduction (11): `F R2 F' R2 F R2 F2 D2 F' U2 F` — landed in 0-swap 2-cycle.
- Half-turn finish (11): `R2 D2 R2 D2 F2 L2 B2 R2 D2 F2 R2`

**What I was thinking.** I NISS-flipped because FB-normal looked parity-cursed at depth 5: every `dr_trigger_options(axis='FB')` candidate from the 4-move 0C2E state died at 0C1E. Inverse-FB also reached DR via 2C1E → 2C0E, but the HTR classifier reported **0-swap 2-cycle** (22-move finish from DR). I knew immediately that was bad — that subset is the worst common landing — but I went ahead because I needed a fallback in the bank.

I tried `replace_and_shorten` on `[5:39]` and it failed: the micro-scramble re-solver couldn't find any DR in the rewrite window. So I shipped 39 as a paper baseline and reset.

**Where it leaked.** Everything after move 17. 22-move HTR-to-solved is a structural loss; the EO and DR were fine.

---

## Draft 2 — 35 moves

**Phases (verified):**
- EO (5): `R2 B' L' U2 R'` — FB-normal
- DR (12, one auto-cancel from `U U → U2`): `F2 D L2 U` (→ DR-2C1E) · `F U' B U2` (→ DR-2C0E) · `F D2 F' U` (→ DR-FB)
- HTR reduction (10): `F' R2 U2 F D2 F' L2 F U2 B` — 2-swap long-cycle
- Finish (8): `L2 U2 F2 D2 F2 L2 U2 F2`

**What I was thinking.** Draft 1's lesson: the HTR subset matters more than the DR move count. Going back to FB-normal, I requeried `dr_trigger_options(axis='FB')` from the post-EO state. Depth-4 returned four DR-0C2E candidates and six DR-2C1E candidates. Draft 1 had implicitly tried a 0C2E path on FB-normal and hit parity. So this time I deliberately picked a 2C1E setup (`F2 D L2 U`) hoping the different residual would give a cleaner closure and, more importantly, a better HTR substate.

The chain went 2C1E → 2C0E in 4, then 2C0E → DR in 5 (the unique closure `U F D2 F' U`, with the leading `U` cancelling the trailing `U2` from the previous block, netting 4 effective moves in the last step). Total to DR: 17 moves — same as draft 1, but the classifier returned **2-swap long-cycle** (10+8 = 18 from DR) instead of 0-swap 2-cycle. Net: −4 moves.

`replace_and_shorten` on `[5:35]` failed (same "no DR found" complaint as draft 1).

**Where it leaked.** Nothing relative to draft 1 — strictly an improvement. The leak is vs Marcin: 17 moves to land DR, when Marcin's 4-move EO `R2 D F B'` led directly into a 6-move 2c3+2e block. I never probed for a 2c+2e direct-solve after EO.

---

## Draft 3 — 31 moves (submitted)

This is the same 35-move FB-normal pipeline as draft 2, banked first, then rewritten by `replace_and_shorten`.

**Submitted solution:** `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`

**What I was thinking.** I restored the `FB-EO-done` bookmark and tried three alternate DR paths from the post-EO state:
1. `F2 R2 B' D` (0C2E option 1) — confirmed parity wall at 0C1E.
2. `D2 F2 B' D` then `B U' B2 U` (different 0C2E geometry) — same wall.
3. `F2 U B2 D` (0C2E option 3) — also dead.

This confirmed draft 2's `F2 D L2 U` → 2C1E → 2C0E → DR was effectively the unique productive DR path on FB-normal. I committed it again, re-ran the HTR reduction (2-swap long-cycle, 10+8), and banked the verified 35. Then I called `replace_and_shorten` on the full span `[0, 35]` — and this time it returned a 4-move savings.

The substituted solution doesn't preserve the phase structure. The first 17 moves are a slab of half-turns that doesn't correspond to any clean EO+DR I could trace by hand:

`U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2` (12) · `B' R2 F' L2 R2 U2 F D' F' U' B` (11) · `L2 F D' R U D F' R'` (8)

What r&s found was almost certainly an HTR-finish-style start (12 half-turns) followed by a non-canonical reduction back through HTR/DR boundary, then a short non-axis-aligned tail. It's structurally weird — but it verifies, and it's −4.

---

## Winning-draft analysis

The 31-mover is, honestly, mostly the r&s tool's win, not my reasoning. What my reasoning bought me was:

1. Choosing FB-normal in draft 2 over the inverse-FB path from draft 1 (−4: 39→35), because I correctly diagnosed that draft 1's 0-swap 2-cycle was the bottleneck and that pushing through the 2C1E intermediate on FB-normal could land in a better subset.
2. Banking the 35 before invoking r&s, so the tool had a clean target.

The r&s win (−4: 35→31) was opportunistic. The fact that r&s succeeded on draft 3's `[0, 35]` span but failed on draft 2's `[5:35]` span is the lesson: I should have tried full-span r&s on draft 2 as well, which would have produced the same 31 a draft earlier and freed budget for further iteration.

Cancellation savings within my own composition: 1 move (the `U U → U2` between DR-2C0E setup and DR closure). Nothing else cancelled.

Alternatives in the neighborhood I rejected:
- UD-normal 4-move EO `R2 D' B' F'`. Prior LLM versions v31/v32/v34 went down this path and ended at 28–30 moves with a long HTR finish. v19 also got 30 here. The 1-move EO saving doesn't compensate for the consistently worse DR/HTR landings on UD for this scramble.
- Inverse-UD `B' D' L' R'`. Never probed — would have been worth one `dr_trigger_options(axis='UD', frame='inverse')` call.

---

## Three-way comparison

**vs Marcin (20 moves).** His commentary is explicit: `R2 D F B'` (4) is a UD-normal EO; `L B2 R D2 L' D'` (6) is a 2c3+2e direct solve to a 10-move state; then `(B2 L' U2 R2 U2 R F2 B2 D2 L')` (10) on the inverse solves the rest directly. He skipped DR and HTR as named phases entirely. The 11-move gap breaks down as roughly: −1 from his 4-move EO vs my 5-move EO, and −10 from his 16-move 2c3+2e+finish vs my 26-move DR→HTR→finish (12+10+8, with my r&s rewrite folding this into 26 net). The lesson is brutally clear: I never queried a 2c+2e direct-solve probe after EO. On a scramble where the EO-axis 2c3+2e is reachable in 6, that single tool gap costs ~10 moves.

**vs nissy axis-locked (35, UD).** Nissy's UD pipeline is 5+10+10+10 = 35. My submitted 31 beats it by 4. Decomposition of the win: I picked FB instead of UD (saved nothing on EO — both are 4–5 mv — but unlocked the 2-swap long-cycle subset, where UD here is locked into 0-swap long-cycle with a 10-move finish). My EO+DR was 17 vs nissy's 15 on UD (lost 2). My HTR was 10 vs nissy's 10 (tied). My finish was 8 vs nissy's 10 (saved 2). Net axis swap was worth roughly 0 by phase, and r&s contributed the −4. So: **axis/NISS choice was worth ~0; r&s was worth 4**. Without r&s I'd have shipped 35, exactly tying nissy.

**vs prior LLM versions.** The best prior was v35_smoke at **24 moves** — `F' U R U B2 R2 D2 U2 R D2 U2 F R D B L2 F' D U2 L2 U2 F' U R`. That's 7 moves better than me, and only 4 worse than Marcin. v35_smoke was clearly running a 2c3+2e-style probe or a much deeper NISS exploration (117 tool calls — three times my budget per draft). The 25-move cluster (v24, v25, v26, v29, v30) all share the same solution `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'` — that's a UD-normal EO into something that finishes in 21 moves post-EO, again strongly suggesting a 2c+2e probe. My 31 sits in the middle of the v31/v32/v34 cluster (28–30) and is worse than v24-30's 25. **I regressed against the median of the prior fleet.**

---

## What I'd change

1. **Add a 2c3+2e direct-solve probe immediately after EO**, on every viable axis (both frames). On this scramble Marcin's `L B2 R D2 L' D'` exists at depth 6 from the 4-move UD EO; v24/v29/v30 found something comparable at 25 total. Skipping this probe was the single biggest miss and cost ~6–10 moves.
2. **Always call `replace_and_shorten` on the full `[0, N]` span, not just the tail.** Draft 2 tried `[5:35]` and got "no DR found"; draft 3 tried `[0:35]` and got −4. The full-span call should be the default whenever I bank a complete solution with ≥30 moves remaining in the budget.
3. **Diversify the DR substate target before committing.** When `dr_trigger_options` returns multiple residual classes (0C2E vs 2C1E vs 2C0E), I should query `htr_classify` against the projected post-DR state for each candidate rather than picking on move-count alone. Draft 2 stumbled onto the 2-swap long-cycle by luck; this should be the default lookup.

A scramble where 4-move EO → 6-move 2c3+2e exists, and I shipped 31: the budget went into draft-1 cleanup instead of probing the structurally cheaper route.
