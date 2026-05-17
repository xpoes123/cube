# Solve — fm_PSSSideDayGdansk2026_s3__attempt1_20260517_151730

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 27 moves
**Solution**: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I should start by inspecting the state to see what I'm working with. The scramble is:
> 
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Let me start with inspect_state to understand the bad edge counts per axis, DR closeness, etc.

I'll solve this FMC scramble step by step, starting with a thorough inspection of the cube state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

**Initial State Analysis:**

I can see:
- **Bad edges per axis**: UD=4, FB=8, RL=6
- **UD axis** is the best candidate for EO (4 bad edges)
- **DR closeness**: UD shows DR-7C3E (poor), FB shows DR-6C3E, RL shows DR-5C3E
- **Important signal**: `top_pairs_on_inverse: 3` on UD axis — this is a STRONG NISS switch signal (≥2 pairs preserved)

**Strategy:** UD has the fewest bad edges (4), but I need to check BOTH normal and inverse frames for EO quality. The 3 pairs on inverse suggests the inverse frame may be superior for the overall solve. Let me scout EO on UD-normal first, then check UD-inverse.

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

**UD-normal EO: 4 moves** (U L R' B').

Now let me check the inverse frame. According to the NISS invariant, the bad-edge count will be the same (4 bad edges on UD axis), but the SOLUTION will differ. With 3 pairs preserved on inverse, this is very promising.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

**UD-inverse EO: 4 moves** (B' R' U B').

Same length as normal. The decision will hinge on DR quality. Let me probe DR for both sides.

I probe what DR would look like if I applied this EO (without committing).

**UD-inverse EO+DR: 4+9 = 13 moves to DR.**

Now let me flip back to normal and probe the UD-normal DR:

NISS flip — switching back to the normal scramble.

I probe what DR would look like if I applied this EO (without committing).

**UD-normal EO+DR: 4+8 = 12 moves to DR.**

Normal side wins by 1 move (12 vs 13). Both are within acceptable range (<15), but I should also check FB axis as a comparison since FB has the next-fewest corners for DR (DR-6C3E vs DR-7C3E on UD).

Let me check FB-normal EO:

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

**FB-normal EO: 4 moves** (R' F D L').

Same length! Let me probe FB DR:

I probe what DR would look like if I applied this EO (without committing).

**FB-normal EO+DR: 4+7 = 11 moves to DR.**

Excellent! FB-normal is 1 move better than UD-normal (11 vs 12). Let me commit to FB-normal EO and proceed.

**Decision: FB-normal axis, EO = R' F D L' (4 moves), expected DR ≤11 moves total.**

I turn `R' F D L'`.

**EO committed on FB axis.** Now I need to find the DR. Let me use dr_trigger_options to get a ranked menu of DR candidates:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Hmm, dr_trigger_options found **no options** within 5-move setup on FB axis. This is surprising given that probe_dr_pattern said total_dr_length = 7. Let me fall back to dr_recognize, which works on any axis:

I check whether the DR is recognizable from this state via the library.

**DR is 7 moves total, but I can only see 4 moves at a time.** This is the realistic human workflow. Let me apply the setup progress and re-query:

I turn `B' D F' U'`.

I check whether the DR is recognizable from this state via the library.

**DR pattern recognized!** I can see a 2-move setup (B L2) followed by a 1-move trigger (D'). Total: 3 more moves to reach DR. Let me apply these:

I turn `B L2`.

I turn `D'`.

**Reached DR at 11 moves** (4 EO + 7 DR). Excellent! Now I'm at DR on the FB axis. Let me verify with quick_check and then proceed to HTR:

Quick check: DR-locked on FB, not yet HTR.

**Confirmed DR-solved on FB axis.** Now let me classify the HTR subset:

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 8 moves, finish is 9 moves (first exposure — learning).

**HTR classification:** 
- Subset: **4-swap long-cycle** with cycle structure [4, 4]
- HTR reduction: 8 moves
- Finish: 9 moves
- **Total from DR: 17 moves**

**Current total: 11 (to DR) + 17 (HTR+finish) = 28 moves.**

This is within acceptable range. Let me proceed with the HTR reduction phase:

For the corner reduction, I see `D2 F2 R2 U2` (chunk of a 8-move phase) — apply and re-check.

**HTR reduction is 8 moves, showing first 4 moves.** Let me apply them and check state:

I turn `D2 F2 R2 U2`.

Quick check: DR-locked on FB, not yet HTR.

Good — the auto-cancel saved 1 move (D' + D2 → D). Not yet in HTR. Let me continue with the remaining HTR reduction:

For the corner reduction: `F' U2 L2 B`.

**Final 4 moves of HTR reduction.** Let me apply and check:

I turn `F' U2 L2 B`.

Quick check: in HTR.

**Excellent! I've reached HTR** (`is_htr_ud: true`). Now I need to finish with half-turns only. Let me apply the finish phase:

For the half-turn finish, I see `R2 U2 B2 R2` (chunk of a 9-move phase) — apply and re-check.

**Finish is 9 moves, showing first 4.** Let me apply and check for early solve:

I turn `R2 U2 B2 R2`.

Quick check: in HTR.

Still not solved. Let me continue with the rest of the finish:

For the half-turn finish, I see `F2 U2 B2 D2` (chunk of a 5-move phase) — apply and re-check.

I turn `F2 U2 B2 D2`.

Quick check: in HTR.

Still not solved. Let me get the last move:

For the half-turn finish: `F2`.

I turn `F2`.

A quick glance — the cube is solved.

**SOLVED!** The cube is now solved in 27 moves. Since this is ≥27 moves and I have plenty of budget remaining, I should try replace_and_shorten to see if I can improve it. Let me compose the canonical solution first:

I assemble the canonical normal-frame solution: **27 moves**, verified.

Let me check my budget status:

Budget check: 3287.12s sim, None tool calls remaining.

**Budget check:**
- Sim spent: 312.88 seconds (out of 3600)
- Sim remaining: 3287.12 seconds
- Tool calls remaining: plenty

I have a 27-move solution, which meets the gates for replace_and_shorten (≥27 moves, ≥30s budget remaining). Let me try to shorten a large tail span. I'll target the DR-to-finish section (moves 11-27), which is 16 moves. Let me try replace_and_shorten on a span like [4, 27]:

replace_and_shorten: substitute is 5 moves longer; reject.

**Replace_and_shorten result: WORSE by 5 moves** (original 23 → substitute 28). I'll keep my original 27-move solution. Let me verify it one more time:

verify_solved: ✓ — 27 moves.

Perfect! The solution is verified. 

## Solution Summary:

**EO (4 moves on FB axis):** R' F D L'
- Started with bad_edges = {UD:4, FB:8, RL:6}
- FB-normal had the best joint EO+DR (11 total to DR)

**DR (7 moves):** B' D F' U' B L2 D'
- Reached DR-FB at move 11
- Used incremental pattern recognition (4-move chunks)

**HTR + Finish (16 moves):**
- HTR reduction: D F2 R2 U2 F' U2 L2 B (8 moves, with 1 cancellation)
- HTR subset: 4-swap long-cycle [4,4]
- Finish: R2 U2 B2 R2 F2 U2 B2 D2 F2 (9 moves)

**Total: 27 moves**

FINAL_SOLUTION: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

**Verified solution (27 moves):** `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
