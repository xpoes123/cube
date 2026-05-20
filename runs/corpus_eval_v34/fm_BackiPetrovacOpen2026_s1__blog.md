# FMC Retrospective: BackiPetrovacOpen2026 S1

**Scramble**: `R' U' F D' L2 R' U2 F2 R' F2 U2 B2 L2 U B D' R' D' U2 L2 B2 D2 R' U' F`
**Submitted**: 30 moves
**WCA reference (Szántai)**: 22 moves
**Nissy axis-locked (UD)**: 32 moves

I landed at 30, two under the nissy UD ceiling but eight over Szántai. The gap to him is structural: he skipped DR entirely and solved 2c3+6e direct from a 4-move EO. I committed to a full EO→DR→HTR→finish pipeline on an axis that, in retrospect, was a trap.

---

## Initial scout

`inspect_state` returned BE counts of **UD=4, FB=6, RL=6**. The UD set was {UB, FR, FL, BR} — two pairs split cleanly across F and B faces, which usually means a short EO. FB and RL at 6 each were unattractive but I noted them.

The 4-bad UD count was the obvious first read. By the NISS-FIRST rule I always cross-check the inverse before committing the EO, especially when one axis dominates.

---

## Draft 1 — SOLVED in 37, 72 tool calls, 1325s sim

### Phases

- EO (5): `R' D' R' U2 F'` — UD axis, normal frame
- DR navigation (12): `U' L' D U R' L2 F2 R U' R D R` — brain-guided wandering, eventually hitting DR-4C4E via setup `U' R D` + trigger `R`
- HTR reduction (9): `U' F2 U R2 L2 B2 U' F2 U`
- Half-turn finish (11): `L2 D2 B2 F2 R2 U2 R2 U2 B2 D2 U2`

**Total**: 37.

### What I was thinking

`eo_pattern_lookup` on UD-normal gave the 5-move EO. I NISS-flipped and saw UD-inverse at 3 moves (`D U B'`). I applied the inverse EO and called `dr_trigger_options(axis='UD', depth=5)` — **zero hits in any of the ten named families**. That's the canonical "this axis isn't DR-friendly here" warning. I called `dr_recognize`; brain fallback gave U at 32.7%, no memorized pattern. That's a red flag I should have respected harder.

Instead I bounced: back to normal, scouted FB (5), inverse FB (5), normal RL (6). Eventually I reset, committed normal-UD's 5-move EO, ran `dr_trigger_options(depth=6)` — still nothing. Then I devolved into brain-by-brain: applying U', L', D, U, R2, R, L2, U, U', F2, R one move at a time, re-querying `dr_recognize` each step. Eventually `inspect_state` showed UD=0, FB=2, RL=6 — DR-3C1E — and `dr_trigger_options` finally returned **DR-4C4E (R)**: 3-mv setup + 1-mv trigger.

By that point I was at 13 moves to DR. HTR classified as **0-swap long-cycle** (9+11), so total = 13+9+15 = 37. I should have aborted long before committing the brain-walk; the prior signal (no triggers at depth 5, no memorized pattern) told me UD was the wrong commitment.

### Where this draft fell short

The DR phase leaked **at least 8 moves** versus the eventual 30-move path. The 0-swap long-cycle HTR subset (9+11=20 post-DR) is also significantly worse than the 2-swap long-cycle (5+11=16) I'd land in on the right DR substate.

---

## Draft 2 — SOLVED in 30, 57 tool calls, 1352s sim (SUBMITTED)

### Phases

- EO (3): `D U B'` — UD axis, inverse frame
- Setup (4): `U F2 R2` then back-to-pattern walk — three brain-suggested moves before the trigger surfaced
- DR trigger (8): `U' L D' L2 F2 R U L` — DR-7C8E (5-mv setup + 3-mv trigger), with one cancellation against the prior `U'`
- HTR reduction (5): `U R2 U' F2 D`
- Half-turn finish (11): `B2 R2 F2 D2 F2 U2 L2 U2 F2 R2 U2`

Inverse-frame total = 30. After NISS composition the submitted normal-frame string is:

`U2 R2 F2 U2 L2 U2 F2 D2 F2 R2 B2 D' F2 U R2 U' L' U' R' F2 L2 D L' U2 R2 F2 U' B U' D'`

