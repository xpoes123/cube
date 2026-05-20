# FMC Retrospective — WesternSicilyOpen2026 S1

**Scramble:** `R' U' F U2 F2 D2 B2 D B' U L' B' F2 R2 U' L2 F2 B2 D' F2 L2 F R' U' F`

**Submitted:** 29 moves (attempt 2) — `D R U2 F' D2 F2 L2 U2 R2 D2 F2 R2 U R2 U' R2 F2 U' B2 U' R' F2 U2 R' D' B2 L2 B2 U2`
**WCA reference (Marcucci):** 19 moves
**Nissy axis-locked (UD):** 33 moves

The 10-move gap to Marcucci is the entire price of committing to a full UD pipeline. She skipped HTR and went EO → DR → direct 2c3+2e finish on inverse; I locked into UD-DR-2C4E and paid 17 moves for HTR-reduction + finish on a 2-swap long-cycle subset.

---

## Initial scout

`inspect_state` on the scramble: bad-edge counts **UD=4, FB=6, RL=4**. UD bad slots {UB, DF, DL, FL}; RL bad slots {UB, DL, DB, BR}.

Two clean 4-bad axes and a 6-bad I immediately discarded. The closeness signals were the real tell: UD pre-EO was tagged DR-4C3E with "2 pairs on inverse" — a textbook NISS prompt. RL pre-EO sat at DR-6C2E, considerably worse. I never seriously considered FB.

Plan going in: scout EO on UD normal, UD inverse, RL normal; pick by joint EO+DR cost, not EO alone.

---

## Draft 1 — SOLVED in 31, ~724s sim

- EO (2 on inverse): `L' F'` — UD axis from inverse, 2-move EO
- (attempted DR via dr_recognize brain iteration: `D U2 F2 D2 F2 R R L2 D'` — 9mv, never reached DR)
- **RESET**
- EO (4): `D R U2 F'` — UD axis normal
- DR (8): `D2 F2 D R U' R F2 R` — DR-2C4E (5-setup + 3-trigger), lands on DR-UD with 5qt corners
- HTR reduction (9): `U' R2 U' L2 U R2 F2 B2 U` — 2-swap long-cycle subset
- Finish (10): `D2 F2 U2 L2 D2 R2 F2 R2 U2 R2`

**What I was thinking.** The 2-move inverse EO `L' F'` was obviously seductive: 2 vs 4 against the normal-side `D R U2 F'`. I committed, then ran `dr_trigger_options(axis=UD, depth=5)` on the post-EO inverse state and got **zero hits across 98k visited states**. That's a hard signal — the named-trigger catalog can't reach DR within 5 moves of setup, meaning the residual is structurally far.

I tried to salvage it with `dr_recognize`, chasing brain probabilities: D (25.3%) → U2 (44.6%) → F2 (99.7%) → D2 (80%) → F2 (99.3%) → R (99.3%) → R (57.7%) → L2 (84.3%) → D' (61.6%). After 9 RZP moves still no DR, and the hard rule "DR ≥ 10 is unrecoverable" was firmly violated. **Reset.**

Back on normal, `dr_trigger_options` returned the clean menu:
- DR-2C4E: `R F2 R` trigger, 5-setup + 3-trigger = 8 (pre=DR-4C1E)
- DR-4C4E: `R U2 F2 R` trigger, 5+4 = 9 (pre=DR-4C2E)

I picked 2C4E for the shorter setup and better substate. `try_alg` confirmed DR-0C0E post-trigger with 5 qt corners. HTR classifier returned **2-swap long-cycle, 9+10 split** — no shortcut. Executed straight through.

**Where it fell short:** zero post-HTR refinement. I had 27 tool calls remaining when I finished and explicitly chose not to call `replace_and_shorten` because I read the gate as ≥30. That's the entire delta to the 29-move submission — leaked 2 moves to gate paranoia.

---

## Draft 2 — SOLVED in 29, ~689s sim (SUBMITTED)

- EO (4): `D R U2 F'` — UD normal
- DR (8): `D2 F2 D R U' R F2 R` — DR-2C4E, same trigger as draft 1
- HTR + finish (raw 19): same as draft 1 → 31mv pre-refinement
- `replace_and_shorten` on tail: −1 (30mv)
- Cancellation pass: U2·U' → U: −1 (29mv)

**What I was thinking.** Same scout pattern: confirmed `L' F'` on inverse-UD (2mv), confirmed `dr_trigger_options` returns nothing within 5 on that state, abandoned inverse without burning further calls on `dr_recognize` — that was the explicit lesson from draft 1. Committed to normal-UD `D R U2 F'`, same DR-2C4E trigger, same HTR-reduction subset.

