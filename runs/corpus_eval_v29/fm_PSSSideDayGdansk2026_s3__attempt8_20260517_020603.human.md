# Solve — fm_PSSSideDayGdansk2026_s3__attempt8_20260517_020603

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 27 moves
**Solution**: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`

---

*Thinking (1):*

> Let me understand the task. I need to solve this scramble:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Looking at the prior attempts:
> - Attempts 1, 2, 3, 5, 6: all 30 moves, identical solution
> - Attempt 4: 34 moves, different
> - Attempt 7: 30 moves, different
> 
> The best is 30 moves. The instruction says to COMMIT HARD - pick a line and drive it to a clean finish. Don't over-ideate between branches. Trust the axis from prior attempts if it looked promising.
> 
> Let me start by inspecting the state to see what we're working with.

I'll solve this scramble systematically. Given the prior attempts all reached 30 moves, my goal is to find a cleaner path through better DR-substate choices. Let me start by inspecting.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.

Good! I see:
- **UD axis: 4 bad edges** (UL, DR, DL, DB) — this is the shortest EO. The bad edges are mostly on the D layer.
- **FB axis: 8 bad edges** — too many.
- **RL axis: 6 bad edges** — moderate.
- **DR-closeness on UD: 7C3E** but **top_pairs_on_inverse = 3** — this is a STRONG NISS signal! With 3 pairs preserved on inverse, the inverse frame likely has a much better DR substate.

**Plan**: Check inverse EO first. The 3 pairs on inverse is a very strong signal that the inverse frame will have cleaner DR options, potentially a 3C2E or better. Let me flip and scout.

NISS flip — switching to the inverse scramble.

Now on inverse. Let me check the state again.

I look over the cube.
Bad-edge counts: UD=4, FB=8, RL=6.
I'm currently working on the inverse scramble.

Still 4 bad edges on UD axis (inverse side). Let me check the EO pattern on inverse-UD.

On UD axis I recognize the EO pattern — `B' R' U B'` fixes it.

Good! 4-move EO on inverse-UD. Now let me probe what DR options this gives using `probe_dr_pattern` to see the DR trigger family AND total before committing.

I probe what DR would look like if I applied this EO (without committing).

Hmm, 9 moves total to DR on inverse-UD (4 EO + ~5 DR setup). That's borderline — within the elite ≤10 rule but not great. Let me also check the normal side's UD axis for comparison before committing.

NISS flip — switching back to the normal scramble.

Back on normal. Let me check normal-UD EO.

On UD axis I recognize the EO pattern — `U L R' B'` fixes it.

Normal-UD also 4-move EO (U L R' B'). Let me probe DR on this.

I probe what DR would look like if I applied this EO (without committing).

Better! Normal-UD: 4 EO + 4 DR = 8 moves to DR (vs inverse 9). The prior 30-move solutions all started with "U L R' B'" — that's this EO! Let me commit to normal-UD and see what DR trigger options I have. I'll apply the EO and then call dr_trigger_options.

I turn `U L R' B'`.

EO complete. Now let me survey DR trigger options on UD.

DR trigger menu on UD: no named trigger fits within 5 setup moves.

Interesting! No trigger options found within 5 moves. Let me try max_setup=6.

I survey the named DR triggers on UD:
  • DR-7C8E (R U L): 6-mv setup + 3-mv trigger (9 total)

Only one option: DR-7C8E in 9 moves (6 setup + 3 trigger). That's acceptable (≤10) but 7C8E is the worst DR substate — typically ~15 moves post-DR. Total would be ~24 moves, giving me a 28-move solution — not better than the 30-move prior.

Let me check FB axis for comparison. Let me undo and try FB EO.

I rewind 4 moves.

Back to scramble. Let me check FB axis EO (8 bad edges — harder but might have a better DR).

On FB axis I recognize the EO pattern — `R' F D L'` fixes it.

Excellent! FB axis also has a 4-move EO (R' F D L')! Let me probe DR on this.

I probe what DR would look like if I applied this EO (without committing).

Even better! FB: 4 EO + 3 DR = **7 moves to DR**. That's 2 moves shorter than UD! Let me commit to FB and check the trigger options.

I turn `R' F D L'`.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

No options within 5. Let me try 6.

DR trigger menu on FB: no named trigger fits within 5 setup moves.

Hmm, no named triggers found. Let me fall back to dr_recognize which will find the DR pattern even if it's not a classic trigger.

I check whether the DR is recognizable from this state via the library.

