# Solve — fm_PSSSideDayGdansk2026_s1__attempt1_20260521_011536

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 39 moves
**Solution**: `R2 F2 D2 R2 B2 L2 F2 D2 R2 D2 R2 F' U2 F D2 F2 R2 F' R2 F R2 F' U' B D2 B' U' D' F' D' B U B' D2 R U D F' R'`

---

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

I see bad_edges: UD=8, FB=6, RL=6. FB and RL are tied; let me look up EO patterns on both.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

Both 5 moves on normal. Let me check inverse — same bad-edge counts but possibly shorter solutions.

NISS flip — switching to the inverse scramble.

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

All 6 candidate (side, axis) EOs are 5 moves. The differentiator is DR substate after EO. Let me return to normal and explore the FB-normal candidate first.

NISS flip — switching back to the normal scramble.

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

I turn `R'`.

EO done in 5 moves on FB. Now check DR options.

Multiple paths to DR-0C2E in 4 moves. Let me commit the first and re-query.

I turn `F2 R2 B' D`.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=4.
Last applied: `U2 R' F2 R2 B' D`.

DR-0C2E stuck at depth 4. Let me try depth 5.

5-move setup to DR-0C1E. Let me commit one and continue.

I turn `U F2 R2 B2 D`.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=2.
Last applied: `D U F2 R2 B2 D`.

Stuck at DR-0C1E (parity issue). Let me back up to the post-EO state (after 5 moves) and try a different DR direction.

I rewind 4 moves.

I rewind 4 moves.

I rewind 1 move.

Let me try a different DR setup from this EO state — the DR-2C1E option.

All depth-5 paths hit 0C2E parity. Let me commit and push through with an iterative approach — go 0C2E, then 0C1E, then continue searching.

Let me undo back to scramble and try inverse-FB EO instead (different decomposition).

I rewind 4 moves.

I rewind 1 move.

NISS flip — switching to the inverse scramble.

I turn `R F D' U'`.

On FB axis I recognize the EO pattern — `R'` fixes it.

I turn `R'`.

3-move setup to DR-2C1E on inverse-FB. Let me commit and continue.

I turn `D2 B U`.

Trying the 2C0E path which is closer to a clean trigger.

I turn `U2 B' D F D`.

5-move setup reaches DR! Let me apply it.

I turn `U B D2 B' U`.

I look over the cube.
Bad-edge counts: UD=2, FB=0, RL=0.
I'm currently working on the inverse scramble.
Last applied: `D U B D2 B' U`.

DR-FB reached in 17 moves. Let me classify HTR.

I recognize the HTR subset: **0-swap 2-cycle**. Reduction is 11 moves, finish is 11 moves (first exposure — learning).

22-move HTR finish is brutal. Let me complete this as a baseline, then try replace_and_shorten.

For the corner reduction, I see `F R2 F' R2` (chunk of a 11-move phase) — apply and re-check.

I turn `F R2 F' R2`.

For the corner reduction, I see `F R2 F2 D2` (chunk of a 7-move phase) — apply and re-check.

I turn `F R2 F2 D2`.

For the corner reduction: `F' U2 F`.

I turn `F' U2 F`.

Quick check: in HTR.

HTR reached at 28 moves. Now finish.

For the half-turn finish, I see `R2 D2 R2 D2` (chunk of a 11-move phase) — apply and re-check.

I turn `R2 D2 R2 D2`.

For the half-turn finish, I see `F2 L2 B2 R2` (chunk of a 7-move phase) — apply and re-check.

I turn `F2 L2 B2 R2`.

For the half-turn finish: `D2 F2 R2`.

I turn `D2 F2 R2`.

A quick glance — the cube is solved.

Solved at 39 moves (verified). Let me try replace_and_shorten on the long tail.

r&s: could not solve micro-scramble for span [5:39]: no DR found

39-move baseline ready. Let me compose it as fallback, then try a fresh attempt for shorter.

I assemble the canonical inverse-frame solution: **39 moves**, verified.

Fallback ready: 39 moves. Let me reset and try UD-axis EO for a potentially better path.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

UD-axis EO is only 4 moves on normal! Let me apply.

I turn `R2 D' B' F'`.

I turn `L2 U' R`.

I turn `L' D L' D' L`.

2C0E stuck at depth 5. Let me undo and try 0C2E path on UD.

I rewind 4 moves.

I rewind 1 move.

I turn `L U' L2 D L`.

Pushing to 0C1E on UD, hoping for a better HTR subset.

I turn `U' R U2 D2 L`.

My trained intuition for dr: top candidates are L (67%), U (13%), L' (7%).

I turn `L`.

Oops, L cancelled with previous L making L2, regressing the state. Let me undo.

I rewind 1 move.

I turn `L`.

I turn `U`.

Let me ship the 39-move FB-inverse fallback solve. Verifying first.

verify_solved: ✓ — 39 moves.

Shipping the 39-move solve. Time to submit.

**Solution summary:**
- EO on inverse-FB: `R F D' U' R'` (5 moves)
- DR-FB setup via 2C1E → 2C0E → DR: 12 more moves (17 total)
- HTR reduction (0-swap 2-cycle subset): 11 moves
- Finish (half-turns): 11 moves
- Total: 39 moves verified.

The DR landed in the worst HTR subset (0-swap 2-cycle, 22-move finish). I explored UD-axis as alternative but it got stuck at DR-0C1E parity and would be similar or longer. The replace_and_shorten attempt failed.

FINAL_SOLUTION: ["R2", "F2", "D2", "R2", "B2", "L2", "F2", "D2", "R2", "D2", "R2", "F'", "U2", "F", "D2", "F2", "R2", "F'", "R2", "F", "R2", "F'", "U'", "B", "D2", "B'", "U'", "D'", "F'", "D'", "B", "U", "B'", "D2", "R", "U", "D", "F'", "R'"]

**Verified solution (39 moves):** `R2 F2 D2 R2 B2 L2 F2 D2 R2 D2 R2 F' U2 F D2 F2 R2 F' R2 F R2 F' U' B D2 B' U' D' F' D' B U B' D2 R U D F' R'`
