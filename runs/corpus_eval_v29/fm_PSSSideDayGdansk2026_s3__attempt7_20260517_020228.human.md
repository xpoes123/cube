# Solve — fm_PSSSideDayGdansk2026_s3__attempt7_20260517_020228

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `U L R' B' F2 D' R' U' F2 L' D' R D2 L2 U2 F2 U2 F2 L2 F2 U2 F2 U' L2 F2 R2 B2 U2 R2 U'`

---

*Thinking (1):*

> Looking at the prior attempts, I can see that attempts 1, 2, 3, 5, and 6 all produced the exact same 30-move solution. Attempt 4 was worse at 34 moves. This suggests that the 30-move solution is a well-established local optimum that's been found repeatedly.
> 
> The instruction is clear: **COMMIT HARD this attempt.** Pick a line and drive it to a clean finish. Don't over-ideate between branches. The prior attempts converged on a 30-move solution, so I should:
> 
> 1. First inspect_state to see the scramble
> 2. Quickly scout EO options on different axes
> 3. Pick ONE promising axis/side combination
> 4. Commit to it fully and drive through EO → DR → HTR → finish
> 5. Use replace_and_shorten at the end if I have budget and the solution is ≥27 moves
> 
> The key insight from the instructions: "A failed or incomplete solve is worse than a 30-move complete one." So my goal is to find a COMPLETE solution, ideally better than 30 moves, but definitely complete.
> 
> Let me start by inspecting the state to see what we're working with.

I'll solve this scramble systematically. The prior attempts converged on a 30-move solution repeatedly, so I need to either find a better line or optimize the finish phase. Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good, I can see the state clearly. **Bad edges per axis: UD=4, FB=8, RL=6**. UD has the fewest bad edges (4), which is typically a 1-3 move EO. However, I notice **top_pairs_on_inverse=3** on the UD axis, which is a STRONG NISS signal. Let me scout both normal and inverse frames before committing.

**EO scouting plan:**
- UD-normal (4 bad edges) 
- UD-inverse (check if pairs-tracing signal pays off)
- Maybe FB if UD looks poor

Let me start with UD-normal EO:

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

UD-normal EO is 4 moves: `U L R' B'`. Now let me check the inverse side, since top_pairs_on_inverse=3 is a strong signal:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

Inverse UD EO is also 4 moves: `B' R' U B'`. Both sides have the same EO length (4 moves), but the **pairs signal is strong on inverse** (3 pairs). Let me probe DR on both sides to decide which to commit to.

First, let me probe DR on the inverse side (where I currently am):

I probe what DR would look like if I applied this EO (without committing).

Inverse: EO=4, DR=9, total to DR=13 moves. Now let me flip back and probe the normal side:

NISS flip — switching back to the normal scramble.

I probe what DR would look like if I applied this EO (without committing).

**Normal: EO=4, DR=8, total to DR=12 moves.** This is 1 move shorter than inverse (13). However, the 3-pair signal on inverse is strong. Let me commit the EO on normal first and actually look at the DR options with dr_trigger_options to see the substates:

I turn `U L R' B'`.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Interesting - dr_trigger_options returned no options within max_setup=5. This means the DR setup is longer than 5 moves. The probe said total_dr_length=8, so it's a bit long. Let me use dr_recognize to see what the actual DR pattern is:

I check whether the DR is recognizable from this state via the library.

The DR is 8 moves total, which is acceptable (elite threshold is ≤10). Let me apply the 4-move setup and continue:

I turn `F2 D' R' U'`.

I check whether the DR is recognizable from this state via the library.

Good! From the current state, it's a 4-move DR: 3-move setup + 1-move R' trigger (DR-4C4E variant). Let me apply these to reach DR:

I turn `F2 L' D'`.

I turn `R'`.

Quick check: DR-locked on UD, not yet HTR.

Perfect! I'm at DR on UD in 12 moves. Now let me classify the HTR substate and finish:

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 8 moves, finish is 11 moves (recall).

