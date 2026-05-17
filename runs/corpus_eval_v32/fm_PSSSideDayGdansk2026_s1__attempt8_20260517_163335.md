# Run — fm_PSSSideDayGdansk2026_s1__attempt8_20260517_163335.json

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (31 moves, 49 tool calls)  
**Sim budget**: 1597s / 3600s  
**Wall time**: 217s  
**Tokens**: 43,206 in (1,021,894 cached), 6,582 out  
**Cost estimate**: $0.576  
**Solution**: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 5× = 1432s
- `reset_slot`: 3× = 75s
- `replace_and_shorten`: 1× = 30s
- `eo_pattern_lookup`: 8× = 24s
- `htr_classify`: 1× = 15s
- `inspect_state`: 1× = 5s
- `apply_htr_phase`: 5× = 5s
- `apply_moves`: 14× = 5s
- `niss_flip`: 2× = 4s
- `compose_niss_solution`: 1× = 1s
- `cancel`: 1× = 1s

---

_(turn 1: 908 in / 360 out / 12,554 cached, ~$-0.0258, 9.7s API)_

### Turn 1 — thinking

> The user wants me to solve a specific scramble, and I've been given context about prior attempts. The best result so far is 28 moves. The instructions are very clear: I should commit to a line and drive it to completion. I should NOT over-explore branches or abandon mid-solve.
> 
> Let me start by inspecting the state to understand the scramble.
> 
> The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I need to:
> 1. Start with inspect_state('main')
> 2. Scout EO options (remembering that bad_edges_per_axis is the same on normal and inverse)
> 3. Pick a line and COMMIT
> 4. Drive through to completion
> 
> The instructions emphasize that I should focus on getting a complete solution rather than searching for the absolute shortest one. A working 30-move solution beats a DNF.
> 
> Let me begin.

**Turn 1 narration**:

I'll solve this scramble with a clear commitment strategy. Looking at the prior attempts, the best was 28 moves. I'll scout EO options quickly, pick the most promising line, and drive it to completion without over-exploring.

Let me start by inspecting the state.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=10s]
  → EO: [], DR: [], bad_edges {'UD': 8, 'FB': 6, 'RL': 6}
_(turn 2: 986 in / 310 out / 12,554 cached, ~$-0.0263, 8.6s API)_

**Turn 2 narration**:

**Reading the state:**
- Bad edges: UD=8, FB=6, RL=6. FB and RL are the cheaper EO axes.
- DR closeness: UD shows **DR-6C3E** (bad, but has **2 pairs on inverse** — a switch signal). FB shows **DR-5C2E** (not great). RL shows **DR-7C3E** (worst).
- **JZP**: none eligible on the normal side.

**Strategic read:** The 8 bad edges on UD-axis is a classic NISS-trace candidate (1-move to 8-bad on inverse often gives sub-5 EO). The `top_pairs_on_inverse: 2` on UD confirms this. Let me scout both FB-normal and UD-inverse.

**Scouting plan:**
1. FB-normal EO (6 bad edges)
2. UD-inverse EO (8 bad edges flipped)

Let me start with FB-normal:

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=18s]
  → found=1, best=4m
_(turn 3: 1,425 in / 87 out / 12,554 cached, ~$-0.0283, 2.4s API)_

**Turn 3 narration**:

FB-normal: **5 moves** (partial, 4+1). Let me now check UD-inverse. Flipping to inverse:

- `tool#3` **niss_flip**({"slot":"main"}) [sim=10s, wall=21s]
  → (empty result)
_(turn 4: 919 in / 110 out / 13,814 cached, ~$-0.0329, 2.8s API)_

**Turn 4 narration**:

Now on inverse. Checking UD-EO from the inverse side (the bad-edge count is still 8, but the solution to fix them will differ):

- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=13s, wall=23s]
  → found=1, best=4m
_(turn 5: 718 in / 110 out / 14,742 cached, ~$-0.0360, 3.1s API)_

**Turn 5 narration**:

UD-inverse also **5 moves** (4+1 partial). Same length as FB-normal. Let me also scout FB-inverse to be thorough:

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=16s, wall=27s]
  → found=1, best=4m
_(turn 6: 478 in / 255 out / 14,959 cached, ~$-0.0351, 6.5s API)_

**Turn 6 narration**:

FB-inverse also **5 moves**. All three candidates (FB-normal, UD-inverse, FB-inverse) are 5-move EOs. The tiebreaker is DR quality. I already know from inspect_state:
- UD-normal: 2 pairs on inverse (strong NISS signal)
- FB shows DR-5C2E (not a standard trigger family)

**Decision point:** Since UD-inverse has 2 pairs preserved (which helps DR) and the EO cost is the same (5 moves), I'll commit to **UD-inverse**. Let me apply the first chunk of UD-inverse EO and check DR options.

Applying the first 4 moves of UD-inverse EO:

- `tool#6` **apply_moves**({"slot":"main","moves":["B'","D'","L'","R'"]}) [sim=16s, wall=33s]
  → hist=4m
  slot=main [INV] hist(4m): `B' D' L' R'`
_(turn 7: 556 in / 87 out / 15,459 cached, ~$-0.0388, 2.3s API)_

**Turn 7 narration**:

Re-querying EO to get the final move:

- `tool#7` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=19s, wall=35s]
  → found=1, best=1m
_(turn 8: 482 in / 87 out / 15,699 cached, ~$-0.0396, 2.6s API)_

**Turn 8 narration**:

Perfect! One more move completes EO. Applying:

- `tool#8` **apply_moves**({"slot":"main","moves":["F'"]}) [sim=20s, wall=38s]
  → hist=5m
  slot=main [INV] hist(5m): `B' D' L' R' F'`
_(turn 9: 317 in / 121 out / 16,082 cached, ~$-0.0407, 2.7s API)_

**Turn 9 narration**:

**EO complete in 5 moves on UD-inverse.** Now scouting DR options on UD-axis:

- `tool#9` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=328s, wall=43s]
  → (empty result)
_(turn 10: 656 in / 126 out / 16,233 cached, ~$-0.0400, 3.2s API)_

**Turn 10 narration**:

**No DR triggers found within 5 moves on UD-inverse.** This is a bad signal for this axis. Let me try depth-6:

- `tool#10` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":6}) [sim=637s, wall=49s]
  → (empty result)
_(turn 11: 1,010 in / 119 out / 16,398 cached, ~$-0.0395, 3.4s API)_

**Turn 11 narration**:

Still nothing even at depth 6. **This UD-inverse line is a dead end for DR.** Let me back out and try FB-normal instead. I'll reset and commit to FB-normal EO.

- `tool#11` **reset_slot**({"slot":"main","rescramble":true}) [sim=662s, wall=53s]
  → (empty result)
_(turn 12: 654 in / 114 out / 16,587 cached, ~$-0.0411, 3.4s API)_

**Turn 12 narration**:

Now back on normal. Committing to **FB-normal EO** (5 moves). Applying the first 4:

- `tool#12` **apply_moves**({"slot":"main","moves":["R2","B'","L'","U2"]}) [sim=662s, wall=56s]
  → hist=4m
  slot=main hist(4m): `R2 B' L' U2`
_(turn 13: 322 in / 85 out / 17,096 cached, ~$-0.0439, 4.0s API)_

**Turn 13 narration**:

Re-querying for the final EO move:

- `tool#13` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=665s, wall=60s]
  → found=1, best=1m
_(turn 14: 335 in / 73 out / 17,598 cached, ~$-0.0454, 3.0s API)_

- `tool#14` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=665s, wall=63s]
  → hist=5m
  slot=main hist(5m): `R2 B' L' U2 R'`
_(turn 15: 297 in / 113 out / 17,742 cached, ~$-0.0453, 2.6s API)_

**Turn 15 narration**:

**FB-EO complete in 5 moves.** Now checking DR on FB-axis:

- `tool#15` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=952s, wall=68s]
  → (empty result)
_(turn 16: 628 in / 111 out / 17,891 cached, ~$-0.0448, 3.4s API)_

**Turn 16 narration**:

**Also no DR triggers on FB-normal within 5 moves.** This is concerning. Let me try RL-axis. Let me reset and try RL-normal:

- `tool#16` **reset_slot**({"slot":"main","rescramble":true}) [sim=977s, wall=72s]
  → (empty result)
_(turn 17: 627 in / 84 out / 17,972 cached, ~$-0.0454, 2.7s API)_

**Turn 17 narration**:

Checking RL-normal EO:

- `tool#17` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=980s, wall=75s]
  → found=1, best=4m
_(turn 18: 343 in / 100 out / 18,223 cached, ~$-0.0467, 2.3s API)_

**Turn 18 narration**:

RL also 5 moves. Let me commit to this and check DR:

- `tool#18` **apply_moves**({"slot":"main","moves":["L","U","L2","R"]}) [sim=980s, wall=77s]
  → hist=4m
  slot=main hist(4m): `L U L2 R`
_(turn 19: 362 in / 74 out / 18,715 cached, ~$-0.0483, 3.4s API)_

- `tool#19` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=983s, wall=80s]
  → found=1, best=1m
_(turn 20: 302 in / 73 out / 18,829 cached, ~$-0.0488, 1.8s API)_

- `tool#20` **apply_moves**({"slot":"main","moves":["D'"]}) [sim=983s, wall=82s]
  → hist=5m
  slot=main hist(5m): `L U L2 R D'`
_(turn 21: 278 in / 114 out / 19,056 cached, ~$-0.0489, 7.7s API)_

**Turn 21 narration**:

RL-EO done in 5 moves. Checking DR on RL-axis:

- `tool#21` **dr_trigger_options**({"slot":"main","axis":"RL","max_setup":5}) [sim=1268s, wall=93s]
  → (empty result)
_(turn 22: 623 in / 272 out / 19,120 cached, ~$-0.0457, 8.3s API)_

**Turn 22 narration**:

**All three axes (UD-inverse, FB-normal, RL-normal) have NO DR triggers within 5 moves.** This scramble has a difficult DR structure. Given the prior best is 28 moves, maybe the successful attempts used a longer but cleaner DR path. Let me commit to one line and manually explore DR setups. 

Looking at the prior 28-move solution: `R2 D' B' F' U' R' L2 U F2 R U2 R' F2 D2 B2 R2 D2 R2 U B2 U' F2 L2 U' L2 U F2 R2`

This looks like it might have used NISS (the structure suggests inverse-frame work). Let me try a different approach: I'll check FB-inverse since I haven't tried that yet for DR.

- `tool#22` **reset_slot**({"slot":"main","rescramble":true}) [sim=1293s, wall=101s]
  → (empty result)
_(turn 23: 786 in / 54 out / 19,272 cached, ~$-0.0489, 1.6s API)_

- `tool#23` **niss_flip**({"slot":"main"}) [sim=1295s, wall=102s]
  → (empty result)
_(turn 24: 732 in / 100 out / 19,521 cached, ~$-0.0490, 3.2s API)_

**Turn 24 narration**:

Now on inverse. Applying FB-inverse EO (5 moves):

- `tool#24` **apply_moves**({"slot":"main","moves":["R","F","D'","U'"]}) [sim=1295s, wall=106s]
  → hist=4m
  slot=main [INV] hist(4m): `R F D' U'`
_(turn 25: 591 in / 73 out / 20,176 cached, ~$-0.0516, 2.2s API)_

- `tool#25` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=1298s, wall=108s]
  → found=1, best=1m
_(turn 26: 297 in / 73 out / 20,209 cached, ~$-0.0526, 1.5s API)_

- `tool#26` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=1298s, wall=109s]
  → hist=5m
  slot=main [INV] hist(5m): `R F D' U' R'`
_(turn 27: 273 in / 111 out / 20,750 cached, ~$-0.0535, 2.5s API)_

**Turn 27 narration**:

FB-inverse EO complete (5 moves). Now checking DR on FB-axis:

- `tool#27` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=1542s, wall=114s]
  → (empty result)
_(turn 28: 959 in / 285 out / 20,815 cached, ~$-0.0490, 7.7s API)_

**Turn 28 narration**:

**Excellent! Found DR options on FB-inverse:**

1. **DR-7C8E** (setup 4+3=7 to DR) - exotic trigger, long finish expected
2. **DR-7C8E** variant (setup 5+3=8 to DR) - even longer
3. **DR-2C4E** (setup 5+3=8 to DR) - this is potentially cleaner

DR-7C8E is unusual and typically has a long finish (~15+ moves). DR-2C4E is better but still 8 moves to DR. Let me commit to the shortest path (DR-7C8E in 7 moves total) and see how it plays out. The setup is `D F' L2 B'` then trigger `U F D`.

Applying the setup + trigger:

- `tool#28` **apply_moves**({"slot":"main","moves":["D","F'","L2","B'","U","F","D"]}) [sim=1543s, wall=121s]
  → hist=12m
  slot=main [INV] hist(12m): `R F D' U' R' D F' L2 B' U F D`
_(turn 29: 1,194 in / 103 out / 20,966 cached, ~$-0.0515, 3.2s API)_