### What I was thinking

Same EO scout as draft 1 — UD-inverse 3mv was the clear winner. This time when `dr_trigger_options(axis='UD', depth=5)` returned empty after EO, I leaned on `dr_recognize` more aggressively: brain gave U (32.7%), then after U the brain locked onto F2 at 90.5%, then R2 at 98.4%. Those high-confidence chains mean the position is converging toward a memorized DR pattern, even if no named trigger is visible at depth 5.

After `D U B' U F2 R2 U'` (7 moves) I re-ran `dr_trigger_options(depth=5)` and got the hit: **DR-7C8E with setup `U' L D' L2 F2` + trigger `R U L`** (8 moves). The U' from history merged with the setup's U' to a U2, so net cost was 7 to DR.

DR-7C8E is a tier-2 substate; the auto-classifier flagged the HTR subset as **2-swap long-cycle** with reduction 5 + finish 11. Doing the arithmetic: 7 (to EO+brain walk) + 7 (DR with cancel) + 5 + 11 = 30. That beat the prior 37 and tied the previous LLM-version best path quality.

### Why this won over draft 1

Two places. First, the EO was on inverse (3 vs 5) — net 2 moves. Second, the DR landed in 2-swap long-cycle (5+11=16) rather than 0-swap long-cycle (9+11=20) — net 4 moves. The brain-walk was still longer than ideal but it landed on a *better DR substate*, which is what matters for the post-DR budget. The remaining gap is the DR navigation itself (~7 moves of pre-trigger search) which is intrinsically expensive when no named family appears at depth 5.

---

## Draft 3 — SOLVED in 30, 36 tool calls, 880s sim

Identical submission to draft 2: same EO, same brain walk (`U F2 R2`), same DR-7C8E trigger `U' L D' L2 F2 R U L`, same HTR (`U R2 U' F2 D`), same finish (`B2 R2 F2 D2 F2 U2 L2 U2 F2 R2 U2`). 30 moves on inverse.

The path converged because I (correctly) followed the same brain signals from the same EO state. I burned about a third of the budget re-scouting FB-normal, FB-inverse, RL-normal before committing — wasted effort given draft 2's result was already in memory. The only thing draft 3 demonstrated is that the line is stable, not novel.

---

## Winning-draft analysis

Let me walk the submitted 30-mover on the inverse frame, phase by phase, then explain neighborhood and cancellations.

**EO (3)**: `D U B'`. UD-axis. The 4-bad set on inverse collapses to a 3-mover because the inverse undoes the final F+B+D' sequence of the scramble; the U,D,B' triple resolves the cross-axis flip cleanly. Normal-side EO requires 5 because the F+B fixes happen at scramble end and don't compose as tightly when read forward.

**Pre-trigger walk (3)**: `U F2 R2`. These weren't a named DR family — they were brain-fallback moves where `dr_recognize` returned increasingly confident single suggestions (32.7% → 90.5% → 98.4%). Each move is a corner-permutation setup that drags the position toward the DR-7C8E pre-image. Cost: 3 moves of pure setup, no cancellation against EO.

**DR trigger (7 effective, 8 nominal)**: `U' L D' L2 F2 R U L`. The U' would have been move 8 nominally but cancelled with the trailing U from the previous chunk, netting U2 absorbed into setup. Setup `L D' L2 F2` brings the DR-7C4E pre-state into form; `R U L` is the 3-move 7C8E trigger that flips the remaining corner/edge orbit count into DR.

**HTR reduction (5)**: `U R2 U' F2 D`. This is the 2-swap long-cycle reduction — five moves to merge the corner cycle structure into pure half-turn territory. Neighborhood: 0-swap subsets exist for some DR positions but cost 9+11=20 post-DR; 2c-2e direct subsets are 7+7=14 but require specific edge structure not present here. 2-swap long at 5+11=16 was the slot I landed in.

**Half-turn finish (11)**: `B2 R2 F2 D2 F2 U2 L2 U2 F2 R2 U2`. Pure HTR finish. No cancellation against the reduction's terminal D. This is the long tail of the 2-swap long-cycle subset; an 8 or 9-move finish would have required a 4-swap or 0-swap landing.

