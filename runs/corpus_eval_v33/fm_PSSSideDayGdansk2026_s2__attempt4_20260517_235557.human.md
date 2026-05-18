# Solve — fm_PSSSideDayGdansk2026_s2__attempt4_20260517_235557

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 34 moves
**Solution**: `R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`

---

*Thinking (1):*

> Looking at the prior attempts, the best solution is 26 moves. Let me start by inspecting the state to understand what axes and EO options are available.
> 
> The instruction emphasizes I should commit hard to one line and finish it cleanly. The prior attempts appear to have converged on good solutions (26 moves is quite strong), so I should aim for similar or better.
> 
> Let me start with inspect_state to see the bad edges per axis and then quickly scout EO options.

I'll solve this scramble systematically, learning from the prior 26-move attempt. Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good, I can see **UD: 6 bad, FB: 4 bad, RL: 4 bad**. The FB and RL axes have the fewest bad edges. The prior 26-move attempt likely used one of these. Also notice **top_pairs_on_inverse: 3** on UD — that's a strong NISS signal for that axis. Let me scout EO on both FB and RL first, then check inverse as well.

**EO scouting strategy**: FB and RL both have 4 bad edges, which typically yields 1-3 move EOs. I'll check both, then also check the inverse side given the strong pairs-on-inverse signal.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL give 4-move EOs. Now let me check the inverse side — the 3 pairs-on-inverse on UD is a strong signal. I'll flip to inverse and check UD-axis EO there.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