The actual improvement came **after** reaching the 31-mv raw solution. With 46 calls remaining I was safely past the gate, so I ran `replace_and_shorten` on the tail span. The substituter found a 1-move shorter substring covering the DR-trigger-into-HTR-reduction transition — essentially refactoring the boundary between the 8-move DR and 9-move HTR-reduction phases into a single 16-move block. Then standard cancellation collapsed `U2 U'` → `U` in the finish join.

The submitted decomposition is properly read as:
- EO (4): `D R U2 F'`
- DR-into-HTR fused block (17): `D2 F2 L2 U2 R2 D2 F2 R2 U R2 U' R2 F2 U' B2 U'`
- Finish remainder (8): `R' F2 U2 R' D' B2 L2 B2 U2`

Calling out that this isn't a clean EO/DR/HTR/finish decomposition anymore — `replace_and_shorten` shuffled moves across the DR/HTR-red boundary. The 8-move tail still includes a quarter-turn `R' ... R' D'`, which means HTR was achieved later in the refactored block than in the raw solution. Good outcome, not a clean phase narrative.

---

## Draft 3 — SOLVED in 29, ~710s sim

Pure replay of draft 2's pipeline. Same `D R U2 F'` EO, same DR-2C4E trigger, same raw 31, same `replace_and_shorten` → 30, same cancellation → 29. Identical final solution string. Useful as a sanity check that the path is robust; no new information.

---

## Draft 4 — SOLVED in 29, ~748s sim

Started identically: confirmed inverse 2-mv EO, confirmed empty `dr_trigger_options` on inverse-UD, reset to normal. Then took a small detour — after committing `D R U2 F'`, I tried `dr_recognize` looking for a sub-8 DR. Got brain probabilities pointing at D'/L2/L'/U. Applied D', re-checked, still not in memory, rewound.

Then I noticed the prior 29-mv solution had `D R U2 F' D2 F2 ...` and tried `dr_trigger_options(depth=3)` directly from after `D R U2 F' D2 F2` (now at DR-4C2E). That returned **DR-2C4E with `D R U'` setup + `R F2 R` trigger = 6 moves** — meaning the full DR is effectively `D2 F2 D R U' R F2 R` (8mv), exactly the same DR I keep hitting from the depth-5 search at the post-EO state. Confirmed the path is canonical.

Finished raw 31, refined to 30 via `replace_and_shorten`, then 29 via cancellation. Same string as draft 2.

---

## Draft 5 — SOLVED in 31, ~674s sim

Same scout, same commit, raw 31. The difference: I noted "URGENCY CRITICAL — 9.3% time budget" before reaching DR. That was wrong — I had ~600s real wall left but mis-read the budget meter — and I shipped without running `replace_and_shorten`. Identical raw 31-move solution as draft 1.

**Where it fell short:** same failure mode as draft 1. The refinement pass was skipped under self-imposed time pressure that wasn't actually present. Worth −2 moves vs draft 2.

---

## Winning-draft analysis (draft 2)

The pipeline:

1. **EO scout & commit.** UD-normal `D R U2 F'` is the obvious 4-mv EO. The inverse `L' F'` 2-mv is a trap: post-EO `dr_trigger_options` returns empty at depth 5, meaning the residual is ≥6 setup moves to any named trigger, almost certainly costing more than the 2mv EO savings. The right reasoning is **joint EO+DR cost**, not EO standalone. Drafts that wasted calls on inverse-UD via `dr_recognize` brain-iteration all eventually came back to normal.

2. **DR trigger pick.** Menu was DR-2C4E (8) vs DR-4C4E (9). 2C4E priors: 10–12mv post-DR. 4C4E priors: 12–14mv. The 1-move savings to DR plus the better substate priors made 2C4E strictly dominant. Trigger: setup `D2 F2 D R U'` + classic `R F2 R` = `D2 F2 D R U' R F2 R`. Landed at DR-UD-0C0E with 5 qt corners.

3. **HTR subset.** Classified as **2-swap long-cycle** (cycle structure [3,2,2,1] on corners post-DR), 9+10 split. No 3-cycle shortcut available — `residual_class` after HTR returned "mixed" with 2 corner 3-cycles plus 2e2e edge pairs. Raw cost is locked at 19 from DR.

