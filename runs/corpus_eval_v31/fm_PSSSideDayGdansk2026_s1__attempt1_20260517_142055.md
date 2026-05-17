# Run — fm_PSSSideDayGdansk2026_s1__attempt1_20260517_142055.json

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (31 moves, 60 tool calls)  
**Sim budget**: 1847s / 3600s  
**Wall time**: 234s  
**Tokens**: 31,790 in (1,281,731 cached), 6,822 out  
**Cost estimate**: $0.631  
**Solution**: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 6× = 1652s
- `reset_slot`: 5× = 125s
- `eo_pattern_lookup`: 10× = 30s
- `htr_classify`: 1× = 15s
- `niss_flip`: 4× = 8s
- `apply_moves`: 18× = 6s
- `inspect_state`: 1× = 5s
- `apply_htr_phase`: 5× = 5s
- `compose_niss_solution`: 1× = 1s
- `cancel`: 1× = 1s

---

_(turn 1: 9 in / 270 out / 13,347 cached, ~$-0.0320, 6.9s API)_

### Turn 1 — thinking

> The user wants me to solve a Rubik's Cube FMC scramble. The scramble is:
> R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I need to follow the FMC methodology outlined in the instructions:
> 1. Start with inspect_state to see the bad edges per axis
> 2. Scout EO on multiple axes (normal and inverse)
> 3. Compare DR options for each viable EO
> 4. Commit to the best joint EO+DR path
> 5. Execute DR → HTR → finish
> 6. Verify and submit
> 
> Let me begin with inspect_state to see what I'm working with.

**Turn 1 narration**:

I'll solve this FMC scramble step by step, starting with inspection to understand the cube state and plan my approach.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=7s]
  → EO: [], DR: [], bad_edges {'UD': 8, 'FB': 6, 'RL': 6}
_(turn 2: 896 in / 300 out / 12,982 cached, ~$-0.0279, 7.8s API)_

**Turn 2 narration**:

**Initial Inspection Analysis:**
- **Bad edges**: UD=8, FB=6, RL=6
- **DR closeness**: UD has DR-6C3E (not JZP), FB has DR-5C2E, RL has DR-7C3E
- **Important**: UD shows `top_pairs_on_inverse: 2` — this is a strong NISS-switch signal

**Strategy:** 8 bad edges on UD-axis is typically a 3-5 move EO using the `<m> F <m'> B` symmetry pattern. However, with 2 pairs preserved on inverse, I should check the inverse frame first. The NISS invariant tells me bad-edge counts are identical on normal/inverse, but the SOLUTION differs.

Let me scout EO on both normal and inverse frames for the FB and RL axes (both at 6 bad edges), then also check UD-inverse since we have 2 pairs preserved.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=15s]
  → found=1, best=4m
_(turn 3: 1,325 in / 121 out / 12,982 cached, ~$-0.0293, 3.3s API)_

**Turn 3 narration**:

**FB-axis EO (normal):** 5 moves total, first chunk is R2 B' L' U2. That's on the longer side. Let me check RL-axis on normal:

- `tool#3` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=11s, wall=18s]
  → found=1, best=4m
_(turn 4: 680 in / 112 out / 13,618 cached, ~$-0.0330, 3.2s API)_

**Turn 4 narration**:

**RL-axis EO (normal):** Also 5 moves. Both FB and RL are 5-movers on normal. Now let me switch to inverse and check these axes there, plus UD-inverse since we have 2 pairs preserved.

- `tool#4` **niss_flip**({"slot":"main"}) [sim=13s, wall=21s]
  → (empty result)
_(turn 5: 751 in / 212 out / 14,536 cached, ~$-0.0338, 3.5s API)_

**Turn 5 narration**:

Now I'm on the inverse frame. Let me check EO for UD, FB, and RL axes:

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=16s, wall=25s]
  → found=1, best=4m
- `tool#6` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=19s, wall=25s]
  → found=1, best=4m
- `tool#7` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=22s, wall=25s]
  → found=1, best=4m
