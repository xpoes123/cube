# Solve — fm_PSSSideDayGdansk2026_s1__attempt1_20260517_142055

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I need to follow the FMC methodology outlined in the instructions:
> 1. Start with inspect_state to see the bad edges per axis
> 2. Scout EO on multiple axes (normal and inverse)
> 3. Compare DR options for each viable EO
> 4. Commit to the best joint EO+DR path
> 5. Execute DR → HTR → finish
> 6. Verify and submit
> 
> Let me begin with inspect_state to see what I'm working with.

I'll solve this FMC scramble step by step, starting with inspection to understand the cube state and plan my approach.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Initial Inspection Analysis:**
- **Bad edges**: UD=8, FB=6, RL=6
- **DR closeness**: UD has DR-6C3E (not JZP), FB has DR-5C2E, RL has DR-7C3E
- **Important**: UD shows `top_pairs_on_inverse: 2` — this is a strong NISS-switch signal

**Strategy:** 8 bad edges on UD-axis is typically a 3-5 move EO using the `<m> F <m'> B` symmetry pattern. However, with 2 pairs preserved on inverse, I should check the inverse frame first. The NISS invariant tells me bad-edge counts are identical on normal/inverse, but the SOLUTION differs.

Let me scout EO on both normal and inverse frames for the FB and RL axes (both at 6 bad edges), then also check UD-inverse since we have 2 pairs preserved.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

**FB-axis EO (normal):** 5 moves total, first chunk is R2 B' L' U2. That's on the longer side. Let me check RL-axis on normal:

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

**RL-axis EO (normal):** Also 5 moves. Both FB and RL are 5-movers on normal. Now let me switch to inverse and check these axes there, plus UD-inverse since we have 2 pairs preserved.

NISS flip — switching to the inverse scramble.

Now I'm on the inverse frame. Let me check EO for UD, FB, and RL axes:

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

**All inverse EOs are also 5 moves.** This is not ideal — all six (side, axis) combinations give 5-move EOs. However, the 2 pairs preserved on UD-inverse is still a strong signal. Let me probe DR options after each EO to make the joint decision.

Let me test UD-inverse first since we have the pairs signal. I'll apply the first 4 moves of the EO and check DR options:

I turn `B' D' L' R'`.

On UD axis I recognize the EO pattern — `F'` fixes it.

