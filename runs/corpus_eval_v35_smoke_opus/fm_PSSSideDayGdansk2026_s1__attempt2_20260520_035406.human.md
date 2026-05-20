# Solve — fm_PSSSideDayGdansk2026_s1__attempt2_20260520_035406

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 31 moves
**Solution**: `R2 D' B' F U2 R2 U2 L2 U2 R2 F2 R2 B2 U R2 U L2 U' F2 R2 U' L2 U' R U R' L' D R D L'`

---

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Prior draft used UD-normal EO with `R2 D' B' F'` (4 moves), then found DR in 13 moves (long), HTR+finish another 14 moves. Same axis is fine — I'll commit the EO and search the DR more carefully this time.

I turn `R2 D' B' F'`.

Same starting options as prior — best is `L2 U' R` to DR-2C1E. Let me commit and probe deeper.

I turn `L2 U' R`.

Prior draft hit a parity trap at 0C1E. Let me try the 2C0E path — 2 corners 0 edges is structurally different (maybe a clean R U2 R' / R U R' trigger lands DR).

I try `L' D L' D' L` on top to see the after-state (without committing).

DR-2C0E **JZP-eligible** — much cleaner than prior draft's path. Commit and search.

I turn `L' D L' D' L`.

Need deeper search — 2C0E requires a quarter-turn trigger.

JZP-eligible 2C0E but no 5-move trigger via EO-preserving moves. Let me ask the brain for DR moves directly.

My trained intuition for dr: top candidates are F2 (36%), D (28%), L2 (27%).

I try `F2 D L2 D'` on top to see the after-state (without committing).

The 2C0E path isn't converging. Let me undo and try a different branch — the `L U' R2 U L'` variant which goes to 0C1E (untested by prior).

I rewind 4 moves.

I rewind 1 move.

I rewind 3 moves.

I turn `L2 U' R'`.

Let me just take prior draft's known DR path to focus tool budget on HTR/finish optimization.

I rewind 3 moves.

I turn `L2 U' R F2 L F2 U R2 U2 F2 D2 L`.

I look over the cube.
Bad-edge counts: UD=0, FB=8, RL=4.
Last applied: `U R2 U2 F2 D2 L`.

I misread prior draft — it actually skipped the `L2 U' R` step and went `F2 L F2 U R` directly (with F' F2→F cancel), then `R U2 F2 D2 L` TWICE. Let me redo.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 D' B' F' F2 L F2 U R R U2 F2 D2 L R U2 F2 D2 L`.

I look over the cube.
Bad-edge counts: UD=0, FB=0, RL=2.
Last applied: `L R U2 F2 D2 L`.

DR-UD at 17 moves, qt_corners=4. Now classify HTR.

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 9 moves, finish is 10 moves (recall).

Same subset as prior (19mv finish). Let me run the HTR pipeline and ship a verified solve, then try replace_and_shorten on the tail.

For the corner reduction, I see `B2 U L2 F2` (chunk of a 9-move phase) — apply and re-check.

I turn `B2 U L2 F2`.

For the corner reduction, I see `U L2 U' B2` (chunk of a 5-move phase) — apply and re-check.

I turn `U L2 U' B2`.

For the corner reduction: `D`.

I turn `D`.

Quick check: in HTR.

HTR at 26 moves. Apply finish.

For the half-turn finish, I see `D2 F2 D2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `D2 F2 D2 R2`.

For the half-turn finish, I see `D2 F2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F2 U2 R2`.

For the half-turn finish: `F2 L2`.

I turn `F2 L2`.

A quick glance — the cube is solved.

Solved at 35 moves — worse than prior's 31. Mandatory r&s, gates pass (35≥27, 113 calls).

replace_and_shorten on the tail span: substitute is 3 moves shorter. Accepted.

r&s saved 3 moves → 32. There's a `U2 U'` adjacent — should cancel to 31. Let me run cancel.

I run cancellation: 32 → 31 moves (saved 1).

31 moves — matches prior exactly. Verify and ship.

verify_solved: ✓ — 31 moves.

Verified 31 moves. Matches the prior draft best — a clean DR-UD path through 2-swap mostly-axial HTR subset.

FINAL_SOLUTION: ["R2", "D'", "B'", "F", "U2", "R2", "U2", "L2", "U2", "R2", "F2", "R2", "B2", "U", "R2", "U", "L2", "U'", "F2", "R2", "U'", "L2", "U'", "R", "U", "R'", "L'", "D", "R", "D", "L'"]

**Verified solution (31 moves):** `R2 D' B' F U2 R2 U2 L2 U2 R2 F2 R2 B2 U R2 U L2 U' F2 R2 U' L2 U' R U R' L' D R D L'`
