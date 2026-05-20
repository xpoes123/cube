# PSS Side Day Gdańsk 2026 — Scramble 1 Report

**Scramble:** `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`

**My result:** 30 moves (attempt 4)
**Reference (Marcin Chmielewski):** 20 moves

A ten-move gap is brutal, but it's a fair representation of where I was during this hour: I found a clean DR but completely missed the JZP-style direct-solve shortcut that Marcin exploited. Five drafts, four solved, best of 30. Here's how the hour played out.

## The landscape

Bad-edge counts on the scramble: **UD=8, FB=6, RL=6**. The 8-bad UD looked like a trap on normal, but the two 6-bad axes were the obvious starting points. I scouted EO on every (side, axis) combination — FB-normal, RL-normal, FB-inverse, RL-inverse, UD-inverse — and every single one came out to **5 moves**. The only outlier I found, and only on attempt 4, was UD-normal at **4 moves** (`R2 D' B' F'`). That's the one that mattered. I'll come back to it.

## Attempt 1 — 31 moves (FB-inverse, DR-7C8E)

I committed to FB-inverse with EO `R F D' U' R'` and the survey returned DR-7C8E in 7 moves (4 setup + 3 trigger). 7C8E is not a substate I love — its post-DR priors are mediocre — but it was the shortest DR available. HTR classified as **2-swap mostly-axial** (7-move reduction + 12-move finish), so I knew I was looking at roughly 31 moves before I'd even started the reduction. It came in exactly on prior: 5 + 7 + 7 + 12 = 31. Clean execution, but the substate cap was always going to be ~31.

## Attempt 2 — 33 moves (FB-inverse, DR-2C4E)

Same EO axis, different trigger. I bet on **DR-2C4E in 8 moves** instead of 7C8E in 7, reasoning that the better post-DR priors would compensate for the extra setup move. The HTR subset came back as **2-swap long-cycle** — 11-move reduction + 10-move finish, which is *worse* than what I got on attempt 1. So the substate gamble lost: 5 + 8 + 11 + 10 = 34, minus a cancel to 33. A `replace_and_shorten` on the tail returned +1 and I rejected it.

## Attempt 3 — DNF (max_tool_calls)

I tried to be cute. Scouted all six (side, axis) EO options, rejected FB-inverse because of the 7C8E substate, rejected RL-inverse because the only trigger was DR-4C4E in 9 moves, then pivoted to UD-inverse where `dr_trigger_options` returned **nothing** at depth 5. I fell back to `dr_recognize` with brain suggestions and started chaining single-move probes — `D'`, then more single moves — and the tool budget evaporated. No solution submitted. Pure branch-hopping failure.

## Attempt 4 — 30 moves ✓ (submitted)

This was the only attempt where I checked **UD-normal** EO instead of dismissing the 8-bad axis. The pattern lookup returned `R2 D' B' F'` — a **4-move EO**, one shorter than every other option I'd looked at across three prior drafts. From there, `dr_trigger_options` gave me **DR-4C2E in 8 moves** (`U' R' L2 U F2 R U2 R'`), landing at DR with 4 qt corners remaining. HTR classified as **0-swap long-cycle** (10 reduction + 9 finish). Total: 4 + 8 + 10 + 8 = 30 after a cancel. Verified, submitted.

## Attempt 5 — 40 moves (UD-inverse, brain-walked)

Tried UD-inverse again, hoping to undercut attempt 4 by avoiding the long DR setup. Same result as attempt 3: no triggers at depth 5, `dr_recognize` walking single moves. This time I didn't run out of calls — I just landed at DR way too late and shipped a bloated 40-mover. Confirmation that the UD-inverse path is structurally bad on this scramble.

## Why attempt 4 won

It was the only draft that found the 4-move EO. Every other attempt assumed the 6-bad axes had to be cheaper than the 8-bad UD — a reasonable prior in general, but wrong here. Once UD-normal opened with a 4 instead of a 5, *and* DR-4C2E was available in 8 with a clean 0-swap long-cycle HTR substate, the line was forced. The other drafts were all chasing local optima on 5-move EOs with worse DR substates downstream.

## The winning solution, phase by phase

`R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`

- **EO (4):** `R2 D' B' F'` — UD axis, kills all 8 bad edges
- **DR (8):** `U' R' L2 U F2 R U2 R'` — DR-4C2E trigger, lands at UD-DR with 4 qt corners
- **HTR reduction (10):** `U F2 U' R2 U L2 U2 R2 F2 U'` — 0-swap long-cycle
- **Half-turn finish (8):** `B2 F2 L2 B2 L2 U2 B2 R2`

The DR phase is the meatiest chunk. The reduction → finish split is fine; nothing leaks moves there.

## Where I lost ten moves

Marcin's solution is the lesson. His EO is **4 moves** (`R2 D F B'`) — same axis as mine, same length, essentially the same idea (UD-normal with `R2` first and the F/B/D triple to flip the remaining edges). So **EO is a wash**. He's not winning there.

Where he wins is the next 6 moves: `L B2 R D2 L' D'` — a **2c3 + 2e** state in 6 moves, not a named DR trigger. Then he solves the rest **directly** in 10 moves: `B2 L' U2 R2 U2 R F2 B2 D2 L'` written on inverse, which composes cleanly with the scramble for a 20-move JZP-style finish.

In my attempt 4 I burned **8 moves to reach a full DR** (DR-4C2E), then **18 more** to walk DR → HTR → solved. That's 26 moves after EO. Marcin spends 16 moves after EO — and crucially, **he never reaches DR or HTR**. He's not playing the same game. He found a 2c3-2e residual at depth 6 from EO and solved it directly, skipping both the DR-trigger setup tax (my +3 moves of trigger appendage) and the HTR-reduction tax (my +10 moves to clean up qt corners).

The specific call that cost me: I never ran a 2c2e/2c3-2e/JZP scan after EO. My pipeline goes EO → `dr_trigger_options` → DR → HTR → finish, and `dr_trigger_options` only knows named DR families. There's no step that asks "what's the cheapest direct solve from this EO state?" — and on a scramble where the EO leaves you 6 moves from a 2c3+2e residual, that omission is fatal. Ten moves fatal.

The 8-move DR-4C2E lookup felt great at the time (best of the five drafts), but in retrospect it's the move that locked me into a 30-move ceiling. A 6-move setup to a non-named 2c+2e state would have given me a shot at 22–24.

## Closer

Clean execution on a path that was never going to be the winning path — I need a "skip-DR" probe in my pipeline before I see a scramble like this again.
