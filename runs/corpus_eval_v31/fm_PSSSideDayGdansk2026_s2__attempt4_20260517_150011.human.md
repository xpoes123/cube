# Solve — fm_PSSSideDayGdansk2026_s2__attempt4_20260517_150011

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`

---

*Thinking (1):*

> Alright, I'm on my 4th attempt on this scramble. The best so far is 30 moves. The instruction is clear: COMMIT HARD. Pick a line and drive it to a clean finish. Don't over-ideate, don't abandon mid-way.
> 
> Looking at my prior attempts, I should:
> 1. Inspect the state to see what the EO options are
> 2. Pick a promising EO+DR axis (maybe analyze what worked in the 30-move solve)
> 3. Commit to that path and drive it to completion
> 4. Use the tools efficiently - don't waste time branching
> 
> Let me start with inspect_state to see the bad edges per axis and understand the landscape.

I'll solve this scramble with full commitment to a single clean line. Let me start by inspecting the state to understand the EO landscape.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good landscape here. I see:
- **FB: 4 bad edges** (DR, DL, FR, BL) — shortest EO candidate
- **RL: 4 bad edges** (UL, DR, DF, FR)  
- **UD: 6 bad edges** — probably not the path

The DR closeness shows **UD has 3 pairs on inverse** (top_pairs_on_inverse: 3), which is a STRONG NISS signal even though UD EO is 6 bad edges. But let me first scout the cleaner FB and RL EO options on the normal side, then check inverse if needed.

Let me scout **FB-axis EO** first (4 bad edges on L/R flipping faces):

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

**FB-axis EO: 4 moves (B2 L2 U2 R')**.

Now let me check **RL-axis EO** (also 4 bad edges):

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

**RL-axis EO: 4 moves (R2 B F2 U')**.

Both FB and RL are 4-move EOs. The 30-move prior solve started with **B2 L2 U2 R'** which is the FB-axis EO! That suggests FB was a good line. But let me also check the **inverse side** because UD has 3 pairs on inverse — that's a strong signal. Let me flip and check UD-inverse EO:

NISS flip — switching to the inverse scramble.

Now on the inverse. UD had 6 bad edges on normal, so it's still 6 bad on inverse (NISS invariant). Let me check the UD-inverse EO:

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

Excellent! **UD-inverse EO: 4 moves (B R2 U F')** — same length as FB/RL on normal! And UD has 3 pairs on inverse, which is a strong NISS signal. Let me probe DR for all three candidates:

1. **FB-normal** (B2 L2 U2 R')
2. **RL-normal** (R2 B F2 U')
3. **UD-inverse** (B R2 U F') — with 3 pairs preserved

Let me probe DR for each. First, flip back to normal and probe FB:

NISS flip — switching back to the normal scramble.

Back on normal. Let me probe FB-axis DR:

I probe what DR would look like if I applied this EO (without committing).

**FB-normal: EO=4, DR=8, total 12 to DR**. That's acceptable but not great. Let me probe RL-normal:

I probe what DR would look like if I applied this EO (without committing).

**RL-normal: EO=4, DR=8, total 12 to DR**. Same as FB.

Now let me flip back to inverse and probe UD-inverse DR:

NISS flip — switching to the inverse scramble.

I probe what DR would look like if I applied this EO (without committing).

**UD-inverse: EO=4, DR=8, total 12 to DR**. All three are identical at 12 moves to DR!

**Decision point:** All three candidates reach DR in 12 moves. The prior 30-move solve used FB-normal. But UD-inverse has **3 pairs preserved**, which is a strong signal for better post-DR quality. Let me **commit to UD-inverse** — the pairs signal suggests a cleaner finish even if the DR cost is the same.

Let me apply the UD-inverse EO:

I turn `B R2 U F'`.

EO complete on UD-inverse (4 moves). Now let me find the DR trigger options:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on UD.**

Hmm, no DR trigger options found within 5 moves! This is unexpected. Let me use dr_recognize instead to get the full DR path:

I check whether the DR is recognizable from this state via the library.

The DR is 8 moves total as probed. Let me apply the first 4 setup moves:

I turn `D' U' L2 R'`.

Now re-query DR:

I check whether the DR is recognizable from this state via the library.

