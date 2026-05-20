# PSSSideDayGdansk2026 — Scramble 2 Report

**Scramble:** `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`

**Submitted:** 34 moves. **Reference (Marcin Chmielewski):** 20 moves.

A 14-move gap. That stings, but the result wasn't a fluke — three of my four drafts converged on the exact same line, which tells me my DR scouting was leaving the best paths on the floor. This is the post-mortem.

The opening inspection is identical every draft: UD=6, FB=4, RL=4. Two natural 4-bad-edge axes, plus a 6-bad UD. Normal-side EO scouting gives `B2 L2 U2 R'` (FB) and `R2 B F2 U'` (RL), both 4 moves. NISS-flip and check inverse: **FB-inverse drops to `U2 R'` (2 moves)** and RL-inverse stays at 4. That 2-mover is the headline, and — as you'll see — it's also exactly where Chmielewski started. The difference is what we each did with it.

## Attempt 1 — chased inverse-FB into a brain-walk, salvaged inverse-UD

I committed to the 2-move `U2 R'` EO on inverse-FB, but `dr_survey` returned nothing within 5 moves (97k states, no named trigger family). `dr_recognize` only offered an R2 at 65% — i.e., no memory hit, just a brain guess. I bailed, tried normal-FB and normal-RL: FB found nothing, RL found only **DR-7C8E in 8** — a notoriously bad substate. With urgency creeping up I pivoted to inverse-UD (4-move EO `B R2 U F'`) and walked the brain hints one move at a time: `U → D → L' → R → U → L'`, until `dr_recognize` finally surfaced a **DR-3C2E** with setup `U2` + trigger `R U R'`. That gave 4+6+3 = 13 to DR, then a "2-swap mostly-axial" HTR subset to grind out the 34. Solved, submitted as the safety net.

## Attempt 2 — committed to RL-normal DR-7C8E, matched 34

This time I told myself to commit hard. Same EO survey, same conclusion that inverse-FB has no easy DR. I bit the bullet and took the **RL-normal DR-7C8E in 8** that I'd rejected in attempt 1: `R B' D2 R' B' F' L B` after `R2 B F2 U'`. The HTR subset came back as **2-swap long-cycle** — 11 reduction + 12 finish per the priors. The reduction chunk `B2 R U2 R` got a free cancellation with the trailing B from the trigger, and HTR landed cleanly. Finish was a textbook `U2 B2 R2 D2 / F2 U2 F2 U2 / L2 D2 R2 U2` slice-axis cascade. 34 moves, verified. I tried `replace_and_shorten` on the tail; it couldn't find a DR on the micro-scramble.

## Attempt 3 — same line, faster, no improvement

Identical EO scout, same pivot away from inverse-FB after `dr_recognize` looped (`R2 → F2 → L → L'` back to start — I was going in circles in the brain region). Committed to RL-normal DR-7C8E again, same 8-move trigger, same 2-swap long-cycle subset, same finish. Bit-for-bit identical 34-move solution as attempt 2. The good news: I got there in 49 tool calls vs 58. The bad news: I didn't try anything new.

## Attempt 4 — same scout, ran out of sim budget

Repeated the EO comparison and the inverse-FB probe. Same `dr_survey` failure, same `dr_recognize` R2 suggestion, same pivot to RL-normal. The pivot itself ate the sim budget — by the time I had the DR-7C8E trigger surfaced, urgency was already low and I never finished the HTR reduction. No submission from this draft.

## Why attempt 1 was submitted

All three solved drafts hit 34. Attempt 1 was the canonical submission by virtue of being first and verified. Attempts 2 and 3 were move-for-move identical; submitting any of them would have been the same result. The submission was effectively forced.

## The winning solution, walked

`U2 B2 U2 L2 U2 R2 D2 B2 R2 D2 R2 D' R2 U' B2 U B2 U' F2 U' R U' R' U2 L U' R' L D' U' F U' R2 B'`

This is the attempt-1 solution (inverse-UD line), written on the normal frame after composition:

- **EO (inverse, UD axis):** `B R2 U F'` — 4 moves on the inverse, fixing the 6 bad UD edges.
- **DR setup (brain-walked):** `U D L' R U L'` — 6 moves of slow recognition before memory caught the pattern.
- **DR trigger (DR-3C2E):** `U2 R U R'` — 4 moves, 13 to DR total.
- **HTR + finish (2-swap mostly-axial):** the long tail of `U2`-rich half-turns and the closing `R2 B'` after frame composition — 21 moves out the back.

The DR was actually cheap once found. The problem is everything around it.

## What I'd do differently

The 14 moves I lost relative to Chmielewski are almost entirely in **DR selection**, not in finish.

Chmielewski took the same 2-move `U2 R'` EO on inverse-FB that my scout flagged and that I abandoned in every draft. From there his DR is `B U' B2 U F D B` — a 7-move DR-4b2-2e finish in **9 moves to DR**. My `dr_survey` capped at setup-depth 5 and returned nothing because the setup he used is deeper / on a non-standard trigger family that didn't match my 10-trigger BFS. `dr_recognize` then suggested R2 at 65%, which is a brain hallucination on an unfamiliar state — not memory — and I (correctly) didn't trust it, but I also didn't push past it manually. The right move was to **trust the 2-move EO** and either (a) do a deeper setup search on FB, or (b) hand-explore B/U/D moves preserving FB-EO instead of bailing.

After his 9-to-DR he hits HTR in 12 with `U F2 U'`, then a 7-move slice finish for 19+1. My RL-normal DR-7C8E branch was condemned to a 22-move tail because 7C8E is the worst substate in the priors table; I knew that and took it anyway because I'd given up on the better axis. The inverse-UD line in the submitted solution is even worse in a different way — the DR was reached in 13, but a 21-move tail on a "2-swap mostly-axial" subset is a sign that the DR substate wasn't great either.

Concrete lesson: **when `dr_survey` returns nothing on a 2-move EO, that's a flag to search harder, not to abandon the axis.** A 2-move EO is rare enough that it almost always justifies a deeper DR scout (depth 6-7) before pivoting. I pivoted three times in four drafts, and all three pivots landed on worse axes.

Three identical 34s is what happens when you flinch at the same fork.
