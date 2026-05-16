# Solve — fm_PSSSideDayGdansk2026_s3__attempt1_20260516_180648

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`

---

*Thinking (1):*

> The user wants me to solve a Rubik's cube FMC (Fewest Moves Challenge) scramble. I need to start by inspecting the state of the cube in the 'main' slot.
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> I'll begin by calling inspect_state on the main slot to see what I'm working with.

I'll solve this FMC scramble systematically, following the champion's pipeline: inspect → NISS-scout → EO → DR → HTR → finish. Let me start by examining the scramble.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good. I see:
- **UD axis**: 4 bad edges (slots UL, DR, DL, DB) — cleanest EO candidate, but DR-7C3E is poor
- **FB axis**: 8 bad edges — typically a NISS-trace opportunity  
- **RL axis**: 6 bad edges
- **Key signal**: UD has `top_pairs_on_inverse: 3` — strong NISS-switch indicator (≥2 pairs preserved)

Before committing to any EO axis, I'll run the mandatory **niss_scout** to compare all 6 options (normal/inverse × 3 axes) by `expected_total_to_solved`. This is the elite-solver workflow.

I scout EO+DR on both normal and inverse, all three axes — 1 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

**NISS-scout results (6 rows returned, sorted by viability):**

1. **inverse-RL**: EO 5mv (`B' L' D' L2 U'`) + DR-3C2E (F L' F') setup=5, trigger=3 → **total DR 8mv**. **Total: 13 moves to DR**. DR-3C2E is an excellent substate (~5-move HTR finish expected). This is the clear winner.

2-6. All other axes (normal UD/FB, inverse UD/FB, normal RL) show **no DR triggers within max_setup=5** — meaning DR would be >13 moves total, worse than option 1.

**Decision**: Taking **inverse-RL** (row 1). The DR-3C2E trigger family is gold-tier (much better than the DR-7C3E/6C3E I saw on normal), and EO+DR in 13 moves total is excellent. I'll flip to inverse now.

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. The scout told me the EO is `B' L' D' L2 U'` (5 moves) on axis RL. Let me apply that EO sequence now. RL-axis EO is fixed by U/D quarter-turns.

I turn `B' L' D' L2 U'`.

EO applied. Now I need to reach DR on RL-axis. The scout said DR-3C2E with setup=5, trigger=3 (total 8 DR moves). Let me query `dr_trigger_options(axis='RL')` to get the actual setup and trigger moves.

I survey the named DR triggers on RL:
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)
  • DR-3C2E (F L F'): 6-mv setup + 3-mv trigger (9 total)
  • DR-7C8E (F L B): 6-mv setup + 3-mv trigger (9 total)

Perfect! I see 3 DR-trigger options on RL:

1. **DR-3C2E (F L' F')**: setup `U2 F' D2 F R'` (5mv) + trigger `F L' F'` (3mv) = **8 moves to DR**. This matches the scout's recommendation.
2. DR-3C2E (F L F'): 6mv setup + 3mv trigger = 9 moves
3. DR-7C8E (F L B): 6mv setup + 3mv trigger = 9 moves

Taking option 1 as planned. DR-3C2E has excellent HTR finish (~5 moves expected). Applying setup + trigger separately for clear narration.

I turn `U2 F' D2 F R'`.

Setup done (10 moves total so far). Now applying the DR-3C2E trigger `F L' F'`:

I turn `F L' F'`.

DR achieved in 13 moves (5 EO + 8 DR). Now I'm at DR on RL-axis. Let me classify the HTR subset to see what corner pattern I have and how many moves to finish.

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 8 moves, finish is 10 moves (first exposure — learning).

HTR subset identified: **0-swap long-cycle** with cycle structure [4,2,1,1]. The finish breakdown is:
- **HTR reduction**: 8 moves (DR → HTR corners via quarter-turns)
- **Finish**: 10 moves (HTR → solved via half-turns)
- **Total from DR**: 18 moves

This gives me **13 (EO+DR) + 18 (HTR finish) = 31 moves** projected total.

That's longer than ideal but within acceptable range. Let me apply the HTR reduction phase first, checking state between chunks since these are 8 moves (will come in 2 chunks of 4):

For the corner reduction, I see `R' D2 R2 B2` (chunk of a 8-move phase) — apply and re-check.

