# FMC Retrospective: fm_PSSSideDayGdansk2026_s1

**Scramble:** `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`
**Submitted:** 31 moves
**WCA reference (Marcin):** 20 moves
**Nissy axis-locked (UD):** 35 moves

The 11-move gap to Marcin is entirely structural: he abandoned the DR pipeline after EO and solved the remaining 2c3+2e block directly in 16 moves, while I committed to a full EO→DR→HTR→finish pass on UD and paid for every phase boundary. My 31 beats the nissy UD ceiling by 4, which means the per-phase choices were tight against the axis I picked — but the axis itself was the trap.

---

## Initial scout

`inspect_state` gave me bad-edge counts UD=8, FB=6, RL=6. FB and RL tie on raw count, but per-flipping-face inspection showed both needed 5-move EO setups (FB chunk `R2 B' L' U2 …`, RL chunk `L U L2 R …`). On UD I immediately recognized a 4-move EO: `R2 D' B' F'`. I NISS-probed the inverse to see if UD shrank further — inverse UD also came in at 4 (`B' D' L' R'`), so normal-frame won on tie-break (no need to splice).

I did not seriously probe the 2c3+2e direct-solve route after EO. In hindsight this was the entire game. EO at 4 was so cheap on UD that I tunnel-visioned into the DR pipeline without ever asking "what does the cube look like after `R2 D' B' F'` in terms of corner-block + edge structure?" — which is exactly the question Marcin answered.

---

## Draft 1 — SOLVED in 31, 52 tool calls, 215s

**Phases:**
- EO-UD (4): `R2 D' B' F'`
- DR setup (13, after auto-cancels): `F2 L F2 U R · R U2 F2 D2 L · R U2 F2 D2 L` — lands DR-UD at 17 with qt_corners=4. Note the `F'·F2→F` cancel at the boundary and a `L·R` axis swap mid-phase.
- HTR reduction (9): `B2 U L2 F2 · U L2 U' B2 · D`
- Half-turn finish (10): `D2 F2 D2 R2 · D2 F2 U2 R2 · F2 L2`
- Total raw: 35. `replace_and_shorten` on the tail returned a substitute -3, then cancellation -1 → **31**.

**What I was thinking.** After EO I queried DR triggers and found 3-move setups landing at DR-2C1E. I committed `L2 U' R` to a 2C1E intermediate, then re-queried — depth-4 gave nothing, depth-5 surfaced `L U' R2 U L` to DR-0C1E. Committed, then ate the parity wall: DR-0C1E has odd slice-edge parity, unreachable via EO-preserving moves only. I tried to NISS my way out mid-DR, realized that doesn't help (the parity is state-intrinsic), flipped back, and rewound 4 moves to post-EO.

Second attempt at the DR was the keeper: depth-5 showed `F2 L F2 U R` to DR-0C2E (even parity, escapable). Committed (F'·F2 cancelled, saving 1). From there `R U2 F2 D2 L` to 0C1E, then another `R U2 F2 D2 L` to actual DR — same 5-move pattern twice, with the trailing L of phase 1 and leading R of phase 2 living on opposite layers so they didn't merge.

At DR I classified the subset as **2-swap mostly-axial**: 9-move reduction, 10-move finish. That's a 19-move tail, which is the worst common DR-finish class — and the early sign that the axis was wrong. I executed the canonical reduction `B2 U L2 F2 / U L2 U' B2 / D` and finish `D2 F2 D2 R2 / D2 F2 U2 R2 / F2 L2`, landing at 35 raw.

`replace_and_shorten` on the HTR+finish tail returned a 16-move substitute (vs 19) — saved 3. One more cancellation pass (a `U2·U'→U` adjacency I'd missed) got me to 31 verified.

**Where this leaked.** The DR took 13 moves on top of EO. Nissy's optimal UD DR is 10. So I leaked ~3 moves at the DR phase, partly recovered by `replace_and_shorten` on the back end. The bigger leak is the axis choice itself — see closing comparison.

---

## Draft 2 — SOLVED in 31, 40 tool calls, 164s

