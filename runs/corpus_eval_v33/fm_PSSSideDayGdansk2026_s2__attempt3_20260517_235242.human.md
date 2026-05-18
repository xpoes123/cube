# Solve — fm_PSSSideDayGdansk2026_s2__attempt3_20260517_235242

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `B2 R' D' R' D' R U F2 R2 U B2 U2 R2 U B2 F2 U2 R2 F2 U2 L2 U2 F U' R2 B'`

---

*Thinking (1):*

> Looking at the prior attempts:
> - Attempt 1: 34 moves
> - Attempt 2: 31 moves (best so far)
> 
> The instruction is clear: COMMIT HARD this attempt. Pick a line and drive it to completion. Don't over-ideate between branches.
> 
> Let me start with inspect_state to see what we have.
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I'll start by inspecting the state, then scout EO on multiple axes (normal + inverse), check DR options for promising candidates, commit to one line, and drive it through to completion.
> 
> The key rules:
> 1. NISS invariant: bad_edges_per_axis is IDENTICAL on normal and inverse
> 2. Always check inverse EO too
> 3. DR decision is JOINT: EO_len + DR_total
> 4. DR ≤6 moves in 85.7% of elite solves; DR ≥10 never appears in sub-22
> 5. Substate quality matters more than DR length (3C2E >> 4C4E)
> 6. JZP halves post-DR cost
> 7. Ship rule: get a complete verified solve, then stop unless there's obvious improvement
> 
> Let me start.

I'll solve this scramble systematically, learning from the prior 31-move result. Let me start by inspecting the state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**Observation**: Bad edges: UD=6, FB=4, RL=4. Both FB and RL look cleaner for EO. The UD axis shows `top_pairs_on_inverse: 3` — that's a STRONG NISS signal (≥2 pairs). Let me scout EO on both normal and inverse sides for FB and RL axes, then check UD-inverse too given the pairs signal.

**Plan**: Scout FB-normal, RL-normal, then flip to inverse and scout UD-inverse (since it has 3 pairs preserved). Compare EO+DR joint costs before committing.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL have 4-move EOs on the normal side. Now let me check the inverse side, especially for UD given the 3 pairs signal.

NISS flip — switching to the inverse scramble.

Now on inverse. Let me scout UD-inverse EO (the axis with 3 pairs) and also check FB/RL inverse for comparison.

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

**Excellent find!** FB-inverse has a 2-move EO (`U2 R'`), versus 4 moves on all the normal-side axes. UD-inverse also 4 moves. Now I need to test DR options for each promising candidate:
- **FB-inverse**: 2-move EO
- **FB-normal**: 4-move EO  
- **RL-normal**: 4-move EO

Let me commit the FB-inverse EO and check DR options there first, since it has the shortest EO.

I turn `U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**No DR options found on FB-inverse within 5-move setup!** This is a bad sign — the EO is short but the DR path is blocked. Let me try dr_recognize to see if the brain suggests next moves.

I check whether the DR is recognizable from this state via the library.

Brain suggests R2 (65% confidence). But this is getting exploratory — I'm now 2 moves into FB-inverse with unclear DR path. Let me check the FB-normal path instead (4-move EO), which might have cleaner DR.

Let me reset and try FB-normal.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `B2 L2 U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

FB-normal also has no DR options at depth 5! This axis is problematic. Let me try RL-normal instead.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B F2 U'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Found DR on RL! **DR-7C8E** with 5-move setup + 3-move trigger = **8 moves to DR total**. But DR-7C8E is a bad substate (7 corners, 8 edges misplaced). This will have a long finish (~14+ moves post-DR). Total projection: 4 EO + 8 DR + 14 finish ≈ 26 moves minimum.

Let me check if I can find better DR by trying dr_recognize after this EO.

I check whether the DR is recognizable from this state via the library.

RL axis is also struggling. Given that both FB and RL axes have weak DR paths, let me check the UD-inverse path (which had 3 pairs preserved and 4-move EO). The pairs signal is strong.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B R2 U F'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

UD-inverse also has no DR options at depth 5! This is a difficult scramble. All three axes I've checked are struggling with DR. Let me try using the brain iteratively on the UD-inverse path since it had the 3 pairs signal.

I check whether the DR is recognizable from this state via the library.

Brain suggests U (42%). Let me try that and re-check.

I turn `U`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Still nothing. This is concerning — I'm now 5 moves deep with no clear DR path. Let me try one more brain iteration.

I check whether the DR is recognizable from this state via the library.

Very strong D signal (93%). Let me apply it.

