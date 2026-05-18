# Run — fm_PSSSideDayGdansk2026_s3__attempt6_20260518_003139.json

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (34 moves, 54 tool calls)  
**Sim budget**: 1874s / 3600s  
**Wall time**: 200s  
**Tokens**: 49,385 in (895,273 cached), 6,480 out  
**Cost estimate**: $0.560  
**Solution**: `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2 R2 F2`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 7× = 1792s
- `reset_slot`: 1× = 25s
- `dr_recognize`: 5× = 20s
- `eo_pattern_lookup`: 3× = 9s
- `apply_htr_phase`: 6× = 6s
- `analyze_residual`: 3× = 6s
- `inspect_state`: 1× = 5s
- `apply_moves`: 15× = 5s
- `niss_flip`: 2× = 4s
- `htr_classify`: 1× = 1s
- `compose_niss_solution`: 1× = 1s
- `undo_moves`: 1× = 0s

---

_(turn 1: 757 in / 395 out / 12,986 cached, ~$-0.0269, 9.7s API)_

### Turn 1 — thinking

> Looking at the context:
> - Attempt 1: 34 moves
> - Attempt 2: FAILED (max_tool_calls)
> - Attempt 3: FAILED (max_tool_calls)
> - Attempt 4: 30 moves (BEST)
> - Attempt 5: FAILED (max_tool_calls)
> 
> The instructions are clear: COMMIT HARD. Pick a line and drive it to completion. Don't over-ideate, don't abandon halfway through. The goal is a COMPLETE solution, not necessarily beating 30 moves (though that would be nice).
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Let me start by inspecting the state to see what the bad edges are per axis, then make a quick decision about which axis to pursue based on the bad edge counts and what I can scout quickly.
> 
> The instructions say:
> 1. inspect_state(main) first
> 2. Scout EO on normal side for 1-2 most promising axes
> 3. Scout EO on inverse side too when needed
> 4. For each viable candidate, probe DR cost
> 5. Pick and commit
> 
> Let me start.

**Turn 1 narration**:

I'll solve this scramble with a commitment-first approach. Let me start by inspecting the state to see the bad edge distribution across axes.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=10s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 8, 'RL': 6}
_(turn 2: 1,001 in / 167 out / 12,986 cached, ~$-0.0296, 4.5s API)_

**Turn 2 narration**:

**State observation**: Bad edges = {UD: 4, FB: 8, RL: 6}. UD has the fewest (4 bad edges) and 3 pairs preserved on inverse - that's a strong NISS signal. The 4 bad edges on UD axis are UL, DR, DL, DB. Let me scout EO on UD normal first, then check inverse.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=8s, wall=14s]
  → found=1, best=4m
_(turn 3: 1,255 in / 154 out / 12,986 cached, ~$-0.0290, 3.4s API)_

**Turn 3 narration**:

UD-normal EO = 4 moves. But `top_pairs_on_inverse: 3` is strong - let me check inverse UD-EO too before committing.

- `tool#3` **niss_flip**({"slot":"main"}) [sim=10s, wall=18s]
  → (empty result)
- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=13s, wall=18s]
  → found=1, best=4m
_(turn 4: 958 in / 134 out / 14,130 cached, ~$-0.0333, 3.9s API)_

**Turn 4 narration**:

Inverse UD-EO is also 4 moves. Same length, but with 3 pairs on inverse, the inverse side should give better DR options. Let me commit the inverse-UD EO and probe DR.

- `tool#5` **apply_moves**({"slot":"main","moves":["B'","R'","U","B'"]}) [sim=13s, wall=21s]
  → hist=4m
  slot=main [INV] hist(4m): `B' R' U B'`
_(turn 5: 899 in / 96 out / 14,895 cached, ~$-0.0361, 3.1s API)_

**Turn 5 narration**:

EO committed on inverse-UD (4 moves). Now checking DR trigger options on this axis.

- `tool#6` **dr_trigger_options**({"slot":"main","axis":"UD"}) [sim=321s, wall=28s]
  → (empty result)
_(turn 6: 679 in / 117 out / 15,080 cached, ~$-0.0369, 3.0s API)_

**Turn 6 narration**:

0 DR trigger options found within 5-move setup - that's a bad sign for UD-inverse. Let me fall back to dr_recognize, which will either find a memory pattern or give brain suggestions.

- `tool#7` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=325s, wall=31s]
  → found=0
_(turn 7: 784 in / 178 out / 15,817 cached, ~$-0.0377, 4.7s API)_

