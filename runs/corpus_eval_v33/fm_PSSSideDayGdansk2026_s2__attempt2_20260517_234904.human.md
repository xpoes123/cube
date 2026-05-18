# Solve — fm_PSSSideDayGdansk2026_s2__attempt2_20260517_234904

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `F2 U2 B2 U2 L2 F2 R2 U2 D' B2 U' R2 U R2 U' R2 U R2 U' R' B2 L U L R2 D' U' F U' R2 B'`

---

*Thinking (1):*

> Alright, I have a scramble to solve with the FMC approach. The prior attempt got 34 moves. I need to commit hard to one line and drive it to completion.
> 
> Let me start by inspecting the state to see the bad edge counts on all axes and DR closeness information.
> 
> The instruction is clear: COMMIT HARD, pick a line, don't over-ideate between branches. If the prior attempt looked promising, maybe use the same axis. 34 moves is decent but can be improved.
> 
> Let me start with inspect_state to see what we're working with.

I'll solve this scramble systematically, committing to one strong line. Starting with inspection.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

**Initial state read:**
- **Bad edges**: UD=6, FB=4, RL=4
- **DR closeness**: UD is DR-7C3E (bad), FB is DR-7C2E, RL is DR-6C2E (better corner orientation)
- **Key signal**: UD has **3 pairs on inverse** — strong NISS switch indicator
- FB=4 and RL=4 bad edges are tied for shortest EO

**Strategy decision:** FB and RL both have 4 bad edges. Let me scout EO on both axes on the normal side first, then check inverse. The UD axis has 3 pairs_on_inverse which suggests the inverse frame might be strong there too.

Let me start by checking FB-axis EO (4 bad edges on DR, DL, FR, BL):

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

