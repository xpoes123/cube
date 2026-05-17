# Solve — fm_PSSSideDayGdansk2026_s2__attempt4_20260517_100111

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`

---

*Thinking (1):*

> Let me understand the context:
> - This is my 4th attempt on this scramble
> - Previous attempts: 32, 29, 30 moves
> - Best so far is 29 moves
> - The instruction is clear: COMMIT HARD to one line, don't over-ideate, drive to a clean finish
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> Let me start by inspecting the state to see the bad edge counts per axis and other key features. Then I'll decide on an axis based on what looks most promising, considering what the prior attempts likely explored.
> 
> My strategy:
> 1. Inspect state to see bad edge counts per axis
> 2. Scout EO on the most promising 1-2 axes (both normal and inverse)
> 3. For each viable EO, probe DR cost using probe_dr_pattern or dr_trigger_options
> 4. Pick the joint-shortest EO+DR combination
> 5. Execute cleanly through DR → HTR → finish
> 6. Submit when verified
> 
> Let's begin.

I'll solve this scramble systematically. With three prior attempts at 29-32 moves, I need to find a cleaner line and execute it fully. Let me start by inspecting the state.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good! I can see:
- **FB axis: 4 bad edges** (DR, DL, FR, BL) — L flips DL+BL, R flips DR+FR. This is a VERY clean 2-move pattern.
- **RL axis: 4 bad edges** (UL, DR, DF, FR) — scattered across U and D faces
- **UD axis: 6 bad edges** — more complex

FB axis looks promising with that symmetric 2-2 split. Also note **top_pairs_on_inverse = 3** on UD axis — that's a strong NISS signal. Let me scout both FB-normal and UD-inverse.

Starting with **FB axis on normal side** (the 4 bad edges split cleanly):

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

**FB-normal EO = 4 moves** (B2 L2 U2 R'). Now let me check the inverse side for UD axis (3 pairs preserved on inverse):

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check UD-axis EO here:

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

**UD-inverse EO = 4 moves** (B R2 U F'). Both axes tie at 4 moves for EO. Now I need to probe DR on each:

Let me probe DR for **FB-normal** first. I'll flip back to normal:

NISS flip — switching back to the normal scramble.

Back to normal. Now probe DR for FB-axis after the 4-move EO:

I probe what DR would look like if I applied this EO (without committing).

**FB-normal: 4-move EO + 8-move DR = 12 moves to DR.** That's acceptable but not great. Now let me probe UD-inverse. I need to flip back:

NISS flip — switching to the inverse scramble.

On inverse now. Probe DR for UD-axis after the 4-move inverse EO:

I probe what DR would look like if I applied this EO (without committing).

**UD-inverse: 4-move EO + 8-move DR = 12 moves to DR** (same as FB-normal). Both tie at 12 moves to DR. However, the **3 pairs preserved on inverse for UD** is a strong signal. Let me commit to **UD-inverse** and apply the EO:

I turn `B R2 U F'`.

Good! **EO complete on UD-axis (inverse side) in 4 moves.** Now I need to find DR. Let me use dr_trigger_options to see all the candidates:

DR trigger menu on UD: no named trigger fits within 5 setup moves.

No triggers found within 5-move setup. Let me try dr_recognize as a fallback:

I check whether the DR is recognizable from this state via the library.

I see 4 moves of setup progress toward DR. This gets me closer but I need to apply them and re-query. Let me apply:

I turn `D' U' L2 R'`.

Now re-query dr_recognize:

I check whether the DR is recognizable from this state via the library.