**Turn 7 narration**:

Brain suggests B2 (0.8 prob). This is the iterative approach - apply one move, re-check. But this is getting expensive. Let me try the normal side instead - maybe the DR is cleaner there even without pairs. Let me undo these 4 EO moves and flip back to normal.

- `tool#8` **undo_moves**({"slot":"main","n":4}) [sim=326s, wall=35s]
  → hist=0m
- `tool#9` **niss_flip**({"slot":"main"}) [sim=328s, wall=35s]
  → (empty result)
_(turn 8: 977 in / 164 out / 15,976 cached, ~$-0.0377, 3.3s API)_

**Turn 8 narration**:

Back on normal side, back at scramble. Let me commit the normal UD EO and check DR there.

- `tool#10` **apply_moves**({"slot":"main","moves":["U","L","R'","B'"]}) [sim=328s, wall=39s]
  → hist=4m
  slot=main hist(4m): `U L R' B'`
- `tool#11` **dr_trigger_options**({"slot":"main","axis":"UD"}) [sim=560s, wall=41s]
  → (empty result)
_(turn 9: 1,322 in / 103 out / 16,476 cached, ~$-0.0390, 6.0s API)_

**Turn 9 narration**:

Normal-UD also shows 0 trigger options within 5 moves. This is concerning. Let me try FB axis instead - it has 8 bad edges but might have better DR structure. Let me reset and scout FB.

- `tool#12` **reset_slot**({"slot":"main"}) [sim=585s, wall=47s]
  → (empty result)
_(turn 10: 783 in / 110 out / 16,804 cached, ~$-0.0414, 2.8s API)_

**Turn 10 narration**:

Reset complete. Let me try FB axis - 8 bad edges is expensive for EO but the DR structure might be better. Checking FB-normal EO first.

- `tool#13` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=588s, wall=50s]
  → found=1, best=4m
_(turn 11: 331 in / 189 out / 17,443 cached, ~$-0.0433, 3.3s API)_

**Turn 11 narration**:

FB-normal EO = 4 moves! That's excellent for 8 bad edges. Let me commit this and probe DR on FB.

- `tool#14` **apply_moves**({"slot":"main","moves":["R'","F","D","L'"]}) [sim=588s, wall=53s]
  → hist=4m
  slot=main hist(4m): `R' F D L'`
- `tool#15` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=844s, wall=55s]
  → (empty result)
_(turn 12: 869 in / 102 out / 18,087 cached, ~$-0.0447, 2.5s API)_

**Turn 12 narration**:

Also 0 on FB. This scramble seems resistant to the named trigger catalog. Let me use dr_recognize on FB to get brain suggestions.

- `tool#16` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=848s, wall=58s]
  → found=0
_(turn 13: 959 in / 179 out / 18,227 cached, ~$-0.0437, 3.0s API)_

**Turn 13 narration**:

Brain suggests R2 (0.342 prob) for FB. Let me follow the brain iteratively - apply R2, then check again.

- `tool#17` **apply_moves**({"slot":"main","moves":["R2"]}) [sim=849s, wall=61s]
  → hist=5m
  slot=main hist(5m): `R' F D L' R2`
- `tool#18` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=1099s, wall=63s]
  → (empty result)
_(turn 14: 954 in / 93 out / 18,430 cached, ~$-0.0455, 4.7s API)_

**Turn 14 narration**:

Still 0 after R2. Let me try another brain move. Checking dr_recognize again.

- `tool#19` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=1103s, wall=68s]
  → found=0
_(turn 15: 943 in / 169 out / 19,089 cached, ~$-0.0462, 3.0s API)_

**Turn 15 narration**:

Brain now suggests L2 (0.407). Let me apply it and try trigger options again.

- `tool#20` **apply_moves**({"slot":"main","moves":["L2"]}) [sim=1103s, wall=71s]
  → hist=5m
  slot=main hist(5m): `R' F D R2 L`
- `tool#21` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=1349s, wall=73s]
  → (empty result)
_(turn 16: 933 in / 118 out / 19,381 cached, ~$-0.0478, 3.0s API)_

**Turn 16 narration**:

I notice auto_cancelled saved 1 move - L2 + R2 cancelled into R2 L (R' and L' combined). Still no triggers. Let me continue with the brain - one more move.

- `tool#22` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=1353s, wall=76s]
  → found=0
_(turn 17: 955 in / 167 out / 20,035 cached, ~$-0.0487, 2.6s API)_

