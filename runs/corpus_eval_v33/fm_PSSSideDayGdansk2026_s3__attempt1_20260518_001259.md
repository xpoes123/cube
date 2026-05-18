# Run — fm_PSSSideDayGdansk2026_s3__attempt1_20260518_001259.json

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (34 moves, 54 tool calls)  
**Sim budget**: 1245s / 3600s  
**Wall time**: 207s  
**Tokens**: 43,807 in (1,135,972 cached), 6,374 out  
**Cost estimate**: $0.657  
**Solution**: `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2 R2 F2`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 4× = 1068s
- `reset_slot`: 4× = 100s
- `dr_recognize`: 6× = 24s
- `htr_classify`: 1× = 15s
- `eo_pattern_lookup`: 4× = 12s
- `inspect_state`: 2× = 10s
- `apply_htr_phase`: 6× = 6s
- `apply_moves`: 15× = 5s
- `niss_flip`: 2× = 4s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 374 in / 214 out / 0 cached, ~$0.0043, 5.2s API)_

### Turn 1 — thinking

> The user wants me to solve the scramble within the one-hour budget. I should start with inspect_state(slot='main') as requested. The scramble is:
> 
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Let me begin by inspecting the state to understand the cube configuration, particularly the bad edges per axis, DR closeness, and HTR closeness.

**Turn 1 narration**:

I'll solve this FMC scramble step by step. Let me start by inspecting the cube state to understand what I'm working with.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=5s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 8, 'RL': 6}
_(turn 2: 820 in / 323 out / 12,986 cached, ~$-0.0278, 8.3s API)_

**Turn 2 narration**:

Good! I can see:
- **UD axis**: 4 bad edges (UL, DR, DL, DB) — best EO count
- **FB axis**: 8 bad edges — all-bad is costly
- **RL axis**: 6 bad edges

**Initial observation**: UD has the fewest bad edges (4), which typically means shortest EO. The bad edges are UL, DR, DL, DB. Let me analyze the flipping pattern: on UD-axis, F and B flips fix edges. I see DB is the only one on the B face, which is tricky.

**DR analysis from inspect**: DR-7C3E on UD (not JZP-eligible), DR-6C3E on FB, DR-5C3E on RL. However, `top_pairs_on_inverse: 3` on UD is a strong signal — this suggests the inverse frame might be very good.

Let me scout EO on **UD-normal** first, then check the **inverse** frame as the NISS-FIRST rule dictates.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=8s, wall=13s]
  → found=1, best=4m
_(turn 3: 1,230 in / 121 out / 12,986 cached, ~$-0.0296, 14.5s API)_

**Turn 3 narration**:

**UD-normal EO: 4 moves** (U L R' B'). That's reasonable for 4 bad edges. Now let me check the **inverse frame** on UD as well — the `top_pairs_on_inverse: 3` strongly suggests I should explore it.

- `tool#3` **niss_flip**({"slot":"main"}) [sim=10s, wall=28s]
  → (empty result)
_(turn 4: 950 in / 94 out / 13,566 cached, ~$-0.0324, 3.4s API)_

**Turn 4 narration**:

Now I'm on the inverse frame. Let me check EO on UD-inverse:

- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=13s, wall=31s]
  → found=1, best=4m
_(turn 5: 721 in / 156 out / 14,487 cached, ~$-0.0346, 3.0s API)_

**Turn 5 narration**:

**UD-inverse EO: 4 moves** (B' R' U B'). Same length as normal, so EO alone doesn't differentiate. But with `top_pairs_on_inverse: 3`, the inverse frame likely has a much better DR. Let me apply this EO and check DR options:

- `tool#5` **apply_moves**({"slot":"main","moves":["B'","R'","U","B'"]}) [sim=13s, wall=34s]
  → hist=4m
  slot=main [INV] hist(4m): `B' R' U B'`
_(turn 6: 402 in / 105 out / 14,696 cached, ~$-0.0369, 5.1s API)_

**Turn 6 narration**:

Now let me probe DR options on UD-inverse:

- `tool#6` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=321s, wall=42s]
  → (empty result)
_(turn 7: 707 in / 131 out / 15,206 cached, ~$-0.0370, 4.9s API)_

**Turn 7 narration**:

**0 DR options within 5 moves** on UD-inverse! That's a bad signal. Despite the high `top_pairs_on_inverse`, the actual DR is not materializing quickly. Let me fall back to `dr_recognize` to use the brain:

- `tool#7` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=325s, wall=47s]
  → found=0
