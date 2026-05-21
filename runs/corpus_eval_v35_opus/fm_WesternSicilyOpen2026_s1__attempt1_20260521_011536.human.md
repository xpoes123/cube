# Solve — fm_WesternSicilyOpen2026_s1__attempt1_20260521_011536

**Scramble**: `R' U' F U2 F2 D2 B2 D B' U L' B' F2 R2 U' L2 F2 B2 D' F2 L2 F R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 34 moves
**Solution**: `R2 F2 U2 B2 U2 B2 R2 F2 U2 R2 U2 L' F2 U2 R2 D2 R U2 R U2 B' D2 R2 U2 F' B' L' F2 L U2 L' U2 D R2`

---

I look over the cube.
Bad-edge counts: UD=4, FB=6, RL=4.

EO scouting: UD=4 bad, FB=6 bad, RL=4 bad. UD and RL are the two cheap-EO candidates. Let me check eo_pattern_lookup on both.

On UD axis I recognize the EO pattern — `D R U2 F'` fixes it.

On RL axis I recognize the EO pattern — `U2 F2 R D'` fixes it.

Both 4-move EOs. Let me probe DR cost for each by try_alg'ing the EO then peeking at dr_progress_options. Also check inverse for FB.

I try `D R U2 F'` on top to see the after-state (without committing).

I try `U2 F2 R D'` on top to see the after-state (without committing).

UD-EO lands at DR-4C2E with FB-axis also showing 3C2E (interesting cross-axis structure). RL-EO lands at DR-4C2E too. Comparable. Let me commit UD-EO and probe DR.

I turn `D R U2 F'`.

No trigger lands within 4 moves. Best is 2C1E in 4 moves. Let me probe a couple of these candidates to see which has a near DR.

I try `U2 R U R'` on top to see the after-state (without committing).

I try `U' F2 R` on top to see the after-state (without committing).

Going with U2 R U R' → 2C1E. Commit and re-query.

I turn `U2 R U R'`.

2C0E in 4 moves available. Let me try if known 2C triggers hit DR directly from the current 2C1E state first.

I try `R U2 R'` on top to see the after-state (without committing).

I try `R U R'` on top to see the after-state (without committing).

I try `R U' R'` on top to see the after-state (without committing).

Commit D2 L' U' L → 2C0E.

I turn `D2 L' U' L`.

Depth 4 doesn't reach DR. Let me look depth 5.

Depth 5 still can't fix 2C0E — these corners need a longer EO-preserving alg. Let me consult brain.

My trained intuition for dr: top candidates are U' (63%), D (23%), D' (11%).

I turn `U'`.

My trained intuition for dr: top candidates are R' (89%), R2 (6%), F2 (3%).

I turn `R'`.

My trained intuition for dr: top candidates are R' (48%), R (28%), F2 (15%).

I look over the cube.
Bad-edge counts: UD=0, FB=4, RL=4.
Last applied: `D2 L' U' L U' R'`.

That broke things — went from 2C0E to 5C2E. Let me undo and try a different tack.

I rewind 2 moves.

Trusting the brain may need a longer 2-twist alg. Let me brain-walk a few more moves but watch closely.

I turn `U' R'`.

My trained intuition for dr: top candidates are R' (48%), R (28%), F2 (15%).

I turn `R'`.

I look over the cube.
Bad-edge counts: UD=0, FB=0, RL=4.
Last applied: `D2 L' U' L U' R2`.

Now UD is at 2C0E and FB is also EO-solved! Brain-walk one more.

My trained intuition for dr: top candidates are D (92%), D' (6%), R2 (1%).

I turn `D`.

My trained intuition for dr: top candidates are D' (68%), D (30%), B2 (1%).

I look over the cube.
Bad-edge counts: UD=0, FB=0, RL=2.
Last applied: `L' U' L U' R2 D`.

Both DRs stuck at 2-twist. Let me try NISS to see what the inverse state looks like.

NISS flip — switching to the inverse scramble.

I look over the cube.
Bad-edge counts: UD=4, FB=6, RL=6.
I'm currently working on the inverse scramble.
Last applied: `L' U' L U' R2 D`.

On UD axis I recognize the EO pattern — `D2 L R F'` fixes it.

NISS flip — switching back to the normal scramble.

I look 4 moves ahead with a small beam.

Let me try brain again from current state — might be a longer alg.