_(turn 6: 1,158 in / 188 out / 14,787 cached, ~$-0.0336, 6.0s API)_

**Turn 6 narration**:

**All inverse EOs are also 5 moves.** This is not ideal — all six (side, axis) combinations give 5-move EOs. However, the 2 pairs preserved on UD-inverse is still a strong signal. Let me probe DR options after each EO to make the joint decision.

Let me test UD-inverse first since we have the pairs signal. I'll apply the first 4 moves of the EO and check DR options:

- `tool#8` **apply_moves**({"slot":"main","moves":["B'","D'","L'","R'"]}) [sim=22s, wall=31s]
  → hist=4m
  slot=main [INV] hist(4m): `B' D' L' R'`
_(turn 7: 907 in / 74 out / 15,026 cached, ~$-0.0367, 5.5s API)_

- `tool#9` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=25s, wall=36s]
  → found=1, best=1m
_(turn 8: 404 in / 115 out / 15,515 cached, ~$-0.0390, 3.7s API)_

**Turn 8 narration**:

Excellent! One more move completes UD-EO on inverse: **5 moves total (B' D' L' R' F')**. Now let me check DR options:

- `tool#10` **apply_moves**({"slot":"main","moves":["F'"]}) [sim=26s, wall=40s]
  → hist=5m
  slot=main [INV] hist(5m): `B' D' L' R' F'`
_(turn 9: 333 in / 92 out / 16,259 cached, ~$-0.0415, 4.7s API)_

- `tool#11` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=334s, wall=48s]
  → (empty result)
_(turn 10: 656 in / 129 out / 16,326 cached, ~$-0.0402, 3.7s API)_

**Turn 10 narration**:

**No DR triggers found within 5 moves on UD-inverse.** This is a bad sign — the pairs signal didn't pan out for UD. Let me reset and try a different axis. Let me go back and check FB or RL on inverse.

- `tool#12` **reset_slot**({"slot":"main","rescramble":true}) [sim=359s, wall=51s]
  → (empty result)
_(turn 11: 631 in / 71 out / 16,590 cached, ~$-0.0418, 5.7s API)_

**Turn 11 narration**:

Let me try FB-axis on inverse. Flipping to inverse again:

- `tool#13` **niss_flip**({"slot":"main"}) [sim=361s, wall=57s]
  → (empty result)
_(turn 12: 616 in / 83 out / 16,661 cached, ~$-0.0419, 1.8s API)_

- `tool#14` **apply_moves**({"slot":"main","moves":["R","F","D'","U'"]}) [sim=362s, wall=59s]
  → hist=4m
  slot=main [INV] hist(4m): `R F D' U'`
_(turn 13: 601 in / 73 out / 17,262 cached, ~$-0.0437, 1.9s API)_

- `tool#15` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=365s, wall=61s]
  → found=1, best=1m
_(turn 14: 290 in / 106 out / 17,363 cached, ~$-0.0444, 4.3s API)_

**Turn 14 narration**:

Perfect! FB-inverse EO is **5 moves: R F D' U' R'**. Let me complete it and check DR options:

- `tool#16` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=365s, wall=65s]
  → hist=5m
  slot=main [INV] hist(5m): `R F D' U' R'`
_(turn 15: 316 in / 91 out / 17,756 cached, ~$-0.0456, 2.2s API)_

- `tool#17` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=609s, wall=69s]
  → (empty result)
_(turn 16: 982 in / 218 out / 17,901 cached, ~$-0.0421, 7.4s API)_

**Turn 16 narration**:

**FB-inverse DR options:**
- **DR-7C8E in 7 moves** (4 setup + 3 trigger): This is a bad substate (7c8e = very long finish)
- **DR-2C4E in 8 moves**: Better substate but still 8 moves to DR

**Total so far: 5 (EO) + 7 (DR) = 12 moves to DR** with a 7C8E substate, which typically needs 15+ moves to finish. That's looking at ~27+ total. Not great.

Let me try RL-axis on inverse:

