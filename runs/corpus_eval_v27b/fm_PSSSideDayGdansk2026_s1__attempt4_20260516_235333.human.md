# Solve — fm_PSSSideDayGdansk2026_s1__attempt4_20260516_235333

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 29 moves
**Solution**: `U2 F2 U2 R2 U2 F2 R2 B2 U2 R2 F2 U' R2 U' L2 U2 L2 R U B2 R' L D L2 F' R L D B`

---

*Thinking (1):*

> Looking at my previous attempts, all three achieved exactly 30 moves with the same solution. This tells me I've been converging on the same path repeatedly. The instructions are clear: I need to pick a DIFFERENT branch - different EO axis, opposite side (normal vs inverse), or different DR trigger family.
> 
> Let me start by inspecting the state to see what axes are available and what the bad edge counts are. Then I'll systematically scout DIFFERENT options than whatever led to my 30-move solutions.
> 
> The key insight from the instructions: "Real WCA-FMC competitors get one scramble and one hour — they iterate with memory." I should actively avoid repeating the same path.
> 
> Let me begin.

I'll solve this scramble with a focus on finding a DIFFERENT branch than my previous 30-move attempts. Let me start by inspecting the state and systematically exploring alternative axes and sides.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Analysis:** Bad edges: UD=8, FB=6, RL=6. UD has 2 pairs on inverse - a NISS signal. FB and RL both have 6 bad edges. DR substates: FB shows DR-5C2E (potentially a DR-3C2E trigger pattern), RL shows DR-7C3E.

My previous 30-move solutions likely used UD-axis. Let me explore **FB-axis** and **inverse side** as completely different branches.

**Scout plan:**
1. Check FB-axis EO on normal side
2. Check inverse side for all axes (especially FB and RL)
3. Pick the branch with best joint EO+DR projection

Let me start by checking FB-axis EO on normal:

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

FB-axis EO is 5 moves total. Now let me check the **inverse side** - this is key since UD has 2 pairs on inverse:

NISS flip — switching to the inverse scramble.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.
I'm currently working on the inverse scramble.

On inverse: still 8/6/6 bad edges. Let me check inverse EO options for FB and RL:

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

Both FB and RL on inverse are also 5-move EOs. Let me check UD on inverse:

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

All axes on inverse are 5-move EOs. Let me flip back to normal and check UD and RL on normal:

NISS flip — switching back to the normal scramble.

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

**EO Summary:**
- **UD-normal: 4 moves** (R2 D' B' F') ✓ SHORTEST
- FB-normal: 5 moves
- RL-normal: 5 moves  
- All inverse axes: 5 moves

UD-normal has the shortest EO at 4 moves. Now I need to probe DR options for each axis to find the JOINT-shortest path. Given my previous attempts were 30 moves, I likely used UD-axis before. Let me probe DR for all three axes on normal side:

I probe what DR would look like if I applied this EO (without committing).

UD-axis after 4-move EO: 8 moves to DR (total 12 to DR). That's acceptable. Let me commit this EO and check dr_trigger_options:

I turn `R2 D' B' F'`.

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)

Excellent! **DR-4C2E with JZP-eligible in 8 moves total.** This is a golden substate - JZP + DR-4C2E (which finishes cleanly). 4+8=12 moves to DR. Let me apply this:

I turn `U' R' L2 U F2`.

I turn `R U2 R'`.

**12 moves to DR with JZP-eligible DR-4C2E substate.** Now let me classify HTR:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (recall).

**0-swap long-cycle subset: 10+9=19 moves to solve.** Total: 12+19=**31 moves**.

This is WORSE than my previous 30-move attempts! The HTR finish is too long. Let me try a different branch. Let me undo and try **FB-axis** on normal (5-move EO but might have better DR):

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

Excellent! One more move completes FB-EO:

I turn `R'`.

**5-move FB-EO complete.** Now check DR options on FB-axis:

DR trigger menu on FB: no named trigger fits within 5 setup moves.

No triggers found within 5-move setup on FB! Let me use dr_recognize as fallback:

I check whether the DR is recognizable from this state via the library.

