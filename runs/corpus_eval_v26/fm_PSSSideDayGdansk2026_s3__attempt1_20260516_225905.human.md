# Solve — fm_PSSSideDayGdansk2026_s3__attempt1_20260516_225905

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 29 moves
**Solution**: `U2 R2 F2 D2 F2 U2 B2 R2 B2 D2 L B2 R' B2 D2 U2 R' F R' F2 U2 R' B2 L2 U' L2 D L B`

---

*Thinking (1):*

> The user wants me to solve the scramble. Let me start by inspecting the state of the main slot to see what we're working with.
> 
> The scramble is: R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> I need to follow the pipeline:
> 1. Inspect state
> 2. Use niss_scout to check both normal and inverse frames across all axes
> 3. Pick the best EO+DR combination
> 4. Execute EO
> 5. Execute DR
> 6. HTR classify and finish
> 7. Verify and submit
> 
> Let me start with inspect_state.

I'll solve this FMC scramble systematically. Let me begin by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good. **State observation**: UD has 4 bad edges (strongest EO candidate), FB has 8 bad (all-bad case), RL has 6 bad. DR-closeness shows 7C3E/6C3E/5C3E — all poor DR states, but UD has **3 pairs on inverse** (strong NISS signal). The 4 bad edges on UD are scattered: UL, DR, DL, DB — not all on one flipping face, so this won't be a 1-move EO.

Now I'll use **niss_scout** to get the full 6-row comparison table (normal × inverse × 3 axes) and let it recommend the best starting direction.

I scout EO+DR on both normal and inverse, all three axes — 1 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

**Scout analysis**: All normal-side options show "no DR triggers within max_setup=5" — this is a bad sign. The **inverse-RL** row shows a DR-3C2E option at 13 total moves (5 EO + 8 DR), but 13 is already long. The normal-side UD/FB both have 4-move EOs but no visible DR.

This is troubling — the scout didn't find good DR options on any axis/side. **This signals I need to probe more carefully**. Let me pick the normal-UD 4-move EO (shortest EO) and manually explore DR with dr_trigger_options, which has a wider search than the scout's max_setup=5 gate.

Starting on **normal-UD** with EO: U L R' B'.

I turn `U L R' B'`.

EO applied. Now let me query **dr_trigger_options** on UD to see the full ranked menu of DR options from this EO state.

I survey the named DR triggers on UD:
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

**DR options on UD**: Only one option found — a DR-7C8E trigger in 9 total moves (6 setup + 3 trigger). That's already 4 EO + 9 DR = **13 moves to DR**, which is borderline too long (elite solves average sub-11 DR). The 7C8E trigger is rare and generally leads to long HTR finishes.

Let me check the **FB axis** DR options from the same starting point, since FB also had a 4-move EO on normal.

I rewind 4 moves.

I turn `R' F D L'`.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

**FB axis**: No DR triggers found within 6-move setup. This is worse than UD.

Let me try the **inverse-RL** option that the scout found (5 EO + 8 DR = 13 total, with a DR-3C2E trigger). DR-3C2E is a good substate — much better finish than 7C8E. Let me switch to inverse and test it.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

Now on inverse. Applying the RL-axis EO: B' L' D' L2 U'.

I turn `B' L' D' L2 U'`.

I check whether the DR is recognizable from this state via the library.

Applying the 4-move setup progress toward DR.

I turn `U2 L2 B2 R`.

I check whether the DR is recognizable from this state via the library.

Excellent! **From the current state**, DR is only 4 more moves: setup U2 F2 R, trigger F'. That puts us at **5 EO + 9 setup + 4 DR = 18 total** — wait, let me recalculate. Current history is 9 moves (5 EO + 4 setup-progress). The next 4 moves (3 setup + 1 trigger) complete DR. So total to DR is **13 moves**, which matches the scout's prediction.

Let me apply the setup and trigger.

I turn `U2 F2 R`.

I turn `F'`.

**DR reached in 13 moves** on inverse-RL. Now let me classify the HTR subset and finish.

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 7 moves, finish is 11 moves (first exposure — learning).

**HTR subset**: "2-swap long-cycle" with 7-move reduction + 11-move finish = **18 moves** from DR to solved. Total would be 13 + 18 = **31 moves**.