My trained intuition for dr: top candidates are D' (68%), D (30%), B2 (1%).

I turn `D'`.

Let me try some known 2-twist DR-preserving algs.

I try `R2 U2 R' F2 R U2 R' F2 R'` on top to see the after-state (without committing).

I try `R U2 R' F2 R U2 R' F2` on top to see the after-state (without committing).

I try `F2 R U2 R' F2 L' U2 L` on top to see the after-state (without committing).

Stuck in a 2C0E well that needs 7+ extra moves. Let me reset and try a different DR path. Budget is ample.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Fresh start. Let me try inverse-side EO this time — the inverse perspective showed potentially better DR substates.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `L' F'` fixes it.

On RL axis I recognize the EO pattern — `R2 D'` fixes it.

2-move EOs on inverse! Big improvement. Let me try both candidates.

I try `L' F'` on top to see the after-state (without committing).

I try `R2 D'` on top to see the after-state (without committing).

R2 D' lands at DR-4C2E on RL — clean trigger family. Committing.

I turn `R2 D'`.

I try `U R2 U2 R2` on top to see the after-state (without committing).

I try `U2 L U2 B` on top to see the after-state (without committing).

I turn `U2 L U2 B`.

5-move setup to 0C1E — excellent! Just 1 slice edge off. Commit and re-query.

I turn `B' L' F2 L B`.

DR in 5 more moves! Total DR = 14 inverse-moves. Committing.

I turn `F U2 R2 D2 B`.

Quick check: DR-locked on RL, not yet HTR.

DR on RL! Time for HTR.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 9 moves, finish is 11 moves (first exposure — learning).

20-move finish is rough. Let me start applying and check for early shortcuts.

For the corner reduction, I see `U2 R' U2 R'` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 R' U2 R'`.

For the corner reduction, I see `D2 R2 U2 F2` (chunk of a 5-move phase) — apply and re-check.

I turn `D2 R2 U2 F2`.

For the corner reduction: `L`.

I turn `L`.

Quick check: in HTR.

At HTR. Let me check for a 3-cycle residual before running finish.

Residual class: mixed.

Just run the finish.

For the half-turn finish, I see `U2 R2 U2 F2` (chunk of a 11-move phase) — apply and re-check.

I turn `U2 R2 U2 F2`.

For the half-turn finish, I see `R2 B2 U2 B2` (chunk of a 7-move phase) — apply and re-check.

I turn `R2 B2 U2 B2`.

For the half-turn finish: `U2 F2 R2`.

I turn `U2 F2 R2`.

A quick glance — the cube is solved.

Solved at 34 moves. Compose and verify.

I assemble the canonical inverse-frame solution: **34 moves**, verified.

Gates pass for replace_and_shorten. Running on the large tail.

r&s: could not solve micro-scramble for span [4:34]: no DR found

R&S failed and cap hit. Submitting 34-move solution.

verify_solved: ✓ — 34 moves.

Verified 34-move solve. Shipping.

**Summary of the solve**:
- Started normal-side, hit a 2C0E stuck position (UD-DR-2-twist with no slice off, hard to escape in ≤5 EO-preserving moves). Reset.
- Switched to **inverse-side**, found 2-move RL-EO: `R2 D'` (vs 4-move normal).
- DR built incrementally: 4-move setup `U2 L U2 B` → 2C1E, then 5-move `B' L' F2 L B` → 0C1E (with 2 cancellations), then 5-move `F U2 R2 D2 B` → DR (RL-axis, 14 moves total).
- HTR-classify: "2-swap long-cycle" subset — heavy 20-move finish (9 reduction + 11 finish), no clean 3-cycle for insertion.
- `replace_and_shorten` micro-scramble timed out finding DR on the tail — accepted 34 as final.

FINAL_SOLUTION: ["R2", "F2", "U2", "B2", "U2", "B2", "R2", "F2", "U2", "R2", "U2", "L'", "F2", "U2", "R2", "D2", "R", "U2", "R", "U2", "B'", "D2", "R2", "U2", "F'", "B'", "L'", "F2", "L", "U2", "L'", "U2", "D", "R2"]

**Verified solution (34 moves):** `R2 F2 U2 B2 U2 B2 R2 F2 U2 R2 U2 L' F2 U2 R2 D2 R U2 R U2 B' D2 R2 U2 F' B' L' F2 L U2 L' U2 D R2`
