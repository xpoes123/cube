# Solve — fm_PSSSideDayGdansk2026_s1__attempt2_20260521_012444

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: SOLVED in 35 moves
**Solution**: `R2 B' L' U2 R' F2 D L2 U F U' B U2 F D2 F' U F' R2 U2 F D2 F' L2 F U2 B L2 U2 F2 D2 F2 L2 U2 F2`

---

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Prior draft 1 was 39 moves on FB-inverse with a brutal 0-swap-2c HTR subset (22-move finish). The bookmark `FB-EO-done` is at FB-normal post-EO (5mv) — the draft abandoned it as "parity-tough", but didn't deeply explore. Let me try harder on FB-normal first; if a clean DR substate exists there, the HTR finish could be much shorter.

Top options at depth 4: four DR-0C2E in 4 moves, six DR-2C1E in 4 moves. Prior draft tried `F2 R2 B' D` (0C2E) and got stuck in parity at depth 5. Let me try a 2C1E setup instead — different residual shape that may close cleanly.

I turn `F2 D L2 U`.

Apply F U' B U → DR-2C0E, then re-query for the close.

I turn `F U' B U`.

Depth 4 from 2C0E shows no progress — need depth 5 to crack it.

`U F D2 F' U` lands me at full DR in 5 moves. Total: 13+5 = 18 moves to DR. The previous attempt was 17 on inverse, but the HTR finish was 22 moves — the SUBSET matters more than the DR move count. Let me commit and check.

I turn `U F D2 F' U`.

Auto-cancelled `U U` → `U2`, dropping to 17 moves at DR (matches prior). Now classify HTR.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 8 moves (first exposure — learning).

2-swap long-cycle: 10+8=18 from DR. Total before cancellations: 17+18 = 35. Better than 39. Apply.

For the corner reduction, I see `F' R2 U2 F` (chunk of a 10-move phase) — apply and re-check.

I turn `F' R2 U2 F`.

For the corner reduction, I see `D2 F' L2 F` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F' L2 F`.

For the corner reduction: `U2 B`.

I turn `U2 B`.

Quick check: in HTR.

In HTR at 27 moves. Apply finish.

For the half-turn finish, I see `L2 U2 F2 D2` (chunk of a 8-move phase) — apply and re-check.

I turn `L2 U2 F2 D2`.

For the half-turn finish: `F2 L2 U2 F2`.

I turn `F2 L2 U2 F2`.

A quick glance — the cube is solved.

Solved in 35 moves — 4 moves better than draft 1. Gates for r&s pass (35≥27, calls=127≥30, not called yet). Try a large tail span.

r&s: could not solve micro-scramble for span [5:35]: no DR found

r&s burned. Compose and submit the 35.

I assemble the canonical normal-frame solution: **35 moves**, verified.

Solved cleanly in 35 moves — a 4-move improvement over draft 1 (39).

**Solution narrative**:
- **EO-FB** (5 moves): `R2 B' L' U2 R'` — same as bookmark
- **DR-FB setup** (12 moves with 1 auto-cancel): `F2 D L2 U` → DR-2C1E, `F U' B U2` → DR-2C0E, `F D2 F' U` → DR
- **HTR reduction** (10 moves): `F' R2 U2 F D2 F' L2 F U2 B` — 2-swap long-cycle subset
- **Finish** (8 moves): `L2 U2 F2 D2 F2 L2 U2 F2`

Key insight vs draft 1: instead of NISS-flipping to inverse-FB and landing on a 0-swap 2-cycle (22-move finish), I pushed FB-normal through the DR-2C1E → DR-2C0E → DR path, which landed me on a 2-swap long-cycle subset with only an 18-move finish from DR.

FINAL_SOLUTION: ["R2", "B'", "L'", "U2", "R'", "F2", "D", "L2", "U", "F", "U'", "B", "U2", "F", "D2", "F'", "U", "F'", "R2", "U2", "F", "D2", "F'", "L2", "F", "U2", "B", "L2", "U2", "F2", "D2", "F2", "L2", "U2", "F2"]

**Verified solution (35 moves):** `R2 B' L' U2 R' F2 D L2 U F U' B U2 F D2 F' U F' R2 U2 F D2 F' L2 F U2 B L2 U2 F2 D2 F2 L2 U2 F2`