_(turn 8: 805 in / 98 out / 15,451 cached, ~$-0.0378, 3.0s API)_

**Turn 8 narration**:

The brain suggests B2 (0.8 prob). This isn't looking good. Let me **abandon UD-inverse** and check **normal side** instead. Let me flip back to normal:

- `tool#8` **niss_flip**({"slot":"main"}) [sim=327s, wall=50s]
  → (empty result)
  slot=main hist(4m): `B' R' U B'`
_(turn 9: 857 in / 106 out / 15,619 cached, ~$-0.0380, 3.4s API)_

**Turn 9 narration**:

Now I'm back on normal with the inverse-side history (B' R' U B'). Let me reset and try UD-normal from scratch:

- `tool#9` **reset_slot**({"slot":"main","rescramble":true}) [sim=352s, wall=53s]
  → (empty result)
_(turn 10: 674 in / 99 out / 16,133 cached, ~$-0.0401, 3.4s API)_

**Turn 10 narration**:

Now applying UD-normal EO (U L R' B'):

- `tool#10` **apply_moves**({"slot":"main","moves":["U","L","R'","B'"]}) [sim=353s, wall=57s]
  → hist=4m
  slot=main hist(4m): `U L R' B'`
_(turn 11: 293 in / 103 out / 16,418 cached, ~$-0.0419, 2.6s API)_

**Turn 11 narration**:

Now checking DR options on UD-normal:

- `tool#11` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=585s, wall=62s]
  → (empty result)
_(turn 12: 643 in / 104 out / 16,967 cached, ~$-0.0423, 2.6s API)_

**Turn 12 narration**:

Also 0 options on UD-normal! This axis is looking bad. Let me try **FB axis** instead. Reset and check FB:

- `tool#12` **reset_slot**({"slot":"main","rescramble":true}) [sim=610s, wall=64s]
  → (empty result)
_(turn 13: 615 in / 73 out / 17,096 cached, ~$-0.0432, 3.4s API)_

- `tool#13` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=613s, wall=68s]
  → found=1, best=4m
_(turn 14: 289 in / 126 out / 17,261 cached, ~$-0.0438, 3.0s API)_

**Turn 14 narration**:

**FB-normal EO: 4 moves** (R' F D L'). 8 bad edges solved in 4 moves is very efficient! Let me apply and check DR:

- `tool#14` **apply_moves**({"slot":"main","moves":["R'","F","D","L'"]}) [sim=613s, wall=71s]
  → hist=4m
  slot=main hist(4m): `R' F D L'`
_(turn 15: 342 in / 91 out / 17,748 cached, ~$-0.0455, 1.9s API)_

- `tool#15` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=869s, wall=75s]
  → (empty result)
_(turn 16: 653 in / 89 out / 17,781 cached, ~$-0.0447, 2.3s API)_

**Turn 16 narration**:

Also 0 on FB! Let me try **RL axis**:

- `tool#16` **reset_slot**({"slot":"main","rescramble":true}) [sim=894s, wall=77s]
  → (empty result)
_(turn 17: 583 in / 74 out / 18,065 cached, ~$-0.0459, 4.1s API)_

- `tool#17` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=897s, wall=81s]
  → found=1, best=4m
_(turn 18: 314 in / 137 out / 18,130 cached, ~$-0.0460, 3.9s API)_

**Turn 18 narration**:

**RL EO: 5 moves** (partial shown). That's longer than the others. Let me stick with FB-normal (4-move EO on 8 bad edges) and use `dr_recognize` with the brain to find DR iteratively. Resetting to FB:

- `tool#18` **reset_slot**({"slot":"main","rescramble":true}) [sim=922s, wall=85s]
  → (empty result)
_(turn 19: 361 in / 83 out / 18,688 cached, ~$-0.0481, 2.9s API)_

- `tool#19` **apply_moves**({"slot":"main","moves":["R'","F","D","L'"]}) [sim=922s, wall=88s]
  → hist=4m
  slot=main hist(4m): `R' F D L'`
_(turn 20: 301 in / 85 out / 18,721 cached, ~$-0.0484, 2.0s API)_

**Turn 20 narration**:

Now using `dr_recognize` to get brain suggestions for FB:

- `tool#20` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=926s, wall=90s]
  → found=0
_(turn 21: 405 in / 96 out / 19,059 cached, ~$-0.0488, 3.1s API)_

**Turn 21 narration**:

Brain suggests R2 (0.342 prob) for FB. Let me try it and iterate:

