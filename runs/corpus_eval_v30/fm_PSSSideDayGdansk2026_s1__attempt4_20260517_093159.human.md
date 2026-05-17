# Solve — fm_PSSSideDayGdansk2026_s1__attempt4_20260517_093159

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 29 moves
**Solution**: `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 D U F R L D B`

---

*Thinking (1):*

> The user wants me to solve this scramble. Prior attempts got 25 moves (twice) and 31 moves. The best is 25 moves. 
> 
> Let me look at the prior 25-move solution:
> `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`
> 
> This is quite good already - 25 moves is solid for FMC. The instructions say to COMMIT HARD this attempt and not over-ideate. I should pick a line and drive it through.
> 
> Let me start by inspecting the state to see what we're working with, then make a committed choice based on the state and what the prior attempts suggest was promising.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> Let me start with inspect_state to see the bad edges per axis and make an informed decision about which axis to pursue.

I'll solve this scramble with full commitment to a single line. The prior attempts achieved 25 moves twice, which is strong. Let me start by inspecting the state to understand the landscape.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Good! I see 8 bad edges on UD, 6 on FB, 6 on RL. Notice `top_pairs_on_inverse: 2` on UD — that's a strong NISS signal. Also, FB shows DR-5C2E which could be promising. Let me check both the normal and inverse perspectives systematically.

**EO candidates to scout:**
- FB: 6 bad edges (might be 2-3 moves)
- RL: 6 bad edges (might be 2-3 moves)
- UD on inverse: has 2 pairs preserved, worth checking

Let me start by scouting FB-axis EO on normal, then check inverse UD.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

FB-EO is 5 moves total (4+1 more). Let me check RL now.

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

RL-EO is also 5 moves. Now let me check inverse — with 2 pairs preserved and UD having 8 bad edges, inverse might flip this to a much better configuration.

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check UD-axis EO here.

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

Inverse UD-EO is also 5 moves. Let me also check inverse FB and RL quickly.

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

**All EO options are 5 moves.** This is unusual — typically there's differentiation. Since all EO lengths are equal, I need to compare based on DR substates. The prior 25-move solutions likely found a good axis. Let me flip back to normal and probe DR patterns systematically.

Given the symmetry, let me commit to **normal-side FB axis** (which showed DR-5C2E — a decent substate). I'll apply the FB-EO and then check DR options.

NISS flip — switching back to the normal scramble.

Back to normal. Let me commit to FB-axis and apply the first chunk of EO, then probe DR.

I turn `R2 B' L' U2`.

Now let me get the final EO move.

On FB axis I recognize the EO pattern — `R'` fixes it.

Perfect! Just R' completes FB-EO. Total: 5 moves (R2 B' L' U2 R'). Let me apply it.

I turn `R'`.

FB-EO complete in 5 moves. Now let me check DR options on FB axis using dr_trigger_options.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

No DR triggers found within 5-move setup on FB axis. Let me try increasing to 6 moves.

I survey the named DR triggers on FB:
  • DR-3C2E (U F' U'): 6-mv setup + 3-mv trigger (9 total)

Found DR-3C2E in 9 moves total (6 setup + 3 trigger). That's 5 EO + 9 DR = 14 moves to DR. DR-3C2E typically finishes in 6-8 moves, so total ~20-22 moves. This could be viable.

But before committing, let me check if the other axes (UD or RL) might have better DR options even with the same 5-move EO. Let me reset and try RL-axis.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me try RL-axis EO and check its DR options.

I turn `L U L2 R`.

On RL axis I recognize the EO pattern — `D'` fixes it.

I turn `D'`.