I turn `D`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on UD:
  • DR-3C2E (R U R'): 5-mv setup + 3-mv trigger (8 total) pre=DR-3C1E
  • DR-2C4E (R F2 R): 5-mv setup + 3-mv trigger (8 total) [JZP] pre=DR-4C1E
  • DR-4C4E (R): 5-mv setup + 1-mv trigger (6 total) [JZP] pre=DR-4C2E

**Breakthrough!** Found DR options after the D move. Comparing the candidates:

1. **DR-3C2E (R U R')**: 5+3=8 total, non-JZP → post-DR ~6-8 moves → total ~14-16 from current state
2. **DR-2C4E (R F2 R)**: 5+3=8 total, **JZP** → post-DR ~5-7 moves → total ~13-15 
3. **DR-4C4E (R or R')**: 5+1=6 total, **JZP** → post-DR ~7-9 moves → total ~13-15

The 4C4E option reaches DR in only **6 moves from here** and is JZP-eligible. Even though 4C4E typically has longer finishes, JZP halves that cost. Total projection: 4 EO + 6 RZP + 6 DR + ~8 finish ≈ **24-26 moves**.

**Decision**: Take the **DR-4C4E (R)** option with JZP. Setup: `R2 L' U' L' B2`, trigger: `R`.

I turn `R2 L' U' L' B2 R`.

Excellent! I'm now at DR on the UD-inverse axis. Total so far: 4 EO + 2 brain-guided + 6 DR = **12 moves**. Now let me classify the HTR subset and finish.

Quick check: DR-locked on UD, not yet HTR.

Confirmed DR on UD. Let me classify the HTR subset.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 8 moves (recall).

**HTR subset: 2-swap long-cycle**. HTR reduction = 11 moves, finish = 8 moves, total = **19 moves from DR**. 

Total projection: 12 (to DR) + 19 (HTR+finish) = **31 moves**. That matches the prior best attempt! Let me apply the HTR phases and check for any opportunistic shortcuts.

For the corner reduction, I see `U R2 U' R2` (chunk of a 11-move phase) — apply and re-check.

I turn `U R2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction, I see `U R2 U' R2` (chunk of a 7-move phase) — apply and re-check.

I turn `U R2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `U B2 D`.

I turn `U B2 D`.

Quick check: in HTR.

Great! Now at HTR (is_htr_ud: true). 23 moves so far. Let me apply the finish phase.

For the half-turn finish, I see `U2 R2 F2 L2` (chunk of a 8-move phase) — apply and re-check.

I turn `U2 R2 F2 L2`.

Quick check: in HTR.

For the half-turn finish: `U2 B2 U2 F2`.

I turn `U2 B2 U2 F2`.

A quick glance — the cube is solved.

**Solved!** 31 moves on the inverse side. Now I need to compose the final solution using compose_niss_solution, which will invert the inverse-side moves and verify the solve.

I assemble the canonical inverse-frame solution: **31 moves**, verified.

Perfect! The solution is **31 moves**, matching the prior best attempt. The solution has been verified by compose_niss_solution.

Let me check the gates for replace_and_shorten: total_moves ≥ 27 ✓ (31 moves). Let me check my tool call budget.

Budget check: 1986.94s sim, None tool calls remaining.

I have 1987s remaining (plenty of budget). I'm at 31 moves, which meets the ≥27 gate. However, the prior attempt ALSO reached 31 moves, and the instruction says to "COMMIT HARD" and get a complete solution rather than chasing optimization mid-solve.

Since I have a verified 31-move solution (matching the prior best), I should try replace_and_shorten ONCE to see if I can improve. The tool has a 1-call cap and gates are met. Let me try shortening a large tail span.

replace_and_shorten on the tail span: substitute is 5 moves shorter. Accepted.

**Excellent!** Replace-and-shorten found a 5-move improvement! The new solution is **26 moves** and solves the scramble. This is better than both prior attempts (34 and 31).

Let me update the slot with the new history and compose the final solution.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B R2 U F' U2 L2 U2 F2 R2 U2 F2 B2 U' R2 U2 B2 U' R2 F2 U' R' D R D R B2`.

I assemble the canonical inverse-frame solution: **26 moves**, verified.

Perfect! Let me verify this solution.

verify_solved: ✓ — 26 moves.

Excellent! **26 moves verified**. This is a 5-move improvement over the prior best (31 moves) and 8 moves better than the first attempt (34 moves).

## Solution Summary

**Route taken**: UD-axis on inverse (NISS)
- **EO**: 4 moves (`B R2 U F'` on inverse)
- **DR setup**: 2 brain-guided moves (`U D`) + 6 DR moves (`R2 L' U' L' B2 R`) = **12 moves to DR**
- **DR substate**: DR-4C4E with JZP eligibility  
- **HTR+finish**: 11 moves HTR reduction + 8 moves finish = **19 moves**
- **Initial solve**: 31 moves
- **After replace_and_shorten**: **26 moves** (5-move savings)

The key decisions:
1. Checked multiple EO axes on both normal and inverse sides
2. Followed the strong 3-pairs signal on UD-inverse
3. Used brain-guided DR exploration when trigger_options returned nothing
4. Picked the JZP-eligible DR-4C4E despite longer DR length (saved post-DR moves)
5. Applied replace_and_shorten on the tail span (saved 5 moves)

**FINAL_SOLUTION**: ["B2", "R'", "D'", "R'", "D'", "R", "U", "F2", "R2", "U", "B2", "U2", "R2", "U", "B2", "F2", "U2", "R2", "F2", "U2", "L2", "U2", "F", "U'", "R2", "B'"]

*Thinking (52):*

> The user is right - I verified the solution and summarized it, but I never actually emitted the FINAL_SOLUTION in the required format. I need to output it now.
> 
> The verified solution is:
> ["B2", "R'", "D'", "R'", "D'", "R", "U", "F2", "R2", "U", "B2", "U2", "R2", "U", "B2", "F2", "U2", "R2", "F2", "U2", "L2", "U2", "F", "U'", "R2", "B'"]
> 
> 26 moves, verified by verify_solved.

FINAL_SOLUTION: ["B2", "R'", "D'", "R'", "D'", "R", "U", "F2", "R2", "U", "B2", "U2", "R2", "U", "B2", "F2", "U2", "R2", "F2", "U2", "L2", "U2", "F", "U'", "R2", "B'"]

**Verified solution (26 moves):** `B2 R' D' R' D' R U F2 R2 U B2 U2 R2 U B2 F2 U2 R2 F2 U2 L2 U2 F U' R2 B'`
