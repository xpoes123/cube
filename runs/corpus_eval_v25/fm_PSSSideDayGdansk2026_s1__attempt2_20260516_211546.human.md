# Solve — fm_PSSSideDayGdansk2026_s1__attempt2_20260516_211546

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 28 moves
**Solution**: `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start by inspecting the state of the main slot. Let me begin the solving process following the structured pipeline described in the instructions.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I'll start by calling inspect_state on the main slot to see what I'm working with.

I'll solve this FMC scramble step by step. Let me start by inspecting the cube state to understand what I'm working with.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

Good! I can see the state. Now let me run **niss_scout** to get the comprehensive view of all EO+DR options across both normal and inverse frames for all three axes. This is the mandatory v16 step before committing to any EO.

I scout EO+DR on both normal and inverse, all three axes — 5 viable rows.
  • normal-UD: EO 4mv → DR-4C2E (R U2 R') DR (8mv) [JZP]
  • normal-UD: EO 4mv → DR-7C8E (R' U L) DR (8mv)
  • inverse-FB: EO 5mv → DR-7C8E (U F D) DR (7mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Excellent! The NISS scout gives me a comprehensive comparison. Let me analyze the results:

**Top candidates:**
1. **UD normal**: EO 4mv + DR-4C2E (8mv total DR) → JZP-eligible, finish 21mv = **33 moves total**
2. **UD normal**: EO 4mv + DR-7C8E (8mv total DR) → finish 21mv = **33 moves total**
3. **FB inverse**: EO 5mv + DR-7C8E (7mv total DR) = 12mv to DR (subset uncached, but 7C8E typically finishes in ~10-12)

The UD-normal axis with JZP-eligible DR-4C2E is the top recommendation. The fact that it's **JZP-eligible** is significant — JZP states have dramatically shorter DR paths and better HTR finishes. Even though the cached finish shows 21 moves (giving 33 total), this is a solid starting point.

**Decision**: I'll take **UD normal, 4-move EO into DR-4C2E (JZP)**. The JZP eligibility and clean 8-move DR path makes this the strongest option.

Let me apply the EO moves:

I turn `R2 D' B' F'`.

Good! EO complete in 4 moves. Now let me get the DR trigger options to see the exact setup and trigger for the DR-4C2E path:

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

Perfect! I can see the **DR-4C2E (R U2 R')** option with 5-move setup is JZP-eligible. The setup is: U' R' L2 U F2, then trigger R U2 R'. Total 8 moves to DR.

Let me apply the setup moves:

I turn `U' R' L2 U F2`.

Now applying the DR-4C2E trigger (R U2 R'):

I turn `R U2 R'`.

Excellent! I'm now at DR in 12 moves (4 EO + 8 DR). Let me verify I'm at DR and check the HTR state:

Quick check: DR-locked on UD, not yet HTR.

Good, confirmed at DR on UD axis. Now let me classify the HTR subset to understand what I'm working with:

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (recall).

Interesting! The subset is a **0-swap long-cycle** with cycle structure [3, 2, 2, 1]. The HTR classification shows:
- HTR reduction: 10 moves
- Finish: 9 moves
- Total: 19 moves

This gives me 12 + 19 = 31 moves total, which is better than the scout's cached estimate of 33! Let me apply the HTR reduction phase:

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

The HTR reduction is 10 moves but I can only see 4 at a time. Let me apply this chunk and check if I hit a solved or insertable state:

I turn `U F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Not at HTR yet. Let me get the next chunk of HTR reduction:

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR. Let me get the final chunk of HTR reduction:

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

Excellent! I'm now at HTR (is_htr_ud: true) in 22 moves. Now let me apply the finish phase to solve the cube. According to the classification, the finish should be 9 moves:

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Quick check: in HTR.

Not solved yet. Let me check if there's an insertable 3-cycle residual at this point:

Residual class: mixed.

Mixed residual, not insertable. Let me continue with the finish phase:

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

Quick check: in HTR.

Let me get the last chunk of the finish:

For the half-turn finish: `R2`.

I turn `R2`.

A quick glance — the cube is solved.

Excellent! The cube is solved in 31 moves! Let me now use compose_niss_solution to get the canonical solution with cancellations:

I assemble the canonical normal-frame solution: **30 moves**, verified.

Perfect! The solution cancelled down to **30 moves** (U U2 → U'). Now let me check if I should try replace_and_shorten. According to the rules, I should try r&s if:
- Total moves ≥ 27 ✓ (30 moves)
- Tool calls remaining ≥ 30 ✓ (I've used only ~20 tool calls)
- Haven't already called r&s this run ✓

Let me try replace_and_shorten on a suspicious span. Looking at the solution, the HTR finish section (moves 22-30) seems long. Let me try to shorten it:

Budget check: 3516.0s sim, None tool calls remaining.

Good, I have plenty of time. Let me try replace_and_shorten on the post-DR section (from move 12 onward, which is the HTR section):

replace_and_shorten on the tail span: substitute is 3 moves shorter. Accepted.

Fantastic! Replace_and_shorten found a 3-move improvement! The new solution is **28 moves** and solves the scramble. Let me verify this solution:

verify_solved: ✓ — 28 moves.

Perfect! The solution is verified and complete. Let me check one more time if there are any obvious cancellations:

I check for cancellations — no savings.

No additional cancellations. The solution is **28 moves** and ready to submit.

## Solution Summary

**Approach taken:**
1. **NISS Scout**: Evaluated all 6 axis×frame combinations. Selected UD-normal with 4-move EO leading to JZP-eligible DR-4C2E trigger.
2. **EO (4 moves)**: R2 D' B' F' — achieved edge orientation on UD axis
3. **DR (8 moves)**: U' R' L2 U F2 (setup) + R U2 R' (DR-4C2E trigger) — reached domino reduction in 12 moves total
4. **HTR + Finish (19 moves initially)**: Classified as "0-swap long-cycle" subset, completed HTR reduction (10 moves) and finish (9 moves) for 31 total
5. **Optimization**: Used replace_and_shorten on the HTR section (moves 12-31), which found a 3-move improvement, reducing from 31 to 28 moves

**Final move count: 28 moves**

FINAL_SOLUTION: ["R2", "D'", "B'", "F'", "U'", "R'", "L2", "U", "F2", "R", "U2", "R'", "F2", "D2", "B2", "R2", "D2", "F2", "R2", "U'", "L2", "U", "R2", "B2", "U", "B2", "U'", "F2"]

**Verified solution (28 moves):** `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 F2 R2 U' L2 U R2 B2 U B2 U' F2`
