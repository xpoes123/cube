# Solve — fm_PSSSideDayGdansk2026_s1__attempt6_20260517_011457

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 28 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`

---

*Thinking (1):*

> Let me analyze the situation. I have five prior attempts:
> - Attempt 1: 30 moves
> - Attempt 2: 25 moves (best)
> - Attempt 3: 29 moves
> - Attempt 4: 29 moves (duplicate of 3)
> - Attempt 5: 31 moves
> 
> The best is 25 moves. The instruction is clear: COMMIT HARD this attempt. Pick a line and drive it to completion. Don't over-ideate or abandon halfway.
> 
> Let me start by inspecting the state to understand the scramble, then quickly scout EO options and commit to one path.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> Let me begin with inspect_state to see what we're working with.

I'll solve this scramble systematically. With prior attempts ranging from 25-31 moves, my goal is to find a clean path and execute it fully. Let me start by inspecting the state.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Observation:** Bad edges: UD=8, FB=6, RL=6. All axes need substantial EO work. UD has 8 bad edges (all-bad-minus-4), FB and RL both have 6. DR closeness shows UD has DR-6C3E, FB has DR-5C2E, RL has DR-7C3E. The UD axis has `top_pairs_on_inverse=2`, which signals a potential NISS opportunity.

**Strategy:** I'll scout EO on all three axes on both normal and inverse frames, then commit to the best joint EO+DR path. Let me start by checking EO patterns on each axis.

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

**EO on normal side:**
- UD: 4 moves complete (R2 D' B' F')
- FB: 5 moves total (first 4 shown: R2 B' L' U2)
- RL: 5 moves total (first 4 shown: L U L2 R)

The UD axis has the shortest EO at 4 moves. But I should also check the inverse frame, especially since `top_pairs_on_inverse=2` for UD.

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check EO on the inverse frame.

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

**EO on inverse side:**
- UD: 5 moves total
- FB: 5 moves total
- RL: 5 moves total

All axes on inverse are 5 moves. On normal, UD is 4 moves (shortest). Let me flip back to normal and proceed with the UD-normal EO. Then I'll check DR options.

NISS flip — switching back to the normal scramble.

Back on normal. I'll commit to UD-axis EO (4 moves: R2 D' B' F'), then probe DR.

I turn `R2 D' B' F'`.

EO committed (4 moves). Now let me check DR trigger options on the UD axis.

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)

**DR options on UD:**
1. **DR-4C2E (R U2 R')**: 5 setup + 3 trigger = 8 total to DR. **JZP-eligible**! This is huge. JZP means the post-DR cost is roughly halved (5-7 moves instead of 9-11).
2. DR-7C8E (R' U L): 5 setup + 3 trigger = 8 total to DR, NOT JZP-eligible.

The 4C2E with JZP is clearly better. Total to DR: 4 (EO) + 8 (DR) = 12 moves. Expected post-DR with JZP: ~5-7 moves. Total projection: 17-19 moves.

Let me commit to this DR path.

I turn `U' R' L2 U F2`.

Setup applied (9 moves total). Now the DR-4C2E trigger: R U2 R'.

I turn `R U2 R'`.

DR trigger applied (12 moves total). Let me verify we're at DR and classify the HTR state.

Quick check: DR-locked on UD, not yet HTR.

Good! We're at DR on UD. Not at HTR yet. Let me classify the HTR subset.

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (recall).

**HTR classification:** 0-swap long-cycle subset. HTR reduction: 10 moves, finish: 9 moves. Total: 19 moves from DR.

**Current total:** 12 (to DR) + 19 (HTR+finish) = 31 moves projected.

This is longer than my best prior (25 moves). Let me apply the HTR reduction and check if there's a 3-cycle residual partway through that I can exploit with a commutator.

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

Partial HTR reduction (4 of 10 moves shown). Let me apply and check state.

I turn `U F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Not yet at HTR. Continue reduction.

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR. Continue.

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

Good! We're now at HTR (all axes EO, DR, and is_htr_ud=true). 22 moves so far. Now the finish phase.

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Auto-cancelled saved 1 move! (U and U2 combined to U'). 25 moves so far. Let me check if solved.

Quick check: in HTR.

Not solved yet. Continue finish.

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

29 moves. Let me check again.

Quick check: in HTR.

Still not solved. Let me check if there's a 3-cycle residual.

Residual class: mixed.

Mixed residual: 2 corner 2-cycles and 2 edge 2-cycles. Not a 3-cycle. Let me continue with the finish phase.

For the half-turn finish: `R2`.

I turn `R2`.

30 moves. Let me check if solved.

A quick glance — the cube is solved.

**Solved!** 30 moves. This matches my first prior attempt. Let me now use `compose_niss_solution` to get the canonical form and verify.

I assemble the canonical normal-frame solution: **30 moves**, verified.

I have a 30-move solve. My best prior was 25 moves. Let me check the budget and see if I should try `replace_and_shorten`.

Budget check: 3518.0s sim, None tool calls remaining.

I have plenty of budget. The solution is 30 moves, which is ≥27. The tool calls so far are minimal. Let me try `replace_and_shorten` on a large span to see if I can improve.

Looking at the solution, the last 10 moves are: "F2 U' B2 F2 L2 B2 L2 U2 B2 R2" — this is the finish phase. Let me try to replace and shorten a span from the DR point onward. The DR happens at move 12, so I'll try replacing moves 12-30.

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

**Excellent!** `replace_and_shorten` saved 2 moves. The new solution is 28 moves and still solves the scramble. Let me update the main slot with this new history.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`.

I assemble the canonical normal-frame solution: **28 moves**, verified.

Perfect! I have a 28-move verified solution. Let me verify it one more time explicitly.

verify_solved: ✓ — 28 moves.

**Verified!** 28 moves. This is better than attempts 1, 3, 4, and 5 (30, 29, 29, 31), though not quite as good as attempt 2 (25 moves). But it's a solid, verified solution.

**FINAL_SOLUTION:**

["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]

## Solution breakdown:
- **EO (UD-axis, 4 moves):** R2 D' B' F' — fixes all 8 bad edges on UD
- **DR setup (5 moves):** U' R' L2 U F2 — setup to DR-4C2E trigger
- **DR trigger (3 moves):** R U2 R' — DR-4C2E with JZP
- **Post-DR to solved (16 moves via replace_and_shorten):** F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2

**Total: 28 moves**

*Thinking (39):*

> The user is right - I verified the solution but didn't actually emit the FINAL_SOLUTION in the required format. I need to output it now.
> 
> I have a verified 28-move solution:
> ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]
> 
> I should emit this now.

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]

**Verified solution (28 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`