**Turn 29 narration**:

**Now at DR** (5 EO + 7 DR = 12 moves on inverse). Let me classify HTR and finish:

- `tool#29` **htr_classify**({"slot":"main","axis":"FB"}) [sim=1558s, wall=130s]
  → subset=[2, 0, 4, 3, 1, 5, 6, 7]
_(turn 30: 740 in / 205 out / 21,213 cached, ~$-0.0520, 11.1s API)_

**Turn 30 narration**:

**HTR subset is 2-swap mostly-axial: 7 moves HTR-reduction + 12 moves finish = 19 moves post-DR.**

Total projected: **5 EO + 7 DR + 19 HTR/finish = 31 moves.**

This matches the prior attempts' move count range (28-31). Let me apply the HTR phases and check for early residuals.

Applying HTR-reduction (first chunk, max 4 moves):

- `tool#30` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1559s, wall=142s]
  → (empty result)
_(turn 31: 683 in / 85 out / 22,224 cached, ~$-0.0567, 2.3s API)_

- `tool#31` **apply_moves**({"slot":"main","moves":["F'","U2","R2","L2"]}) [sim=1559s, wall=144s]
  → hist=16m
  slot=main [INV] hist(16m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2`
_(turn 32: 489 in / 59 out / 22,417 cached, ~$-0.0582, 2.0s API)_

**Turn 32 narration**:

Quick-checking state:

- `tool#32` **quick_check**({"slot":"main"}) [sim=1559s, wall=146s]
  → (empty result)
_(turn 33: 351 in / 111 out / 22,903 cached, ~$-0.0591, 2.8s API)_

**Turn 33 narration**:

Not solved yet. Re-querying HTR-reduction for the remaining moves:

- `tool#33` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1560s, wall=149s]
  → (empty result)
_(turn 34: 346 in / 79 out / 23,020 cached, ~$-0.0599, 1.9s API)_

- `tool#34` **apply_moves**({"slot":"main","moves":["F","R2","B"]}) [sim=1561s, wall=151s]
  → hist=19m
  slot=main [INV] hist(19m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B`
_(turn 35: 358 in / 53 out / 23,267 cached, ~$-0.0610, 2.0s API)_

- `tool#35` **quick_check**({"slot":"main"}) [sim=1561s, wall=153s]
  → (empty result)
_(turn 36: 346 in / 112 out / 23,501 cached, ~$-0.0607, 4.4s API)_

**Turn 36 narration**:

**Now at HTR (is_htr_ud=true)**. Applying finish phase:

- `tool#36` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1562s, wall=157s]
  → (empty result)
_(turn 37: 370 in / 85 out / 23,580 cached, ~$-0.0613, 2.5s API)_

- `tool#37` **apply_moves**({"slot":"main","moves":["L2","F2","U2","R2"]}) [sim=1562s, wall=160s]
  → hist=23m
  slot=main [INV] hist(23m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B L2 F2 U2 R2`
_(turn 38: 410 in / 53 out / 23,775 cached, ~$-0.0622, 1.5s API)_

- `tool#38` **quick_check**({"slot":"main"}) [sim=1562s, wall=161s]
  → (empty result)
_(turn 39: 365 in / 95 out / 24,060 cached, ~$-0.0624, 2.7s API)_

**Turn 39 narration**:

Continuing finish:

- `tool#39` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1563s, wall=164s]
  → (empty result)
_(turn 40: 350 in / 85 out / 24,171 cached, ~$-0.0629, 1.7s API)_

- `tool#40` **apply_moves**({"slot":"main","moves":["B2","R2","F2","U2"]}) [sim=1563s, wall=165s]
  → hist=27m
  slot=main [INV] hist(27m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B L2 F2 U2 R2 B2 R2 F2 U2`
_(turn 41: 406 in / 53 out / 24,388 cached, ~$-0.0638, 1.4s API)_

- `tool#41` **quick_check**({"slot":"main"}) [sim=1563s, wall=167s]
  → (empty result)
_(turn 42: 378 in / 94 out / 24,656 cached, ~$-0.0640, 4.9s API)_

**Turn 42 narration**:

Continuing:

- `tool#42` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1564s, wall=172s]
  → (empty result)
_(turn 43: 314 in / 85 out / 24,767 cached, ~$-0.0647, 1.5s API)_