- `tool#21` **apply_moves**({"slot":"main","moves":["R2"]}) [sim=927s, wall=93s]
  → hist=5m
  slot=main hist(5m): `R' F D L' R2`
_(turn 22: 421 in / 70 out / 19,092 cached, ~$-0.0492, 1.6s API)_

- `tool#22` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=931s, wall=95s]
  → found=0
_(turn 23: 405 in / 82 out / 19,319 cached, ~$-0.0497, 1.9s API)_

**Turn 23 narration**:

Suggests L2. Applying:

- `tool#23` **apply_moves**({"slot":"main","moves":["L2"]}) [sim=931s, wall=97s]
  → hist=5m
  slot=main hist(5m): `R' F D R2 L`
_(turn 24: 389 in / 89 out / 19,602 cached, ~$-0.0504, 3.0s API)_

**Turn 24 narration**:

Good! Auto-cancelled L' + L2 → L. Let me continue:

- `tool#24` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=935s, wall=100s]
  → found=0
_(turn 25: 406 in / 89 out / 19,671 cached, ~$-0.0506, 1.7s API)_

**Turn 25 narration**:

Very high prob for D2 (0.816). Applying:

- `tool#25` **apply_moves**({"slot":"main","moves":["D2"]}) [sim=935s, wall=102s]
  → hist=6m
  slot=main hist(6m): `R' F D R2 L D2`
_(turn 26: 416 in / 70 out / 20,007 cached, ~$-0.0517, 1.6s API)_

- `tool#26` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=939s, wall=103s]
  → found=0
_(turn 27: 396 in / 80 out / 20,161 cached, ~$-0.0520, 4.1s API)_

**Turn 27 narration**:

Suggests D. Applying:

- `tool#27` **apply_moves**({"slot":"main","moves":["D"]}) [sim=939s, wall=107s]
  → hist=6m
  slot=main hist(6m): `R' F D R2 L D'`
_(turn 28: 386 in / 84 out / 20,436 cached, ~$-0.0528, 2.1s API)_

**Turn 28 narration**:

Cancelled D2 + D → D'. Continuing:

- `tool#28` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=943s, wall=109s]
  → found=0
_(turn 29: 400 in / 154 out / 20,508 cached, ~$-0.0519, 4.4s API)_

**Turn 29 narration**:

Suggests B2. I'm at 6 moves total from EO, and DR is still not found. This is getting long. Let me try a different approach. Let me use `dr_trigger_options` with max_setup=6 to see if there are longer setups:

- `tool#29` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":6}) [sim=1215s, wall=116s]
  → (empty result)
_(turn 30: 910 in / 200 out / 20,841 cached, ~$-0.0505, 6.0s API)_

**Turn 30 narration**:

Excellent! Found **DR-4C4E in 9 moves total** from current state: setup (L2 B U' F' B) + trigger (U F2 L2 U). But wait — I've already done 6 moves (R' F D R2 L D'). So from EO end, this would be **6 + 9 = 15 moves to DR**. That's borderline acceptable (elite target is sub-11). The pre_trigger_signature is DR-4C2E (not bad). Let me undo my last exploration moves and apply this clean path. First let me check my current state:

- `tool#30` **inspect_state**({"slot":"main"}) [sim=1220s, wall=122s]
  → EO: ['FB'], DR: [], bad_edges {'UD': 8, 'FB': 0, 'RL': 6}
_(turn 31: 1,439 in / 146 out / 20,994 cached, ~$-0.0502, 3.2s API)_

**Turn 31 narration**:

I see I'm at **FB-EO solved** with 6 moves. Now applying the DR setup + trigger (L2 B U' F' B U F2 L2 U):

- `tool#31` **apply_moves**({"slot":"main","moves":["L2","B","U'","F'","B","U","F2","L2","U"]}) [sim=1221s, wall=125s]
  → hist=15m
  slot=main hist(15m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U`
_(turn 32: 1,026 in / 80 out / 21,335 cached, ~$-0.0533, 2.7s API)_

**Turn 32 narration**:

**15 moves to DR**. Now let me verify I'm at DR and proceed to HTR. Let me check:

- `tool#32` **quick_check**({"slot":"main"}) [sim=1221s, wall=128s]
  → (empty result)
_(turn 33: 427 in / 94 out / 22,040 cached, ~$-0.0568, 5.9s API)_

**Turn 33 narration**:

Perfect! **FB-DR is solved**. Now I need to classify the HTR subset and finish:

- `tool#33` **htr_classify**({"slot":"main","axis":"FB"}) [sim=1236s, wall=135s]
  → subset=[1, 0, 2, 7, 4, 3, 6, 5]
_(turn 34: 554 in / 188 out / 22,787 cached, ~$-0.0570, 4.2s API)_

**Turn 34 narration**:

HTR subset: **2-swap mostly-axial**, htr_reduction = 11 moves, finish = 10 moves, total = 21 moves from DR. That's quite long! Total solution would be **15 (to DR) + 21 (finish) = 36 moves**. That's not great, but let me proceed and see if there are any opportunistic shortcuts via analyze_residual checks:

- `tool#34` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1237s, wall=141s]
  → (empty result)
