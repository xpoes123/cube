# Solve — fm_PSSSideDayGdansk2026_s3__attempt7_20260517_172028

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`

---

*Thinking (1):*

> Looking at the prior attempts, all 6 attempts ended up at 30-31 moves. The pattern looks like there are two main solution branches:
> 1. Attempts 1, 3, 5, 6: 30 moves - `U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`
> 2. Attempts 2, 4: 31 moves - `U B D L U' B' L U2 L2 B F L2 F' R2 U2 F2 U2 R' U2 F2 R L2 U2 B2 D2 R2 B2 U2 L2 U2 R2`
> 
> The instruction says to COMMIT HARD and drive to a clean finish. The best is 30 moves. I should:
> 1. Start with inspect_state to see the cube
> 2. Scout EO on all axes (both normal and inverse)
> 3. Pick the most promising axis based on EO+DR joint cost
> 4. Commit and drive through to completion
> 5. Use replace_and_shorten if I have ≥27 moves and sufficient budget remaining
> 
> The instruction emphasizes NOT to over-ideate or abandon mid-solve. I need to be decisive and complete.
> 
> Let me start.

I'll solve this scramble systematically, following the elite FMC pipeline. The prior attempts all converged around 30-31 moves, so I need to find either the same line with better finish optimization or discover a cleaner DR substate path.

Let me start by inspecting the cube state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good. I can see:
- **UD axis: 4 bad edges** (UL, DR, DL, DB) — cheapest EO
- **FB axis: 8 bad edges** — all-bad, likely NISS candidate
- **RL axis: 6 bad edges**
- **DR closeness**: UD shows DR-7C3E (bad), BUT `top_pairs_on_inverse: 3` — that's a strong NISS signal (≥2 pairs)
- No JZP eligible on any axis in normal frame

**NISS-FIRST RULE**: With 3 pairs on inverse for UD, I should check inverse-UD. The bad-edge count stays the same (NISS invariant), but the solution and DR options will differ.

**Strategy**: Scout UD-normal EO first (4 bad edges should be 1-3 moves), then flip to inverse and scout UD-inverse EO. Compare the joint EO+DR cost. With 3 pairs preserved on inverse, the inverse frame is likely superior.

Let me scout UD-normal EO first:

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

UD-normal EO is **4 moves** (U L R' B'). Now let me check the inverse frame:

NISS flip — switching to the inverse scramble.

Now on inverse. Let me scout UD-inverse EO:

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

UD-inverse EO is also **4 moves** (B' R' U B'). Same length, so the deciding factor will be DR options. With 3 pairs on inverse, I expect inverse-UD to have cleaner DR. Let me commit the inverse EO and probe DR:

I turn `B' R' U B'`.

Now check DR options on UD axis from this EO state:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

No DR options within 5 moves on inverse-UD! This is unexpected given the 3 pairs signal. Let me check if I should try a different axis. But first, let me compare: if inverse-UD doesn't have good DR options, maybe normal-UD does. Let me flip back and test:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Back to normal. Let me apply the normal-UD EO and check its DR options:

I turn `U L R' B'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Also no options on normal-UD within 5 moves! This suggests the UD axis might not be the right choice despite having the fewest bad edges. Let me try FB axis. Let me reset and check FB:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

FB has 8 bad edges (all-bad). Let me scout FB-normal EO:

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

FB-normal is also **4 moves** (R' F D L'). Let me apply and check DR:

I turn `R' F D L'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Also nothing! Let me try RL axis:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On RL axis I recognize the EO pattern — the first chunk is `U' B' D' R'` (full fix is 4 moves).

RL is **5 moves** (partial showing 4). This is getting long. All axes are showing 4-5 move EOs with no DR options within 5 moves. This scramble seems difficult for the standard EO→DR pipeline.

Looking at the prior attempts, they all started with `U B D L` — let me check what that sequence does:

I try `U B D L` on top to see the after-state (without committing).

After `U B D L`:
- RL goes from 6→4 bad edges
- UD stays at 4 bad edges (but different edges)
- top_pairs_on_inverse increases to 4 on UD

This is interesting! `U B D L` is a 4-move setup that improves RL to 4 bad edges. Let me apply this and continue on RL:

I turn `U B D L`.

Now check RL EO from this state:

On RL axis I recognize the EO pattern — `U'` fixes it.

Excellent! After `U B D L`, RL-axis EO is just **1 move** (U')! So total EO is `U B D L U'` = 5 moves to RL-EO. This matches the pattern in the prior attempts. Let me apply and check DR:

I turn `U'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C2E (F L2 F'): 5-mv setup + 3-mv trigger (8 total) pre=DR-4C1E