Perfect! DR trigger is visible now: **setup (U' L' U2) + trigger (R')**. Total 4 more moves (12 to DR as probed). Let me apply them:

I turn `U' L' U2 R'`.

DR reached! 12 moves on the inverse side. Now let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 10 moves (recall).

HTR subset: **2-swap long-cycle**. HTR reduction = 11 moves, finish = 10 moves. Total 21 moves from DR to solved. So the complete solve would be:
- EO (inverse): 4 moves
- DR (inverse): 8 moves
- HTR reduction: 11 moves
- Finish: 10 moves
**Total: 33 moves** (same as attempt 1!)

This is not improving. Let me think — the issue is the HTR finish is too long (21 moves). Let me apply the HTR reduction and check for residuals along the way:

For the corner reduction, I see `U2 R2 U' B2` (chunk of a 11-move phase) — apply and re-check.

HTR reduction is partial (11 moves total, showing first 4). Let me apply this chunk:

I turn `U2 R2 U' B2`.

Let me check if we've landed on a residual:

Quick check: DR-locked on UD, not yet HTR.

Not in HTR yet. Let me continue the HTR reduction:

For the corner reduction, I see `U R2 U2 F2` (chunk of a 7-move phase) — apply and re-check.

I turn `U R2 U2 F2`.

Quick check: DR-locked on UD, not yet HTR.

Still not in HTR. Continue:

For the corner reduction: `U' F2 U`.

I turn `U' F2 U`.

Quick check: in HTR.

HTR reached! 23 moves on inverse. Now let me check if there's a clean residual before finishing:

Residual class: mixed.

Not a clean 3-cycle — it's a mixed state with 8 corners and 9 edges unsolved. Let me continue with the HTR finish:

For the half-turn finish, I see `L2 F2 D2 R2` (chunk of a 10-move phase) — apply and re-check.

I turn `L2 F2 D2 R2`.

Quick check: in HTR.

Still not solved. Continue finish:

For the half-turn finish, I see `F2 R2 F2 D2` (chunk of a 6-move phase) — apply and re-check.

I turn `F2 R2 F2 D2`.

Quick check: in HTR.

Continue:

For the half-turn finish: `U2 R2`.

I turn `U2 R2`.

A quick glance — the cube is solved.

**Solved!** 33 moves on the inverse side. This matches attempt 1 (also 33 moves), so it's not improving. Let me compose the solution and see if there are any cancellations:

I assemble the canonical inverse-frame solution: **33 moves**, verified.

The solution is 33 moves with no cancellations. This is the same as attempt 1, NOT improving over the 30-move prior best.

The UD-inverse line didn't work better despite the 3-pairs signal. Let me **reset and try the FB-normal line** that produced the 30-move solve in the prior attempt. I need to commit to a different axis.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Let me go with **FB-normal** (the 30-move prior line). Apply the FB EO:

I turn `B2 L2 U2 R'`.

FB EO done (4 moves on normal). Now let me get the DR options:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤6), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤6 moves on FB.**

No trigger options found on FB either! Let me use dr_recognize:

I check whether the DR is recognizable from this state via the library.

I turn `R2 B' D L2`.

Good, there was 1 cancellation (R' + R2 = R). Continue:

I check whether the DR is recognizable from this state via the library.

I turn `U B2 F' U'`.

DR reached! 11 moves (one less than UD-inverse due to the cancellation). Now HTR classify:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 10 moves, finish is 9 moves (recall).

Excellent! **2-swap mostly-axial**: HTR reduction = 10, finish = 9, total 19 from DR. This is **2 moves better** than the UD-inverse path (which was 21 moves from DR). Total projected:
- EO: 4
- DR: 7 (with 1 cancel)
- HTR+finish: 19
**Total: 30 moves** — matches the prior best!

Let me apply the HTR and see if we can find a better residual or any optimizations:

For the corner reduction, I see `F' R2 F L2` (chunk of a 10-move phase) — apply and re-check.

I turn `F' R2 F L2`.

Quick check: DR-locked on FB, not yet HTR.

Continue HTR reduction:

For the corner reduction, I see `F' U2 R2 F'` (chunk of a 6-move phase) — apply and re-check.

I turn `F' U2 R2 F'`.

Quick check: DR-locked on FB, not yet HTR.

For the corner reduction: `L2 B`.

I turn `L2 B`.

Quick check: in HTR.

HTR reached at 21 moves. Let me check for a residual:

Residual class: mixed.

Not a pure 3-cycle. Continue with finish:

For the half-turn finish, I see `U2 L2 U2 R2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 L2 U2 R2`.

Quick check: in HTR.

For the half-turn finish, I see `B2 D2 U2 L2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 D2 U2 L2`.

Quick check: in HTR.

For the half-turn finish: `U2`.

I turn `U2`.

A quick glance — the cube is solved.

**SOLVED in 30 moves!** This matches the prior best. Let me compose and verify:

I assemble the canonical normal-frame solution: **30 moves**, verified.

30 moves, solves correctly. This is FB-normal, matching the prior 30-move solution from attempt 3 (which also started with B2 L2 U2 R'). The solution is almost identical — it's the same line!

I'm at 30 moves, which ties the best. The instructions say I can try replace_and_shorten IF I have ≥30 tool calls remaining. Let me check my budget:

Budget check: 2937.26s sim, None tool calls remaining.

I have ~2937s remaining (plenty of budget). The 30-move solution qualifies for replace_and_shorten (≥27 moves). Let me try it on a large span to see if I can find a shortcut. I'll try the tail from move 4 onward (after EO):

r&s: too few tool calls remaining (13) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

I don't have enough tool calls remaining for replace_and_shorten. The tool says I need ≥30 tool calls but I only have 13 remaining. I should submit the current 30-move solution.

Let me verify the solution one more time:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified and solves the scramble in 30 moves.

## FINAL SOLUTION

**30 moves** — FB-axis normal solve:

**EO (FB-axis, 4 moves):** B2 L2 U2 R — fixes the 4 bad edges on the L/R flipping faces.

**DR (8 moves with 1 cancellation → 7 net):** R' cancelled to R when followed by R2 B' D L2, then setup + trigger U B2 F' U'.

**HTR reduction (10 moves):** F' R2 F L2 F' U2 R2 F' L2 B — reducing to the 2-swap mostly-axial HTR subset.

**Finish (9 moves):** U2 L2 U2 R2 B2 D2 U2 L2 U2 — half-turn-only finish.

This matches the prior best of 30 moves. The FB-normal line is consistent and clean. I committed to this axis and drove it to completion without branching mid-solve.

FINAL_SOLUTION: ["B2", "L2", "U2", "R", "B'", "D", "L2", "U", "B2", "F'", "U'", "F'", "R2", "F", "L2", "F'", "U2", "R2", "F'", "L2", "B", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "L2", "U2"]

**Verified solution (30 moves):** `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`
