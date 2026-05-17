# Solve — fm_PSSSideDayGdansk2026_s1__attempt1_20260516_223733

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 28 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 R2 U B2 U' F2 L2 U' L2 U F2 R2`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble. Let me start by inspecting the state of the main slot to understand what I'm working with.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I'll start with inspect_state to see the bad edges per axis, DR closeness, HTR closeness, etc.

I'll solve this FMC scramble systematically. Let me begin by inspecting the cube state to understand what I'm working with.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Good. I can see the scramble state:
- **UD axis**: 8 bad edges, DR-6C3E, 2 pairs on inverse (NISS signal)
- **FB axis**: 6 bad edges, DR-5C2E
- **RL axis**: 6 bad edges, DR-7C3E

Following the v16 protocol, I should now call **niss_scout** to get the full 6-row comparison table (normal × inverse × 3 axes) before committing to any EO axis. This is the mandatory first step for elite solvers.

I scout EO+DR on both normal and inverse, all three axes — 5 viable rows.
  • normal-UD: EO 4mv → DR-4C2E (R U2 R') DR (8mv) [JZP]
  • normal-UD: EO 4mv → DR-7C8E (R' U L) DR (8mv)
  • inverse-FB: EO 5mv → DR-7C8E (U F D) DR (7mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The NISS-scout gave me the full picture. Let me analyze:

**Top candidates**:
1. **UD-normal** (row 1): EO 4mv + DR-4C2E 8mv → **total 33mv to solved (CACHED)**. JZP-eligible! This is the winner.
2. UD-normal (row 2): Same EO + DR-7C8E → also 33mv but DR-7C8E is worse structure.
3. FB-inverse: EO 5mv + DR-7C8E 7mv → 12 total to DR, but no cached finish (uncached subset).
4. FB-normal/RL-normal/others: no DR triggers within max_setup=5 or longer.

**Decision**: Row 1 (UD-normal, JZP-eligible) is the clear winner. The JZP flag means even the "bad" 4C2E case should finish clean. Total cached at 33 moves, which beats any uncached option. I'll commit to **UD-axis EO on normal frame**.

Let me apply the EO moves: R2 D' B' F'

I turn `R2 D' B' F'`.