Found one option:
- **DR-4C2E trigger** with setup `B' L U2 L2 B`, total **8 moves to DR** (5 setup + 3 trigger)
- Not JZP-eligible
- DR-4C2E typically has 9-11 move post-DR finish

So the path would be:
- EO: 5 moves (`U B D L U'`)
- DR: 8 moves (`B' L U2 L2 B F L2 F'`)
- Total to DR: 13 moves
- Expected total to solved: 13 + ~10 = **~23 moves**

This is promising! Much better than the 30-move prior attempts. Let me commit to this path and drive through to completion:

I turn `B' L U2 L2 B F L2 F'`.

At DR in 13 moves. Now let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 8 moves, finish is 10 moves (recall).

The HTR subset is "2-swap long-cycle" with:
- HTR reduction: 8 moves
- Finish: 10 moves
- Total: 18 moves

So projected total: 13 (to DR) + 18 (to solved) = **31 moves**. This is same as the 30-31 move prior attempts. Let me continue and see if there are opportunities to shorten:

For the corner reduction, I see `R2 U2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

Partial HTR reduction (4 moves shown). Let me apply and check state:

I turn `R2 U2 F2 U2`.

Quick check: DR-locked on RL, not yet HTR.

Still in DR, not at HTR yet. Continue:

For the corner reduction: `R' U2 F2 R`.

I turn `R' U2 F2 R`.

Quick check: in HTR.

Now at HTR! 21 moves so far. Let me proceed with the finish:

For the half-turn finish, I see `L2 U2 B2 D2` (chunk of a 10-move phase) — apply and re-check.

I turn `L2 U2 B2 D2`.

Quick check: in HTR.

Still in HTR, not solved. Let me check if there's a 3-cycle residual:

Residual class: mixed.

Mixed residual with 2 corner 2-cycles and complex edge cycles. Not a pure 3-cycle. Let me continue the finish:

For the half-turn finish, I see `R2 B2 U2 L2` (chunk of a 6-move phase) — apply and re-check.

I turn `R2 B2 U2 L2`.

Quick check: in HTR.

Residual class: mixed.

Now I have two corner 3-cycles! But also edge issues, so not pure. Let me continue:

For the half-turn finish: `U2 R2`.

I turn `U2 R2`.

A quick glance — the cube is solved.

Solved in **31 moves**! Same as attempts 2 and 4. Let me verify and check for cancellations:

I check for cancellations — no savings.

No cancellations. Still 31 moves. Let me verify it solves:

verify_solved: ✓ — 31 moves.

Verified 31-move solution. I should try replace_and_shorten since I have a complete solve ≥27 moves and plenty of budget remaining:

Budget check: 2391.43s sim, None tool calls remaining.

I have 2391 seconds of sim budget remaining. The instruction says to use replace_and_shorten if I have ≥27 moves and ≥30 tool calls remaining. I've used about 30 tool calls so far, so I should have plenty remaining. Let me try replace_and_shorten on a large span. Looking at the solution, the finish is quite long (last ~15 moves). Let me try to shorten the tail:

replace_and_shorten: substitute is 1 moves longer; reject.

Replace_and_shorten made it **worse** (+1 move). The substitute is 19 moves vs original 18. Let me not accept this. My current solution is still 31 moves, same as prior attempts 2 and 4.

Looking at the prior best (30 moves from attempts 1, 3, 5, 6), they started with the same `U B D L` but then had `U L' F2 U2 L` instead of `U' B' L U2 L2 B F L2 F'`. Let me see if I can find a different path. But the instruction says to COMMIT and not over-ideate. I have a working 31-move solution.

However, I notice in the prior attempts, the best ones (30 moves) had a different continuation after `U B D L`. Let me reset and try that path:

Actually, wait. The instruction says "COMMIT HARD this attempt" and "do NOT abandon a path halfway through". I already have a complete 31-move solution. The prior best is 30 moves. I should check if there's an obvious improvement I can make before submitting.

Looking at my solution more carefully:
`U B D L U' B' L U2 L2 B F L2 F' R2 U2 F2 U2 R' U2 F2 R L2 U2 B2 D2 R2 B2 U2 L2 U2 R2`

This is actually identical to attempts 2 and 4! And the 30-move solution was:
`U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`

The difference starts at move 5. Mine has `U' B' L U2 L2 B F L2 F'`, theirs has `U L' F2 U2 L D2 F L2 U2 F R'`. 

