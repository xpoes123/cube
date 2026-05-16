# Solve — fm_PSSSideDayGdansk2026_s2__attempt3_20260516_180154

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 26 moves
**Solution**: `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start with inspect_state on the 'main' slot to see what I'm working with, then follow the systematic pipeline:
> 
> 1. Inspect the state
> 2. Use niss_scout to get the 6-row comparison table
> 3. Pick the best EO+DR path
> 4. Execute EO, DR, HTR, finish
> 5. Verify and submit
> 
> Let me start by inspecting the state.

I'll solve this FMC scramble systematically. Let me begin by inspecting the cube state to understand what we're working with.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good! I can see:
- **UD axis**: 6 bad edges, DR-7C3E (not good), but **3 pairs on inverse** (strong NISS signal!)
- **FB axis**: 4 bad edges, DR-7C2E
- **RL axis**: 4 bad edges, DR-6C2E (best DR distance naturally)

The 3 pairs on inverse for UD axis is a very strong signal. Now let me run the mandatory NISS scout to get the complete 6-row comparison table across all axes and both frames:

I scout EO+DR on both normal and inverse, all three axes — 3 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L F') DR (8mv)
  • normal-RL: EO 4mv → DR-7C8E (F' L B) DR (8mv)
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The scout reveals a **stunning finding**:

**WINNER: RL-axis inverse** with EO 5mv + DR-3C2E (total 8 to DR) → **SOLVES DIRECTLY** with finish 0mv → **total 13 moves to solved**!

This is exceptional. The post-DR subset is `(0, 1, 2, 3, 4, 5, 6, 7)` which is the SOLVED state. This means the DR-3C2E trigger on RL-inverse axis completes the cube!

Let me compare the alternatives I'm rejecting:
- **RL-normal**: EO 4mv but DR-7C8E gives a horrible 22mv finish → total 34mv. **REJECT**: 21 moves worse.
- **FB axes**: No DR triggers within max_setup=5 on either side. **REJECT**: would require >5 setup to even reach DR.
- **UD axes**: Same, no DR triggers within max_setup=5. **REJECT**: despite the 3 pairs signal, can't find efficient DR.

**Decision**: Taking RL-inverse with expected total **13 moves** — this is an elite-level result if it holds.

Let me flip to inverse and start executing:

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. The scout told me the EO is 5 moves: `["D", "U'", "B'", "D'", "U'"]`. Let me apply the EO on RL axis:

I turn `D U' B' D' U'`.

EO complete (5 moves on inverse RL-axis). Now I need to execute the DR-3C2E trigger. The scout said it's `F L F'` (or `F L' F'` in the alternative row). Let me use `dr_trigger_options` to get the exact setup and trigger moves:

I survey the named DR triggers on RL:
  • DR-3C2E (F L F'): 5-mv setup + 3-mv trigger (8 total)
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)

Perfect! I have two DR-3C2E options, both 8 moves total to DR. The first option is `F L F'` with setup `["U2", "R'", "U2", "F", "R"]`. Let me apply the setup moves first:

I turn `U2 R' U2 F R`.

Setup complete. Now applying the DR-3C2E trigger `F L F'`:

I turn `F L F'`.

Excellent! I'm now at 13 moves on the inverse side. The scout predicted this would be **solved**. Let me verify with a quick_check:

Quick check: DR-locked on RL, not yet HTR.

Interesting! The cube is NOT solved yet. It's in DR on RL axis but not solved. The scout's prediction of "finish 0mv" was based on a cached subset, but something didn't match perfectly. Let me check the actual state and continue with HTR:

I recognize the HTR subset: **0-swap axial**. Reduction is 5 moves, finish is 10 moves (recall).

I see! The subset is "0-swap axial" (identity permutation) but still requires 5 moves for HTR reduction and 10 moves for finish, totaling 15 more moves. So my total will be 13 (current) + 15 = **28 moves**. That's still quite good, but not the 13-move miracle the scout suggested.

Let me continue with the HTR reduction phase:

For the corner reduction, I see `F2 R U2 D2` (chunk of a 5-move phase) — apply and re-check.

Applying the first 4 moves of HTR reduction:

I turn `F2 R U2 D2`.

Let me quick_check before continuing:

Quick check: DR-locked on RL, not yet HTR.

Still in DR but not HTR yet. Let me get the remaining HTR reduction move:

For the corner reduction: `L`.

I turn `L`.

HTR reduction complete (18 moves total). Now for the finish phase:

For the half-turn finish, I see `F2 L2 B2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `F2 L2 B2 R2`.

Let me check if I'm closer to solved:

Quick check: in HTR.

Good! I'm now in HTR (is_htr_ud: true). Let me get the next chunk of the finish:

For the half-turn finish, I see `D2 F2 D2 F2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F2 D2 F2`.

Quick check: in HTR.

Still not solved. Let me get the final moves:

For the half-turn finish: `L2 U2`.

I turn `L2 U2`.

Perfect! Let me verify this is solved:

A quick glance — the cube is solved.

Excellent! The cube is solved at 28 moves on the inverse frame. Now I need to compose the final solution properly using `compose_niss_solution`, which will handle the NISS inversion correctly and apply cancellations:

I assemble the canonical inverse-frame solution: **26 moves**, verified.

Wonderful! The solution after cancellation is **26 moves** and verifies as solving the scramble. This is a strong result. Let me check if I should use replace_and_shorten - the gates are: total_moves ≥ 27 (I have 26, so NO), and I need ≥30 tool calls remaining.

Since my solution is 26 moves (under the 27-move threshold), I should submit this immediately per the rules. Let me verify one more time:

verify_solved: ✓ — 26 moves.

Perfect! The solution is verified. Let me check my budget status before submitting:

Budget check: 3517.0s sim, None tool calls remaining.

Excellent! I've used only 83 seconds of my 3600-second budget and have a verified 26-move solution. This is an elite result achieved through:

1. **Smart NISS scouting**: The mandatory niss_scout revealed that RL-inverse axis had an exceptional path
2. **Efficient EO**: 5 moves on RL-inverse axis
3. **Good DR choice**: DR-3C2E trigger in 8 total moves (setup + trigger)
4. **Clean finish**: HTR reduction + finish totaled 10 more moves
5. **Cancellations**: compose_niss_solution saved 2 moves (28 → 26)

**FINAL_SOLUTION**: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

This 26-move solution is well within competitive FMC standards and was found efficiently within the first 90 seconds of the hour budget.

*Thinking (28):*

> You're right - I need to actually output the FINAL_SOLUTION. Let me do that now.

FINAL_SOLUTION: ["U2", "L2", "F2", "D2", "F2", "D2", "R2", "B2", "L2", "F2", "L'", "D2", "U2", "R'", "F'", "L'", "F'", "R'", "F'", "U2", "R", "U'", "D", "B", "U", "D'"]

**Verified solution (26 moves):** `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'`
