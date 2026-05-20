# Solve — fm_PSSSideDayGdansk2026_s1__attempt3_20260520_040110

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 31 moves
**Solution**: `R2 D' B' F U2 R2 U2 L2 U2 R2 F2 R2 B2 U R2 U L2 U' F2 R2 U' L2 U' R U R' L' D R D L'`

---

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Two prior drafts converged on UD-normal with 31 moves. Let me see if FB axis (lower bad-corner+edge count: 5C2E vs UD's 6C3E) gives a shorter path. I'll scout EO on FB first.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

UD wins (4 vs 5). Same EO as priors. Now my plan: commit UD EO, then push for a DIFFERENT DR landing — prior 2-swap-mostly-axial subset gives 19mv finish. Let me look for paths that don't end in that subset.

I turn `R2 D' B' F'`.

Same options the priors saw. Let me commit `F2 L F2 U R` (with auto-cancel F'+F2→F saves a move), then search depth-5 from there for the cheapest completion to DR.

I turn `F2 L F2 U R`.

Same starting position as prior. Prior used `R U2 F2 D2 L` twice (landing in 2-swap mostly-axial → 19mv finish). Let me try the `R U2 B2 U2 R` branch instead — might land in a different (cheaper) HTR subset. Bookmark current state first.

I turn `R U2 B2 U2 R`.

Auto-cancel saved 1 (R+R→R2). Now at 12 moves. Let me see how close to DR.

Excellent — `R F2 U2 F2 R` lands at full DR in 5 moves, and last R + first R cancel → save 1 more! Apply.

I turn `R F2 U2 F2 R`.

DR at 16 moves (saved 1 vs prior's 17). Now classify HTR subset.

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 9 moves, finish is 10 moves (recall).

Same subset, but with 16 DR (not 17) and 19 finish → 35 raw, expect ~30 after cancels. Apply HTR.

For the corner reduction, I see `B2 U L2 F2` (chunk of a 9-move phase) — apply and re-check.

I turn `B2 U L2 F2`.

For the corner reduction, I see `U L2 U' B2` (chunk of a 5-move phase) — apply and re-check.

I turn `U L2 U' B2`.

For the corner reduction: `D`.

I turn `D`.

For the half-turn finish, I see `D2 F2 D2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `D2 F2 D2 R2`.

Auto-cancel saved 1 (D+D2→D'). At 28. Continue finish.

For the half-turn finish, I see `D2 F2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F2 U2 R2`.

For the half-turn finish: `F2 L2`.

I turn `F2 L2`.

A quick glance — the cube is solved.

Solved at 34 raw moves (vs prior's 35). Gates pass for r&s (34≥27, 125 calls). Let me run cancel first to see the clean count.

I check for cancellations — no savings.

34 clean. r&s on the tail:

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

r&s saved 2: 34→32. There's `U2 U'` which should cancel to `U`. Let me apply this history and cancel.

I run cancellation: 32 → 31 moves (saved 1).

31 moves — identical to prior drafts. The path converges. Verify and ship.

verify_solved: ✓ — 31 moves.

Verified 31 moves — matches the prior drafts' converged solution. The DR-UD path through the 2-swap mostly-axial subset is locked in.

FINAL_SOLUTION: ["R2", "D'", "B'", "F", "U2", "R2", "U2", "L2", "U2", "R2", "F2", "R2", "B2", "U", "R2", "U", "L2", "U'", "F2", "R2", "U'", "L2", "U'", "R", "U", "R'", "L'", "D", "R", "D", "L'"]

**Verified solution (31 moves):** `R2 D' B' F U2 R2 U2 L2 U2 R2 F2 R2 B2 U R2 U L2 U' F2 R2 U' L2 U' R U R' L' D R D L'`
