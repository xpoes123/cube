# Solve — fm_PSSSideDayGdansk2026_s2__attempt2_20260520_020959

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 34 moves
**Solution**: `R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`

---

*Thinking (1):*

> The user wants me to solve this scramble. I've already seen that a prior attempt got 34 moves. The instruction is clear: COMMIT HARD to one line and drive it to completion. Don't over-ideate, don't abandon halfway through.
> 
> Let me start by inspecting the state to understand what I'm working with.
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I should:
> 1. inspect_state to see bad edges per axis
> 2. Scout EO on the most promising axes (both normal and inverse)
> 3. Pick one (side, axis) and commit
> 4. Drive through DR → HTR → finish without second-guessing
> 
> Let's begin.

I'll solve this scramble with a committed single-line approach. Starting with inspection.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**Observation**: Bad edges per axis: UD=6, FB=4, RL=4. Both FB and RL have 4 bad edges — these are my best EO candidates. The prior 34-move solution likely used one of these axes. Let me scout EO on both normal side first, then check inverse for comparison.

**Plan**: Scout FB and RL on normal, then flip to inverse and check again. Pick the (side, axis) with shortest joint EO+DR cost.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL give 4-move EOs on normal. Now let me check inverse for both axes.

NISS flip — switching to the inverse scramble.

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

**Excellent!** Inverse-FB gives a **2-move EO** (U2 R'). This is significantly shorter than the 4-move options. Now I need to test DR cost from this EO. Let me commit the inverse-FB EO and probe DR.

I turn `U2 R'`.

Now I'll scout DR options on FB axis from this EO-solved state.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**No DR triggers found within 5 moves on FB axis.** This is a signal that this axis/side combination might not be good. Let me fall back to dr_recognize to see what the brain suggests.

I check whether the DR is recognizable from this state via the library.

The brain suggests R2 as the most likely next move. But this is already getting expensive. Let me reset and try a different approach. The prior 34-move solution exists, so there must be a viable path. Let me go back to normal and try a different axis.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me try the normal-side FB 4-move EO and check its DR options.

I turn `B2 L2 U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Still no DR triggers on FB. Let me try RL axis instead. Resetting.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B F2 U'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

**Found a DR trigger on RL!** DR-7C8E in 8 moves total (5 setup + 3 trigger). This is not great (DR-7C8E has poor substates typically), but it's within range. Let me commit this and see the residual, then push through to finish.

**Committing to RL-axis normal-side**. EO: `R2 B F2 U'` (4 moves) + DR setup+trigger: 8 moves = 12 moves to DR. This meets the sub-15 DR target.

I turn `R B' D2 R' B' F' L B`.

Now I'm at DR on RL axis. Let me classify the HTR subset and finish.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 12 moves (first exposure — learning).

The subset is "2-swap long-cycle" with 11 moves for HTR reduction + 12 for finish = 23 moves post-DR. Total would be 12 + 23 = **35 moves** — slightly worse than the prior 34. But let me proceed and check for opportunistic 3-cycle residuals along the way.

For the corner reduction, I see `B2 R U2 R` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 R U2 R`.

Good — 1 move cancelled already (B + B' → B'). Let me check if this is solved or a clean residual before continuing.

Quick check: DR-locked on RL, not yet HTR.

Not solved, still in DR on RL. Continue HTR reduction.

For the corner reduction, I see `F2 R2 B2 D2` (chunk of a 7-move phase) — apply and re-check.

I turn `F2 R2 B2 D2`.

Quick check: DR-locked on RL, not yet HTR.

For the corner reduction: `R F2 R`.

I turn `R F2 R`.

Quick check: in HTR.

Great! I'm now at HTR (is_htr_ud=true). Now the finish phase.

For the half-turn finish, I see `U2 B2 R2 D2` (chunk of a 12-move phase) — apply and re-check.

I turn `U2 B2 R2 D2`.

Quick check: in HTR.

For the half-turn finish, I see `F2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 U2`.

Quick check: in HTR.

For the half-turn finish: `L2 D2 R2 U2`.

I turn `L2 D2 R2 U2`.

A quick glance — the cube is solved.

**Solved at 34 moves!** This matches the prior attempt. Now let me cancel and verify before considering replace_and_shorten.

I assemble the canonical normal-frame solution: **34 moves**, verified.

Perfect — 34 moves and verified. Now I have enough tool calls (44 remaining, gate is ≥30) and the solution is ≥27 moves (gate is ≥27), so I should try replace_and_shorten once per the mandatory rule.

Let me try replace_and_shorten on a large tail span to see if I can improve.

r&s: could not solve micro-scramble for span [4:34]: no DR found

Replace_and_shorten failed to find a better path on that span. The solution is already quite clean at 34 moves, matching the prior best. Let me submit this as the final solution.

verify_solved: ✓ — 34 moves.

Perfect! The solution is verified and clean at **34 moves**, matching the previous best attempt.

## FINAL_SOLUTION

**R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2**

**Solution breakdown:**
- **EO (RL-axis)**: R2 B F2 U' — 4 moves, orienting the 4 bad edges on RL axis
- **DR setup + trigger**: R B' D2 R' B' F' L B — 8 moves to reach DR-7C8E on RL axis (12 total to DR)
- **HTR + Finish**: 22 moves through the "2-swap long-cycle" subset
- **Total**: 34 moves (with 1 move saved via automatic cancellation)

This solution matches the prior best of 34 moves. The RL-axis proved viable with a clean 12-move path to DR and systematic HTR finish.

*Thinking (38):*

> The user is right - I narrated that I would submit the final solution but didn't actually emit it in the required format. I need to output the FINAL_SOLUTION in the exact format requested.
> 
> The verified solution is:
> ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "R", "U2", "R", "F2", "R2", "B2", "D2", "R", "F2", "R", "U2", "B2", "R2", "D2", "F2", "U2", "F2", "U2", "L2", "D2", "R2", "U2"]
> 
> 34 moves total.

FINAL_SOLUTION: ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "R", "U2", "R", "F2", "R2", "B2", "D2", "R", "F2", "R", "U2", "B2", "R2", "D2", "F2", "U2", "F2", "U2", "L2", "D2", "R2", "U2"]

**Verified solution (34 moves):** `R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`
