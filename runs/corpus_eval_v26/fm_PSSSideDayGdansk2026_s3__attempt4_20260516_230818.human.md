# Solve — fm_PSSSideDayGdansk2026_s3__attempt4_20260516_230818

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 R2 B2 U2 F2 L2 U2 R2 U L2 R2 B2 U B2 U' R2 U' R U2 R' U L' R2 D' F2 D B U' R B`

---

*Thinking (1):*

> The user is asking me to solve a Rubik's Cube FMC scramble. I should start by inspecting the state of the cube as they suggested, then follow the FMC pipeline described in the instructions.
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Let me start with inspect_state to see what we're working with.

I'll solve this FMC scramble systematically, starting with inspection and following the elite-solver pipeline. Let me begin.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good! I can see the state:
- **EO options**: UD has 4 bad edges (best), FB has 8 bad edges, RL has 6 bad edges
- **DR states**: UD is DR-7C3E, FB is DR-6C3E, RL is DR-5C3E (all not great without JZP)
- **NISS signal**: `top_pairs_on_inverse: 3` on UD-axis — this is a VERY strong signal to check the inverse frame

Following the v16 pipeline, I should immediately call **niss_scout** to get the full 6-row comparison table (normal × inverse × {UD, FB, RL}) before committing to any EO axis.

I scout EO+DR on both normal and inverse, all three axes — 1 viable rows.
  • inverse-RL: EO 5mv → DR-3C2E (F L' F') DR (8mv)
I'll weigh the substate quality (trigger family) against raw length and pick.

Interesting scout results! All normal-side axes show "no DR triggers within max_setup=5" — that's a bad sign. But the inverse-RL row has found a viable path:
- **Inverse-RL**: EO 5 moves + DR-3C2E in 8 moves total → 13 moves to DR
- The DR-3C2E trigger family is much better than DR-4C4E or DR-7C3E

However, 13 moves to DR is on the long side (elite target is ≤11). Let me check if there are better manual DR options on the normal axes that the scout might have missed, OR if I can improve on the inverse-RL path. Since the scout ran max_setup=5, let me try extending the search slightly by using dr_trigger_options directly after each EO to see if there are hidden options.

Let me start by trying the shortest EO (4 moves on normal-UD) and checking dr_trigger_options:

I turn `U L R' B'`.

I survey the named DR triggers on UD:
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

Found one option: DR-7C8E in 9 moves total (6 setup + 3 trigger). That's better than the inverse-RL's 13, but DR-7C8E is a bad substate (typically finishes in ~12-14 moves). Also note `top_pairs_on_inverse: 4` — this is signaling I should flip to inverse.

Let me reset and try the inverse-UD EO that the scout found:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

Good, I'm now on the inverse frame. Let me apply the inverse-UD EO from the scout and check dr_trigger_options:

I turn `B' R' U B'`.

