# Solve — fm_PSSSideDayGdansk2026_s2__attempt7_20260517_014038

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `L2 F D2 F2 U2 L2 F R2 B L2 D2 B2 R2 B2 L2 U2 F2 U2 F2 U' R2 U' F' R2 B2 U B' U2 R U2`

---

*Thinking (1):*

> Looking at the prior attempts, I see:
> - Attempt 2 and 4 both achieved 27 moves and appear to be identical solutions
> - The best prior solve is 27 moves
> - The instructions emphasize committing hard to ONE line and finishing cleanly
> 
> Let me start by inspecting the state to understand what we're working with, then I'll analyze what the prior 27-move attempts likely did and either reproduce that path or find a sister branch.
> 
> The key instruction is: "COMMIT HARD this attempt." Pick a line and drive it to completion. Don't over-ideate between branches.
> 
> Let me begin with inspect_state to see the initial configuration.

I'll solve this scramble with a committed, focused approach. The prior best is 27 moves—let me see if I can match or beat that by committing to a clean line early.

Starting with state inspection:

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**Initial state analysis:**
- Bad edges: UD=6, FB=4, RL=4 (FB and RL are tied for fewest)
- Bad corners: UD=7, FB=7, RL=6
- **Key signal**: `top_pairs_on_inverse: 3` on UD axis—this is a STRONG NISS-switch indicator (≥2 pairs preserved on inverse)
- RL has the fewest bad corners (6) but both FB and RL have 4 bad edges

**Strategy:** The prior 27-move solutions likely used inverse-side solving given the 3-pairs signal. Let me check both normal and inverse perspectives for FB and RL axes, focusing on the joint EO+DR cost.

Let me scout EO on normal-FB first, then check inverse:

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL have 4-move EOs on normal. Now let me check the inverse side. With `top_pairs_on_inverse: 3`, the inverse frame should be promising:

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check EO on FB and RL axes from this perspective:

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

