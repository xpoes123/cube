# Run — fm_PSSSideDayGdansk2026_s1__attempt3_20260517_010434.json

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (29 moves, 54 tool calls)  
**Sim budget**: 277s / 3600s  
**Wall time**: 197s  
**Tokens**: 40,465 in (1,117,610 cached), 6,332 out  
**Cost estimate**: $0.592  
**Solution**: `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 D U F R L D B`  

**Sim-time spent by tool**:

- `reset_slot`: 3× = 90s
- `apply_moves`: 16× = 64s
- `dr_trigger_options`: 4× = 32s
- `htr_classify`: 2× = 30s
- `niss_flip`: 4× = 20s
- `eo_pattern_lookup`: 6× = 18s
- `undo_moves`: 3× = 9s
- `inspect_state`: 1× = 5s
- `apply_htr_phase`: 5× = 5s
- `probe_dr_pattern`: 1× = 3s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 694 in / 303 out / 12,867 cached, ~$-0.0281, 6.8s API)_

### Turn 1 — thinking

> Let me understand what I need to do:
> 
> 1. This is my 3rd attempt at this scramble
> 2. Previous attempts: 30 moves, then 25 moves
> 3. I need to commit hard to a line and finish it cleanly
> 4. Don't over-ideate or abandon paths halfway
> 
> The instruction is clear: pick a line and drive it to completion. Let me start by inspecting the state to understand the scramble.
> 
> Scramble: R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F
> 
> I should:
> 1. Inspect the state
> 2. Scout EO on normal and inverse
> 3. Compare DR options
> 4. Pick ONE line and commit
> 5. Execute cleanly through HTR + finish
> 6. Submit
> 
> Let's start.

**Turn 1 narration**:

I'll solve this scramble methodically, learning from the prior 25-move solution. Let me start by inspecting the cube state.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=7s]
  → EO: [], DR: [], bad_edges {'UD': 8, 'FB': 6, 'RL': 6}
_(turn 2: 929 in / 232 out / 12,867 cached, ~$-0.0285, 5.6s API)_

**Turn 2 narration**:

**EO scan**: UD=8 bad, FB=6 bad, RL=6 bad. The 8-bad on UD suggests a symmetry pattern — I should check inverse for EO. FB and RL both have 6 bad edges, so I'll scout EO on these axes.

**DR snapshot**: UD is DR-6C3E (bad), FB is DR-5C2E (better), RL is DR-7C3E (worst). Notice `top_pairs_on_inverse: 2` on UD — this is a NISS signal. Let me scout EO on both normal and inverse.

Let me check FB-axis EO first on normal:

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=12s]
  → found=1, best=4m
_(turn 3: 1,290 in / 102 out / 12,867 cached, ~$-0.0293, 2.1s API)_

**Turn 3 narration**:

FB-axis EO is 5 moves (seeing the first 4). Let me check RL-axis EO:

- `tool#3` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=11s, wall=15s]
  → found=1, best=4m
_(turn 4: 593 in / 97 out / 13,856 cached, ~$-0.0342, 3.1s API)_

**Turn 4 narration**:

Both FB and RL are 5 moves. Now let me check the inverse frame — the 2 pairs on inverse + 8-bad UD on normal suggests checking inverse-UD:

- `tool#4` **niss_flip**({"slot":"main"}) [sim=16s, wall=18s]
  → (empty result)
_(turn 5: 717 in / 74 out / 14,706 cached, ~$-0.0364, 2.0s API)_

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=19s, wall=20s]
  → found=1, best=4m
_(turn 6: 691 in / 113 out / 14,938 cached, ~$-0.0366, 3.1s API)_

**Turn 6 narration**:

Inverse-UD is also 5 moves. So all three candidate axes (normal-FB, normal-RL, inverse-UD) are 5-move EOs. The tiebreaker is DR quality. Let me probe DR after each EO:

- `tool#6` **niss_flip**({"slot":"main"}) [sim=24s, wall=23s]
  → (empty result)
_(turn 7: 706 in / 127 out / 15,162 cached, ~$-0.0369, 4.3s API)_

