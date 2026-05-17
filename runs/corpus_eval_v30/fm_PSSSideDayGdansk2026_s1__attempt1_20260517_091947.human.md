# Solve — fm_PSSSideDayGdansk2026_s1__attempt1_20260517_091947

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 25 moves
**Solution**: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`

---

*Thinking (1):*

> Alright, I'm starting a new FMC solve. The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I need to follow the systematic FMC pipeline:
> 1. Inspect state to see bad edges per axis
> 2. Scout EO on multiple axes (both normal and inverse)
> 3. Check DR feasibility for each EO candidate
> 4. Pick the joint-shortest EO+DR path
> 5. Execute DR
> 6. HTR classify and finish
> 7. Cancel and verify
> 
> Let me start by inspecting the main slot to understand the initial state.

I'll solve this FMC scramble systematically, starting with inspection and multi-axis EO scouting. The goal is a verified solution within the 1-hour (3600s) budget.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**Initial state scan:**
- Bad edges: UD=8, FB=6, RL=6
- FB and RL look most promising (fewer bad edges)
- UD has 8 bad edges but shows `top_pairs_on_inverse: 2` — this is a signal that NISS to inverse might help
- FB is DR-5C2E (5 misoriented corners, 2 misplaced edges) from the scramble state
- JZP not eligible on any axis from scramble

**EO Strategy:** 8 bad edges on UD typically needs 3-5 moves (classic `<setup> F <setup'> B` pattern). FB and RL with 6 bad edges are 2-4 move candidates. But the `top_pairs_on_inverse: 2` on UD is a strong signal — I should scout the inverse side first.

Let me scout EO on multiple axes, starting with the inverse (since pairs-tracing suggests it).

NISS flip — switching to the inverse scramble.

Now on inverse. Let me inspect the inverse state and scout EO on all axes.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.
I'm currently working on the inverse scramble.

Interesting — the inverse has the same bad-edge distribution (UD=8, FB=6, RL=6). Let me scout EO on FB and RL axes on this inverse side.

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

Both FB and RL on inverse show 5-move EOs. Let me check the normal side now to compare. Flipping back.

NISS flip — switching back to the normal scramble.

Now back on normal side. Let me scout EO on FB and RL here.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

On UD axis I recognize the EO pattern — `R2 D' B' F'` fixes it.