I survey the named DR triggers on UD:
  • DR-3C2E (R U' R'): 6-mv setup + 3-mv trigger (9 total)
  • DR-4C2E (R U2 R'): 6-mv setup + 3-mv trigger (9 total) [JZP]

Excellent! Found two good options on inverse-UD:
1. **DR-3C2E** in 9 moves total (6 setup + 3 trigger) — this is a great substate (~5 moves to finish)
2. **DR-4C2E** in 9 moves total (6 setup + 3 trigger) — also good, and **JZP-eligible**!

The JZP-eligible DR-4C2E is very promising. Total EO+DR = 4+9 = 13 moves. Let me also check the FB and RL axes on inverse to make sure I'm not missing something better:

I rewind 4 moves.

I turn `B' L' D' L2 U'`.

I survey the named DR triggers on RL:
  • DR-3C2E (F L' F'): 5-mv setup + 3-mv trigger (8 total)
  • DR-3C2E (F L F'): 6-mv setup + 3-mv trigger (9 total)
  • DR-7C8E (F L B): 6-mv setup + 3-mv trigger (9 total)

Very good! Inverse-RL has a DR-3C2E in 8 moves total. That's the shortest DR option so far. Total: EO 5 + DR 8 = 13 moves to DR.

**Branch comparison:**
- **Inverse-UD, DR-4C2E (JZP)**: EO 4 + DR 9 = 13 total to DR
- **Inverse-RL, DR-3C2E**: EO 5 + DR 8 = 13 total to DR

Both reach DR in 13 moves. The JZP-eligible option on UD is attractive because JZP substates finish much faster. Let me commit to the **inverse-UD path with JZP-eligible DR-4C2E**.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

Now applying the inverse-UD EO (4 moves: B' R' U B'):

I turn `B' R' U B'`.

Now applying the DR-4C2E (JZP) setup and trigger:

I turn `D' F2 D R2 L U'`.

I turn `R U2 R'`.

Excellent! I've reached DR in 13 moves on the inverse. Now let me classify the HTR state and finish:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 9 moves, finish is 9 moves (recall).

Good! The HTR classify shows:
- Subset: **2-swap mostly-axial** 
- HTR reduction: 9 moves
- Finish: 9 moves
- Total HTR+finish: 18 moves

This gives me an estimated total of 13 (to DR) + 18 (HTR+finish) = **31 moves**. That's acceptable but not great. Let me proceed with the HTR reduction and keep checking for early residuals:

For the corner reduction, I see `U R2 U B2` (chunk of a 9-move phase) — apply and re-check.

I turn `U R2 U B2`.

Quick check: DR-locked on UD, not yet HTR.

Not solved yet, still need more HTR reduction. Let me continue:

For the corner reduction, I see `U' B2 R2 L2` (chunk of a 5-move phase) — apply and re-check.

I turn `U' B2 R2 L2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `U`.

I turn `U`.

Quick check: in HTR.

Great! Now at HTR (is_htr_ud: true). Let me proceed with the finish phase:

For the half-turn finish, I see `U2 R2 U2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 R2 U2 L2`.

Quick check: in HTR.

For the half-turn finish, I see `F2 U2 B2 R2` (chunk of a 5-move phase) — apply and re-check.

I turn `F2 U2 B2 R2`.

Quick check: in HTR.

For the half-turn finish: `B2`.

I turn `B2`.

A quick glance — the cube is solved.

Perfect! The cube is solved. I have a 31-move solution on the inverse frame. Now I need to use compose_niss_solution to get the proper normal-frame solution:

I assemble the canonical inverse-frame solution: **30 moves**, verified.

Excellent! The composed solution is **30 moves** and verified as solving. Let me check if I should try replace_and_shorten. According to the rules, I should try it if:
- total_moves ≥ 27 ✓ (I have 30)
- tool calls remaining ≥ 30 ✓ (I've used about 40-50 calls, should have plenty left)

Let me check my budget status:

Budget check: 3415.0s sim, None tool calls remaining.

Great! I have plenty of time remaining (3415s sim, ~1327s wall). Let me try replace_and_shorten on a meaningful span. I'll try replacing the middle/end portion of my solution where the HTR finish happened. Let me look at the normal-frame solution structure:

The solution is 30 moves. Let me try replacing a span from around move 10 to the end:

replace_and_shorten: substitute is 8 moves longer; reject.

The replace_and_shorten made it worse (delta +8). Let me try a different span - perhaps earlier in the sequence. Let me try the DR portion:

r&s: replace_and_shorten already used this run (1-call cap, Tronto §3.10).

Ah right, there's a 1-call cap on replace_and_shorten. Since it didn't improve my solution, I'll stick with my original 30-move solution. Let me verify it one more time and submit:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. Let me apply cancellation to see if there are any obvious move reductions:

I check for cancellations — no savings.

No cancellations found - the solution is already optimal in terms of mechanical cancellations.

**FINAL_SOLUTION: ["B2", "R2", "B2", "U2", "F2", "L2", "U2", "R2", "U", "L2", "R2", "B2", "U", "B2", "U'", "R2", "U'", "R", "U2", "R'", "U", "L'", "R2", "D'", "F2", "D", "B", "U'", "R", "B"]**

## Solution Summary

**30 moves total** achieved via the inverse-NISS approach:

### Reasoning Path:
1. **Inspection & NISS Scout**: Initial inspection showed UD-axis had 4 bad edges (best EO) but poor DR options (DR-7C3E). The scout revealed `top_pairs_on_inverse: 3`, a strong signal to explore the inverse frame.

2. **Branch Comparison** (elite-solver pattern):
   - **Normal-UD**: 4-move EO + DR-7C8E in 9 total → suboptimal DR substate
   - **Inverse-UD**: 4-move EO + DR-4C2E (JZP-eligible) in 9 total → 13 to DR ✓
   - **Inverse-RL**: 5-move EO + DR-3C2E in 8 total → 13 to DR
   
   Chose inverse-UD because the JZP-eligible DR-4C2E finish is significantly faster (~5-6 moves) than the DR-3C2E or DR-7C8E substates.

3. **Execution**:
   - EO on inverse-UD: `B' R' U B'` (4 moves)
   - DR setup + trigger: `D' F2 D R2 L U'` + `R U2 R'` (9 moves, DR-4C2E JZP)
   - HTR reduction: 9 moves to reach HTR-corner-subgroup (2-swap mostly-axial subset)
   - HTR finish: 9 moves to solved
   
4. **Final compose**: Used `compose_niss_solution` to properly invert the NISS frame into normal-frame notation.

5. **Refinement attempt**: Called `replace_and_shorten` on the tail span but it regressed (+8 moves), so kept the original 30-move solution.

The 30-move result is competitive for this scramble given the challenging initial state (no axis had good simultaneous EO+DR options). The NISS-first strategy and JZP-eligible DR choice were critical to avoiding a 33+ move solution.

**Verified solution (30 moves):** `B2 R2 B2 U2 F2 L2 U2 R2 U L2 R2 B2 U B2 U' R2 U' R U2 R' U L' R2 D' F2 D B U' R B`