**Turn 7 narration**:

Back to normal. Let me probe DR after FB-axis EO:

- `tool#7` **probe_dr_pattern**({"slot":"main","eo_alg":["R2","B'","L'","U2","L"],"axis":"FB"}) [sim=27s, wall=27s]
  → ERROR: EO not yet solved on axis FB; run eo_pattern_lookup + apply_moves first.
_(turn 8: 695 in / 96 out / 15,555 cached, ~$-0.0385, 4.0s API)_

**Turn 8 narration**:

Let me actually commit the FB EO first:

- `tool#8` **apply_moves**({"slot":"main","moves":["R2","B'","L'","U2"]}) [sim=31s, wall=31s]
  → hist=4m
  slot=main hist(4m): `R2 B' L' U2`
_(turn 9: 351 in / 73 out / 15,869 cached, ~$-0.0407, 1.7s API)_

- `tool#9` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=34s, wall=33s]
  → found=1, best=1m
_(turn 10: 307 in / 73 out / 16,386 cached, ~$-0.0422, 1.7s API)_

- `tool#10` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=35s, wall=34s]
  → hist=5m
  slot=main hist(5m): `R2 B' L' U2 R'`
_(turn 11: 287 in / 97 out / 16,549 cached, ~$-0.0424, 2.3s API)_

**Turn 11 narration**:

Good! FB-axis EO is done in 5 moves. Now let me check DR options on FB:

- `tool#11` **dr_trigger_options**({"slot":"main","axis":"FB"}) [sim=43s, wall=39s]
  → (empty result)
_(turn 12: 351 in / 91 out / 16,616 cached, ~$-0.0424, 2.5s API)_

**Turn 12 narration**:

No DR triggers found on FB within 5 setup moves. This is a red flag — let me go back and try RL-axis EO instead. Let me reset:

- `tool#12` **reset_slot**({"slot":"main"}) [sim=73s, wall=42s]
  → (empty result)
_(turn 13: 330 in / 93 out / 16,767 cached, ~$-0.0429, 2.5s API)_

**Turn 13 narration**:

Let me try RL-axis EO:

- `tool#13` **apply_moves**({"slot":"main","moves":["L","U","L2","R"]}) [sim=77s, wall=44s]
  → hist=4m
  slot=main hist(4m): `L U L2 R`
_(turn 14: 267 in / 74 out / 17,002 cached, ~$-0.0440, 4.1s API)_

- `tool#14` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=80s, wall=48s]
  → found=1, best=1m
_(turn 15: 297 in / 73 out / 17,212 cached, ~$-0.0445, 1.7s API)_

- `tool#15` **apply_moves**({"slot":"main","moves":["D'"]}) [sim=81s, wall=50s]
  → hist=5m
  slot=main hist(5m): `L U L2 R D'`
_(turn 16: 280 in / 97 out / 17,335 cached, ~$-0.0445, 2.4s API)_

**Turn 16 narration**:

RL-axis EO complete in 5 moves. Now let me check DR options on RL:

- `tool#16` **dr_trigger_options**({"slot":"main","axis":"RL"}) [sim=89s, wall=55s]
  → (empty result)
_(turn 17: 345 in / 85 out / 17,399 cached, ~$-0.0447, 3.4s API)_

**Turn 17 narration**:

No DR triggers on RL either within 5 setup! This is concerning. Let me try the inverse-UD line. Resetting:

- `tool#17` **reset_slot**({"slot":"main"}) [sim=119s, wall=58s]
  → (empty result)
_(turn 18: 321 in / 54 out / 17,551 cached, ~$-0.0456, 1.6s API)_

- `tool#18` **niss_flip**({"slot":"main"}) [sim=124s, wall=60s]
  → (empty result)
_(turn 19: 546 in / 103 out / 17,783 cached, ~$-0.0448, 2.6s API)_

**Turn 19 narration**:

Now I'm on inverse. Let me apply the inverse-UD EO:

- `tool#19` **apply_moves**({"slot":"main","moves":["B'","D'","L'","R'"]}) [sim=128s, wall=62s]
  → hist=4m
  slot=main [INV] hist(4m): `B' D' L' R'`
_(turn 20: 597 in / 74 out / 17,989 cached, ~$-0.0457, 5.2s API)_

- `tool#20` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=131s, wall=68s]
  → found=1, best=1m
_(turn 21: 304 in / 73 out / 18,022 cached, ~$-0.0467, 7.4s API)_

- `tool#21` **apply_moves**({"slot":"main","moves":["F'"]}) [sim=132s, wall=75s]
  → hist=5m
  slot=main [INV] hist(5m): `B' D' L' R' F'`
_(turn 22: 277 in / 98 out / 18,566 cached, ~$-0.0478, 2.5s API)_

**Turn 22 narration**:

Inverse-UD EO complete in 5 moves. Now let me check DR options on UD:

- `tool#22` **dr_trigger_options**({"slot":"main","axis":"UD"}) [sim=140s, wall=80s]
  → (empty result)
_(turn 23: 343 in / 123 out / 18,633 cached, ~$-0.0474, 3.1s API)_

**Turn 23 narration**:

All three axes have no DR triggers within 5 setup! This is unusual. Let me try extending the search to max_setup=6:

- `tool#23` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":6}) [sim=148s, wall=96s]
  → (empty result)
_(turn 24: 930 in / 281 out / 18,785 cached, ~$-0.0437, 6.2s API)_

**Turn 24 narration**:

Good! I found DR options. **Comparing**:
- DR-7C8E in 9 moves (6+3) — bad substate, long DR
- DR-3C2E in 9 moves (6+3) — **good substate** (3C2E typically finishes in 6-8 moves), non-JZP
- DR-4C4E in 10 moves (6+4) — **JZP-eligible**, substate is worse than 3C2E

The **DR-3C2E at 9 moves total is my best option**. EO was 5 moves, so 5+9=14 moves to DR. That's acceptable (sub-15 DR). Let me commit to this line.

Applying setup for DR-3C2E:

- `tool#24` **apply_moves**({"slot":"main","moves":["U'","D'","F2","U'","F2","L"]}) [sim=154s, wall=102s]
  → hist=11m
  slot=main [INV] hist(11m): `B' D' L' R' F' U' D' F2 U' F2 L`
_(turn 25: 1,082 in / 79 out / 19,021 cached, ~$-0.0469, 1.6s API)_

- `tool#25` **apply_moves**({"slot":"main","moves":["R","U","R'"]}) [sim=157s, wall=104s]
  → hist=14m
  slot=main [INV] hist(14m): `B' D' L' R' F' U' D' F2 U' F2 L R U R'`
_(turn 26: 532 in / 105 out / 19,265 cached, ~$-0.0488, 3.0s API)_

**Turn 26 narration**:

DR is reached at 14 moves (I'm on inverse, so this will be the tail of the final solution). Now let me classify HTR:

- `tool#26` **htr_classify**({"slot":"main","axis":"UD"}) [sim=172s, wall=107s]
  → subset=[0, 1, 2, 5, 4, 3, 7, 6]
_(turn 27: 552 in / 202 out / 20,152 cached, ~$-0.0497, 5.1s API)_

**Turn 27 narration**:

HTR subset is 2-swap mostly-axial: 5 moves htr_reduction + 11 moves finish = 16 moves post-DR. So total = 14 (to DR) + 16 (HTR+finish) = **30 moves**. That matches my first attempt but not better than the 25-move prior attempt.

Let me check if there's a better DR option. Actually, let me reconsider — maybe I should try the JZP-eligible DR-4C4E option instead, even though it's 10 moves to DR:

- `tool#27` **undo_moves**({"slot":"main","n":3}) [sim=175s, wall=112s]
  → hist=11m
  slot=main [INV] hist(11m): `B' D' L' R' F' U' D' F2 U' F2 L`
_(turn 28: 654 in / 85 out / 20,246 cached, ~$-0.0514, 1.9s API)_

**Turn 28 narration**:

Let me undo more to try the JZP path:

- `tool#28` **undo_moves**({"slot":"main","n":4}) [sim=179s, wall=114s]
  → hist=7m
  slot=main [INV] hist(7m): `B' D' L' R' F' U' D'`
_(turn 29: 411 in / 71 out / 20,528 cached, ~$-0.0531, 3.3s API)_

- `tool#29` **undo_moves**({"slot":"main","n":2}) [sim=181s, wall=117s]
  → hist=5m
  slot=main [INV] hist(5m): `B' D' L' R' F'`
_(turn 30: 256 in / 110 out / 21,018 cached, ~$-0.0543, 2.8s API)_

**Turn 30 narration**:

Now I'm at EO. Let me try the JZP-eligible path:

- `tool#30` **apply_moves**({"slot":"main","moves":["D","L","U2","B2","R'","D'"]}) [sim=187s, wall=120s]
  → hist=11m
  slot=main [INV] hist(11m): `B' D' L' R' F' D L U2 B2 R' D'`
_(turn 31: 304 in / 83 out / 21,184 cached, ~$-0.0550, 2.1s API)_

- `tool#31` **apply_moves**({"slot":"main","moves":["R","U2","F2","R"]}) [sim=191s, wall=122s]
  → hist=15m
  slot=main [INV] hist(15m): `B' D' L' R' F' D L U2 B2 R' D' R U2 F2 R`
_(turn 32: 361 in / 104 out / 21,253 cached, ~$-0.0547, 2.8s API)_

**Turn 32 narration**:

DR reached at 15 moves via JZP-eligible path (5 EO + 10 DR). Let me classify HTR:

- `tool#32` **htr_classify**({"slot":"main","axis":"UD"}) [sim=206s, wall=125s]
  → subset=[1, 0, 2, 6, 5, 3, 7, 4]
_(turn 33: 531 in / 133 out / 21,489 cached, ~$-0.0544, 3.9s API)_

**Turn 33 narration**:

JZP path: 8 moves HTR reduction + 12 moves finish = 20 moves post-DR. Total = 15 + 20 = **35 moves**. That's worse!

The DR-3C2E path at 30 moves is better. Let me go back to that path and complete it. Resetting:

- `tool#33` **reset_slot**({"slot":"main"}) [sim=236s, wall=129s]
  → (empty result)
_(turn 34: 506 in / 54 out / 21,582 cached, ~$-0.0559, 1.5s API)_

- `tool#34` **niss_flip**({"slot":"main"}) [sim=241s, wall=130s]
  → (empty result)
_(turn 35: 578 in / 140 out / 21,870 cached, ~$-0.0552, 3.4s API)_

**Turn 35 narration**:

Committing to inverse-UD with DR-3C2E path:

- `tool#35` **apply_moves**({"slot":"main","moves":["B'","D'","L'","R'","F'","U'","D'","F2","U'","F2","L","R","U","R'"]}) [sim=255s, wall=134s]
  → hist=14m
  slot=main [INV] hist(14m): `B' D' L' R' F' U' D' F2 U' F2 L R U R'`
_(turn 36: 655 in / 103 out / 22,270 cached, ~$-0.0566, 3.2s API)_

**Turn 36 narration**:

Now let me apply HTR reduction:

- `tool#36` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=256s, wall=137s]
  → (empty result)
_(turn 37: 428 in / 85 out / 22,303 cached, ~$-0.0577, 1.6s API)_

- `tool#37` **apply_moves**({"slot":"main","moves":["R2","B2","U'","F2"]}) [sim=260s, wall=139s]
  → hist=17m
  slot=main [INV] hist(17m): `B' D' L' R' F' U' D' F2 U' F2 L R U R B2 U' F2`
_(turn 38: 383 in / 73 out / 22,884 cached, ~$-0.0595, 2.2s API)_

**Turn 38 narration**:

Good, 1 cancellation saved! Let me check if HTR reduction is complete:

- `tool#38` **quick_check**({"slot":"main"}) [sim=260s, wall=141s]
  → (empty result)
