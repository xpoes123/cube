# Solve — fm_PSSSideDayGdansk2026_s2__attempt1_20260517_144958

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 33 moves
**Solution**: `L' B2 U2 R' D' B F U2 B R2 U' R2 F R2 F U2 F2 U2 L2 F D2 F R2 D2 L2 D2 B2 R2 B2 U2 F2 R2 U2`

---

*Thinking (1):*

> The user wants me to solve the FMC scramble. Let me start by inspecting the state to see what I'm working with. The scramble is:
> 
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I should start with inspect_state to see the bad edges per axis and other relevant information.

I'll solve this FMC scramble step by step. Let me start by inspecting the cube state to understand what I'm working with.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Good! I can see:
- **UD axis**: 6 bad edges (UF, UL, DR, FR, FL, BR), DR-7C3E, JZP not eligible, but **3 pairs on inverse** (strong NISS signal!)
- **FB axis**: 4 bad edges (DR, DL, FR, BL), DR-7C2E
- **RL axis**: 4 bad edges (UL, DR, DF, FR), DR-6C2E

The UD axis has **3 pairs on inverse**, which is a strong signal to check the inverse frame. Let me scout EO on both normal and inverse for the most promising axes.

**EO scouting plan**: 
1. FB and RL both have 4 bad edges on normal → likely 1-3 move EO
2. UD has 6 bad edges BUT 3 pairs on inverse → check inverse-UD

Let me start by checking EO patterns on normal for FB and RL:

On FB axis I recognize the EO pattern — `B2 L2 U2 R'` fixes it.

On RL axis I recognize the EO pattern — `R2 B F2 U'` fixes it.

Both FB and RL give 4-move EOs on normal. Now let me check the inverse frame since UD has 3 pairs preserved on inverse (strong signal). I'll flip to inverse and check UD:

NISS flip — switching to the inverse scramble.

On UD axis I recognize the EO pattern — `B R2 U F'` fixes it.