**Turn 17 narration**:

D2 at 0.816 prob - very confident. Let me apply it.

- `tool#23` **apply_moves**({"slot":"main","moves":["D2"]}) [sim=1353s, wall=79s]
  → hist=6m
  slot=main hist(6m): `R' F D R2 L D2`
- `tool#24` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=1581s, wall=81s]
  → (empty result)
_(turn 18: 958 in / 292 out / 20,317 cached, ~$-0.0476, 8.7s API)_

**Turn 18 narration**:

This is getting long (6 moves deep in RZP) with no DR trigger found. My best prior attempt was 30 moves. Let me try a different approach - maybe I should look at my successful Attempt 4 solution to understand what worked:

Attempt 4: `U B D L U L' F2 U2 L D2 F L2 U2 F R' U2 R U2 R2 F2 L F2 L2 B2 L2 U2 L2 R2 F2 U2`

That's 30 moves. Let me try to replicate part of this line or find a similar structure. Looking at the opening: U B D L - that's 4 moves. Let me check if that's an EO on some axis.

Actually, wait - the instruction says "COMMIT HARD" - pick a line and drive it to completion. Let me continue following the brain on FB. One more move.

- `tool#25` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=1585s, wall=89s]
  → found=0
_(turn 19: 1,130 in / 160 out / 20,995 cached, ~$-0.0509, 3.0s API)_

**Turn 19 narration**:

D at 0.452 prob. Applying it.

- `tool#26` **apply_moves**({"slot":"main","moves":["D"]}) [sim=1585s, wall=92s]
  → hist=6m
  slot=main hist(6m): `R' F D R2 L D'`
- `tool#27` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=1857s, wall=95s]
  → (empty result)
_(turn 20: 1,248 in / 258 out / 21,274 cached, ~$-0.0498, 6.2s API)_

**Turn 20 narration**:

EXCELLENT! Found a DR trigger! DR-4C4E with setup L2 B U' F' B, then trigger U F2 L2 U. Total to DR = 9 moves. Current history is 6 moves, so total EO+DR = 6+9 = 15 moves to DR. That's acceptable (sub-15 is beginner, this is exactly 15).

Pre-trigger signature is DR-4C2E, which means at the pre-trigger state it's 4 corners 2 edges from DR. The final trigger is U F2 L2 U (4 moves). Not JZP but 2 pairs on inverse.

Let me commit this DR path. Applying the setup moves first.

- `tool#28` **apply_moves**({"slot":"main","moves":["L2","B","U'","F'","B"]}) [sim=1858s, wall=101s]
  → hist=11m
  slot=main hist(11m): `R' F D R2 L D' L2 B U' F' B`
_(turn 21: 1,113 in / 106 out / 22,130 cached, ~$-0.0548, 2.4s API)_

**Turn 21 narration**:

Setup committed (11 moves total). Now applying the DR trigger U F2 L2 U.

- `tool#29` **apply_moves**({"slot":"main","moves":["U","F2","L2","U"]}) [sim=1858s, wall=104s]
  → hist=15m
  slot=main hist(15m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U`
_(turn 22: 546 in / 100 out / 22,402 cached, ~$-0.0573, 3.5s API)_

**Turn 22 narration**:

DR reached at 15 moves on FB axis. Now I need to finish via HTR. Let me classify the HTR subset.

- `tool#30` **htr_classify**({"slot":"main","axis":"FB"}) [sim=1859s, wall=108s]
  → subset=[1, 0, 2, 7, 4, 3, 6, 5]
_(turn 23: 576 in / 196 out / 23,348 cached, ~$-0.0584, 5.9s API)_

**Turn 23 narration**:

HTR classified: "2-swap mostly-axial" subset. HTR reduction = 11 moves, finish = 10 moves, total = 21 moves from DR to solved. Combined with my 15-move DR, that's 15 + 21 = 36 moves total.

This is worse than my best attempt (30 moves), but let me complete it and see if there are any opportunities for improvement. Applying HTR reduction phase.

- `tool#31` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1860s, wall=115s]
  → (empty result)
_(turn 24: 677 in / 147 out / 23,541 cached, ~$-0.0593, 2.9s API)_

**Turn 24 narration**:

Partial HTR reduction (4 of 11 moves). Applying this chunk and checking state with quick_check.

