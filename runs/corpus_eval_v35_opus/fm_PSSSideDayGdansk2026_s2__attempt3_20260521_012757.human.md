# Solve — fm_PSSSideDayGdansk2026_s2__attempt3_20260521_012757

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 33 moves
**Solution**: `D' F U D2 R2 U F2 L2 U F2 D2 F R2 F' U2 F2 U2 L2 F R2 F2 R2 F2 U2 B2 U2 R2 D2 U2 B U' R U2`

---

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

I'll restore the bookmark from draft 2 and try to find a better DR/HTR completion. The 33-move solve was already strong; if I can find a different DR finish that yields a cleaner HTR subset, I could potentially beat it.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `B' U2 R2 F2 L2 D`.

DR is at 2C0E. Depth-5 BFS confirms no reduction in bad pieces within 5 EO-preserving moves — same situation as draft 2. Let me explore different DR completions to see if a different HTR subset yields a shorter finish than draft 2's 11-move finish.

I try `R2 U2 D' F U2 F' D` on top to see the after-state (without committing).

I try `U2 L2 F U2 F' L2` on top to see the after-state (without committing).

I try `F U2 F' U2 R2 D2 R2` on top to see the after-state (without committing).

I try `B U2 B' U2 R2 U2 R2` on top to see the after-state (without committing).

Let me try a few more DR completions to see if any are shorter than draft 2's 7-move finisher:

I try `F R2 U F2 U' R2 F'` on top to see the after-state (without committing).

I try `L2 F U2 F' L2 U2` on top to see the after-state (without committing).

I try `R2 F U2 F' R2 U2` on top to see the after-state (without committing).

I try `D L2 F U2 F' L2 D'` on top to see the after-state (without committing).

None of the alternatives beat draft 2's 7-move DR finish. Committing to that proven path and trusting the pipeline.

I turn `R2 U2 D' F U2 F' D`.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 9 moves, finish is 11 moves (recall).

For the corner reduction, I see `F R2 F R2` (chunk of a 9-move phase) — apply and re-check.

I turn `F R2 F R2`.

For the corner reduction, I see `F' U2 F R2` (chunk of a 5-move phase) — apply and re-check.

I turn `F' U2 F R2`.

For the corner reduction: `B`.

I turn `B`.

For the half-turn finish, I see `B2 L2 F2 D2` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 L2 F2 D2`.

Auto-cancelled B + B2 → B'. Continuing the finish.

For the half-turn finish, I see `R2 D2 R2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `R2 D2 R2 U2`.

For the half-turn finish: `F2 R2 U2`.

I turn `F2 R2 U2`.

A quick glance — the cube is solved.

Solved at 35 moves. Gates pass for replace_and_shorten (≥27 moves, 122 calls left). Composing first, then applying r&s.

I assemble the canonical inverse-frame solution: **35 moves**, verified.

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

r&s saved 2 moves (35→33), matching draft 2's result. Now I need to materialize the new history into the slot. Resetting and rebuilding cleanly:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `U2 R' U B' U2 D2 R2 U2 B2 U2 F2 R2 F2 R2 F' L2 U2 F2 U2 F R2 F' D2 F2 U' L2 F2 U' R2 D2 U' F' D`.

A quick glance — the cube is solved.

Solved in 33 moves. Composing the final inverse-frame solution:

I assemble the canonical inverse-frame solution: **33 moves**, verified.

Verified 33-move solution, matching draft 2's best. r&s is already used (1-call cap). Shipping.

FINAL_SOLUTION: ["D'", "F", "U", "D2", "R2", "U", "F2", "L2", "U", "F2", "D2", "F", "R2", "F'", "U2", "F2", "U2", "L2", "F", "R2", "F2", "R2", "F2", "U2", "B2", "U2", "R2", "D2", "U2", "B", "U'", "R", "U2"]

**Verified solution (33 moves):** `D' F U D2 R2 U F2 L2 U F2 D2 F R2 F' U2 F2 U2 L2 F R2 F2 R2 F2 U2 B2 U2 R2 D2 U2 B U' R U2`