Interesting! Inverse-UD also gives a 4-move EO (B R2 U F'). So I have:
- Normal-FB: 4 moves
- Normal-RL: 4 moves  
- Inverse-UD: 4 moves

Since all three are the same length, I need to probe DR options to make the joint decision. Let me check DR prospects after each EO:

I probe what DR would look like if I applied this EO (without committing).

Inverse-UD gives 8-move total DR (4 EO + 4 more to DR). That's reasonable. Let me flip back to normal and check the other axes:

NISS flip — switching back to the normal scramble.

I probe what DR would look like if I applied this EO (without committing).

I probe what DR would look like if I applied this EO (without committing).

Excellent! All three options give the same total DR length of 8 moves (4 EO + 4 to DR). Since they're tied on length, I need to check the DR trigger families and substates to make the decision. Let me commit one EO and check dr_trigger_options. I'll start with inverse-UD since it had 3 pairs preserved:

NISS flip — switching to the inverse scramble.

I turn `B R2 U F'`.

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

Hmm, no DR triggers found within 5 moves on inverse-UD after that EO. This is surprising given the probe said 8 total. Let me try a different approach - let me reset and try normal-FB instead:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `B2 L2 U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Also no triggers on FB. Let me try RL:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 B F2 U'`.

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-7C8E (F' L B): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E

Good! On RL-axis I found a **DR-7C8E** trigger in 8 total moves (5 setup + 3 trigger). The substate is 7C8E which is not great (expected ~15+ moves post-DR). Let me also check max_setup=6 to see if there's anything better, and also try using dr_recognize which might find longer sequences:

I check whether the DR is recognizable from this state via the library.

Interesting! dr_recognize found a different 8-move path. Let me apply those setup moves and continue:

I turn `L' B' L' R2`.

I check whether the DR is recognizable from this state via the library.

Wait, this says 4 MORE moves to DR from here. That would be 8 + 4 = 12 total, which contradicts the "full_optimal_length": 8. Let me check the state to see what's happening:

Quick check: EO solved on RL, working toward DR.

I'm at RL-EO with 8 moves. The dr_recognize found 4 more moves. Let me apply them:

I turn `U2 B R2 F'`.

Quick check: DR-locked on RL, not yet HTR.

Great! I reached RL-DR in 12 moves. That's longer than ideal (the DR-length rule says elite solves get DR ≤6 moves with 85% probability). Let me check if there's a better path. Let me try a completely different approach - let me look for shorter EO options or different axes. Let me reset and check if there's a 2-bad-edge EO somewhere:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I look over the cube.
Bad-edge counts: UD=6, FB=4, RL=4.

Let me try a different strategy. Looking at the bad edges more carefully:
- RL has only 4 bad edges (UL, DR, DF, FR), with U-flipping affecting only UL, and D-flipping affecting DR and DF
- This could be a 2-3 move EO if I can set it up right

Let me try policy intuition to see what moves look good from the start:

I check my gut for plausible next moves.

The policy strongly suggests L as the first move. Let me try exploring from L and see if I can find a shorter EO+DR:

I try `L` on top to see the after-state (without committing).

Interesting! After L:
- RL-axis still has 4 bad edges but now they're (DR, DF, FR, FL) with NO bad edges affected by U-flips
- UD-axis improved to DR-7C1E and FB improved to DR-6C1E

Let me continue and apply L, then check EO options:

I turn `L`.

On RL axis I recognize the EO pattern — `R' B' L D'` fixes it.

Still 4 moves for RL-EO. Let me also check FB which is now at DR-6C1E:

On FB axis I recognize the EO pattern — `L2 B2 U2 R'` fixes it.

Also 4 moves. Let me now probe DR for both to see which is better:

I probe what DR would look like if I applied this EO (without committing).

Excellent! FB-axis after L gives 7-move total DR (4 EO + 3 more). Combined with the L premove, that's **8 moves to DR total** (1 + 4 + 3). Let me commit this path:

I turn `L2 B2 U2 R'`.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

Note it auto-cancelled L + L2 → L'. So my current state is L' B2 U2 R' with FB-EO solved. No triggers found within 5 moves. Let me use dr_recognize to find the full path:

I check whether the DR is recognizable from this state via the library.

I turn `D' B F U2`.

I check whether the DR is recognizable from this state via the library.

Great! 3 more moves to DR. Let me apply them:

I turn `B R2 U'`.

Quick check: DR-locked on FB, not yet HTR.

Perfect! I've reached FB-DR in 11 moves: **L' B2 U2 R' D' B F U2 B R2 U'**

This is better than the 12-move RL-DR I found earlier. Now let me proceed to HTR. First, let me classify the HTR subset:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 11 moves, finish is 11 moves (first exposure — learning).

The HTR subset is a "2-swap long-cycle" requiring 11 moves for HTR reduction and 11 moves for finish = **22 moves post-DR**. Combined with my 11-move DR, that would be **33 moves total**. That's acceptable but not great. Let me apply the HTR reduction:

For the corner reduction, I see `R2 F R2 F` (chunk of a 11-move phase) — apply and re-check.

I turn `R2 F R2 F`.

Quick check: DR-locked on FB, not yet HTR.

Still not at HTR. Let me continue:

For the corner reduction, I see `U2 F2 U2 L2` (chunk of a 7-move phase) — apply and re-check.

I turn `U2 F2 U2 L2`.

Quick check: DR-locked on FB, not yet HTR.

For the corner reduction: `F D2 F`.

I turn `F D2 F`.

Quick check: in HTR.

Excellent! I'm now at HTR-UD (all axes DR, HTR-UD true) in 22 moves. Now let me apply the finish:

For the half-turn finish, I see `R2 D2 L2 D2` (chunk of a 11-move phase) — apply and re-check.

I turn `R2 D2 L2 D2`.

Quick check: in HTR.

Still not solved. Let me continue:

For the half-turn finish, I see `B2 R2 B2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `B2 R2 B2 U2`.

Quick check: in HTR.

For the half-turn finish: `F2 R2 U2`.

I turn `F2 R2 U2`.

A quick glance — the cube is solved.

Perfect! The cube is SOLVED in **33 moves**:
**L' B2 U2 R' D' B F U2 B R2 U' R2 F R2 F U2 F2 U2 L2 F D2 F R2 D2 L2 D2 B2 R2 B2 U2 F2 R2 U2**

Let me now verify this solution and apply cancellation:

I assemble the canonical normal-frame solution: **33 moves**, verified.

Great! The solution is verified and is 33 moves. Since this is ≥27 moves, I should check if replace_and_shorten can improve it. Let me check my budget first:

Budget check: 2350.02s sim, None tool calls remaining.

I have plenty of budget remaining (2350s simulated, 1335s wall time). Since my solution is 33 moves (≥27) and I have budget, I should try replace_and_shorten on a large span. Let me target the HTR finish portion which was quite long (22 moves from move 11 to move 33):

r&s: too few tool calls remaining (19) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

I don't have enough tool calls remaining for replace_and_shorten. Let me submit my current 33-move solution.

## FINAL SOLUTION

I found a **33-move solution** using the FB-axis:

**Solution breakdown:**
- **Premove**: L' (1 move) - improved DR prospects  
- **EO (FB-axis)**: B2 U2 R' (3 moves, with L' → L2 cancellation from premove)
- **DR (FB-axis)**: D' B F U2 B R2 U' (7 moves)
- **HTR reduction**: R2 F R2 F U2 F2 U2 L2 F D2 F (11 moves)
- **HTR finish**: R2 D2 L2 D2 B2 R2 B2 U2 F2 R2 U2 (11 moves)

**Total**: 11 moves to DR + 22 moves to finish = **33 moves**

FINAL_SOLUTION: ["L'", "B2", "U2", "R'", "D'", "B", "F", "U2", "B", "R2", "U'", "R2", "F", "R2", "F", "U2", "F2", "U2", "L2", "F", "D2", "F", "R2", "D2", "L2", "D2", "B2", "R2", "B2", "U2", "F2", "R2", "U2"]

**Verified solution (33 moves):** `L' B2 U2 R' D' B F U2 B R2 U' R2 F R2 F U2 F2 U2 L2 F D2 F R2 D2 L2 D2 B2 R2 B2 U2 F2 R2 U2`