RL-EO complete in 5 moves (L U L2 R D'). Now check DR options on RL axis.

I survey the named DR triggers on RL:
  • DR-7C8E (F L B): 6-mv setup + 3-mv trigger (9 total)

DR-7C8E in 9 moves — that's a terrible substate (7 misoriented corners, 8 misplaced edges). This will finish in 14+ moves. Not good.

Let me check normal UD-axis now, even though it had 8 bad edges initially. Maybe after flipping to inverse twice we have better options. Let me reset and check if there's a shorter path I'm missing.

Actually, wait — I should reconsider. The prior 25-move solutions likely found something better. Let me think: they used a very different structure. Looking at that solution: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`

This looks like it might have used inverse + a different approach. Let me try checking the inverse side more carefully. Let me reset and go to inverse UD.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

On inverse. Let me apply inverse UD-EO and check DR options there.

I turn `B' D' L' R'`.

On UD axis I recognize the EO pattern — `F'` fixes it.

I turn `F'`.

Inverse UD-EO in 5 moves (B' D' L' R' F'). Now check DR on UD axis.

I survey the named DR triggers on UD:
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)
  • DR-7C8E (R' U L): 6-mv setup + 3-mv trigger (9 total)
  • DR-3C2E (R U R'): 6-mv setup + 3-mv trigger (9 total)

Interesting! Several options here:
- DR-7C8E options in 9 moves (bad substates)
- **DR-3C2E in 9 moves** (U' D' F2 U' F2 L + R U R') — good substate, should finish in 6-8 moves
- **DR-4C4E in 10 moves with JZP** (D L U2 B2 R' D' + R U2 F2 R) — JZP halves post-DR cost, so ~7-9 move finish

The JZP option is interesting. 5 EO + 10 DR = 15 moves to DR, finishing in ~7-9 = **22-24 moves total**. 
The DR-3C2E: 5 EO + 9 DR = 14 to DR, finishing in ~6-8 = **20-22 moves total**.

Both look competitive! Let me commit to the **DR-3C2E path** since it's slightly shorter expected total. That's 5 EO + 9 DR = 14 moves to reach DR.

I turn `U' D' F2 U' F2 L`.

I turn `R U R'`.

DR reached in 14 moves (on inverse side). Now let me classify the HTR substate and finish.

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 5 moves, finish is 11 moves (first exposure — learning).

HTR-classify shows: 5-move reduction + 11-move finish = 16 moves from DR to solved. Total: 14 DR + 16 finish = **30 moves**. That's worse than the prior 25-move best.

Let me check if there's a 3-cycle residual opportunity by applying just the reduction and checking.

For the corner reduction, I see `R2 B2 U' F2` (chunk of a 5-move phase) — apply and re-check.

I turn `R2 B2 U' F2`.

Notice auto-cancelled 1 move (R R' → nothing, plus other cancellations). Let me check state.

Quick check: DR-locked on UD, not yet HTR.

Not at HTR yet. Let me get the last move of HTR reduction.

For the corner reduction: `D`.

I turn `D`.

Quick check: in HTR.

At HTR now (18 moves). Let me check for residual.

Residual class: mixed.

Mixed residual (4 corners, 7 edges). Not a pure 3-cycle. Let me continue with the finish phase.

For the half-turn finish, I see `B2 L2 D2 L2` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 L2 D2 L2`.

Quick check: in HTR.

Still at HTR, not solved. Continue finish.

For the half-turn finish, I see `D2 B2 R2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `D2 B2 R2 U2`.

Quick check: in HTR.

For the half-turn finish: `F2 U2 R2`.

I turn `F2 U2 R2`.

A quick glance — the cube is solved.

Solved! 29 moves on the inverse side. Now I need to compose the NISS solution properly to get the normal-frame solution.

I assemble the canonical inverse-frame solution: **29 moves**, verified.

Got a 29-move solution! That's 4 moves longer than the best 25-move prior solution, but it's complete and verified.

Given that I have a complete 29-move solution and the prior best was 25, let me check if replace_and_shorten can help. I have plenty of tool calls remaining (budget_status will confirm). The instructions say to use r&s if total ≥27 AND tool calls ≥30 remaining. Let me check budget.

Budget check: 3401.0s sim, None tool calls remaining.

Good! I have 3401s remaining and 29 moves. The gates pass (29 ≥ 27, and I have way more than 30 tool calls remaining). Let me try replace_and_shorten on a large span to see if I can improve.

Looking at the solution: `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 D U F R L D B`

The tail (from move ~4 onward) is where DR and HTR happened. Let me try r&s on roughly the DR-to-finish span, say from move 4 to the end (move 29).

replace_and_shorten: substitute is 6 moves longer; reject.

Replace_and_shorten made it WORSE (delta +6, from 29 to 35 moves). That's not helpful. The original 29-move solution is better. Per the instructions, r&s has a 1-call cap, so I can't try again.

My current best solution is 29 moves. This is 4 moves longer than the prior 25-move best. However, I've committed to this path and have a working solution. The instructions emphasize SHIP RULE: a verified solve beats a DNF.

But let me reconsider — do I have time to try a different axis? I still have 3300+ seconds. The prior 25-move solution likely used a different approach. Let me try one more reset and explore the JZP option on inverse UD, which had a 10-move DR but JZP-eligible with expected ~7-9 move finish.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me go back to inverse UD and try the JZP path (DR-4C4E in 10 moves with JZP).

NISS flip — switching to the inverse scramble.

I turn `B' D' L' R' F'`.

EO done (5 moves). Now let me apply the JZP DR path: D L U2 B2 R' D' + R U2 F2 R.

I turn `D L U2 B2 R' D'`.

I turn `R U2 F2 R`.

DR reached in 15 moves (5 EO + 10 DR) with JZP. Let me classify HTR.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 8 moves, finish is 12 moves (first exposure — learning).

HTR shows 8-move reduction + 12-move finish = 20 moves. Total: 15 DR + 20 finish = **35 moves**! That's WORSE than my 29-move solution. The JZP didn't help as much as expected.

The non-JZP DR-3C2E path I tried first gave 29 moves, which is better. Let me go back and submit that 29-move solution. It's 4 moves longer than the prior 25-move best, but it's a complete verified solve.

Actually, wait — let me reconsider. I should try to understand what the prior 25-move solution did differently. Looking at it: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`

This has a lot of double-turn moves, suggesting it might have used a different EO axis or found a much better DR. The structure suggests maybe they used normal side, not inverse. Let me try one more approach: normal-side UD axis using inverse techniques. But wait, the instructions say COMMIT HARD and don't over-ideate. I already have a 29-move solution.

Per the SHIP RULE: I have a verified 29-move solve. It's worse than the 25-move best but still solid (sub-30 is good). The instructions emphasize that a working solution beats timeout. Let me submit the 29-move solution.

**FINAL_SOLUTION:** R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 D U F R L D B

Wait, let me verify this solution one more time to be absolutely sure.

verify_solved: ✓ — 29 moves.

Verified! 29 moves, solves the scramble.

**FINAL_SOLUTION:** ["R2", "U2", "F2", "U2", "R2", "B2", "D2", "L2", "D2", "L2", "B2", "D'", "F2", "U", "B2", "R'", "U'", "R'", "L'", "F2", "U", "F2", "D", "U", "F", "R", "L", "D", "B"]

*Thinking (55):*

> The user is right - I need to actually emit the final solution. I verified it and it works (29 moves), so I should submit it now.

FINAL_SOLUTION: ["R2", "U2", "F2", "U2", "R2", "B2", "D2", "L2", "D2", "L2", "B2", "D'", "F2", "U", "B2", "R'", "U'", "R'", "L'", "F2", "U", "F2", "D", "U", "F", "R", "L", "D", "B"]

**Verified solution (29 moves):** `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 D U F R L D B`
