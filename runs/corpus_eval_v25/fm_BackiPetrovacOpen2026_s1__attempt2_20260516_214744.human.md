# Solve — fm_BackiPetrovacOpen2026_s1__attempt2_20260516_214744

**Scramble**: `R' U' F D' L2 R' U2 F2 R' F2 U2 B2 L2 U B D' R' D' U2 L2 B2 D2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `U' R2 F2 U' L2 U2 R2 B2 D B2 D2 F2 R2 U2 L2 D2 B2 R2 U2 R D2 L U2 F2 U R2 D' B U' D'`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble. Let me start by inspecting the state to see the cube configuration, then follow the v17 pipeline with NISS-scout before committing to any EO axis.
> 
> The scramble is:
> R' U' F D' L2 R' U2 F2 R' F2 U2 B2 L2 U B D' R' D' U2 L2 B2 D2 R' U' F
> 
> Let me start with inspect_state to see what we're working with.

I'll solve this FMC scramble systematically. Let me begin by inspecting the cube state to understand what we're working with.

I look over the cube.
Bad-edge counts: UD=4, FB=6, RL=6.

Good! Initial inspection reveals:
- **UD axis**: 4 bad edges (UB, FR, FL, BR) — this is the cleanest EO at first glance
- **FB/RL axes**: 6 bad edges each — worse starting points
- **DR closeness**: UD shows DR-7C2E (poor substate), but has **2 pairs on inverse** (Wen's signal)
- **JZP**: none eligible on normal side

The 2 pairs on inverse is a strong NISS signal. Before committing to any axis, I must run niss_scout to compare all 6 branches (normal×inverse×3 axes) systematically.

I scout EO+DR on both normal and inverse, all three axes — 0 viable rows.
I'll weigh the substate quality (trigger family) against raw length and pick.

Interesting! The scout shows:
- **Best EO length**: inverse-UD with only **3 moves** (D U B')
- **Problem**: NO DR triggers found within max_setup=5 on ANY axis/side combination

This is unusual — the scout couldn't find viable DR paths. This means the DR will require either longer setup (6+ moves) or the EO choices here don't lead to good DR states. Let me pick the shortest EO (inverse-UD, 3 moves) and manually explore DR options afterward.

**Decision**: Start on **inverse-UD** with the 3-move EO: D U B'

Let me flip to inverse and apply the EO:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `D U B'` fixes it.

Perfect! The 3-move EO is confirmed. Applying it now:

I turn `D U B'`.

Good! EO complete on inverse-UD in 3 moves. Now I need to explore DR options. Since niss_scout found no triggers within max_setup=5, I'll use dr_trigger_options with a higher max_setup to see what's available:

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Hmm, still no DR triggers found even at max_setup=6. This is a very difficult state for the UD-axis DR. Let me check if maybe I should reconsider and try a different axis. Let me look at FB axis DR options from this EO state:

DR trigger menu on FB: EO not yet solved on axis FB; run eo_pattern_lookup and apply EO moves first.

Right — I can only check DR on the axis where EO is solved (UD). Let me try using dr_recognize as a fallback to see what the actual DR state looks like:

I check whether the DR is recognizable from this state via the library.

Good! The DR is 8 moves total, which is acceptable (elite target is ≤11). I see 4 moves of setup progress. Let me apply them:

I turn `D R2 U' F2`.

Now let me re-query DR to see the trigger:

I check whether the DR is recognizable from this state via the library.

Excellent! I can see the full DR now: 3-move setup (U2 L' D2) + 1-move trigger (R'). Total DR from this point is 4 moves, so:
- **EO**: 3 moves (D U B')
- **DR**: 8 moves total (4 setup + 4 more)

Applying the setup and trigger:

I turn `U2 L' D2`.

I turn `R'`.

Perfect! DR complete in 11 moves (3 EO + 8 DR). Now let me classify the HTR state to see what subset I'm working with:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 9 moves, finish is 12 moves (first exposure — learning).

The HTR subset is **0-swap long-cycle** with:
- **HTR reduction**: 9 moves
- **Finish**: 12 moves
- **Total from DR**: 21 moves

This gives a projected total of 11 + 21 = **32 moves**, which is acceptable but not great. Let me proceed with the HTR finish and check for early residuals (per the v17 pipeline, I should use quick_check between chunks).

Applying HTR reduction:

For the corner reduction, I see `U2 L2 U L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 L2 U L2`.

Let me quick_check for early residuals:

Quick check: DR-locked on UD, not yet HTR.

Not yet in HTR. Continuing with the reduction:

For the corner reduction, I see `U2 F2 U' R2` (chunk of a 5-move phase) — apply and re-check.

I turn `U2 F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `U`.

I turn `U`.

Quick check: in HTR.

Good! I'm now in HTR (is_htr_ud = true). The HTR reduction took 9 moves as expected. Now applying the finish phase:

For the half-turn finish, I see `F2 L2 B2 L2` (chunk of a 12-move phase) — apply and re-check.

I turn `F2 L2 B2 L2`.

Quick check: in HTR.

Not yet solved. Continuing finish:

For the half-turn finish, I see `D2 B2 R2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `D2 B2 R2 U2`.

Quick check: in HTR.

Let me check if I'm at a corner 3-cycle residual:

Residual class: mixed.

Not a pure 3-cycle — it's a mixed residual with multiple corner and edge cycles. Let me continue with the finish:

For the half-turn finish: `F2 L2 R2 U2`.

I turn `F2 L2 R2 U2`.

A quick glance — the cube is solved.

Excellent! The cube is solved! I have a complete solution in 32 moves on the inverse. Now I need to use compose_niss_solution to properly assemble the final solution (since I'm on the inverse frame):

I assemble the canonical inverse-frame solution: **32 moves**, verified.

Perfect! I have a verified 32-move solution. Let me check the budget and see if I should try replace_and_shorten:

Budget check: 3479.0s sim, None tool calls remaining.

Good! I have plenty of time (3479s remaining) and tool calls. The solution is 32 moves, which qualifies for replace_and_shorten (≥27 moves). Let me try to optimize a large span. I'll target the middle/end section which has the HTR finish:

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

Excellent! Replace_and_shorten found a 2-move improvement! The span was reduced from 21 moves to 19 moves. Let me update the slot with this new history and compose the final solution:

I turn `D U B' D R2 U' F2 U2 L' D2 R' U2 R2 B2 D2 L2 U2 R2 F2 D2 B2 D' B2 R2 U2 L2 U F2 R2 U`.

Wait, that added the moves instead of replacing. Let me reset and properly set the new history. Actually, looking at the replace_and_shorten output, it already gave me the new_history. Let me reset the slot and apply the correct sequence:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `D U B' D R2 U' F2 U2 L' D2 R' U2 R2 B2 D2 L2 U2 R2 F2 D2 B2 D' B2 R2 U2 L2 U F2 R2 U`.

A quick glance — the cube is solved.

Perfect! The 30-move solution is verified. Now let me compose the final NISS solution:

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Excellent! I have a verified **30-move solution**. Let me verify it one final time:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. Let me check the budget one final time:

Budget check: 3353.0s sim, None tool calls remaining.

Excellent! I used only 247 seconds out of 3600 (less than 7% of budget) and achieved a **30-move solution**.

## Solution Summary

**Approach**: Inverse-UD axis via NISS
- **EO (3 moves)**: D U B' — shortest EO found by niss_scout on inverse
- **DR (8 moves)**: D R2 U' F2 U2 L' D2 R' — reached DR-single-inverse trigger
- **HTR reduction (9 moves)**: U2 R2 B2 D2 L2 U2 R2 F2 D2 B2 (partially shown in chunks, optimized by replace_and_shorten)
- **Finish (10 moves)**: D' B2 R2 U2 L2 U F2 R2 U (optimized from original 12-move finish)

**Total**: 30 moves

The replace_and_shorten tool successfully reduced the HTR finish section from 21 moves to 19 moves, saving 2 moves overall (from 32 to 30).

**FINAL_SOLUTION**: ["U'", "R2", "F2", "U'", "L2", "U2", "R2", "B2", "D", "B2", "D2", "F2", "R2", "U2", "L2", "D2", "B2", "R2", "U2", "R", "D2", "L", "U2", "F2", "U", "R2", "D'", "B", "U'", "D'"]

*Thinking (45):*

> The user is right - I verified the solution and checked the budget but didn't actually emit the FINAL_SOLUTION. I should output it now.
> 
> The verified solution is:
> ["U'", "R2", "F2", "U'", "L2", "U2", "R2", "B2", "D", "B2", "D2", "F2", "R2", "U2", "L2", "D2", "B2", "R2", "U2", "R", "D2", "L", "U2", "F2", "U", "R2", "D'", "B", "U'", "D'"]
> 
> 30 moves total, verified as solving the scramble.

You're absolutely right! Let me submit the final solution:

**FINAL_SOLUTION**: ["U'", "R2", "F2", "U'", "L2", "U2", "R2", "B2", "D", "B2", "D2", "F2", "R2", "U2", "L2", "D2", "B2", "R2", "U2", "R", "D2", "L", "U2", "F2", "U", "R2", "D'", "B", "U'", "D'"]

*Thinking (46):*

> The user is asking me to output the FINAL_SOLUTION in the exact format specified. I need to output it as a JSON array. Let me do that now.

FINAL_SOLUTION: ["U'", "R2", "F2", "U'", "L2", "U2", "R2", "B2", "D", "B2", "D2", "F2", "R2", "U2", "L2", "D2", "B2", "R2", "U2", "R", "D2", "L", "U2", "F2", "U", "R2", "D'", "B", "U'", "D'"]

**Verified solution (30 moves):** `U' R2 F2 U' L2 U2 R2 B2 D B2 D2 F2 R2 U2 L2 D2 B2 R2 U2 R D2 L U2 F2 U R2 D' B U' D'`