Good, EO applied (4 moves). Now I need to get to DR. The scout said the best DR option is **DR-4C2E (R U2 R')** with 5 moves setup + 3 moves trigger = 8 total to DR. Let me call dr_trigger_options to get the detailed setup and trigger moves:

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

Perfect! The dr_trigger_options confirms:
- **Option 1 (DR-4C2E)**: setup U' R' L2 U F2, then trigger R U2 R'. Total 8 moves, **JZP-eligible**. This matches the scout's recommendation.
- Option 2 (DR-7C8E): same 8 moves but worse structure (7C8E).

I'll take Option 1. Applying setup moves first:

I turn `U' R' L2 U F2`.

Setup applied (5 moves). Now the DR-4C2E trigger: R U2 R'

I turn `R U2 R'`.

Excellent! I've reached DR in 12 moves (EO 4 + DR 8). The scout said this DR state finishes in 21 more moves for a total of 33. Let me verify I'm at DR and check the HTR state:

Quick check: DR-locked on UD, not yet HTR.

Perfect! DR on UD is confirmed. Now I need to classify the HTR subset and finish. Let me call htr_classify:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (first exposure — learning).

Interesting! The HTR classifier reports:
- **Subset**: 0-swap long-cycle (cycle structure 3,2,2,1)
- **HTR reduction**: 10 moves
- **Finish**: 9 moves
- **Total**: 19 moves (not the 21 the scout predicted, but close)

This gives me a total of 12 (EO+DR) + 19 (HTR+finish) = **31 moves**, which is better than the scout's 33!

Let me apply the HTR reduction phase:

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

The HTR reduction is partial (10 moves total, showing first 4). Let me apply this chunk and check if we've reached a useful residual:

I turn `U F2 U' R2`.

Applied 4 moves of HTR reduction (16 total). Let me check the state with quick_check before continuing:

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR. Let me continue with the next chunk of HTR reduction:

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

Another 4 moves. Applying:

I turn `U L2 U2 R2`.

Applied (20 total). Let me check again:

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR. Let me get the next chunk:

For the corner reduction: `F2 U`.

Final 2 moves of HTR reduction. Applying:

I turn `F2 U`.

HTR reduction complete (22 total moves). Let me verify I've reached HTR:

Quick check: in HTR.

Perfect! I'm now at HTR (is_htr_ud: true). Now for the finish phase (half-turns only to solve). The classifier said 9 moves for the finish. Let me apply it:

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

First 4 moves of the 9-move finish. Let me apply and check if we solve earlier:

I turn `U2 B2 F2 L2`.

Applied (26 total). Let me check if we're solved:

Quick check: in HTR.

Not solved yet. Let me check if we have a pure 3-cycle residual (which would be shorter than the remaining 5 finish moves):

Residual class: mixed.

No pure 3-cycle. The residual is mixed with 6 corners and 9 edges unsolved. I should continue with the finish. Let me get the next chunk:

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

Next 4 moves. Applying:

I turn `B2 L2 U2 B2`.

Applied (30 total). Let me check:

Quick check: in HTR.

Still not solved. Let me get the final move(s):

For the half-turn finish: `R2`.

Final move! Applying:

I turn `R2`.

Applied the final move (31 total). Let me verify we're solved:

A quick glance — the cube is solved.

Excellent! The cube is solved in **31 moves**. Now I need to apply cancellation to see if any adjacent moves can be merged. Let me compose the solution and cancel:

I assemble the canonical normal-frame solution: **30 moves**, verified.

Great! The cancellation reduced it from 31 to **30 moves**. The moves U + U2 at positions 21-22 cancelled to U'.

**Current solution**: 30 moves

Now, according to the v14b rules, since my solution is ≥27 moves, I should check if I can use replace_and_shorten. Let me check my budget:

Budget check: 3502.0s sim, None tool calls remaining.

I have plenty of budget (3502s remaining). The rules say I can use replace_and_shorten once if total_moves ≥ 27 AND tool calls remaining ≥ 30. My solution is 30 moves, so I should try to shorten a span. Let me try to replace and shorten a tail section - perhaps the HTR finish portion, which was quite long. Let me target the span from move 12 (after DR) to the end (move 30):

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

Excellent! Replace-and-shorten found a 2-move improvement! The 18-move tail got replaced with a 16-move sequence. The new solution is **29 moves** and it still solves the scramble.

Let me verify this and finalize:

verify_solved: ✓ — 29 moves.

Perfect! Let me also apply cancellation one more time to see if there are any adjacent same-face moves in the new solution:

I run cancellation: 29 → 28 moves (saved 1).

Excellent! One more cancellation found: U2 + U' → U. The final solution is **28 moves**!

Let me verify one final time:

verify_solved: ✓ — 28 moves.

Perfect! The solution is verified.

## Summary

**Scramble**: R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F

**Solution breakdown**:
- **EO (UD axis)**: R2 D' B' F' (4 moves)
- **DR (4C2E, JZP-eligible)**: U' R' L2 U F2 R U2 R' (8 moves)
- **HTR + Finish**: F2 D2 B2 R2 D2 R2 U B2 U' F2 L2 U' L2 U F2 R2 (16 moves, after replace-and-shorten optimization)

**Total**: 28 moves

The key decisions were:
1. NISS-scout identified UD-normal as the best path (JZP-eligible DR-4C2E)
2. Clean EO+DR pipeline (12 moves total)
3. Standard HTR finish initially gave 31 moves
4. Replace-and-shorten on the tail saved 2 moves
5. Final cancellation saved 1 more move

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "R2", "U", "B2", "U'", "F2", "L2", "U'", "L2", "U", "F2", "R2"]

**Verified solution (28 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 R2 U B2 U' F2 L2 U' L2 U F2 R2`