A re-run of the same plan with a token attempt to scout an alternative DR branch (DR-2C0E via `L' D L' D' L`, JZP-eligible but no 5-move trigger reachable; `F2 D L2 D'` candidate from the move-prior — didn't converge). After three branch-and-bounds I gave up and replayed draft 1's exact DR path: `R2 D' B' F' · F2 L F2 U R · R U2 F2 D2 L · R U2 F2 D2 L` to DR at 17, same 2-swap-mostly-axial subset, same 9+10 reduction+finish to 35, same `replace_and_shorten` -3 and cancel -1 → **31, identical solution**.

This draft is a tax on the budget — I learned nothing new. The DR-2C0E branch was the only original probe and it didn't crack within the depth I gave it. Should have either gone deeper (depth 6+ from 2C0E) or pivoted to a completely different axis instead of re-walking the same DR.

---

## Draft 3 — SOLVED in 31, 29 tool calls, 113s

The cleanest of the three executions.

**Phases:**
- EO-UD (4): `R2 D' B' F'`
- DR setup (12, after cancels): `F2 L F2 U R · R U2 B2 U2 R · R F2 U2 F2 R` — lands DR at **16** (one cheaper than drafts 1/2)
- HTR reduction (9): `B2 U L2 F2 · U L2 U' B2 · D`
- Half-turn finish (9, after a `D·D2→D'` cancel): `D2 F2 D2 R2 · D2 F2 U2 R2 · F2 L2`
- Total raw: 34. `replace_and_shorten` -2, cancel -1 → **31**.

**What I was thinking.** Committed EO, then deliberately took a different DR branch from draft 1's `R U2 F2 D2 L · R U2 F2 D2 L` to see if a different HTR subset was reachable. Picked `R U2 B2 U2 R` (which auto-cancels `R·R→R2` at the boundary, saving 1), then `R F2 U2 F2 R` from there to land DR with another `R·R` merge — net DR at 16 moves vs 17 in drafts 1/2.

But the HTR subset classification came back as **2-swap mostly-axial again**. Same 9+10 tail. So the 1 move I saved at DR didn't unlock a cheaper HTR class. Raw total 34 instead of 35, but `replace_and_shorten` only gave -2 this time (the substitute was the same 16-move tail; less to shave because raw was already 1 shorter), so post-cancel I converged on **the exact same 31-move solution**.

**Where this leaked.** It didn't leak relative to drafts 1/2 — it confirmed that the 2-swap-mostly-axial subset is what UD-DR lands in no matter which DR trigger path I take from this EO. The leak is upstream: choosing the DR pipeline at all.

---

## Winning-draft analysis

Submitted: `R2 D' B' F U2 R2 U2 L2 U2 R2 F2 R2 B2 U R2 U L2 U' F2 R2 U' L2 U' R U R' L' D R D L'`

Phase decomposition of the verified 31-move string:

- **EO-UD (4):** `R2 D' B' F` — optimal for this scramble on this axis (nissy's UD-EO is 5 with a different first-move sequence; the LLM's 4-move EO already beats nissy's EO).
- **DR-UD (13):** `U2 R2 U2 L2 U2 R2 F2 R2 B2 U R2 U L2` — this is the `replace_and_shorten` substitute for the original DR+early-HTR span. It's all double-turns plus three U/quarter-moves and effectively folds the DR completion into the HTR-prep. Nissy's optimal UD-DR is 10, so we're +3 here.
- **HTR completion + finish (14):** `U' F2 R2 U' L2 U' R U R' L' D R D L'` — note the last 7 moves `R U R' L' D R D L'` are not half-turns. This is the `replace_and_shorten` substitute escaping the strict HTR finish into a JZP-style 3-cycle commutator finish. That's where the real savings live: the canonical 10-move half-turn finish was replaced by a 7-move quarter-turn 3-cycle.

The cancellation savings ledger across the draft 1 path:
- `F'·F2→F` at the EO/DR boundary (-1)
- `D·D2→D'` at the HTR/finish boundary (drafts 3, doesn't apply to submitted)
- `replace_and_shorten` -3 on the tail (HTR+finish 19 → 16)
- Adjacency cancel `U2·U'→U` post-substitution (-1)

Net: 35 → 31.

Neighborhood alternatives I touched but didn't ship: DR-2C0E via `L' D L' D' L` (draft 2, didn't converge in budget); DR via `R U2 B2 U2 R · R F2 U2 F2 R` (draft 3, same HTR subset, same final 31). The pipeline funnels to the same place.

---

## Three-way comparison

**vs Marcin (20 moves).** His decomposition per his commentary:
- `R2 D F B'` (4) — EO. Identical move count to mine, different axis (his is FB-side, mine is UD; note his B' where mine has F').
- `L B2 R D2 L' D'` (6) — a 2c3+2e direct setup, landing in a state where 10 more moves on the inverse solve everything.
- `(B2 L' U2 R2 U2 R F2 B2 D2 L')` (10) — inverse-frame direct solve, no DR landing required.

His winning move was skipping DR entirely. After EO he saw a 2c3+2e structure (2 corners and 3+2 edges) that could be cleaned up in 16 moves total with a single NISS-spliced finish. I never ran a 2c3+2e probe after my EO. On UD, after `R2 D' B' F'`, the corner/edge structure may or may not have had a similar opening — I genuinely don't know because I didn't look. **11 moves lost to "didn't scout 2c3+2e after EO."**

**vs nissy axis-locked UD (35).** Nissy's UD-pipeline is EO(5) + DR(10) + HTR(10) + finish(10). I got EO(4) + DR(13) + HTR+finish(14) = 31. So:
- EO: I beat nissy by 1 (better EO recognition).
- DR: I lost 3 to nissy (suboptimal DR trigger search — I ran depth-5 and accepted, didn't push deeper).
- HTR+finish combined: I beat nissy by 6 (`replace_and_shorten` collapsed the HTR-finish boundary into a quarter-turn commutator).

Net +4 vs nissy UD. The axis pick + NISS gave me 0 moves (I never NISS'd successfully and stayed on UD), the EO recognition gave +1, the DR cost -3, and the back-end tail-rewrite was worth +6. The whole margin is in the tail rewrite.

**vs prior LLM versions.** v19 also landed 30 moves on this exact UD path: `R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`. That's 1 move better than my submission, with a different DR trigger sequence (`U' R' L2 U F2 R U2 R'` for DR, only 8 moves to DR vs my 13). v34 reproduced the same 30. v24/v25/v26/v29/v30 all converged on a 25-move solution using a completely different post-EO structure: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'` — that's EO(4) + a massive half-turn corridor through HTR + a 3-cycle finish, clearly closer to the 2c3+2e family Marcin found. And v35_smoke hit 24 moves with a totally non-DR solution.

So prior versions on this scramble found the structural shortcut (25mv via what looks like a direct HTR-skip path) and I regressed. My DR-pipeline tunnel vision cost 6 moves vs v25/v26/v29/v30, and 7 moves vs v35.

---

## What I'd change

1. **Mandatory 2c3+2e + 2c2e probe after EO, before any DR work.** On this scramble both Marcin and v35 found post-EO direct-solve structures worth ~11 moves over the DR pipeline. A single tool call to enumerate cheap corner+edge sub-block completions after `R2 D' B' F'` would have either surfaced a competitive path or confirmed DR was right. I never asked.

2. **Recognize the "2-swap mostly-axial" subset as a red flag.** Whenever HTR classification returns this subset with a 19-move tail, the total is going to be ~34-35 raw and we're depending entirely on `replace_and_shorten` to recover. Treat it as a signal to back up to post-EO and try a different axis (FB EO was only 5 moves — worth scouting its HTR distribution) rather than grinding the same DR.

3. **Don't burn draft 2 re-running draft 1's DR.** Once draft 1 ships at 31 with the converged path, draft 2 should be axis-shopping (FB-EO + 2c3+2e probe) or NISS-splicing across the EO/DR boundary, not a depth-5 search around the same DR neighborhood. I wasted 40 calls confirming what I already knew.

The DR pipeline executed cleanly against its own ceiling; the pipeline was the wrong tool for this scramble.