_(turn 35: 651 in / 97 out / 22,968 cached, ~$-0.0586, 2.4s API)_

**Turn 35 narration**:

Partial — 4 moves shown. Applying:

- `tool#35` **apply_moves**({"slot":"main","moves":["U2","F'","R2","F"]}) [sim=1237s, wall=143s]
  → hist=18m
  slot=main hist(18m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F`
_(turn 36: 485 in / 64 out / 23,185 cached, ~$-0.0602, 2.4s API)_

**Turn 36 narration**:

Let me check if solved or interesting residual:

- `tool#36` **quick_check**({"slot":"main"}) [sim=1237s, wall=145s]
  → (empty result)
_(turn 37: 370 in / 103 out / 23,654 cached, ~$-0.0612, 3.8s API)_

**Turn 37 narration**:

Not solved. Continuing HTR reduction:

- `tool#37` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1238s, wall=149s]
  → (empty result)
_(turn 38: 376 in / 85 out / 23,864 cached, ~$-0.0620, 1.7s API)_

- `tool#38` **apply_moves**({"slot":"main","moves":["R2","F'","L2","D2"]}) [sim=1239s, wall=151s]
  → hist=22m
  slot=main hist(22m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2`
_(turn 39: 402 in / 53 out / 24,041 cached, ~$-0.0629, 1.8s API)_

- `tool#39` **quick_check**({"slot":"main"}) [sim=1239s, wall=153s]
  → (empty result)
_(turn 40: 360 in / 97 out / 24,267 cached, ~$-0.0630, 2.0s API)_

**Turn 40 narration**:

Continuing:

- `tool#40` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=1240s, wall=155s]
  → (empty result)
_(turn 41: 319 in / 80 out / 24,384 cached, ~$-0.0637, 1.8s API)_

- `tool#41` **apply_moves**({"slot":"main","moves":["F'","R2","B"]}) [sim=1240s, wall=157s]
  → hist=25m
  slot=main hist(25m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B`
_(turn 42: 362 in / 68 out / 24,598 cached, ~$-0.0643, 3.8s API)_

**Turn 42 narration**:

HTR reduction complete (25 moves). Now the finish phase:

- `tool#42` **quick_check**({"slot":"main"}) [sim=1240s, wall=160s]
  → (empty result)
_(turn 43: 378 in / 102 out / 24,868 cached, ~$-0.0645, 2.4s API)_

**Turn 43 narration**:

Great! Now in HTR. Applying finish:

- `tool#43` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1241s, wall=163s]
  → (empty result)
_(turn 44: 367 in / 85 out / 24,948 cached, ~$-0.0650, 2.8s API)_

- `tool#44` **apply_moves**({"slot":"main","moves":["B2","U2","L2","U2"]}) [sim=1241s, wall=166s]
  → hist=28m
  slot=main hist(28m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2`
_(turn 45: 413 in / 53 out / 25,233 cached, ~$-0.0661, 1.4s API)_

- `tool#45` **quick_check**({"slot":"main"}) [sim=1241s, wall=167s]
  → (empty result)
_(turn 46: 378 in / 90 out / 25,458 cached, ~$-0.0663, 1.9s API)_

- `tool#46` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1242s, wall=169s]
  → (empty result)
_(turn 47: 337 in / 85 out / 25,569 cached, ~$-0.0668, 2.0s API)_

- `tool#47` **apply_moves**({"slot":"main","moves":["R2","B2","D2","U2"]}) [sim=1243s, wall=171s]
  → hist=32m
  slot=main hist(32m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2`
_(turn 48: 414 in / 53 out / 25,807 cached, ~$-0.0676, 2.9s API)_

- `tool#48` **quick_check**({"slot":"main"}) [sim=1243s, wall=174s]
  → (empty result)
_(turn 49: 391 in / 90 out / 25,983 cached, ~$-0.0676, 1.8s API)_

- `tool#49` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=1244s, wall=176s]
  → (empty result)
