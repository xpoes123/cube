# Solve — fm_PSSSideDayGdansk2026_s2__attempt3_20260517_145653

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`

---

*Thinking (1):*

> Let me start by inspecting the state to see what we're working with. This is a fresh attempt, but I have context from two prior solves:
> - Attempt 1: 33 moves
> - Attempt 2: 31 moves
> 
> The instruction is clear: COMMIT HARD to one line, don't over-ideate, finish cleanly. Let me start with inspect_state to see the bad edges per axis and other key information.

I'll solve this scramble systematically. Let me start by inspecting the cube state to understand what I'm working with.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good starting state. I see:
- **FB and RL axes both have 4 bad edges** (best EO candidates)
- **UD axis has 6 bad edges** (feasible but longer)
- **UD axis has 3 pairs on inverse** (strong NISS signal per Wen's pairs-tracing)
- **FB: DR-7C2E**, **RL: DR-6C2E** — both are reasonable starting points

Given the prior attempts reached 31-33 moves, I'll commit to one path and drive it cleanly. Let me scout EO on the normal side first for FB and RL (the 4-bad-edge axes), then check inverse if needed.

**FB-axis EO scouting** (4 bad edges on DR, DL, FR, BL):
FB-axis flipping moves are L, L', R, R'. Let me look at the pattern:

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

**RL-axis EO scouting** (4 bad edges on UL, DR, DF, FR):
RL-axis flipping moves are U, U', D, D'.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL give 4-move EOs. Now let me check **inverse** for both axes since the UD axis showed 3 pairs on inverse (strong NISS signal). Let me flip and check FB on inverse:

NISS flip — switching to the inverse scramble.

Now I'm on the inverse. Let me check FB-axis EO on inverse:

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

**Excellent!** FB-axis on inverse gives a **2-move EO** (U2 R'). This is 2 moves shorter than the normal-side 4-move EOs. Combined with the 3 pairs on inverse signal, this is a strong candidate.

Let me also check RL-axis on inverse for completeness:

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

RL on inverse is 5 moves (partial shown). So:
- **FB-inverse: 2-move EO** ✓
- **RL-inverse: 5-move EO**
- **FB-normal: 4-move EO**
- **RL-normal: 4-move EO**

Now let me probe DR options for the FB-inverse 2-move EO to see if the joint EO+DR is favorable:

I probe what DR would look like if I applied this EO (without committing).

**FB-inverse: 2 EO + 7 DR = 9 total to DR** — that's good, but let me commit to the 2-move EO and then use dr_trigger_options to see the specific trigger families and substates. Applying the 2-move FB-inverse EO:

I turn `U2 R'`.

Good. Now I'm EO-solved on FB-axis (on inverse side). Let me call dr_trigger_options to see what DR options I have:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**No DR trigger options found within 5 moves** on FB-inverse. This suggests the FB-axis might not be the best choice, or the DR is beyond the standard trigger families. Let me backtrack and try a different approach.

Given that the prior attempts reached 31-33 moves, let me try the **UD-axis on inverse** since it showed 3 pairs on inverse. Let me undo and test:

I rewind 2 moves.

I'm back at the inverse scramble start. Let me check UD-axis EO on inverse:

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

