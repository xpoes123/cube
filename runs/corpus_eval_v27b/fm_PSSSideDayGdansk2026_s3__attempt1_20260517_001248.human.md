# Solve — fm_PSSSideDayGdansk2026_s3__attempt1_20260517_001248

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `R2 D2 B2 L2 F2 L2 U2 R2 U' F2 U R2 F2 U L2 U' L2 U' R U D' L U L D' R L' B U' R B`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble. I should start by inspecting the state to see the bad edges per axis and other critical information, then proceed with the standard FMC pipeline: EO scouting → DR feasibility → commit to best axis → DR → HTR → finish.
> 
> Let me begin with inspect_state to see what we're working with.

I'll solve this FMC scramble systematically. Let me start by inspecting the cube state to understand the initial position.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

**Initial inspection**: I see UD has 4 bad edges (UL, DR, DL, DB), FB has 8 bad edges, and RL has 6. UD is the clear EO winner at 4 bad edges. However, I notice `top_pairs_on_inverse: 3` on UD — this is a VERY strong NISS signal (≥2 pairs means the inverse frame likely has better DR options). The DR-closeness shows DR-7C3E on UD (not great), but the 3 pairs on inverse suggest I should scout the inverse side.

**EO Axis Scouting Plan**: 
1. Check UD-axis EO on normal side (4 bad edges)
2. Check UD-axis EO on inverse side (due to 3 pairs signal)
3. Compare and decide

Let me start with UD-axis EO on the normal side:

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

**UD-normal EO = 4 moves** (`U L R' B'`). Now let me check the inverse frame — with 3 pairs preserved, the inverse should have a cleaner DR structure even if EO is similar length:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

**UD-inverse EO = 4 moves** (`B' R' U B'`). Same length as normal, but the 3 pairs on inverse means DR should be much cleaner. Let me probe DR options on the inverse side by committing the EO and checking dr_trigger_options:

I turn `B' R' U B'`.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Interesting — no DR triggers found within 5-move setup on UD-inverse. Let me check the current state and try using dr_recognize as a fallback:

I look over the cube.
Bad-edge counts: UD=0, FB=6, RL=6.
I'm currently working on the inverse scramble.
Last applied: `B' R' U B'`.

**Current state after UD-EO on inverse**: UD-EO is solved, but DR-closeness shows DR-6C3E on UD (6 misoriented corners, 3 misplaced edges). However, I notice **FB-axis shows DR-4C2E** (4 corners, 2 edges) — this is a MUCH better substate! DR-4C2E via the `R U2 R'` trigger is one of the best DR substates.

Let me try FB axis instead. I'll check dr_trigger_options on FB:

DR trigger menu on FB: EO not yet solved on axis FB; run eo_pattern_lookup and apply EO moves first.

Right, I need FB-EO first. Let me check FB-EO on the current inverse state:

On FB axis I recognize the EO pattern — `L D2 U R'` fixes it.

**Decision point**: I have UD-EO done (4 moves on inverse), but to get to the better FB-axis DR-4C2E substate, I'd need to redo EO for FB (another 4 moves). That's 8 total moves just for EO, which is too expensive. Let me stick with the UD-axis path and use dr_recognize to find the DR completion:

I check whether the DR is recognizable from this state via the library.

**DR setup on UD-inverse**: The full DR is 9 moves total. I see 4 moves of setup (`L R' D L'`). Let me apply these and re-query:

I turn `L R' D L'`.

I check whether the DR is recognizable from this state via the library.

Another 4 moves of setup. Total DR would be 4 (EO) + 4 + 4 + 1 = 13 moves, which is marginal but acceptable. Let me continue:

I turn `U' L' D U'`.

I check whether the DR is recognizable from this state via the library.

Excellent! **Single R' trigger for DR**. Total to DR: 4 (EO) + 4 + 4 + 1 = 13 moves. Let me apply the trigger:

I turn `R'`.

Quick check: DR-locked on UD, not yet HTR.

**DR achieved on UD-inverse!** Now I'm at 13 moves on the inverse side. Let me classify the HTR subset and finish:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 10 moves, finish is 8 moves (first exposure — learning).

**HTR classification**: 2-swap mostly-axial subset. HTR reduction is 10 moves, finish is 8 moves. Total from DR: 10 + 8 = 18 moves. **Full solution length estimate**: 13 (to DR) + 18 (HTR+finish) = 31 moves.

This is acceptable but I should check if there's a 3-cycle residual that emerges during HTR. Let me apply HTR reduction in chunks and check:

For the corner reduction, I see `U L2 U L2` (chunk of a 10-move phase) — apply and re-check.

