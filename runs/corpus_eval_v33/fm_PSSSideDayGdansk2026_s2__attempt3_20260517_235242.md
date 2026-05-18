# Run — fm_PSSSideDayGdansk2026_s2__attempt3_20260517_235242.json

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (26 moves, 52 tool calls)  
**Sim budget**: 1674s / 3600s  
**Wall time**: 195s  
**Tokens**: 47,761 in (1,105,813 cached), 6,642 out  
**Cost estimate**: $0.624  
**Solution**: `B2 R' D' R' D' R U F2 R2 U B2 U2 R2 U B2 F2 U2 R2 F2 U2 L2 U2 F U' R2 B'`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 6× = 1490s
- `reset_slot`: 4× = 100s
- `replace_and_shorten`: 1× = 30s
- `dr_recognize`: 4× = 16s
- `eo_pattern_lookup`: 4× = 12s
- `apply_moves`: 13× = 7s
- `niss_flip`: 3× = 6s
- `inspect_state`: 1× = 5s
- `apply_htr_phase`: 5× = 5s
- `compose_niss_solution`: 2× = 2s
- `htr_classify`: 1× = 1s

---

_(turn 1: 717 in / 411 out / 12,976 cached, ~$-0.0267, 12.3s API)_

### Turn 1 — thinking

> Looking at the prior attempts:
> - Attempt 1: 34 moves
> - Attempt 2: 31 moves (best so far)
> 
> The instruction is clear: COMMIT HARD this attempt. Pick a line and drive it to completion. Don't over-ideate between branches.
> 
> Let me start with inspect_state to see what we have.
> 
> The scramble is:
> R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F
> 
> I'll start by inspecting the state, then scout EO on multiple axes (normal + inverse), check DR options for promising candidates, commit to one line, and drive it through to completion.
> 
> The key rules:
> 1. NISS invariant: bad_edges_per_axis is IDENTICAL on normal and inverse
> 2. Always check inverse EO too
> 3. DR decision is JOINT: EO_len + DR_total
> 4. DR ≤6 moves in 85.7% of elite solves; DR ≥10 never appears in sub-22
> 5. Substate quality matters more than DR length (3C2E >> 4C4E)
> 6. JZP halves post-DR cost
> 7. Ship rule: get a complete verified solve, then stop unless there's obvious improvement
> 
> Let me start.

**Turn 1 narration**:

I'll solve this scramble systematically, learning from the prior 31-move result. Let me start by inspecting the state.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=12s]
  → EO: [], DR: [], bad_edges {'UD': 6, 'FB': 4, 'RL': 4}
_(turn 2: 999 in / 273 out / 12,976 cached, ~$-0.0279, 6.6s API)_

**Turn 2 narration**:

**Observation**: Bad edges: UD=6, FB=4, RL=4. Both FB and RL look cleaner for EO. The UD axis shows `top_pairs_on_inverse: 3` — that's a STRONG NISS signal (≥2 pairs). Let me scout EO on both normal and inverse sides for FB and RL axes, then check UD-inverse too given the pairs signal.

**Plan**: Scout FB-normal, RL-normal, then flip to inverse and scout UD-inverse (since it has 3 pairs preserved). Compare EO+DR joint costs before committing.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=19s]
  → found=1, best=4m
- `tool#3` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=11s, wall=19s]
  → found=1, best=4m
_(turn 3: 1,494 in / 92 out / 12,976 cached, ~$-0.0292, 2.5s API)_

**Turn 3 narration**:

Both FB and RL have 4-move EOs on the normal side. Now let me check the inverse side, especially for UD given the 3 pairs signal.

- `tool#4` **niss_flip**({"slot":"main"}) [sim=13s, wall=21s]
  → (empty result)
_(turn 4: 993 in / 164 out / 14,096 cached, ~$-0.0326, 3.0s API)_

**Turn 4 narration**:

Now on inverse. Let me scout UD-inverse EO (the axis with 3 pairs) and also check FB/RL inverse for comparison.

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=16s, wall=24s]
  → found=1, best=4m
