# Solve — fm_PSSSideDayGdansk2026_s2__attempt2_20260517_095459

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 29 moves
**Solution**: `U' F2 U L2 U2 L2 F2 U R2 D U2 B2 U2 R2 D2 U2 F2 R U2 L U R L2 U D F U' R2 B'`

---

*Thinking (1):*

> The user wants me to solve the scramble within the one-hour budget. They've given context that the previous attempt achieved 32 moves.
> 
> Key instructions:
> 1. Start with inspect_state(slot='main')
> 2. COMMIT HARD - pick one line and drive it to completion
> 3. Don't over-ideate or abandon paths halfway
> 4. A complete 30-move solution is better than an incomplete attempt
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I need to:
> 1. Inspect the state to understand the initial conditions
> 2. Scout EO options quickly but decisively
> 3. Pick an axis and commit
> 4. Drive through DR → HTR → finish
> 5. Submit a complete solution
> 
> Let me start by inspecting the main state.

I'll solve this scramble with a committed, decisive approach. Let me start by inspecting the initial state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**Initial state analysis:**
- **bad_edges_per_axis**: UD=6, FB=4, RL=4 — FB and RL both have 4 bad edges, which is in the strong 1-3 move EO range
- **UD has 3 pairs on inverse** — strong NISS signal (Wen's pairs tracing: ≥2 pairs preserved suggests inverse is viable)
- **DR closeness**: all axes show 6-7 misoriented corners (poor), but RL has only 6C2E which is slightly better structurally

**Strategy**: Given the prior 32-move solve, I need to find a cleaner path. The 4 bad edges on FB and RL are promising. Let me scout EO on both FB and RL axes, then also check the inverse side for UD (since it has 3 pairs on inverse).

Starting with **FB axis EO** (4 bad edges on DR, DL, FR, BL):

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

**FB-axis EO**: 4 moves `B2 L2 U2 R'`. Now check **RL axis EO** (4 bad edges on UL, DR, DF, FR):

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

**RL-axis EO**: 4 moves `R2 B F2 U'`. Both FB and RL give 4-move EOs. Now let me check **inverse-UD** (6 bad edges but 3 pairs on inverse):

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

**Inverse-UD EO**: also 4 moves `B R2 U F'`. All three candidates (FB-normal, RL-normal, UD-inverse) give 4-move EOs. Now I need to **probe DR** for each to make the joint decision:

NISS flip — switching back to the normal scramble.

Back on normal. Let me probe DR for **FB-normal** first:

I probe what DR would look like if I applied this EO (without committing).

**FB-normal**: EO=4, DR=8, total=12. Now probe **RL-normal**:

I probe what DR would look like if I applied this EO (without committing).

**RL-normal**: EO=4, DR=8, total=12. Now probe **UD-inverse**:

NISS flip — switching to the inverse scramble.

I probe what DR would look like if I applied this EO (without committing).

**UD-inverse**: EO=4, DR=8, total=12. All three candidates tie at 12 moves to DR! This is unusual. Let me commit to **UD-inverse** because it had 3 pairs on inverse (strong NISS signal) and staying on inverse might yield a cleaner substate. Applying the EO:

I turn `B R2 U F'`.

**EO complete on UD-inverse** (4 moves). Now finding DR triggers on UD axis:

DR trigger menu on UD: no named trigger fits within 5 setup moves.

**No DR triggers found within 5 moves!** This is a bad signal. Let me use dr_recognize as fallback:

I check whether the DR is recognizable from this state via the library.

DR is 8 moves total, which matches the probe. Let me apply the 4 setup moves:

I turn `D' U' L2 R'`.

I check whether the DR is recognizable from this state via the library.

The remaining 4 moves break down as 3-move setup + 1-move `R'` trigger. Applying:

I turn `U' L' U2 R'`.

**DR complete** at 12 moves (4 EO + 8 DR). Now classifying HTR:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 10 moves (first exposure — learning).

**HTR subset**: 2-swap long-cycle. HTR reduction = 11 moves, finish = 10 moves, total = 21 moves. Full solve projection: 12 (to DR) + 21 = **33 moves**. This is similar to the prior 32-move attempt. Let me proceed and see if I can improve during the finish. Applying HTR reduction:

For the corner reduction, I see `U2 R2 U' B2` (chunk of a 11-move phase) — apply and re-check.

I turn `U2 R2 U' B2`.

Let me check state with quick_check before continuing:

Quick check: DR-locked on UD, not yet HTR.

Not in HTR yet. Continuing HTR reduction:

For the corner reduction, I see `U R2 U2 F2` (chunk of a 7-move phase) — apply and re-check.

I turn `U R2 U2 F2`.

Quick check: DR-locked on UD, not yet HTR.

Still not HTR. Continuing:

For the corner reduction: `U' F2 U`.

I turn `U' F2 U`.

Quick check: in HTR.

**HTR complete** at 23 moves. Now applying finish phase:

For the half-turn finish, I see `L2 F2 D2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `L2 F2 D2 R2`.

Quick check: in HTR.

Continuing finish:

For the half-turn finish, I see `F2 R2 F2 D2` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 R2 F2 D2`.

Quick check: in HTR.

For the half-turn finish: `U2 R2`.

I turn `U2 R2`.

A quick glance — the cube is solved.

**Solved!** at 33 moves on inverse. Now I need to compose the NISS solution using compose_niss_solution:

I assemble the canonical inverse-frame solution: **33 moves**, verified.

**Solution found: 33 moves**. This is 1 move longer than the prior best (32 moves). Given that I have a complete solution and it's close to the prior attempt, let me check if I should try replace_and_shorten. Current status:

- 33 moves total
- I have budget remaining (need ≥30 tool calls for r&s)

Let me check budget:

Budget check: 3493.0s sim, None tool calls remaining.

I have plenty of budget (3493s remaining). Since the solution is 33 moves (≥27) and I have tool calls remaining, I should try replace_and_shorten on a large chunk. Let me target the second half of the solution (the HTR finish region tends to have the most redundancy):

replace_and_shorten on the tail span: substitute is 4 moves shorter. Accepted.

**Excellent!** replace_and_shorten saved **4 moves**, reducing from 33 to **29 moves**. The new history solves the scramble. Let me verify this solution:

I assemble the canonical inverse-frame solution: **33 moves**, verified.

Wait, compose_niss_solution still shows 33 moves. This is because the tool is reading the OLD history in the slot. Let me manually apply the new history. Actually, I need to reset and apply the new shortened history:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B R2 U F' D' U' L2 R' U' L' U2 R' F2 U2 D2 R2 U2 B2 U2 D' R2 U' F2 L2 U2 L2 U' F2 U`.

I assemble the canonical inverse-frame solution: **29 moves**, verified.

**Perfect!** The solution is **29 moves** and solves the scramble. This is a **3-move improvement** over the prior best (32 moves). Let me verify it one final time:

verify_solved: ✓ — 29 moves.

**VERIFIED: 29 moves**. This is a complete, clean solution that beats the prior best by 3 moves.

## Summary

**Final Solution Path:**
1. **EO**: 4 moves on UD-inverse (`B R2 U F'`) — chose inverse due to 3 pairs on inverse signal
2. **DR**: 8 moves (`D' U' L2 R' U' L' U2 R'`) — single inverse trigger (DR-4C4E family)
3. **HTR**: 11 moves of corner reduction → HTR subset "2-swap long-cycle"
4. **Finish**: 10 moves initial → reduced to 6 moves via replace_and_shorten
5. **Optimization**: replace_and_shorten on moves 12-33 saved 4 moves

**Total: 29 moves** (verified)

FINAL_SOLUTION: ["U'", "F2", "U", "L2", "U2", "L2", "F2", "U", "R2", "D", "U2", "B2", "U2", "R2", "D2", "U2", "F2", "R", "U2", "L", "U", "R", "L2", "U", "D", "F", "U'", "R2", "B'"]

**Verified solution (29 moves):** `U' F2 U L2 U2 L2 F2 U R2 D U2 B2 U2 R2 D2 U2 F2 R U2 L U R L2 U D F U' R2 B'`