The HTR substate is **4-swap long-cycle** with 8-move reduction + 11-move finish = 19 moves. Total so far: 12 (to DR) + 19 (finish) = **31 moves**. This is 1 move worse than my best prior attempts. Let me proceed with the finish and then try replace_and_shorten:

For the corner reduction, I see `U R2 U R2` (chunk of a 8-move phase) — apply and re-check.

I turn `U R2 U R2`.

Quick check: DR-locked on UD, not yet HTR.

Still need more HTR reduction. Let me continue:

For the corner reduction: `L2 U L2 D`.

I turn `L2 U L2 D`.

Quick check: in HTR.

Great! I'm now at HTR (is_htr_ud=true) in 20 moves. Now let me apply the finish phase:

For the half-turn finish, I see `L2 F2 U2 L2` (chunk of a 11-move phase) — apply and re-check.

I turn `L2 F2 U2 L2`.

Quick check: in HTR.

Still not solved. Let me continue the finish:

For the half-turn finish, I see `B2 R2 B2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `B2 R2 B2 U2`.

Quick check: in HTR.

Let me get the final chunk:

For the half-turn finish: `R2 F2 U2`.

I turn `R2 F2 U2`.

A quick glance — the cube is solved.

Excellent! The cube is solved in **31 moves**. This is slightly worse than the 30-move solution, but I can optimize with cancellation and replace_and_shorten. Let me first run compose_niss_solution to get the final solution with cancellations:

I assemble the canonical normal-frame solution: **31 moves**, verified.

Good, the solution is verified at 31 moves with no cancellations. Since 31 ≥ 27 and I have plenty of tool calls remaining, I should try replace_and_shorten to see if I can improve. Let me check my budget:

Budget check: 3521.0s sim, None tool calls remaining.

I have plenty of budget. Let me try replace_and_shorten on a substantial portion of the solution. I'll target the middle-to-end section where the HTR finish happened:

replace_and_shorten: same length, no improvement.

Replace_and_shorten found an alternative with the same length (delta=0), so no improvement there. Let me try a different span - maybe the earlier DR section:

Actually, wait - I've already used my 1 replace_and_shorten call (rs_calls_used=1). The tool enforces a 1-call cap. Let me look at the current solution and see if there are obvious cancellations I can manually identify:

Looking at the solution: `U L R' B' F2 D' R' U' F2 L' D' R' R2 D2 L2 U2 F2 U2 F2 L2 F2 U2 F2 U' L2 F2 R2 B2 U2 R2 U'`

I can see that after the replace_and_shorten, there's an `R' R2` which can cancel to `R`. Let me manually apply the substitution and then cancel:

I run cancellation: 31 → 30 moves (saved 1).

Excellent! The cancellation saved 1 move, bringing us down to **30 moves**. This matches the best prior attempts. Let me verify this solution:

verify_solved: ✓ — 30 moves.

Perfect! I have a verified 30-move solution. This matches the best from prior attempts. However, I want to see if I can do better. Let me try a different approach - let me check the inverse side more carefully since it had 3 pairs preserved. Let me reset and explore that path:

Budget check: 3490.0s sim, None tool calls remaining.

I have lots of time remaining. Let me explore the inverse path to see if I can beat 30 moves. Let me reset and try the inverse:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B' R' U B'`.