4. **Refinement.** This is where draft 2 won. `replace_and_shorten` on the tail span found a substitute one move shorter — refactoring the DR-into-HTR-reduction boundary. Then cancellation collapsed `U2 U'` → `U`. Total savings: 2 moves over the raw pipeline.

**Neighborhood alternatives I didn't explore:**
- DR-2C3 or 3C2E direct-solve probes off this DR-2C4E pre-state — none surfaced in the trigger menu but a 2c3+2e direct search would have been the only realistic path to compete with Marcucci.
- RL-axis DR (DR-6C2E pre-EO) was discarded without scouting DR cost. Possibly the right call given the 6C2E pre-substate, but never verified.
- FB axis was never scouted at all.

---

## Three-way comparison

**vs Marcucci (19, −10).** Her decomposition from commentary:
- `(L' F')` — EO on inverse-UD, the same 2-move EO I rejected
- `(L' D' R L2 D' R2 D)` — DR 4a1 on inverse, 7 moves
- `L' (L2 U2 F2 L' F2 L)` — direct finish, 7 moves (one normal-side move + 6 inverse)
- `(U2 F2 U2)` — final 3-move tail

Where she won: **she trusted the inverse 2-move EO and found DR 4a1 in 7 setup moves on the inverse side**, where my `dr_trigger_options` returned empty at depth 5. The 4a1 trigger family isn't in my named-trigger catalog at the depth I searched — or it required a longer setup the depth-5 BFS couldn't reach. She got to DR in 9 moves total vs my 12. Then she **skipped HTR entirely** with a direct 7-move finish (2c3+2e territory — corners reduce to a 2c3 with 2 edge pair, solvable directly without going through HTR). Her finish-from-DR was 10 moves vs my 17.

Net: she won 3 moves at DR (better setup) and 7 moves at finish (skipped HTR phase). Total 10.

**vs nissy axis-locked UD (33, +4).** Nissy on this scramble does EO(4) + DR(10) + HTR(8) + finish(11) = 33. My 29 beats nissy by 4 — that's the value of NISS-aware EO selection plus the `replace_and_shorten` boundary refactor. Specifically:
- EO: tied at 4 (`D R U2 F'` ≡ `R D2 B2 D` up to symmetry, both optimal on UD-normal)
- DR: I won 2 (8 vs 10) by hitting DR-2C4E directly
- HTR + finish: nissy 19, me 17 — won 2 via the boundary substitution

So the axis-locked optimal floor is 33, and a real solver with refinement tools can shave 4 off it without leaving UD. The remaining 10-move gap to Marcucci is **entirely** the HTR-skip strategy.

**vs prior LLM versions.**
- v19: 30 moves — same family of solution, raw pipeline with one refinement pass
- v24_n4: 31 moves — identical to my draft 1/5 (the raw `D R U2 F' D2 F2 D R U' R F2 R ...` line, no refinement)
- v25: 29 moves — different decomposition (`F U2 F L2 F D2 F' R2 F D2 R2 ...`), looks like an RL-axis or FB-axis attempt; matched my move count

Versions tied or improved across the board. The convergence on the same UD-DR-2C4E line across v19/v24/v25/this run is strong evidence the named-trigger menu is steering everyone into the same local optimum.

---

## What I'd change

1. **Add a 2c3+2e direct-solve probe after DR.** On this scramble, post-DR with 5qt corners and the residual edge structure, Marcucci finished in 10 moves by skipping HTR. A `direct_finish_options` or `dr_to_solved` search with depth ≤12 would have surfaced shorter solutions than going through HTR-reduction → finish. The 2-swap long-cycle subset's 19-move HTR cost is exactly when the direct probe pays off.

2. **Don't abandon inverse on empty `dr_trigger_options`.** I correctly read the empty depth-5 result as "named-catalog trigger is far" — but Marcucci's 7-mv DR 4a1 setup proves there's a viable DR within 7 moves on inverse-UD, just not in the named-trigger families I queried. Either widen the catalog or fall back to a generic DR-search (not `dr_recognize` brain-iteration, which I correctly identified as unreliable).

3. **Standardize the refinement gate.** Drafts 1 and 5 both shipped 31 because I either misread the tool-call gate or misread the time budget. `replace_and_shorten` + cancellation reliably saves 1–2 moves on a raw HTR-pipeline solution; running it should be a hard policy at the end of every solve where the raw count exceeds the median prior, not a discretionary call.

---

The submitted 29 was the best of a converged UD-pipeline strategy that's structurally 10 moves behind a competition-class HTR-skip on this specific scramble.