_(turn 39: 360 in / 108 out / 23,088 cached, ~$-0.0596, 2.2s API)_

**Turn 39 narration**:

HTR not yet reached. Let me get the next chunk:

- `tool#39` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=261s, wall=143s]
  → (empty result)
_(turn 40: 340 in / 72 out / 23,206 cached, ~$-0.0606, 4.8s API)_

- `tool#40` **apply_moves**({"slot":"main","moves":["D"]}) [sim=262s, wall=148s]
  → hist=18m
  slot=main [INV] hist(18m): `B' D' L' R' F' U' D' F2 U' F2 L R U R B2 U' F2 D`
_(turn 41: 330 in / 53 out / 23,473 cached, ~$-0.0616, 2.6s API)_

- `tool#41` **quick_check**({"slot":"main"}) [sim=262s, wall=151s]
  → (empty result)
_(turn 42: 327 in / 108 out / 23,704 cached, ~$-0.0614, 2.2s API)_

**Turn 42 narration**:

HTR reached at 18 moves! Now let me apply the finish:

- `tool#42` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=263s, wall=153s]
  → (empty result)
_(turn 43: 356 in / 85 out / 23,777 cached, ~$-0.0619, 1.6s API)_

- `tool#43` **apply_moves**({"slot":"main","moves":["B2","L2","D2","L2"]}) [sim=267s, wall=154s]
  → hist=22m
  slot=main [INV] hist(22m): `B' D' L' R' F' U' D' F2 U' F2 L R U R B2 U' F2 D B2 L2 D2 L2`
_(turn 44: 395 in / 53 out / 23,964 cached, ~$-0.0627, 2.4s API)_

- `tool#44` **quick_check**({"slot":"main"}) [sim=267s, wall=157s]
  → (empty result)
_(turn 45: 353 in / 100 out / 24,245 cached, ~$-0.0629, 2.4s API)_

**Turn 45 narration**:

Not solved yet. Let me continue:

- `tool#45` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=268s, wall=159s]
  → (empty result)
_(turn 46: 345 in / 85 out / 24,357 cached, ~$-0.0635, 2.1s API)_

- `tool#46` **apply_moves**({"slot":"main","moves":["D2","B2","R2","U2"]}) [sim=272s, wall=161s]
  → hist=26m
  slot=main [INV] hist(26m): `B' D' L' R' F' U' D' F2 U' F2 L R U R B2 U' F2 D B2 L2 D2 L2 D2 B2 R2 U2`
_(turn 47: 400 in / 53 out / 24,573 cached, ~$-0.0644, 1.4s API)_

- `tool#47` **quick_check**({"slot":"main"}) [sim=272s, wall=163s]
  → (empty result)
_(turn 48: 366 in / 91 out / 24,846 cached, ~$-0.0646, 2.9s API)_

- `tool#48` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=273s, wall=166s]
  → (empty result)
_(turn 49: 297 in / 81 out / 24,958 cached, ~$-0.0653, 1.9s API)_

- `tool#49` **apply_moves**({"slot":"main","moves":["F2","U2","R2"]}) [sim=276s, wall=167s]
  → hist=29m
  slot=main [INV] hist(29m): `B' D' L' R' F' U' D' F2 U' F2 L R U R B2 U' F2 D B2 L2 D2 L2 D2 B2 R2 U2 F2 U2 R2`
_(turn 50: 360 in / 53 out / 25,190 cached, ~$-0.0661, 1.3s API)_

- `tool#50` **quick_check**({"slot":"main"}) [sim=276s, wall=169s]
  → SOLVED
_(turn 51: 371 in / 84 out / 25,366 cached, ~$-0.0661, 2.5s API)_

**Turn 51 narration**:

Excellent! The cube is solved at 29 moves on the inverse. Now I need to compose the NISS solution:

- `tool#51` **compose_niss_solution**({"slot":"main"}) [sim=277s, wall=171s]
  → solves=True
_(turn 52: 407 in / 102 out / 25,530 cached, ~$-0.0662, 3.3s API)_

