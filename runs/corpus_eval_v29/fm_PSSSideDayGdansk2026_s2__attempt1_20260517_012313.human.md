# Solve — fm_PSSSideDayGdansk2026_s2__attempt1_20260517_012313

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 33 moves
**Solution**: `R2 U2 D2 F2 R2 F2 R2 D2 F2 L2 U' F2 U F2 U2 R2 U' B2 U R2 U2 R U2 L U R L2 U D F U' R2 B'`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble. I need to start by inspecting the state of the main slot to understand what I'm working with.
> 
> Let me begin by calling inspect_state on the main slot to see the bad edges per axis, DR closeness, HTR state, and other relevant information.

I'll solve this FMC scramble step by step, starting with inspecting the cube state to understand the edge orientation and DR options across all axes.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good! I can see the scramble state:
- **Bad edges**: UD=6, FB=4, RL=4
- **FB and RL both have 4 bad edges** — these are the easiest EO targets (potentially 1-3 moves)
- **UD has 6 bad edges** — typically 2-4 moves
- **DR closeness**: All axes show poor DR states (7C3E, 7C2E, 6C2E), BUT UD has **3 pairs on inverse** — a strong NISS signal
- **JZP**: none eligible on normal side

The 3 pairs on inverse for UD is significant. Let me scout EO options on both normal and inverse frames.

**Strategy**: I'll check FB-axis EO (4 bad edges) on normal, then flip to inverse and check UD-axis EO (since it has 3 pairs preserved). I'll probe DR for each viable candidate before committing.

Let me start by scouting FB-axis EO on the normal side:

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

