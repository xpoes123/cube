# FMC Retrospective: fm_PSSSideDayGdansk2026_s2

**Scramble:** `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`

**Submitted:** 34 moves · **Marcin (WCA):** 20 moves · **Nissy axis-locked (UD):** 28 moves

The 14-move gap to Marcin came almost entirely from one decision: I committed to the EO→DR→HTR→finish pipeline on a scramble where the reference solver bypassed DR entirely with a direct 4b2/2e block-style attack out of EO. Inside the pipeline I also picked the wrong axis (RL instead of UD), leaking another ~6 moves vs nissy.

---

## Initial scout

`inspect_state` returned bad-edge counts **UD=6, FB=4, RL=4**. Standard read: FB and RL are the natural EO candidates (4 BE typically resolves in 1–3 quarter turns). UD's 6 BE looked scattered enough that I wrote it off as a 4–5 move EO axis, which — in hindsight — was wrong, since nissy finds `F L2 B D` (4) on UD.

EO scouting across both frames:

| Axis | Normal | Inverse |
|------|--------|---------|
| FB | `B2 L2 U2 R'` (4) | `U2 R'` (2) |
| RL | `R2 B F2 U'` (4) | 4 (partial: `D U' B' D'…`) |
| UD | 5 (partial) | `B R2 U F'` (4) |

The 2-move inverse-FB EO (`U2 R'`) was the obvious headline. Every attempt opened by scouting it.

---

## Draft-by-draft

### Draft 1 — SOLVED in 34, 1540s sim

**Phases (final, on inverse frame, then composed):**
- EO (4): `B R2 U F'` — inverse-UD, kills all 6 BE
- DR setup (6): `U D L' R U L'` — brain-guided, no `dr_trigger_options` hit
- DR trigger (4): `U2 R U R'` — DR-3C2E family
- HTR reduction (9): `U F2 U B2 U' B2 U R2 D` — 2-swap mostly-axial
- HTR finish (11): `R2 D2 R2 B2 D2 R2 U2 L2 U2 B2 U2`

**What I was thinking.** Opened with the 2-move `U2 R'` on inverse-FB. `dr_trigger_options(axis='FB', max_setup=5)` returned **nothing** — 97k states explored, zero family hits. `dr_recognize` fell through to brain with `R2` at 65%, which is the "I'm guessing" range. I bailed. Tried normal-FB after the 4-move EO: again no triggers ≤5. Tried normal-RL: one hit, **DR-7C8E with 5+3=8 setup+trigger**. The 7C8E substate is the worst common DR class — priors say 15+ move finishes — so 4+8+15 = 27+ floor, and that's optimistic.

Pivoted to UD. Normal-UD EO was 5; inverse-UD was 4 (`B R2 U F'`). After applying, `dr_trigger_options(axis='UD', max_setup=5)` returned nothing, and even bumping to `max_setup=6` capped back at 5 internally. Fell to brain-guided iteration: `U` (42%) → `D` (93%) → `L'` (98%) → `R` (98%) → `U` (99%) → `L'` (99%) — six moves of monotonically increasing confidence — until `dr_recognize` finally landed **DR-3C2E** with setup `U2` + trigger `R U R'`.

So total to DR was 4 + 6 + 4 = **14 moves**. The 3C2E label is misleading here though: the HTR classifier returned "2-swap mostly-axial" with 9+11 = 20 moves post-DR, not the 6–8 the 3C2E prior implies. That meant 34 total. I checked the `replace_and_shorten` gates (tool calls remaining 23 < 30), declined, and submitted.

**Where this fell short.** Two leaks. (1) Six wasted setup moves chasing the brain on UD before reaching a known trigger — nissy's UD DR is 7 moves (`B' L F' R' B2 R' F`) from EO, I spent 10. (2) The HTR-finish phase was 20 moves on what's nominally a friendly substate; nissy's UD HTR+finish is 9+8=17.

### Draft 2 — SOLVED in 34, 967s sim