Got it! The DR is 7 moves total (matching the probe), but I can only see 4 moves at a time. Let me apply the setup progress.

I turn `B' D F' U'`.

Now re-query DR.

I check whether the DR is recognizable from this state via the library.

Excellent! I see a 2-move setup (B L2) followed by a 1-move trigger (D'). Total remaining: 3 moves. Let me apply them.

I turn `B L2`.

I turn `D'`.

Great! I'm at DR in 11 moves (4 EO + 7 DR). Now let me classify the HTR substate.

I recognize the HTR subset: **4-swap long-cycle**. Reduction is 8 moves, finish is 9 moves (first exposure — learning).

I see the substate: **4-swap long-cycle** with cycle structure [4,4]. The finish is 8+9=17 moves. Total solution: 11 DR + 17 finish = **28 moves**! That's 2 moves better than the prior 30-move attempts!

Let me apply the HTR reduction phase.

For the corner reduction, I see `D2 F2 R2 U2` (chunk of a 8-move phase) — apply and re-check.

Partial! Only seeing 4 moves. Let me apply them.

I turn `D2 F2 R2 U2`.

Good, 1 auto-cancellation already (D' + D2 → D). Let me check if I'm in HTR yet with a quick_check.

Quick check: DR-locked on FB, not yet HTR.

Not at HTR yet. Let me continue the HTR reduction.

For the corner reduction: `F' U2 L2 B`.

Good, the rest of HTR reduction (4 moves). Let me apply.

I turn `F' U2 L2 B`.

At 18 moves, should now be in HTR. Let me verify.

Quick check: in HTR.

Perfect! Now in HTR (is_htr_ud=true). The finish should be 9 moves. Let me apply it.

For the half-turn finish, I see `R2 U2 B2 R2` (chunk of a 9-move phase) — apply and re-check.

Partial again. Let me apply.

I turn `R2 U2 B2 R2`.

Let me check if solved yet.

Quick check: in HTR.

Not solved yet. Let me continue the finish.

For the half-turn finish, I see `F2 U2 B2 D2` (chunk of a 5-move phase) — apply and re-check.

I turn `F2 U2 B2 D2`.

Quick check: in HTR.

Still not solved. Let me get the last move.

For the half-turn finish: `F2`.

I turn `F2`.

A quick glance — the cube is solved.

SOLVED in 27 moves! That's 3 moves better than all prior attempts! Let me now run cancellation and compose the final solution.

I assemble the canonical normal-frame solution: **27 moves**, verified.

Perfect! The solution is 27 moves and verified. Now, per the rules: I should check if I can use replace_and_shorten. I have 27 moves (≥27 ✓) and I should check my remaining tool calls. Let me check budget.

Budget check: 3467.0s sim, None tool calls remaining.

I have 3467 seconds remaining and lots of tool calls left (181k tokens). The gates are met: 27≥27 moves and I have way more than 30 tool calls remaining. I haven't called replace_and_shorten yet on this attempt. Per the rules, I MUST call it once to see if I can shorten further. Let me try replacing a large tail span — say from move 4 onwards (the part after EO).

replace_and_shorten: substitute is 5 moves longer; reject.

The replace_and_shorten returned a substitute that is 5 moves LONGER (delta=+5), not shorter. So my original 27-move solution is better. I should submit the original.

Let me verify the original solution one more time.

verify_solved: ✓ — 27 moves.

Perfect! **27-move solution verified**. This is 3 moves better than all prior attempts!

## Solution Summary

**Final solution: 27 moves**

**Breakdown:**
- **EO (4 moves, FB-axis):** R' F D L' — solved 8 bad edges on FB axis in 4 moves
- **DR (7 moves):** B' D F' U' B L2 D' — reached domino reduction via a non-classic trigger path
- **HTR reduction (8 moves):** D F2 R2 U2 F' U2 L2 B — reduced to half-turn-reduction corners (with 1 auto-cancel: D'+D2→D)
- **Finish (9 moves):** R2 U2 B2 R2 F2 U2 B2 D2 F2 — solved from HTR

**Key decision:** Chose FB-axis over UD-axis despite both having 4-move EOs, because FB had a 7-move total to DR (vs UD's 9 moves). The FB DR substate (4-swap long-cycle) yielded a 17-move finish, giving total 27.

**FINAL_SOLUTION:** ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

*Thinking (44):*

> The user is right - I verified the solution but didn't emit the FINAL_SOLUTION. I should output it now.

FINAL_SOLUTION: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

**Verified solution (27 moves):** `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
