# Solve — fm_PSSSideDayGdansk2026_s1__attempt2_20260516_174614

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 28 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`

---

*Thinking (1):*

> Perfect! I'll start by inspecting the state of the cube and then use the niss_scout tool to evaluate all axes and frames systematically before committing to an EO axis. Let me follow the FMC pipeline exactly as documented.
> 
> I'll:
> 1. inspect_state on 'main' to see the bad edges per axis
> 2. niss_scout to get the 6-row joint table (normal × inverse × {UD, FB, RL}) sorted by expected_total_to_solved
> 3. Follow the recommendation from the scout
> 4. Apply EO incrementally
> 5. Use dr_trigger_options for DR composition
> 6. Complete through HTR finish
> 7. Verify and submit
> 
> Let me start!

I'll solve this FMC scramble following the elite-solver pipeline. Let me begin by inspecting the state and scouting all axes/frames systematically.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Now I'll run niss_scout to get the comprehensive 6-row table comparing all axes and frames:

I scout EO+DR on both normal and inverse, all three axes — 5 viable rows.
  • normal-UD: EO 4mv → DR-4C2E (R U2 R') DR (8mv) [JZP]
  • normal-UD: EO 4mv → DR-7C8E (R' U L) DR (8mv)
  • inverse-FB: EO 5mv → DR-7C8E (U F D) DR (7mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

**Scouting complete.** Reading the table:

**TOP OPTION (tied)**: UD-normal with EO 4mv + DR-4C2E (8mv total to DR), **JZP-eligible** → verified total 33 moves to solved. The JZP flag is critical — it means this is a structurally superior DR state.

**ALTERNATIVES REJECTED**:
- UD-normal DR-7C8E: also 33mv total but NOT JZP (worse structure)
- FB-inverse: EO 5mv + DR-7C8E (12-13mv to DR) — no cached finish but 7C8E is typically longer
- RL-inverse: EO 5mv + DR-4C4E (14mv to DR) — much worse

**DECISION**: I'll take the UD-normal axis with the 4mv EO + DR-4C2E JZP-eligible path. The JZP flag means the post-DR state will have cleaner corner orientation and dramatically shorter HTR finish. Let me apply the EO first:

I turn `R2 D' B' F'`.

**EO complete (4 moves).** Now I need to reach DR-4C2E. The scout said 5-move setup + 3-move R U2 R' trigger. Let me use dr_trigger_options to get the exact sequence:

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

**DR options reviewed:**
- **DR-4C2E (R U2 R')**: 5-move setup, **JZP-eligible** → total 8 to DR
- DR-7C8E (R' U L): also 8 to DR but NOT JZP (4 pairs on inverse though!)
- DR-7C8E (R U L): 9 to DR
- DR-2C4E (R F2 R): 9 to DR, JZP-eligible

**Picking DR-4C2E** because it's JZP-eligible (cleaner structure) and shortest. The scout verified this path gives a 33-move total. Let me apply the setup + trigger:

I turn `U' R' L2 U F2`.

I turn `R U2 R'`.

**DR reached in 12 moves (EO 4 + DR 8).** Now I need to complete the HTR finish. Let me classify the HTR subset:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (recall).

**HTR subset identified**: 0-swap long-cycle with cycle structure [3, 2, 2, 1]. This will take:
- HTR reduction: 10 moves
- Finish: 9 moves
- Total from DR: 19 moves → projected total: 12 + 19 = **31 moves**

This is actually BETTER than the scout's prediction of 33! Let me apply the HTR reduction phase:

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

The HTR reduction is 10 moves total, showing first 4. Let me apply them and check if we've landed on something insertable:

I turn `U F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Not in HTR yet. Continue with the next chunk of HTR reduction:

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not in HTR. Get the final chunk:

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

**HTR reached!** Now in HTR-UD. At 22 moves currently. Let me apply the finish phase:

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Quick check: in HTR.

Not solved yet, continue with the next finish chunk:

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

Quick check: in HTR.

Get the final move:

For the half-turn finish: `R2`.

I turn `R2`.

A quick glance — the cube is solved.

**SOLVED!** The cube is complete in 31 moves. Now I need to cancel and verify before submitting. Let me compose the solution properly:

I assemble the canonical normal-frame solution: **30 moves**, verified.

Excellent! The solution **cancels down to 30 moves** (U + U2 → U' at move 22-23). The solution is verified and solves the cube.

**Current state: 30-move solution**

According to the pipeline rules, with a solution ≥27 moves, I should check if replace_and_shorten can help. Let me check my budget first:

Budget check: 3518.0s sim, None tool calls remaining.

I have plenty of budget (3518s remaining). The solution is 30 moves, which meets the ≥27 threshold. Let me try replace_and_shorten on a large segment of the solution. The HTR finish was quite long (9 moves), so let me target that portion. I'll try shortening the end section (from around the HTR reduction onward):

replace_and_shorten on the tail span: substitute is 3 moves shorter. Accepted.

**EXCELLENT!** Replace_and_shorten found a 3-move improvement! The HTR-to-finish section (19 moves) was replaced with a 16-move substitute. The new solution is **28 moves** and solves the scramble.

Let me verify this new solution:

verify_solved: ✓ — 28 moves.

Perfect! The 28-move solution is verified. This is a strong result. Let me check once more if there's any manual cancellation possible:

I check for cancellations — no savings.

No further cancellations possible. The final solution is **28 moves**.

## Solution Summary

**Strategy**: UD-normal axis with JZP-eligible DR-4C2E path
- **EO (4 moves)**: R2 D' B' F' — solved 8 bad edges on UD axis using algorithmic pattern
- **DR (8 moves)**: U' R' L2 U F2 + R U2 R' — setup + DR-4C2E trigger (JZP-eligible)
- **HTR finish (16 moves after r&s)**: F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2 — shortened from original 19 moves via replace_and_shorten

**Total: 28 moves**

The JZP-eligible DR choice was critical — it provided cleaner corner structure for the HTR finish. The replace_and_shorten tool found a 3-move savings in the HTR section, bringing the solution from 30 → 28 moves.

**FINAL_SOLUTION**: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]

*Thinking (32):*

> The user is right - I need to actually emit the FINAL_SOLUTION in the required format. I have verified the solution is correct (28 moves, solves the scramble), so I should output it now.

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]

**Verified solution (28 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`
