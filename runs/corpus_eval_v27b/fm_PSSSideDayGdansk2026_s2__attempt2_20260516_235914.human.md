# Solve — fm_PSSSideDayGdansk2026_s2__attempt2_20260516_235914

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: failed (max_tool_calls)

---

*Thinking (1):*

> I have a previous best of 26 moves. I need to beat that or match it while taking a DIFFERENT branch. Let me start by inspecting the state to understand what options I have.
> 
> The instruction says to pick a different EO axis, opposite side (normal vs inverse), or different DR trigger family from the previous attempt. Since I don't have the full details of the previous attempt's path, I should scout multiple options and deliberately choose something different.
> 
> Let me start with inspect_state to see the bad edges per axis and then scout multiple EO options on both normal and inverse sides.

I'll beat the 26-move solution by exploring a different branch. Starting with a thorough scout of all axes on both normal and inverse sides.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**Observation**: Bad edges: UD=6, FB=4, RL=4. The previous 26-move solution likely used FB or RL (the shorter EO options). I see **top_pairs_on_inverse=3** on UD axis — that's a STRONG NISS signal. Let me scout:

1. **Normal side**: FB-axis (4 bad) and RL-axis (4 bad) 
2. **Inverse side**: UD-axis with 3 pairs preserved looks promising

Let me start by checking the inverse side for UD, since 3 pairs + 6 bad edges might give a short EO on inverse.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