That's acceptable but long. Let me apply the HTR phases and check for early residuals with quick_check.

For the corner reduction, I see `R U2 D2 B2` (chunk of a 7-move phase) — apply and re-check.

I turn `R U2 D2 B2`.

Quick check: DR-locked on RL, not yet HTR.

Not solved yet. Continuing HTR reduction.

For the corner reduction: `R B2 L`.

I turn `R B2 L`.

Quick check: in HTR.

Good! HTR-UD reached. Now the finish phase.

For the half-turn finish, I see `L2 D2 B2 R2` (chunk of a 11-move phase) — apply and re-check.

I turn `L2 D2 B2 R2`.

Quick check: in HTR.

Still not solved. Let me check if this might be a 3-cycle residual.

Residual class: mixed.

**Mixed residual** with 2 corner swaps + 2 edge 3-cycles. Not a clean insertable state. I'll continue the finish.

For the half-turn finish, I see `B2 U2 F2 D2` (chunk of a 7-move phase) — apply and re-check.

I turn `B2 U2 F2 D2`.

Quick check: in HTR.

Residual class: mixed.

The residual is getting worse (more pieces unsolved). Let me continue the finish sequence.

For the half-turn finish: `F2 R2 U2`.

I turn `F2 R2 U2`.

A quick glance — the cube is solved.

**SOLVED!** The cube is solved in **31 moves** on the inverse frame. Now I need to use compose_niss_solution to assemble the canonical normal-frame solution (it will invert the moves and cancel).

I assemble the canonical inverse-frame solution: **29 moves**, verified.

Excellent! **After cancellation, the solution is 29 moves**. That's within acceptable range. Let me verify it solves the scramble.

verify_solved: ✓ — 29 moves.

Perfect! The solution verifies. Let me check if I have budget for replace_and_shorten to try to optimize further.

Budget check: 3440.0s sim, None tool calls remaining.

I have plenty of budget remaining (3440s sim, ~1355s wall). Since the solution is ≥27 moves and I haven't called replace_and_shorten yet, let me try it on a large span to see if I can reduce the length further. I'll target the middle/end span where the HTR finish happened.

replace_and_shorten: substitute is 6 moves longer; reject.

**replace_and_shorten made it worse** (delta +6), so I'll keep my original 29-move solution. The tool has used its 1-call cap, so I can't try again. 

My final verified solution is **29 moves**.

**FINAL_SOLUTION**: ["U2", "R2", "F2", "D2", "F2", "U2", "B2", "R2", "B2", "D2", "L", "B2", "R'", "B2", "D2", "U2", "R'", "F", "R'", "F2", "U2", "R'", "B2", "L2", "U'", "L2", "D", "L", "B"]

## Solution Summary

**Approach**: Inverse-RL axis
- **EO** (5 moves): B' L' D' L2 U' on inverse-RL
- **DR** (8 moves): Setup and single-inverse trigger reached DR in 13 total
- **HTR** (7 moves reduction + 11 moves finish): "2-swap long-cycle" subset
- **Total**: 31 moves on inverse → 29 moves after NISS inversion and cancellation

The scramble presented a difficult case with no good DR triggers on the normal side. Switching to the inverse-RL frame enabled a cleaner path to DR via a DR-3C2E-like trigger pattern, though the total DR length of 13 moves was still on the long side for elite standards. The HTR finish was lengthy (18 moves) due to the "2-swap long-cycle" subset, but the solve completed successfully at 29 moves.

*Thinking (39):*

> The user is right - I narrated the solution but didn't formally emit it. I have a verified 29-move solution and I should output it in the required format.
> 
> Let me emit the FINAL_SOLUTION now.

FINAL_SOLUTION: ["U2", "R2", "F2", "D2", "F2", "U2", "B2", "R2", "B2", "D2", "L", "B2", "R'", "B2", "D2", "U2", "R'", "F", "R'", "F2", "U2", "R'", "B2", "L2", "U'", "L2", "D", "L", "B"]

**Verified solution (29 moves):** `U2 R2 F2 D2 F2 U2 B2 R2 B2 D2 L B2 R' B2 D2 U2 R' F R' F2 U2 R' B2 L2 U' L2 D L B`