HTR reduction is 8 moves, showing first 4: `R' D2 R2 B2`. Applying this chunk:

I turn `R' D2 R2 B2`.

17 moves applied. Let me check if I've reached HTR or solved state before continuing:

Quick check: DR-locked on RL, not yet HTR.

Not yet in HTR. Continuing HTR reduction with the next chunk:

For the corner reduction: `U2 F2 D2 L`.

Second chunk of HTR reduction: `U2 F2 D2 L`. Applying:

I turn `U2 F2 D2 L`.

HTR reduction complete (21 moves total). Now applying the finish phase (10 moves, will come in chunks):

For the half-turn finish, I see `B2 U2 B2 L2` (chunk of a 10-move phase) — apply and re-check.

Finish phase first chunk: `B2 U2 B2 L2`. Applying:

I turn `B2 U2 B2 L2`.

25 moves so far. Let me check state before continuing:

Quick check: in HTR.

Good! I'm now in HTR (`is_htr_ud: true`). Let me check if there's a cleaner residual before finishing the last 6 moves:

Residual class: mixed.

Residual is mixed with 2 corner 3-cycles and multiple edge cycles — not insertable. I'll continue with the HTR finish. Querying the next chunk:

For the half-turn finish, I see `D2 L2 F2 L2` (chunk of a 6-move phase) — apply and re-check.

Next chunk: `D2 L2 F2 L2`. Applying:

I turn `D2 L2 F2 L2`.

29 moves. Checking state:

Quick check: in HTR.

Still in HTR, not solved. Getting the final chunk:

For the half-turn finish: `U2 B2`.

Final chunk: `U2 B2`. Applying:

I turn `U2 B2`.

31 moves on the inverse frame. Let me verify this is solved:

A quick glance — the cube is solved.

Excellent! The cube is solved. Now I need to compose the final solution. Since I worked on the inverse frame, I must use `compose_niss_solution` to correctly assemble the normal-frame solution:

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Great! The solution is **30 moves** and verifies correctly. The `compose_niss_solution` tool inverted my 31-move inverse sequence and found 1 move of cancellation, yielding 30 moves total.

Let me verify this solution one more time against the original scramble:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. Let me check my budget status to see if I have time for a refinement attempt:

Budget check: 3498.0s sim, None tool calls remaining.

I have 3498 seconds remaining (97% of budget left). My current solution is 30 moves. Since it's ≥27 moves and I have ample budget, I should attempt one `replace_and_shorten` call to see if I can improve it. The tool enforces a 1-call cap, so I'll try to shorten a large tail section. Let me target the DR+HTR finish portion (moves 6-30, which is 24 moves):

replace_and_shorten: substitute is 2 moves longer; reject.

The `replace_and_shorten` attempt resulted in a **+2 move increase** (26→28), making the total solution 33 moves instead of 30. This is worse, so I'll reject this substitution and keep my original 30-move solution.

**Final solution achieved: 30 moves**

Summary of solve:
- **EO**: 5 moves on inverse-RL axis (`B' L' D' L2 U'`)
- **DR**: 8 moves using DR-3C2E trigger (setup `U2 F' D2 F R'` + trigger `F L' F'`)
- **HTR finish**: 18 moves (8 reduction + 10 finish)
- **Total inverse**: 31 moves → **30 moves after NISS inversion with 1 cancellation**

FINAL_SOLUTION: ["B2", "U2", "L2", "F2", "L2", "D2", "L2", "B2", "U2", "B2", "L'", "D2", "F2", "U2", "B2", "R2", "D2", "R", "F", "L", "F'", "R", "F'", "D2", "F", "U'", "L2", "D", "L", "B"]

**Verified solution (30 moves):** `B2 U2 L2 F2 L2 D2 L2 B2 U2 B2 L' D2 F2 U2 B2 R2 D2 R F L F' R F' D2 F U' L2 D L B`
