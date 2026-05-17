# Solve — fm_PSSSideDayGdansk2026_s2__attempt3_20260517_164345

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 34 moves
**Solution**: `R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`

---

*Thinking (1):*

> The user wants me to solve this FMC scramble. I have two prior attempts:
> - Attempt 1: 34 moves
> - Attempt 2: 31 moves
> 
> The instruction is very clear: COMMIT HARD this attempt. Pick a line and drive it to a clean finish. Don't over-ideate between branches. The goal is to get a COMPLETE solution, and if possible improve on the 31-move best.
> 
> Let me start by inspecting the state to see what we're working with.
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I'll begin with inspect_state to see the bad edges per axis and other key metrics.

I'll solve this scramble systematically, aiming to beat the 31-move best. Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good! Bad edges: UD=6, FB=4, RL=4. Both FB and RL have 4 bad edges, which is often a sweet spot (1-3 move EO). Let me scout EO on both axes, and also check the inverse side.

**EO scouting plan**: FB and RL both have 4 bad edges. The prior 31-move solution likely used one of these. I'll check both on normal, then also probe inverse if needed.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both axes give 4-move EOs: FB = `B2 L2 U2 R'`, RL = `R2 B F2 U'`. The RL EO matches the start of both prior attempts! Let me also check inverse side to be thorough.

NISS flip — switching to the inverse scramble.

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

Excellent! **Inverse-FB gives 2-move EO**: `U2 R'`. This is significantly shorter than the 4-move options on normal. The UD axis had `top_pairs_on_inverse: 3`, which is a strong NISS signal. Let me commit to inverse-FB EO and probe DR from there.

**Decision**: Taking inverse-FB EO (`U2 R'`, 2 moves). This is 2 moves shorter than the prior attempts' 4-move RL EO on normal.

I turn `U2 R'`.

Now let me probe DR options on the FB axis (still on inverse side):

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

No DR triggers found within 5 moves on FB axis from this state. Let me check the other axes (UD and RL) to see if a different axis has a cleaner DR path:

DR trigger menu on UD: EO not yet solved on axis UD; run eo_pattern_lookup and apply EO moves first.

DR trigger menu on RL: EO not yet solved on axis RL; run eo_pattern_lookup and apply EO moves first.

Right, I've only solved EO on FB axis. The FB axis has no DR triggers within 5 moves. This is concerning. Let me try a different approach: go back to normal side and use the RL EO that the prior attempts used, since those reached 31-34 moves (complete solutions).

**Pivot decision**: The inverse-FB EO is shorter (2 vs 4 moves) but leads nowhere for DR. The prior attempts used RL-normal EO and found complete solutions. I'll switch back to normal and commit to RL EO.

NISS flip — switching back to the normal scramble.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Good, I'm back at the scramble on normal side. Now let me commit to the RL EO that worked in prior attempts:

I turn `R2 B F2 U'`.

Now let me probe DR options on RL axis:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Only one DR option found: **DR-7C8E** in 8 moves total (5 setup + 3 trigger). This is a long DR but has `top_pairs_on_inverse: 3` which suggests switching to inverse after DR might be good. The 7C8E substate is typically difficult (12-15 move finish). This would give us 4 EO + 8 DR + ~14 finish = ~26 moves, competitive with the 31-move prior.

Let me also check what happens if I explore further setup moves manually to find a better DR:

I check my gut for plausible next moves.

The policy suggests `B'` and `F2` as top moves. Let me try a different approach: commit to the DR-7C8E path since it's what I found, apply it, and then work through HTR systematically.

I turn `R B' D2 R' B' F' L B`.

Now I'm at DR on RL axis. Let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 12 moves (recall).

HTR finish is **23 moves total** (11 reduction + 12 finish). This gives us:
- EO: 4 moves
- DR: 8 moves  
- HTR: 23 moves
- **Total: 35 moves**

This is worse than the 31-move prior attempt. Let me reconsider. The issue is the DR path is too long (8 moves) and leads to a difficult subset (23-move finish).

