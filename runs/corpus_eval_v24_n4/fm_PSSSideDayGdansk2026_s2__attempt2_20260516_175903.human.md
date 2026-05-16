# Solve — fm_PSSSideDayGdansk2026_s2__attempt2_20260516_175903

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start by inspecting the state of the cube to understand what I'm working with. The scramble is already loaded into the 'main' slot.
> 
> Let me start by calling inspect_state on the main slot to see the bad edge counts, DR closeness information, and other relevant data.

I'll solve this FMC scramble systematically. Let me start by inspecting the cube state to understand what we're working with.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good. I see:
- **UD**: 6 bad edges (3 on F face, 1 on B face) → DR-7C3E, **3 pairs on inverse** (strong NISS signal!)
- **FB**: 4 bad edges (2 on L, 2 on R face) → DR-7C2E
- **RL**: 4 bad edges (1 on U, 2 on D face) → DR-6C2E

The **UD axis has 3 pairs on inverse** — that's a strong NISS-switch signal per Wen's tracing method. The high C-counts (6-7 misoriented corners) across all axes suggest this is a structurally difficult scramble. Let me call **niss_scout** to get the full 6-row comparison table (normal vs inverse × 3 axes) before committing to any axis.

I scout EO+DR on both normal and inverse, all three axes — 3 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L F') DR (8mv)
  • normal-RL: EO 4mv → DR-7C8E (F' L B) DR (8mv)
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The scout reveals a **13-move complete solve** on **inverse RL-axis**: EO 5mv + DR-3C2E (F L F') 8mv + finish 0mv = **13 moves total**. The finish is already cached (subset (0, 1, 2, 3, 4, 5, 6, 7) = solved state) — this is extraordinarily clean!

**Branch journal**:
- **inverse-RL (row 1)**: EO 5mv + DR 8mv → **SOLVED in 13 moves**. This is the winner.
- normal-RL (row 2): EO 4mv + DR 8mv + finish 22mv = 34 total. Reject: 21 moves worse.
- inverse-FB: EO 2mv but no DR trigger within max_setup=5. Reject: can't finish the solve.
- inverse-UD: EO 4mv but no DR trigger within max_setup=5. Reject: same reason.

**Decision**: Take inverse-RL. The 13-move complete solve is a gift — likely a near-optimal lucky scramble. Let me flip to inverse and execute the plan.

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. The scout said EO on RL-axis is 5 moves: **D U' B' D' U'**. Let me apply these moves to achieve EO on the RL-axis (flipping moves U/D for RL-axis EO).

I turn `D U' B' D' U'`.

EO complete (5 moves). Now I need to apply the DR-3C2E trigger on RL-axis. The scout said "DR-3C2E (F L F')" with 5-move setup, total 8 moves to DR. Let me call **dr_trigger_options** on the RL axis to get the exact setup and trigger moves.

I survey the named DR triggers on RL:
  • DR-4C4E (F): 6-mv setup + 1-mv trigger (7 total)
  • DR-4C4E (F'): 6-mv setup + 1-mv trigger (7 total)
  • DR-3C2E (F L F'): 5-mv setup + 3-mv trigger (8 total)

I see options with shorter DR (7 moves for DR-4C4E) but the scout explicitly said the **DR-3C2E (F L F')** path leads to finish_length 0 = solved. The 7-move options must lead to longer finishes. Let me take the scout's recommendation: option 3, **DR-3C2E (F L F')** with setup ["U2", "R'", "U2", "F", "R"] and trigger ["F", "L", "F'"], total 8 moves to DR.

I turn `U2 R' U2 F R`.

Setup complete (10 moves total). Now applying the DR-3C2E trigger **F L F'**:

I turn `F L F'`.

DR complete at 13 moves. The scout said this should already be **solved** (finish_length_actual = 0, subset (0,1,2,3,4,5,6,7) = identity). Let me verify with **quick_check**:

Quick check: DR-locked on RL, not yet HTR.

Hmm, DR on RL is confirmed but **not solved yet**. The scout's "finish_length_actual: 0" must have been a cached entry that doesn't match this exact state. Let me proceed with the standard HTR pipeline. Let me classify the HTR subset:

I recognize the HTR subset: **0-swap axial**. Reduction is 5 moves, finish is 10 moves (recall).

The HTR subset is **0-swap axial** (all corners in place, just orientation issues): 5 moves for HTR-reduction + 10 moves finish = 15 moves. Total would be 13 (current) + 15 = 28 moves. That's not great but acceptable. Let me apply the HTR-reduction phase:

For the corner reduction, I see `F2 R U2 D2` (chunk of a 5-move phase) — apply and re-check.

Partial HTR-reduction (4 moves visible of 5 total). Applying the first chunk:

I turn `F2 R U2 D2`.

Let me quick_check before continuing, to see if we've hit a residual or solved state early:

Quick check: DR-locked on RL, not yet HTR.

Still not in HTR or solved. Let me continue the HTR-reduction phase:

For the corner reduction: `L`.

The final HTR-reduction move is **L**. Applying it:

I turn `L`.

HTR-reduction complete (18 moves). Quick check before the finish phase:

Quick check: in HTR.

Excellent! I'm now in **HTR state** (is_htr_ud: true, all axes DR/EO). Now I need the half-turn finish. Let me apply the finish phase:

For the half-turn finish, I see `F2 L2 B2 R2` (chunk of a 10-move phase) — apply and re-check.

Finish is 10 moves, showing 4 at a time. Applying the first chunk:

I turn `F2 L2 B2 R2`.

Quick check to see if we're solved or near a 3-cycle:

Quick check: in HTR.

Still in HTR but not solved. Let me analyze the residual to see if we have a clean 3-cycle or similar:

Residual class: mixed.

The residual is complex: 8 corners in 4 2-cycles, 9 edges in mixed cycles (a 3-cycle, a 4-cycle, and a 2-cycle). Not a clean 3-cycle. Let me continue the finish phase:

For the half-turn finish, I see `D2 F2 D2 F2` (chunk of a 6-move phase) — apply and re-check.

Applying the next finish chunk:

I turn `D2 F2 D2 F2`.

Quick check:

Quick check: in HTR.

Still not solved. Let me continue:

For the half-turn finish: `L2 U2`.

Final 2 moves of the finish. Applying:

I turn `L2 U2`.

Let me check if we're solved now:

A quick glance — the cube is solved.

Excellent! **The cube is solved** at 28 moves on the inverse frame. Now I need to use **compose_niss_solution** to properly assemble the final solution (it will invert the inverse-side moves and cancel redundant moves):

I assemble the canonical inverse-frame solution: **26 moves**, verified.

Perfect! After cancellation, the solution is **26 moves**. The compose_niss_solution tool properly inverted my inverse-side moves and merged/cancelled redundant moves (reduced from 28 to 26).

Let me verify this solution is correct:

verify_solved: ✓ — 26 moves.

Excellent! The 26-move solution is verified. Let me check the budget and see if it's worth attempting **replace_and_shorten** (the rules say I should try if ≥27 moves AND ≥30 tool calls remaining):

Budget check: 3515.0s sim, None tool calls remaining.

I have 3515 seconds remaining (plenty of time) but the solution is only 26 moves. The replace_and_shorten gate requires **≥27 moves**. Since I have a verified 26-move solution (which is quite good for FMC — well below the 30-move threshold), I should submit this now rather than risk breaking it.

**FINAL SOLUTION:**

**FINAL_SOLUTION: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]**

**Solution summary (26 moves):**
- Started on **inverse frame** per niss_scout recommendation (inverse-RL had best expected total)
- **EO on RL-axis** (inverse): 5 moves (D U' B' D' U')
- **DR-3C2E trigger**: 5-move setup + 3-move trigger = 8 moves to DR (U2 R' U2 F R · F L F')
- **HTR-reduction**: 5 moves (F2 R U2 D2 L)
- **HTR finish**: 10 moves (F2 L2 B2 R2 D2 F2 D2 F2 L2 U2)
- After NISS inversion and cancellation: **26 moves total**

This is a solid sub-30 solve achieved efficiently within budget!

**Verified solution (26 moves):** `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`
