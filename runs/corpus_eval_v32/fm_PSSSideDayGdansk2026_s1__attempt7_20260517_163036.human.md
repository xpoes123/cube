# Solve — fm_PSSSideDayGdansk2026_s1__attempt7_20260517_163036

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `U2 F2 R2 U2 R2 U2 B2 U2 F2 L2 D2 U' B2 U' F2 U' R2 U R U' R L B2 D2 U' R2 F R L D B`

---

*Thinking (1):*

> Looking at the prior attempts:
> - Attempt 2: 31 moves
> - Attempt 4: 29 moves  
> - Attempt 5: 28 moves (BEST)
> 
> The best solution is 28 moves. The instruction is clear: COMMIT HARD this attempt. Pick a line and drive it to a clean finish. Don't over-ideate or abandon paths halfway through.
> 
> Let me start by inspecting the state to see what we're working with.

I'll solve this scramble with a committed, focused approach. Starting with state inspection to identify the best EO axis.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**State snapshot:** UD=8 bad edges, FB=6, RL=6. FB and RL are tied at 6 bad edges. The UD axis shows `top_pairs_on_inverse: 2`, which is a NISS-switch signal. Let me scout EO on both normal and inverse frames for FB and RL axes.

**Scouting plan:**
1. FB-normal EO (6 bad edges)
2. RL-normal EO (6 bad edges)
3. Inverse-FB EO (NISS signal from pairs tracing)
4. Compare DR options after each EO

Starting with FB-normal:

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

**FB-normal:** 5-move EO (partial shown). Let me check RL-normal:

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

**RL-normal:** Also 5-move EO. Now let me check the inverse frame. The UD axis had `top_pairs_on_inverse: 2`, suggesting NISS might help. Flipping to inverse:

NISS flip — switching to the inverse scramble.

**Now on inverse.** NISS INVARIANT: bad-edge counts don't change, but the SOLUTION to fix them does. Let me scout FB-inverse and RL-inverse:

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

**FB-inverse:** Also 5 moves. Let me check RL-inverse:

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

**All options are 5-move EO.** The prior best (28 moves) likely used one of these. To commit, I need to check DR feasibility after each. Let me apply FB-inverse EO and check DR options:

I turn `R F D' U'`.

On FB axis I recognize the EO pattern — `R'` fixes it.

**Excellent!** One more move to complete FB-EO (total 5 moves):

I turn `R'`.