- `tool#32` **apply_moves**({"slot":"main","moves":["U2","F'","R2","F"]}) [sim=1860s, wall=118s]
  → hist=18m
  slot=main hist(18m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F`
- `tool#33` **quick_check**({"slot":"main"}) [sim=1860s, wall=118s]
  → (empty result)
_(turn 25: 721 in / 137 out / 23,742 cached, ~$-0.0599, 6.2s API)_

**Turn 25 narration**:

Not solved yet. History is 18 moves (auto-cancel saved 1 move - the U and U' cancelled). Still in DR on FB, not solved. Let me continue HTR reduction.

- `tool#34` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1861s, wall=125s]
  → (empty result)
_(turn 26: 662 in / 136 out / 24,214 cached, ~$-0.0614, 2.2s API)_

**Turn 26 narration**:

Next 4 of HTR reduction. Applying and checking.

- `tool#35` **apply_moves**({"slot":"main","moves":["R2","F'","L2","D2"]}) [sim=1862s, wall=127s]
  → hist=22m
  slot=main hist(22m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2`
- `tool#36` **quick_check**({"slot":"main"}) [sim=1862s, wall=127s]
  → (empty result)
_(turn 27: 668 in / 123 out / 24,438 cached, ~$-0.0621, 4.7s API)_

**Turn 27 narration**:

22 moves, not solved. Continuing HTR reduction (should have 3 more moves left in the 11-move reduction).

- `tool#37` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1863s, wall=132s]
  → (empty result)
_(turn 28: 615 in / 132 out / 24,884 cached, ~$-0.0634, 4.7s API)_

**Turn 28 narration**:

Last 3 moves of HTR reduction. Applying and checking.

- `tool#38` **apply_moves**({"slot":"main","moves":["F'","R2","B"]}) [sim=1863s, wall=136s]
  → hist=25m
  slot=main hist(25m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B`
- `tool#39` **quick_check**({"slot":"main"}) [sim=1863s, wall=136s]
  → (empty result)
_(turn 29: 623 in / 121 out / 25,098 cached, ~$-0.0641, 10.2s API)_

**Turn 29 narration**:

Excellent! At 25 moves, I'm now in HTR (is_htr_ud: true, all axes DR-solved and EO-solved). Now I need to apply the finish phase (10 moves predicted). Let me check if there's a 3-cycle residual before finishing.

- `tool#40` **analyze_residual**({"slot":"main"}) [sim=1865s, wall=146s]
  → (empty result)
_(turn 30: 721 in / 156 out / 25,546 cached, ~$-0.0645, 4.7s API)_

**Turn 30 narration**:

Mixed residual - 6 corners unsolved (two 3-cycles), 9 edges unsolved (4-cycle, 2-cycle, 3-cycle). Not a pure 3-cycle, so can't use derive_corner_3cycle. Let me continue with the finish phase.

- `tool#41` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1866s, wall=151s]
  → (empty result)
_(turn 31: 553 in / 138 out / 25,719 cached, ~$-0.0657, 7.9s API)_

**Turn 31 narration**:

First 4 of 10 finish moves. Applying and checking.

- `tool#42` **apply_moves**({"slot":"main","moves":["B2","U2","L2","U2"]}) [sim=1867s, wall=159s]
  → hist=28m
  slot=main hist(28m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2`
- `tool#43` **quick_check**({"slot":"main"}) [sim=1867s, wall=159s]
  → (empty result)
_(turn 32: 703 in / 92 out / 26,176 cached, ~$-0.0672, 3.2s API)_

**Turn 32 narration**:

28 moves now (B2 and B' cancelled into B'). Not solved yet. Let me check residual to see if we landed on a 3-cycle.

- `tool#44` **analyze_residual**({"slot":"main"}) [sim=1869s, wall=162s]
  → (empty result)
_(turn 33: 717 in / 125 out / 26,511 cached, ~$-0.0676, 2.7s API)_

**Turn 33 narration**:

Still mixed - 6 corners (two 3-cycles), 11 edges (various cycles). Not a pure 3-cycle. Continuing finish.

- `tool#45` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1870s, wall=165s]
  → (empty result)
_(turn 34: 499 in / 134 out / 26,721 cached, ~$-0.0686, 3.2s API)_

**Turn 34 narration**:

Next 4 of finish. Applying and checking.

- `tool#46` **apply_moves**({"slot":"main","moves":["R2","B2","D2","U2"]}) [sim=1870s, wall=168s]
  → hist=32m
  slot=main hist(32m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2`
- `tool#47` **quick_check**({"slot":"main"}) [sim=1870s, wall=168s]
  → (empty result)
_(turn 35: 682 in / 69 out / 27,162 cached, ~$-0.0703, 2.7s API)_

**Turn 35 narration**:

32 moves, not solved. Let me check residual again.

- `tool#48` **analyze_residual**({"slot":"main"}) [sim=1872s, wall=171s]
  → (empty result)
_(turn 36: 688 in / 107 out / 27,474 cached, ~$-0.0705, 2.5s API)_

**Turn 36 narration**:

Still mixed. Continuing with finish (should be 2 more moves).

- `tool#49` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1873s, wall=173s]
  → (empty result)
_(turn 37: 400 in / 127 out / 27,680 cached, ~$-0.0716, 2.2s API)_

**Turn 37 narration**:

Last 2 moves of finish. Applying and checking.

- `tool#50` **apply_moves**({"slot":"main","moves":["R2","F2"]}) [sim=1873s, wall=176s]
  → hist=34m
  slot=main hist(34m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2 R2 F2`
- `tool#51` **quick_check**({"slot":"main"}) [sim=1873s, wall=176s]
  → SOLVED
_(turn 38: 623 in / 106 out / 28,114 cached, ~$-0.0724, 3.3s API)_

**Turn 38 narration**:

SOLVED! 34 moves total. This matches my Attempt 1 (also 34 moves), but is worse than my best Attempt 4 (30 moves). Let me compose the solution and verify it.

- `tool#52` **compose_niss_solution**({"slot":"main"}) [sim=1874s, wall=179s]
  → solves=True
_(turn 39: 768 in / 100 out / 28,392 cached, ~$-0.0729, 3.0s API)_

**Turn 39 narration**:

Solution verified at 34 moves. According to the rules, since this is ≥27 moves and I have plenty of tool calls remaining (only used ~50 tool calls), I should try replace_and_shorten to see if I can reduce it. Let me check budget status first.

- `tool#53` **budget_status**({}) [sim=1874s, wall=182s]
  → sim=1874s
_(turn 40: 625 in / 167 out / 28,551 cached, ~$-0.0727, 4.1s API)_

**Turn 40 narration**:

I have 1725s of sim time remaining and plenty of wall time. Let me try replace_and_shorten on a large tail section. I'll try from move 4 to the end (34), which is 30 moves - a large chunk to potentially optimize.

- `tool#54` **replace_and_shorten**({"slot":"main","start":4,"end":34,"axis":"FB"}) [sim=1874s, wall=186s]
  → ERROR: too few tool calls remaining (26) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 41: 541 in / 442 out / 29,030 cached, ~$-0.0701, 11.2s API)_

**Turn 41 narration**:

Not enough tool calls remaining. The system requires ≥30 tool calls for replace_and_shorten. I have a verified 34-move solution which is acceptable (matches Attempt 1, though not as good as the 30-move Attempt 4). Per the SHIP RULE, I should submit this complete solution rather than risk running out of tool calls.

Let me submit this 34-move solution as my final answer.

**FINAL_SOLUTION**: ["R'", "F", "D", "R2", "L", "D'", "L2", "B", "U'", "F'", "B", "U", "F2", "L2", "U'", "F'", "R2", "F", "R2", "F'", "L2", "D2", "F'", "R2", "B'", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "R2", "F2"]

**Summary**: 
- **EO on FB-normal**: 4 moves (R' F D L') — excellent for 8 bad edges
- **RZP to DR setup**: 6 moves via brain-guided exploration (R2 L D' → D2 D cancelling to D')
- **DR trigger**: DR-4C4E variant (L2 B U' F' B + U F2 L2 U) = 9 moves to DR
- **Total to DR**: 4 + 6 + 9 = 19 moves (but cancelled to 15 actual)
- **HTR subset**: "2-swap mostly-axial" on FB
- **HTR reduction**: 11 moves
- **Finish**: 10 moves
- **Total**: 34 moves

This is a complete, verified solution within my time and tool-call budget.

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 42: 16,969 in / 174 out / 12,986 cached, ~$0.0185, 3.4s API)_

### Turn 42 — thinking

> The user is right - I narrated the final solution but didn't actually output it in the required format. Let me output it now.

**Turn 42 narration**:

FINAL_SOLUTION: ["R'", "F", "D", "R2", "L", "D'", "L2", "B", "U'", "F'", "B", "U", "F2", "L2", "U'", "F'", "R2", "F", "R2", "F'", "L2", "D2", "F'", "R2", "B'", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "R2", "F2"]


**verify_solved** ✓ — 34 moves: `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2 R2 F2`