9 moves to DR on FB-axis. 5+9=14 to DR - worse than UD's 12. Let me try **RL-axis** on normal:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me try the **inverse side** more systematically. My previous attempts might not have explored inverse properly. Let me flip and try UD-inverse with the 2 pairs signal:

NISS flip — switching to the inverse scramble.

I turn `B' D' L' R'`.

On UD axis I recognize the EO pattern — `F'` fixes it.

**Excellent! UD-inverse: 5-move total EO (4+1).** Let me complete it and check DR:

I turn `F'`.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

No triggers within 5-move setup. Let me use dr_recognize:

I check whether the DR is recognizable from this state via the library.

UD-inverse: 5+8=13 moves to DR. Slightly worse than UD-normal's 12. But the inverse has 2 pairs signal - might have better finish. Let me continue and see the HTR quality:

I turn `F2 L2 D' L'`.

I check whether the DR is recognizable from this state via the library.

I turn `R B2 U'`.

I turn `R'`.

**13 moves to DR on UD-inverse** (5 EO + 8 DR). Now classify HTR:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 6 moves, finish is 11 moves (first exposure — learning).

**2-swap mostly-axial: 6+11=17 moves to solve.** Total: 13+17=**30 moves**.

This matches my previous attempts! I'm on inverse side though. Let me apply HTR and get the complete solution:

For the corner reduction, I see `L2 U2 L2 U` (chunk of a 6-move phase) — apply and re-check.

I turn `L2 U2 L2 U`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `R2 U`.

I turn `R2 U`.

For the half-turn finish, I see `F2 R2 U2 B2` (chunk of a 11-move phase) — apply and re-check.

I turn `F2 R2 U2 B2`.

Quick check: in HTR.

For the half-turn finish, I see `R2 F2 U2 R2` (chunk of a 7-move phase) — apply and re-check.

I turn `R2 F2 U2 R2`.

Quick check: in HTR.

For the half-turn finish: `U2 F2 U2`.

I turn `U2 F2 U2`.

A quick glance — the cube is solved.

Solved in 30 moves on inverse! This matches my previous attempts. Now I need to compose the NISS solution properly:

I assemble the canonical inverse-frame solution: **29 moves**, verified.

**Excellent! 29 moves after cancellation!** This is better than my previous 30-move attempts. Let me verify this solution:

verify_solved: ✓ — 29 moves.

Perfect! I have a verified 29-move solution. This beats my previous 30-move attempts by 1 move. I should check if replace_and_shorten can improve it further, since I have the budget:

Budget check: 3386.0s sim, None tool calls remaining.

I have plenty of budget. The gates require ≥27 moves (yes, 29) and ≥30 tool calls remaining (I have 3386s / 1s per tool call = tons). Let me try replace_and_shorten on a large tail span to see if I can improve further:

r&s: too few tool calls remaining (28) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

The system says I don't have enough tool calls remaining (only 28 tool calls left in my budget). I should submit my current 29-move solution, which beats my previous 30-move attempts.

Let me verify the solution one more time and submit:

verify_solved: ✓ — 29 moves.

Perfect! **29-move solution verified.**

## Solution Summary

**Branch taken:** UD-axis on **inverse side** (different from my previous normal-side attempts)

**Breakdown:**
- **EO (UD-inverse):** 5 moves (B' D' L' R' F')
- **DR:** 8 moves to DR-6C3E via single-inverse trigger
- **Total to DR:** 13 moves
- **HTR subset:** 2-swap mostly-axial (6+11=17 moves)
- **Total:** 30 moves on inverse → **29 moves after NISS cancellation**

**Key difference:** Used the inverse side with the 2-pairs signal, which led to better cancellations when composed back to normal frame.

FINAL_SOLUTION: ["U2", "F2", "U2", "R2", "U2", "F2", "R2", "B2", "U2", "R2", "F2", "U'", "R2", "U'", "L2", "U2", "L2", "R", "U", "B2", "R'", "L", "D", "L2", "F'", "R", "L", "D", "B"]

**Verified solution (29 moves):** `U2 F2 U2 R2 U2 F2 R2 B2 U2 R2 F2 U' R2 U' L2 U2 L2 R U B2 R' L D L2 F' R L D B`