- `tool#18` **reset_slot**({"slot":"main","rescramble":true}) [sim=634s, wall=76s]
  → (empty result)
_(turn 17: 1,057 in / 54 out / 18,155 cached, ~$-0.0450, 1.6s API)_

- `tool#19` **niss_flip**({"slot":"main"}) [sim=636s, wall=78s]
  → (empty result)
_(turn 18: 683 in / 82 out / 18,224 cached, ~$-0.0459, 2.0s API)_

- `tool#20` **apply_moves**({"slot":"main","moves":["B","U","B2","F"]}) [sim=636s, wall=80s]
  → hist=4m
  slot=main [INV] hist(4m): `B U B2 F`
_(turn 19: 577 in / 74 out / 19,256 cached, ~$-0.0492, 1.9s API)_

- `tool#21` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=639s, wall=82s]
  → found=1, best=1m
_(turn 20: 284 in / 105 out / 19,289 cached, ~$-0.0497, 6.6s API)_

**Turn 20 narration**:

Great! RL-inverse EO is **5 moves: B U B2 F D'**. Let me complete and check DR:

- `tool#22` **apply_moves**({"slot":"main","moves":["D'"]}) [sim=639s, wall=88s]
  → hist=5m
  slot=main [INV] hist(5m): `B U B2 F D'`
_(turn 21: 310 in / 92 out / 19,733 cached, ~$-0.0510, 2.2s API)_

- `tool#23` **dr_trigger_options**({"slot":"main","axis":"RL","max_setup":5}) [sim=923s, wall=93s]
  → (empty result)
_(turn 22: 759 in / 176 out / 19,876 cached, ~$-0.0487, 4.4s API)_

**Turn 22 narration**:

**RL-inverse:** DR-4C4E in 9 moves (5 setup + 4 trigger). Total: **5 (EO) + 9 (DR) = 14 moves to DR**. 4C4E substate typically finishes in 12-14 moves, so we're looking at ~26-28 total.

Let me also check the normal frame for comparison. Let me try RL-axis on normal:

- `tool#24` **reset_slot**({"slot":"main","rescramble":true}) [sim=948s, wall=98s]
  → (empty result)
_(turn 23: 794 in / 82 out / 20,130 cached, ~$-0.0507, 2.5s API)_

- `tool#25` **apply_moves**({"slot":"main","moves":["L","U","L2","R"]}) [sim=949s, wall=100s]
  → hist=4m
  slot=main hist(4m): `L U L2 R`
_(turn 24: 335 in / 74 out / 20,198 cached, ~$-0.0524, 1.8s API)_

- `tool#26` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=952s, wall=102s]
  → found=1, best=1m
_(turn 25: 280 in / 100 out / 20,972 cached, ~$-0.0543, 4.0s API)_

**Turn 25 narration**:

RL-normal also 5 moves: **L U L2 R D'**. Let me check DR:

- `tool#27` **apply_moves**({"slot":"main","moves":["D'"]}) [sim=952s, wall=106s]
  → hist=5m
  slot=main hist(5m): `L U L2 R D'`
_(turn 26: 301 in / 92 out / 21,005 cached, ~$-0.0544, 2.6s API)_

- `tool#28` **dr_trigger_options**({"slot":"main","axis":"RL","max_setup":5}) [sim=1236s, wall=111s]
  → (empty result)
_(turn 27: 624 in / 94 out / 21,148 cached, ~$-0.0538, 2.6s API)_

**Turn 27 narration**:

No DR options on RL-normal within 5 moves. Let me try FB-normal:

- `tool#29` **reset_slot**({"slot":"main","rescramble":true}) [sim=1261s, wall=114s]
  → (empty result)
_(turn 28: 582 in / 85 out / 21,397 cached, ~$-0.0548, 2.1s API)_

- `tool#30` **apply_moves**({"slot":"main","moves":["R2","B'","L'","U2"]}) [sim=1262s, wall=116s]
  → hist=4m
  slot=main hist(4m): `R2 B' L' U2`