**Phases (normal frame, RL axis):**
- EO (4): `R2 B F2 U'` — kills RL's 4 BE
- DR setup+trigger (8): `R B' D2 R' B' F' L B` — DR-7C8E, with one `B`/`B'` cancellation netting it down
- HTR reduction (11→ ~10 after cancellation): `B2 R U2 R F2 R2 B2 D2 R F2 R`
- HTR finish (12): `U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`

**What I was thinking.** Same scout: inverse-FB 2mv looked great, no DR. Normal-FB no DR. Normal-RL → the same DR-7C8E in 8. This time I just took it rather than chasing UD with the brain. 7C8E classified as **2-swap long-cycle** at HTR, 11+12 = 23 post-DR. Total floor was 12+23-cancellation = 34.

Tried `replace_and_shorten` on span `[4:34]` (everything after EO). Returned `could not solve micro-scramble: no DR found` — the same wall I'd hit in scouting. Submitted.

**Where this fell short.** Identical move count to draft 1 but a fundamentally worse pipeline choice. I committed to the *known* trigger (RL-7C8E in 8) over the *uncertain* path (UD-3C2E via brain, total 14). That avoided sim cost but the substate penalty made up the difference exactly. Net wash at 34. The real miss: I should have tested normal-UD's DR after the partial-5 EO, or pushed `max_setup=6` harder.

### Draft 3 — SOLVED in 34, 660s sim

Effectively a faster re-run of draft 2. Same scout sequence (FB-inverse 2 / FB-normal / RL-normal), same DR-7C8E commitment after `dr_recognize` on FB-inverse went in circles (R2 65% → F2 66% → L 41% / D 39% — confidence collapsed, indicating off-path). Same 34-move composition. `replace_and_shorten[4:34]` failed identically. Two sentences of new content over draft 2.

### Draft 4 — FAILED (sim_budget)

Scouted all four (axis, side) pairs again, applied `U2 R'` inverse-FB, hit the no-trigger wall, fell to `dr_recognize`, bailed back to normal-RL, found the same DR-7C8E in 8, ran out of sim time at the HTR classification step. Twelve tool calls, no submission. The scout phase had become ritualized — I was re-deriving the same map every attempt instead of caching the insight that RL-normal DR-7C8E is the floor of the "fast" branch and UD-inverse 3C2E-via-brain is the floor of the "slow" branch.

---

## Winning-draft analysis (Draft 1, 34 moves)

`U2 B2 U2 L2 U2 R2 D2 B2 R2 D2 R2 D' R2 U' B2 U B2 U' F2 U' R U' R' U2 L U' R' L D' U' F U' R2 B'`

This is the composed-and-inverted form. On the inverse frame the construction was:

1. **EO (4):** `B R2 U F'` — orients all 6 UD bad edges. Optimal for inverse-UD; nissy's normal-UD EO is also 4 (`F L2 B D`), so EO was not the leak.
2. **DR setup (6):** `U D L' R U L'` — pure brain-walk. No theoretical justification I can defend; the brain just kept pushing confidence up. The `U D` opener simultaneously broke and re-set corner parity in a way that exposed a 3C2E trigger. Nissy's setup to DR is 7 moves *including* the trigger — my 6+4=10 leaks 3 here.
3. **DR trigger (4):** `U2 R U R'` — DR-3C2E. Composed setup-into-trigger had a `U`/`U2` adjacency but no cancellation.
4. **HTR reduction (9):** `U F2 U B2 U' B2 U R2 D` — the "2-swap mostly-axial" 9-mover from the classifier. Nissy's UD HTR is 9 moves (`U R2 U L2 B2 L2 U' R2 U`), so this phase was *on par* with optimal.
5. **HTR finish (11):** `R2 D2 R2 B2 D2 R2 U2 L2 U2 B2 U2` — this is the bleed. Nissy's UD finish is 8 (`U2 F2 U2 L2 F2 B2 D2 R2`). Three full moves leaked to a suboptimal HTR-coset solver.

Cancellation savings during composition: zero notable cancellations across phase boundaries in the inverse-frame construction. The `U2 R'` from my discarded inverse-FB scout did *not* persist — I'd reset.

