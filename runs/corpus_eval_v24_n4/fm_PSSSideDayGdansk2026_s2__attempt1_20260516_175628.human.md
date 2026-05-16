# Solve — fm_PSSSideDayGdansk2026_s2__attempt1_20260516_175628

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I need to start with inspect_state on the main slot. Let me follow the pipeline:
> 
> 1. First inspect_state to see the cube state
> 2. Then use niss_scout to get the 6-row comparison table (normal×inverse×{UD,FB,RL})
> 3. Pick the best axis/side based on expected_total_to_solved
> 4. Apply EO
> 5. Find DR
> 6. HTR classify and finish
> 7. Cancel and verify
> 
> Let me begin.

I'll solve this FMC scramble step by step, following the elite-solver methodology. Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good. I can see:
- **UD axis**: 6 bad edges, DR-7C3E (hard), but **3 pairs on inverse** (strong NISS signal)
- **FB axis**: 4 bad edges, DR-7C2E
- **RL axis**: 4 bad edges, DR-6C2E

The 3 pairs on inverse for UD is a strong signal. Now let me run niss_scout to get the full 6-row comparison table across normal/inverse and all three axes.

I scout EO+DR on both normal and inverse, all three axes — 3 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L F') DR (8mv)
  • normal-RL: EO 4mv → DR-7C8E (F' L B) DR (8mv)
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

**Excellent!** The niss_scout has revealed a clear winner:

**Top choice: inverse-RL axis**
- EO 5 moves: D U' B' D' U'
- DR-3C2E (F L F') with 5-move setup → total DR = 8 moves
- **Post-DR state is ALREADY SOLVED** (finish_length_actual = 0)
- **Total to solved: 13 moves!**

This is remarkable — the DR-3C2E trigger puts the cube directly into the solved state. The other axes either have no DR triggers within max_setup or finish in 34+ moves.

**Branch journal:**
- **Inverse-RL (chosen)**: EO 5 + DR 8 = 13 moves total. Clean 3C2E trigger lands on solved. **TAKING THIS.**
- Normal-RL: EO 4 + DR 8 + finish 22 = 34 moves. **Rejected** — 21 moves worse.
- Inverse-FB/Normal-FB/Inverse-UD/Normal-UD: no DR triggers within max_setup. **Rejected** — not viable.

Let me flip to inverse and apply the solution:

NISS flip — switching to the inverse scramble.

Good. Now on the inverse frame. Let me apply the EO sequence first (RL-axis EO: D U' B' D' U'):

I turn `D U' B' D' U'`.

EO applied (5 moves on inverse for RL-axis). Now let me verify EO is solved and get the DR trigger details:

Quick check: EO solved on RL, working toward DR.

Perfect! RL-axis EO is confirmed. Now let me get the DR trigger options:

I survey the named DR triggers on RL:
  • DR-3C2E (F L F'): 5-mv setup + 3-mv trigger (8 total)
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)

Great! I see two 3C2E triggers, both 8 moves total (5 setup + 3 trigger). The niss_scout indicated the first one (F L F') leads to solved. Let me apply the first option:

**Setup moves (5):** U2 R' U2 F R

I turn `U2 R' U2 F R`.

**DR trigger (F L F'):**

I turn `F L F'`.

Let me check if we're solved:

Quick check: DR-locked on RL, not yet HTR.

Interesting — we have DR on RL (confirmed), but not solved yet. The niss_scout said finish_length_actual=0, which may have been from a cached state. Let me check the actual HTR state:

I recognize the HTR subset: **0-swap axial**. Reduction is 5 moves, finish is 10 moves (first exposure — learning).

I see — the subset is "0-swap axial" which requires 5 moves for HTR reduction + 10 moves for finish = 15 moves total. So the complete solution will be 13 (EO+DR) + 15 (HTR finish) = 28 moves. Let me proceed with the HTR phases:

**HTR reduction (5 moves):**

For the corner reduction, I see `F2 R U2 D2` (chunk of a 5-move phase) — apply and re-check.

I turn `F2 R U2 D2`.

Let me check state before continuing:

Quick check: DR-locked on RL, not yet HTR.

Not yet in HTR. Let me get the next chunk:

For the corner reduction: `L`.

I turn `L`.

Now let me check if we're in HTR and continue with the finish:

Quick check: in HTR.

Perfect! Now in HTR (is_htr_ud=true). Let me apply the finish phase:

For the half-turn finish, I see `F2 L2 B2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `F2 L2 B2 R2`.

Quick check: in HTR.

Still not solved. Let me continue with the next chunk:

For the half-turn finish, I see `D2 F2 D2 F2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F2 D2 F2`.

Quick check: in HTR.

Let me get the remaining finish moves:

For the half-turn finish: `L2 U2`.

I turn `L2 U2`.

A quick glance — the cube is solved.

**Excellent! The cube is solved!** We have a 28-move solution on the inverse frame. Now I need to compose the final solution properly using compose_niss_solution, which will invert the moves and cancel where possible:

I assemble the canonical inverse-frame solution: **26 moves**, verified.

Great! The composed solution has 26 moves after cancellation (saved 2 moves from the raw 28). Let me verify this solution:

verify_solved: ✓ — 26 moves.

Perfect! The solution is verified at 26 moves. Let me check my budget status:

Budget check: 3503.0s sim, None tool calls remaining.

I have 3503 seconds remaining (plenty of time), and the solution is 26 moves. According to the rules, since the solution is ≥27 moves threshold is NOT met (26 < 27), I should NOT call replace_and_shorten. However, let me double-check the instruction:

Looking at the rules: "REFINEMENT (MANDATORY when gates pass): after you have a verified solve, if total_moves ≥ 27 AND tool calls remaining ≥ 30 AND you haven't already called replace_and_shorten this run..."

Since my solution is 26 moves (< 27), the gate does NOT pass, so I should NOT call replace_and_shorten.

**Solution Summary:**
- Used NISS-scout to identify the optimal axis/frame
- Chose inverse-RL with EO 5 moves + DR-3C2E trigger (8 moves total)
- Completed HTR finish: 5 moves reduction + 10 moves finish
- Total: 28 moves on inverse → 26 moves after cancellation in normal frame

This is a strong sub-30 solution achieved efficiently!

**FINAL_SOLUTION:** ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

*Thinking (30):*

> The user is right - I verified the solution and determined I should submit it, but I never actually outputted the FINAL_SOLUTION line in the required format. Let me do that now.

FINAL_SOLUTION: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

**Verified solution (26 moves):** `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`