FB-axis EO = **4 moves** (B2 L2 U2 R'). Now check RL-axis EO (4 bad edges on UL, DR, DF, FR):

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

RL-axis EO = **4 moves** (R2 B F2 U'). Both FB and RL have 4-move EOs on normal side. Now let me check **inverse** — the UD axis showed 3 pairs_on_inverse which is a strong signal. Let me flip to inverse and check all three axes there:

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check EO on UD (which had 3 pairs_on_inverse), FB, and RL:

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

On FB axis I recognize the EO pattern — `U2 R'` fixes it.

On RL axis I recognize the EO pattern — the first chunk is `D U' B' D'` (full fix is 4 moves).

**Excellent! Inverse-FB EO = 2 moves** (U2 R'). This is the clear winner:
- Normal FB: 4 moves
- Normal RL: 4 moves
- Inverse UD: 4 moves
- **Inverse FB: 2 moves** ✓
- Inverse RL: 5 moves

**Committing to inverse-FB axis with 2-move EO (U2 R').** Now I need to apply the EO and check DR options on FB axis. Applying EO:

I turn `U2 R'`.

Good, EO applied. Now checking DR trigger options on FB axis from this EO-solved state:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**No DR triggers found within 5 moves on FB axis.** This is concerning but not fatal. Let me try `dr_recognize` which has the 3,657-pattern memory plus brain fallback:

I check whether the DR is recognizable from this state via the library.

The brain suggests R2 (65% probability). This is a half-turn on an axis-move (FB-axis), which preserves EO. Let me try it:

I turn `R2`.

Good! Auto-cancelled R' + R2 = R. Now re-checking DR options:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Still no DR triggers within 5 moves. The FB-axis inverse line isn't working well for DR. Let me reconsider. The prior attempt got 34 moves — let me **switch strategy** and check the normal side RL-axis which had 4-move EO and RL had the best corner orientation (DR-6C2E vs 7C for others).

Let me flip back to normal and try RL:

NISS flip — switching back to the normal scramble.

Back on normal. Let me reset and try RL-axis from scratch:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Now applying RL-axis EO (R2 B F2 U') on normal side:

I turn `R2 B F2 U'`.

Good. Now checking DR trigger options on RL axis:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Found one option: **DR-7C8E** in 8 moves total (5 setup + 3 trigger). This is a poor DR substate (7C8E is bad). Total EO+DR = 4+8 = **12 moves to DR**. This exceeds the sub-11 target and the substate is bad. Let me check if there's a better option by using dr_recognize:

I check whether the DR is recognizable from this state via the library.

Brain suggests F2. Let me try applying F2 and re-checking:

I turn `F2`.

Now re-checking DR options:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Still DR-7C8E in 8 moves. This RL line isn't promising. Let me try the **normal FB-axis** (4-move EO: B2 L2 U2 R'). Let me reset and try that:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Applying FB-axis EO (B2 L2 U2 R'):

I turn `B2 L2 U2 R'`.

Checking DR options on FB:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

No DR triggers on normal FB either. This scramble is being difficult across all axes. Let me try **UD-axis inverse** which had 3 pairs_on_inverse (strong NISS signal) and 4-move EO. Let me reset, flip to inverse, and try UD:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

On inverse. Applying UD-axis EO (B R2 U F'):

I turn `B R2 U F'`.

Checking DR options on UD axis:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Still no DR triggers! This scramble is very difficult for finding clean DR patterns. Let me try using dr_recognize with the brain to guide me move-by-move toward DR:

I check whether the DR is recognizable from this state via the library.

Brain suggests U (42%). Let me apply U and re-check:

I turn `U`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Still nothing. Let me continue with brain guidance:

I check whether the DR is recognizable from this state via the library.

Very strong signal for D (93%). Applying:

I turn `D`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on UD:
  • DR-3C2E (R U R'): 5-mv setup + 3-mv trigger (8 total) pre=DR-3C1E
  • DR-2C4E (R F2 R): 5-mv setup + 3-mv trigger (8 total) [JZP] pre=DR-4C1E
  • DR-4C4E (R): 5-mv setup + 1-mv trigger (6 total) [JZP] pre=DR-4C2E

**Excellent! Found DR triggers!** Multiple options:
1. **DR-4C4E (R)** - 6 moves to DR (5 setup + 1), JZP-eligible ✓
2. **DR-4C4E (R')** - 6 moves to DR (5 setup + 1), JZP-eligible ✓
3. DR-3C2E (R U R') - 8 moves to DR, not JZP
4. DR-2C4E (R F2 R) - 8 moves to DR, JZP-eligible

The **DR-4C4E with JZP** in 6 moves is the best choice! Setup: R2 L' U' L' B2, then trigger R.

Total so far: 4 (EO) + 2 (brain moves) + 6 (DR) = **12 moves to DR** on inverse UD-axis.

Applying the DR setup + trigger:

I turn `R2 L' U' L' B2 R`.

Perfect! Now at DR on UD-axis inverse with JZP. Let me check the HTR state:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 8 moves (first exposure — learning).

HTR subset is **2-swap long-cycle** with:
- HTR reduction: 11 moves  
- Finish: 8 moves
- Total: 19 moves from DR to solved

So the full solution would be: 12 (to DR) + 19 (DR to solved) = **31 moves** total. This is better than the 34-move prior attempt!

Let me apply the HTR reduction phase:

For the corner reduction, I see `U R2 U' R2` (chunk of a 11-move phase) — apply and re-check.

Partial reduction (4 of 11 moves). Applying:

I turn `U R2 U' R2`.

Let me do a quick check to see if I've solved early or hit a 3-cycle:

Quick check: DR-locked on UD, not yet HTR.

Not solved yet, HTR not reached. Continuing HTR reduction:

For the corner reduction, I see `U R2 U' R2` (chunk of a 7-move phase) — apply and re-check.

Another 4 moves:

I turn `U R2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not HTR. Continuing:

For the corner reduction: `U B2 D`.

Final 3 moves of reduction:

I turn `U B2 D`.

Quick check: in HTR.

**HTR reached!** Now applying the finish phase:

For the half-turn finish, I see `U2 R2 F2 L2` (chunk of a 8-move phase) — apply and re-check.

I turn `U2 R2 F2 L2`.

Quick check: in HTR.

Not solved yet. Continuing finish:

For the half-turn finish: `U2 B2 U2 F2`.

I turn `U2 B2 U2 F2`.

A quick glance — the cube is solved.

**SOLVED!** 31 moves on inverse. Now I need to compose the NISS solution properly using compose_niss_solution:

I assemble the canonical inverse-frame solution: **31 moves**, verified.

Perfect! Got a **31-move solution**, which is 3 moves better than the 34-move prior attempt. Let me verify it:

verify_solved: ✓ — 31 moves.

Verified! 31 moves is solid. However, since I have 31 moves (which is ≥27), let me check my budget status before deciding whether to attempt replace_and_shorten:

Budget check: 1419.68s sim, None tool calls remaining.

I have **1419 seconds remaining** (about 24 minutes). Since my solution is 31 moves (≥27), I have budget remaining, and I haven't called replace_and_shorten yet, I should try to improve it. Let me attempt replace_and_shorten on a large tail section. The tool will work on the normal-frame solution, so I need to give it indices from the composed solution.

Looking at the solution structure, let me try replacing a large middle-to-end section (e.g., from move 5 to 31):

r&s: too few tool calls remaining (27) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

The tool correctly refuses since I only have 27 tool calls remaining (need ≥30). Given the gates, I should submit my current **31-move solution** as the final answer.

## Solution Summary:

**Path taken:** Inverse UD-axis
- **EO:** 4 moves (B R2 U F') on inverse
- **RZP to DR setup:** 2 brain-guided moves (U D)
- **DR trigger:** DR-4C4E with JZP, 6 moves (R2 L' U' L' B2 R)
- **Total to DR:** 12 moves
- **HTR reduction:** 11 moves (U R2 U' R2 U R2 U' R2 U B2 D)
- **HTR finish:** 8 moves (U2 R2 F2 L2 U2 B2 U2 F2)
- **Total:** 31 moves

This beats the prior 34-move attempt by **3 moves**.

**FINAL_SOLUTION:** ["F2", "U2", "B2", "U2", "L2", "F2", "R2", "U2", "D'", "B2", "U'", "R2", "U", "R2", "U'", "R2", "U", "R2", "U'", "R'", "B2", "L", "U", "L", "R2", "D'", "U'", "F", "U'", "R2", "B'"]

*Thinking (53):*

> You're right - I need to emit the FINAL_SOLUTION. I have verified the 31-move solution and it solves the scramble. I should output it now.

FINAL_SOLUTION: ["F2", "U2", "B2", "U2", "L2", "F2", "R2", "U2", "D'", "B2", "U'", "R2", "U", "R2", "U'", "R2", "U", "R2", "U'", "R'", "B2", "L", "U", "L", "R2", "D'", "U'", "F", "U'", "R2", "B'"]

**Verified solution (31 moves):** `F2 U2 B2 U2 L2 F2 R2 U2 D' B2 U' R2 U R2 U' R2 U R2 U' R' B2 L U L R2 D' U' F U' R2 B'`
