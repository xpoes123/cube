# Solve — fm_PSSSideDayGdansk2026_s1__attempt8_20260517_144552

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 28 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`

---

*Thinking (1):*

> The user wants me to solve this FMC scramble. I have context from 7 prior attempts, with the best being 28 moves. The instruction is clear: COMMIT HARD this time - pick a line and drive it to completion without over-ideating between branches.
> 
> Let me start by inspecting the state to see the bad edges per axis and other key information.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> Let me begin with inspect_state on slot 'main'.

I'll solve this FMC scramble systematically. Given the prior attempts achieved 28-33 moves, I'll commit hard to a promising line and drive it to completion.

Let me start by inspecting the scrambled state:

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Initial State Analysis:**

Bad edges per axis: UD=8, FB=6, RL=6. This is an 8-bad UD state, suggesting NISS to inverse might give a cleaner EO. The DR-closeness shows:
- UD: DR-6C3E (not ideal), but `top_pairs_on_inverse=2` — strong NISS signal
- FB: DR-5C2E (better substate)
- RL: DR-7C3E (worst)

Strategy: The 8-bad UD edge count typically responds well to NISS. With `top_pairs_on_inverse=2` on UD, I should check the inverse frame first. Let me flip to inverse and scout EO options on multiple axes.

NISS flip — switching to the inverse scramble.

Now on inverse. The bad-edge counts remain the same (NISS invariant), but the EO solutions will differ. Let me scout EO on inverse-UD first (since normal-UD had 8 bad edges + 2 pairs on inverse):

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

Inverse-UD EO = 5 moves (partial shown). That's reasonable for 8-bad. Let me also check inverse-FB and inverse-RL before committing:

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

All three inverse axes show 5-move EOs. Let me flip back to normal and check the normal-side EOs for comparison:

NISS flip — switching back to the normal scramble.

Back on normal. Let me scout normal-side EO options:

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

**EO Comparison:**
- Normal-UD: **4 moves** (R2 D' B' F') — complete!
- Normal-FB: 5 moves (partial)
- Normal-RL: 5 moves (partial)
- All inverse axes: 5 moves

Normal-UD with 4 moves is the shortest. Now I need to probe DR after each candidate to make the joint decision. Let me probe DR for normal-UD:

I probe what DR would look like if I applied this EO (without committing).

Normal-UD: 4 EO + 8 DR = 12 moves to DR. That's acceptable (≤15 is good). Let me commit to this line and drive it through. Applying the 4-move EO:

I turn `R2 D' B' F'`.

**EO committed** (normal-UD, 4 moves). The setup `R2 D' B' F'` uses opposite flipping faces F and B to handle the 8-bad configuration symmetrically. Now I need to find DR on UD axis. Using dr_trigger_options to get all DR options with their substates:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP] pre=DR-4C1E
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

**DR Options Found:**
1. **DR-4C2E (R U2 R')**: setup 5mv, trigger 3mv, **total 8mv to DR**, **JZP-eligible** ✓
2. DR-7C8E (R' U L): setup 5mv, trigger 3mv, total 8mv, not JZP

The first option is **JZP-eligible DR-4C2E** in 8 moves. According to the DR-substate priors table, JZP-eligible 4C2E typically finishes in **5-7 moves** post-DR. So expected total: 4 EO + 8 DR + ~6 finish ≈ **18 moves**. That's excellent!

Committing to DR-4C2E (JZP). Setup first:

I turn `U' R' L2 U F2`.

Setup applied (5 moves). Now the trigger `R U2 R'`:

I turn `R U2 R'`.

**DR achieved** (12 moves total: 4 EO + 8 DR). This is a JZP-eligible DR-4C2E state — excellent substate quality. Now I'll classify the HTR subset and complete the finish:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (recall).

**HTR Subset identified:** 0-swap long-cycle (cycle structure [3,2,2,1]). The finish is:
- HTR reduction: 10 moves
- Finish: 9 moves
- **Total post-DR: 19 moves**

Wait — that's much worse than expected! The DR-substate priors table suggested JZP-eligible 4C2E should finish in ~5-7 moves, but I'm seeing 19 moves here. This is a bad outcome. Let me check if there's an opportunistic 3-cycle residual during the finish. Let me apply the HTR reduction in chunks and check:

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

Partial HTR reduction (4 of 10). Let me apply and check for residuals:

I turn `U F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Not solved yet, not in HTR yet. Let me continue the HTR reduction:

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not in HTR. Continue:

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

**HTR achieved** (22 moves). Now in HTR-corner-subgroup. Let me apply the finish phase:

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Quick check: in HTR.

Good! Auto-cancelled 1 move (U + U2 = U'). Currently at 25 moves, still not solved. Let me check for a 3-cycle residual:

Residual class: mixed.

Not a clean 3-cycle — mixed residual with 6 corners and 9 edges unsolved. Let me continue the finish:

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

Quick check: in HTR.

29 moves, still not solved. Let me check for a 3-cycle now:

Residual class: mixed.

Still mixed (2 corner 2-cycles and 2 edge 2-cycles). Not a pure 3-cycle. Let me finish:

For the half-turn finish: `R2`.

I turn `R2`.

A quick glance — the cube is solved.

**SOLVED!** 30 moves. This matches my 6th prior attempt. Let me verify and then look for cancellations:

I assemble the canonical normal-frame solution: **30 moves**, verified.

Solution verified (30 moves). Now I need to check if I can use replace_and_shorten. The gates are: total_moves ≥ 27 (yes, 30 ≥ 27), and I need ≥ 30 tool calls remaining. Let me check budget:

Budget check: 3256.68s sim, None tool calls remaining.

Good, plenty of budget remaining (3256s sim, plenty of real-wall time). I have a 30-move solution. According to the rules, I should try replace_and_shorten ONCE on a large tail span since I'm ≥27 moves. Let me target the DR-to-finish span (moves 12-30, indices 12-30):

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

**replace_and_shorten SUCCESS!** Saved 2 moves. New solution is **28 moves**, matching my best prior attempt. The substitute reduced the post-DR finish from 18 to 16 moves. Let me verify this new solution:

verify_solved: ✓ — 28 moves.

**VERIFIED!** 28-move solution. This matches my best prior attempt. Let me check for any cancellations to see if we can squeeze out one more move:

I check for cancellations — no savings.

No further cancellations found. The solution is already optimally cancelled at 28 moves. This matches my best prior attempt.

**FINAL SOLUTION:**

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]

**Solution breakdown:**
- **EO (normal-UD, 4 moves):** R2 D' B' F' — symmetric opposite-flipping-face pattern for 8-bad edges
- **DR (8 moves):** U' R' L2 U F2 R U2 R' — setup into JZP-eligible DR-4C2E trigger
- **HTR + Finish (16 moves, after replace_and_shorten):** F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2

**Total: 28 moves** (ties best prior attempt)

**Verified solution (28 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`