_(turn 50: 294 in / 77 out / 26,181 cached, ~$-0.0687, 1.9s API)_

- `tool#50` **apply_moves**({"slot":"main","moves":["R2","F2"]}) [sim=1244s, wall=178s]
  → hist=34m
  slot=main hist(34m): `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2 R2 F2`
_(turn 51: 371 in / 53 out / 26,435 cached, ~$-0.0695, 3.3s API)_

- `tool#51` **quick_check**({"slot":"main"}) [sim=1244s, wall=181s]
  → SOLVED
_(turn 52: 388 in / 87 out / 26,611 cached, ~$-0.0694, 3.1s API)_

**Turn 52 narration**:

**SOLVED in 34 moves!** Now let me use compose_niss_solution to get the canonical solution with cancellations:

- `tool#52` **compose_niss_solution**({"slot":"main"}) [sim=1245s, wall=184s]
  → solves=True
_(turn 53: 435 in / 83 out / 26,769 cached, ~$-0.0697, 3.1s API)_

**Turn 53 narration**:

**34-move solution verified!** Now, following the rules, since this is ≥27 moves, I should try replace_and_shorten ONCE if I have enough budget. Let me check budget:

- `tool#53` **budget_status**({}) [sim=1245s, wall=187s]
  → sim=1245s
_(turn 54: 562 in / 173 out / 27,023 cached, ~$-0.0687, 4.5s API)_

**Turn 54 narration**:

I have plenty of budget left (2354s sim remaining). The solution is 34 moves. Per the rules, I should try replace_and_shorten on a large span. Let me try the tail end — maybe start=10, end=34 (the DR+HTR+finish part):

- `tool#54` **replace_and_shorten**({"slot":"main","start":10,"end":34,"axis":"FB"}) [sim=1245s, wall=192s]
  → ERROR: too few tool calls remaining (26) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 55: 504 in / 412 out / 27,283 cached, ~$-0.0660, 9.6s API)_

**Turn 55 narration**:

I don't have enough tool calls remaining (need 30, have 26). That's OK — the solution is valid at 34 moves. Let me submit it:

**FINAL_SOLUTION**: ["R'", "F", "D", "R2", "L", "D'", "L2", "B", "U'", "F'", "B", "U", "F2", "L2", "U'", "F'", "R2", "F", "R2", "F'", "L2", "D2", "F'", "R2", "B'", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "R2", "F2"]

**Solution summary:**
- **EO (FB-axis)**: R' F D L' → 4 moves (8 bad edges)
- **DR (FB-axis)**: R2 L D' L2 B U' F' B U F2 L2 U → 11 more moves (15 total to DR)
- **HTR reduction**: U' F' R2 F R2 F' L2 D2 F' R2 B' → 10 moves (25 total)
- **HTR finish**: U2 L2 U2 R2 B2 D2 U2 R2 F2 → 9 moves (34 total)

The solve took the **FB-axis** route with a 4-move EO on 8 bad edges (very efficient). The DR was long at 15 moves (borderline acceptable), and the HTR subset (2-swap mostly-axial) required a long finish. Total: **34 moves verified**.

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 56: 15,336 in / 350 out / 12,986 cached, ~$0.0162, 5.5s API)_

### Turn 56 — thinking

> The user is right - I narrated the solution but didn't actually emit it in the correct format. I need to output the FINAL_SOLUTION in the exact format requested.
> 
> Looking back at my compose_niss_solution result, I have a verified 34-move solution:
> ["R'", "F", "D", "R2", "L", "D'", "L2", "B", "U'", "F'", "B", "U", "F2", "L2", "U'", "F'", "R2", "F", "R2", "F'", "L2", "D2", "F'", "R2", "B'", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "R2", "F2"]
> 
> I should output this now as the FINAL_SOLUTION.

**Turn 56 narration**:

FINAL_SOLUTION: ["R'", "F", "D", "R2", "L", "D'", "L2", "B", "U'", "F'", "B", "U", "F2", "L2", "U'", "F'", "R2", "F", "R2", "F'", "L2", "D2", "F'", "R2", "B'", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "R2", "F2"]


**verify_solved** ✓ — 34 moves: `R' F D R2 L D' L2 B U' F' B U F2 L2 U' F' R2 F R2 F' L2 D2 F' R2 B' U2 L2 U2 R2 B2 D2 U2 R2 F2`
