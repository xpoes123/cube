# Solve — fm_PSSSideDayGdansk2026_s3__attempt3_20260521_012556

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 33 moves
**Solution**: `R' F D L' U' F D B U D2 R2 B2 D2 F2 B2 R F2 R B2 R2 D2 R' F2 R F2 R' F' U2 F' U2 F D2 R`

---

I'll commit to the proven 14-move EO+DR path from Draft 2 (FB-EO then RL-DR), and try to optimize the finish more aggressively this time. Let me start by inspecting.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Committing the proven EO+DR path from Draft 2 (14 moves to DR-RL).

I turn `R' F D L' U' F D B U B' L' U2 L B`.

Quick check: DR-locked on RL, not yet HTR.

DR-RL at 14 moves confirmed. Let me classify HTR.

I recognize the HTR subset: **2-swap 2-cycle**. Reduction is 10 moves, finish is 12 moves (recall).

Same 22-move HTR finish as before. Let me apply chunks and watch for early residuals.

For the corner reduction, I see `D2 R D2 R'` (chunk of a 10-move phase) — apply and re-check.

I turn `D2 R D2 R'`.

For the corner reduction, I see `F2 R U2 R'` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 R U2 R'`.

For the corner reduction: `D2 R`.

I turn `D2 R`.

Quick check: in HTR.

HTR at 24. Now the 12-move finish — checking for early residuals between chunks.

For the half-turn finish, I see `B2 L2 B2 U2` (chunk of a 12-move phase) — apply and re-check.

I turn `B2 L2 B2 U2`.

Quick check: in HTR.

For the half-turn finish, I see `F2 U2 F2 L2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 L2`.

For the half-turn finish: `R2 U2 R2 U2`.

I turn `R2 U2 R2 U2`.

A quick glance — the cube is solved.

Solved at 36 raw moves — same as Draft 2. Gates pass for replace_and_shorten. Let me try a different span this time — start=9 (post-EO) to re-solve the entire DR+HTR+finish section.

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

Saved 2 moves → 34. And `R2 R'` will cancel to `R`. Let me reset, apply the substitute, then cancel.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R' F D L' U' F D B U D2 R2 B2 D2 F2 B2 R2 R' F2 R B2 R2 D2 R' F2 R F2 R' F' U2 F' U2 F D2 R`.

Auto-cancelled to 33 moves — matches Draft 2's score. Let me compose and verify.

I assemble the canonical normal-frame solution: **33 moves**, verified.

Verified 33-move solution. Same as Draft 2's best — replace_and_shorten produced an equivalent saving. Shipping.

FINAL_SOLUTION: ["R'", "F", "D", "L'", "U'", "F", "D", "B", "U", "D2", "R2", "B2", "D2", "F2", "B2", "R", "F2", "R", "B2", "R2", "D2", "R'", "F2", "R", "F2", "R'", "F'", "U2", "F'", "U2", "F", "D2", "R"]

**Verified solution (33 moves):** `R' F D L' U' F D B U D2 R2 B2 D2 F2 B2 R F2 R B2 R2 D2 R' F2 R F2 R' F' U2 F' U2 F D2 R`
