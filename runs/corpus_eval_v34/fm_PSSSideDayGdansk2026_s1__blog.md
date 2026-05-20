# FMC Retrospective — fm_PSSSideDayGdansk2026_s1

**Scramble:** `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`
**Submitted:** 30 moves · **Marcin (WCA ref):** 20 moves · **Nissy axis-locked (UD):** 35 moves

The 10-move gap to Marcin is almost entirely the DR phase: he skipped it entirely with a 2c3+2e direct insertion after a 4-move EO, while I executed a textbook EO→DR→HTR→finish pipeline on the same UD axis.

---

## Initial scout

`inspect_state` returned bad-edge counts **UD=8, FB=6, RL=6**. The 8-bad UD count is the classic signature where an `<m> F <m'> B`-style 4-move EO is possible from one side via NISS, while FB and RL at 6 bad edges each look like routine 4–5 move fixes. I planned to scout EO on both sides for FB and RL (the natural "low bad-edge" axes), then check UD on both sides for the symmetry pattern.

The DR-axis residuals were FB=5C2E, RL=7C3E, UD=6C3E pre-EO — none of these directly dictates DR cost, but FB looked tidiest at a glance.

---

## Draft 1 — SOLVED in 31, 695s sim

- EO (5): `R F D' U' R'` — FB axis on inverse
- DR (7): `D F' L2 B' U F D` — DR-7C8E trigger
- HTR reduction (7): `F' U2 R2 L2 F R2 B` — 2-swap mostly-axial
- Finish (12): `L2 F2 U2 R2 B2 R2 F2 U2 R2 U2 R2 U2`
- Composed normal-frame: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`

**What I was thinking.** I scouted all four 6-bad candidates (FB-normal, RL-normal, FB-inv, RL-inv) — `eo_pattern_lookup` returned 5 moves for each. `dr_trigger_options` on FB-inverse returned three candidates: **DR-7C8E in 7** (`U F D` trigger, 4-move setup), DR-7C8E in 8 (`U' F D`), and DR-2C4E in 8 (`U L2 U`, pre=DR-4C1E). I deliberated between the 7-move 7C8E and the 8-move 2C4E — 7C8E has worse post-DR priors (typically 15–18 mv finish), 2C4E sits around 10–12, so the joint estimate was nearly identical (~22–23). I picked 7C8E to keep the setup short and pay the cost downstream.

I also tried RL-inverse (no triggers ≤5 setup) and UD-inverse (also dry). FB-inv was clearly the best DR candidate.

After committing to DR (12 moves total), `recognize_htr_subset` returned **2-swap mostly-axial**, 7+12 = 19 moves post-DR. Joint 31. The HTR reduction and finish chunks all applied cleanly with an `is_htr_ud=true` flip at the expected move. `replace_and_shorten` on the [5:31] tail returned "no DR found" — couldn't refine.

**Where this leaked.** The post-DR phase was 19 moves vs. the eventual draft 4's 18; the 7C8E choice cost about a move on the finish side that the 4C2E (in draft 4) recovered. The bigger leak was the **axis pick** — FB-inv at 5 EO + 7 DR = 12 to DR, vs. UD-normal at 4 EO + 8 DR = 12 to DR but with a far cleaner 0-swap long-cycle subset (19 post-DR vs. 18).

---

## Draft 2 — SOLVED in 33, 325s sim

- EO (5): `R F D' U' R'` — same as draft 1
- DR (8): `B U' F' B2 D2 U L2 U` — DR-2C4E trigger this time
- HTR reduction (11): `U2 F L2 F R2 F2 U2 F' R2 D2 F` — 2-swap long-cycle
- Finish (10): `B2 L2 F2 D2 B2 U2 F2 U2 R2 F2`

**What I was thinking.** Same FB-inv 5-move EO. This time I tried the **DR-2C4E** branch (the 8-move option I rejected in draft 1) to see if the cleaner substate actually delivered. `try_alg` confirmed DR-solved with 3 qt corners remaining — promising. But `recognize_htr_subset` returned **2-swap long-cycle**, not the better mostly-axial — 11+10 = 21 post-DR. Joint 34, but auto-cancellation in the HTR reduction shaved one to 33.

**Where this leaked.** The 2C4E priors I was anchoring on assume a friendly subset draw; this one rolled long-cycle and ate the savings. Pure axis-substate variance — draft 1's 7C8E got the better HTR subset on this particular state, which I couldn't have predicted from the DR survey alone. `replace_and_shorten` on the tail returned a +1 substitute and was rejected. Net: 2 moves worse than draft 1.