- `tool#6` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=19s, wall=24s]
  → found=1, best=2m
_(turn 5: 876 in / 204 out / 14,892 cached, ~$-0.0345, 5.1s API)_

**Turn 5 narration**:

**Excellent find!** FB-inverse has a 2-move EO (`U2 R'`), versus 4 moves on all the normal-side axes. UD-inverse also 4 moves. Now I need to test DR options for each promising candidate:
- **FB-inverse**: 2-move EO
- **FB-normal**: 4-move EO  
- **RL-normal**: 4-move EO

Let me commit the FB-inverse EO and check DR options there first, since it has the shortest EO.

- `tool#7` **apply_moves**({"slot":"main","moves":["U2","R'"]}) [sim=19s, wall=29s]
  → hist=2m
  slot=main [INV] hist(2m): `U2 R'`
_(turn 6: 639 in / 91 out / 15,263 cached, ~$-0.0379, 2.1s API)_

- `tool#8` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=316s, wall=34s]
  → (empty result)
_(turn 7: 735 in / 121 out / 15,774 cached, ~$-0.0386, 2.9s API)_

**Turn 7 narration**:

**No DR options found on FB-inverse within 5-move setup!** This is a bad sign — the EO is short but the DR path is blocked. Let me try dr_recognize to see if the brain suggests next moves.

- `tool#9` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=320s, wall=37s]
  → found=0
_(turn 8: 781 in / 139 out / 16,247 cached, ~$-0.0394, 3.6s API)_

**Turn 8 narration**:

Brain suggests R2 (65% confidence). But this is getting exploratory — I'm now 2 moves into FB-inverse with unclear DR path. Let me check the FB-normal path instead (4-move EO), which might have cleaner DR.

Let me reset and try FB-normal.

- `tool#10` **reset_slot**({"slot":"main","rescramble":true}) [sim=345s, wall=41s]
  → (empty result)
_(turn 9: 477 in / 85 out / 16,306 cached, ~$-0.0413, 1.8s API)_

- `tool#11` **apply_moves**({"slot":"main","moves":["B2","L2","U2","R'"]}) [sim=345s, wall=43s]
  → hist=4m
  slot=main hist(4m): `B2 L2 U2 R'`
_(turn 10: 317 in / 91 out / 16,896 cached, ~$-0.0433, 2.4s API)_

- `tool#12` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=644s, wall=48s]
  → (empty result)
_(turn 11: 620 in / 101 out / 17,222 cached, ~$-0.0431, 2.2s API)_

**Turn 11 narration**:

FB-normal also has no DR options at depth 5! This axis is problematic. Let me try RL-normal instead.

- `tool#13` **reset_slot**({"slot":"main","rescramble":true}) [sim=669s, wall=50s]
  → (empty result)
_(turn 12: 601 in / 84 out / 17,255 cached, ~$-0.0435, 2.1s API)_

- `tool#14` **apply_moves**({"slot":"main","moves":["R2","B","F2","U'"]}) [sim=669s, wall=52s]
  → hist=4m
  slot=main hist(4m): `R2 B F2 U'`
_(turn 13: 275 in / 92 out / 17,404 cached, ~$-0.0448, 1.8s API)_

- `tool#15` **dr_trigger_options**({"slot":"main","axis":"RL","max_setup":5}) [sim=912s, wall=56s]
  → (empty result)
_(turn 14: 736 in / 195 out / 17,974 cached, ~$-0.0434, 5.1s API)_

**Turn 14 narration**:

Found DR on RL! **DR-7C8E** with 5-move setup + 3-move trigger = **8 moves to DR total**. But DR-7C8E is a bad substate (7 corners, 8 edges misplaced). This will have a long finish (~14+ moves post-DR). Total projection: 4 EO + 8 DR + 14 finish ≈ 26 moves minimum.

Let me check if I can find better DR by trying dr_recognize after this EO.

- `tool#16` **dr_recognize**({"slot":"main","axis":"RL"}) [sim=916s, wall=61s]
  → found=0
