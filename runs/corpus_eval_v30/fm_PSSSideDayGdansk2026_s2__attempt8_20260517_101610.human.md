# Solve — fm_PSSSideDayGdansk2026_s2__attempt8_20260517_101610

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 32 moves
**Solution**: `U R2 U R2 U' R2 L2 F2 U B2 D R2 U2 R2 D2 U2 F2 R2 U2 R U2 R' L2 U L D2 U R2 F U' R2 B'`

---

*Thinking (1):*

> Looking at the prior attempts, they're all in the 29-30 move range. The best is 29 moves. I need to commit hard to ONE path and drive it to completion efficiently.
> 
> Let me start by inspecting the state to see what axes look promising, then pick one and push through to completion without thrashing between options.
> 
> The key is:
> 1. Quick EO axis scouting (both normal and inverse)
> 2. Pick ONE axis/side based on joint EO+DR cost
> 3. Execute DR cleanly
> 4. HTR finish with inter-phase quick_checks
> 5. Ship it
> 
> Let's begin.

I'll solve this scramble efficiently by committing to ONE clean path. Starting with state inspection to scout EO axes.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**STATE READING:** FB and RL both have 4 bad edges (best EO candidates), UD has 6. The DR-closeness shows UD has **3 pairs on inverse** — a strong NISS signal. Let me scout EO on multiple candidates.

**EO SCOUTING PLAN:** 
1. FB-axis normal (4 bad edges)
2. RL-axis normal (4 bad edges) 
3. UD-axis inverse (leveraging those 3 pairs)

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL give 4-move EOs. Now let me check inverse-UD (leveraging those 3 pairs):

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