**UD-inverse: 4-move EO** (B R2 U F'). Let me probe DR for this:

I probe what DR would look like if I applied this EO (without committing).

**UD-inverse: 4 EO + 4 DR = 8 total to DR** — this is better than FB-inverse (2 EO + 7 DR = 9). Let me commit to UD-inverse and apply the EO:

I turn `B R2 U F'`.

Good! EO is solved on UD-axis (inverse side). Now let me call dr_trigger_options to see the specific trigger families:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Again no options within 5 moves. This is challenging. Let me use dr_recognize instead as a fallback to get the DR pattern beyond the trigger catalog:

I check whether the DR is recognizable from this state via the library.

The DR is 8 moves total (4 setup shown). Let me apply these 4 setup moves and then query again:

I turn `D' U' L2 R'`.

I check whether the DR is recognizable from this state via the library.

Good! The remaining DR is 4 moves (3 setup + 1 trigger). So total to DR is 8 + 4 = **12 moves** on UD-inverse. That's higher than the 8-move estimate, which means the probe was optimistic. Let me apply these final 4 DR moves:

I turn `U' L' U2 R'`.

I'm now at DR on UD-axis (12 moves so far on inverse). Let me check the HTR state and classify the subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 10 moves (first exposure — learning).

**This is concerning**: the HTR finish is 21 moves (11 reduction + 10 finish). Combined with 12 to DR, that's **33 total moves** — matching the first prior attempt. This path isn't better.

Let me reconsider. I'll reset and try the **normal side** instead. The prior attempts might have been on normal RL or FB. Let me reset and explore normal-side options more carefully:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I'm back to the normal scramble. Let me try **RL-normal 4-move EO** and probe its DR:

I probe what DR would look like if I applied this EO (without committing).

**RL-normal: 4 EO + 4 DR = 8 total to DR** — same as UD-inverse. Let me commit to RL-normal and see if the finish is better:

I turn `R2 B F2 U'`.

I check whether the DR is recognizable from this state via the library.

I turn `L' B' L' R2`.

I check whether the DR is recognizable from this state via the library.

I turn `U2 B R2 F'`.

I'm at DR on RL-axis (12 moves). Let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 11 moves (first exposure — learning).

Again **21-move finish** (10 + 11), giving **33 total** (12 + 21). This is the same as UD-inverse. Let me try **FB-normal** to see if it's any better:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `B2 L2 U2 R'`.

I check whether the DR is recognizable from this state via the library.

I turn `R2 B' D L2`.

There was an auto-cancel (R' + R2 = R). Good! Let me continue:

I check whether the DR is recognizable from this state via the library.

I turn `U B2 F' U'`.

I'm at DR in **11 moves** (1 move saved from cancel). Let me classify HTR:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 10 moves, finish is 9 moves (first exposure — learning).

**Better!** HTR finish is 19 moves (10 + 9), giving **30 total** (11 + 19). This is 1 move better than the prior best attempt (31). Let me proceed with the HTR finish and then see if I can optimize further:

For the corner reduction, I see `F' R2 F L2` (chunk of a 10-move phase) — apply and re-check.

I turn `F' R2 F L2`.

Let me do a quick_check to see if I've already reached an insertable residual:

Quick check: DR-locked on FB, not yet HTR.

Still in DR on FB, not yet HTR. Let me continue the HTR reduction:

For the corner reduction, I see `F' U2 R2 F'` (chunk of a 6-move phase) — apply and re-check.

I turn `F' U2 R2 F'`.

Quick check: DR-locked on FB, not yet HTR.

Still not HTR yet. Let me continue:

For the corner reduction: `L2 B`.

I turn `L2 B`.

Quick check: in HTR.

Great! I'm now at **HTR** (21 moves). Now let me apply the finish phase:

For the half-turn finish, I see `U2 L2 U2 R2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 L2 U2 R2`.

Quick check: in HTR.

Still not solved. Let me continue the finish:

For the half-turn finish, I see `B2 D2 U2 L2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 D2 U2 L2`.

Quick check: in HTR.

For the half-turn finish: `U2`.

I turn `U2`.

A quick glance — the cube is solved.

**Excellent!** The cube is solved in **30 moves**. This is 1 move better than the prior best (31). Now let me apply cancellation to see if I can save any moves:

I assemble the canonical normal-frame solution: **30 moves**, verified.

The solution is already cancelled and verified at **30 moves**. Now, since I have a 30-move solution (≥27) and haven't called replace_and_shorten yet, let me try to apply it once to see if I can improve further. The tool will check the gates automatically:

Budget check: 2874.64s sim, None tool calls remaining.

I have plenty of budget. Let me try replace_and_shorten on a suspicious span. Looking at the solution, the tail has many double moves which might be optimizable. Let me try the span from move 4 to the end:

r&s: too few tool calls remaining (25) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

The tool gate blocks me because I don't have enough tool calls remaining. That's fine — I have a solid **30-move solution** which is 1 move better than the prior best. Let me verify and submit:

verify_solved: ✓ — 30 moves.

Perfect! The solution is verified. Let me submit it:

## FINAL_SOLUTION: ["B2", "L2", "U2", "R", "B'", "D", "L2", "U", "B2", "F'", "U'", "F'", "R2", "F", "L2", "F'", "U2", "R2", "F'", "L2", "B", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "L2", "U2"]

**Solution summary:**
- **30 moves total** (1 move improvement over prior best of 31)
- **Approach:** FB-axis normal-side solve
  - **EO:** 4 moves (B2 L2 U2 R')
  - **DR:** 7 moves (with 1 cancel) → 11 moves total to DR
  - **HTR subset:** 2-swap mostly-axial
  - **HTR reduction:** 10 moves → 21 moves total to HTR
  - **Finish:** 9 moves → 30 moves total

The FB-normal axis gave the shortest overall path by producing a better HTR subset (19-move finish vs 21-move on other axes). The key was selecting the axis not just by shortest EO, but by the joint EO+DR+finish length, which FB-normal optimized best.

**Verified solution (30 moves):** `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`