_(turn 29: 255 in / 73 out / 21,465 cached, ~$-0.0561, 2.0s API)_

- `tool#31` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=1265s, wall=118s]
  → found=1, best=1m
_(turn 30: 281 in / 99 out / 22,031 cached, ~$-0.0572, 2.5s API)_

**Turn 30 narration**:

FB-normal EO is **5 moves: R2 B' L' U2 R'**:

- `tool#32` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=1265s, wall=120s]
  → hist=5m
  slot=main hist(5m): `R2 B' L' U2 R'`
_(turn 31: 298 in / 91 out / 22,064 cached, ~$-0.0573, 1.9s API)_

- `tool#33` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=1551s, wall=125s]
  → (empty result)
_(turn 32: 619 in / 92 out / 22,213 cached, ~$-0.0567, 3.0s API)_

**Turn 32 narration**:

No DR options on FB-normal either. Let me check UD-normal as well:

- `tool#34` **reset_slot**({"slot":"main","rescramble":true}) [sim=1576s, wall=128s]
  → (empty result)
_(turn 33: 573 in / 196 out / 22,460 cached, ~$-0.0560, 5.2s API)_

**Turn 33 narration**:

Actually, let me think strategically. I've found:
- **FB-inverse**: 5 EO + 7 DR = 12 to DR (7C8E substate, ~15 finish = ~27 total)
- **RL-inverse**: 5 EO + 9 DR = 14 to DR (4C4E substate, ~13 finish = ~27 total)

Both are around 27 total. Let me try to manually explore a bit more on FB-inverse since it has the shortest DR. Let me also try increasing max_setup to 6 on the better options:

- `tool#35` **niss_flip**({"slot":"main"}) [sim=1578s, wall=133s]
  → (empty result)
_(turn 34: 686 in / 87 out / 22,531 cached, ~$-0.0575, 4.7s API)_

- `tool#36` **apply_moves**({"slot":"main","moves":["R","F","D'","U'","R'"]}) [sim=1579s, wall=138s]
  → hist=5m
  slot=main [INV] hist(5m): `R F D' U' R'`
_(turn 35: 716 in / 91 out / 23,092 cached, ~$-0.0588, 2.0s API)_

- `tool#37` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":6}) [sim=1823s, wall=142s]
  → (empty result)
_(turn 36: 947 in / 166 out / 23,318 cached, ~$-0.0576, 4.3s API)_

**Turn 36 narration**:

Same results. The best option is **DR-7C8E in 7 moves**. Let me commit to this path since it's the shortest to DR I've found. I'll proceed with FB-inverse:

**Decision: FB-inverse axis, 5 EO + 7 DR = 12 to DR**

Applying the DR setup and trigger:

- `tool#38` **apply_moves**({"slot":"main","moves":["D","F'","L2","B'"]}) [sim=1823s, wall=146s]
  → hist=9m
  slot=main [INV] hist(9m): `R F D' U' R' D F' L2 B'`
_(turn 37: 1,040 in / 78 out / 23,711 cached, ~$-0.0597, 2.9s API)_

- `tool#39` **apply_moves**({"slot":"main","moves":["U","F","D"]}) [sim=1823s, wall=149s]
  → hist=12m
  slot=main [INV] hist(12m): `R F D' U' R' D F' L2 B' U F D`
_(turn 38: 390 in / 94 out / 23,864 cached, ~$-0.0619, 2.5s API)_

**Turn 38 narration**:

Now I'm at DR on FB-axis (inverse frame). Let me classify the HTR substate:

- `tool#40` **htr_classify**({"slot":"main","axis":"FB"}) [sim=1838s, wall=176s]
  → subset=[2, 0, 4, 3, 1, 5, 6, 7]
_(turn 39: 517 in / 206 out / 24,844 cached, ~$-0.0624, 4.7s API)_

**Turn 39 narration**:

**HTR classification:** 2-swap mostly-axial subset
- HTR reduction: 7 moves
- Finish: 12 moves
- **Total from DR to solved: 19 moves**