Excellent! One more move completes UD-EO on inverse: **5 moves total (B' D' L' R' F')**. Now let me check DR options:

I turn `F'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

**No DR triggers found within 5 moves on UD-inverse.** This is a bad sign — the pairs signal didn't pan out for UD. Let me reset and try a different axis. Let me go back and check FB or RL on inverse.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me try FB-axis on inverse. Flipping to inverse again:

NISS flip — switching to the inverse scramble.

I turn `R F D' U'`.

On FB axis I recognize the EO pattern — `R'` fixes it.

Perfect! FB-inverse EO is **5 moves: R F D' U' R'**. Let me complete it and check DR options:

I turn `R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on FB:
  • DR-7C8E (U F D): 4-mv setup + 3-mv trigger (7 total) pre=DR-7C4E
  • DR-7C8E (U' F D): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E
  • DR-2C4E (U L2 U): 5-mv setup + 3-mv trigger (8 total) pre=DR-4C1E

**FB-inverse DR options:**
- **DR-7C8E in 7 moves** (4 setup + 3 trigger): This is a bad substate (7c8e = very long finish)
- **DR-2C4E in 8 moves**: Better substate but still 8 moves to DR

**Total so far: 5 (EO) + 7 (DR) = 12 moves to DR** with a 7C8E substate, which typically needs 15+ moves to finish. That's looking at ~27+ total. Not great.

Let me try RL-axis on inverse:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B U B2 F`.

On RL axis I recognize the EO pattern — `D'` fixes it.

Great! RL-inverse EO is **5 moves: B U B2 F D'**. Let me complete and check DR:

I turn `D'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C4E (F L2 U2 F): 5-mv setup + 4-mv trigger (9 total) pre=DR-4C2E

**RL-inverse:** DR-4C4E in 9 moves (5 setup + 4 trigger). Total: **5 (EO) + 9 (DR) = 14 moves to DR**. 4C4E substate typically finishes in 12-14 moves, so we're looking at ~26-28 total.

Let me also check the normal frame for comparison. Let me try RL-axis on normal:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `L U L2 R`.

On RL axis I recognize the EO pattern — `D'` fixes it.

RL-normal also 5 moves: **L U L2 R D'**. Let me check DR:

I turn `D'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on RL.**

No DR options on RL-normal within 5 moves. Let me try FB-normal:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

FB-normal EO is **5 moves: R2 B' L' U2 R'**:

I turn `R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

No DR options on FB-normal either. Let me check UD-normal as well:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Actually, let me think strategically. I've found:
- **FB-inverse**: 5 EO + 7 DR = 12 to DR (7C8E substate, ~15 finish = ~27 total)
- **RL-inverse**: 5 EO + 9 DR = 14 to DR (4C4E substate, ~13 finish = ~27 total)

Both are around 27 total. Let me try to manually explore a bit more on FB-inverse since it has the shortest DR. Let me also try increasing max_setup to 6 on the better options:

NISS flip — switching to the inverse scramble.

I turn `R F D' U' R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on FB:
  • DR-7C8E (U F D): 4-mv setup + 3-mv trigger (7 total) pre=DR-7C4E
  • DR-7C8E (U' F D): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E
  • DR-2C4E (U L2 U): 5-mv setup + 3-mv trigger (8 total) pre=DR-4C1E

Same results. The best option is **DR-7C8E in 7 moves**. Let me commit to this path since it's the shortest to DR I've found. I'll proceed with FB-inverse:

**Decision: FB-inverse axis, 5 EO + 7 DR = 12 to DR**

Applying the DR setup and trigger:

I turn `D F' L2 B'`.

I turn `U F D`.

Now I'm at DR on FB-axis (inverse frame). Let me classify the HTR substate:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 7 moves, finish is 12 moves (first exposure — learning).

**HTR classification:** 2-swap mostly-axial subset
- HTR reduction: 7 moves
- Finish: 12 moves
- **Total from DR to solved: 19 moves**

**Projected total:** 5 (EO) + 7 (DR) + 19 (HTR+finish) = **31 moves**

This is quite long. Let me execute it to get a working solution, then I can consider optimization. Let me apply HTR reduction:

For the corner reduction, I see `F' U2 R2 L2` (chunk of a 7-move phase) — apply and re-check.

I turn `F' U2 R2 L2`.

Let me do a quick check before continuing:

Quick check: DR-locked on FB, not yet HTR.

Still in DR on FB. Let me continue HTR reduction:

For the corner reduction: `F R2 B`.

I turn `F R2 B`.

Quick check: in HTR.

Great! I'm now in HTR (is_htr_ud: true). Let me apply the finish phase:

For the half-turn finish, I see `L2 F2 U2 R2` (chunk of a 12-move phase) — apply and re-check.

I turn `L2 F2 U2 R2`.

Quick check: in HTR.

Still in HTR. Let me continue the finish:

For the half-turn finish, I see `B2 R2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `B2 R2 F2 U2`.

Quick check: in HTR.

For the half-turn finish: `R2 U2 R2 U2`.

I turn `R2 U2 R2 U2`.

A quick glance — the cube is solved.

Excellent! The cube is solved. I'm on the inverse frame, so I need to use compose_niss_solution to get the correct normal-frame solution:

I assemble the canonical inverse-frame solution: **31 moves**, verified.

I have a 31-move solution! Now let me check the budget and consider if I should try replace_and_shorten:

Budget check: 1753.79s sim, None tool calls remaining.

I have plenty of budget remaining (1753s simulated, ~1285s real wall time). Since my solution is 31 moves and I have enough budget, I should try replace_and_shorten to optimize it. The gate requires ≥27 moves AND ≥30 tool calls remaining — I'm at 31 moves, so I qualify.

Let me try replace_and_shorten on a large span. I'll target the HTR-finish portion (moves 12-31), which is 19 moves:

r&s: too few tool calls remaining (22) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

I don't have enough tool calls remaining for replace_and_shorten. Let me verify and submit my current solution:

verify_solved: ✓ — 31 moves.

Perfect! The solution is verified. Let me check if there are any obvious cancellations I can make manually:

I check for cancellations — no savings.

No cancellations were found. The solution is already optimally formatted.

## FINAL_SOLUTION

**Solution breakdown:**
- **EO (FB-axis, inverse):** R F D' U' R' (5 moves)
- **DR setup:** D F' L2 B' (4 moves)  
- **DR trigger (7C8E):** U F D (3 moves)
- **HTR reduction:** F' U2 R2 L2 F R2 B (7 moves)
- **HTR finish:** L2 F2 U2 R2 B2 R2 F2 U2 R2 U2 R2 U2 (12 moves)

Total: **31 moves**

FINAL_SOLUTION: ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]

**Verified solution (31 moves):** `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`
