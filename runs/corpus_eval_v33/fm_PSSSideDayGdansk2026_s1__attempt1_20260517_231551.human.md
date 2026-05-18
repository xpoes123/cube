# Solve — fm_PSSSideDayGdansk2026_s1__attempt1_20260517_231551

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 29 moves
**Solution**: `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 U D F R L D B`

---

*Thinking (1):*

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start by inspecting the state to see the bad edges per axis and other information, then proceed through the FMC pipeline: EO → DR → HTR → finish.
> 
> Let me start with inspect_state on the main slot.

I'll solve this FMC scramble systematically. Let me begin by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Initial inspection**: The cube shows 8 bad edges on UD, 6 on FB, and 6 on RL. FB and RL are tied for the fewest bad edges. DR closeness shows DR-6C3E on UD (not ideal), DR-5C2E on FB (more interesting), and DR-7C3E on RL. FB has 5 misoriented corners and 2 misplaced slice edges — DR-5C2E suggests it might need more setup. I notice `top_pairs_on_inverse: 2` on UD axis, which is a strong NISS signal.

Let me scout EO on both normal and inverse sides for the two most promising axes (FB and RL with 6 bad edges each).

**Normal side FB-axis EO:**

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

FB-axis EO on normal side is 5 moves total (4 shown as partial). Let me check RL-axis on normal:

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

Both FB and RL need 5 moves for EO on normal. Now let me check the inverse side. The inspect shows `top_pairs_on_inverse: 2` on UD — that's a strong NISS signal. Let me flip to inverse and check UD-axis EO there:

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check UD-axis EO (since top_pairs_on_inverse=2 was strong):

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

UD on inverse is also 5 moves. Let me also check FB and RL on inverse to be thorough:

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

All EO options are 5 moves across all axes on both sides. Since they're all tied, I need to probe DR quality to make the decision. Let me pick FB-axis on normal side first (DR-5C2E looked reasonable). Let me go back to normal and test that path:

NISS flip — switching back to the normal scramble.

Back on normal side. Let me apply the FB-axis EO and then check DR options:

I turn `R2 B' L' U2`.

Now let me check if I need one more move for FB-EO:

On FB axis I recognize the EO pattern — `R'` fixes it.

Perfect! One more move to complete FB-EO:

I turn `R'`.

**FB-axis EO complete in 5 moves**: R2 B' L' U2 R'. Now let me check DR trigger options on FB-axis:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**No DR triggers found within 5 moves on FB-axis!** This is a bad sign. Let me try dr_recognize instead to see if the brain can suggest something:

I check whether the DR is recognizable from this state via the library.

The brain suggests R2 strongly (83.5%). This path seems murky. Let me back up and try a different axis. Let me reset and try RL-axis on normal instead:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me try RL-axis EO on normal:

I turn `L U L2 R`.

On RL axis I recognize the EO pattern — `D'` fixes it.

I turn `D'`.

**RL-axis EO complete in 5 moves**: L U L2 R D'. Now let me check DR triggers on RL:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on RL.**

Also no DR triggers on RL. Let me try the inverse side with UD-axis since that had top_pairs_on_inverse=2. Let me reset and flip:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

On inverse. Let me apply UD-axis EO:

I turn `B' D' L' R'`.

On UD axis I recognize the EO pattern — `F'` fixes it.

I turn `F'`.

**UD-axis EO complete in 5 moves on inverse**: B' D' L' R' F'. Now let me check DR triggers on UD:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Still no DR triggers within 5 moves! This scramble seems to have difficult DR access. Let me use dr_recognize with the brain to find DR incrementally:

I check whether the DR is recognizable from this state via the library.

The brain strongly suggests D' (76.8%). Let me apply it and re-check:

I turn `D'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on UD:
  • DR-3C2E (R U R'): 5-mv setup + 3-mv trigger (8 total) pre=DR-3C1E

Excellent! Found **DR-3C2E** with 5-move setup: U' F2 U' F2 L, then trigger R U R'. Total to DR = 8 moves from current position. Combined with my 6-move EO on inverse, that's 6 + 8 = 14 moves to DR. The DR-3C2E substate typically finishes in 6-8 moves (not JZP), so estimated total ~20-22 moves. Let me apply this:

I turn `U' F2 U' F2 L R U R'`.

**At DR in 14 moves on inverse**. Now let me classify the HTR substate:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 5 moves, finish is 11 moves (first exposure — learning).

**HTR subset**: 2-swap mostly-axial with 5-move HTR reduction + 11-move finish = 16 moves post-DR. Total: 14 (EO+DR on inverse) + 16 (HTR) = **30 moves**. This is acceptable but not great. Let me apply the HTR phases:

For the corner reduction, I see `R2 B2 U' F2` (chunk of a 5-move phase) — apply and re-check.

I turn `R2 B2 U' F2`.

Good, there was 1 cancellation (R' + R2 → R). Let me check if I'm at HTR or need the last move:

Quick check: DR-locked on UD, not yet HTR.

Not at HTR yet. Let me get the last move:

For the corner reduction: `D`.

I turn `D`.

Now at HTR in 18 moves. Let me apply the finish phase:

For the half-turn finish, I see `B2 L2 D2 L2` (chunk of a 11-move phase) — apply and re-check.

I turn `B2 L2 D2 L2`.

Let me check if it's solved yet:

Quick check: in HTR.

Still not solved. Let me continue the finish:

For the half-turn finish, I see `D2 B2 R2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `D2 B2 R2 U2`.

Quick check: in HTR.

Still not solved. Continue:

For the half-turn finish: `F2 U2 R2`.

I turn `F2 U2 R2`.

A quick glance — the cube is solved.

**Solved in 29 moves on inverse!** Now I need to compose the final NISS solution properly using compose_niss_solution:

I assemble the canonical inverse-frame solution: **29 moves**, verified.

Perfect! The solution is verified and solves in 29 moves. Since this is ≥27 moves, I should check if replace_and_shorten can improve it. Let me check my budget first:

Budget check: 2285.53s sim, None tool calls remaining.

I have 2285s remaining (~38 minutes). I have a 29-move solution which triggers the replace_and_shorten gate (≥27 moves). Let me try to improve it. I'll target a large middle section:

r&s: could not solve micro-scramble for span [4:25]: no DR found

The replace_and_shorten attempt failed (couldn't find DR for that span). That's okay - I've used my 1 allowed call. My current 29-move solution is solid. Let me verify it once more and submit:

verify_solved: ✓ — 29 moves.

Perfect! The solution is verified as correct.

## FINAL SOLUTION

**Solution breakdown:**
- **EO on inverse (UD-axis)**: 5 moves (B' D' L' R' F')
- **DR setup + trigger**: 9 moves (D' U' F2 U' F2 L R U R')
- **HTR reduction**: 5 moves (R2 B2 U' F2 D) with 1 cancellation
- **HTR finish**: 11 moves
- **Total**: 29 moves

The solve used NISS (inverse frame) with UD-axis EO and a DR-3C2E trigger. The HTR subset was "2-swap mostly-axial" which finished in 16 moves post-DR.

FINAL_SOLUTION: ["R2", "U2", "F2", "U2", "R2", "B2", "D2", "L2", "D2", "L2", "B2", "D'", "F2", "U", "B2", "R'", "U'", "R'", "L'", "F2", "U", "F2", "U", "D", "F", "R", "L", "D", "B"]

**Verified solution (29 moves):** `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 U D F R L D B`