_(turn 15: 970 in / 124 out / 18,007 cached, ~$-0.0438, 6.0s API)_

**Turn 15 narration**:

RL axis is also struggling. Given that both FB and RL axes have weak DR paths, let me check the UD-inverse path (which had 3 pairs preserved and 4-move EO). The pairs signal is strong.

- `tool#17` **reset_slot**({"slot":"main","rescramble":true}) [sim=941s, wall=67s]
  → (empty result)
_(turn 16: 531 in / 54 out / 18,154 cached, ~$-0.0466, 2.3s API)_

- `tool#18` **niss_flip**({"slot":"main"}) [sim=943s, wall=70s]
  → (empty result)
_(turn 17: 605 in / 83 out / 18,938 cached, ~$-0.0481, 2.1s API)_

- `tool#19` **apply_moves**({"slot":"main","moves":["B","R2","U","F'"]}) [sim=943s, wall=72s]
  → hist=4m
  slot=main [INV] hist(4m): `B R2 U F'`
_(turn 18: 595 in / 92 out / 19,249 cached, ~$-0.0488, 2.5s API)_

- `tool#20` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=1215s, wall=77s]
  → (empty result)
_(turn 19: 613 in / 129 out / 19,282 cached, ~$-0.0483, 4.1s API)_

**Turn 19 narration**:

UD-inverse also has no DR options at depth 5! This is a difficult scramble. All three axes I've checked are struggling with DR. Let me try using the brain iteratively on the UD-inverse path since it had the 3 pairs signal.

- `tool#21` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=1219s, wall=81s]
  → found=0
_(turn 20: 783 in / 88 out / 19,739 cached, ~$-0.0496, 2.5s API)_

**Turn 20 narration**:

Brain suggests U (42%). Let me try that and re-check.

- `tool#22` **apply_moves**({"slot":"main","moves":["U"]}) [sim=1219s, wall=83s]
  → hist=5m
  slot=main [INV] hist(5m): `B R2 U F' U`
_(turn 21: 460 in / 92 out / 19,884 cached, ~$-0.0509, 1.7s API)_

- `tool#23` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=1435s, wall=87s]
  → (empty result)
_(turn 22: 619 in / 101 out / 20,485 cached, ~$-0.0519, 3.3s API)_

**Turn 22 narration**:

Still nothing. This is concerning — I'm now 5 moves deep with no clear DR path. Let me try one more brain iteration.

- `tool#24` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=1439s, wall=90s]
  → found=0
_(turn 23: 753 in / 85 out / 20,760 cached, ~$-0.0525, 2.8s API)_

**Turn 23 narration**:

Very strong D signal (93%). Let me apply it.

- `tool#25` **apply_moves**({"slot":"main","moves":["D"]}) [sim=1439s, wall=93s]
  → hist=6m
  slot=main [INV] hist(6m): `B R2 U F' U D`
_(turn 24: 430 in / 92 out / 20,828 cached, ~$-0.0536, 6.0s API)_

- `tool#26` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=1604s, wall=101s]
  → (empty result)
_(turn 25: 1,074 in / 383 out / 21,401 cached, ~$-0.0488, 9.3s API)_

**Turn 25 narration**:

**Breakthrough!** Found DR options after the D move. Comparing the candidates:

