# Solve — fm_PSSSideDayGdansk2026_s2__attempt7_20260517_165507

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `R2 B F2 U' R B' D2 R' B' F' L B' U2 F2 R2 F2 U2 B2 R2 F2 R D2 R' B2 U2 R2 D2 R' U2 R' F2`

---

*Thinking (1):*

> Looking at the prior attempts, all seem to cluster around 31-34 moves. The best is 31 moves, achieved multiple times with the same solution. Let me start by inspecting the state to understand what axes are available.
> 
> The instructions are clear: COMMIT HARD this attempt. Pick a line and drive it to completion. Don't overthink between branches. The goal is a complete, clean solution.
> 
> Let me start with inspect_state to see the initial state analysis.

I'll solve this scramble by first inspecting the state, then committing hard to a single promising line based on the prior attempts' patterns. Let me begin.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**ANALYSIS:**
- Bad edges per axis: UD=6, FB=4, RL=4
- FB and RL both have 4 bad edges, which is typically a 1-3 move EO range
- UD has 3 pairs on inverse (strong NISS signal!)
- FB has DR-7C2E (awkward), RL has DR-6C2E (less awkward)

The prior 31-move solutions all start with `R2 B F2 U'...`, which suggests they found a good line on one axis. Let me scout **FB-axis EO first** on the normal side (4 bad edges), then check inverse.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

FB-axis normal side: 4 moves. Now let me check RL-axis normal side (also 4 bad edges):

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

**RL-axis EO is `R2 B F2 U'`** — this matches the first 4 moves of ALL prior attempts! This is the successful line. Now let me flip to inverse and check if there's a shorter EO option before committing.

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check RL-axis EO on inverse (bad-edge count is identical per NISS invariant):

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

Inverse RL-EO is 5 moves (partial 4+). Let me also check FB inverse quickly:

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

**DECISION POINT:**
- Normal RL: 4-move EO (`R2 B F2 U'`)
- Inverse FB: **2-move EO** (`U2 R'`)
- Normal FB: 4-move EO
- Inverse RL: 5-move EO

The inverse FB EO is 2 moves shorter! But all prior attempts used normal RL. Let me check DR options for BOTH before committing:

**Path A (normal RL, 4-move EO):** This is what worked before for 31 moves.
**Path B (inverse FB, 2-move EO):** Potentially better if DR is clean.

Let me flip back to normal and commit the RL EO, then check DR options:

NISS flip — switching back to the normal scramble.

Back on normal. **COMMITTING to normal RL-axis** (the proven 31-move path). Applying EO `R2 B F2 U'`:

I turn `R2 B F2 U'`.

EO applied (4 moves). Now scouting DR options on RL-axis:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Only one option found: **DR-7C8E in 8 moves total** (5 setup + 3 trigger). This is a bad substate (7C8E is the worst family). Let me try a different approach — maybe I need to commit 1-2 RZP moves first and re-scan. But wait, let me check the prior solutions more carefully.

Looking at the best 31-move solution: `R2 B F2 U' R B' D2 R' B' F' L B' U2 F2 R2 F2 U2 B2 R2 F2 R D2 R' B2 U2 R2 D2 R' U2 R' F2`

After EO (`R2 B F2 U'`), the next moves are `R B' D2 R' B' F' L B'`. Let me try applying these as RZP and see what DR emerges:

I turn `R B' D2 R' B' F' L B'`.

Applied 8 RZP moves (total 12 moves). Let me check if this reached DR:

Quick check: DR-locked on RL, not yet HTR.

**Excellent!** I'm at DR on RL-axis in 12 moves (4 EO + 8 RZP/trigger). This matches the prior successful path. Now let me classify the HTR state:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 12 moves (recall).

**HTR classified as 2-swap long-cycle:**
- HTR reduction: 10 moves
- Finish: 12 moves
- **Total: 22 moves post-DR**
- **Grand total: 12 + 22 = 34 moves**

This matches the 34-move prior attempts. The 31-move solution must have found better HTR or insertions. Let me apply the HTR reduction and check for insertable 3-cycles along the way:

For the corner reduction, I see `R U2 R F2` (chunk of a 10-move phase) — apply and re-check.

Applying first 4 moves of HTR reduction:

I turn `R U2 R F2`.

Checking state after 4 moves of reduction:

Quick check: DR-locked on RL, not yet HTR.

Not at HTR yet. Continuing reduction:

For the corner reduction, I see `R2 B2 D2 R` (chunk of a 6-move phase) — apply and re-check.

I turn `R2 B2 D2 R`.

Quick check: DR-locked on RL, not yet HTR.

Continuing:

For the corner reduction: `F2 R`.

I turn `F2 R`.

HTR reduction complete (10 moves total). Now at 22 moves. Let me check state and then apply finish:

Quick check: in HTR.

Perfect! Now at HTR (all axes EO+DR, is_htr_ud=true). Applying finish phase:

For the half-turn finish, I see `U2 B2 R2 D2` (chunk of a 12-move phase) — apply and re-check.

I turn `U2 B2 R2 D2`.

Quick check: in HTR.

Continuing finish:

For the half-turn finish, I see `F2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 U2`.

Quick check: in HTR.

Continuing:

For the half-turn finish: `L2 D2 R2 U2`.

I turn `L2 D2 R2 U2`.

A quick glance — the cube is solved.

**SOLVED in 34 moves!** This matches some prior attempts but is 3 moves longer than the best 31. Let me compose and verify the solution, then see if I can optimize with cancellation or replace_and_shorten:

I assemble the canonical normal-frame solution: **34 moves**, verified.

I have a 34-move solution. Since this is ≥27 moves, I should try replace_and_shorten on a tail span. Looking at the solution, the finish phase (moves 23-34) is 12 moves long. Let me try replace_and_shorten on that span:

Budget check: 3325.42s sim, None tool calls remaining.

I have plenty of budget (3325s sim remaining). Let me try replace_and_shorten on the HTR finish portion (moves 12-34):

replace_and_shorten on the tail span: substitute is 1 move shorter. Accepted.

**Great!** Replace_and_shorten saved 1 move (from 34 to 33). The new history is verified to solve. Let me apply cancellation to see if there are any same-face merges:

I run cancellation: 33 → 31 moves (saved 2).

**Excellent!** Cancellation saved 2 more moves. The solution is now **31 moves** — matching the best prior attempts! Let me verify this solution:

verify_solved: ✓ — 31 moves.

**VERIFIED!** 31-move solution confirmed. This matches the best prior result. Let me check my budget and submit:

Budget check: 3294.42s sim, None tool calls remaining.

Perfect! I achieved a **31-move solution** with plenty of time remaining (only 306s of 3600s used). This matches the best prior result.

**SOLUTION BREAKDOWN:**
- **EO (RL-axis, normal):** `R2 B F2 U'` — 4 moves
- **RZP + DR:** `R B' D2 R' B' F' L B'` — 8 moves (total 12 to DR)
- **HTR reduction + Finish:** 22 moves (optimized to 19 via replace_and_shorten + cancellation)
- **Total:** 31 moves

The key insight was following the proven RL-axis path from prior attempts, then applying replace_and_shorten to optimize the post-DR phase, followed by cancellation to merge adjacent moves.

**FINAL_SOLUTION:** ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "U2", "F2", "R2", "F2", "U2", "B2", "R2", "F2", "R", "D2", "R'", "B2", "U2", "R2", "D2", "R'", "U2", "R'", "F2"]

*Thinking (38):*

> The user is right - I need to formally submit the solution. I have verified it's a 31-move solution that solves the scramble. Let me output the FINAL_SOLUTION.

**FINAL_SOLUTION:** ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "U2", "F2", "R2", "F2", "U2", "B2", "R2", "F2", "R", "D2", "R'", "B2", "U2", "R2", "D2", "R'", "U2", "R'", "F2"]

*Thinking (39):*

> The user is asking me to output the FINAL_SOLUTION. I've already verified a 31-move solution that matches the best prior attempts. I should output it in the exact format requested.
> 
> The solution I verified is:
> ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "U2", "F2", "R2", "F2", "U2", "B2", "R2", "F2", "R", "D2", "R'", "B2", "U2", "R2", "D2", "R'", "U2", "R'", "F2"]
> 
> Let me output this properly.

FINAL_SOLUTION: ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "U2", "F2", "R2", "F2", "U2", "B2", "R2", "F2", "R", "D2", "R'", "B2", "U2", "R2", "D2", "R'", "U2", "R'", "F2"]

**Verified solution (31 moves):** `R2 B F2 U' R B' D2 R' B' F' L B' U2 F2 R2 F2 U2 B2 R2 F2 R D2 R' B2 U2 R2 D2 R' U2 R' F2`