**EO scouting summary:**
- **UD-normal**: 4 moves (R2 D' B' F') — FULL solution, no partial
- **FB-normal**: 5 moves
- **RL-normal**: 5 moves
- **FB-inverse**: 5 moves
- **RL-inverse**: 5 moves

UD-normal has the shortest EO at 4 moves complete. Now I need to probe DR for each candidate to make the joint decision. Let me probe DR after the UD-normal EO.

I probe what DR would look like if I applied this EO (without committing).

UD-normal: 4-move EO + 8-move DR = 12 moves to DR. That's reasonable (elite target is ≤11, but 12 is acceptable). Let me also probe FB-normal quickly to compare.

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

Excellent! After those 4 moves, FB-EO is just 1 move (R'). So FB-normal would be 5 total moves to EO. Let me check DR from here.

I turn `R'`.

I look over the cube.
Bad-edge counts: UD=6, FB=0, RL=6.
Last applied: `R2 B' L' U2 R'`.

Perfect! FB-EO is now solved. The state shows:
- FB axis: DR-4C3E (4 misoriented corners, 3 misplaced edges)
- This is close to DR-4C4E (R trigger) or DR-4C2E (R U2 R')

Let me use dr_trigger_options to see what's available on FB.

I survey the named DR triggers on FB:
  • DR-3C2E (U F' U'): 6-mv setup + 3-mv trigger (9 total)

FB shows a DR-3C2E option in 6+3=9 moves total. That's 5 (EO) + 9 (DR) = 14 moves to DR. The UD path was 4 + 8 = 12 moves. But DR-3C2E typically finishes in 6-8 moves post-DR, while the UD path's DR-substate wasn't specified yet.

Let me reset and check the UD path properly.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 D' B' F'`.

Now let me check dr_trigger_options on UD after this 4-move EO.

I survey the named DR triggers on UD:
  • DR-4C2E (R U2 R'): 5-mv setup + 3-mv trigger (8 total) [JZP]
  • DR-7C8E (R' U L): 5-mv setup + 3-mv trigger (8 total)
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

**Excellent DR options on UD after the 4-move EO:**

1. **DR-4C2E (R U2 R')** — JZP-eligible, 5+3=8 moves to DR → Total 4(EO)+8(DR)=12 to DR
   - DR-4C2E typically finishes in 5-7 moves with JZP
   - Estimated total: ~17-19 moves

2. **DR-7C8E (R' U L)** — 8 moves to DR, 4 pairs on inverse (strong NISS signal)
   - DR-7C8E is a harder substate, ~10-14 moves post-DR
   - Not worth it

The **DR-4C2E with JZP** at total 12 to DR looks very strong. JZP halves the post-DR cost, so ~5-7 moves post-DR = ~17-19 total.

**Decision:** Taking UD-normal with the 4-move EO (R2 D' B' F'), then the JZP-eligible DR-4C2E path.

I turn `U' R' L2 U F2`.

Setup moves applied (5 moves). Now applying the DR-4C2E trigger: R U2 R'.

I turn `R U2 R'`.

Quick check: DR-locked on UD, not yet HTR.

Perfect! DR on UD is achieved in 12 moves. Now I'm in JZP-eligible DR-4C2E substate. Let me classify the HTR subset and proceed with the finish.

I recognize the HTR subset: **0-swap long-cycle**. Reduction is 10 moves, finish is 9 moves (first exposure — learning).

HTR subset is **0-swap long-cycle** with cycle structure [3,2,2,1]. The total HTR+finish is 10+9=19 moves. That would give us 12 (to DR) + 19 (HTR+finish) = 31 moves total. That's longer than ideal but acceptable as a first solve.

Let me apply the HTR reduction phase.

For the corner reduction, I see `U F2 U' R2` (chunk of a 10-move phase) — apply and re-check.

I turn `U F2 U' R2`.

Quick check: DR-locked on UD, not yet HTR.

Still not at HTR yet. Continuing HTR reduction.

For the corner reduction, I see `U L2 U2 R2` (chunk of a 6-move phase) — apply and re-check.

I turn `U L2 U2 R2`.

Quick check: DR-locked on UD, not yet HTR.

For the corner reduction: `F2 U`.

I turn `F2 U`.

Quick check: in HTR.

Great! Now at HTR after 22 moves. Let me check for any residual (3-cycle opportunity) before applying the final finish phase.

Residual class: mixed.

Mixed residual with 4 corners and 9 edges unsolved. Not a pure 3-cycle. Let me apply the finish phase.

For the half-turn finish, I see `U2 B2 F2 L2` (chunk of a 9-move phase) — apply and re-check.

I turn `U2 B2 F2 L2`.

Quick check: in HTR.

Residual class: mixed.

Still mixed. Continuing the finish phase.

For the half-turn finish, I see `B2 L2 U2 B2` (chunk of a 5-move phase) — apply and re-check.

I turn `B2 L2 U2 B2`.

Quick check: in HTR.

Residual class: mixed.

Still 4 corners and 4 edges unsolved. Let me finish the last chunk.

For the half-turn finish: `R2`.

I turn `R2`.

A quick glance — the cube is solved.

Excellent! The cube is solved in 30 moves. Now let me compose the final solution and check for any cancellations.

I assemble the canonical normal-frame solution: **30 moves**, verified.

I have a 30-move solution. However, since the move count is ≥27 and I should have plenty of budget remaining, let me check if replace_and_shorten can improve this. Let me first check my budget status.

Budget check: 3444.0s sim, None tool calls remaining.

I have 3444s remaining and many tool calls left. The gates for replace_and_shorten should pass (30 moves ≥ 27, and I have way more than 30 tool calls remaining). Let me try to shorten a large tail span — I'll target moves 4 through 30 (the post-EO portion).

replace_and_shorten on the tail span: substitute is 4 moves shorter. Accepted.

**Excellent!** Replace_and_shorten found a 4-move improvement! The new solution is 26 moves total. The substitute solves the scramble.

Let me update the slot with this new history and verify.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `R2 D' B' F' B2 R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`.

Nice! One move cancelled automatically (B' → B = cancel). Let me verify this solution.

A quick glance — the cube is solved.

Perfect! The cube is solved in **25 moves** after the automatic cancellation. Let me compose the final solution.

I assemble the canonical normal-frame solution: **25 moves**, verified.

Let me verify this solution one final time against the original scramble.

verify_solved: ✓ — 25 moves.

Perfect! The solution is verified.

## **FINAL SOLUTION**

**Solution breakdown:**
- **EO on UD (4 moves):** R2 D' B' F' — recognized the 8-bad-edge pattern
- **DR via JZP-eligible 4C2E path (replaced and shortened):** The initial 8-move DR path was replaced with a more efficient 21-move continuation
- **Total: 25 moves**

**Final move sequence:**

FINAL_SOLUTION: ["R2", "D'", "F'", "B", "R2", "F2", "R2", "U2", "F2", "D2", "R2", "D2", "L2", "U'", "B2", "U'", "F2", "U", "R", "U", "L2", "D", "L", "D'", "L'"]

**Summary:**
- Started with UD-axis EO (4 moves) as it was the shortest complete EO available
- Pursued the JZP-eligible DR-4C2E path (12 moves to DR)
- HTR classification showed 0-swap long-cycle subset
- Initial solve: 30 moves
- Used replace_and_shorten on the post-EO span [4:30], which found a 4-move savings
- After cancellation: **25 moves**
- Time spent: 186s simulated out of 3600s budget

**Verified solution (25 moves):** `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`
