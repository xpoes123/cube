# Solve — fm_PSSSideDayGdansk2026_s3__attempt3_20260517_170708

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`

---

*Thinking (1):*

> Let me start by following the instructions. I need to inspect_state on the main slot to understand this scramble.
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Prior attempts were 30 and 31 moves. The instruction is to COMMIT HARD and not over-ideate. I should pick a promising line and drive it to completion.
> 
> Let me start with inspect_state to see the bad edges per axis and make an informed decision about which axis to pursue.

I'll solve this scramble with a committed, single-branch approach. Let me begin by inspecting the state.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

**INITIAL STATE READ**: UD has 4 bad edges (the shortest EO), FB has 8, RL has 6. Bad edges on UD are UL, DR, DL, DB. DR-closeness shows UD is DR-7C3E (unpromising), FB is DR-6C3E, RL is DR-5C3E. **Key signal**: `top_pairs_on_inverse: 3` on UD axis — this is a strong NISS switch signal.

**AXIS SCOUTING PLAN**: Given the prior attempts hit 30-31 moves, I'll scout UD on BOTH normal and inverse. The 4 bad edges on UD should give a short EO, and the 3 pairs on inverse suggest the inverse side might have better DR options. Let me check EO on normal first, then flip to inverse and compare.

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

**UD-normal EO = 4 moves** (`U L R' B'`). Now let me check the inverse side before committing. The NISS invariant tells me the bad-edge count will still be 4 on UD-inverse, but the SOLUTION moves will differ.

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

**UD-inverse EO = 4 moves** (`B' R' U B'`). Same length, so the decision hinges on DR quality. Let me apply the inverse-side EO and check DR options.

I turn `B' R' U B'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

**UD-inverse DR scouting: NO options at depth 5**. This is a bad sign. Let me bounce back to the normal side and check DR there.

NISS flip — switching back to the normal scramble.

Now I'm back on normal with 4 inverse moves in history. Let me reset and try UD-normal EO instead.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `U L R' B'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

**UD-normal also gives NO DR options at depth 5**. The UD axis is not viable. Let me try FB axis — it has 8 bad edges (longer EO expected) but might have cleaner DR.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

**FB-normal EO = 4 moves** (`R' F D L'`). Excellent — the 8-bad-edge case has a clean 4-move fix. Let me apply and check DR.

I turn `R' F D L'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**FB-normal also has NO DR at depth 5**. Let me try RL axis before giving up.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On RL axis I recognize the EO pattern — the first chunk is `U' B' D' R'` (full fix is 4 moves).

**RL EO = 5 moves total** (partial chunk). Let me apply and complete it.

I turn `U' B' D' R'`.

On RL axis I recognize the EO pattern — `U'` fixes it.

I turn `U'`.

**RL EO complete: 5 moves** (`U' B' D' R' U'`). Now checking DR options on RL axis.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on RL.**

**ALL THREE AXES show NO DR at depth 5**. This is a difficult scramble. Following the instruction to "commit a setup move you think looks promising", let me use policy_intuition to get the top candidate moves and extend the search manually. I'll go back to UD-normal (shortest EO at 4 moves) and try a 1-2 move extension.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `U L R' B'`.

I check my gut for plausible next moves.

Top moves are U, U', D2. Let me try `U` first and search DR from depth 6.

I turn `U`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Still nothing. Let me try a different strategy — maybe I should look at the prior solutions' patterns. Both used the sequence starting with `U B D L`. Let me try that beginning.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `U B D L`.

Let me check what axes this achieves EO on.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=4.
Last applied: `U B D L`.

This `U B D L` doesn't achieve EO on any axis yet (still 4/8/4 bad edges). Continuing the pattern from Attempt 1, which was `U B D L U L'`. Let me try adding those moves.

I turn `U L'`.

I look over the cube.
Bad-edge counts: UD=4, FB=6, RL=0.
Last applied: `U B D L U L'`.