Perfect! **DR trigger visible: 3-move setup (U' L' U2) + 1-move trigger (R') = 4 more moves to DR.** Total: 4 (EO) + 4 (first setup) + 4 (second setup + trigger) = **12 moves to DR** on inverse. Let me apply:

I turn `U' L' U2`.

I turn `R'`.

**DR reached in 12 moves!** Now let me check if I'm actually in DR and classify the HTR subset:

Quick check: DR-locked on UD, not yet HTR.

Confirmed: **DR on UD axis achieved!** Not yet HTR. Let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 10 moves (recall).

This is a **2-swap long-cycle subset**: 11 moves for HTR reduction + 10 moves for finish = **21 moves from DR to solved**. Total would be 12 + 21 = **33 moves**, which is worse than my best prior (29 moves).

This line isn't better. Let me reconsider. I should try the **FB-normal axis** instead — it also had 12 moves to DR. Let me reset and try that:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Now let me try **FB-normal axis**. Apply the 4-move EO:

I turn `B2 L2 U2 R'`.

Now find DR on FB axis:

DR trigger menu on FB: no named trigger fits within 5 setup moves.

No triggers within 5 moves. Use dr_recognize:

I check whether the DR is recognizable from this state via the library.

8 moves total for DR on FB. Apply the 4 setup moves:

I turn `R2 B' D L2`.

Good, 1 move cancelled (R' + R2 → R). Now re-query:

I check whether the DR is recognizable from this state via the library.

Perfect! 3-move setup + 1-move trigger. Apply:

I turn `U B2 F' U'`.

**DR reached in 11 moves on FB axis!** That's 1 move better than UD-inverse. Let me check and classify HTR:

Quick check: DR-locked on FB, not yet HTR.

Confirmed DR on FB. Now classify HTR:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 10 moves, finish is 9 moves (first exposure — learning).

**2-swap mostly-axial subset**: 10 moves HTR reduction + 9 moves finish = 19 moves. Total: 11 + 19 = **30 moves**. Still not better than my 29-move best.

Let me think... Both axes gave me ~30+ moves. Maybe I need a different approach. Let me check if there's a shorter EO option I missed. Let me reset and try **RL axis**:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

**RL also has 4-move EO.** Let me probe DR:

I probe what DR would look like if I applied this EO (without committing).

**RL: 4-move EO + 8-move DR = 12 moves to DR.** Same as the others. All three axes are performing similarly. Given that my best prior solve was 29 moves, and I'm consistently getting ~30 moves, perhaps I need to execute one line cleanly and look for optimizations in the finish phase, or try replace_and_shorten if I go over 27 moves.

Let me commit to **FB-normal** since it gave me 11 moves to DR (slightly better than the 12 for the others). Let me apply the full sequence:

I turn `B2 L2 U2 R'`.

I turn `R2 B' D L2`.

I turn `U B2 F' U'`.

**DR in 11 moves on FB axis.** Now apply HTR reduction:

For the corner reduction, I see `F' R2 F L2` (chunk of a 10-move phase) — apply and re-check.

HTR reduction is 10 moves (partial, showing 4). Apply them:

I turn `F' R2 F L2`.

Let me check if I accidentally landed on a solved or simpler state:

Quick check: DR-locked on FB, not yet HTR.

Still not HTR. Continue with the next chunk of HTR reduction:

For the corner reduction, I see `F' U2 R2 F'` (chunk of a 6-move phase) — apply and re-check.

I turn `F' U2 R2 F'`.

Quick check: DR-locked on FB, not yet HTR.

Continue:

For the corner reduction: `L2 B`.

Last chunk:

I turn `L2 B`.

Quick check: in HTR.

**HTR achieved!** (is_htr_ud: true, all axes in DR). 21 moves so far. Now apply the finish:

For the half-turn finish, I see `U2 L2 U2 R2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 L2 U2 R2`.

Quick check: in HTR.

Continue finish:

For the half-turn finish, I see `B2 D2 U2 L2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 D2 U2 L2`.

Quick check: in HTR.

Last move:

For the half-turn finish: `U2`.

I turn `U2`.

A quick glance — the cube is solved.

**SOLVED in 30 moves!** Now let me cancel and verify:

I assemble the canonical normal-frame solution: **30 moves**, verified.

I have a **30-move solution**, which ties my attempt #3. This is not better than my best of 29 moves. However, since I have 30 moves and the gates allow replace_and_shorten (≥27 moves), let me try to optimize. Let me check budget first:

Budget check: 3396.0s sim, None tool calls remaining.

I have **3396 seconds remaining** (plenty of budget). Let me try replace_and_shorten on a large tail section. I'll target moves 5-30 (the DR+HTR+finish portion):

r&s: too few tool calls remaining (27) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

The tool refuses because I have only 27 tool calls remaining (need ≥30). I should submit my current 30-move solution. It's not an improvement over 29, but it's a complete, verified solve.

Actually, wait — let me look at the move sequence to see if there are obvious cancellations I can manually spot:

```
B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2
```

I don't see obvious long cancellations. Let me submit this solution:

verify_solved: ✓ — 30 moves.

**VERIFIED SOLVED in 30 moves.**

## FINAL_SOLUTION

**FINAL_SOLUTION:** ["B2", "L2", "U2", "R", "B'", "D", "L2", "U", "B2", "F'", "U'", "F'", "R2", "F", "L2", "F'", "U2", "R2", "F'", "L2", "B", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "L2", "U2"]

**Move count: 30 moves**

### Solution breakdown:
- **EO (FB-axis, normal side):** B2 L2 U2 R (4 moves) — Clean 2+2 symmetric pattern on FB axis
- **DR (FB-axis):** B' D L2 U B2 F' U' (7 moves) → 11 total to DR
- **HTR reduction:** F' R2 F L2 F' U2 R2 F' L2 B (10 moves) → 21 total to HTR
- **Finish:** U2 L2 U2 R2 B2 D2 U2 L2 U2 (9 moves) → 30 total

This is a clean, complete solution on FB-normal axis. The 2-swap mostly-axial HTR subset required 19 moves post-DR, which is reasonable for this subset family. Not an improvement over the prior best of 29 moves, but a solid, verified solve within budget.

*Thinking (56):*

> The user is right - I said "FINAL_SOLUTION:" but didn't format it correctly. Let me output it in the proper format they're asking for.

FINAL_SOLUTION: ["B2", "L2", "U2", "R", "B'", "D", "L2", "U", "B2", "F'", "U'", "F'", "R2", "F", "L2", "F'", "U2", "R2", "F'", "L2", "B", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "L2", "U2"]

**Verified solution (30 moves):** `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`