**Turn 52 narration**:

I have a 29-move solution. This is better than my first 30-move attempt but not better than the 25-move second attempt. Since I have budget and the solution is ≥27 moves, I should try replace_and_shorten once to see if I can improve it:

- `tool#52` **budget_status**({}) [sim=277s, wall=175s]
  → sim=277s
_(turn 53: 534 in / 186 out / 25,770 cached, ~$-0.0652, 4.5s API)_

**Turn 53 narration**:

I have plenty of budget (3323s remaining). Let me try replace_and_shorten. I'll target a large tail span from the beginning to see if I can shorten the entire solution. Actually, looking at the instructions, I should target a sub-sequence that looks "lumpy" (8+ moves). Let me try the DR+HTR portion:

- `tool#53` **replace_and_shorten**({"slot":"main","start":5,"end":29,"axis":"UD"}) [sim=277s, wall=179s]
  → ERROR: too few tool calls remaining (27) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 54: 514 in / 188 out / 26,027 cached, ~$-0.0659, 3.2s API)_

**Turn 54 narration**:

I don't have enough tool calls remaining for replace_and_shorten. Let me verify and submit my 29-move solution:

- `tool#54` **verify_solved**({"solution":["R2","U2","F2","U2","R2","B2","D2","L2","D2","L2","B2","D'","F2","U","B2","R'","U'","R'","L'","F2","U","...) [sim=277s, wall=182s]
  → solves=True, moves=29
_(turn 55: 423 in / 408 out / 26,322 cached, ~$-0.0637, 10.0s API)_

**Turn 55 narration**:

Perfect! The solution is verified at 29 moves. This is better than my first attempt (30 moves) but not as good as my second attempt (25 moves). However, I have a complete, verified solution within budget.

**FINAL_SOLUTION:** ["R2", "U2", "F2", "U2", "R2", "B2", "D2", "L2", "D2", "L2", "B2", "D'", "F2", "U", "B2", "R'", "U'", "R'", "L'", "F2", "U", "F2", "D", "U", "F", "R", "L", "D", "B"]

## Solution Summary

**Line:** Inverse-UD axis, DR-3C2E trigger
**Breakdown:**
- EO (inverse-UD): 5 moves (B' D' L' R' F')
- DR setup + trigger: 9 moves (U' D' F2 U' F2 L + R U R')
- HTR reduction: 5 moves (R2 B2 U' F2 D) with 1 cancellation
- HTR finish: 11 moves (B2 L2 D2 L2 D2 B2 R2 U2 F2 U2 R2)
**Total:** 29 moves

The DR-3C2E substate delivered on its promise (6-8 move typical post-DR cost would have been ~21-23, but I got 16 actual due to the subset). This is a clean, complete solve that beats my first attempt. The 25-move second attempt was likely a different branch or had better cancellations.

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 56: 14,306 in / 289 out / 12,867 cached, ~$0.0125, 4.6s API)_

### Turn 56 — thinking

> The user is right - I wrote "**FINAL_SOLUTION:**" in my narration but didn't actually output it in the correct format. I need to emit it properly now.
> 
> I have a verified 29-move solution:
> ["R2", "U2", "F2", "U2", "R2", "B2", "D2", "L2", "D2", "L2", "B2", "D'", "F2", "U", "B2", "R'", "U'", "R'", "L'", "F2", "U", "F2", "D", "U", "F", "R", "L", "D", "B"]
> 
> Let me output it correctly.

**Turn 56 narration**:

FINAL_SOLUTION: ["R2", "U2", "F2", "U2", "R2", "B2", "D2", "L2", "D2", "L2", "B2", "D'", "F2", "U", "B2", "R'", "U'", "R'", "L'", "F2", "U", "F2", "D", "U", "F", "R", "L", "D", "B"]


**verify_solved** ✓ — 29 moves: `R2 U2 F2 U2 R2 B2 D2 L2 D2 L2 B2 D' F2 U B2 R' U' R' L' F2 U F2 D U F R L D B`