1. **DR-3C2E (R U R')**: 5+3=8 total, non-JZP → post-DR ~6-8 moves → total ~14-16 from current state
2. **DR-2C4E (R F2 R)**: 5+3=8 total, **JZP** → post-DR ~5-7 moves → total ~13-15 
3. **DR-4C4E (R or R')**: 5+1=6 total, **JZP** → post-DR ~7-9 moves → total ~13-15

The 4C4E option reaches DR in only **6 moves from here** and is JZP-eligible. Even though 4C4E typically has longer finishes, JZP halves that cost. Total projection: 4 EO + 6 RZP + 6 DR + ~8 finish ≈ **24-26 moves**.

**Decision**: Take the **DR-4C4E (R)** option with JZP. Setup: `R2 L' U' L' B2`, trigger: `R`.

- `tool#27` **apply_moves**({"slot":"main","moves":["R2","L'","U'","L'","B2","R"]}) [sim=1604s, wall=110s]
  → hist=12m
  slot=main [INV] hist(12m): `B R2 U F' U D R2 L' U' L' B2 R`
_(turn 26: 1,394 in / 109 out / 21,673 cached, ~$-0.0527, 3.4s API)_

**Turn 26 narration**:

Excellent! I'm now at DR on the UD-inverse axis. Total so far: 4 EO + 2 brain-guided + 6 DR = **12 moves**. Now let me classify the HTR subset and finish.

- `tool#28` **quick_check**({"slot":"main"}) [sim=1604s, wall=114s]
  → (empty result)
_(turn 27: 693 in / 88 out / 21,744 cached, ~$-0.0553, 2.4s API)_

**Turn 27 narration**:

Confirmed DR on UD. Let me classify the HTR subset.

- `tool#29` **htr_classify**({"slot":"main","axis":"UD"}) [sim=1605s, wall=116s]
  → subset=[2, 0, 3, 6, 1, 4, 5, 7]
_(turn 28: 563 in / 186 out / 23,056 cached, ~$-0.0578, 4.0s API)_

**Turn 28 narration**:

**HTR subset: 2-swap long-cycle**. HTR reduction = 11 moves, finish = 8 moves, total = **19 moves from DR**. 

Total projection: 12 (to DR) + 19 (HTR+finish) = **31 moves**. That matches the prior best attempt! Let me apply the HTR phases and check for any opportunistic shortcuts.

- `tool#30` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=1606s, wall=121s]
  → (empty result)
_(turn 29: 630 in / 84 out / 23,256 cached, ~$-0.0596, 1.9s API)_

- `tool#31` **apply_moves**({"slot":"main","moves":["U","R2","U'","R2"]}) [sim=1607s, wall=123s]
  → hist=16m
  slot=main [INV] hist(16m): `B R2 U F' U D R2 L' U' L' B2 R U R2 U' R2`
_(turn 30: 475 in / 53 out / 23,467 cached, ~$-0.0611, 1.6s API)_

- `tool#32` **quick_check**({"slot":"main"}) [sim=1607s, wall=125s]
  → (empty result)
_(turn 31: 350 in / 94 out / 23,909 cached, ~$-0.0621, 2.1s API)_

- `tool#33` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=1608s, wall=127s]
  → (empty result)
_(turn 32: 367 in / 84 out / 24,026 cached, ~$-0.0625, 1.9s API)_

- `tool#34` **apply_moves**({"slot":"main","moves":["U","R2","U'","R2"]}) [sim=1608s, wall=129s]
  → hist=20m
  slot=main [INV] hist(20m): `B R2 U F' U D R2 L' U' L' B2 R U R2 U' R2 U R2 U' R2`
_(turn 33: 395 in / 53 out / 24,216 cached, ~$-0.0634, 1.4s API)_

- `tool#35` **quick_check**({"slot":"main"}) [sim=1608s, wall=130s]
  → (empty result)
_(turn 34: 362 in / 94 out / 24,392 cached, ~$-0.0634, 1.6s API)_

- `tool#36` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=1609s, wall=132s]
  → (empty result)
_(turn 35: 327 in / 79 out / 24,600 cached, ~$-0.0643, 1.6s API)_

- `tool#37` **apply_moves**({"slot":"main","moves":["U","B2","D"]}) [sim=1609s, wall=133s]
  → hist=23m
  slot=main [INV] hist(23m): `B R2 U F' U D R2 L' U' L' B2 R U R2 U' R2 U R2 U' R2 U B2 D`
_(turn 36: 360 in / 53 out / 24,805 cached, ~$-0.0651, 1.4s API)_

- `tool#38` **quick_check**({"slot":"main"}) [sim=1609s, wall=135s]
  → (empty result)
_(turn 37: 364 in / 122 out / 24,981 cached, ~$-0.0645, 4.8s API)_