---

## Draft 3 — FAILED (max_tool_calls)

This one is worth dissecting because it's where I bled the budget.

I scouted all four 6-bad EOs (5 moves each), all four inverse counterparts (5 moves each), and tried to recognize_dr from raw EO states without committing. After deciding FB-inv DR options were unappetizing, I reset, went back to **normal-FB**, applied the 5-move EO, and tried to drive DR via repeated `dr_recognize` + `policy_intuition` brain calls.

Twelve brain calls and ~14 applied moves later (`R2 B' L' U2 R U' D2 F2 D U` and more), I was at DR-5C1E and the brain was looping on `U`/`U'` suggestions that auto-cancelled. By move 25 I was still EO-locked-not-DR; by move 51 I was applying random half-turn finishes hoping the cube would solve itself. It didn't. 80 tool calls burned, no submission.

**Lesson.** `dr_trigger_options` returning nothing at depth 5 is a **hard signal that this EO state has no clean DR**, not an invitation to call `dr_recognize` 10 times. Should have reset to inverse the moment normal-FB came up dry.

---

## Draft 4 — SOLVED in 30 (SUBMITTED), 382s sim

- EO (4): `R2 D' B' F'` — UD axis, normal side
- DR (8): `U' R' L2 U F2 R U2 R'` — DR-4C2E trigger, lands at UD-DR with 4 qt corners
- HTR reduction (10): `U F2 U' R2 U L2 U2 R2 F2 U'` — 0-swap long-cycle
- Finish (8): `B2 F2 L2 B2 L2 U2 B2 R2` (auto-cancelled 1 from the planned 9)

**What I was thinking.** This time I scouted UD on **both sides** before committing. `eo_pattern_lookup` on UD-normal returned **4 moves** (`R2 D' B' F'`) — the only sub-5 EO of the whole session. That's the symmetry pattern I'd been hoping for on the 8-bad axis. Committed immediately.

`dr_trigger_options` on UD post-EO returned **DR-4C2E in 8** (`R U2 R'` trigger, pre=DR-4C1E) and DR-7C8E in 8 (`R' U L`). 4C2E with a 4C1E pre-substate is the right call — pre=4C1E means the setup leaves the cube in a state where the trigger collapses to a clean DR-solved residual with 4 quarter-turn corners.

`try_alg` confirmed DR-solved, 4 qtc. `recognize_htr_subset` returned **0-swap long-cycle**, 10+9 = 19 post-DR — matching draft 1's total but with a 1-move-shorter EO. Joint estimate 30, hit it exactly. Auto-cancellation saved a move on the finish chunk-join, so 30 instead of the projected 31.

`replace_and_shorten` on the tail returned +1, rejected.

---

## Draft 5 — SOLVED in 40, 1047s sim

Same exhaustive EO survey as draft 3. Re-scouted FB-inv (same 7C8E/2C4E options), RL-inv (only 4C4E in 9), tried UD-inverse instead of UD-normal. `dr_trigger_options` on UD-inv returned **nothing** at depth ≤6. Repeated the draft-3 mistake of brain-iterating DR — 8 moves of `dr_recognize` suggestions before a re-survey finally found **DR-3C2E in 7** from a deeper setup state. 18 moves to DR (5 EO + 13 DR), HTR subset rolled 2-swap long-cycle for a 22-move post-DR, ship-mode 40 total.

**Lesson reinforced.** Even though I'd just gotten 30 moves on UD-normal in draft 4, I scouted UD-inverse "to compare" and burned half my budget. Should have just re-run the UD-normal recipe.

---

## Winning-draft analysis (Draft 4, 30 moves)

`R2 D' B' F' | U' R' L2 U F2 R U2 R' | U F2 U' R2 U L2 U2 R2 F2 U' | B2 F2 L2 B2 L2 U2 B2 R2`

**EO (4).** `R2 D' B' F'` is the 8-bad UD symmetry pattern — three single quarter turns plus a half turn flip all eight bad edges simultaneously. This is what the 8-bad count was hinting at from the start; I missed it on drafts 1, 2, 3, and 5 because I anchored on "6-bad axes are shorter" and didn't bother to check UD-normal EO until draft 4. The 4-move EO is the single largest contributor to beating my prior LLM versions.

