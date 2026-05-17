# Solve — fm_PSSSideDayGdansk2026_s2__attempt5_20260517_150415

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `L2 B' F2 R2 U F L2 U' F R2 F U2 R2 F U2 L2 B2 F2 U2 B2 L2 F2 B' U2 R U2`

---

*Thinking (1):*

> Looking at the prior attempts, all of them reached 30-31 moves. The instructions are clear: commit hard to one line and finish it completely. Let me start by inspecting the state to understand what we're working with.
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I need to:
> 1. Start with inspect_state to see bad edges per axis
> 2. Scout EO on the most promising axes (both normal and inverse)
> 3. Pick one (side, axis) combination and COMMIT
> 4. Drive through DR → HTR → finish without backtracking
> 5. Use compose_niss_solution before final submission
> 
> Let me begin.

I'll solve this scramble systematically, committing hard to the best line I find early. Starting with inspection.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**EO scouting**: FB and RL both have 4 bad edges (tied for best), UD has 6. Per prior attempts reaching 30 moves, I need to scout both FB and RL on normal AND inverse to find the joint-shortest EO+DR path.

**FB-axis bad edges**: DR, DL, FR, BL — split 2 on L face, 2 on R face. This suggests a 2-move FB-EO (L + R flips). 
**RL-axis bad edges**: UL, DR, DF, FR — split 1 on U, 3 on D-side. Might need setup.

**NISS signal**: `top_pairs_on_inverse: 3` on UD axis is STRONG (≥2 is the switch threshold). Even though UD has 6 bad edges, the inverse side might have a better combined path. Let me scout:

1. FB-normal EO
2. RL-normal EO  
3. Then flip to inverse and scout the most promising axis there

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL give 4-move EOs on normal. Now let me flip to inverse and scout those same axes there (bad-edge counts are identical per the NISS invariant, but the SOLUTION differs):

NISS flip — switching to the inverse scramble.

Now on inverse. Scouting FB and RL EO on this side:

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

**EXCELLENT**: FB-inverse gives a **2-move EO** (`U2 R'`), crushing the 4-move normal options. RL-inverse is 5 moves (worse). 

Now I need to probe DR after the FB-inverse 2-move EO. Per the pipeline: test DR cost before committing:

I probe what DR would look like if I applied this EO (without committing).

**FB-inverse EO=2, DR total=9, so 2+9=11 to DR**. That's competitive. Let me also check what happens with the 4-move normal options for comparison:

NISS flip — switching back to the normal scramble.

Back on normal. Let me probe FB-normal 4-move EO's DR:

I probe what DR would look like if I applied this EO (without committing).

**FB-normal: EO=4, DR=8, total 4+8=12 to DR**. Worse than inverse (2+9=11). Let me also check RL-normal for completeness:

I probe what DR would look like if I applied this EO (without committing).

**RL-normal: EO=4, DR=8, total 4+8=12 to DR**. Same as FB-normal.

**DECISION**: FB-inverse (2+9=11) is the shortest path to DR by 1 move. The prior attempts reaching 30 moves likely used different paths. **COMMITTING to FB-inverse EO + DR.**

Flipping back to inverse and applying the 2-move EO:

NISS flip — switching to the inverse scramble.

I turn `U2 R'`.

**EO complete on FB-inverse with U2 R' (2 moves)**. Now finding DR. Using dr_trigger_options for FB axis:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on FB.**

**0 trigger options found within 5-move setup** on FB. This is unusual. Let me fall back to dr_recognize to see what the DR pattern actually is:

I check whether the DR is recognizable from this state via the library.

DR is 9 moves total (matching the probe). I see the first 4 setup moves: `U2 B U' B2`. Applying them:

I turn `U2 B U' B2`.

I check whether the DR is recognizable from this state via the library.

Now 5 more moves needed. Applying the next 4:

I turn `R2 F U R2`.

I check whether the DR is recognizable from this state via the library.

**DR trigger found**: Just `U'` (1 move). Total to DR: 2 (EO) + 8 (setup) + 1 (trigger) = **11 moves**. Applying the trigger:

I turn `U'`.

Quick check: DR-locked on FB, not yet HTR.

**DR achieved on FB-axis in 11 moves** (on inverse). Now proceeding to HTR. Classifying the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 12 moves (first exposure — learning).

**HTR subset**: 2-swap long-cycle. **HTR reduction = 10 moves**, **finish = 12 moves**, total **22 moves** from DR to solved.

Total projected: 11 (to DR) + 22 (HTR+finish) = **33 moves**. This matches the first prior attempt. Let me execute the HTR phases with inter-phase checks for early residuals:

For the corner reduction, I see `U2 F' L2 F` (chunk of a 10-move phase) — apply and re-check.

HTR reduction is 10 moves, seeing first 4. Applying and checking state:

I turn `U2 F' L2 F`.

Quick check: DR-locked on FB, not yet HTR.

Not solved yet. Continuing HTR reduction:

For the corner reduction, I see `D2 F R2 F'` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F R2 F'`.

Quick check: DR-locked on FB, not yet HTR.

For the corner reduction: `U2 B`.

I turn `U2 B`.

Quick check: in HTR.

**HTR achieved** (is_htr_ud=true). Now the finish phase (12 moves):

For the half-turn finish, I see `R2 F2 D2 R2` (chunk of a 12-move phase) — apply and re-check.

I turn `R2 F2 D2 R2`.

Quick check: in HTR.

For the half-turn finish, I see `D2 F2 R2 B2` (chunk of a 8-move phase) — apply and re-check.

I turn `D2 F2 R2 B2`.

Quick check: in HTR.

For the half-turn finish: `L2 U2 R2 U2`.

I turn `L2 U2 R2 U2`.

A quick glance — the cube is solved.

**SOLVED in 32 moves on inverse!** Now composing the final solution with compose_niss_solution (it will invert and cancel):

I assemble the canonical inverse-frame solution: **32 moves**, verified.

**32-move solution verified!** This beats attempt 1 (33 moves) but is tied with attempts 2-4 (30-31). Let me check if replace_and_shorten can improve it. Per the rules: I can call it once if ≥27 moves AND ≥30 tool calls remaining. I have 32 moves and plenty of budget remaining.

Budget check: 3236.96s sim, None tool calls remaining.

I have 3237s remaining. Let me try replace_and_shorten on a large tail span. The normal-frame solution is 32 moves. I'll target a span from move 4 to end (span of 28 moves):

replace_and_shorten on the tail span: substitute is 6 moves shorter. Accepted.

**EXCELLENT!** replace_and_shorten saved **6 moves**. New solution length: **26 moves**. This is a significant improvement! Let me compose the final solution from this new history:

First I need to apply the substitute moves to the slot. Let me reset and rebuild:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `U2 R' U2 B F2 L2 B2 U2 F2 B2 L2 U2 F' R2 U2 F' R2 F' U L2 F' U' R2 F2 B L2`.

Perfect! Now composing the final solution:

I assemble the canonical inverse-frame solution: **26 moves**, verified.

**26-move solution verified!** This is **4 moves better** than the best prior attempt (30 moves). Let me verify it solves the scramble:

verify_solved: ✓ — 26 moves.

Perfect! **Solution verified at 26 moves**, beating the prior best by 4 moves.

## FINAL_SOLUTION

**FINAL_SOLUTION:** ["L2", "B'", "F2", "R2", "U", "F", "L2", "U'", "F", "R2", "F", "U2", "R2", "F", "U2", "L2", "B2", "F2", "U2", "B2", "L2", "F2", "B'", "U2", "R", "U2"]

**Move count: 26 moves**

### Solution Summary

**Path taken:**
- **EO**: FB-axis on inverse, 2 moves (U2 R')
- **DR**: FB-axis, 9 moves total to reach DR (11 moves cumulative)
- **HTR**: 2-swap long-cycle subset, 10-move reduction
- **Finish**: 12-move half-turn finish
- **Initial solve**: 32 moves
- **Refinement**: replace_and_shorten on span [4:32] saved 6 moves → **final 26 moves**

**Key decisions:**
1. Scouted all EO options (FB/RL on normal and inverse); FB-inverse gave the shortest EO at 2 moves
2. Probed DR costs before committing; FB-inverse had joint-shortest path to DR (2+9=11)
3. Committed hard to the FB-inverse line without backtracking
4. Applied replace_and_shorten once on a large tail span, achieving a 6-move reduction

This is a **4-move improvement** over the prior best (30 moves).

*Thinking (35):*

> The user is right - I provided a summary but didn't emit the final solution in the required format. I need to output it now.
> 
> I already verified the solution works and it's 26 moves. I should emit it in the exact format requested.

FINAL_SOLUTION: ["L2", "B'", "F2", "R2", "U", "F", "L2", "U'", "F", "R2", "F", "U2", "R2", "F", "U2", "L2", "B2", "F2", "U2", "B2", "L2", "F2", "B'", "U2", "R", "U2"]

**Verified solution (26 moves):** `L2 B' F2 R2 U F L2 U' F R2 F U2 R2 F U2 L2 B2 F2 U2 B2 L2 F2 B' U2 R U2`