**EXCELLENT!** `U B D L U L'` achieves **RL-EO in 6 moves** AND the DR state is DR-4C2E (a good substate). This is what the prior attempts used. Let me check DR options on RL axis now.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C4E (F L2 U2 F): 4-mv setup + 4-mv trigger (8 total) pre=DR-4C2E
  • DR-3C2E (F L F'): 5-mv setup + 3-mv trigger (8 total) pre=DR-3C1E

**FOUND DR OPTIONS!** Two choices:
1. **DR-4C4E (F L2 U2 F)**: setup 4mv + trigger 4mv = **8 moves to DR**, total from start = 6+8 = 14. Pre-trigger is DR-4C2E (good). Typical post-DR for 4C4E is 12-14 moves → **expected total ~26-28**.
2. **DR-3C2E (F L F')**: setup 5mv + trigger 3mv = **8 moves to DR**, total from start = 6+8 = 14. Pre-trigger is DR-3C1E. Typical post-DR for 3C2E is 6-8 moves → **expected total ~20-22**.

**Taking option 2 (DR-3C2E)** — much better substate quality despite same DR length. Committing the setup moves.

I turn `U2 B' L B L' F L F'`.

**DR reached in 14 moves** (6 EO + 8 DR). Now classifying the HTR subset.

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (first exposure — learning).

**HTR subset is "4-swap long-cycle"** (single 8-cycle). HTR reduction = 10 moves, finish = 9 moves, total = 19 moves. Full solution projection: 14 DR + 19 finish = **33 moves**. This is worse than the prior 30-move best.

Let me check if there's a better DR option I missed, or if I should try the alternate DR trigger. Let me undo and try option 1 (DR-4C4E) to compare.

I rewind 4 moves.

I rewind 4 moves.

Now trying option 1 (DR-4C4E).

I turn `F2 U2 L D2 F L2 U2 F`.

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 7 moves, finish is 9 moves (recall).

**Better!** DR-4C4E gives HTR reduction = 7 moves, finish = 9 moves, total = 16 moves. Full solution: 14 DR + 16 finish = **30 moves**. This matches the prior best. Let me apply the HTR phases and complete this solution.

For the corner reduction, I see `R' U2 R U2` (chunk of a 7-move phase) — apply and re-check.

I turn `R' U2 R U2`.

Quick check: DR-locked on RL, not yet HTR.

Still in DR on RL, not yet HTR. Continuing the reduction.

For the corner reduction: `R2 F2 L`.

I turn `R2 F2 L`.

Quick check: in HTR.

**HTR reached in 21 moves** (is_htr_ud = true). Now applying the finish phase.

For the half-turn finish, I see `F2 L2 B2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `F2 L2 B2 L2`.

Quick check: in HTR.

Still not solved. Continuing finish.

For the half-turn finish, I see `U2 L2 R2 F2` (chunk of a 5-move phase) — apply and re-check.

I turn `U2 L2 R2 F2`.

Quick check: in HTR.

29 moves and still not solved. One more move expected.

For the half-turn finish: `U2`.

I turn `U2`.

A quick glance — the cube is solved.

**SOLVED in 30 moves!** Now let me compose the solution and verify.

I assemble the canonical normal-frame solution: **30 moves**, verified.

30 moves — matches the prior best. Before submitting, let me check if replace_and_shorten can improve it. The gate is ≥27 moves AND ≥30 tool calls remaining. I have 30 moves and should have plenty of budget left.

Budget check: 1799.7s sim, None tool calls remaining.

I have 1799.7 seconds remaining (plenty of budget) and the solution is 30 moves. Let me try replace_and_shorten on a large tail span.

r&s: too few tool calls remaining (25) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

The tool enforces a minimum of 30 remaining tool calls. I've used too many already. Let me submit this 30-move solution as-is.

verify_solved: ✓ — 30 moves.

**VERIFIED SOLVE: 30 moves**

## FINAL_SOLUTION

**U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2**

### Solution breakdown:
- **EO (RL-axis)**: `U B D L U L'` — 6 moves
- **DR setup + trigger**: `F2 U2 L D2` (setup) + `F L2 U2 F` (DR-4C4E trigger) — 8 moves
- **HTR reduction**: `R' U2 R U2 R2 F2 L` — 7 moves  
- **HTR finish**: `F2 L2 B2 L2 U2 L2 R2 F2 U2` — 9 moves

**Total: 30 moves** (ties the prior best)

This solve uses the same opening sequence (`U B D L U L'`) as the prior attempts, achieving RL-EO in 6 moves with a good DR-4C2E pre-state. The DR-4C4E trigger (8 moves) leads to a 0-swap long-cycle HTR subset that finishes cleanly in 16 moves post-DR.

*Thinking (58):*

> The user is right - I verified the solution and described it but didn't actually emit the FINAL_SOLUTION in the required format. Let me do that now.

FINAL_SOLUTION: ["U", "B", "D", "L", "U", "L'", "F2", "U2", "L", "D2", "F", "L2", "U2", "F", "R'", "U2", "R", "U2", "R2", "F2", "L", "F2", "L2", "B2", "L2", "U2", "L2", "R2", "F2", "U2"]

**Verified solution (30 moves):** `U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`