**Projected total:** 5 (EO) + 7 (DR) + 19 (HTR+finish) = **31 moves**

This is quite long. Let me execute it to get a working solution, then I can consider optimization. Let me apply HTR reduction:

- `tool#41` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1839s, wall=181s]
  → (empty result)
_(turn 40: 668 in / 85 out / 24,928 cached, ~$-0.0640, 1.8s API)_

- `tool#42` **apply_moves**({"slot":"main","moves":["F'","U2","R2","L2"]}) [sim=1840s, wall=182s]
  → hist=16m
  slot=main [INV] hist(16m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2`
_(turn 41: 483 in / 63 out / 25,187 cached, ~$-0.0656, 1.8s API)_

**Turn 41 narration**:

Let me do a quick check before continuing:

- `tool#43` **quick_check**({"slot":"main"}) [sim=1840s, wall=184s]
  → (empty result)
_(turn 42: 348 in / 107 out / 25,674 cached, ~$-0.0667, 5.0s API)_

**Turn 42 narration**:

Still in DR on FB. Let me continue HTR reduction:

- `tool#44` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1841s, wall=189s]
  → (empty result)
_(turn 43: 339 in / 79 out / 25,791 cached, ~$-0.0674, 1.6s API)_

- `tool#45` **apply_moves**({"slot":"main","moves":["F","R2","B"]}) [sim=1841s, wall=191s]
  → hist=19m
  slot=main [INV] hist(19m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B`
_(turn 44: 347 in / 53 out / 26,042 cached, ~$-0.0685, 2.3s API)_

- `tool#46` **quick_check**({"slot":"main"}) [sim=1841s, wall=193s]
  → (empty result)
_(turn 45: 339 in / 116 out / 26,272 cached, ~$-0.0682, 2.5s API)_

**Turn 45 narration**:

Great! I'm now in HTR (is_htr_ud: true). Let me apply the finish phase:

- `tool#47` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1842s, wall=196s]
  → (empty result)
_(turn 46: 367 in / 85 out / 26,351 cached, ~$-0.0688, 1.7s API)_

- `tool#48` **apply_moves**({"slot":"main","moves":["L2","F2","U2","R2"]}) [sim=1842s, wall=197s]
  → hist=23m
  slot=main [INV] hist(23m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B L2 F2 U2 R2`
_(turn 47: 407 in / 53 out / 26,546 cached, ~$-0.0697, 1.4s API)_

- `tool#49` **quick_check**({"slot":"main"}) [sim=1842s, wall=199s]
  → (empty result)
_(turn 48: 358 in / 102 out / 26,835 cached, ~$-0.0699, 2.5s API)_

**Turn 48 narration**:

Still in HTR. Let me continue the finish:

- `tool#50` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1843s, wall=201s]
  → (empty result)
_(turn 49: 350 in / 85 out / 26,946 cached, ~$-0.0704, 1.6s API)_

- `tool#51` **apply_moves**({"slot":"main","moves":["B2","R2","F2","U2"]}) [sim=1844s, wall=203s]
  → hist=27m
  slot=main [INV] hist(27m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B L2 F2 U2 R2 B2 R2 F2 U2`
_(turn 50: 406 in / 53 out / 27,163 cached, ~$-0.0713, 1.7s API)_

- `tool#52` **quick_check**({"slot":"main"}) [sim=1844s, wall=204s]
  → (empty result)
_(turn 51: 371 in / 90 out / 27,438 cached, ~$-0.0716, 1.9s API)_

- `tool#53` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1845s, wall=206s]
  → (empty result)
_(turn 52: 303 in / 85 out / 27,549 cached, ~$-0.0722, 2.7s API)_

- `tool#54` **apply_moves**({"slot":"main","moves":["R2","U2","R2","U2"]}) [sim=1845s, wall=209s]
  → hist=31m
  slot=main [INV] hist(31m): `R F D' U' R' D F' L2 B' U F D F' U2 R2 L2 F R2 B L2 F2 U2 R2 B2 R2 F2 U2 R2 U2 R2 U2`