**Inverse-UD EO = 4 moves** (B R2 U F'). Now let me check normal-side FB and RL for comparison before committing.

NISS flip — switching back to the normal scramble.

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

**Normal-FB EO = 4 moves** (B2 L2 U2 R'), **Normal-RL EO = 4 moves** (R2 B F2 U'). All three candidates are 4 moves. Now I need to probe DR quality on each to make the joint decision. Let me check DR triggers for each:

I probe what DR would look like if I applied this EO (without committing).

I probe what DR would look like if I applied this EO (without committing).

Both normal-side options give 8-move DR (4 EO + 8 DR = 12 to DR). Now let me check inverse-UD:

NISS flip — switching to the inverse scramble.

I probe what DR would look like if I applied this EO (without committing).

All three options give **4 EO + 8 DR = 12 to DR**. Since the previous 26-move solution likely used one of these, let me commit to **inverse-UD** (4 EO on inverse + 8 DR) because of the 3 pairs on inverse signal. This is a different branch. Let me apply the EO and then get detailed DR trigger options.

I turn `B R2 U F'`.

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 6-mv setup + 3-mv trigger (9 total) [JZP]
  • DR-3C2E (R U' R'): 6-mv setup + 3-mv trigger (9 total)

**Excellent!** Two 9-move DR options (6 setup + 3 trigger):
- **DR-4C2E (R U2 R')** — JZP-eligible! This is gold.
- **DR-3C2E (R U' R')** — not JZP but still a good substate.

Taking the **JZP-eligible DR-4C2E** path. Total so far: 4 EO + 9 DR = 13 moves to DR. Let me apply the setup + trigger separately for clear narration:

I turn `R2 U' D2 L' U' L2`.

I turn `R U2 R'`.

Quick check: DR-locked on UD, not yet HTR.

**DR achieved on UD axis!** 13 moves on inverse. Now for HTR classification:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 11 moves (first exposure — learning).

**2-swap long-cycle subset**: 11 HTR-reduction + 11 finish = 22 moves from DR. Total would be 13 DR + 22 HTR/finish = **35 moves** — that's worse than my 26-move target. This JZP path didn't pay off. Let me backtrack and try the normal-side branches.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `B2 L2 U2 R'`.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

No DR triggers found within 6 moves on FB axis after this EO! That's a bad sign. Let me try the RL-axis normal path:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B F2 U'`.

I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total)
  • DR-7C8E (F L B): 6-mv setup + 3-mv trigger (9 total)

**RL axis**: DR-7C8E trigger in 8 moves total (5 setup + 3 trigger). That's 4 EO + 8 DR = 12 to DR. DR-7C8E is a complex substate but let me try it. This is definitely a different branch from the previous attempt.

I turn `R B' D2 R' B'`.

I turn `F' L B`.

Quick check: DR-locked on RL, not yet HTR.

**DR achieved on RL axis** in 12 moves! Now HTR classification:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 12 moves (first exposure — learning).

**Another 2-swap long-cycle**: 11 + 12 = 23 moves from DR. Total = 12 + 23 = **35 moves** again. Still too long. Let me try a completely different approach — maybe exploring other EO options or checking if there's a shorter EO I missed. Let me go back and try 2-3 move EO options by manual exploration.

Budget check: 3419.0s sim, None tool calls remaining.

I have plenty of time. Let me try a completely different approach: check if there are shorter EO options I'm missing by using brain_suggest and policy_intuition from the scramble.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

My trained intuition for eo: top candidates are R2 (94%), L2 (4%), D' (1%).

**Brain strongly suggests R2** (93.6% prob). Let me try that and see where it leads:

I try `R2` on top to see the after-state (without committing).

R2 doesn't help — still 6/4/4 bad edges. Let me try a different strategy: look for 2-3 move EO combinations manually. Let me check if there's a 2-move EO by trying common pairs:

I try `F B` on top to see the after-state (without committing).

Still 6/4/4. Let me go back to the 26-move solution path and think differently. The previous solution was 26 moves. Let me try to explore if there's a 3-move EO somewhere. Let me check what the lookahead tool suggests for EO:

I look 4 moves ahead with a small beam.

I look 4 moves ahead with a small beam.

I look 4 moves ahead with a small beam.

No EO within 4 moves on any axis from scramble directly. The 4-move EOs I found earlier are indeed optimal from the scramble. Let me reconsider: maybe the issue is that I need to find a BETTER HTR finish after DR, not a better DR. Let me go back to the best DR I had (12 moves on RL-axis with DR-7C8E) and try to work through the HTR more carefully with opportunistic 3-cycle checks:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B F2 U' R B' D2 R' B' F' L B`.

Now let me apply HTR-reduction with inter-phase quick_checks:

For the corner reduction, I see `B2 R U2 R` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 R U2 R`.

Quick check: DR-locked on RL, not yet HTR.

Not solved yet. Continue HTR-reduction:

For the corner reduction, I see `F2 R2 B2 D2` (chunk of a 7-move phase) — apply and re-check.

I turn `F2 R2 B2 D2`.

Quick check: DR-locked on RL, not yet HTR.

Continue:

For the corner reduction: `R F2 R`.

I turn `R F2 R`.

Quick check: in HTR.

**HTR reached!** Now the finish phase:

For the half-turn finish, I see `U2 B2 R2 D2` (chunk of a 12-move phase) — apply and re-check.

I turn `U2 B2 R2 D2`.

Quick check: in HTR.

27 moves and still not solved. Let me check if there's a 3-cycle residual:

Residual class: mixed.

Complex residual with 8 corners and 10 edges unsolved. Continue with finish:

For the half-turn finish, I see `F2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U2 F2 U2`.

Quick check: in HTR.

31 moves, still not solved. Continue:

For the half-turn finish: `L2 D2 R2 U2`.

I turn `L2 D2 R2 U2`.

A quick glance — the cube is solved.

**SOLVED!** 35 moves. But that's worse than the 26-move target. Let me try cancellation:

I assemble the canonical normal-frame solution: **34 moves**, verified.

34 moves after cancellation. Still worse than 26. I need a different strategy. Let me try exploring other DR options more aggressively. Let me check if there's a better path on inverse-UD with the non-JZP DR-3C2E trigger:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B R2 U F'`.

I turn `B2 U2 D2 L' F2 L2`.

I turn `R U' R'`.

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 8 moves, finish is 10 moves (first exposure — learning).

**Much better!** DR-3C2E gives a "2-swap mostly-axial" subset: 8 + 10 = 18 moves from DR. Total = 13 + 18 = **31 moves**. Still not beating 26. Let me complete this and see if there are good cancellations or residual shortcuts:

For the corner reduction, I see `F2 U' L2 U` (chunk of a 8-move phase) — apply and re-check.

I turn `F2 U' L2 U`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `R2 U' B2 D`.

I turn `R2 U' B2 D`.

Quick check: in HTR.

HTR reached in 21 moves. Now finish:

For the half-turn finish, I see `F2 L2 F2 L2` (chunk of a 10-move phase) — apply and re-check.

I turn `F2 L2 F2 L2`.

Quick check: in HTR.

Let me check if it's a 3-cycle now:

Residual class: mixed.

Complex residual. Continue:

For the half-turn finish, I see `U2 B2 R2 D2` (chunk of a 6-move phase) — apply and re-check.

I turn `U2 B2 R2 D2`.

Quick check: in HTR.

For the half-turn finish: `R2 D2`.

I turn `R2 D2`.

A quick glance — the cube is solved.

Solved in 31 moves on inverse! Let me compose and see if there are good cancellations:

I assemble the canonical inverse-frame solution: **31 moves**, verified.

31 moves — still worse than 26. I'm not making progress. Let me think: the previous 26-move solution must have found a significantly better path. Maybe I need to try 3-move EO options or look at completely different angles. Let me try exploring if there are any 3-move EO options by checking shorter setups manually:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.
