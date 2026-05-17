# Solve — fm_PSSSideDayGdansk2026_s3__attempt3_20260516_213834

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. Let me start by inspecting the state of the cube as instructed.
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> I need to follow the FMC methodology:
> 1. Start with inspect_state to see the cube state
> 2. Use niss_scout to evaluate all axes and sides (normal vs inverse)
> 3. Pick the best EO+DR path based on expected_total_to_solved
> 4. Complete the solve through HTR and finish
> 5. Submit using compose_niss_solution
> 
> Let me begin.

I'll solve this FMC scramble step by step. Let me start by inspecting the cube state to see what I'm working with.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good start. I can see:
- **UD axis**: 4 bad edges (UL, DR, DL, DB), DR-7C3E, **3 pairs on inverse** (strong NISS signal!)
- **FB axis**: 8 bad edges (all over), DR-6C3E
- **RL axis**: 6 bad edges, DR-5C3E

The **3 pairs_on_inverse** on UD axis is a very strong signal to check the inverse frame. Let me now run **niss_scout** to get the complete 6-row comparison table across all axes and both frames:

I scout EO+DR on both normal and inverse, all three axes — 1 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The scout has returned a clear winner:

**Analysis of NISS-scout results:**
1. **Row 1 (WINNER) — inverse-RL**: EO 5mv + DR-3C2E trigger (total DR 8mv) = **13 moves to DR**. The DR-3C2E trigger is one of the best substates (typically finishes in ~5 moves from HTR).
2. Rows 2-6: All show "no DR triggers within max_setup=5" — these would require longer DR exploration.

**Decision**: I'll take **inverse-RL axis** with the 5-move EO followed by the DR-3C2E trigger. The DR-3C2E substate is excellent — significantly better than the common DR-4C4E.

Let me flip to inverse and apply the EO:

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. The EO sequence from the scout is **B' L' D' L2 U'** (5 moves). Let me apply it:

I turn `B' L' D' L2 U'`.

Perfect. Now I should have EO solved on RL axis. Let me verify and get the DR trigger options:

I survey the named DR triggers on RL:
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)
  • DR-3C2E (F L F'): 6-mv setup + 3-mv trigger (9 total)
  • DR-7C8E (F L B): 6-mv setup + 3-mv trigger (9 total)

Excellent! I have three DR trigger options on RL axis:

**DR trigger comparison:**
1. **DR-3C2E (F L' F')**: 5 setup + 3 trigger = **8 moves total to DR**. This is the one the scout recommended. DR-3C2E is a premium substate (typically ~5 HTR+finish).
2. DR-3C2E (F L F'): 6 setup + 3 trigger = 9 moves. Slightly longer.
3. DR-7C8E (F L B): 6 setup + 3 trigger = 9 moves. DR-7C8E is a much worse substate.

**Decision**: Taking option 1 — the **5-move setup followed by F L' F' trigger** for a total of 8 moves to DR. This gives me **EO 5 + DR 8 = 13 moves** to reach DR with an excellent DR-3C2E substate.

Let me apply the setup moves:

I turn `U2 F' D2 F R'`.

Good. Now applying the DR-3C2E trigger **F L' F'**:

I turn `F L' F'`.

Excellent! I'm now at DR on RL axis in 13 moves (5 EO + 8 DR). Let me classify the HTR subset to understand what I'm working with:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 8 moves, finish is 10 moves (recall).

I see the HTR subset: **0-swap long-cycle** with cycle structure [4, 2, 1, 1]. The finish is:
- **HTR reduction**: 8 moves
- **Finish**: 10 moves
- **Total from DR to solved**: 18 moves

This gives me a projected total of **13 (to DR) + 18 (HTR+finish) = 31 moves**. That's not great, but let me proceed and see if there are opportunities for shortcuts along the way.

Let me apply the HTR reduction phase:

For the corner reduction, I see `R' D2 R2 B2` (chunk of a 8-move phase) — apply and re-check.

The HTR reduction is 8 moves but I can only see 4 at a time. Let me apply this first chunk and check if we hit any early residual:

I turn `R' D2 R2 B2`.

Let me use quick_check to see if I've hit any lucky states:

Quick check: DR-locked on RL, not yet HTR.

Not solved yet, still in DR on RL. Let me get the next chunk of HTR reduction:

For the corner reduction: `U2 F2 D2 L`.

Good, here's the remaining 4 moves of HTR reduction:

I turn `U2 F2 D2 L`.

Now at 21 moves. Let me check again before finishing:

Quick check: in HTR.

Great! I'm now in HTR state (is_htr_ud: true). Now let me apply the finish phase:

For the half-turn finish, I see `B2 U2 B2 L2` (chunk of a 10-move phase) — apply and re-check.

The finish is 10 moves total. Let me apply the first 4:

I turn `B2 U2 B2 L2`.

Let me check the state:

Quick check: in HTR.

Still in HTR, not solved yet. Let me check if we have a 3-cycle residual that could be inserted:

Residual class: mixed.

Mixed residual with multiple cycles - not a pure 3-cycle. Let me continue with the remaining finish moves:

For the half-turn finish, I see `D2 L2 F2 L2` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 L2 F2 L2`.

Quick check: in HTR.

Residual class: mixed.

Still a mixed residual. Let me get the final 2 moves of the finish:

For the half-turn finish: `U2 B2`.

I turn `U2 B2`.

Perfect! Let me verify this is solved:

A quick glance — the cube is solved.

Excellent! The cube is solved in 31 moves on the inverse frame. Now I need to use **compose_niss_solution** to get the correct normal-frame solution (it will invert my inverse-frame moves and handle cancellations):

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Wonderful! The solution after cancellation is **30 moves**. This is a solid solve. However, the note suggests I could try **replace_and_shorten** if the gates pass (≥27 moves and ≥30 tool calls remaining). Let me check my budget:

Budget check: 3510.0s sim, None tool calls remaining.

I have plenty of budget (3510s remaining). The solution is 30 moves, which is ≥27. Let me try **replace_and_shorten** on a substantial portion of the solution to see if I can improve it. I'll target the middle-to-end section where there might be inefficiencies:

replace_and_shorten: substitute is 8 moves longer; reject.

Unfortunately, **replace_and_shorten made it worse** (delta +8, increasing from 21 to 29 moves in that span). This is expected sometimes - the tool is exploring alternative paths but doesn't always find shorter ones.

I should stick with my original **30-move solution**. Let me verify it once more before submitting:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified and solves the scramble in **30 moves**.

## Summary of solve:

**Strategy chosen**: Inverse-RL axis based on niss_scout recommendation
- **EO (inverse-RL)**: 5 moves — B' L' D' L2 U'
- **DR-3C2E trigger**: 8 moves (5 setup + 3 trigger) — U2 F' D2 F R' F L' F'
- **HTR reduction**: 8 moves — R' D2 R2 B2 U2 F2 D2 L
- **HTR finish**: 10 moves — B2 U2 B2 L2 D2 L2 F2 L2 U2 B2
- **Total**: 31 moves on inverse → **30 moves after cancellation in normal frame**

The DR-3C2E substate choice was good, though the specific HTR subset (0-swap long-cycle) required 18 moves to finish from DR. Overall, a clean solve achieving sub-35 moves.

**FINAL_SOLUTION**: ["B2", "U2", "L2", "F2", "L2", "D2", "L2", "B2", "U2", "B2", "L'", "D2", "F2", "U2", "B2", "R2", "D2", "R", "F", "L", "F'", "R", "F'", "D2", "F", "U'", "L2", "D", "L", "B"]

*Thinking (31):*

> You're right - I verified the solution but didn't emit the final solution in the required format. Let me output it now.

FINAL_SOLUTION: ["B2", "U2", "L2", "F2", "L2", "D2", "L2", "B2", "U2", "B2", "L'", "D2", "F2", "U2", "B2", "R2", "D2", "R", "F", "L", "F'", "R", "F'", "D2", "F", "U'", "L2", "D", "L", "B"]

**Verified solution (30 moves):** `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`
