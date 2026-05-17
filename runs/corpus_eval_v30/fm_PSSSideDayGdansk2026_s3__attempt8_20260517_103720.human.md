# Solve — fm_PSSSideDayGdansk2026_s3__attempt8_20260517_103720

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 27 moves
**Solution**: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`

---

*Thinking (1):*

> The user wants me to solve this FMC scramble. I have prior attempts showing 27-30 moves. The best is 27 moves. The instruction is to COMMIT HARD - pick a line and drive it to finish without over-ideating.
> 
> Looking at the prior attempts:
> - Attempts 1-3: all identical 30-move solutions
> - Attempts 4-5, 7: identical 27-move solutions
> - Attempt 6: 28 moves
> 
> The 27-move solutions appear to be the best path. Let me start by inspecting the state to understand the scramble, then decide on an approach.
> 
> I should:
> 1. inspect_state to see bad edges per axis
> 2. Scout EO on different axes (including inverse)
> 3. Pick the most promising EO+DR combination
> 4. Execute through DR → HTR → finish
> 5. Use compose_niss_solution before final submission
> 
> Let me start.

I'll solve this scramble methodically, committing to the best line I find. Let me start by inspecting the scrambled state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good! I can see:
- **UD axis**: 4 bad edges (UL, DR, DL, DB) — shortest EO, but DR-7C3E (bad substate)
- **FB axis**: 8 bad edges — longer EO
- **RL axis**: 6 bad edges — medium EO
- **Important**: UD has `top_pairs_on_inverse: 3` — strong NISS signal!

Let me scout EO on UD-normal first, then check UD-inverse since the pairs-tracing count is high.

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

UD-normal EO is 4 moves: `U L R' B'`. Now let me check the inverse frame because of the 3 pairs signal.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

Inverse UD EO is also 4 moves: `B' R' U B'`. Same length as normal. But 3 pairs on inverse is a strong signal. Let me probe DR on both sides to decide.

I probe what DR would look like if I applied this EO (without committing).

Inverse: 4 EO + 9 DR = 13 moves to DR. Let me flip back to normal and probe that.

NISS flip — switching back to the normal scramble.

I probe what DR would look like if I applied this EO (without committing).

Normal: 4 EO + 8 DR = 12 moves to DR. That's 1 move better than inverse, but 3 pairs on inverse suggests the inverse might have a cleaner finish. Let me check FB axis too before committing.

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

FB-normal EO is also 4 moves! Let me probe DR on FB.

I probe what DR would look like if I applied this EO (without committing).

FB-normal: 4 EO + 7 DR = 11 moves to DR. That's the best so far! Let me commit to FB-normal axis. This matches the pattern of the 27-move prior attempts which likely used this axis.

I turn `R' F D L'`.

Good! FB-axis EO complete in 4 moves: `R' F D L'`. Now let me get DR trigger options on FB axis.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

Hmm, no trigger options found within 5 moves setup. Let me use dr_recognize as fallback.

I check whether the DR is recognizable from this state via the library.

DR requires 7 moves total, I can see the first 4 setup moves: `B' D F' U'`. Let me apply them.

I turn `B' D F' U'`.

Now let me recognize the DR trigger from this position.

I check whether the DR is recognizable from this state via the library.

Great! 2-move setup + 1-move trigger: `B L2 D'`. Total DR = 4+4+3 = 11 moves. Let me apply the setup and trigger.

I turn `B L2`.

I turn `D'`.

Excellent! I'm at DR in 11 moves on FB axis. Now let me classify the HTR subset and complete the finish.

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 8 moves, finish is 9 moves (recall).

This is a "4-swap long-cycle" subset. HTR reduction is 8 moves, finish is 9 moves, total 17 moves from DR. That gives me 11 + 17 = 28 moves total. Let me execute the HTR reduction first, checking state between chunks.

For the corner reduction, I see `D2 F2 R2 U2` (chunk of a 8-move phase) — apply and re-check.

First 4 moves of HTR reduction: `D2 F2 R2 U2`. Let me apply and check state.

I turn `D2 F2 R2 U2`.

Quick check: DR-locked on FB, not yet HTR.

Not solved yet, still at DR on FB. Let me get the next chunk of HTR reduction.

For the corner reduction: `F' U2 L2 B`.

Next 4 moves: `F' U2 L2 B`. Let me apply and check again.

I turn `F' U2 L2 B`.

Quick check: in HTR.

Great! Now I'm at HTR (is_htr_ud: true). 18 moves so far. Now let me apply the finish phase to solve.

For the half-turn finish, I see `R2 U2 B2 R2` (chunk of a 9-move phase) — apply and re-check.

First 4 moves of finish: `R2 U2 B2 R2`. Let me apply and check.

I turn `R2 U2 B2 R2`.

Quick check: in HTR.

Still not solved. Let me check if there's a 3-cycle residual I can exploit.

Residual class: mixed.

Not a pure 3-cycle, still many pieces unsolved. Let me continue with the finish phase.

For the half-turn finish, I see `F2 U2 B2 D2` (chunk of a 5-move phase) — apply and re-check.

Next 4 moves: `F2 U2 B2 D2`. Let me apply and check.

I turn `F2 U2 B2 D2`.

Quick check: in HTR.

Still not solved, at 26 moves. Let me get the last move of the finish.

For the half-turn finish: `F2`.

Final move: `F2`. Let me apply and verify it's solved.

I turn `F2`.

A quick glance — the cube is solved.

Perfect! The cube is solved in 27 moves. Now let me compose the solution and verify it.

I assemble the canonical normal-frame solution: **27 moves**, verified.

Excellent! I have a 27-move solution that matches my best prior attempts. Since I have tool calls remaining and the solution is ≥27 moves, let me try replace_and_shorten to see if I can improve it.

Budget check: 3516.0s sim, None tool calls remaining.

I have plenty of time and tool calls remaining. Let me try replace_and_shorten on a large span to see if I can improve the solution. I'll target the DR-to-finish section (moves 11-27).

replace_and_shorten: substitute is 3 moves longer; reject.

Replace_and_shorten made the solution worse (delta +3), so I'll keep my original 27-move solution. Let me verify it one more time.

verify_solved: ✓ — 27 moves.

Perfect! My solution is verified at 27 moves, matching the best prior attempts.

## FINAL_SOLUTION

**Solution breakdown:**
- **EO on FB axis** (4 moves): `R' F D L'` — recognized the 8-bad-edge pattern, found the 4-move fix
- **DR setup + trigger** (7 moves): `B' D F' U' B L2 D'` — setup through RZP to single-move trigger
- **HTR reduction** (8 moves): `D F2 R2 U2 F' U2 L2 B` — reducing to HTR corner subgroup (4-swap long-cycle)
- **HTR finish** (9 moves): `R2 U2 B2 R2 F2 U2 B2 D2 F2` — half-turn only finish to solved

**Total: 27 moves** (FB-axis solve, 4-swap long-cycle subset)

**Move-count decomposition:**
- EO: 4 moves
- DR: 11 moves (4 EO + 7 RZP-to-trigger)
- HTR reduction: 8 moves
- Finish: 9 moves
- **Total: 4 + 7 + 8 + 9 = 28 → 27** (one move saved via auto-cancel during apply)

FINAL_SOLUTION: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

**Verified solution (27 moves):** `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