FB-axis EO is **4 moves** (B2 L2 U2 R'). Now let me check RL-axis EO on normal (also 4 bad edges):

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

RL-axis EO is also **4 moves** (R2 B F2 U'). Now let me flip to inverse and scout UD-axis EO (6 bad edges on normal, but inverse might be better given the 3 pairs signal):

NISS flip — switching to the inverse scramble.

Now I'm on the inverse frame. Let me inspect the state and scout UD-axis EO:

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.
I'm currently working on the inverse scramble.

Interesting — on inverse the bad edge counts are the same (UD=6, FB=4, RL=4). Let me scout UD-axis EO on inverse:

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

Inverse UD-axis EO is **4 moves** (B R2 U F'). All three candidate axes have 4-move EOs. Now I need to compare their DR substates. Since I have 3 pairs on inverse for UD-axis, let me probe DR after this inverse-UD EO:

I probe what DR would look like if I applied this EO (without committing).

Inverse-UD: 4 EO + 8 DR = **12 moves to DR**. That's acceptable (sub-15 target). Let me flip back to normal and probe FB-axis DR:

NISS flip — switching back to the normal scramble.

Back on normal. Now let me probe FB-axis DR:

I probe what DR would look like if I applied this EO (without committing).

Normal-FB: 4 EO + 8 DR = **12 moves to DR**. Same as inverse-UD. Let me also probe RL-axis DR on normal:

I probe what DR would look like if I applied this EO (without committing).

Normal-RL: 4 EO + 8 DR = **12 moves to DR**. All three are tied at 12 moves to DR. The tiebreaker is the **3 pairs on inverse** for UD-axis — that's a strong NISS signal. I'll commit to **inverse-UD**.

Let me flip back to inverse and commit the EO:

NISS flip — switching to the inverse scramble.

Now I'm on inverse. Applying the 4-move UD-axis EO (B R2 U F'):

I turn `B R2 U F'`.

Good! EO complete in 4 moves on inverse. Now let me use dr_trigger_options to find the best DR path on UD-axis:

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Hmm, dr_trigger_options returned no options within 5 setup moves. Let me fall back to dr_recognize:

I check whether the DR is recognizable from this state via the library.

DR is 8 moves total. I can see the first 4 setup moves (D' U' L2 R'). Let me apply them and re-query:

I turn `D' U' L2 R'`.

Now let me check what's left in the DR:

I check whether the DR is recognizable from this state via the library.

Good! The remaining DR is 4 moves: 3-move setup (U' L' U2) + 1-move trigger (R'). This is the classic **R-trigger DR-4C4E** pattern. Total to DR: 4 EO + 8 DR = **12 moves**. Let me apply the setup and trigger:

I turn `U' L' U2`.

I turn `R'`.

Excellent! DR reached in 12 moves on the inverse side. Now let me classify the HTR state and finish:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 10 moves (first exposure — learning).

The HTR subset is **2-swap long-cycle** with an 11-move HTR reduction + 10-move finish = **21 moves** from DR. Total so far: 12 (to DR) + 21 (HTR+finish) = **33 moves**. That's acceptable, but let me apply the HTR reduction in chunks and check for early residuals with quick_check:

For the corner reduction, I see `U2 R2 U' B2` (chunk of a 11-move phase) — apply and re-check.

HTR reduction is 11 moves; I see the first 4 (U2 R2 U' B2). Let me apply and check:

I turn `U2 R2 U' B2`.

Quick check: DR-locked on UD, not yet HTR.

Not at HTR yet. Let me continue the reduction:

For the corner reduction, I see `U R2 U2 F2` (chunk of a 7-move phase) — apply and re-check.

I turn `U R2 U2 F2`.

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR. Let me continue:

For the corner reduction: `U' F2 U`.

I turn `U' F2 U`.

Quick check: in HTR.

Great! I'm now at HTR (is_htr_ud: true) in 23 moves. Now let me apply the finish phase:

For the half-turn finish, I see `L2 F2 D2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `L2 F2 D2 R2`.

Quick check: in HTR.

Not solved yet. Let me continue the finish:

For the half-turn finish, I see `F2 R2 F2 D2` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 R2 F2 D2`.

Quick check: in HTR.

Still not solved. Let me get the last chunk:

For the half-turn finish: `U2 R2`.

I turn `U2 R2`.

A quick glance — the cube is solved.

Perfect! The cube is solved on the inverse side in **33 moves**. Now I need to compose the final solution using compose_niss_solution, which will properly invert the inverse-side moves and assemble the canonical normal-frame solution:

I assemble the canonical inverse-frame solution: **33 moves**, verified.

Excellent! I have a **33-move solution** that solves the scramble. Let me verify it:

verify_solved: ✓ — 33 moves.

Perfect! The solution is verified. Now, since my solution is **33 moves** (≥27) and I have plenty of tool calls remaining, I should check if replace_and_shorten can improve it. Let me check my budget:

Budget check: 3488.0s sim, None tool calls remaining.

I have plenty of budget (3488s remaining). Since the solution is 33 moves (≥27), I'm allowed to try replace_and_shorten. However, the current slot is on inverse, so I need to work with the normal-frame solution. Let me create a new slot with the normal-frame solution:

I create a fresh slot `refine` for an alternate branch.

Now let me apply the normal-frame solution to this slot:

I turn `R2 U2 D2 F2 R2 F2 R2 D2 F2 L2 U' F2 U F2 U2 R2 U' B2 U R2 U2 R U2 L U R L2 U D F U' R2 B'`.

Good! Now let me try replace_and_shorten on a large tail span. Looking at the solution, I'll try to shorten the last 25 moves (from index 8 to 33):

replace_and_shorten: same length, no improvement.

The replace_and_shorten found the same sequence (delta = 0), so no improvement. Let me try a different span — perhaps the middle section. Let me try from index 4 to 29:

Actually, wait. I've already used my 1 replace_and_shorten call (rs_calls_used: 1), and the tool enforces a 1-call cap. So I cannot call it again.

Since the solution is verified at 33 moves and I cannot improve it further with replace_and_shorten, I should submit this solution now.

Let me check for any obvious cancellations by calling cancel on the solution:

I check for cancellations — no savings.

No cancellations found. The solution is already optimal in terms of move cancellation. Let me verify it one more time and then submit:

verify_solved: ✓ — 33 moves.

Perfect! The solution is verified and solves the scramble in **33 moves**.

## Solution Summary

**Approach:** Inverse-UD axis (chosen for 3 pairs on inverse signal)
- **EO (inverse):** 4 moves — B R2 U F'
- **DR (inverse):** 8 moves — D' U' L2 R' U' L' U2 R' (total: 12 moves to DR)
- **HTR subset:** 2-swap long-cycle
  - HTR reduction: 11 moves
  - Finish: 10 moves
- **Total:** 33 moves

The solution uses the NISS technique (solving on the inverse frame), which allowed me to leverage the 3 pairs preserved on inverse. The final solution was assembled correctly by compose_niss_solution.

**FINAL_SOLUTION:** ["R2", "U2", "D2", "F2", "R2", "F2", "R2", "D2", "F2", "L2", "U'", "F2", "U", "F2", "U2", "R2", "U'", "B2", "U", "R2", "U2", "R", "U2", "L", "U", "R", "L2", "U", "D", "F", "U'", "R2", "B'"]

*Thinking (47):*

> The user is right - I verified the solution and said I would submit it, but I didn't actually emit the FINAL_SOLUTION. I need to output it now.
> 
> The solution is:
> ["R2", "U2", "D2", "F2", "R2", "F2", "R2", "D2", "F2", "L2", "U'", "F2", "U", "F2", "U2", "R2", "U'", "B2", "U", "R2", "U2", "R", "U2", "L", "U", "R", "L2", "U", "D", "F", "U'", "R2", "B'"]
> 
> This has been verified to solve the scramble in 33 moves.

FINAL_SOLUTION: ["R2", "U2", "D2", "F2", "R2", "F2", "R2", "D2", "F2", "L2", "U'", "F2", "U", "F2", "U2", "R2", "U'", "B2", "U", "R2", "U2", "R", "U2", "L", "U", "R", "L2", "U", "D", "F", "U'", "R2", "B'"]

**Verified solution (33 moves):** `R2 U2 D2 F2 R2 F2 R2 D2 F2 L2 U' F2 U F2 U2 R2 U' B2 U R2 U2 R U2 L U R L2 U D F U' R2 B'`
