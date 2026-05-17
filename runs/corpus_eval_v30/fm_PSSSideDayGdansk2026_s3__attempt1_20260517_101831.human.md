# Solve — fm_PSSSideDayGdansk2026_s3__attempt1_20260517_101831

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 30 moves
**Solution**: `U L R' B' U2 F2 L2 F2 R2 B2 U2 L2 B2 U' L2 U' L2 U B2 U' F2 U' R U R B2 L' U R' D'`

---

*Thinking (1):*

> The user is asking me to solve a Rubik's Cube FMC scramble within a simulated one-hour budget. I need to start by inspecting the state to understand the cube configuration, then follow the FMC methodology outlined in the instructions.
> 
> Let me begin by calling inspect_state on the 'main' slot to see what I'm working with.

I'll solve this FMC scramble step by step, starting with inspection and following elite FMC methodology.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

**Initial state inspection:**
- **Bad edges per axis**: UD=4, FB=8, RL=6. UD axis is the clear winner for EO.
- **DR-closeness**: UD is DR-7C3E (not great), FB is DR-6C3E, RL is DR-5C3E.
- **Critical observation**: `top_pairs_on_inverse: 3` on UD axis! This is a strong signal to check the inverse side first (Wen's pairs-tracing: 2+ pairs = switch signal).
- The 4 bad edges on UD axis are at UL, DR, DL, DB — scattered across multiple flipping faces.

Elite FMC strategy: with 3 pairs on inverse, I MUST scout the inverse frame for EO+DR before committing. Let me flip to inverse and check the EO there.

NISS flip — switching to the inverse scramble.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.
I'm currently working on the inverse scramble.

**On the inverse side:**
- Still UD=4 bad edges (different slots: UL, UB, DR, BL), FB=8, RL=6.
- The DR-closeness is identical (DR-7C3E on UD, etc.). The 3 pairs preserved means inverse should give better DR access.

Let me scout EO on inverse-UD axis first, since it has the fewest bad edges (4).

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

**Inverse-UD EO: 4 moves** (B' R' U B'). Now let me flip back to normal and scout EO there for comparison, then probe DR for both sides.

NISS flip — switching back to the normal scramble.

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

**Normal-UD EO: 4 moves** (U L R' B'). Both sides have identical 4-move EOs. Now I need to probe DR for each to make the joint decision. Let me probe DR on normal side first.

I probe what DR would look like if I applied this EO (without committing).

Normal-UD: EO=4, DR=8, total=12 to DR. Now let me probe inverse-UD:

NISS flip — switching to the inverse scramble.

I probe what DR would look like if I applied this EO (without committing).

**Comparison:**
- **Normal-UD**: EO=4, DR=8, total=12 to DR
- **Inverse-UD**: EO=4, DR=9, total=13 to DR

Normal side is 1 move better to DR. Despite the 3 pairs-on-inverse signal, the actual DR length on normal is shorter. I'll commit to **normal-UD**.

Let me apply the EO and then use dr_trigger_options to see the DR substates available:

NISS flip — switching back to the normal scramble.

I turn `U L R' B'`.

**EO complete**: 4 moves (U L R' B'). Now let me check DR trigger options:

DR trigger menu on UD: no named trigger fits within 5 setup moves.

No DR trigger options found within 5-move setup! This means DR is harder than expected from this state. Let me use dr_recognize as the fallback:

I check whether the DR is recognizable from this state via the library.

**DR is 8 moves total** (beyond 4-move view). The setup_progress is F2 D' R' U'. Let me apply these 4 moves and re-query:

I turn `F2 D' R' U'`.

I check whether the DR is recognizable from this state via the library.

Wait, dr_recognize now says 4 moves total (F2 L' D' + R'), but I already applied 4 moves. Let me undo and re-think:

I rewind 4 moves.

I check whether the DR is recognizable from this state via the library.

Back to the 8-move full optimal. The probe confirmed this. **Decision**: 8 moves to DR is acceptable (sub-15 total to DR is the target, 4+8=12 is good). Let me commit the full DR path. I'll apply the 4 setup moves first:

I turn `F2 D' R' U'`.

I check whether the DR is recognizable from this state via the library.

Now it shows DR in 4 more moves (F2 L' D' R'). Total: 8 (current) + 4 = 12 to DR. Let me apply these:

I turn `F2 L' D' R'`.

Quick check: DR-locked on UD, not yet HTR.

**DR reached!** 12 moves total (EO=4 + DR=8). Now I need to proceed through HTR. Let me classify the HTR subset:

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 8 moves, finish is 11 moves (first exposure — learning).

**HTR subset: 4-swap long-cycle**
- HTR reduction: 8 moves
- Finish: 11 moves
- Total from DR: 19 moves

**Total solution estimate**: 12 (to DR) + 19 (HTR+finish) = **31 moves**.

This is acceptable for a first solve. Let me apply the HTR reduction phase:

For the corner reduction, I see `U R2 U R2` (chunk of a 8-move phase) — apply and re-check.

HTR reduction is 8 moves but only 4 visible. Let me apply the first chunk and check if we're already solved (inter-phase check):

I turn `U R2 U R2`.

Quick check: DR-locked on UD, not yet HTR.

Not solved yet. Let me get the next 4 moves of HTR reduction:

For the corner reduction: `L2 U L2 D`.

I turn `L2 U L2 D`.

Quick check: in HTR.

**HTR reached!** (is_htr_ud=true). 20 moves so far. Now let me apply the finish phase:

For the half-turn finish, I see `L2 F2 U2 L2` (chunk of a 11-move phase) — apply and re-check.

I turn `L2 F2 U2 L2`.

Quick check: in HTR.

Not solved yet. Let me continue with the next chunk of finish moves:

For the half-turn finish, I see `B2 R2 B2 U2` (chunk of a 7-move phase) — apply and re-check.

I turn `B2 R2 B2 U2`.

Quick check: in HTR.

Still not solved. Let me get the next chunk:

For the half-turn finish: `R2 F2 U2`.

I turn `R2 F2 U2`.

A quick glance — the cube is solved.

**SOLVED!** 31 moves total. Now let me compose the final solution with cancellation:

I assemble the canonical normal-frame solution: **31 moves**, verified.

Perfect! I have a verified 31-move solution. Since it's ≥27 moves and I have plenty of tool calls remaining, I should try `replace_and_shorten` to see if I can improve it. Let me check my budget:

Budget check: 3478.0s sim, None tool calls remaining.

I have plenty of budget (3478s remaining). The solution is 31 moves (≥27), so the gates should pass for replace_and_shorten. Let me try it on a large tail span to see if it can shorten the DR+HTR section:

replace_and_shorten on the tail span: substitute is 1 move shorter. Accepted.

**Excellent!** replace_and_shorten saved 1 move: 31 → 30 moves. The new solution solves the scramble. Let me verify this and then submit:

verify_solved: ✓ — 30 moves.

Perfect! The 30-move solution is verified. Let me now check if there are any obvious cancellations I can spot by calling cancel:

I check for cancellations — no savings.

No additional cancellations found. The solution is already optimally cancelled at 30 moves.

**FINAL SOLUTION BREAKDOWN:**
- **EO (UD axis)**: U L R' B' (4 moves)
- **DR**: The replace_and_shorten tool re-solved the post-EO section more efficiently
- **Total**: 30 moves

FINAL_SOLUTION: ["U", "L", "R'", "B'", "U2", "F2", "L2", "F2", "R2", "B2", "U2", "L2", "B2", "U'", "L2", "U'", "L2", "U", "B2", "U'", "F2", "U'", "R", "U", "R", "B2", "L'", "U", "R'", "D'"]

**Verified solution (30 moves):** `U L R' B' U2 F2 L2 F2 R2 B2 U2 L2 B2 U' L2 U' L2 U B2 U' F2 U' R U R B2 L' U R' D'`