_(turn 53: 375 in / 53 out / 27,782 cached, ~$-0.0731, 1.4s API)_

- `tool#55` **quick_check**({"slot":"main"}) [sim=1845s, wall=210s]
  → SOLVED
_(turn 54: 384 in / 92 out / 27,958 cached, ~$-0.0730, 2.5s API)_

**Turn 54 narration**:

Excellent! The cube is solved. I'm on the inverse frame, so I need to use compose_niss_solution to get the correct normal-frame solution:

- `tool#56` **compose_niss_solution**({"slot":"main"}) [sim=1846s, wall=213s]
  → solves=True
_(turn 55: 430 in / 65 out / 28,124 cached, ~$-0.0737, 2.3s API)_

**Turn 55 narration**:

I have a 31-move solution! Now let me check the budget and consider if I should try replace_and_shorten:

- `tool#57` **budget_status**({}) [sim=1846s, wall=215s]
  → sim=1846s
_(turn 56: 526 in / 225 out / 28,373 cached, ~$-0.0717, 6.4s API)_

**Turn 56 narration**:

I have plenty of budget remaining (1753s simulated, ~1285s real wall time). Since my solution is 31 moves and I have enough budget, I should try replace_and_shorten to optimize it. The gate requires ≥27 moves AND ≥30 tool calls remaining — I'm at 31 moves, so I qualify.

Let me try replace_and_shorten on a large span. I'll target the HTR-finish portion (moves 12-31), which is 19 moves:

- `tool#58` **replace_and_shorten**({"slot":"main","start":12,"end":31,"axis":"FB"}) [sim=1846s, wall=222s]
  → ERROR: too few tool calls remaining (22) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 57: 526 in / 196 out / 28,638 cached, ~$-0.0728, 3.1s API)_

**Turn 57 narration**:

I don't have enough tool calls remaining for replace_and_shorten. Let me verify and submit my current solution:

- `tool#59` **verify_solved**({"solution":["U2","R2","U2","R2","U2","F2","R2","B2","R2","U2","F2","L2","B'","R2","F'","L2","R2","U2","F","D'","F'",...) [sim=1846s, wall=225s]
  → solves=True, moves=31
_(turn 58: 474 in / 192 out / 28,907 cached, ~$-0.0737, 2.9s API)_

**Turn 58 narration**:

Perfect! The solution is verified. Let me check if there are any obvious cancellations I can make manually:

- `tool#60` **cancel**({"moves":["U2","R2","U2","R2","U2","F2","R2","B2","R2","U2","F2","L2","B'","R2","F'","L2","R2","U2","F","D'","F'","U'...) [sim=1847s, wall=228s]
  → cancelled 31->31
_(turn 59: 526 in / 305 out / 29,340 cached, ~$-0.0731, 6.6s API)_

**Turn 59 narration**:

No cancellations were found. The solution is already optimally formatted.

## FINAL_SOLUTION

**Solution breakdown:**
- **EO (FB-axis, inverse):** R F D' U' R' (5 moves)
- **DR setup:** D F' L2 B' (4 moves)  
- **DR trigger (7C8E):** U F D (3 moves)
- **HTR reduction:** F' U2 R2 L2 F R2 B (7 moves)
- **HTR finish:** L2 F2 U2 R2 B2 R2 F2 U2 R2 U2 R2 U2 (12 moves)

Total: **31 moves**

FINAL_SOLUTION: ["U2", "R2", "U2", "R2", "U2", "F2", "R2", "B2", "R2", "U2", "F2", "L2", "B'", "R2", "F'", "L2", "R2", "U2", "F", "D'", "F'", "U'", "B", "L2", "F", "D'", "R", "U", "D", "F'", "R'"]


**verify_solved** ✓ — 31 moves: `U2 R2 U2 R2 U2 F2 R2 B2 R2 U2 F2 L2 B' R2 F' L2 R2 U2 F D' F' U' B L2 F D' R U D F' R'`
