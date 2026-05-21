# Solve — fm_PSSSideDayGdansk2026_s2__attempt2_20260521_012423

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 33 moves
**Solution**: `D' F U D2 R2 U F2 L2 U F2 D2 F R2 F' U2 F2 U2 L2 F R2 F2 R2 F2 U2 B2 U2 R2 D2 U2 B U' R U2`

---

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

I have a clear handoff: bookmark `post-EO-2C0E` is 9 moves in on inverse, at DR-2C0E on FB. Just need to close the 2-corner DR cleanly and finish HTR. Let me restore and inspect.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `B' U2 R2 F2 L2 D`.

DR-2C0E on FB - just 2 corners to orient. Let me search DR options.

All depth-5 options still show 2 bad corners — DR is >5 moves away. Let me try brain.

My trained intuition for dr: top candidates are R2 (94%), D2 (5%), F2 (0%).

I turn `R2`.

My trained intuition for dr: top candidates are U2 (99%), F2 (1%), U' (0%).

I turn `U2`.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `R2 F2 L2 D R2 U2`.

My trained intuition for dr: top candidates are U2 (99%), F2 (1%), U' (0%).

Brain is in the same loop as draft 1. Let me undo back to the bookmark state and try alternative DR sequences manually.

I rewind 2 moves.

I try `F U F' U F U2 F'` on top to see the after-state (without committing).

I try `B U B' U B U2 B'` on top to see the after-state (without committing).

I try `F U' F' U' F U2 F'` on top to see the after-state (without committing).

I try `B U' B' U' B U2 B'` on top to see the after-state (without committing).

Let me redo R2 U2 and check dr_progress_options from there (brain wasn't crazy; maybe the BFS from that state shows a path).

I turn `R2 U2`.

Brain was right — after R2 U2 the 5-move closer `D' F U2 F' D` lands at full DR. Total DR = 9+2+5 = 16 moves. Commit it.

I turn `D' F U2 F' D`.

I look over the cube.
Bad-edge counts: UD=4, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `U2 D' F U2 F' D`.

DR on FB achieved at 16 moves. Now HTR classify and finish.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 9 moves, finish is 11 moves (first exposure — learning).

20 moves HTR + finish. Total ~36. Better than 44. Let me commit phase by phase.

For the corner reduction, I see `F R2 F R2` (chunk of a 9-move phase) — apply and re-check.

I turn `F R2 F R2`.

Quick check: DR-locked on FB, not yet HTR.

For the corner reduction, I see `F' U2 F R2` (chunk of a 5-move phase) — apply and re-check.

I turn `F' U2 F R2`.

For the corner reduction: `B`.

I turn `B`.

For the half-turn finish, I see `B2 L2 F2 D2` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 L2 F2 D2`.

For the half-turn finish, I see `R2 D2 R2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `R2 D2 R2 U2`.

For the half-turn finish: `F2 R2 U2`.

I turn `F2 R2 U2`.

A quick glance — the cube is solved.

Solved at 35 moves. Compose the final solution.

I assemble the canonical inverse-frame solution: **35 moves**, verified.

35 moves verified. Gates pass (≥27, 114 calls remaining) — try replace_and_shorten on tail.

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

I look over the cube.
Bad-edge counts: UD=0, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `D2 R2 U2 F2 R2 U2`.

The tool returns the substitute but doesn't apply it. Let me verify_solved on the composed normal-frame solution directly.

verify_solved: ✓ — 33 moves.

I check for cancellations — no savings.

Solved in 33 moves, beating draft 1's 44.

FINAL_SOLUTION: ["D'", "F", "U", "D2", "R2", "U", "F2", "L2", "U", "F2", "D2", "F", "R2", "F'", "U2", "F2", "U2", "L2", "F", "R2", "F2", "R2", "F2", "U2", "B2", "U2", "R2", "D2", "U2", "B", "U'", "R", "U2"]

**Verified solution (33 moves):** `D' F U D2 R2 U F2 L2 U F2 D2 F R2 F' U2 F2 U2 L2 F R2 F2 R2 F2 U2 B2 U2 R2 D2 U2 B U' R U2`