I turn `U L2 U L2`.

Quick check: DR-locked on UD, not yet HTR.

Not in HTR yet, not solved. Let me continue HTR reduction:

For the corner reduction, I see `U' F2 R2 U'` (chunk of a 6-move phase) — apply and re-check.

I turn `U' F2 R2 U'`.

Quick check: DR-locked on UD, not yet HTR.

Let me continue:

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

**HTR achieved!** I'm now in HTR at 23 moves. Let me check if there's a 3-cycle residual before finishing:

Residual class: mixed.

Not a pure 3-cycle — it's mixed with 2 corner 3-cycles and multiple edge cycles. Let me proceed with the finish phase:

For the half-turn finish, I see `R2 U2 L2 F2` (chunk of a 8-move phase) — apply and re-check.

I turn `R2 U2 L2 F2`.

Quick check: in HTR.

Let me check for a 3-cycle now:

Residual class: mixed.

Still mixed. Let me continue the finish:

For the half-turn finish: `L2 B2 D2 R2`.

I turn `L2 B2 D2 R2`.

A quick glance — the cube is solved.

**SOLVED!** The cube is solved at 31 moves on the inverse side. Now I need to compose the NISS solution correctly. Since I worked entirely on the inverse side, the final solution is the inverse of my history. Let me use compose_niss_solution to get the correct normal-frame solution:

I assemble the canonical inverse-frame solution: **31 moves**, verified.

Perfect! I have a 31-move solution. Let me verify it's correct:

verify_solved: ✓ — 31 moves.

Excellent! The solution is verified. Now let me check if I can use replace_and_shorten. I have 31 moves and should have plenty of tool calls remaining. Let me check budget:

Budget check: 3495.0s sim, None tool calls remaining.

I have plenty of budget remaining (3495 simulated seconds). Since I have 31 moves (≥27) and plenty of tool calls remaining, I should try replace_and_shorten on a large segment. Let me target the DR setup + HTR reduction section which seems long. Let me try shortening the span from move 4 to the end (moves 4-31):

replace_and_shorten: substitute is 1 moves longer; reject.

The replace_and_shorten actually made it **worse** by 1 move (31 → 32). I'll keep my original 31-move solution. Let me check if I can try a different segment, but actually the tool enforces a 1-call cap, so I can't call it again.

My final solution is **31 moves**. Let me submit it:

**FINAL_SOLUTION**: ["R2", "D2", "B2", "L2", "F2", "L2", "U2", "R2", "U'", "F2", "U", "R2", "F2", "U", "L2", "U'", "L2", "U'", "R", "U", "D'", "L", "U", "L", "D'", "R", "L'", "B", "U'", "R", "B"]

## Solution Summary

**Approach**: Worked entirely on the inverse frame after detecting 3 pairs on inverse.

**Breakdown**:
- **EO (inverse, UD-axis)**: B' R' U B' (4 moves)
- **DR setup + trigger (inverse, UD-axis)**: L R' D L' + U' L' D U' + R' (9 moves total)
- **HTR reduction (UD-axis)**: U L2 U L2 + U' F2 R2 U' + F2 U (10 moves)
- **HTR finish**: R2 U2 L2 F2 + L2 B2 D2 R2 (8 moves)

**Total**: 31 moves (4 EO + 9 DR + 18 HTR/finish)

The solution successfully solves the scramble. While 31 moves is longer than elite sub-25 targets, it's a solid solve that avoids timeout and demonstrates the complete FMC pipeline with NISS.

*Thinking (30):*

> The user is right - I need to actually emit the FINAL_SOLUTION in the correct format. I have already verified the solution works (31 moves), and I've already used my one allowed replace_and_shorten call. I should submit the solution now.
> 
> The solution from compose_niss_solution was:
> ["R2", "D2", "B2", "L2", "F2", "L2", "U2", "R2", "U'", "F2", "U", "R2", "F2", "U", "L2", "U'", "L2", "U'", "R", "U", "D'", "L", "U", "L", "D'", "R", "L'", "B", "U'", "R", "B"]
> 
> This is 31 moves and verified to solve the scramble. I should submit it.

FINAL_SOLUTION: ["R2", "D2", "B2", "L2", "F2", "L2", "U2", "R2", "U'", "F2", "U", "R2", "F2", "U", "L2", "U'", "L2", "U'", "R", "U", "D'", "L", "U", "L", "D'", "R", "L'", "B", "U'", "R", "B"]

**Verified solution (31 moves):** `R2 D2 B2 L2 F2 L2 U2 R2 U' F2 U R2 F2 U L2 U' L2 U' R U D' L U L D' R L' B U' R B`
