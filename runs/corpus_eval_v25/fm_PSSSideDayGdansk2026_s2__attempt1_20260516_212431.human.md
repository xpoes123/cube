# Solve — fm_PSSSideDayGdansk2026_s2__attempt1_20260516_212431

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`

---

*Thinking (1):*

> The user wants me to solve the scramble within the one-hour simulated budget. I should start with inspect_state as instructed, then follow the FMC pipeline:
> 
> 1. Inspect the state
> 2. Use niss_scout to check both normal and inverse frames across all 3 axes
> 3. Choose the best EO+DR combination
> 4. Execute EO
> 5. Find DR
> 6. HTR classify and finish
> 7. Cancel and verify
> 8. Submit using compose_niss_solution
> 
> Let me start by inspecting the state to see what we're working with.

I'll solve this scramble step by step, following the elite FMC workflow. Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Now I see the cube state. I have:
- **UD axis**: 6 bad edges, DR-7C3E (7 misoriented corners, 3 misplaced slice edges), **3 pairs on inverse** — strong NISS signal
- **FB axis**: 4 bad edges, DR-7C2E  
- **RL axis**: 4 bad edges, DR-6C2E

The 3 pairs on inverse for the UD axis is a strong signal to check the inverse frame. Let me run niss_scout to get the full 6-row comparison table across both normal and inverse frames.

I scout EO+DR on both normal and inverse, all three axes — 3 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L F') DR (8mv)
  • normal-RL: EO 4mv → DR-7C8E (F' L B) DR (8mv)
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The niss_scout reveals a **CLEAR WINNER**: 

**Row 1 (RL axis, inverse frame)**: 
- EO 5 moves: `D U' B' D' U'`
- DR-3C2E trigger family (F L F'): 5 setup + 3 trigger = 8 moves to DR
- **finish_length_actual: 0 moves** — this already SOLVES after DR!
- **Total: 13 moves to solved**

This is an incredible result — the inverse-RL branch gets EO in 5, DR in 8, and the state is already solved after DR (0 finish moves). This is a 13-move solution!

Let me flip to inverse and execute this path.

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. Let me apply the 5-move EO sequence for RL axis: `D U' B' D' U'`

I turn `D U' B' D' U'`.

EO applied. Now I need to find the DR-3C2E trigger on the RL axis. According to niss_scout, the trigger family is "DR-3C2E (F L F')" with 5 setup moves, then 3 trigger moves. Let me use dr_trigger_options to get the exact moves.

I survey the named DR triggers on RL:
  • DR-4C4E (F): 6-mv setup + 1-mv trigger (7 total)
  • DR-4C4E (F'): 6-mv setup + 1-mv trigger (7 total)
  • DR-3C2E (F L F'): 5-mv setup + 3-mv trigger (8 total)

Perfect! Option 3 matches the niss_scout prediction: "DR-3C2E (F L F')" with setup `U2 R' U2 F R` (5 moves) and trigger `F L F'` (3 moves) = 8 moves total to DR.

The niss_scout said this results in 0 finish moves (already solved). Let me apply the setup moves first:

I turn `U2 R' U2 F R`.

Setup applied. Now let me apply the DR trigger: `F L F'`

I turn `F L F'`.

Excellent! I now have 13 moves on the inverse frame. According to niss_scout, this should already be solved. Let me verify with quick_check:

Quick check: DR-locked on RL, not yet HTR.

Interesting! It says DR is achieved on RL axis, but the cube is not solved yet. The niss_scout cache might have been showing an optimistic prediction. Let me inspect the current state to see what's left:

I look over the cube.
Bad-edge counts: UD=0, FB=4, RL=0.
I'm currently working on the inverse scramble.
Last applied: `U2 F R F L F'`.

Good progress! I'm at DR on RL axis with:
- All corners solved (8 corners)
- 4 edges solved, 8 edges unsolved
- 4 quarter-turn corners remaining in HTR

I need to continue through HTR. Let me classify the HTR subset:

I recognize the HTR subset: **0-swap axial**. Reduction is 5 moves, finish is 10 moves (first exposure — learning).

This is a **0-swap axial subset** (all corners in place, just oriented wrongly). It needs:
- HTR reduction: 5 moves
- Finish: 10 moves
- Total: 15 more moves

Current total: 13 + 15 = 28 moves. Let me proceed with the HTR reduction phase:

For the corner reduction, I see `F2 R U2 D2` (chunk of a 5-move phase) — apply and re-check.

The HTR reduction is 5 moves but I can only see 4 at a time. Let me apply these 4 moves:

I turn `F2 R U2 D2`.

Now let me check if I've reached HTR or if there's one more move needed:

Quick check: DR-locked on RL, not yet HTR.

Not at HTR yet. Let me get the remaining HTR reduction move:

For the corner reduction: `L`.

I turn `L`.

Now let me apply the finish phase (10 moves):

For the half-turn finish, I see `F2 L2 B2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `F2 L2 B2 R2`.

Let me check if solved yet:

Quick check: in HTR.

Good! I'm now at HTR. Let me continue with the finish phase:

For the half-turn finish, I see `D2 F2 D2 F2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F2 D2 F2`.

Quick check: in HTR.

Still at HTR but not solved. Let me continue:

For the half-turn finish: `L2 U2`.

I turn `L2 U2`.

A quick glance — the cube is solved.

Perfect! The cube is solved in 28 moves on the inverse frame. Now I need to use compose_niss_solution to get the canonical normal-frame solution with proper cancellations:

I assemble the canonical inverse-frame solution: **26 moves**, verified.

Excellent! After cancellation, the solution is **26 moves**. The compose_niss_solution has already verified it solves the scramble. 

Since this is 26 moves (less than 27), I don't meet the gate for replace_and_shorten. Let me verify this solution one final time:

verify_solved: ✓ — 26 moves.

Perfect! The solution is verified. Let me check the budget status:

Budget check: 3498.0s sim, None tool calls remaining.

Excellent! I've solved the scramble in **26 moves** using only 102 seconds of simulated time (out of 3600 available).

## Solution Summary:

**Strategy**: Following the niss_scout recommendation, I worked on the **inverse frame, RL axis**:
- **EO (5 moves)**: `D U' B' D' U'` — RL-axis edge orientation
- **DR (8 moves total)**: Setup `U2 R' U2 F R` + Trigger `F L F'` (DR-3C2E family)
- **HTR reduction (5 moves)**: `F2 R U2 D2 L` — reduced to HTR corner subgroup (0-swap axial)
- **HTR finish (10 moves)**: `F2 L2 B2 R2 D2 F2 D2 F2 L2 U2` — half-turn finish to solved

After inversion and cancellation, the final solution is **26 moves**.

**FINAL_SOLUTION**: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

*Thinking (29):*

> The user is right - I verified the solution but didn't emit the FINAL_SOLUTION. I have a verified 26-move solution. Let me output it now.

FINAL_SOLUTION: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

**Verified solution (26 moves):** `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`