**EO complete on FB-inverse in 5 moves.** Now checking DR options:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on FB:
  • DR-7C8E (U F D): 4-mv setup + 3-mv trigger (7 total) pre=DR-7C4E
  • DR-7C8E (U' F D): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E
  • DR-2C4E (U L2 U): 5-mv setup + 3-mv trigger (8 total) pre=DR-4C1E

**DR options on FB-inverse after 5-move EO:**
- DR-7C8E in 7 moves (4 setup + 3 trigger) — bad substate, expect long finish
- DR-2C4E in 8 moves (5 setup + 3 trigger) — better substate but still long

These are not great. Let me reset and try RL-inverse instead, which had the same 5-move EO length:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

**Back on inverse.** Trying RL-inverse EO:

I turn `B U B2 F`.

On RL axis I recognize the EO pattern — `D'` fixes it.

I turn `D'`.

**RL-EO complete on inverse in 5 moves.** Checking DR options:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C4E (F L2 U2 F): 5-mv setup + 4-mv trigger (9 total) pre=DR-4C2E

**RL-inverse DR:** Only a 9-move DR-4C4E option. Also not great. The best prior was 28 moves. Let me try going deeper on one promising move manually. Let me reset and commit to FB-normal (not inverse) and probe deeper:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

**Committing to FB-normal.** Apply the 5-move EO:

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

I turn `R'`.

**FB-EO complete in 5 moves (normal frame).** Checking DR deeper (max_setup=6):

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on FB.**

**No DR options on FB-normal within 6 moves.** This axis is bad. Let me try UD-inverse — the original inspection showed `top_pairs_on_inverse: 2` on UD. Reset and check UD-axis on inverse:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

**On inverse.** UD has 8 bad edges. Let me check the EO:

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

**UD-inverse:** 5-move EO also. All axes have 5-move EO. Looking at the best prior solve (28 moves from attempt 5), it was `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 R2 U B2 U' F2 L2 U' L2 U F2 R2`. This looks like it might have used inverse UD. Let me commit to UD-inverse and push through:

I turn `B' D' L' R'`.

On UD axis I recognize the EO pattern — `F'` fixes it.

I turn `F'`.

**UD-EO complete on inverse in 5 moves.** Checking DR:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on UD.**

**No DR options within 6 moves on UD-inverse either.** This is a hard scramble. Let me try a manual setup move that looks promising and re-query. Let me try R2:

I turn `R2`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on UD:
  • DR-3C2E (R U R'): 5-mv setup + 3-mv trigger (8 total) pre=DR-3C1E
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

**Found DR options after R2!**
- DR-3C2E (R U R') in 8 more moves (5 setup + 3 trigger) = **14 total to DR** (6 EO + 8 DR)
- DR-7C8E in 8 moves — bad substate

The 3C2E is promising. Per the DR-substate table, 3C2E typical post-DR = 6-8 moves. Total estimate: 6 EO + 8 DR + 7 finish ≈ **21 moves**. This is competitive with the 28-move best. **Committing to DR-3C2E:**

I turn `U D2 B2 R2 L' R U R'`.

**13 moves (auto-cancelled 1).** Note: `R2 R` cancelled to `R'` in the setup. Let me verify DR status:

Quick check: DR-locked on UD, not yet HTR.

**DR-UD confirmed in 13 moves!** Now classify HTR:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 7 moves, finish is 11 moves (first exposure — learning).

**2-swap mostly-axial subset:** 7-move HTR reduction + 11-move finish = **18 more moves**. Total projection: 13 + 18 = **31 moves**. This matches attempt 2 (31 moves). I can improve by checking for early residuals during the finish. Let me apply HTR reduction first:

For the corner reduction, I see `U' R2 U F2` (chunk of a 7-move phase) — apply and re-check.

I turn `U' R2 U F2`.

For the corner reduction: `U B2 U`.

I turn `U B2 U`.

**HTR reduction complete in 20 moves.** Quick-check before finish:

Quick check: in HTR.

**HTR confirmed.** Applying finish:

For the half-turn finish, I see `D2 L2 F2 U2` (chunk of a 11-move phase) — apply and re-check.

I turn `D2 L2 F2 U2`.

Quick check: in HTR.

**Still in HTR after 24 moves.** Continuing finish:

For the half-turn finish, I see `B2 U2 R2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `B2 U2 R2 U2`.

Quick check: in HTR.

**28 moves, still HTR.** Continuing:

For the half-turn finish: `R2 F2 U2`.

I turn `R2 F2 U2`.

A quick glance — the cube is solved.

**SOLVED in 31 moves on inverse!** Now I need to compose the NISS solution. The slot is on_inverse, so compose_niss_solution will handle the inversion algebra:

I assemble the canonical inverse-frame solution: **31 moves**, verified.

**31-move solution verified.** This matches attempt 2 (31 moves). I'm at 31 moves, which is above the 28-move best from attempt 5 BUT within the refinement threshold. I have sufficient tool calls remaining. Let me try replace_and_shorten on a large tail span to see if I can improve:

Budget check: 2040.05s sim, None tool calls remaining.

**Budget status:** I have ~2040s remaining and am sitting on a 31-move solve. The tool calls used so far are minimal. I should try replace_and_shorten on a tail span. Let me try the HTR finish portion (roughly moves 14-31):

replace_and_shorten: substitute is 3 moves longer; reject.

**Replace-and-shorten made it WORSE** (delta +3, from 31 to 34 moves). This is not helpful. I'll stick with my current 31-move solution. Let me try a different span — maybe the earlier DR portion (moves 6-13):

Wait, the tool enforces a 1-call cap (rs_calls_used: 1). I can't call it again. I must submit my current 31-move solution.

Actually, let me verify the 31-move solution is correct:

verify_solved: ✓ — 31 moves.

**Verified: 31 moves, solves the scramble.** This is worse than the best prior attempt (28 moves), but it's a complete solution. Per the SHIP RULE, I should submit this rather than risk a timeout. However, I still have significant budget (~2000s) and could try a different line. 

Let me reconsider: the instruction says "COMMIT HARD this attempt" and "don't over-ideate between branches." I committed to UD-inverse and got 31 moves, matching attempt 2. The 28-move solution from attempt 5 must have used a different approach. But I've already spent time on this line — should I reset and try another axis?

Given the instruction to "drive it to a clean finish" and not abandon halfway, and that I have a working 31-move solution, I should **submit this**. A 31-move verified solve beats a DNF.

**FINAL_SOLUTION:**

FINAL_SOLUTION: ["U2", "F2", "R2", "U2", "R2", "U2", "B2", "U2", "F2", "L2", "D2", "U'", "B2", "U'", "F2", "U'", "R2", "U", "R", "U'", "R", "L", "B2", "D2", "U'", "R2", "F", "R", "L", "D", "B"]

**Verified solution (31 moves):** `U2 F2 R2 U2 R2 U2 B2 U2 F2 L2 D2 U' B2 U' F2 U' R2 U R U' R L B2 D2 U' R2 F R L D B`
