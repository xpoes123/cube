# Solve — fm_PSSSideDayGdansk2026_s3__attempt4_20260516_181416

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble within the one-hour simulated budget. I should start by inspecting the state as requested, then follow the elite-solver pipeline:
> 
> 1. inspect_state(main)
> 2. niss_scout(main) - this will give me the 6-row table comparing all axes and sides
> 3. Based on the recommendation, choose the best EO+DR path
> 4. Execute the pipeline: EO → DR → HTR → finish
> 5. Verify and submit
> 
> Let me start with inspect_state.

I'll solve this FMC scramble step by step, following the elite-solver pipeline. Let me begin by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good! I can see:
- **UD axis**: 4 bad edges (UL, DR, DL, DB) — promising for EO
- **FB axis**: 8 bad edges — typical all-bad case
- **RL axis**: 6 bad edges
- **DR labels**: UD is DR-7C3E (not ideal), FB is DR-6C3E, RL is DR-5C3E
- **Key signal**: `top_pairs_on_inverse: 3` on UD axis — this is a strong NISS signal!

Now let me run niss_scout to get the full 6-row comparison table (normal × inverse × 3 axes) and see which path has the best expected_total_to_solved.

I scout EO+DR on both normal and inverse, all three axes — 1 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The niss_scout table shows:
- **Top row**: **inverse-RL axis** with EO 5mv + DR-3C2E trigger (total 8mv to DR = 13 total) — this is the winner!
- All other rows either have no DR triggers within max_setup=5 (meaning DR would be ≥10 moves, which is a red flag per the hard rule).
- The DR-3C2E trigger is much better than DR-4C4E or DR-7C3E for HTR finish.

**Decision**: I'll take the **inverse-RL** path. The EO is 5 moves, DR is 8 moves (setup 5 + trigger 3), giving 13 total to DR. The DR-3C2E substate finishes efficiently.

Let me flip to inverse and apply the EO.

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. Let me apply the 5-move EO for RL axis: **B' L' D' L2 U'**

I turn `B' L' D' L2 U'`.

EO applied (5 moves on inverse). Now I need to find the DR on RL axis. The scout said there's a DR-3C2E trigger with 5-move setup. Let me use dr_trigger_options to see the menu.

