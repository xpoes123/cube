# Solve — fm_PSSSideDayGdansk2026_s3__attempt2_20260521_012425

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 33 moves
**Solution**: `R' F D L' U' F D B U D2 R2 B2 D2 F2 B2 R F2 R B2 R2 D2 R' F2 R F2 R' F' U2 F' U2 F D2 R`

---

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Following the proven path from draft 1: FB-EO with `R' F D L'`, then `U' F D B U` to a state where RL is also EO, then `B' L' U2 L B` for DR-RL. The previous solve got DR in 14 moves but ballooned in finish. Let me commit to that DR and focus on a clean finish.

I turn `R' F D L' U' F D B U B' L' U2 L B`.

Quick check: DR-locked on RL, not yet HTR.

DR-RL confirmed at 14 moves. Now HTR classify on RL axis.

I recognize the HTR subset: **2-swap 2-cycle**. Reduction is 10 moves, finish is 12 moves (recall).

22 more moves — that's where the prior draft died. Let me see the htr_reduction phase first and check if there's a cleaner alternative DR. Actually the instruction says commit hard — let me just push through and apply, but I'll use quick_check between chunks to spot any early residual.

For the corner reduction, I see `D2 R D2 R'` (chunk of a 10-move phase) — apply and re-check.

I turn `D2 R D2 R'`.

For the corner reduction, I see `F2 R U2 R'` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 R U2 R'`.

For the corner reduction: `D2 R`.

I turn `D2 R`.

Quick check: in HTR.

HTR at 24 moves. Now the 12-move finish.

For the half-turn finish, I see `B2 L2 B2 U2` (chunk of a 12-move phase) — apply and re-check.

I turn `B2 L2 B2 U2`.

Quick check: in HTR.

Residual class: mixed.

For the half-turn finish, I see `F2 U2 F2 L2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 L2`.

For the half-turn finish: `R2 U2 R2 U2`.

I turn `R2 U2 R2 U2`.

A quick glance — the cube is solved.

Solved at 36 moves. Gates pass for replace_and_shorten (≥27 moves, ≥30 calls remaining). Let me try it once on a large tail span.

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

Saved 2 moves. The new_history has `R2 R'` which cancels to `R'`. Let me cancel it and check.

I run cancellation: 34 → 33 moves (saved 1).

verify_solved: ✓ — 33 moves.

33 moves, verified solved. That's 3 better than the prior 36-move draft. Let me ship.

FINAL_SOLUTION: ["R'", "F", "D", "L'", "U'", "F", "D", "B", "U", "D2", "R2", "B2", "D2", "F2", "B2", "R", "F2", "R", "B2", "R2", "D2", "R'", "F2", "R", "F2", "R'", "F'", "U2", "F'", "U2", "F", "D2", "R"]

**Verified solution (33 moves):** `R' F D L' U' F D B U D2 R2 B2 D2 F2 B2 R F2 R B2 R2 D2 R' F2 R F2 R' F' U2 F' U2 F D2 R`