Inverse UD also gives a 4-move EO (for 6 bad edges, that's quite good). Now I need to probe DR on each candidate to make the joint decision. Let me commit one EO at a time and check DR options:

**Candidate 1: Inverse UD-axis, EO = B R2 U F'**

I turn `B R2 U F'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

**No DR options found within 5 moves on inverse UD.** That's not good. Let me reset and try the normal-side FB or RL axes. I'll reset and test FB-axis first.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

**Candidate 2: Normal FB-axis, EO = B2 L2 U2 R'**

I turn `B2 L2 U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Also no options on FB. Let me reset and try RL-axis.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

**Candidate 3: Normal RL-axis, EO = R2 B F2 U'**

I turn `R2 B F2 U'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Good! **RL-axis gives DR-7C8E in 8 moves total (5 setup + 3 trigger)**. That's within the acceptable range. However, DR-7C8E is a poor substate (typically 14-16 moves post-DR). Looking at the prior 26-move solution, it likely used a different approach. Let me check if `dr_recognize` can find a better path by using the brain fallback.

Let me try `dr_recognize` to see if the brain suggests better moves:

I check whether the DR is recognizable from this state via the library.

The brain suggests F2 with highest probability. Let me apply it and re-query:

I turn `F2`.

I check whether the DR is recognizable from this state via the library.

This is taking too long. Let me commit to the DR-7C8E option I found and continue. The total to DR would be 4 (EO) + 8 (DR) = 12 moves, which is acceptable. Let me apply the setup and trigger:

I rewind 1 move.

I turn `R B' D2 R' B' F' L B`.

Good, I'm now at DR on RL-axis. Let me classify the HTR state and finish:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 12 moves (recall).

**HTR classify shows 11-move reduction + 12-move finish = 23 moves post-DR.** Total would be 12 (to DR) + 23 = **35 moves**, which is worse than my prior attempts. This line is not competitive. Let me try a different approach.

Let me reset and reconsider. The prior 26-move solution suggests there's a much better path. Let me check if there's an inverse-side option I missed. I'll reset and try inverse-FB or inverse-RL.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

Now let me try FB-axis on the inverse:

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

Excellent! **Inverse FB-axis gives a 2-move EO: U2 R'**. Let me apply it and check DR options:

I turn `U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

No DR options within 5 moves on inverse FB either. Let me try `dr_recognize` with the brain:

I check whether the DR is recognizable from this state via the library.

The brain suggests R2 strongly. Let me apply it iteratively:

I turn `R2`.

I check whether the DR is recognizable from this state via the library.

Good, R' and R2 cancelled to R. Brain suggests F2 next:

I turn `F2`.

I check whether the DR is recognizable from this state via the library.

Brain suggests L or D. Let me try L:

I turn `L`.

I check whether the DR is recognizable from this state via the library.

Brain strongly suggests L'. Let me apply it:

I turn `L'`.

I check whether the DR is recognizable from this state via the library.

L and L' cancelled. I'm going in circles. This approach is not working. Let me try a different strategy — I'll go back to the normal side and try a longer but more systematic search. Let me reset and look at the prior 26-move solution structure to understand what approach worked.

Looking at attempt 3: `B2 R' D' R' D' R U F2 R2 U B2 U2 R2 U B2 F2 U2 R2 F2 U2 L2 U2 F U' R2 B'`

This looks like it might start with B2 R' which could be an EO or premove setup. Let me try this systematically by examining what happens with a shorter EO. Let me check if there are any 1-2 move EO options I missed by checking inverse-RL:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

Inverse RL is 5 moves (partial). This is taking too long. Let me take a much more direct approach. I'll use the best EO I found (inverse FB, 2 moves), then manually work through DR using a more flexible approach. Let me reset and commit to inverse FB:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `U2 R'`.

Good, I'm at EO on inverse FB-axis (2 moves). Let me try using `brain_suggest` for the DR step, which is more flexible than the catalog search:

My trained intuition for dr: top candidates are R2 (65%), F2 (23%), B2 (9%).

Brain suggests R2. Let me try a sequence iteratively — I'll apply R2, then recheck. Let me use try_alg to preview longer sequences without committing:

I try `R2 F2 U2 R2` on top to see the after-state (without committing).

Still DR-5C2E on FB after that sequence — not at DR yet. Let me try a different strategy. Given the time constraints and the difficulty finding clean DR paths, let me check the budget and consider trying a completely different approach — maybe starting from normal side with a different EO method.

Budget check: 2301.24s sim, None tool calls remaining.

I still have plenty of time (2301s sim, 1383s wall). But I'm spinning my wheels on finding DR. Let me be more decisive. I'll commit to the brain's suggestions and work through DR step-by-step with apply_moves, checking after each move:

I turn `R2 F2 U2 R2 F2 U2`.

Quick check: EO solved on FB, working toward DR.

Not at DR yet (7 moves so far). Let me continue with the brain's suggestion:

My trained intuition for dr: top candidates are L' (86%), U' (3%), D' (3%).

Brain strongly suggests L'. Let me apply it and check:

I turn `L'`.

Quick check: still scrambled.

Wait — L' broke the FB-EO! I need to backtrack. Let me undo:

I rewind 1 move.

The brain is suggesting moves that break EO. I need to use `dr_trigger_options` with a larger depth or manually recognize patterns. Let me try depth 6:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on FB.**

Still no trigger found. This line is too difficult. Let me reset and try a completely different approach. Looking at my time budget, I should try to finish quickly with a working solution rather than chase perfection. Let me go back to the RL-axis solution I found earlier (35 moves total) and complete it to have SOMETHING, then if time permits, I can optimize.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me quickly execute the RL-axis path I found earlier: EO (4 moves) + DR (8 moves) + HTR (23 moves):

I turn `R2 B F2 U' R B' D2 R' B' F' L B`.

Now let me apply the HTR phases:

For the corner reduction, I see `B2 R U2 R` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 R U2 R`.

Quick check: DR-locked on RL, not yet HTR.

Good, still at DR on RL. Continue HTR reduction:

For the corner reduction, I see `F2 R2 B2 D2` (chunk of a 7-move phase) — apply and re-check.

I turn `F2 R2 B2 D2`.

For the corner reduction: `R F2 R`.

I turn `R F2 R`.

Quick check: in HTR.

Excellent! I'm at HTR after 22 moves (is_htr_ud: true). Now let me apply the finish phase:

For the half-turn finish, I see `U2 B2 R2 D2` (chunk of a 12-move phase) — apply and re-check.

I turn `U2 B2 R2 D2`.

Quick check: in HTR.

Still at HTR. Continue finish:

For the half-turn finish, I see `F2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 U2`.

Quick check: in HTR.

For the half-turn finish: `L2 D2 R2 U2`.

I turn `L2 D2 R2 U2`.

A quick glance — the cube is solved.

Perfect! **The cube is SOLVED in 34 moves.** Now let me compose the final solution and verify:

I assemble the canonical normal-frame solution: **34 moves**, verified.

Good! I have a verified 34-move solution. However, this is worse than my prior best (26 moves) and even worse than attempt 1 (34 moves). I still have plenty of time. Let me try replace_and_shorten to see if I can improve it:

Budget check: 1964.84s sim, None tool calls remaining.

I have enough budget. Let me call replace_and_shorten on the latter part of the solution (after DR):

r&s: too few tool calls remaining (9) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

I don't have enough tool calls remaining for replace_and_shorten. I need to ship the current solution. This 34-move solution matches my first attempt. Let me verify it one more time and submit:

verify_solved: ✓ — 34 moves.

Perfect! The solution is verified. **FINAL_SOLUTION:**

**FINAL_SOLUTION: ["R2", "B", "F2", "U'", "R", "B'", "D2", "R'", "B'", "F'", "L", "B'", "R", "U2", "R", "F2", "R2", "B2", "D2", "R", "F2", "R", "U2", "B2", "R2", "D2", "F2", "U2", "F2", "U2", "L2", "D2", "R2", "U2"]**

**Move count: 34 moves**

## Solution breakdown:
- **EO (RL-axis)**: R2 B F2 U' (4 moves)
- **DR setup + trigger**: R B' D2 R' B' F' L B (8 moves) → DR-7C8E trigger
- **HTR reduction**: B' R U2 R F2 R2 B2 D2 R F2 R (11 moves)
- **HTR finish**: U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2 (12 moves)

This solution uses the **RL-axis** approach with a relatively clean finish through the HTR pipeline. While it doesn't beat the prior best of 26 moves, it's a complete, verified solution that demonstrates the standard FMC methodology: EO → DR → HTR → finish.

**Verified solution (34 moves):** `R2 B F2 U' R B' D2 R' B' F' L B' R U2 R F2 R2 B2 D2 R F2 R U2 B2 R2 D2 F2 U2 F2 U2 L2 D2 R2 U2`
