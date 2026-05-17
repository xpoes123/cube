# Solve — fm_PSSSideDayGdansk2026_s3__attempt4_20260517_171034

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `U B D L U' B' L U2 L2 B F L2 F' R2 U2 F2 U2 R' U2 F2 R L2 U2 B2 D2 R2 B2 U2 L2 U2 R2`

---

*Thinking (1):*

> Alright, I'm being asked to solve this scramble within a one-hour budget. The prior three attempts all achieved 30-31 moves, so I have a baseline to beat or match.
> 
> The key directives:
> 1. Start with inspect_state(slot='main')
> 2. COMMIT HARD - pick a line and drive it through
> 3. Don't over-ideate or abandon paths halfway
> 4. Focus on finding ONE complete, clean solution
> 5. If prior attempts reached similar counts, trust that axis and optimize the FINISH
> 
> Let me start by inspecting the state to see what we're working with.

I'll solve this scramble systematically. Let me start by inspecting the cube state to understand the bad-edge distribution and DR potential across axes.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good! I see:
- **Bad edges**: UD=4, FB=8, RL=6
- **UD axis** has the fewest bad edges (4) and shows **3 pairs on inverse** — this is a strong NISS signal
- **DR closeness**: UD is DR-7C3E, FB is DR-6C3E, RL is DR-5C3E (all non-standard triggers)

The UD axis with 4 bad edges is the most promising for EO. Since `top_pairs_on_inverse = 3`, I should check both normal and inverse sides. Let me scout EO on UD-normal first:

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

UD-normal EO is **4 moves**: `U L R' B'`. Now let me check the inverse side since we have 3 pairs preserved there:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

UD-inverse EO is also **4 moves**: `B' R' U B'`. Both sides have 4-move EO, but the inverse side has 3 pairs preserved. Let me commit to the inverse-side EO and check DR options there:

I turn `B' R' U B'`.

Now I'm in EO-UD on the inverse side. Let me explore DR triggers:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

No DR triggers found within 5 moves on the inverse-UD axis. This is unexpected given the 3 pairs signal. Let me try a couple of intuitive setup moves and check again. Let me use policy intuition first:

I check my gut for plausible next moves.

The policy suggests `L'` strongly. Let me try it and check DR again:

I turn `L'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Still no DR triggers within 5 moves. This inverse-UD path is looking difficult for DR despite the pairs signal. Let me reconsider: I should check the normal side instead. Let me reset and try the normal-side EO:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Now let me try the normal-side UD EO and check DR options there:

I turn `U L R' B'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Also no DR triggers within 5 on normal-UD. Let me check the FB axis instead — it had 8 bad edges but might have better DR structure. Let me reset and try FB:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

FB-normal EO is **4 moves** too: `R' F D L'`. Let me apply it and check DR:

I turn `R' F D L'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

No DR within 5 on FB either. This scramble seems to have a difficult DR structure. Let me try adding a couple of setup moves on FB and checking again. Let me use policy intuition:

I check my gut for plausible next moves.

Policy suggests `F'`. Let me try a few moves:

I turn `F' D`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤4), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤4 moves on FB.**

This is frustrating — no standard triggers are showing up. Looking at my prior attempts, they all started with `U B D L U...` which suggests they found a working path. Let me analyze that pattern: `U B D L` looks like it could be an EO on some axis. Let me reset and try that exact opening:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I try `U B D L` on top to see the after-state (without committing).

`U B D L` gives RL=4 bad edges, which is an improvement on RL (6→4). It's not a pure EO move sequence, but it's making progress. Let me check if this leads to an EO on RL:

I turn `U B D L`.

On RL axis I recognize the EO pattern — `U'` fixes it.

Excellent! After `U B D L`, we need just **1 more move** `U'` to achieve EO-RL. So the full EO is 5 moves: `U B D L U'`. Let me apply it and check DR:

I turn `U'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C2E (F L2 F'): 5-mv setup + 3-mv trigger (8 total) pre=DR-4C1E

Great! Found a DR trigger on RL axis:
- **DR-4C2E (F L2 F')** with setup `B' L U2 L2 B`
- Total to DR: **8 moves** (5 setup + 3 trigger)
- Not JZP-eligible, but 4C2E is a decent substate (typical post-DR 9-11 moves)
- **Total from EO end: 5 (EO) + 8 (DR) = 13 moves to DR**

