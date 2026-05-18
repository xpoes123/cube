# Solve — fm_PSSSideDayGdansk2026_s1__attempt4_20260517_232551

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: SOLVED in 31 moves
**Solution**: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`

---

*Thinking (1):*

> Alright, I have a scramble where the prior best is 29 moves. The system is telling me to commit hard this attempt - pick a line and drive it clean. Let me start by inspecting the state.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> Prior attempts got 29-30 moves. I need to:
> 1. Inspect state first
> 2. Scout EO on normal and inverse for 1-2 most promising axes
> 3. Pick a (side, axis) based on JOINT EO+DR cost
> 4. Commit and drive to finish
> 5. Don't overthink - complete the solve
> 
> Let me start with inspect_state to see what we have.

I'll solve this scramble with a commit-hard strategy. Starting with inspection to understand the initial state.

I look over the cube.
Bad-edge counts: UD=8, FB=6, RL=6.

**OBSERVATION**: Bad edges per axis: UD=8, FB=6, RL=6. FB and RL look more promising for EO. The DR state shows DR-6C3E on UD with 2 pairs on inverse (a NISS switch signal), DR-5C2E on FB (non-JZP), DR-7C3E on RL. 

**STRATEGY**: I'll scout FB and RL on both normal and inverse. The prior 29-move solution likely used one of these axes. Let me start with FB on normal.

On FB axis I recognize the EO pattern — the first chunk is `R2 B' L' U2` (full fix is 4 moves).

FB-normal EO is **5 moves** (seeing first 4 now). Let me also check RL-normal.

On RL axis I recognize the EO pattern — the first chunk is `L U L2 R` (full fix is 4 moves).

RL-normal is also **5 moves**. Now let me check the inverse side — flipping to inverse and checking FB and RL there. The prior attempts starting around 29-30 might have used inverse.

NISS flip — switching to the inverse scramble.

Now on inverse. Checking FB-inverse EO (remember bad_edges_per_axis is the same, so still 6 bad edges on FB).

On FB axis I recognize the EO pattern — the first chunk is `R F D' U'` (full fix is 4 moves).

FB-inverse is also **5 moves**. Checking RL-inverse.

On RL axis I recognize the EO pattern — the first chunk is `B U B2 F` (full fix is 4 moves).

**ALL AXES ARE 5 MOVES** on both sides. The bad edges pattern (UD=8, FB=6, RL=6) doesn't give a quick EO. Now I need to probe DR cost for each viable candidate. The inspect_state showed `top_pairs_on_inverse: 2` on UD-axis, which is a NISS signal. Let me also check UD's EO on inverse.

On UD axis I recognize the EO pattern — the first chunk is `B' D' L' R'` (full fix is 4 moves).

UD-inverse is also **5 moves**. All axes are equal on EO length (5mv). The decision comes down to DR quality. Let me commit to one line and probe DR. I'll test **FB-inverse** first since FB had DR-5C2E (better than UD's 6C3E and RL's 7C3E). I'm currently on inverse, so let me apply the FB-inverse EO and check DR options.

Applying FB-inverse EO (first 4 moves):

I turn `R F D' U'`.

Getting the last move of FB EO:

On FB axis I recognize the EO pattern — `R'` fixes it.

