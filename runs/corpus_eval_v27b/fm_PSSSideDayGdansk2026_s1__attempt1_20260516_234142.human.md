# Solve — fm_PSSSideDayGdansk2026_s1__attempt1_20260516_234142

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble. I should start by inspecting the initial state to see the bad edges per axis, DR closeness, and other key metrics. Let me begin with inspect_state on the 'main' slot.

I'll solve this scramble using the FMC methodology. Let me start by inspecting the initial state to understand what I'm working with.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Good! I can see:
- **Bad edges per axis**: UD=8, FB=6, RL=6. The scramble has 8 bad edges on UD (all-bad would be 12), 6 on FB, and 6 on RL.
- **DR closeness**: UD is DR-6C3E, FB is DR-5C2E (best!), RL is DR-7C3E.
- **Pairs on inverse (UD)**: 2 pairs preserved → NISS-switch signal.
- **ARM stats**: FB-axis shows arm_other_axis C=6, E=3 on UD.

**Initial axis scout plan**: FB has the best DR-closeness (DR-5C2E) and only 6 bad edges. Let me check both normal and inverse EO options on FB and UD before committing.

Let me scout EO on FB-axis first (normal side):

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

FB-axis EO on normal is **5 moves total** (4 visible now). Let me check UD-axis EO (normal side) as well:

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

UD-axis EO on normal is **4 moves**. Now let me check the **inverse side** for both axes, since `top_pairs_on_inverse=2` signals a potential NISS opportunity.

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check UD-axis EO on the inverse:

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

UD-inverse EO is **5 moves**. Let me check FB-inverse:

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

FB-inverse is also **5 moves**. So my EO candidates:
- **UD-normal**: 4 moves (R2 D' B' F')
- **FB-normal**: 5 moves
- **UD-inverse**: 5 moves
- **FB-inverse**: 5 moves

UD-normal wins on EO length. But I need to check **DR total** for each, not just EO length. Let me probe DR after UD-normal EO:

NISS flip — switching back to the normal scramble.

Back to normal. Let me probe DR on UD-axis after the 4-move UD-normal EO:

I probe what DR would look like if I applied this EO (without committing).

UD-normal: EO=4, DR=8, **total to DR = 12**. Let me also probe FB-normal:

I probe what DR would look like if I applied this EO (without committing).

I need the full 5-move FB EO. Let me apply the first 4 moves temporarily to see the 5th:

I try `R2 B' L' U2` on top to see the after-state (without committing).

After 4 moves, FB still has 4 bad edges. I need one more move. Let me check which move completes FB EO. The 4 bad edges are on R-side (UR, DR, FR, BR). An R or R' flip should complete it. Let me commit to the **UD-normal path** since it has a clear 4-move EO and total-to-DR of 12 moves. Let me apply the UD-normal EO and then use dr_trigger_options to find the best DR:

I turn `R2 D' B' F'`.

**EO complete on UD-axis (4 moves):** R2 D' B' F'. Now let me find the best DR trigger options on UD:

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)

Excellent! Two DR options, both **8 moves total to DR**:
1. **DR-4C2E (R U2 R')**: 5-move setup + 3-move trigger = 8 total. **JZP-eligible** → much cleaner finish.
2. **DR-7C8E (R' U L)**: 5-move setup + 3-move trigger = 8 total. NOT JZP, but has 4 pairs on inverse.

The **DR-4C2E with JZP** is the gold standard here. Combined with my 4-move EO, that's **4+8=12 moves to DR**, and JZP substates finish in ~5-6 moves typically. Let me commit to this path:

**Setup moves** (5): U' R' L2 U F2

I turn `U' R' L2 U F2`.

**DR trigger** (3): R U2 R'

I turn `R U2 R'`.

**DR achieved in 12 moves** (4 EO + 8 DR) with a JZP-eligible DR-4C2E substate. Now let me classify the HTR subset and finish:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (first exposure — learning).

HTR subset is **0-swap long-cycle** with cycle structure [3,2,2,1]. Total HTR+finish is **19 moves** (10 HTR reduction + 9 finish). That seems long. My current total would be **12 (to DR) + 19 (HTR+finish) = 31 moves**. Let me apply the HTR reduction and check for intermediate residuals with quick_check:

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

HTR reduction is 10 moves total, I see the first 4. Let me apply them and check state:

I turn `U F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Not yet at HTR. Let me continue HTR reduction:

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR. Let me get the final chunk of HTR reduction:

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

Great! **HTR reached at 22 moves**. Now let me apply the finish phase:

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Quick check: in HTR.

Not solved yet. Let me continue the finish:

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

Quick check: in HTR.

For the half-turn finish: `R2`.

I turn `R2`.

A quick glance — the cube is solved.

Excellent! **Cube is solved in 31 moves**. Let me cancel adjacent moves and verify the solution:

I assemble the canonical normal-frame solution: **30 moves**, verified.

Great! The cancellation reduced it from 31 to **30 moves** (U and U2 → U'). My solution is **30 moves**. Now, I should try **replace_and_shorten** since I have 30 moves (≥27) and plenty of tool calls remaining (>30). Let me target a large tail span to re-solve. I'll try the span from move 4 to the end (indices 4 to 30):

replace_and_shorten: same length, no improvement.

The replace_and_shorten found a substitute with **delta=0** (no improvement, still 31 moves after substitution). Let me try a different span. Let me target the DR-to-finish section (from move 12 onwards):

Budget check: 3477.0s sim, None tool calls remaining.

I've used 123s of simulated time and have 3477s remaining. The replace_and_shorten is capped at 1 call, and I've already used it. My current best solution is **30 moves** (after cancellation). Let me submit this solution:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified as solving the scramble in **30 moves**.

## Solution Summary

**Branch decision log:**
- **EO candidates**: UD-normal (4 moves), FB-normal (5 moves), UD-inverse (5 moves), FB-inverse (5 moves)
- **DR probe**: UD-normal reached DR in 8 moves with JZP-eligible DR-4C2E substate
- **Joint reasoning**: 4-move EO + 8-move DR = 12 moves to DR with JZP → committed to UD-normal path

**Solution breakdown:**
1. **EO (4 moves)**: R2 D' B' F' — solved 8 bad edges on UD-axis
2. **DR setup (5 moves)**: U' R' L2 U F2 — prepared for DR-4C2E trigger
3. **DR trigger (3 moves)**: R U2 R' — entered JZP-eligible DR-4C2E substate (12 moves total to DR)
4. **HTR reduction (10 moves)**: U F2 U' R2 U L2 U2 R2 F2 U — reduced corners to HTR-corner-subgroup
5. **HTR finish (9 moves)**: U2 B2 F2 L2 B2 L2 U2 B2 R2 — half-turn finish to solved
6. **Cancellation**: U + U2 → U' saved 1 move

**Final move count: 30 moves**

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "U", "F2", "U'", "R2", "U", "L2", "U2", "R2", "F2", "U'", "B2", "F2", "L2", "B2", "L2", "U2", "B2", "R2"]

**Verified solution (30 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`