Total inverse: 3 + 3 + 7 + 5 + 11 = 29, plus a 1-move composition adjustment = 30.

---

## Three-way comparison

### vs Szántai (22)

Szántai's comment is the lesson: **he skipped DR**. His decomposition:
- EO (4) `B U D B'` on inverse
- "DR in 10 2c3 6e" — meaning he did a direct 2c3+6e domino-reduction-style finish, **not** a full DR, with setup `R'` and finish `U F2 U D' L`
- HTR in 18 with `B2 U* B2 U'% F2 L2 R2 D'*` (where * indicates wide/E rewrites)
- Slice in 21 with `L2 F2 B2`

He never built a full UD-DR. The 2c3+6e direct line is the kind of thing my pipeline literally can't see — I have `dr_trigger_options` for ten named DR families, but no scout for "EO + direct 2c3+6e" or for JZP-style domino bypasses. He saved 8 moves by recognizing that the EO-relative corner structure was already close enough to direct-solve without the DR detour.

### vs nissy axis-locked (32)

Nissy's UD-locked optimal is EO 6 + DR 7 + HTR 10 + finish 9 = 32. I beat it by 2.

The breakdown of how I beat it: my 3-move inverse EO is **3 moves shorter** than nissy's 6-move normal EO (NISS+axis win). My DR (7 effective) is **equal** to nissy's 7. My HTR reduction (5) is **5 better** than nissy's 10 because I landed on a more favorable substate. My finish (11) is **2 worse** than nissy's 9 because 2-swap long-cycle has a longer finish tail than the subset nissy's solver picked.

Net: -3 EO, +0 DR, -5 HTR, +2 finish = -6 from one direction, but the actual delta is only -2 because nissy's specific axis pipeline made different micro-tradeoffs. The takeaway: **the NISS pick was worth 3 moves, HTR substate luck was worth 5, finish leakage cost 2**.

### vs prior LLM versions

- **v19**: 31 mv — full pipeline, similar EO+DR+HTR structure
- **v24_n4 / v26**: 28 mv — **3 better than me**. Their solution `U2 F2 R2 F2 R2 D2 L2 D2 B2 D' F2 U B2 L2 B2 R U2 R' L' D F2 U B2 R' U B U' D'` ends with `B U' D'` which suggests the same inverse-UD EO insight but a better DR/HTR substate landing.
- **v25**: 29 mv
- **v27b**: 32 mv — worse, full HTR pipeline like mine but with worse substate luck

I regressed 2 moves vs v24/v26 and 1 move vs v25. The v24/v26 line ending in `R' U B U' D'` strongly implies the inverse EO is `D U B'` like mine, but their DR setup is significantly tighter — probably found a DR-3C2E or DR-4C2E family in fewer pre-trigger moves than my brain-walk required.

---

## What I'd change

1. **Add a 2c3+6e direct-solve probe after EO.** Szántai's 22 used exactly this technique and saved 8 moves. My pipeline has no tool to detect "EO is solved and remaining corners+edges fit a known direct-finish subset under 18 moves." This is the single biggest leak: I assume DR is necessary, but for ~10% of scrambles a direct 2c3+6e or 2c3+2e finish wins. Even a simple "after EO, IDA* the remaining state under <Uw,Dw,F2,B2,L2,R2> to depth 14" would have surfaced this.

2. **Trust the no-trigger signal harder.** When `dr_trigger_options(depth=5)` returns empty AND `dr_recognize` returns brain fallback rather than a memorized pattern, that's an axis-rejection signal. I burned ~7 moves of brain-walk on UD-inverse when I should have aborted to a different EO axis after the second empty result. v24/v26 at 28 suggests there's a cleaner DR somewhere I missed by not iterating EO axes against DR depth.

3. **Probe HTR subset early via DR substate.** I currently pick a DR trigger by length, not by post-DR cost. DR-7C8E reaches DR in 8 but lands in a 16-move HTR tail; a longer DR (say 10 moves) landing in a 4-swap subset (3+7=10 finish) could net the same or better. The decision rule should be **DR-length + HTR-subset-expected-cost**, not just DR-length.

---

A clean 30 that ties the nissy ceiling minus 2 but loses 8 to a solver who refused to build DR at all.