I survey the named DR triggers on RL:
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)
  • DR-3C2E (F L F'): 6-mv setup + 3-mv trigger (9 total)
  • DR-7C8E (F L B): 6-mv setup + 3-mv trigger (9 total)

Perfect! The menu shows:
1. **DR-3C2E (F L' F')**: setup 5mv, trigger 3mv, total 8mv to DR — this matches the scout's recommendation
2. DR-3C2E (F L F'): 9mv total
3. DR-7C8E (F L B): 9mv total

I'll take option 1: **U2 F' D2 F R'** (setup) + **F L' F'** (trigger) = 8 moves to DR.

I turn `U2 F' D2 F R'`.

I turn `F L' F'`.

DR reached in 13 moves (5 EO + 8 DR). Now let me verify I'm in DR and classify the HTR subset for RL axis.

Quick check: DR-locked on RL, not yet HTR.

Perfect! DR is confirmed on RL axis. Now let me classify the HTR subset to understand what I'm dealing with.

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 8 moves, finish is 10 moves (recall).

The HTR subset is **0-swap long-cycle** with cycle structure [4, 2, 1, 1]. The finish will be:
- HTR reduction: 8 moves
- Finish: 10 moves
- Total from DR: 18 moves

Current total: **13 (to DR) + 18 (HTR+finish) = 31 moves**

This is reasonable but let me proceed through HTR. I'll apply the reduction phase first, checking for early residuals.

For the corner reduction, I see `R' D2 R2 B2` (chunk of a 8-move phase) — apply and re-check.

HTR reduction is 8 moves total, showing me the first 4. Let me apply them and check the state.

I turn `R' D2 R2 B2`.

Quick check: DR-locked on RL, not yet HTR.

Not solved yet, still in DR. Let me get the remaining 4 moves of HTR reduction.

For the corner reduction: `U2 F2 D2 L`.

I turn `U2 F2 D2 L`.

Quick check: in HTR.

Excellent! I'm now in HTR (is_htr_ud: true). 21 moves so far. Now let me apply the finish phase (10 moves).

For the half-turn finish, I see `B2 U2 B2 L2` (chunk of a 10-move phase) — apply and re-check.

I turn `B2 U2 B2 L2`.

Quick check: in HTR.

Still in HTR, not solved yet. Let me check if this might be a corner 3-cycle before continuing with the remaining 6 moves.

Residual class: mixed.

Not a pure 3-cycle — it's a mixed state with multiple corner and edge cycles. Let me continue with the finish phase.

For the half-turn finish, I see `D2 L2 F2 L2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 L2 F2 L2`.

Quick check: in HTR.

Still not solved. Let me get the remaining moves.

For the half-turn finish: `U2 B2`.

I turn `U2 B2`.

A quick glance — the cube is solved.

Excellent! The cube is **solved** in 31 moves on the inverse frame. Now I need to compose the final solution using compose_niss_solution, which will invert my inverse-frame moves and apply cancellations.

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Great! The solution is **30 moves** after cancellation. Let me verify this solution is correct.

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. Let me check my budget status to see if I should attempt replace_and_shorten.

Budget check: 3512.0s sim, None tool calls remaining.

I have plenty of time remaining (3512s simulated, ~88s spent). The solution is 30 moves and verified. According to the rules, I should NOT attempt replace_and_shorten unless the solution is ≥27 moves AND I have ≥30 tool calls remaining. Let me count my tool calls so far:

1. inspect_state
2. niss_scout
3. niss_flip
4. apply_moves (EO)
5. dr_trigger_options
6. apply_moves (DR setup)
7. apply_moves (DR trigger)
8. quick_check
9. htr_classify
10. apply_htr_phase (reduction chunk 1)
11. apply_moves
12. quick_check
13. apply_htr_phase (reduction chunk 2)
14. apply_moves
15. quick_check
16. apply_htr_phase (finish chunk 1)
17. apply_moves
18. quick_check
19. analyze_residual
20. apply_htr_phase (finish chunk 2)
21. apply_moves
22. quick_check
23. apply_htr_phase (finish chunk 3)
24. apply_moves
25. quick_check
26. compose_niss_solution
27. verify_solved
28. budget_status

That's 28 tool calls. I have ≥30 remaining (estimating ~50-60 total available). The solution is 30 moves (≥27). So I should attempt replace_and_shorten on a large span to potentially save moves.

Let me try replace_and_shorten on a tail span. I'll target moves 4-31 (the DR+HTR+finish portion), leaving the first few EO moves intact.

replace_and_shorten: substitute is 6 moves longer; reject.

The replace_and_shorten attempt actually made the solution longer (delta +6, from 27 to 33 in that span). This is not an improvement. I should keep my original 30-move solution.

Since my current verified solution is 30 moves and replace_and_shorten didn't help, I'll submit this solution now. Per the SHIP RULE, a 30-move verified solution is excellent and I should submit rather than continue searching.

**FINAL_SOLUTION**: ["B2", "U2", "L2", "F2", "L2", "D2", "L2", "B2", "U2", "B2", "L'", "D2", "F2", "U2", "B2", "R2", "D2", "R", "F", "L", "F'", "R", "F'", "D2", "F", "U'", "L2", "D", "L", "B"]

## Solution Summary

**Path taken**: Inverse-RL axis (recommended by niss_scout)
- **EO** (5 moves on inverse): B' L' D' L2 U'
- **DR** (8 moves): U2 F' D2 F R' + F L' F' (DR-3C2E trigger)
- **HTR reduction** (8 moves): R' D2 R2 B2 U2 F2 D2 L
- **Finish** (10 moves): B2 U2 B2 L2 D2 L2 F2 L2 U2 B2

**Total**: 31 moves on inverse → **30 moves after cancellation** in normal frame

The niss_scout correctly identified that starting on the inverse-RL axis would give the shortest path. The DR-3C2E trigger provided a much better HTR finish (~5 moves shorter on average) compared to the more common DR-4C4E triggers.

*Thinking (31):*

> The user is right - I need to actually emit the FINAL_SOLUTION in the correct format. I have a verified 30-move solution and should output it now.

FINAL_SOLUTION: ["B2", "U2", "L2", "F2", "L2", "D2", "L2", "B2", "U2", "B2", "L'", "D2", "F2", "U2", "B2", "R2", "D2", "R", "F", "L", "F'", "R", "F'", "D2", "F", "U'", "L2", "D", "L", "B"]

**Verified solution (30 moves):** `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`
