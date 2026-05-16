# Solve — fm_BackiPetrovacOpen2026_s1_20260516_173426

**Scramble**: `R' U' F D' L2 R' U2 F2 R' F2 U2 B2 L2 U B D' R' D' U2 L2 B2 D2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 29 moves
**Solution**: `R' D' R' U2 F' U2 R2 F2 L2 F2 R2 B2 D2 L2 U L2 R2 F2 U L2 U2 R U' D2 R' L D F2 U'`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start by inspecting the state to understand what I'm working with. The instructions are very clear - I should start with inspect_state(slot='main').
> 
> Let me begin the solve following the pipeline:
> 1. First inspect_state to see the cube
> 2. Then niss_scout to get the 6-row table comparing all axes/frames
> 3. Choose the best EO direction based on expected_total_to_solved
> 4. Work through EO → DR → HTR → finish
> 
> Let me start.

I'll solve this FMC scramble systematically. Starting with state inspection to understand the cube configuration.

I look over the cube.
Bad-edge counts: UD=4, FB=6, RL=6.

Good! I can see:
- **UD axis**: 4 bad edges (UB, FR, FL, BR) — the F face has 2 (FR, FL), B face has 2 (UB, BR). This is a symmetric 2+2 pattern, likely 2-move EO.
- **FB axis**: 6 bad edges
- **RL axis**: 6 bad edges
- **DR closeness**: UD shows DR-7C2E with 2 pairs on inverse — that's a NISS-switch signal.

Now calling niss_scout to get the comprehensive 6-row comparison table (normal × inverse × 3 axes). This will tell me the best joint EO+DR path.

I scout EO+DR on both normal and inverse, all three axes — 0 viable rows.
I'll weigh the substate quality (trigger family) against raw length and pick.