Alternative neighborhood: the obvious one was committing to RL-7C8E (draft 2's choice) for 12 to DR + 23 post-DR. Identical total. The non-obvious one — and the one I never tested — was extending the UD brain-walk one step further before triggering, or backing off the `U D` opener to see if a 5-move setup existed.

---

## Three-way comparison

**vs Marcin (20 moves).** He skipped DR. His decomposition:
- `(U2 R)` EO on inverse — same 2-move EO I found on inverse-FB but he correctly identified it as the *right* axis to commit to despite the bad DR landscape.
- `(B U' B2 U F D B)` — a 4b2+2e direct attack, 9 moves. This is the move I didn't have in my toolkit. It's a 2c3+2e/block-style finish from EO that doesn't route through DR at all.
- `U F2 U'` to HTR (12 total).
- `L2 U2 B2 L2 B2 U2 L2` slice insertion to finish (19+1=20).

His commentary — "Found in 20 minutes, didn't feel enough… missed a fairly easy 18 from extending different 9+2 into 10+2" — tells you this scramble has a *direct-from-EO* attack so strong that DR is dominated by it. My 14 moves to DR is more than his entire EO+blocks total. **Marcin wins +14 from picking the right strategy class.**

**vs nissy axis-locked (28 on UD).** Nissy commits to UD-pipeline and gets EO 4 / DR 7 / HTR 9 / finish 8 = 28. My draft 1 on the same axis got 4 / 10 / 9 / 11 = 34. So on the matching pipeline I leaked **6 moves**: 3 in DR (brain-walk vs optimal trigger) and 3 in HTR finish (subset solver vs coset optimal). EO and HTR-reduction were optimal. The "axis pick + NISS choice" was worth essentially **0** vs nissy — I picked the same axis (UD) on the inverse frame, nissy picked UD on normal, EO cost was identical at 4. The entire LLM gap to nissy is phase-execution.

**vs prior LLM versions.** Best prior was **v19/v24/v25/v26 at 26 moves** with the solution `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`. That's an inverse-frame solve opening `(D U' B' D' U' R) (F R F L F L F R) (U2 D2 L F2 D2 F2 B2 R2 L2 D2 F2 U2)` — i.e., RL-inverse EO into what looks like a direct EOFB-to-end attack rather than full DR. **The prior versions found a non-DR path on RL-inverse that I never explored.** v27b/v31 at 26 used yet another structure (`L2 B' F2 R2 U F L2 U' F R2 F U2…`) opening with an FB-axis line. So multiple prior versions independently found 26 on this scramble via non-pipeline solves. The current version (v33-ish) regressed by **8 moves** because I locked into the EO→DR→HTR→finish template and refused to recognize that the DR landscape was hostile.

---

## What I'd change

1. **When `dr_trigger_options` returns nothing on the short-EO axis AND `dr_recognize` brain confidence is <70%, abandon the pipeline.** Don't fall through to brain-walk. Instead invoke a direct-from-EO probe — a "2c3+2e attack" or "blocks-after-EO" tool — exactly what Marcin used. Three of four drafts hit the no-trigger wall on inverse-FB and *all three* burned moves anyway.
2. **Cache the scout across drafts.** Drafts 2/3/4 each re-derived "FB-inverse=2, FB-normal=4, RL-normal=4 with DR-7C8E in 8, UD-inverse=4 with no triggers." That's ~8 tool calls of sunk cost per draft. A scratchpad summary at the top of attempt 2 would have freed sim time for the direct-solve probe.
3. **HTR finish leaks 3 moves consistently.** The "2-swap mostly-axial" 11-mover came back identical across attempts and is 3 over nissy. Either the HTR coset solver is using a precomputed sequence per subset (and missing 3-move optima), or it's not considering all four axis equivalences. Worth auditing the classifier's finish output against a true HTR-finish optimizer.

A scramble where the WCA reference solved in 20 and prior LLM versions hit 26, but I locked into a DR pipeline that floors at 28 and executed at 34 — a 14-move avoidable loss that started with one strategic refusal to leave the EO→DR template.
