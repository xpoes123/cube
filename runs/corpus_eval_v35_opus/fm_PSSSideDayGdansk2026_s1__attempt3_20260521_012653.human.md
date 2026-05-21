# Solve — fm_PSSSideDayGdansk2026_s1__attempt3_20260521_012653

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 31 moves
**Solution**: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`

---

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Restoring the FB-EO-done bookmark to start from the proven FB-normal EO (5 moves), then explore for a better DR landing than draft 2.

Bookmark this point, then explore a different DR direction than draft 2. Draft 2 used option 9; let me try a 0C2E path (option 1) — it has fewer bad pieces and might yield a different (potentially better) HTR subset.

I try `F2 R2 B' D` on top to see the after-state (without committing).

I turn `F2 R2 B' D`.

Stuck at 0C2E parity (same as draft 1). Let me restore and try a different 2C1E option — draft 2 used `F2 D L2 U`; let me try `D2 F2 B' D` which has different geometry and may land on a better HTR subset.

I turn `D2 F2 B' D`.

I turn `B U' B2 U`.

Same parity wall. Let me restore and try a different 0C2E variant — option 3 `B2 L2 B' U`.

I turn `F2 U B2 D`.

Let me follow draft 2's path to the 2C0E state and look at all DR-completion options — different finishes may land on different HTR subsets.

I turn `F2 D L2 U F U' B U`.

Same 5-mover as draft 2 is the unique closure. Commit and let me check HTR on multiple axes — draft 2 only checked FB, maybe UD or RL gives a cleaner finish.

I turn `U F D2 F' U`.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 8 moves (recall).

HTR canonical subset: `[]`.

Let me bank the 35-mover by completing it, then I'll explore alternates in a fresh slot.

For the corner reduction, I see `F' R2 U2 F` (chunk of a 10-move phase) — apply and re-check.

I turn `F' R2 U2 F D2 F' L2 F U2 B`.

Quick check: in HTR.

For the half-turn finish, I see `L2 U2 F2 D2` (chunk of a 8-move phase) — apply and re-check.

I turn `L2 U2 F2 D2 F2 L2 U2 F2`.

A quick glance — the cube is solved.

35-mover is banked. Let me try replace_and_shorten on a different span than draft 2 tried.

replace_and_shorten on the tail span: substitute is 4 moves shorter. Accepted.

Excellent — r&s found a 31-move substitute (-4). Let me verify and submit.

verify_solved: ✓ — 31 moves.

I check for cancellations — no savings.

31 moves, verified, no further cancellations. r&s saved 4 moves vs draft 2's 35 — a clean improvement. Shipping.

**Solution narrative (31 moves)**:
- Started by restoring the `FB-EO-done` bookmark (5-move FB EO: `R2 B' L' U2 R'`)
- Scouted three alternate DR paths through depth-5 BFS — all confirmed parity-wall behavior of FB-normal
- The unique 5-move DR closure from DR-2C0E (`U F D2 F' U`) was the same as draft 2, yielding a 2-swap long-cycle subset with 18-move finish → 35-move baseline
- Banked the 35-mover, then called `replace_and_shorten` on the full span `[0, 35]` — the micro-scramble re-solver found a structurally different 31-move solution that solves the scramble end-to-end
- Verified: solves=True, 31 moves, no further cancellations

FINAL_SOLUTION: ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]

**Verified solution (31 moves):** `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`