**Turn 37 narration**:

Great! Now at HTR (is_htr_ud: true). 23 moves so far. Let me apply the finish phase.

- `tool#39` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=1610s, wall=139s]
  → (empty result)
_(turn 38: 384 in / 85 out / 25,152 cached, ~$-0.0655, 1.8s API)_

- `tool#40` **apply_moves**({"slot":"main","moves":["U2","R2","F2","L2"]}) [sim=1611s, wall=141s]
  → hist=27m
  slot=main [INV] hist(27m): `B R2 U F' U D R2 L' U' L' B2 R U R2 U' R2 U R2 U' R2 U B2 D U2 R2 F2 L2`
_(turn 39: 439 in / 53 out / 25,362 cached, ~$-0.0664, 1.6s API)_

- `tool#41` **quick_check**({"slot":"main"}) [sim=1611s, wall=143s]
  → (empty result)
_(turn 40: 383 in / 91 out / 25,657 cached, ~$-0.0668, 2.0s API)_

- `tool#42` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=1612s, wall=145s]
  → (empty result)
_(turn 41: 318 in / 85 out / 25,769 cached, ~$-0.0673, 1.7s API)_

- `tool#43` **apply_moves**({"slot":"main","moves":["U2","B2","U2","F2"]}) [sim=1612s, wall=146s]
  → hist=31m
  slot=main [INV] hist(31m): `B R2 U F' U D R2 L' U' L' B2 R U R2 U' R2 U R2 U' R2 U B2 D U2 R2 F2 L2 U2 B2 U2 F2`
_(turn 42: 389 in / 53 out / 26,001 cached, ~$-0.0682, 1.6s API)_

- `tool#44` **quick_check**({"slot":"main"}) [sim=1612s, wall=148s]
  → SOLVED
_(turn 43: 396 in / 101 out / 26,177 cached, ~$-0.0680, 3.3s API)_

**Turn 43 narration**:

**Solved!** 31 moves on the inverse side. Now I need to compose the final solution using compose_niss_solution, which will invert the inverse-side moves and verify the solve.

- `tool#45` **compose_niss_solution**({"slot":"main"}) [sim=1613s, wall=151s]
  → solves=True
_(turn 44: 452 in / 107 out / 26,345 cached, ~$-0.0682, 3.6s API)_

**Turn 44 narration**:

Perfect! The solution is **31 moves**, matching the prior best attempt. The solution has been verified by compose_niss_solution.

Let me check the gates for replace_and_shorten: total_moves ≥ 27 ✓ (31 moves). Let me check my tool call budget.

- `tool#46` **budget_status**({}) [sim=1613s, wall=155s]
  → sim=1613s
_(turn 45: 589 in / 236 out / 26,593 cached, ~$-0.0665, 6.5s API)_

**Turn 45 narration**:

I have 1987s remaining (plenty of budget). I'm at 31 moves, which meets the ≥27 gate. However, the prior attempt ALSO reached 31 moves, and the instruction says to "COMMIT HARD" and get a complete solution rather than chasing optimization mid-solve.

Since I have a verified 31-move solution (matching the prior best), I should try replace_and_shorten ONCE to see if I can improve. The tool has a 1-call cap and gates are met. Let me try shortening a large tail span.

- `tool#47` **replace_and_shorten**({"slot":"main","axis":"UD","start":4,"end":31}) [sim=1643s, wall=163s]
  → (empty result)
_(turn 46: 921 in / 138 out / 26,867 cached, ~$-0.0677, 4.8s API)_

**Turn 46 narration**:

**Excellent!** Replace-and-shorten found a 5-move improvement! The new solution is **26 moves** and solves the scramble. This is better than both prior attempts (34 and 31).

Let me update the slot with the new history and compose the final solution.

- `tool#48` **reset_slot**({"slot":"main","rescramble":true}) [sim=1668s, wall=168s]
  → (empty result)
_(turn 47: 774 in / 54 out / 27,178 cached, ~$-0.0702, 2.2s API)_

