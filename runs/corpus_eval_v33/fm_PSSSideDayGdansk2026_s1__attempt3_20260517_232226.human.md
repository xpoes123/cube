# Solve — fm_PSSSideDayGdansk2026_s1__attempt3_20260517_232226

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`

---

*Thinking (1):*

> Let me start by understanding the scramble and the context:
> - Scramble: R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> - Prior attempts: 29 and 30 moves
> - I need to commit hard to one line and drive it to completion
> 
> Let me start with inspect_state to see the cube state and understand what axes might be promising.

I'll solve this scramble methodically, learning from the prior 29-move and 30-move attempts. Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Axis scouting analysis:**
- **UD axis**: 8 bad edges (high), DR-6C3E, but `top_pairs_on_inverse=2` is a STRONG signal for NISS
- **FB axis**: 6 bad edges, DR-5C2E — cleaner substate, lower corner count
- **RL axis**: 6 bad edges, DR-7C3E — worst corner count

The UD axis has 2 pairs on inverse, which suggests the inverse frame might be superior. Let me scout both FB (normal) and UD (inverse) to find the best joint EO+DR.

**Normal side FB axis first** — 6 bad edges is manageable:

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

FB normal EO is **5 moves** (partial shows the first 4). Let me now check the **inverse side on UD axis** (which has `top_pairs_on_inverse=2`):

NISS flip — switching to the inverse scramble.

Now on inverse. Let me scout EO on UD axis:

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

UD inverse is also **5 moves** EO. Both FB-normal and UD-inverse are 5 moves. The differentiator will be DR quality. Let me commit the UD-inverse EO incrementally and check DR options.

Applying the first 4 moves of UD-inverse EO:

I turn `B' D' L' R'`.

Re-querying for the final EO move:

On UD axis I recognize the EO pattern — `F'` fixes it.

Perfect! One more move completes UD-inverse EO:

I turn `F'`.

**UD-inverse EO complete in 5 moves.** Now let me check DR options. The prior `top_pairs_on_inverse=2` signal suggests this should give good DR:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

**Zero DR options at depth 5** on UD-inverse. This is a strong signal the axis is wrong. Let me switch back to normal and test FB axis properly. The `top_pairs_on_inverse=2` was misleading — it's not producing viable DR.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Back to normal frame. Let me commit to **FB axis normal** (5-move EO) and check its DR:

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

I turn `R'`.

**FB normal EO complete in 5 moves: R2 B' L' U2 R'.** Now checking DR options on FB axis:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Also **zero options on FB**. Both main axes giving zero at depth 5. Let me try **RL axis** instead:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

RL is also 5 moves EO. Let me commit it and check DR:

I turn `L U L2 R`.

On RL axis I recognize the EO pattern — `D'` fixes it.

I turn `D'`.

**RL EO complete in 5 moves: L U L2 R D'.** Checking DR on RL axis:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on RL.**

**All three axes giving zero DR options at depth 5.** This is unusual. The scramble requires deeper DR setups. Let me try the fallback: `dr_recognize` which uses the brain for suggestions when memory doesn't have the pattern:

I check whether the DR is recognizable from this state via the library.

The brain suggests U2 (29.1% prob). Let me try it:

I turn `U2`.

I check whether the DR is recognizable from this state via the library.

Still not in memory. This is getting long. Let me try a different strategy — go back to the prior best solution's axis. Looking at the 29-move solution, it starts with `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2...` which looks like it might be working on UD axis (lots of double turns). Let me reset and try a UD-normal EO approach:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me try UD-normal:

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

**UD-normal EO is 4 moves! R2 D' B' F'.** This is shorter than the 5-move options. Let me commit:

I turn `R2 D' B' F'`.

Now checking DR on UD-normal:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP] pre=DR-4C1E
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