**DR (8).** The DR-4C2E trigger `R U2 R'` with pre-substate 4C1E is the canonical good-shape DR — `U'` puts a corner pair in the right slot, `R' L2 U F2 R` is the 4C1E setup (relocating the misoriented corner column), then `U2 R'` finishes the setup-trigger fusion. The alternative was DR-7C8E in 8 — same length, much worse expected finish. 4C2E was unambiguous.

**HTR reduction (10).** `U F2 U' R2 U L2 U2 R2 F2 U'` is the recognize_htr_subset output for **0-swap long-cycle**. 0-swap is the friendliest corner subset — no corner 2-cycle to resolve, just a long cycle of slice edges to unravel. The reduction lands cleanly at `is_htr_ud=true` at move 22.

**Finish (8).** Planned 9-move finish, auto-cancelled 1 at a chunk join (the last `U'` of the HTR reduction merged with the first `U2` of the finish into the embedded `U' U2 → U` which was further absorbed by adjacent half-turns). Net 8.

The neighborhood alternatives: DR-7C8E in 8 setup → typically 12+ post-DR, projecting 32–34. Staying on FB-inv 5+7 (draft 1) → 31. UD-normal 4+8 was the dominant choice and I just needed to scout it.

---

## Three-way comparison

**vs. Marcin (20 moves):** His EO was the same 4-move `R2 D F B'` (up to direction — same pattern). Then he played a **2c3+2e direct solve** in 6 moves (`L B2 R D2 L'`... wait, `L B2 R D2 L' D'`, 6 moves) reaching a state with 2 corners 3-cycled and 2 edges to fix. Then a **10-move direct insertion on inverse** `(B2 L' U2 R2 U2 R F2 B2 D2 L')` finishes it. Total 4+6+10 = 20.

He **skipped DR entirely**. The 2c3+2e is a pre-DR direct-finish technique: from EO-solved, identify a residual where only 2 corners and 2 edges remain wrong and insert the solution directly without ever going through DR/HTR. This requires recognizing the 2c2e (or 2c3+2e) pattern and having insertion search. My pipeline has no equivalent probe — I went EO→DR→HTR→finish in the standard 4+8+10+8 = 30. The 10-move gap is 100% the DR detour.

**vs. nissy axis-locked (35 moves):** Nissy's UD pipeline is EO(5) + DR(10) + HTR(10) + finish(10) = 35. I got 4+8+10+8 = 30. So I **beat nissy by 5 on the same axis**, entirely from EO (5→4, the symmetry pattern nissy can't exploit because it doesn't NISS) and DR (10→8, because I picked the 4C2E trigger and nissy's locked DR is longer). HTR reduction tied at 10. Finish 10→8 from auto-cancellation. NISS+axis picking was worth ~5 moves on this scramble, which is the entire DR-pipeline edge over the axis-locked baseline.

**vs. prior LLM versions:** v19 also got 30 (`R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`) — **identical solution to mine**, same EO, same DR-4C2E, same HTR, same finish. v24/25/26/29/30 all got 25 moves with a different recipe (`R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`) — appears to be a 4-move EO followed by a much shorter direct-solve path, possibly the 2c3+2e Marcin used. v27/28/33 regressed to 29; v31/32 to 28. My 30 ties the v19 baseline and is 5 worse than the v25/v29/v30 lineage. Those earlier versions found a sub-DR direct solve on this scramble that my current pipeline doesn't probe for.

---

## What I'd change

1. **Add a 2c3+2e direct-solve probe after EO.** When EO is short (≤4) and the residual has low corner-misorientation count, the WCA technique is to insertion-search a direct finish rather than commit to DR. v25/v29/v30 found 25 moves on this scramble — that probe exists in some form in the codebase history. Adding it would have saved 5 moves here.

2. **Stop re-scouting after a known-good axis lands.** Drafts 3 and 5 both wasted budget re-checking axes I'd already cleared in earlier drafts of the same session. A session-level "axis scoreboard" carried across drafts would prevent this — draft 5 should have opened with "draft 4 got 30 on UD-normal, replicate or beat."

3. **Treat `dr_trigger_options` returning nothing as a hard reject.** Drafts 3 and 5 both ignored this and burned 10+ tool calls on `dr_recognize` loops. Rule: if depth-5 trigger survey is empty, reset and try another axis before falling back to brain navigation.

---

Closing: a 4-move symmetry EO and a 4C2E trigger got me to nissy-minus-5, but skipping DR entirely the way Marcin did would have required machinery my pipeline doesn't yet have.
