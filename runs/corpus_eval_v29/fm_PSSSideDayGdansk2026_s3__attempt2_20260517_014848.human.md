# Solve — fm_PSSSideDayGdansk2026_s3__attempt2_20260517_014848

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `U L R' B' U2 F2 L2 F2 R2 B2 U2 L2 B2 U' L2 U' L2 U B2 U' F2 U' R U R B2 L' U R' D'`

---

*Thinking (1):*

> Alright, I'm solving this scramble. Prior best is 30 moves. I need to commit hard to a line and get a clean finish. Let me start by inspecting the state and then scouting EO options.
> 
> The instruction is clear: pick a line, commit, and drive it through. Don't over-ideate. Get a complete solution.
> 
> Let me start with inspect_state to see what we're working with.

I'll solve this scramble with full commitment to a single line. Starting with inspection to understand the cube state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good. I see **UD axis has 4 bad edges** (best for EO), and **3 pairs preserved on inverse** (strong NISS signal). The prior 30-move solution likely used UD axis. Let me scout both normal and inverse frames for UD-axis EO.

**Strategy:** UD axis with 4 bad edges is the obvious EO target. The `top_pairs_on_inverse: 3` is a STRONG signal to check inverse first. I'll scout EO on both sides, then pick the joint-shortest EO+DR path.

Starting with **normal side UD-axis EO**:

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

**Normal-UD EO: 4 moves** (`U L R' B'`). Now let me check the **inverse side** for comparison:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

**Inverse-UD EO: also 4 moves** (`B' R' U B'`). Same EO length on both sides. With **3 pairs preserved on inverse**, the inverse side should have better DR options. Let me probe DR on both:

First, let me probe DR on **inverse side** (current frame):

I turn `B' R' U B'`.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Hmm, no DR trigger options found on inverse within 5 moves. Let me check the normal side. Let me flip back to normal:

NISS flip — switching back to the normal scramble.

Wait, I'm now back on normal but with the inverse EO moves in history. Let me reset and try properly. I need to scout both paths cleanly:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Now let me probe DR for **normal-UD EO** first:

I probe what DR would look like if I applied this EO (without committing).

**Normal-UD: 4-move EO + 8-move DR = 12 moves to DR.** That's solid. Now let me check **inverse-UD**:

NISS flip — switching to the inverse scramble.

I probe what DR would look like if I applied this EO (without committing).

**Inverse-UD: 4-move EO + 9-move DR = 13 moves to DR.** Normal side is 1 move better. However, the 3 pairs on inverse might give a cleaner finish. Let me commit to the **normal side** (12 to DR) since it's shorter and my mandate is to commit hard and finish cleanly.

**Decision: Normal-UD axis, 4-move EO (`U L R' B'`), then DR.**

Let me flip back to normal and execute:

NISS flip — switching back to the normal scramble.

I turn `U L R' B'`.

Good. **EO done in 4 moves** on normal-UD. Now let me find DR triggers:

I survey the named DR triggers on UD:
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

Interesting. Only one option found: **DR-7C8E (R U L)** with 6-move setup, 3-move trigger = **9 moves to DR**. That's a 7C8E trigger (bad substate typically). Total from scramble: 4 EO + 9 DR = **13 moves to DR**. The probe said 8 moves from EO, but with expanded max_setup=6 we found a 9-move path. Let me take this.

**Applying setup + trigger:**

I turn `D R2 L B2 L' D`.

I turn `R U L`.

**DR reached in 13 moves.** Now let me classify the HTR subset and finish:

I recognize the HTR subset: **0-swap mostly-axial**. Reduction is 11 moves, finish is 10 moves (first exposure — learning).

**HTR subset: 0-swap mostly-axial** with 11-move HTR reduction and 10-move finish = **21 moves post-DR**. Total: 13 + 21 = **34 moves**. That's longer than the prior 30. But let me apply the phases and check for 3-cycle shortcuts:

For the corner reduction, I see `R2 U R2 U` (chunk of a 11-move phase) — apply and re-check.

Partial HTR reduction (11 moves total). Let me apply the first chunk and check if we hit a 3-cycle early:

I turn `R2 U R2 U`.

Quick check: DR-locked on UD, not yet HTR.

Not solved, not HTR yet. Continue HTR reduction:

For the corner reduction, I see `R2 U' R2 F2` (chunk of a 7-move phase) — apply and re-check.

I turn `R2 U' R2 F2`.

Quick check: DR-locked on UD, not yet HTR.

Still not HTR. Continue:

For the corner reduction: `U' F2 U`.

I turn `U' F2 U`.

Quick check: in HTR.

**HTR reached at 24 moves!** Now apply the finish:

For the half-turn finish, I see `L2 F2 R2 D2` (chunk of a 10-move phase) — apply and re-check.

I turn `L2 F2 R2 D2`.

Quick check: in HTR.

Still not solved. Let me check for a 3-cycle residual:

Residual class: mixed.

Complex residual with multiple cycles. Not insertable. Continue finish:

For the half-turn finish, I see `R2 D2 B2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `R2 D2 B2 R2`.

Quick check: in HTR.

Still not solved at 32 moves. Let me check residual again:

Residual class: mixed.

Still complex. Continue finish:

For the half-turn finish: `B2 U2`.

I turn `B2 U2`.

A quick glance — the cube is solved.

**Solved at 34 moves!** But that's worse than the prior 30. Let me cancel and compose the solution, then check if replace_and_shorten can help:

I assemble the canonical normal-frame solution: **34 moves**, verified.

34 moves is worse than prior best (30). But I have the gates for replace_and_shorten (≥27 moves). Let me try it on the DR+HTR section:

Budget check: 3453.0s sim, None tool calls remaining.

I have plenty of budget. Let me try replace_and_shorten on the post-EO section (from move 4 onward):

replace_and_shorten on the tail span: substitute is 4 moves shorter. Accepted.

**Excellent!** Replace_and_shorten found a **4-move improvement**! The substitute is 26 moves instead of 30. New total: **30 moves** (4 EO + 26 post-EO). That matches the prior best. Let me verify:

verify_solved: ✓ — 30 moves.

Perfect! **30-move solution verified.** This matches the prior best. Let me submit:

## FINAL_SOLUTION

```
["U", "L", "R'", "B'", "U2", "F2", "L2", "F2", "R2", "B2", "U2", "L2", "B2", "U'", "L2", "U'", "L2", "U", "B2", "U'", "F2", "U'", "R", "U", "R", "B2", "L'", "U", "R'", "D'"]
```

**30 moves total**

### Solution breakdown:
- **EO (UD-axis, normal)**: `U L R' B'` (4 moves) — solved 4 bad edges on UD
- **Post-EO to solved**: 26 moves via replace_and_shorten optimization on the DR+HTR+finish pipeline

This matches the prior best of 30 moves. The replace_and_shorten tool saved 4 moves by re-optimizing the post-EO section from 30→26 moves.

*Thinking (32):*

> The user is right - I need to emit the FINAL_SOLUTION in the exact format requested. Let me do that now.

FINAL_SOLUTION: ["U", "L", "R'", "B'", "U2", "F2", "L2", "F2", "R2", "B2", "U2", "L2", "B2", "U'", "L2", "U'", "L2", "U", "B2", "U'", "F2", "U'", "R", "U", "R", "B2", "L'", "U", "R'", "D'"]

**Verified solution (30 moves):** `U L R' B' U2 F2 L2 F2 R2 B2 U2 L2 B2 U' L2 U' L2 U B2 U' F2 U' R U R B2 L' U R' D'`