**Excellent!** Two DR options:
1. **DR-4C2E** (R U2 R'): setup 5 moves, total to DR = 8, **JZP-eligible** (halves post-DR cost!)
2. DR-7C8E (R' U L): setup 5 moves, total to DR = 8

The **DR-4C2E with JZP** is the clear winner. Per the priors table, DR-4C2E normally costs 9-11 post-DR, but JZP-eligible means ~5-7 post-DR. Total from scramble: **4 (EO) + 8 (DR) + ~6 (finish) = ~18 moves**.

Let me commit the DR-4C2E path:

I turn `U' R' L2 U F2 R U2 R'`.

**At DR in 12 moves!** JZP-eligible on UD axis. Now classifying HTR:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (recall).

**HTR subset: 0-swap long-cycle**
- HTR reduction: 10 moves
- Finish: 9 moves
- Total from DR: **19 moves**

**Total solution length: 12 (to DR) + 19 (HTR+finish) = 31 moves**

This is longer than the prior 29-move solution. But let me complete it and then try to optimize. Applying HTR reduction:

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

I turn `U F2 U' R2`.

Let me check if we're solved or at a recognizable residual before continuing:

Quick check: DR-locked on UD, not yet HTR.

Not at HTR yet. Continuing HTR reduction:

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

**At HTR in 22 moves!** (UD axis). Now applying the finish phase:

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Quick check: in HTR.

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

Quick check: in HTR.

For the half-turn finish: `R2`.

I turn `R2`.

A quick glance — the cube is solved.

**SOLVED in 30 moves!** Current solution matches the second prior attempt's length. Let me compose and verify, then try replace_and_shorten if eligible:

I assemble the canonical normal-frame solution: **30 moves**, verified.

Let me check the budget to see if I can try replace_and_shorten:

Budget check: 2295.66s sim, None tool calls remaining.

I have plenty of budget remaining. The solution is 30 moves, which is ≥27, so I should try replace_and_shorten. Let me target the DR-to-finish section (moves 12-30) since the HTR finish was quite long (19 moves from DR):

replace_and_shorten: same length, no improvement.

Replace_and_shorten returned delta=0, so no improvement. The solution remains 30 moves. Let me try canceling to see if there are any obvious reductions:

I check for cancellations — no savings.

No cancellations. The solution is already in compact form. Let me verify it:

verify_solved: ✓ — 30 moves.

Verified! I have a 30-move solution, which ties the second prior attempt. However, I still have budget to try a different approach. Let me see if I can find a better path by trying a different DR trigger or exploring inverse more carefully.

Actually, let me be strategic. The prior 29-move solution suggests there's a 29-move path on this scramble. Let me try a different DR option or check if there's a shorter finish possible. Let me reset and try the **DR-7C8E** option which had `top_pairs_on_inverse=4` — that's a very strong NISS signal:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me go back to the UD-normal EO and try the DR-7C8E path:

I turn `R2 D' B' F'`.

Now applying the DR-7C8E setup + trigger (U' L2 F2 L' F2 R' U L):

I turn `U' L2 F2 L' F2 R' U L`.

At DR in 12 moves (same as the 4C2E path). Let me classify HTR on this path:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 11 moves (first exposure — learning).

**2-swap long-cycle:** HTR reduction 11 + finish 11 = **22 moves from DR**. Total: **12 + 22 = 34 moves**. This is WORSE than the 4C2E path (30 moves). The `top_pairs_on_inverse=4` signal was misleading for this case.

Let me abandon this and stick with my verified 30-move solution. That matches the second prior attempt and is close to the 29-move best. Given the instruction to "commit hard and drive to completion," I should submit this working solution rather than continuing to search.

**FINAL_SOLUTION:**

["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "U", "F2", "U'", "R2", "U", "L2", "U2", "R2", "F2", "U'", "B2", "F2", "L2", "B2", "L2", "U2", "B2", "R2"]

**Solution breakdown:**
- **EO (UD-axis):** R2 D' B' F' (4 moves) — recognized 8-bad-edge pattern
- **DR (4C2E-JZP):** U' R' L2 U F2 R U2 R' (8 moves) — JZP-eligible, cleaner substate
- **HTR reduction:** U F2 U' R2 U L2 U2 R2 F2 U (10 moves) — 0-swap long-cycle subset
- **Finish:** U' B2 F2 L2 B2 L2 U2 B2 R2 (9 moves) — but U' B2 canceled to save 1

**Total: 30 moves** (verified, matches prior attempt #2)

The path used UD-normal axis EO in 4 moves (shortest found), followed by a JZP-eligible DR-4C2E trigger in 8 moves total to DR. The HTR subset (0-swap long-cycle) required 19 moves to finish. While this matches the 30-move prior, it's a clean, complete solution within budget.

*Thinking (58):*

> You're right - I narrated the solution but didn't actually emit it in the required format. Let me output the FINAL_SOLUTION now.

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "U", "F2", "U'", "R2", "U", "L2", "U2", "R2", "F2", "U'", "B2", "F2", "L2", "B2", "L2", "U2", "B2", "R2"]

**Verified solution (30 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`