Let me try the 30-move path. I'll reset and scout that direction:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `U B D L U L' F2 U2 L`.

Quick check: EO solved on RL, working toward DR.

This gives RL-EO in 9 moves. Let me check DR options:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C4E (F L2 U2 F): 1-mv setup + 4-mv trigger (5 total) pre=DR-4C2E
  • DR-4C2E (F L2 F'): 4-mv setup + 3-mv trigger (7 total) pre=DR-4C1E
  • DR-4C4E (F): 4-mv setup + 1-mv trigger (5 total) pre=DR-4C2E

Great! Multiple DR options from this path:
- **DR-4C4E** with 1-move setup (D2), total 5 to DR → 9 + 5 = 14 to DR
- **DR-4C4E** with 4-move setup, total 5 to DR → 9 + 5 = 14 to DR

So this path reaches DR in 14 moves (vs my 13-move path). The prior 30-move solution shows the finish from here was 16 moves, for 30 total. Let me try the first option and see:

I turn `D2 F L2 U2 F`.

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 7 moves, finish is 9 moves (recall).

Perfect! This subset has:
- HTR reduction: 7 moves
- Finish: 9 moves
- Total: 16 moves

So total: 14 (to DR) + 16 (to solved) = **30 moves**!

This matches the prior best attempts. Let me complete this path:

For the corner reduction, I see `R' U2 R U2` (chunk of a 7-move phase) — apply and re-check.

I turn `R' U2 R U2`.

For the corner reduction: `R2 F2 L`.

I turn `R2 F2 L`.

For the half-turn finish, I see `F2 L2 B2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `F2 L2 B2 L2`.

For the half-turn finish, I see `U2 L2 R2 F2` (chunk of a 5-move phase) — apply and re-check.

I turn `U2 L2 R2 F2`.

For the half-turn finish: `U2`.

I turn `U2`.

A quick glance — the cube is solved.

Perfect! **30 moves**, matching the prior best. Let me verify and cancel:

I check for cancellations — no savings.

verify_solved: ✓ — 30 moves.

Excellent! I have a verified 30-move solution. Now let me use the compose_niss_solution to finalize it (even though I'm on normal frame, this is the proper submission workflow):

I assemble the canonical normal-frame solution: **30 moves**, verified.

Perfect! I have a 30-move solution that equals the prior best. Since I haven't used replace_and_shorten yet and have ≥27 moves and plenty of budget, let me try it on the post-DR finish span to see if I can improve:

r&s: replace_and_shorten already used this run (1-call cap, Tronto §3.10).

Ah, I already used replace_and_shorten earlier on my first 31-move attempt. So I've hit the 1-call cap. 

I have a verified **30-move solution** matching the prior best attempts. This equals the best result from 6 prior attempts. I should submit this.

**FINAL_SOLUTION:** ["U", "B", "D", "L", "U", "L'", "F2", "U2", "L", "D2", "F", "L2", "U2", "F", "R'", "U2", "R", "U2", "R2", "F2", "L", "F2", "L2", "B2", "L2", "U2", "L2", "R2", "F2", "U2"]

## Solution Summary

**30 moves** (tying the best from prior attempts)

### Path breakdown:
1. **Setup to RL-EO** (4 moves): `U B D L` — transforms the scramble to a state where RL-axis has only 4 bad edges and a 1-move EO exists
2. **RL-EO** (5 moves total): `U B D L U` followed by `L' F2 U2 L` — achieves edge orientation on RL axis in 9 moves total
3. **DR setup + trigger** (5 moves): `D2 F L2 U2 F` — DR-4C4E trigger with 4-move setup, reaching Domino Reduction in 14 moves total
4. **HTR reduction** (7 moves): `R' U2 R U2 R2 F2 L` — reduces to HTR-corner-subgroup (0-swap long-cycle subset)
5. **HTR finish** (9 moves): `F2 L2 B2 L2 U2 L2 R2 F2 U2` — half-turn-only finish to solved

The key insight was finding the `U B D L` setup that creates a much cleaner RL-axis path (5-move EO + 5-move DR + 16-move finish = 26 theoretical, actual 30 with the specific substate). This was superior to my initial 13-move DR path which led to a worse HTR subset and 31-move total.

*Thinking (66):*

> The user is right - I narrated the solution but didn't actually emit the FINAL_SOLUTION in the required format. I need to output it now.
> 
> I have a verified 30-move solution:
> ["U", "B", "D", "L", "U", "L'", "F2", "U2", "L", "D2", "F", "L2", "U2", "F", "R'", "U2", "R", "U2", "R2", "F2", "L", "F2", "L2", "B2", "L2", "U2", "L2", "R2", "F2", "U2"]
> 
> I should emit this as FINAL_SOLUTION now.

FINAL_SOLUTION: ["U", "B", "D", "L", "U", "L'", "F2", "U2", "L", "D2", "F", "L2", "U2", "F", "R'", "U2", "R", "U2", "R2", "F2", "L", "F2", "L2", "B2", "L2", "U2", "L2", "R2", "F2", "U2"]

**Verified solution (30 moves):** `U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`