I survey the named DR triggers on UD:
  • DR-3C2E (R U' R'): 6-mv setup + 3-mv trigger (9 total)
  • DR-4C2E (R U2 R'): 6-mv setup + 3-mv trigger (9 total) [JZP]

Interesting! On the inverse side after EO, I have two options:
1. DR-3C2E in 9 moves (6+3), not JZP
2. DR-4C2E in 9 moves (6+3), **JZP-eligible**

The JZP-eligible 4C2E option should have a much shorter finish (5-7 moves typical vs 9-11 non-JZP). Let me take the JZP option:

I turn `D' F2 D R2 L U'`.

I turn `R U2 R'`.

Quick check: DR-locked on UD, not yet HTR.

Perfect! I'm at DR on the inverse in 13 moves. Now let me classify the HTR substate:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 9 moves, finish is 9 moves (first exposure — learning).

Excellent! This is a **2-swap mostly-axial** subset with 9-move reduction + 9-move finish = 18 moves. Much better than the 19 moves on the normal side! Total so far: 13 (to DR) + 18 (finish) = **31 moves** before cancellations. Let me proceed with the finish:

For the corner reduction, I see `U R2 U B2` (chunk of a 9-move phase) — apply and re-check.

I turn `U R2 U B2`.

For the corner reduction, I see `U' B2 R2 L2` (chunk of a 5-move phase) — apply and re-check.

I turn `U' B2 R2 L2`.

For the corner reduction: `U`.

I turn `U`.

Quick check: in HTR.

Great! I'm at HTR in 22 moves on the inverse. Now let me apply the finish phase:

For the half-turn finish, I see `U2 R2 U2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 R2 U2 L2`.

Quick check: in HTR.

I notice auto_cancelled_saved=1! There was a cancellation between U and U2 that resulted in U'. Let me continue with the finish:

For the half-turn finish, I see `F2 U2 B2 R2` (chunk of a 5-move phase) — apply and re-check.

I turn `F2 U2 B2 R2`.

Quick check: in HTR.

For the half-turn finish: `B2`.

I turn `B2`.

A quick glance — the cube is solved.

Perfect! Solved on the inverse in **30 moves**. Now let me compose the final solution (this will invert the inverse-side moves and combine them properly):

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Excellent! I have a 30-move solution from the inverse path. Let me verify it:

verify_solved: ✓ — 30 moves.

Perfect! This is also a 30-move solution, matching the best from prior attempts. I have two different 30-move solutions now. Since both paths (normal and inverse) converge to 30 moves, and I've already used my replace_and_shorten call, let me check if there are any additional optimizations I can explore.

Let me compare the two solutions:
1. Normal path: `U L R' B' F2 D' R' U' F2 L' D' R D2 L2 U2 F2 U2 F2 L2 F2 U2 F2 U' L2 F2 R2 B2 U2 R2 U'`
2. Inverse path: `B2 R2 B2 U2 F2 L2 U2 R2 U L2 R2 B2 U B2 U' R2 U' R U2 R' U L' R2 D' F2 D B U' R B`

Both are 30 moves. Since this matches the best prior attempts and I've committed to finishing this solve, let me submit the first solution I found:

**FINAL_SOLUTION:** ["U", "L", "R'", "B'", "F2", "D'", "R'", "U'", "F2", "L'", "D'", "R", "D2", "L2", "U2", "F2", "U2", "F2", "L2", "F2", "U2", "F2", "U'", "L2", "F2", "R2", "B2", "U2", "R2", "U'"]

This is a complete, verified 30-move solution that matches the best from prior attempts. The solve followed the standard FMC pipeline:
- **EO (UD-normal)**: 4 moves `U L R' B'`
- **DR (UD-axis)**: 8 moves total to reach DR
- **HTR + Finish**: 18 moves (with 1 move saved by cancellation)
- **Total**: 30 moves

*Thinking (44):*

> The user is right - I narrated the solution but didn't actually emit it in the required format. I have a verified 30-move solution. Let me output it properly.

FINAL_SOLUTION: ["U", "L", "R'", "B'", "F2", "D'", "R'", "U'", "F2", "L'", "D'", "R", "D2", "L2", "U2", "F2", "U2", "F2", "L2", "F2", "U2", "F2", "U'", "L2", "F2", "R2", "B2", "U2", "R2", "U'"]

**Verified solution (30 moves):** `U L R' B' F2 D' R' U' F2 L' D' R D2 L2 U2 F2 U2 F2 L2 F2 U2 F2 U' L2 F2 R2 B2 U2 R2 U'`