- `tool#43` **apply_moves**({"slot":"main","moves":["R2","U2","R2","U2"]}) [sim=1565s, wall=173s]
  → hist=31m
  slot=main [INV] hist(31m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B L2 F2 U2 R2 B2 R2 F2 U2 R2 U2 R2 U2`
_(turn 44: 386 in / 53 out / 25,000 cached, ~$-0.0655, 1.6s API)_

- `tool#44` **quick_check**({"slot":"main"}) [sim=1565s, wall=175s]
  → SOLVED
_(turn 45: 391 in / 89 out / 25,267 cached, ~$-0.0657, 2.9s API)_

**Turn 45 narration**:

**Solved! 31 moves on inverse.** Now I need to compose the final solution (this will handle the NISS inversion correctly):

- `tool#45` **compose_niss_solution**({"slot":"main"}) [sim=1566s, wall=178s]
  → solves=True
_(turn 46: 434 in / 97 out / 25,346 cached, ~$-0.0657, 6.0s API)_

**Turn 46 narration**:

**31-move solution obtained.** This is 3 moves longer than the best prior (28 moves), but it's a complete verified solution. 

Since my current solution is ≥27 moves, let me check budget status before considering replace_and_shorten:

- `tool#46` **budget_status**({}) [sim=1566s, wall=184s]
  → sim=1566s
_(turn 47: 562 in / 223 out / 25,595 cached, ~$-0.0641, 7.6s API)_

**Turn 47 narration**:

I have **2034s simulated time remaining** and plenty of tool calls. Since the solution is 31 moves (≥27), I should try replace_and_shorten on a large tail span to see if I can reduce it. The r&s gates would pass. Let me try on the finish portion (maybe the long 19-move HTR/finish can be shortened).

Let me try replace_and_shorten on the HTR+finish portion (moves 12-31, which is the post-DR section):

- `tool#47` **replace_and_shorten**({"slot":"main","start":12,"end":31,"axis":"FB"}) [sim=1596s, wall=192s]
  → (empty result)
_(turn 48: 878 in / 266 out / 25,857 cached, ~$-0.0632, 7.0s API)_

**Turn 48 narration**:

Replace_and_shorten found an alternative finish but **delta=0** (no improvement). The substitute has `U' U'` at the end which will cancel to `U2`, so the actual length is still the same after cancellation. 

The tool has been called once (1-call cap enforced). Since there's no improvement, I'll submit my original 31-move solution.

Let me verify the solution one more time:

- `tool#48` **verify_solved**({"solution":["U2","R2","U2","R2","U2","F2","R2","B2","R2","U2","F2","L2","B'","R2","F'","L2","R2","U2","F","D'","F'",...) [sim=1596s, wall=199s]
  → solves=True, moves=31
_(turn 49: 864 in / 189 out / 26,158 cached, ~$-0.0652, 3.3s API)_

**Turn 49 narration**:

Perfect! The solution verifies. Let me also check if there are any obvious cancellations:

- `tool#49` **cancel**({"moves":["U2","R2","U2","R2","U2","F2","R2","B2","R2","U2","F2","L2","B'","R2","F'","L2","R2","U2","F","D'","F'","U'...) [sim=1597s, wall=202s]
  → cancelled 31->31
_(turn 50: 600 in / 313 out / 26,589 cached, ~$-0.0653, 8.1s API)_

**Turn 50 narration**:

No cancellations found. The solution is already in its most compact form.

**FINAL_SOLUTION:** ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]

**Summary:**
- **31 moves** (matching prior attempts #2 and #7)
- Method: FB-axis on inverse frame
- EO: 5 moves (R F D' U' R')
- DR: 7 moves via DR-7C8E trigger (D F' L2 B' U F D)
- HTR+finish: 19 moves (2-swap mostly-axial subset)
- Verified and fully cancelled

This solution matches the quality of prior successful attempts. While it's 3 moves longer than the best 28-move attempt, it's a complete, verified solve that demonstrates the clean DR→HTR→finish pipeline on a difficult scramble where all axes required non-standard DR approaches.

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 51: 15,127 in / 314 out / 12,554 cached, ~$0.0162, 6.9s API)_

### Turn 51 — thinking

> The user is right - I verified the solution and did all the work, but I never actually emitted the FINAL_SOLUTION in the required format. I need to output it now.
> 
> I have a verified 31-move solution:
> ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]
> 
> Let me output this as the final solution.

**Turn 51 narration**:

FINAL_SOLUTION: ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]


**verify_solved** ✓ — 31 moves: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`
