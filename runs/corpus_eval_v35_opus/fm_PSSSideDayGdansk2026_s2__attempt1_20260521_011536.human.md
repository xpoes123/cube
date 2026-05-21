# Solve — fm_PSSSideDayGdansk2026_s2__attempt1_20260521_011536

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 44 moves
**Solution**: `U2 R2 F2 U2 L2 F2 U2 B2 U2 L2 F2 D' F2 U2 R2 U' F2 U2 R2 U' B2 L' D2 F2 U2 B2 R' D' U' B R2 F2 D' L2 R2 U' F D' F' R2 D U2 R U2`

---

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both axes have 4-move EOs. Let me also check inverse-side for these to find the cleanest joint EO+DR.

NISS flip — switching to the inverse scramble.

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

Excellent — inverse-FB has a **2-move EO** (U2 R'). That dominates. Committing.

I turn `U2 R'`.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=4.
I'm currently working on the inverse scramble.
Last applied: `U2 R'`.

EO complete (FB axis solved). DR-FB shows 5C2E — let me search DR options.

Going with `U B' U` (3 moves) to DR-2C1E, then re-query for the final approach.

I turn `U B' U`.

Depth 4 doesn't reduce. Try depth 5.

The 5-mv options start with `U` which cancel-merges with my trailing `U` (saves 1 move). Picking `U R2 F2 L2 D` → lands at DR-2C0E.

I turn `U R2 F2 L2 D`.

My trained intuition for dr: top candidates are R2 (94%), D2 (5%), F2 (0%).

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `B' U2 R2 F2 L2 D`.

Brain strongly suggests `R2`. Apply and check.

I try `R2` on top to see the after-state (without committing).

I turn `R2`.

My trained intuition for dr: top candidates are U2 (99%), F2 (1%), U' (0%).

I turn `U2`.

My trained intuition for dr: top candidates are U2 (99%), F2 (1%), U' (0%).

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `R2 F2 L2 D R2 U2`.

I try `R U2 R'` on top to see the after-state (without committing).

I try `F2 R U2 R' F2` on top to see the after-state (without committing).

Brain looping on U2 — that's a stuck signal. Let me undo the R2 U2 and try a different DR setup direction.

I rewind 2 moves.

I look 4 moves ahead with a small beam.

Let me back up further to the 2C1E state and try alternate DR setups.

I rewind 4 moves.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=4.
I'm currently working on the inverse scramble.
Last applied: `U2 R' U B' U2`.

I rewind 1 move.

I turn `U`.

Let me back up to the pure post-EO state and search DR at depth 5 directly (skip the 2C1E intermediate).

I rewind 3 moves.

Excellent — depth-5 finds `U2 D' R2 F D` (5 moves) landing at **DR-0C2E** (only 2 slice edges off, no corner twists). Much better than the 2C0E branch. Committing.

I turn `U2 D' R2 F D`.

My trained intuition for dr: top candidates are R (14%), L (11%), D2 (10%).

Top option "F' U R2 L2 D" lands at 0C1E. Let me commit and continue.

I turn `F' U R2 L2 D`.

I look over the cube.
Bad-edge counts: UD=4, FB=0, RL=2.
I'm currently working on the inverse scramble.
Last applied: `D F' U R2 L2 D`.

I try `F R L F'` on top to see the after-state (without committing).

I try `B R L B'` on top to see the after-state (without committing).

I try `F2 R L F2` on top to see the after-state (without committing).

Let me try NISS flipping — the current 0C1E might resolve cleanly on the other side.

NISS flip — switching back to the normal scramble.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.
Last applied: `D F' U R2 L2 D`.

NISS flip — switching to the inverse scramble.

I try `U R2 U' L2` on top to see the after-state (without committing).

I try `D L2 D' R2` on top to see the after-state (without committing).

I try `U2 R2 D2 L2` on top to see the after-state (without committing).

Switching strategy — UD has 4 bad edges and is only 2C2E for DR. Cheaper to do UD-EO + UD-DR than continue FB. Let me lookup UD EO.

On UD axis I recognize the EO pattern — `F2 R2 B'` fixes it.

On RL axis I recognize the EO pattern — `D F' D'` fixes it.

I try `F2 R2 B'` on top to see the after-state (without committing).

I try `D F' D'` on top to see the after-state (without committing).

Path A (`F2 R2 B'`) is brilliant — solves UD-EO without breaking FB-EO, leaving us at **UD-axis 4C0E** (4 unoriented corners, 0 slice edges off — essentially JZP-ready). Apply it.

I turn `F2 R2 B'`.

I try `R F2 R'` on top to see the after-state (without committing).

I try `L F2 L'` on top to see the after-state (without committing).

I try `R U2 L F2 L' U2 R'` on top to see the after-state (without committing).

Let me commit the 5-move setup `U D R B2 R` → 0C1E and continue.

I turn `U D R B2 R`.

🎯 **DR FOUND!** `R' U2 F2 D2 L` reaches DR. And since my last move was `R`, the leading `R'` cancels — saving 1 move (net 4 moves to DR).

I turn `R' U2 F2 D2 L`.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 11 moves (first exposure — learning).

HTR is 21 moves — total ~44. Too long. Let me check the other axes' HTR subset to see if any is cheaper.

HTR classify: could not compute HTR phases for this subset.

HTR classify: could not compute HTR phases for this subset.

UD is our only DR axis. Apply HTR reduction.

For the corner reduction, I see `B2 U R2 U2` (chunk of a 10-move phase) — apply and re-check.

I turn `B2 U R2 U2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction, I see `F2 U R2 U2` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 U R2 U2`.

For the corner reduction: `F2 D`.

I turn `F2 D`.

Quick check: in HTR.

HTR reached. Apply finish phase.

For the half-turn finish, I see `F2 L2 U2 B2` (chunk of a 11-move phase) — apply and re-check.

I turn `F2 L2 U2 B2`.

Quick check: in HTR.

For the half-turn finish, I see `U2 F2 L2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `U2 F2 L2 U2`.

For the half-turn finish: `F2 R2 U2`.

I turn `F2 R2 U2`.

A quick glance — the cube is solved.

Solved at 44 moves on inverse — way too long. Let me try replace_and_shorten on the lumpy DR setup span.

I assemble the canonical inverse-frame solution: **44 moves**, verified.

r&s: could not solve micro-scramble for span [4:44]: no DR found

R&S failed (1-call cap used). 44 moves it is — within the 50-move acceptability threshold. Verify and ship.

verify_solved: ✓ — 44 moves.

Verified. The solve narrative:
- **EO** (2 mv, inverse-FB): `U2 R'`
- **DR setup** (5 mv, lumpy because the 2C0E branch was sticky): `U2 D' R2 F D`
- **More DR setup** (5 mv to 0C1E): `F' U R2 L2 D`
- **Pivot to UD-axis** (3 mv solving UD-EO without breaking FB-EO): `F2 R2 B'`
- **UD-DR reach** (8 mv after cancellation): `U D R B2 U2 F2 D2 L`
- **HTR reduction** (10 mv) + **finish** (11 mv): half-turn slabs

44 moves is long — the DR phase was inefficient because the 0C1E "1 misplaced slice edge" substate doesn't reduce within the depth-5 BFS horizon. A cleaner DR path would have saved 8–10 moves but the search-and-commit loop committed before I saw the trap.

FINAL_SOLUTION: ["U2", "R2", "F2", "U2", "L2", "F2", "U2", "B2", "U2", "L2", "F2", "D'", "F2", "U2", "R2", "U'", "F2", "U2", "R2", "U'", "B2", "L'", "D2", "F2", "U2", "B2", "R'", "D'", "U'", "B", "R2", "F2", "D'", "L2", "R2", "U'", "F", "D'", "F'", "R2", "D", "U2", "R", "U2"]

**Verified solution (44 moves):** `U2 R2 F2 U2 L2 F2 U2 B2 U2 L2 F2 D' F2 U2 R2 U' F2 U2 R2 U' B2 L' D2 F2 U2 B2 R' D' U' B R2 F2 D' L2 R2 U' F D' F' R2 D U2 R U2`