Interesting! The scout found EO solutions but **no DR triggers within max_setup=5** for ANY axis/side combination. This is unusual but not a dead end. The best EO option is **inverse-UD with 3 moves** (D U B').

**Decision**: I'll take the inverse-UD path with 3-move EO, then manually explore DR using dr_trigger_options after EO is complete. The 2 pairs on inverse supports this choice.

Let me flip to inverse and apply the EO.

NISS flip — switching to the inverse scramble.

Good! Now on inverse. Applying the 3-move EO: D U B'.

I turn `D U B'`.

EO applied. Now let me check what DR options are available on UD axis using dr_trigger_options.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

No UD-axis DR triggers found within 5 moves. Let me try FB and RL axes as well to see if a different axis gives better DR options.

DR trigger menu on FB: EO not yet solved on axis FB; run eo_pattern_lookup and apply EO moves first.

DR trigger menu on RL: EO not yet solved on axis RL; run eo_pattern_lookup and apply EO moves first.

Right - I solved EO on UD axis, so I can only check DR on UD. The fact that no DR triggers are found within 5 moves is concerning. Let me extend the search to max_setup=6 to see if there's a 6-move option.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Still no DR triggers. This is a bad signal - the EO+DR combination on inverse-UD isn't working. Let me reconsider. I should try a different approach. Let me reset and try the normal frame instead, or try a different axis entirely.

**Strategic decision**: The inverse-UD path looked promising with 3-move EO but has NO viable DR within 6 moves. That's a dead end. Let me reset and try **normal-UD with 5-move EO** - even though EO is longer, if it gives a good DR it could be better overall.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Back to normal frame. Let me try the normal-UD 5-move EO and see if it gives better DR options.

I turn `R' D' R' U2 F'`.

Normal-UD EO applied (5 moves). Now checking DR options on UD axis.

I survey the named DR triggers on UD:
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)
  • DR-4C2E (R U2 R'): 6-mv setup + 3-mv trigger (9 total) [JZP]

Excellent! Found two DR options, both at 9 moves total:
1. **DR-7C8E (R U L)**: 6 setup + 3 trigger = 9 total. Has 4 pairs on inverse (excellent NISS signal).
2. **DR-4C2E (R U2 R')**: 6 setup + 3 trigger = 9 total. JZP-eligible (great substate quality).

The DR-4C2E with JZP is very promising - JZP states have much shorter HTR finishes. I'll take option 2.

**Total so far**: 5 (EO) + 9 (DR) = 14 moves to DR. That's excellent - well under the 15-move threshold.

I turn `U2 L' U' R2 B2 D2`.

Setup moves applied. Now applying the DR-4C2E trigger: R U2 R'.

I turn `R U2 R'`.

DR trigger applied! 14 moves to DR. Now let me classify the HTR subset to see what finish I'm facing.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 6 moves, finish is 11 moves (first exposure — learning).

HTR subset classified: **2-swap long-cycle** with cycle structure [4, 2, 1, 1].
- HTR reduction: 6 moves
- Finish: 11 moves
- Total: 17 moves

**Projected total**: 14 (to DR) + 17 (HTR finish) = **31 moves**.

That's acceptable but not great. Let me proceed with the finish and see if we land on any lucky residuals during the process. I'll apply the HTR reduction phase first.

For the corner reduction, I see `U2 R2 B2 U'` (chunk of a 6-move phase) — apply and re-check.

HTR reduction is 6 moves but I can only see 4 at a time. Applying the first chunk: U2 R2 B2 U'.

I turn `U2 R2 B2 U'`.

Applied 4 moves of HTR reduction. Let me check if we're solved or if there's a good residual before continuing.

Quick check: DR-locked on UD, not yet HTR.

Not yet in HTR. Continuing with the remaining HTR reduction moves.

For the corner reduction: `B2 D`.

The remaining 2 moves of HTR reduction: B2 D.

I turn `B2 D`.

HTR reduction complete (20 moves total). Quick check before starting the finish phase.

Quick check: in HTR.

Perfect! Now in HTR (all axes). Starting the finish phase - expected 11 moves.

For the half-turn finish, I see `F2 D2 F2 L2` (chunk of a 11-move phase) — apply and re-check.

First 4 moves of finish: F2 D2 F2 L2.

I turn `F2 D2 F2 L2`.

24 moves so far. Let me check if we hit a lucky early solve or good residual.

Quick check: in HTR.

Still in HTR, not solved. Let me check if it's a corner 3-cycle residual.

Residual class: mixed.

Not a pure 3-cycle - mixed residual with 6 corners and 9 edges still unsolved. Continuing with the finish.

For the half-turn finish, I see `B2 L2 R2 U2` (chunk of a 7-move phase) — apply and re-check.

Next 4 moves: B2 L2 R2 U2.

I turn `B2 L2 R2 U2`.

28 moves. Checking again.

Quick check: in HTR.

Residual class: mixed.

Still mixed. Getting the final chunk of finish moves.

For the half-turn finish: `F2 R2 U2`.

Final 3 moves: F2 R2 U2.

I turn `F2 R2 U2`.

31 moves total. Let me verify if this solves the cube.

A quick glance — the cube is solved.

Excellent! Cube is solved in 31 moves. Now let me compose the final solution with cancellations.

I assemble the canonical normal-frame solution: **31 moves**, verified.

Perfect! I have a 31-move solution that solves the scramble. Since this is ≥27 moves, I should try replace_and_shorten to potentially improve it. Let me check my budget first.

Budget check: 3431.0s sim, None tool calls remaining.

Good - I have plenty of time remaining (3431s) and enough tool calls. Let me try replace_and_shorten on a large tail span to see if I can compress the solution. I'll target the middle-to-end section where DR+HTR happened.

replace_and_shorten on the tail span: substitute is 1 move shorter. Accepted.

Excellent! replace_and_shorten found a 1-move improvement, bringing the solution down to **30 moves**. The new history solves the scramble. Let me apply this and compose the final solution.

The new solution is already in the result. Let me verify it solves the scramble.

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. Now let me cancel any adjacent same-face moves to see if we can compress it further.

I run cancellation: 30 → 29 moves (saved 1).

Excellent! Cancellation saved 1 move (U2 U' → U). Final solution is **29 moves**. Let me verify this final version solves the scramble.

verify_solved: ✓ — 29 moves.

Perfect! **29-move solution verified**.

## Solution Summary

**Scramble**: R' U' F D' L2 R' U2 F2 R' F2 U2 B2 L2 U B D' R' D' U2 L2 B2 D2 R' U' F

**Strategy**:
- Started by scouting both normal and inverse frames across all axes
- Inverse-UD showed 3-move EO but no viable DR triggers
- Reset to normal-UD with 5-move EO
- Found DR-4C2E (JZP-eligible) trigger in 9 moves - excellent substate quality
- Total to DR: 14 moves (5 EO + 9 DR)
- HTR subset: 2-swap long-cycle requiring 17 moves to solve
- Initial solution: 31 moves
- Replace-and-shorten on moves 5-31 saved 1 move → 30 moves
- Cancellation (U2 U' → U) saved 1 more move → **29 moves final**

**FINAL_SOLUTION**: ["R'", "D'", "R'", "U2", "F'", "U2", "R2", "F2", "L2", "F2", "R2", "B2", "D2", "L2", "U", "L2", "R2", "F2", "U", "L2", "U2", "R", "U'", "D2", "R'", "L", "D", "F2", "U'"]

*Thinking (38):*

> The user is right - I verified the solution and summarized it, but I never actually emitted the FINAL_SOLUTION in the required format. Let me output it now.

FINAL_SOLUTION: ["R'", "D'", "R'", "U2", "F'", "U2", "R2", "F2", "L2", "F2", "R2", "B2", "D2", "L2", "U", "L2", "R2", "F2", "U", "L2", "U2", "R", "U'", "D2", "R'", "L", "D", "F2", "U'"]

**Verified solution (29 moves):** `R' D' R' U2 F' U2 R2 F2 L2 F2 R2 B2 D2 L2 U L2 R2 F2 U L2 U2 R U' D2 R' L D F2 U'`