Let me reset and try the FB axis EO instead, which also gave 4 moves on normal:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `B2 L2 U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on FB.**

FB axis also has no DR triggers within 6 moves. Let me check UD axis:

DR trigger menu on UD: EO not yet solved on axis UD; run eo_pattern_lookup and apply EO moves first.

Alright, the FB-normal EO doesn't lead to a clean DR either. Let me go back to the RL path that found a solution (even if 35 moves), and try to optimize the finish. The instructions say "COMMIT HARD" and get a complete solution. 35 moves is better than DNF.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B F2 U' R B' D2 R' B' F' L B`.

Now let me apply the HTR reduction phase:

For the corner reduction, I see `B2 R U2 R` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 R U2 R`.

Good! 1 move was cancelled (B and B2 became B'). Let me check if we've reached a useful state with quick_check:

Quick check: DR-locked on RL, not yet HTR.

Still in DR on RL, not yet HTR. Let me continue the HTR reduction:

For the corner reduction, I see `F2 R2 B2 D2` (chunk of a 7-move phase) — apply and re-check.

I turn `F2 R2 B2 D2`.

Quick check: DR-locked on RL, not yet HTR.

For the corner reduction: `R F2 R`.

I turn `R F2 R`.

Quick check: in HTR.

Excellent! Now at HTR (all axes EO/DR solved, is_htr_ud = true). Now apply the finish phase:

For the half-turn finish, I see `U2 B2 R2 D2` (chunk of a 12-move phase) — apply and re-check.

I turn `U2 B2 R2 D2`.

Quick check: in HTR.

For the half-turn finish, I see `F2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 U2`.

Quick check: in HTR.

For the half-turn finish: `L2 D2 R2 U2`.

I turn `L2 D2 R2 U2`.

A quick glance — the cube is solved.

Excellent! The cube is solved in **34 moves**. This matches Attempt 1. Let me verify and apply cancellation:

I assemble the canonical normal-frame solution: **34 moves**, verified.

The solution is 34 moves, which equals my Attempt 1 but is 3 moves longer than the 31-move Attempt 2. Since I have 34 moves and the guidelines say to use replace_and_shorten when ≥27 moves, let me try that to see if I can improve:

Budget check: 2635.16s sim, None tool calls remaining.

I have plenty of time remaining (2635s). Let me try replace_and_shorten on a large segment to see if we can shorten this:

r&s: could not solve micro-scramble for span [4:34]: no DR found

The replace_and_shorten didn't find a better solution. I've now used my 1 allowed call. Let me submit the 34-move solution:

verify_solved: ✓ — 34 moves.

Perfect! The solution is verified. This is a complete 34-move solution, matching Attempt 1 but not beating the 31-move Attempt 2. 

## FINAL_SOLUTION

**FINAL_SOLUTION**: ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "R", "U2", "R", "F2", "R2", "B2", "D2", "R", "F2", "R", "U2", "B2", "R2", "D2", "F2", "U2", "F2", "U2", "L2", "D2", "R2", "U2"]

**Total moves: 34**

### Solution breakdown:
- **EO (RL-axis)**: R2 B F2 U' (4 moves)
- **DR (RL-axis)**: R B' D2 R' B' F' L B (8 moves) — DR-7C8E trigger
- **HTR reduction**: B' R U2 R F2 R2 B2 D2 R F2 R (11 moves, with 1 cancellation)
- **HTR finish**: U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2 (12 moves)

This matches my first attempt's move count. The challenge was that this scramble has difficult DR access — the shortest DR trigger found was 8 moves with a complex 7C8E substate requiring a 23-move finish. A complete, verified solution is achieved.

*Thinking (37):*

> The user is right - I narrated the solution but didn't properly emit it in the required format. Let me output the FINAL_SOLUTION in the correct format.

FINAL_SOLUTION: ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "R", "U2", "R", "F2", "R2", "B2", "D2", "R", "F2", "R", "U2", "B2", "R2", "D2", "F2", "U2", "F2", "U2", "L2", "D2", "R2", "U2"]

**Verified solution (34 moves):** `R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`