This aligns with my prior attempts which started similarly. Let me commit to this path:

I turn `B' L U2 L2 B F L2 F'`.

Now I'm at DR on RL axis with 13 moves. Let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 8 moves, finish is 10 moves (recall).

HTR classification:
- **Subset**: 2-swap long-cycle (cycle structure [4, 2, 1, 1])
- **HTR reduction**: 8 moves (DR → HTR corners)
- **Finish**: 10 moves (HTR → solved)
- **Total HTR+finish**: 18 moves

**Projected total**: 13 (to DR) + 18 (HTR+finish) = **31 moves**

This matches my prior attempt's length. Let me proceed with the HTR phases, but I'll insert free checks between chunks to see if we land on a 3-cycle early:

For the corner reduction, I see `R2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

HTR reduction is partial (8 moves total, showing first 4). Let me apply and check state:

I turn `R2 U2 F2 U2`.

Quick check: DR-locked on RL, not yet HTR.

Not solved yet, still in DR-RL. Let me get the next chunk of HTR reduction:

For the corner reduction: `R' U2 F2 R`.

I turn `R' U2 F2 R`.

Quick check: in HTR.

Good! Now I'm in HTR (all axes in DR, is_htr_ud = true). At 21 moves. Now I need the finish phase:

For the half-turn finish, I see `L2 U2 B2 D2` (chunk of a 10-move phase) — apply and re-check.

I turn `L2 U2 B2 D2`.

Quick check: in HTR.

Still in HTR, not solved. At 25 moves. Let me check if there's a 3-cycle residual here:

Residual class: mixed.

Not a pure 3-cycle — mixed residual with 4 corners and 7 edges unsolved. Let me continue with the finish:

For the half-turn finish, I see `R2 B2 U2 L2` (chunk of a 6-move phase) — apply and re-check.

I turn `R2 B2 U2 L2`.

Quick check: in HTR.

At 29 moves, still not solved. Let me check for a 3-cycle again:

Residual class: mixed.

Still mixed. Let me get the final chunk:

For the half-turn finish: `U2 R2`.

I turn `U2 R2`.

A quick glance — the cube is solved.

Excellent! The cube is **SOLVED** in **31 moves**. Now let me compose the final solution and verify it:

I assemble the canonical normal-frame solution: **31 moves**, verified.

I have a verified **31-move solution**. Now let me check if I should attempt replace_and_shorten. According to the rules, I should try it if:
- total_moves ≥ 27 ✓ (31 moves)
- tool calls remaining ≥ 30 ✓ (I've used about 30 calls so far, plenty left)

Let me try to shorten a large tail section. I'll target the HTR-finish section which was 18 moves (moves 14-31):

Budget check: 2037.12s sim, None tool calls remaining.

Good, I have 2037 seconds remaining (over 30 minutes). Let me try replace_and_shorten on the DR-to-finish section (from move 13 to 31):

replace_and_shorten: substitute is 7 moves longer; reject.

The replace_and_shorten made things WORSE (delta +7, giving 38 moves total). I'll keep my original 31-move solution. Let me verify it one more time:

verify_solved: ✓ — 31 moves.

Perfect! The solution is verified and solves the scramble in 31 moves.

## Summary

**EO-RL path (5 moves):** `U B D L U'`
- Started with `U B D L` which reduced RL bad edges from 6→4
- Completed EO-RL with one more move `U'`

**DR setup on RL axis (8 moves):** `B' L U2 L2 B F L2 F'`
- Used DR-4C2E trigger (F L2 F') with 5-move setup
- Total to DR: 13 moves

**HTR finish (18 moves):**
- HTR reduction (8 moves): reduced corners to HTR-corner-subgroup
- Finish (10 moves): half-turn finish to solved
- Subset: 2-swap long-cycle

**Final result: 31 moves** (matching my second-best prior attempt)

FINAL_SOLUTION: ["U", "B", "D", "L", "U'", "B'", "L", "U2", "L2", "B", "F", "L2", "F'", "R2", "U2", "F2", "U2", "R'", "U2", "F2", "R", "L2", "U2", "B2", "D2", "R2", "B2", "U2", "L2", "U2", "R2"]

**Verified solution (31 moves):** `U B D L U' B' L U2 L2 B F L2 F' R2 U2 F2 U2 R' U2 F2 R L2 U2 B2 D2 R2 B2 U2 L2 U2 R2`