**Excellent! Inverse-FB has a 2-move EO** (U2 R') vs 4 moves on normal. This is the signal to commit. Now let me probe the DR cost after this EO:

I probe what DR would look like if I applied this EO (without committing).

**Inverse-FB: 2-move EO + 9-move DR = 11 moves to DR.** That's within the sub-15 DR target. Let me commit to this line (inverse-FB) and drive it to completion.

Applying the 2-move EO:

I turn `U2 R'`.

**EO achieved on inverse-FB in 2 moves.** Now using dr_trigger_options to find the DR setup:

DR trigger menu on FB: no named trigger fits within 5 setup moves.

No named triggers found within 6 moves. Let me fall back to dr_recognize:

I check whether the DR is recognizable from this state via the library.

DR is 9 moves total, but I can only see 4 at a time. Applying the first chunk:

I turn `U2 B U' B2`.

Re-querying DR:

I check whether the DR is recognizable from this state via the library.

Another 4 moves toward DR:

I turn `R2 F U R2`.

Re-querying DR (should see the trigger now with 1 move left):

I check whether the DR is recognizable from this state via the library.

**Found the DR trigger!** 1-move final trigger (U') to complete DR. Total to DR: 2 (EO) + 4 + 4 + 1 = 11 moves.

I turn `U'`.

**DR achieved in 11 moves** (2 EO + 9 DR). Now classifying the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 12 moves (recall).

**HTR subset: 2-swap long-cycle.** HTR reduction = 10 moves, finish = 12 moves. Total from here: 10 + 12 = 22 moves. 

**Running total: 11 (to DR) + 22 = 33 moves.** That matches the worst prior attempt. Let me check if there's a 3-cycle residual opportunity during the HTR phases using quick_check between chunks.

Starting HTR reduction:

For the corner reduction, I see `U2 F' L2 F` (chunk of a 10-move phase) — apply and re-check.

Applying first HTR-reduction chunk and checking state:

I turn `U2 F' L2 F`.

Quick check: DR-locked on FB, not yet HTR.

Not solved yet. Continue HTR reduction:

For the corner reduction, I see `D2 F R2 F'` (chunk of a 6-move phase) — apply and re-check.

I turn `D2 F R2 F'`.

Quick check: DR-locked on FB, not yet HTR.

Continue:

For the corner reduction: `U2 B`.

I turn `U2 B`.

Quick check: in HTR.

**HTR reduction complete!** Now at HTR (all EO/DR/HTR flags true). Now the finish phase:

For the half-turn finish, I see `R2 F2 D2 R2` (chunk of a 12-move phase) — apply and re-check.

I turn `R2 F2 D2 R2`.

Quick check: in HTR.

Continue finish:

For the half-turn finish, I see `D2 F2 R2 B2` (chunk of a 8-move phase) — apply and re-check.

I turn `D2 F2 R2 B2`.

Quick check: in HTR.

Continue:

For the half-turn finish: `L2 U2 R2 U2`.

I turn `L2 U2 R2 U2`.

A quick glance — the cube is solved.

**SOLVED!** 32 moves on the inverse side. Now I need to compose the final solution using compose_niss_solution (which will invert the inverse-side moves and assemble them correctly):

I assemble the canonical inverse-frame solution: **32 moves**, verified.

**32-move solution found.** That's 5 moves longer than the best prior (27 moves). Let me check if replace_and_shorten can improve it. The gates are: ≥27 moves (✓ 32 moves), ≥30 tool calls remaining (need to check), and haven't used r&s yet this run (✓).

Let me check budget status:

Budget check: 3517.0s sim, None tool calls remaining.

I have plenty of time (3517s remaining). Let me try replace_and_shorten on a large span to see if I can reduce this 32-move solution. I'll target the DR-to-finish portion (moves 11-32):

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

**Excellent!** Replace_and_shorten found a 2-move improvement. The new solution is 30 moves. Let me update the slot history with this improved version:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `U2 R' U2 B U' B2 R2 F U R2 U F2 U2 F2 U2 L2 B2 R2 B2 D2 L2 B' R2 F' L2 U2 F2 D2 F' L2`.

Now composing the final solution with the improved 30-move history:

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Perfect! Let me verify this 30-move solution:

verify_solved: ✓ — 30 moves.

**VERIFIED: 30-move solution!**

## Final Solution Summary

**Approach:** Inverse-FB axis solving
- **EO (inverse-FB):** 2 moves (U2 R')
- **DR:** 9 moves total to reach DR on FB axis
- **Total to DR:** 11 moves
- **HTR subset:** 2-swap long-cycle
- **HTR finish:** 21 moves initially, reduced to 19 via replace_and_shorten
- **Final count:** 30 moves

**Replace_and_shorten** saved 2 moves on the DR-to-finish portion (span [11:32], 21→19 moves).

The solution is 3 moves longer than the best prior attempt (27 moves), but it's a complete, verified solve achieved through committed execution of the inverse-FB line.

**FINAL_SOLUTION:** ["L2", "F", "D2", "F2", "U2", "L2", "F", "R2", "B", "L2", "D2", "B2", "R2", "B2", "L2", "U2", "F2", "U2", "F2", "U'", "R2", "U'", "F'", "R2", "B2", "U", "B'", "U2", "R", "U2"]

*Thinking (34):*

> The user is right - I verified the solution but didn't emit the FINAL_SOLUTION format. I should output it now in the required format.

FINAL_SOLUTION: ["L2", "F", "D2", "F2", "U2", "L2", "F", "R2", "B", "L2", "D2", "B2", "R2", "B2", "L2", "U2", "F2", "U2", "F2", "U'", "R2", "U'", "F'", "R2", "B2", "U", "B'", "U2", "R", "U2"]

**Verified solution (30 moves):** `L2 F D2 F2 U2 L2 F R2 B L2 D2 B2 R2 B2 L2 U2 F2 U2 F2 U' R2 U' F' R2 B2 U B' U2 R U2`
