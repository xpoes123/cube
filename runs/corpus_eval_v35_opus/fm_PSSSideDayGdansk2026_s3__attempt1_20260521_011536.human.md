# Solve — fm_PSSSideDayGdansk2026_s3__attempt1_20260521_011536

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 36 moves
**Solution**: `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2`

---

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

UD has 4 bad edges (lowest count). FB has 8, RL has 6. Let me look up EO patterns on UD.

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

4-move EO on UD-normal. Let me NISS-check the inverse, then probe DR options.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

Both sides have 4-move UD-EO. Let me commit UD-normal EO and probe DR.

NISS flip — switching back to the normal scramble.

I turn `U L R' B'`.

Let me also probe DR on FB and RL axes from this same post-EO state, since EO-preserving moves on UD only excludes F/B quarters — but a different axis might reach DR faster.

Right, UD-EO only enables UD-axis DR. Let me commit the first setup `U R D2 L` and re-query.

I turn `U R D2 L`.

Down to 2C1E in 3 more moves. Let me commit `B2 U' R` and look one more time.

I turn `B2 U' R`.

Stuck at 2C1E at depth 4. Let me try depth 5 to see if DR is reachable.

Picks `R2 B2 R U2 R'` → DR-2C0E (only 2 misoriented corners left). Let me commit.

I turn `R2 B2 R U2 R'`.

Let me commit `R F2 R F2 R'` → 0C1E and continue.

I turn `R F2 R F2 R'`.

Cancelled 2 moves — now at 18. Let me check DR options.

I look over the cube.
Bad-edge counts: UD=0, FB=2, RL=4.
Last applied: `R U2 F2 R F2 R'`.

My trained intuition for dr: top candidates are L' (53%), L (36%), B2 (7%).

I try `L'` on top to see the after-state (without committing).

Let me bookmark and try inverse side — DR-0C1E with odd parity is awkward.

NISS flip — switching to the inverse scramble.

I look over the cube.
Bad-edge counts: UD=4, FB=6, RL=6.
I'm currently working on the inverse scramble.
Last applied: `R U2 F2 R F2 R'`.

On UD axis I recognize the EO pattern — the first chunk is `U' R' D2 U'` (full fix is 4 moves).

NISS on inverse needs another EO. Let me revert and continue on normal — push through the awkward 0C1E.

NISS flip — switching back to the normal scramble.

Brain top is L' — let me commit and see if subsequent depth-4 finds DR.

I turn `L'`.

I rewind 1 move.

Let me commit L and search deeper — L stays at 0C1E count-wise but moves to a different position in that class.

I turn `L`.

The 0C1E path will need ≥6 more moves. Let me restore and try a different axis instead. Reset and try FB.

I turn `R2 L D2`.

This branch is deeply stuck on parity. Let me restore and instead undo to right after EO, then try a different DR setup.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me start on inverse this time — the EO was also 4 moves and DR substate might be different.

NISS flip — switching to the inverse scramble.

I turn `B' R' U B'`.

Inverse looks more tractable — 2C1E in 4. Committing `R' U D2 R`.

I turn `R' U D2 R`.

Committing `U2 D' L U L'` (5 moves) → DR-2C0E.

I turn `U2 D' L U L'`.

The 2C0E/0C1E parity is fundamental to this scramble's UD axis. Let me reset and try FB-axis EO from the start.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

I turn `R' F D L'`.

5 moves to 3C0E or 0C3E. Let me try the 3C0E path — committing `U' F D B U`.

I turn `U' F D B U`.

My trained intuition for dr: top candidates are D2 (62%), D' (13%), F2 (7%).

I try `D2` on top to see the after-state (without committing).

Both FB AND RL are EO-solved! Let me explore RL DR.

5-move DR-solved on RL axis! Total 14 moves to DR.

I turn `B' L' U2 L B`.

Quick check: DR-locked on RL, not yet HTR.

DR on RL achieved! Now HTR classify.

I recognize the HTR subset: **2-swap 2-cycle**. Reduction is 10 moves, finish is 12 moves (first exposure — learning).

22 move HTR finish — long. Let me apply HTR reduction and see.

For the corner reduction, I see `D2 R D2 R'` (chunk of a 10-move phase) — apply and re-check.

I turn `D2 R D2 R'`.

For the corner reduction, I see `F2 R U2 R'` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 R U2 R'`.

For the corner reduction: `D2 R`.

I turn `D2 R`.

Quick check: in HTR.

HTR reached at 24 moves. Now finish.

For the half-turn finish, I see `B2 L2 B2 U2` (chunk of a 12-move phase) — apply and re-check.

I turn `B2 L2 B2 U2`.

For the half-turn finish, I see `F2 U2 F2 L2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 L2`.

For the half-turn finish: `R2 U2 R2 U2`.

I turn `R2 U2 R2 U2`.

A quick glance — the cube is solved.

Solved at 36 moves. Gates pass for replace_and_shorten. Let me run it on a large tail.

r&s: could not solve micro-scramble for span [4:36]: no DR found

R&S used and failed. Let me submit the 36-move solve.

I assemble the canonical normal-frame solution: **36 moves**, verified.

Solution verified at 36 moves. Submitting.

FINAL_SOLUTION: ["R'", "F", "D", "L'", "U'", "F", "D", "B", "U", "B'", "L'", "U2", "L", "B", "D2", "R", "D2", "R'", "F2", "R", "U2", "R'", "D2", "R", "B2", "L2", "B2", "U2", "F2", "U2", "F2", "L2", "R2", "U2", "R2", "U2"]

**Verified solution (36 moves):** `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2`
