# Solve — fm_PSSSideDayGdansk2026_s3__attempt5_20260517_102805

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 27 moves
**Solution**: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`

---

*Thinking (1):*

> I need to solve this scramble within the one-hour budget. The prior attempts achieved 27 moves (best) to 30 moves.
> 
> Looking at the context, the instruction is to COMMIT HARD - pick a line and drive it to completion. Don't over-ideate between branches. The goal is to get a complete, clean solution.
> 
> Let me start by inspecting the state to see what I'm working with.

I'll solve this scramble systematically. The prior best is 27 moves, so I need to find a clean line and commit to it. Let me start by inspecting the scramble state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good, I can see the scramble state clearly:
- **UD axis**: 4 bad edges (UL, DR, DL, DB) — the best EO starting point
- **FB axis**: 8 bad edges — likely needs NISS
- **RL axis**: 6 bad edges

**Top_pairs_on_inverse = 3 on UD** is a STRONG signal. This suggests the inverse frame may have a better DR path. Let me scout EO on both the normal and inverse sides for the UD axis.

First, let me check the UD-axis EO on the normal side:

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

**UD-axis EO on normal: 4 moves** (`U L R' B'`). Now let me scout the inverse side, since `top_pairs_on_inverse = 3` is a strong signal:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

**Inverse UD-axis EO: also 4 moves** (`B' R' U B'`). Same length, but with `top_pairs_on_inverse = 3`, the inverse side should have a cleaner DR. Let me probe the DR options on the inverse side:

I turn `B' R' U B'`.

Now let me check the DR trigger options on the inverse UD axis after this EO:

DR trigger menu on UD: no named trigger fits within 5 setup moves.

No DR triggers found within 5 moves on inverse UD. Let me try dr_recognize to see what the actual DR distance is:

I check whether the DR is recognizable from this state via the library.

**9 moves to DR on inverse UD** is too long (the hard rule is DR ≥10 is a signal the axis is wrong). Let me backtrack and try the normal side instead. I'll flip back to normal:

NISS flip — switching back to the normal scramble.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Now let me try the normal UD-axis EO and check the DR options:

I turn `U L R' B'`.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

I check whether the DR is recognizable from this state via the library.

**8 moves to DR on normal UD** is also too long. Both UD paths are poor. Let me check FB axis since 8 bad edges might actually lead to a short DR via NISS or a symmetry pattern. Let me reset and try FB:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

Excellent! **FB-axis EO is only 4 moves** despite having 8 bad edges. This is the symmetry pattern I suspected. Let me apply this EO and check DR:

I turn `R' F D L'`.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

I check whether the DR is recognizable from this state via the library.

**7 moves to DR on FB** — that's 4+7=11 total to DR, which is better than UD's options. Let me commit to this and continue:

I turn `B' D F' U'`.

I check whether the DR is recognizable from this state via the library.

Great! Only **3 more moves to DR** (2-move setup `B L2` + 1-move trigger `D'`). Total to DR = 4+4+3 = 11 moves. Let me apply these:

I turn `B L2`.

I turn `D'`.

Now I'm at DR on the FB axis. Let me classify the HTR state:

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 8 moves, finish is 9 moves (recall).

**HTR subset: 4-swap long-cycle** with 8-move reduction + 9-move finish = **17 moves** to finish. Total so far: 11 (to DR) + 17 = **28 moves**. This is close to the prior attempts. Let me apply the HTR reduction:

For the corner reduction, I see `D2 F2 R2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `D2 F2 R2 U2`.

Good, there's already 1 move cancelled (`D'` + `D2` → `D`). Let me check if I've reached a solvable residual before continuing:

Quick check: DR-locked on FB, not yet HTR.

Not solved yet. Let me continue the HTR reduction:

For the corner reduction: `F' U2 L2 B`.

I turn `F' U2 L2 B`.

Quick check: in HTR.

Excellent! I'm now at HTR on all axes (`is_htr_ud: true`). Let me apply the finish phase:

For the half-turn finish, I see `R2 U2 B2 R2` (chunk of a 9-move phase) — apply and re-check.

I turn `R2 U2 B2 R2`.

Quick check: in HTR.

Let me check if this is a clean residual (3-cycle or similar):

Residual class: mixed.

Not a clean 3-cycle; it's a complex mixed state. Let me continue the finish:

For the half-turn finish, I see `F2 U2 B2 D2` (chunk of a 5-move phase) — apply and re-check.

I turn `F2 U2 B2 D2`.

Quick check: in HTR.

For the half-turn finish: `F2`.

I turn `F2`.

A quick glance — the cube is solved.

Perfect! **The cube is solved in 27 moves**, matching the prior best attempt. Now let me compose the final solution with cancellation:

I assemble the canonical normal-frame solution: **27 moves**, verified.

Let me verify this solution:

verify_solved: ✓ — 27 moves.

Excellent! I have a verified **27-move solution** that matches the prior best. According to the rules, since this is ≥27 moves and I have plenty of budget remaining, I should try `replace_and_shorten` once to see if I can improve it. Let me check my budget status:

Budget check: 3435.0s sim, None tool calls remaining.

I have 3435 seconds remaining, which is plenty. The replace_and_shorten gates require ≥27 moves (I have 27) and ≥30 tool calls remaining (I've used about 30 tool calls, so I have plenty left). Let me try to shorten the tail of the solution:

replace_and_shorten: substitute is 5 moves longer; reject.

The replace_and_shorten result is **+5 moves worse** (delta=+5), making a 32-move solution. I should keep my original 27-move solution. Let me submit it:

**FINAL_SOLUTION**: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

**Solution breakdown:**
- **EO (FB-axis)**: `R' F D L'` — 4 moves, solved 8 bad edges using the symmetry pattern
- **DR setup**: `B' D F' U' B L2` — 6 moves of RZP setup  
- **DR trigger**: `D'` → cancelled with next move to `D` — 1 move (single inverse trigger)
- **HTR reduction**: `D F2 R2 U2 F' U2 L2 B` — 8 moves to HTR corner subgroup (4-swap long-cycle subset)
- **HTR finish**: `R2 U2 B2 R2 F2 U2 B2 D2 F2` — 9 moves half-turn finish

**Total: 27 moves**

This matches the prior best attempt of 27 moves. The solution is clean, fully verified, and used the FB-axis path which gave a manageable 11-move route to DR despite initially looking unpromising with 8 bad edges.

*Thinking (44):*

> The user is right - I need to explicitly emit the FINAL_SOLUTION in the exact format requested. Let me output it now.

FINAL_SOLUTION: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

**Verified solution (27 moves):** `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
