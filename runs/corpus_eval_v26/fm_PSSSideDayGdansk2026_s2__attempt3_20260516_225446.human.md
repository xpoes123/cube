# Solve — fm_PSSSideDayGdansk2026_s2__attempt3_20260516_225446

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start by inspecting the state on the 'main' slot, then follow the FMC pipeline outlined in the instructions.
> 
> The scramble is: R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> Let me start by inspecting the state to see the cube configuration.

I'll solve this FMC scramble step-by-step following elite solver methodology. Starting with state inspection.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**State analysis:** UD axis has 6 bad edges (moderate), FB and RL both have 4 (good candidates). The UD axis shows `top_pairs_on_inverse: 3` which is a STRONG NISS-switch signal. DR-closeness shows all axes require significant work (7C3E, 7C2E, 6C2E). 

Per the v16 pipeline, I must now call **niss_scout** to get the 6-row comparison table (normal × inverse × 3 axes) before committing to any EO. This is mandatory elite-solver procedure.

I scout EO+DR on both normal and inverse, all three axes — 3 viable rows.
  • normal-RL: EO 4mv → DR-7C8E (F' L B) DR (8mv)
  • inverse-RL: EO 5mv → DR-3C2E (F L F') DR (8mv)
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

**NISS-scout analysis - GOLD FOUND:**

Looking at the table:
- **INVERSE-RL (row 6)**: EO 5mv + DR 8mv (DR-3C2E trigger, F L F') → **total_to_solved_actual: 13 moves** with finish 0mv. This is a DIRECT SOLVE in 13 moves!
- Normal-RL: EO 4mv + DR 8mv → 34 moves total (terrible finish)
- Normal-FB: EO 4mv, no DR within view
- Inverse-FB: EO 2mv, no DR within view
- Normal/Inverse-UD: EO 4-5mv, no DR within view

**Decision: Taking INVERSE-RL with the 13-move direct solve.** This is a sub-15 solution right from the scout — a rare optimal-path find. The DR-3C2E trigger on inverse-RL leads directly to solved state.

Switching to inverse frame now:

NISS flip — switching to the inverse scramble.

**Now on inverse frame.** Applying the 5-move EO for RL-axis: D U' B' D' U'

I turn `D U' B' D' U'`.

**EO complete (5 moves on inverse-RL axis).** Now need to compose the DR. The scout showed DR-3C2E with setup_length=5 + trigger_length=3 = 8 moves total to DR. Let me use dr_trigger_options to see the actual DR menu:

I survey the named DR triggers on RL:
  • DR-4C4E (F): 6-mv setup + 1-mv trigger (7 total)
  • DR-4C4E (F'): 6-mv setup + 1-mv trigger (7 total)
  • DR-3C2E (F L F'): 5-mv setup + 3-mv trigger (8 total)

**DR trigger options analysis:**
- **Option 1**: DR-4C4E (F) - 7 moves total (6 setup + 1 trigger). Shortest DR but 4C4E substate finishes poorly.
- **Option 3**: DR-3C2E (F L F') - 8 moves total (5 setup + 3 trigger). This is what the scout found! The DR-3C2E substate is superior.

However, the scout showed this leads to a **0-move finish** (total 13 moves = 5 EO + 8 DR + 0). Let me verify by applying option 3 and checking if it solves:

Applying the DR-3C2E option (setup: U2 R' U2 F R, trigger: F L F'):

I turn `U2 R' U2 F R`.

I turn `F L F'`.

**DR complete at 13 moves on inverse.** Now checking if this actually solves the cube (as the scout predicted with finish=0):

Quick check: DR-locked on RL, not yet HTR.

**Not solved yet. DR-RL is reached but not solved.** The scout's "finish=0" was likely a cache artifact or the subset lookup wasn't fully accurate. Let me proceed with HTR classify and finish:

I recognize the HTR subset: **0-swap axial**. Reduction is 5 moves, finish is 10 moves (recall).

**HTR subset: 0-swap axial.** This is actually SOLVED corners already! The phases show 5 moves HTR-reduction + 10 moves finish = 15 more moves. Total would be 13 + 15 = 28 moves.

Wait, the subset is (0,1,2,3,4,5,6,7) which is identity — corners are already solved! Let me check the HTR-reduction phase:

For the corner reduction, I see `F2 R U2 D2` (chunk of a 5-move phase) — apply and re-check.

**Partial HTR-reduction (4 of 5 moves).** Applying and checking:

I turn `F2 R U2 D2`.

Quick check: DR-locked on RL, not yet HTR.

**Still not at HTR. Need the remaining 1 move of reduction:**

For the corner reduction: `L`.

I turn `L`.

Quick check: in HTR.

**HTR reached! All axes show EO/DR solved, is_htr_ud=true.** Now applying the finish phase (10 moves expected):

For the half-turn finish, I see `F2 L2 B2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `F2 L2 B2 R2`.

Quick check: in HTR.

**Still not solved after 4 moves of finish. Continuing:**

For the half-turn finish, I see `D2 F2 D2 F2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F2 D2 F2`.

Quick check: in HTR.

**Still in HTR, not solved. Continuing with remaining finish moves:**

For the half-turn finish: `L2 U2`.

I turn `L2 U2`.

A quick glance — the cube is solved.

**SOLVED at 28 moves on the inverse frame!** Now I need to compose the NISS solution properly. The current history is 28 moves on the inverse, so the final solution will be the inverse of these 28 moves applied to the normal scramble.

Using compose_niss_solution to get the canonical form:

I assemble the canonical inverse-frame solution: **26 moves**, verified.

**Solution composed: 26 moves after cancellation!** The compose_niss_solution inverted and cancelled to get from 28 moves down to 26. 

Let me verify this solution works:

verify_solved: ✓ — 26 moves.

**Verified: 26-move solution is correct!** 

Now checking if I should try replace_and_shorten. The rules state: use it if total_moves ≥ 27 AND tool calls remaining ≥ 30. I have 26 moves, which is below the threshold. However, let me check my remaining budget:

Budget check: 3517.0s sim, None tool calls remaining.

**Budget status: 83s spent, 3517s remaining, excellent time.** My solution is 26 moves, which is BELOW the 27-move threshold for replace_and_shorten. According to the rules, r&s gates are: "total_moves ≥ 27 AND tool calls remaining ≥ 30". Since I have only 26 moves, I should NOT call replace_and_shorten.

**This is a strong sub-27 solve (26 moves) achieved efficiently.** Per the SHIP RULE: "Any verified solve under 50 moves beats a timeout. Once you have a working complete solution... CALL FINAL_SOLUTION and STOP."

**FINAL_SOLUTION:**

U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'

**Summary:**
- **Approach**: NISS-first methodology — scouted all 6 (side × axis) combinations
- **Path chosen**: Inverse-RL axis with 5-move EO + 8-move DR-3C2E + 15-move HTR finish
- **EO**: 5 moves on inverse-RL axis (D U' B' D' U')
- **DR**: 8 moves via DR-3C2E trigger (U2 R' U2 F R + F L F')
- **HTR**: 5-move reduction + 10-move half-turn finish
- **Raw**: 28 inverse moves → 26 normal moves after NISS-inversion and cancellation
- **Time used**: 83 seconds of 3600-second budget (2.3%)

This is a clean elite-quality solve: sub-27, efficient scouting, proper NISS decision-making, and strong DR-trigger choice leading to a manageable HTR subset.

*Thinking (29):*

> The user is right - I need to actually emit the FINAL_SOLUTION in the correct format. I already have the verified 26-move solution from compose_niss_solution. Let me output it now.

FINAL_SOLUTION: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

**Verified solution (26 moves):** `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`