- `tool#49` **niss_flip**({"slot":"main"}) [sim=1670s, wall=170s]
  → (empty result)
_(turn 48: 592 in / 167 out / 27,621 cached, ~$-0.0703, 2.5s API)_

- `tool#50` **apply_moves**({"slot":"main","moves":["B","R2","U","F'","U2","L2","U2","F2","R2","U2","F2","B2","U'","R2","U2","B2","U'","R2","F2",...) [sim=1673s, wall=172s]
  → hist=26m
  slot=main [INV] hist(26m): `B R2 U F' U2 L2 U2 F2 R2 U2 F2 B2 U' R2 U2 B2 U' R2 F2 U' R' D R D R B2`
_(turn 49: 736 in / 56 out / 28,161 cached, ~$-0.0730, 2.8s API)_

- `tool#51` **compose_niss_solution**({"slot":"main"}) [sim=1674s, wall=175s]
  → solves=True
_(turn 50: 519 in / 160 out / 28,194 cached, ~$-0.0722, 2.8s API)_

**Turn 50 narration**:

Perfect! Let me verify this solution.

- `tool#52` **verify_solved**({"solution":["B2","R'","D'","R'","D'","R","U","F2","R2","U","B2","U2","R2","U","B2","F2","U2","R2","F2","U2","L2","U2...) [sim=1674s, wall=178s]
  → solves=True, moves=26
_(turn 51: 391 in / 420 out / 28,651 cached, ~$-0.0699, 11.6s API)_

**Turn 51 narration**:

Excellent! **26 moves verified**. This is a 5-move improvement over the prior best (31 moves) and 8 moves better than the first attempt (34 moves).

## Solution Summary

**Route taken**: UD-axis on inverse (NISS)
- **EO**: 4 moves (`B R2 U F'` on inverse)
- **DR setup**: 2 brain-guided moves (`U D`) + 6 DR moves (`R2 L' U' L' B2 R`) = **12 moves to DR**
- **DR substate**: DR-4C4E with JZP eligibility  
- **HTR+finish**: 11 moves HTR reduction + 8 moves finish = **19 moves**
- **Initial solve**: 31 moves
- **After replace_and_shorten**: **26 moves** (5-move savings)

The key decisions:
1. Checked multiple EO axes on both normal and inverse sides
2. Followed the strong 3-pairs signal on UD-inverse
3. Used brain-guided DR exploration when trigger_options returned nothing
4. Picked the JZP-eligible DR-4C4E despite longer DR length (saved post-DR moves)
5. Applied replace_and_shorten on the tail span (saved 5 moves)

**FINAL_SOLUTION**: ["B2", "R'", "D'", "R'", "D'", "R", "U", "F2", "R2", "U", "B2", "U2", "R2", "U", "B2", "F2", "U2", "R2", "F2", "U2", "L2", "U2", "F", "U'", "R2", "B'"]

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 52: 16,505 in / 271 out / 12,976 cached, ~$0.0185, 5.3s API)_

### Turn 52 — thinking

> The user is right - I verified the solution and summarized it, but I never actually emitted the FINAL_SOLUTION in the required format. I need to output it now.
> 
> The verified solution is:
> ["B2", "R'", "D'", "R'", "D'", "R", "U", "F2", "R2", "U", "B2", "U2", "R2", "U", "B2", "F2", "U2", "R2", "F2", "U2", "L2", "U2", "F", "U'", "R2", "B'"]
> 
> 26 moves, verified by verify_solved.

**Turn 52 narration**:

FINAL_SOLUTION: ["B2", "R'", "D'", "R'", "D'", "R", "U", "F2", "R2", "U", "B2", "U2", "R2", "U", "B2", "F2", "U2", "R2", "F2", "U2", "L2", "U2", "F", "U'", "R2", "B'"]


**verify_solved** ✓ — 26 moves: `B2 R' D' R' D' R U F2 R2 U B2 U2 R2 U B2 F2 U2 R2 F2 U2 L2 U2 F U' R2 B'`
