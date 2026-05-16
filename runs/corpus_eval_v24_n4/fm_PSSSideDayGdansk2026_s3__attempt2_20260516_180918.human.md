# Solve — fm_PSSSideDayGdansk2026_s3__attempt2_20260516_180918

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I should start by inspecting the state and then follow the FMC methodology outlined in the instructions.
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Let me start by inspecting the state to see what we're working with.

I'll solve this FMC scramble step by step, starting with the initial inspection.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good! I can see the scramble state:
- **UD axis**: 4 bad edges (UL, DR, DL, DB), DR-7C3E, **3 pairs on inverse** (strong NISS signal)
- **FB axis**: 8 bad edges (all-bad scenario)
- **RL axis**: 6 bad edges

The **3 pairs on inverse** for UD is a very strong signal to check the inverse frame. Let me run the NISS scout to get the full picture across all axes and both frames.

I scout EO+DR on both normal and inverse, all three axes — 1 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The NISS scout reveals:

**Top candidate**: **inverse-RL axis** with EO 5mv + DR-3C2E trigger (total DR 8mv) = **13 moves to DR**. The DR-3C2E trigger family is excellent quality (typically finishes in ~5 moves vs ~9 for 4C4E).

All other options show "no DR triggers within max_setup=5", which means they would require deeper exploration. The inverse-RL option gives us a clean path with a known DR trigger family.

**Decision**: I'll take the **inverse-RL** branch. The DR-3C2E trigger is worth the slightly longer EO (5 moves), and 13 moves to DR is solid.

Let me flip to inverse and apply the EO:

NISS flip — switching to the inverse scramble.

Good! Now I'm on the inverse frame. The scout showed the EO for inverse-RL is ["B'", "L'", "D'", "L2", "U'"]. Let me apply these moves:

I turn `B' L' D' L2 U'`.

EO applied (5 moves on inverse-RL). Now let me check the DR trigger options on the RL axis:

I survey the named DR triggers on RL:
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)

Perfect! I found the DR-3C2E trigger option that the scout predicted:
- **Setup**: U2 F' D2 F R' (5 moves)
- **Trigger**: F L' F' (3 moves)
- **Total to DR**: 8 moves

The setup is 5 moves, so I need to apply it in chunks. Let me apply the first 4 moves:

I turn `U2 F' D2 F`.

Now applying the last setup move and the trigger:

I turn `R' F L' F'`.

Good! I'm now at DR (13 moves: 5 EO + 8 DR). Let me verify DR status and check the HTR classification:

Quick check: DR-locked on RL, not yet HTR.

Excellent! DR is confirmed on RL axis. Now let me classify the HTR subset to see what finish I'm facing:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 8 moves, finish is 10 moves (recall).

HTR subset identified: **0-swap long-cycle** with:
- **HTR reduction**: 8 moves (DR → HTR corners)
- **Finish**: 10 moves (HTR → solved)
- **Total HTR+finish**: 18 moves

This gives us **13 (to DR) + 18 (finish) = 31 moves** projected total. Let me apply the HTR reduction phase:

For the corner reduction, I see `R' D2 R2 B2` (chunk of a 8-move phase) — apply and re-check.

HTR reduction is 8 moves, so it's chunked. Let me apply the first 4 moves:

I turn `R' D2 R2 B2`.

Let me check if we've hit any shortcuts:

Quick check: DR-locked on RL, not yet HTR.

Not solved yet. Let me get the next chunk of HTR reduction:

For the corner reduction: `U2 F2 D2 L`.

Good! The second chunk completes the HTR reduction. Applying it:

I turn `U2 F2 D2 L`.

HTR reduction complete (21 moves total). Let me quick-check before proceeding to the finish:

Quick check: in HTR.

Perfect! I'm now in HTR state (is_htr_ud: true). Now let me apply the finish phase:

For the half-turn finish, I see `B2 U2 B2 L2` (chunk of a 10-move phase) — apply and re-check.

Finish is 10 moves total. Applying the first 4:

I turn `B2 U2 B2 L2`.

Let me check if we're solved or have hit a residual:

Quick check: in HTR.

Still not solved. Let me check for a residual pattern:

Residual class: mixed.

Mixed residual with 6 corners and 10 edges unsolved. Not a clean 3-cycle pattern. Let me continue with the finish. Getting the next chunk:

For the half-turn finish, I see `D2 L2 F2 L2` (chunk of a 6-move phase) — apply and re-check.

Applying the next chunk:

I turn `D2 L2 F2 L2`.

Quick check: in HTR.

Let me get the final chunk of the finish:

For the half-turn finish: `U2 B2`.

Applying the final moves:

I turn `U2 B2`.

Let me check if the cube is solved:

A quick glance — the cube is solved.

Excellent! The cube is solved! I now have a 31-move solution on the inverse frame. Let me use `compose_niss_solution` to get the canonical normal-frame solution with cancellations:

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Great! The solution with cancellations is **30 moves**. The compose function inverted the inverse-frame history and found 1 cancellation (31 → 30). 

Let me verify this solution is correct:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. I have a **30-move solution** that solves the scramble.

Now let me check if I should run `replace_and_shorten` - the guidelines say I should if:
- Total moves ≥ 27 ✓ (30 moves)
- Tool calls remaining ≥ 30 ✓ (I've used about 20 calls)
- Haven't called it yet ✓

Let me check my budget status:

Budget check: 3512.0s sim, None tool calls remaining.

I have plenty of budget remaining (3512s simulated, 1385s wall time). I should try `replace_and_shorten` to potentially reduce the solution length. Let me try shortening a large tail span. I'll target moves 4-30 (26 moves) to see if the DR-through-finish can be compressed:

replace_and_shorten: substitute is 6 moves longer; reject.

The replace_and_shorten produced a +6 move delta (worse), so I should keep my original 30-move solution. Let me submit it now.

## Solution Summary

**Approach**: Inverse-RL axis solve
- **EO** (5 moves on inverse-RL): B' L' D' L2 U'
- **DR** (8 moves, DR-3C2E trigger): U2 F' D2 F R' F L' F'
- **HTR+Finish** (18 moves): via the 0-swap long-cycle subset

**Normal-frame solution** (after NISS inversion + cancellation): **30 moves**

FINAL_SOLUTION: ["B2", "U2", "L2", "F2", "L2", "D2", "L2", "B2", "U2", "B2", "L'", "D2", "F2", "U2", "B2", "R2", "D2", "R", "F", "L", "F'", "R", "F'", "D2", "F", "U'", "L2", "D", "L", "B"]

**Verified solution (30 moves):** `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`