**INVERSE-UD EO: 4 moves** (B R2 U F'). All three axes need 4-move EOs. Now I need to probe DR cost for each to pick the joint-shortest path.

**DR PROBING:** I'll probe DR after each EO candidate:

I probe what DR would look like if I applied this EO (without committing).

Inverse-UD: EO=4, DR=8, **total 12 moves to DR**. Let me flip back to normal and probe the other two:

NISS flip — switching back to the normal scramble.

I probe what DR would look like if I applied this EO (without committing).

I probe what DR would look like if I applied this EO (without committing).

**COMPARISON:**
- Inverse-UD: EO=4 + DR=8 = **12 moves to DR** (3 pairs preserved)
- Normal-FB: EO=4 + DR=8 = **12 moves to DR**
- Normal-RL: EO=4 + DR=8 = **12 moves to DR**

All three are identical at 12 moves to DR. The inverse-UD has the **3 pairs on inverse** signal. I'll **commit to inverse-UD** and drive it through.

NISS flip — switching to the inverse scramble.

I turn `B R2 U F'`.

**COMMITTED:** Inverse-UD EO complete (B R2 U F'). Now finding DR triggers on UD axis:

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 6-mv setup + 3-mv trigger (9 total) [JZP]
  • DR-3C2E (R U' R'): 6-mv setup + 3-mv trigger (9 total)

**DR OPTIONS:**
1. **DR-4C2E (R U2 R')**: 6-move setup + 3-move trigger = **9 to DR**, **JZP-eligible** 
2. **DR-3C2E (R U' R')**: 6-move setup + 3-move trigger = **9 to DR**, NOT JZP

Using the priors table:
- DR-4C2E with JZP: 9mv to DR + 5-7mv post-DR = **14-16 total**
- DR-3C2E non-JZP: 9mv to DR + 6-8mv post-DR = **15-17 total**

**PICKING DR-4C2E** (the JZP-eligible option). Applying setup then trigger:

I turn `R2 U' D2 L' U' L2`.

I turn `R U2 R'`.

Quick check: DR-locked on UD, not yet HTR.

**DR REACHED** on inverse-UD (13 moves). EO=4 + DR=9 = 13 total. Now classifying HTR and finishing:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 11 moves (recall).

**HTR SUBSET:** 2-swap long-cycle with 5-2-1 cycle structure. HTR reduction = 11 moves, finish = 11 moves, **total 22 from DR**. Combined: 13 (to DR) + 22 = **35 moves**. 

That's worse than prior best (29). But let me execute it cleanly and use inter-phase quick_checks to catch any early solve or 3c residuals:

For the corner reduction, I see `F2 U L2 U` (chunk of a 11-move phase) — apply and re-check.

I turn `F2 U L2 U`.

Quick check: DR-locked on UD, not yet HTR.

Not HTR yet (still in HTR-reduction). Continuing:

For the corner reduction, I see `R2 U' L2 F2` (chunk of a 7-move phase) — apply and re-check.

I turn `R2 U' L2 F2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `U' L2 U`.

I turn `U' L2 U`.

Quick check: in HTR.

**HTR REACHED** (24 moves). Now applying the finish phase:

For the half-turn finish, I see `U2 B2 L2 R2` (chunk of a 11-move phase) — apply and re-check.

I turn `U2 B2 L2 R2`.

Quick check: in HTR.

Still in HTR, continuing finish:

For the half-turn finish, I see `U2 L2 F2 R2` (chunk of a 7-move phase) — apply and re-check.

I turn `U2 L2 F2 R2`.

Quick check: in HTR.

For the half-turn finish: `U2 F2 R2`.

I turn `U2 F2 R2`.

A quick glance — the cube is solved.

**SOLVED!** 34 moves on inverse. Now composing the NISS solution (which will invert the inverse-side moves back to normal):

I assemble the canonical inverse-frame solution: **34 moves**, verified.

**COMPLETE SOLUTION: 34 moves.** That's worse than the prior best (29). Let me check if replace_and_shorten can improve it (the gates: ≥27 moves ✓, ≥30 tool calls remaining — let me check budget):

Budget check: 3511.0s sim, None tool calls remaining.

I have plenty of budget (3511s remaining) and tool calls. The solution is 34 moves (≥27 ✓), so replace_and_shorten is eligible. Let me try it on the HTR tail span (from move 13 onward, which is after DR):

replace_and_shorten on the tail span: substitute is 2 moves shorter. Accepted.

**REPLACE_AND_SHORTEN SUCCESS:** saved 2 moves! New solution is **32 moves**. Let me compose this updated solution:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

I turn `B R2 U F' R2 U' D2 L' U' L2 R U2 R' U2 R2 F2 U2 D2 R2 U2 R2 D' B2 U' F2 L2 R2 U R2 U' R2 U'`.

I assemble the canonical inverse-frame solution: **32 moves**, verified.

**FINAL SOLUTION: 32 moves** after replace_and_shorten optimization. Let me verify this solves the scramble:

verify_solved: ✓ — 32 moves.

**VERIFIED ✓** 

## SOLUTION SUMMARY

**Path taken:** Inverse-UD axis
- **EO (inverse):** B R2 U F' (4 moves)
- **DR trigger:** DR-4C2E with JZP (6-move setup + 3-move trigger = 9 to DR)
- **Total to DR:** 13 moves
- **HTR subset:** 2-swap long-cycle (11-move reduction + 11-move finish = 22 moves)
- **Initial solution:** 34 moves
- **After replace_and_shorten:** **32 moves** (saved 2 moves on the HTR tail)

**FINAL_SOLUTION:** ["U", "R2", "U", "R2", "U'", "R2", "L2", "F2", "U", "B2", "D", "R2", "U2", "R2", "D2", "U2", "F2", "R2", "U2", "R", "U2", "R'", "L2", "U", "L", "D2", "U", "R2", "F", "U'", "R2", "B'"]

This is 3 moves worse than the best prior attempt (29 moves), but it's a clean, complete solve executed efficiently. The inverse-UD path with 3 pairs preserved on inverse led to a JZP-eligible DR, but the resulting HTR subset (2-swap long-cycle) had a long finish. Replace_and_shorten recovered 2 moves from the tail.

*Thinking (28):*

> The user is right - I verified the solution but didn't emit the FINAL_SOLUTION. I should output it now.

FINAL_SOLUTION: ["U", "R2", "U", "R2", "U'", "R2", "L2", "F2", "U", "B2", "D", "R2", "U2", "R2", "D2", "U2", "F2", "R2", "U2", "R", "U2", "R'", "L2", "U", "L", "D2", "U", "R2", "F", "U'", "R2", "B'"]

**Verified solution (32 moves):** `U R2 U R2 U' R2 L2 F2 U B2 D R2 U2 R2 D2 U2 F2 R2 U2 R U2 R' L2 U L D2 U R2 F U' R2 B'`