Perfect! FB EO completes in **5 moves total** (R F D' U' R'). Applying:

I turn `R'`.

**FB EO complete on inverse: R F D' U' R' (5 moves)**. Now checking DR options on FB axis.

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on FB:
  • DR-7C8E (U F D): 4-mv setup + 3-mv trigger (7 total) pre=DR-7C4E
  • DR-7C8E (U' F D): 5-mv setup + 3-mv trigger (8 total) pre=DR-7C4E
  • DR-2C4E (U L2 U): 5-mv setup + 3-mv trigger (8 total) pre=DR-4C1E

**FB-inverse DR options**: Best is DR-7C8E in 7 moves total (4 setup + 3 trigger). That's a DR-7C8E substate which is NOT in my memorized table (likely 14+ moves post-DR). **This is BAD** — the 5mv EO + 7mv DR = 12mv to DR, and 7C8E is one of the worst substates.

Let me reset and try a different axis. I'll test **RL-inverse** next since it also had 5mv EO.

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Flipping back to inverse:

NISS flip — switching to the inverse scramble.

Applying RL-inverse EO (B U B2 F):

I turn `B U B2 F`.

Getting the last RL EO move:

On RL axis I recognize the EO pattern — `D'` fixes it.

I turn `D'`.

**RL EO complete on inverse: B U B2 F D' (5 moves)**. Checking DR on RL axis:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
I survey the named DR triggers on RL:
  • DR-4C4E (F L2 U2 F): 5-mv setup + 4-mv trigger (9 total) pre=DR-4C2E

**RL-inverse DR**: DR-4C4E in 9 moves (5 setup + 4 trigger). EO=5 + DR=9 = **14 moves to DR**, and 4C4E has 12-14mv post-DR (non-JZP). Total ~26-28 moves. This is worse than FB.

Let me try **UD-inverse** since it had `top_pairs_on_inverse: 2` which is a NISS signal. Resetting again:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

Applying UD-inverse EO (B' D' L' R'):

I turn `B' D' L' R'`.

On UD axis I recognize the EO pattern — `F'` fixes it.

I turn `F'`.

**UD EO complete on inverse: B' D' L' R' F' (5 moves)**. Checking DR on UD axis:

_DR survey on UD: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on UD.**

**UD-inverse DR: NO options at depth 5**. This means DR is >10 moves away, which violates the elite-solver hard rule (DR ≥10 never appears in sub-22). This axis is dead.

I need to try normal-side options now. Let me go back to normal and test **FB-normal** with a DR probe:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

Applying FB-normal EO (R2 B' L' U2 for the first 4):

I turn `R2 B' L' U2`.

On FB axis I recognize the EO pattern — `R'` fixes it.

I turn `R'`.

**FB-normal EO: R2 B' L' U2 R' (5 moves)**. Checking DR:

_DR survey on FB: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on FB.**

**FB-normal: NO DR options at depth 5**. Also dead. Let me try **RL-normal**:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

I turn `L U L2 R`.

On RL axis I recognize the EO pattern — `D'` fixes it.

I turn `D'`.

**RL-normal EO: L U L2 R D' (5 moves)**. Checking DR:

_DR survey on RL: BFS over EO-preserving moves (setup depth ≤5), checking each visited state against the 10 named trigger families (DR-4C4E, DR-3C2E, DR-4C2E, ...). Returns the shortest setup found for each family that fit._
**No trigger family had a setup ≤5 moves on RL.**

**NONE OF THE 5-MOVE EO AXES GIVE DR ≤10 MOVES**. This is a very hard scramble. The only viable paths I found were:
- **FB-inverse**: EO=5, DR-7C8E in 7 (total 12 to DR, ~26-28 expected)
- **RL-inverse**: EO=5, DR-4C4E in 9 (total 14 to DR, ~26-28 expected)

Both are marginal. The prior 29-move solution must have used one of these or found a different approach. Let me **COMMIT to FB-inverse** with the DR-7C8E path since it reaches DR faster (12 vs 14). I'll drive through HTR and optimize the finish.

Resetting to commit to FB-inverse:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

**COMMITTING TO FB-INVERSE**. Applying EO (R F D' U' R'):

I turn `R F D' U' R'`.

Applying DR setup + trigger (D F' L2 B' + U F D):

I turn `D F' L2 B' U F D`.

**12 moves to DR** (5 EO + 7 DR). Now classifying the HTR subset on FB axis:

I recognize the HTR subset: **2-swap mostly-axial**. Reduction is 7 moves, finish is 12 moves (first exposure — learning).

**HTR subset: 2-swap mostly-axial** (htr_reduction=7, finish=12, total=19 post-DR). Combined: 12 (to DR) + 19 (DR to solved) = **31 moves**. This is WORSE than the prior 29-move best.

Let me try the **RL-inverse** path to see if the 4C4E substate gives a better finish despite the longer DR:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

**COMMITTING TO RL-INVERSE**. Applying EO (B U B2 F D'):

I turn `B U B2 F D'`.

Applying DR setup + trigger (L2 B2 L' U2 R2 + F L2 U2 F):

I turn `L2 B2 L' U2 R2 F L2 U2 F`.

**14 moves to DR**. Classifying HTR on RL axis:

I recognize the HTR subset: **2-swap long-cycle**. Reduction is 10 moves, finish is 10 moves (first exposure — learning).

**HTR: 2-swap long-cycle** (htr_reduction=10, finish=10, total=20 post-DR). Combined: 14 + 20 = **34 moves**. Even WORSE.

This scramble is genuinely hard. Both viable paths are 31-34 moves. The prior 29-move solution likely used a different technique or got lucky with cancellations/insertions. Let me **go back to the FB-inverse path (31 moves projected)** and complete it, then use replace_and_shorten if I have budget.

Resetting to FB-inverse again:

I reset the cube back to the scramble — fresh start, dropping the branch I was on.

NISS flip — switching to the inverse scramble.

Rebuilding FB-inverse to DR:

I turn `R F D' U' R' D F' L2 B' U F D`.

Applying HTR reduction (first 4 moves):

For the corner reduction, I see `F' U2 R2 L2` (chunk of a 7-move phase) — apply and re-check.

I turn `F' U2 R2 L2`.

Checking if solved or HTR reached:

Quick check: DR-locked on FB, not yet HTR.

Still in HTR reduction. Getting the rest:

For the corner reduction: `F R2 B`.

I turn `F R2 B`.

**19 moves** (12 to DR + 7 HTR reduction). Now the finish (12 moves expected):

For the half-turn finish, I see `L2 F2 U2 R2` (chunk of a 12-move phase) — apply and re-check.

I turn `L2 F2 U2 R2`.

Quick check: in HTR.

HTR done, in finish phase. Continuing:

For the half-turn finish, I see `B2 R2 F2 U2` (chunk of a 8-move phase) — apply and re-check.

I turn `B2 R2 F2 U2`.

Quick check: in HTR.

For the half-turn finish: `R2 U2 R2 U2`.

I turn `R2 U2 R2 U2`.

A quick glance — the cube is solved.

**SOLVED in 31 moves on inverse!** Now composing the NISS solution (this will invert the inverse-side moves):

I assemble the canonical inverse-frame solution: **31 moves**, verified.

**31-move solution verified!** This matches the projected length. Now I need to try **replace_and_shorten** since:
- Total moves (31) ≥ 27 ✓
- I haven't called it yet ✓
- I need to check if I have ≥30 tool calls remaining

Let me check budget:

Budget check: 1926.26s sim, None tool calls remaining.

I have ~1926s remaining (plenty). The solution is 31 moves, and I should try replace_and_shorten to see if I can beat the prior 29. Let me target a large tail span (e.g., moves 4-31) to re-solve the bulk:

r&s: too few tool calls remaining (17) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.

**Can't use replace_and_shorten** — only 17 tool calls left (need 30). I'll submit the 31-move solution. It's 2 moves worse than the prior best (29), but it's a complete, verified solve.

**FINAL_SOLUTION:**

["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]

**Solution breakdown:**
- **FB-axis inverse EO**: R F D' U' R' (5 moves)
- **DR via 7C8E trigger**: D F' L2 B' U F D (7 moves, total 12 to DR)
- **HTR reduction**: F' U2 R2 L2 F R2 B (7 moves, total 19)
- **HTR finish**: L2 F2 U2 R2 B2 R2 F2 U2 R2 U2 R2 U2 (12 moves, total 31)

This scramble is genuinely difficult — all EO axes required 5 moves, and no axis gave DR ≤10 moves on the standard trigger catalog. The FB-inverse path with DR-7C8E was the best available option, reaching a 2-swap mostly-axial HTR subset that finished in 19 moves post-DR.

**31 moves total.** Verified complete solve.

*Thinking (65):*

> The user is right - I narrated the solution but didn't actually emit it in the required format. Let me output it now.

FINAL_SOLUTION: ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]

**Verified solution (31 moves):** `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`
