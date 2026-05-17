# Run — fm_PSSSideDayGdansk2026_s1__attempt8_20260517_094719.json

**Scramble**: `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (31 moves, 52 tool calls)  
**Sim budget**: 185s / 3600s  
**Wall time**: 269s  
**Tokens**: 43,712 in (1,116,027 cached), 6,528 out  
**Cost estimate**: $0.607  
**Solution**: `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U B2 D2 F2 R2 B2 F2 U2 F2 L2 R2`  

**Sim-time spent by tool**:

- `reset_slot`: 2× = 60s
- `apply_moves`: 14× = 41s
- `dr_trigger_options`: 3× = 24s
- `eo_pattern_lookup`: 6× = 18s
- `niss_flip`: 3× = 15s
- `dr_recognize`: 4× = 12s
- `apply_htr_phase`: 6× = 6s
- `inspect_state`: 1× = 5s
- `try_alg`: 1× = 2s
- `htr_classify`: 1× = 1s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 1,063 in / 274 out / 12,867 cached, ~$-0.0274, 10.3s API)_

### Turn 1 — thinking

> Looking at the prior attempts:
> - Attempts 1, 3, 5, 6: all **25 moves** with the same solution
> - Attempts 2, 4, 7: 29-31 moves with different solutions
> 
> The 25-move solution has been found 4 times, which suggests it's a solid line. Let me start by inspecting the current state to understand what's available, then commit to a path quickly.
> 
> The instruction is clear: COMMIT HARD. Pick a line and drive it through. Don't over-ideate. The best is 25 moves, so I should aim to either:
> 1. Follow the same axis/approach that got 25 moves
> 2. Find a clear improvement if I see one immediately
> 
> Let me start with inspect_state to see what we're working with.

**Turn 1 narration**:

I'll solve this scramble methodically, committing hard to the first viable line I find. Let me start by inspecting the state.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=10s]
  → EO: [], DR: [], bad_edges {'UD': 8, 'FB': 6, 'RL': 6}
_(turn 2: 900 in / 292 out / 12,867 cached, ~$-0.0277, 7.6s API)_

**Turn 2 narration**:

**Analysis of scramble state:**
- Bad edges: UD=8, FB=6, RL=6
- DR closeness: UD is DR-6C3E, FB is DR-5C2E, RL is DR-7C3E
- **Top_pairs_on_inverse=2 on UD** — this is a NISS signal
- FB has 6 bad edges AND DR-5C2E (better than UD's 6C3E)

The 8-bad on UD suggests NISS might help (pairs=2 confirms). FB with 6 bad edges and better DR state (5C2E vs 6C3E) looks promising. Let me scout EO on both normal and inverse frames for FB and UD axes.

**Scout plan:** Check FB-normal EO first (6 bad edges), then UD-inverse EO (8 bad → might become easier on inverse given pairs=2).

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=18s]
  → found=1, best=4m
_(turn 3: 1,321 in / 101 out / 12,867 cached, ~$-0.0293, 7.9s API)_

**Turn 3 narration**:

FB-normal EO is **5 moves total** (I see the first 4). Now let me check UD on the inverse side since pairs=2 suggests NISS might give a clean EO.

- `tool#3` **niss_flip**({"slot":"main"}) [sim=13s, wall=26s]
  → (empty result)
_(turn 4: 915 in / 96 out / 14,196 cached, ~$-0.0341, 36.5s API)_

**Turn 4 narration**:

Good, now I'm on the inverse side. Let me scout UD-axis EO here.

- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=16s, wall=62s]
  → found=1, best=4m
_(turn 5: 718 in / 103 out / 15,106 cached, ~$-0.0371, 3.5s API)_

**Turn 5 narration**:

UD-inverse is also **5 moves**. Both are the same length. Let me also check FB on inverse for completeness.

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=19s, wall=66s]
  → found=1, best=4m
_(turn 6: 457 in / 179 out / 15,337 cached, ~$-0.0374, 5.1s API)_

**Turn 6 narration**:

All three candidates (FB-normal, UD-inverse, FB-inverse) are **5 moves**. Now I need to probe DR for each to make the joint decision.

**Decision point:** All EOs are 5 moves. I'll probe DR for each:
1. FB-normal (5mv EO) with DR-5C2E base
2. UD-inverse (5mv EO) with pairs=2 signal
3. FB-inverse (5mv EO)

Let me flip back to normal and probe FB-normal first.

- `tool#6` **niss_flip**({"slot":"main"}) [sim=24s, wall=71s]
  → (empty result)
_(turn 7: 799 in / 133 out / 15,823 cached, ~$-0.0383, 9.2s API)_

**Turn 7 narration**:

Back on normal. Let me probe DR for FB-normal with the 5-move EO.

- `tool#7` **probe_dr_pattern**({"slot":"main","eo_alg":["R2","B'","L'","U2","?"],"axis":"FB"}) [sim=24s, wall=80s]
  → ERROR: ValueError: unparseable tokens in alg: '?'
_(turn 8: 730 in / 124 out / 16,056 cached, ~$-0.0393, 6.4s API)_

**Turn 8 narration**:

Right, the EO is 5 moves but I only see 4. Let me commit those 4 and then get the 5th move, THEN probe DR.

- `tool#8` **apply_moves**({"slot":"main","moves":["R2","B'","L'","U2"]}) [sim=28s, wall=87s]
  → hist=4m
  slot=main hist(4m): `R2 B' L' U2`
_(turn 9: 348 in / 73 out / 16,363 cached, ~$-0.0420, 5.9s API)_

- `tool#9` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=31s, wall=92s]
  → found=1, best=1m
_(turn 10: 335 in / 120 out / 16,886 cached, ~$-0.0428, 3.3s API)_

**Turn 10 narration**:

Good! The 5th move is R'. So FB-normal EO is `R2 B' L' U2 R'` (5 moves). Now let me apply it and check DR options.

- `tool#10` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=32s, wall=96s]
  → hist=5m
  slot=main hist(5m): `R2 B' L' U2 R'`
_(turn 11: 334 in / 91 out / 17,040 cached, ~$-0.0436, 2.7s API)_

- `tool#11` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=40s, wall=101s]
  → (empty result)
_(turn 12: 392 in / 98 out / 17,107 cached, ~$-0.0435, 4.1s API)_

**Turn 12 narration**:

No DR options within 5 setup moves on FB! This is bad. Let me try dr_recognize as a fallback.

- `tool#12` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=43s, wall=105s]
  → found=0
_(turn 13: 410 in / 162 out / 17,375 cached, ~$-0.0433, 4.2s API)_

**Turn 13 narration**:

FB-normal requires **9 moves to DR** after the 5-move EO. Total: 5+9=14 moves to DR. That's not good. Let me reset and try a different axis.

**Decision:** FB-normal is 14 moves to DR (too long). Let me try UD-inverse since it had pairs=2. I'll reset and go directly to that path.

- `tool#13` **reset_slot**({"slot":"main","rescramble":true}) [sim=73s, wall=109s]
  → (empty result)
_(turn 14: 401 in / 54 out / 17,646 cached, ~$-0.0456, 4.4s API)_

- `tool#14` **niss_flip**({"slot":"main"}) [sim=78s, wall=114s]
  → (empty result)
_(turn 15: 637 in / 119 out / 17,741 cached, ~$-0.0442, 3.0s API)_

**Turn 15 narration**:

Now on inverse. Let me commit the UD-inverse EO (5 moves: B' D' L' R' + 1 more).

- `tool#15` **apply_moves**({"slot":"main","moves":["B'","D'","L'","R'"]}) [sim=82s, wall=117s]
  → hist=4m
  slot=main [INV] hist(4m): `B' D' L' R'`
_(turn 16: 627 in / 74 out / 18,012 cached, ~$-0.0456, 2.1s API)_

- `tool#16` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=85s, wall=119s]
  → found=1, best=1m
_(turn 17: 334 in / 73 out / 18,045 cached, ~$-0.0466, 2.3s API)_

- `tool#17` **apply_moves**({"slot":"main","moves":["F'"]}) [sim=86s, wall=121s]
  → hist=5m
  slot=main [INV] hist(5m): `B' D' L' R' F'`
_(turn 18: 291 in / 132 out / 18,605 cached, ~$-0.0474, 2.9s API)_

**Turn 18 narration**:

**EO complete on UD-inverse:** `B' D' L' R' F'` (5 moves on inverse). Now let me check DR options on UD.

- `tool#18` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=94s, wall=127s]
  → (empty result)
_(turn 19: 391 in / 87 out / 18,672 cached, ~$-0.0479, 2.5s API)_

**Turn 19 narration**:

No options within 5 moves! Let me try dr_recognize.

- `tool#19` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=97s, wall=130s]
  → found=0
_(turn 20: 446 in / 193 out / 18,824 cached, ~$-0.0466, 5.7s API)_

**Turn 20 narration**:

UD-inverse is 5+8=**13 moves to DR**. Still long. Let me check the prior successful 25-move solutions — they likely used a different approach. Let me reset and try RL axis, or reconsider the normal side entirely.

Actually, wait — the prior 25-move solutions all start with `R2 D' F' B...`. Let me decode that: on normal side, those are regular moves. Let me see if that's a different EO approach. Let me reset and try RL-normal.

- `tool#20` **reset_slot**({"slot":"main","rescramble":true}) [sim=127s, wall=136s]
  → (empty result)
_(turn 21: 415 in / 74 out / 19,094 cached, ~$-0.0492, 2.1s API)_

- `tool#21` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=130s, wall=138s]
  → found=1, best=4m
_(turn 22: 418 in / 146 out / 19,302 cached, ~$-0.0487, 4.1s API)_

**Turn 22 narration**:

RL is also 5 moves. Actually, looking at the 25-move solution `R2 D' F' B ...`, that starts with `R2 D' F' B` which are 4 moves. Let me try those and see what happens.

- `tool#22` **try_alg**({"slot":"main","alg":["R2","D'","F'","B"]}) [sim=132s, wall=142s]
  → (empty result)
_(turn 23: 1,616 in / 153 out / 19,605 cached, ~$-0.0458, 3.8s API)_

**Turn 23 narration**:

**EXCELLENT!** `R2 D' F' B` gives **4-move EO on UD axis** (0 bad edges on UD). After EO, the state is DR-5C3E on UD. This is much better than my earlier attempts! Let me commit this path.

- `tool#23` **apply_moves**({"slot":"main","moves":["R2","D'","F'","B"]}) [sim=136s, wall=145s]
  → hist=4m
  slot=main hist(4m): `R2 D' F' B`
_(turn 24: 1,630 in / 130 out / 19,638 cached, ~$-0.0462, 2.8s API)_

**Turn 24 narration**:

**EO complete on UD-normal in 4 moves: `R2 D' F' B`**. Now let me find DR on UD axis.

- `tool#24` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=144s, wall=151s]
  → (empty result)
_(turn 25: 458 in / 93 out / 19,982 cached, ~$-0.0512, 2.5s API)_

**Turn 25 narration**:

No triggers within 5 moves. Let me use dr_recognize to see the full DR path.

- `tool#25` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=147s, wall=153s]
  → found=0
_(turn 26: 443 in / 137 out / 21,411 cached, ~$-0.0544, 3.9s API)_

**Turn 26 narration**:

DR is **8 moves** on UD after the 4-move EO. Total to DR: 4+8=12 moves. That's acceptable (under the 15-move intermediate target). Let me commit the DR setup.

- `tool#26` **apply_moves**({"slot":"main","moves":["R","B2","R'","D2"]}) [sim=151s, wall=157s]
  → hist=8m
  slot=main hist(8m): `R2 D' F' B R B2 R' D2`
_(turn 27: 406 in / 71 out / 21,604 cached, ~$-0.0560, 2.2s API)_

- `tool#27` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=154s, wall=159s]
  → found=1
_(turn 28: 375 in / 118 out / 21,818 cached, ~$-0.0560, 3.6s API)_

**Turn 28 narration**:

Perfect! DR trigger is visible: **setup `L D2 U'` + trigger `R'`** (4 moves total). Let me apply the setup first.

- `tool#28` **apply_moves**({"slot":"main","moves":["L","D2","U'"]}) [sim=157s, wall=163s]
  → hist=11m
  slot=main hist(11m): `R2 D' F' B R B2 R' D2 L D2 U'`
_(turn 29: 366 in / 73 out / 22,064 cached, ~$-0.0574, 2.1s API)_

- `tool#29` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=158s, wall=165s]
  → hist=12m
  slot=main hist(12m): `R2 D' F' B R B2 R' D2 L D2 U' R'`
_(turn 30: 359 in / 94 out / 22,145 cached, ~$-0.0573, 10.0s API)_

**Turn 30 narration**:

**DR complete in 12 moves!** Now let me classify the HTR state and finish.

- `tool#30` **htr_classify**({"slot":"main","axis":"UD"}) [sim=159s, wall=175s]
  → subset=[2, 0, 4, 3, 1, 7, 6, 5]
_(turn 31: 514 in / 199 out / 22,432 cached, ~$-0.0560, 5.1s API)_

**Turn 31 narration**:

HTR finish is **19 moves** (9 for HTR reduction + 10 for finish). Total so far: 12 (to DR) + 19 (HTR+finish) = **31 moves**. That's close to the prior 29-31 move attempts, but not as good as the 25-move solution.

Let me apply the HTR phases but also check for shortcuts (like a 3-cycle residual) along the way.

- `tool#31` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=160s, wall=180s]
  → (empty result)
_(turn 32: 660 in / 84 out / 22,524 cached, ~$-0.0576, 4.1s API)_

- `tool#32` **apply_moves**({"slot":"main","moves":["U2","R2","U","B2"]}) [sim=164s, wall=185s]
  → hist=16m
  slot=main hist(16m): `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2`
_(turn 33: 489 in / 71 out / 22,781 cached, ~$-0.0590, 3.2s API)_

**Turn 33 narration**:

Let me check if we've hit a 3-cycle or solved state early.

- `tool#33` **quick_check**({"slot":"main"}) [sim=164s, wall=188s]
  → (empty result)
_(turn 34: 369 in / 108 out / 23,248 cached, ~$-0.0600, 2.7s API)_

**Turn 34 narration**:

Not yet in HTR. Let me continue HTR reduction.

- `tool#34` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=165s, wall=190s]
  → (empty result)
_(turn 35: 398 in / 84 out / 23,365 cached, ~$-0.0606, 2.1s API)_

- `tool#35` **apply_moves**({"slot":"main","moves":["U","R2","U'","R2"]}) [sim=169s, wall=193s]
  → hist=20m
  slot=main hist(20m): `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2`
_(turn 36: 410 in / 53 out / 23,625 cached, ~$-0.0618, 2.6s API)_

- `tool#36` **quick_check**({"slot":"main"}) [sim=169s, wall=195s]
  → (empty result)
_(turn 37: 363 in / 94 out / 23,856 cached, ~$-0.0619, 2.7s API)_

- `tool#37` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=170s, wall=198s]
  → (empty result)
_(turn 38: 319 in / 72 out / 23,973 cached, ~$-0.0627, 2.0s API)_

- `tool#38` **apply_moves**({"slot":"main","moves":["U"]}) [sim=171s, wall=200s]
  → hist=21m
  slot=main hist(21m): `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U`
_(turn 39: 340 in / 53 out / 24,180 cached, ~$-0.0635, 1.9s API)_

- `tool#39` **quick_check**({"slot":"main"}) [sim=171s, wall=202s]
  → (empty result)
_(turn 40: 351 in / 106 out / 24,356 cached, ~$-0.0631, 4.8s API)_

**Turn 40 narration**:

Good! Now in HTR. Let me apply the finish phase.

- `tool#40` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=172s, wall=207s]
  → (empty result)
_(turn 41: 367 in / 85 out / 24,520 cached, ~$-0.0638, 4.0s API)_

- `tool#41` **apply_moves**({"slot":"main","moves":["B2","D2","F2","R2"]}) [sim=176s, wall=211s]
  → hist=25m
  slot=main hist(25m): `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U B2 D2 F2 R2`
_(turn 42: 417 in / 53 out / 24,718 cached, ~$-0.0647, 2.8s API)_

- `tool#42` **quick_check**({"slot":"main"}) [sim=176s, wall=213s]
  → (empty result)
_(turn 43: 377 in / 91 out / 24,997 cached, ~$-0.0650, 4.7s API)_

- `tool#43` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=177s, wall=218s]
  → (empty result)
_(turn 44: 349 in / 85 out / 25,109 cached, ~$-0.0655, 2.5s API)_

- `tool#44` **apply_moves**({"slot":"main","moves":["B2","F2","U2","F2"]}) [sim=181s, wall=221s]
  → hist=29m
  slot=main hist(29m): `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U B2 D2 F2 R2 B2 F2 U2 F2`
_(turn 45: 415 in / 53 out / 25,336 cached, ~$-0.0664, 1.9s API)_

- `tool#45` **quick_check**({"slot":"main"}) [sim=181s, wall=223s]
  → (empty result)
_(turn 46: 390 in / 91 out / 25,512 cached, ~$-0.0663, 2.5s API)_

- `tool#46` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=182s, wall=225s]
  → (empty result)
_(turn 47: 306 in / 77 out / 25,712 cached, ~$-0.0673, 2.8s API)_

- `tool#47` **apply_moves**({"slot":"main","moves":["L2","R2"]}) [sim=184s, wall=228s]
  → hist=31m
  slot=main hist(31m): `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U B2 D2 F2 R2 B2 F2 U2 F2 L2 R2`
_(turn 48: 372 in / 53 out / 25,955 cached, ~$-0.0682, 1.9s API)_

- `tool#48` **quick_check**({"slot":"main"}) [sim=184s, wall=230s]
  → SOLVED
_(turn 49: 387 in / 85 out / 26,131 cached, ~$-0.0681, 3.4s API)_

**Turn 49 narration**:

**SOLVED in 31 moves!** Now let me try to optimize with cancellation and see if there are obvious reductions.

- `tool#49` **compose_niss_solution**({"slot":"main"}) [sim=185s, wall=233s]
  → solves=True
_(turn 50: 432 in / 119 out / 26,291 cached, ~$-0.0679, 4.3s API)_

**Turn 50 narration**:

31 moves is not as good as the 25-move solution from prior attempts. However, I have a complete solution. Let me check if I should try replace_and_shorten. The tool says it's gated — I need ≥27 moves (yes, I have 31) and ≥30 tool calls remaining.

Let me check my budget status.

- `tool#50` **budget_status**({}) [sim=185s, wall=238s]
  → sim=185s
_(turn 51: 583 in / 314 out / 26,534 cached, ~$-0.0652, 8.8s API)_

**Turn 51 narration**:

I've used 185s of my 3600s budget — plenty of time remaining. The note says I should consider replace_and_shorten if gated. Let me count tool calls: I'm at about 40+ tool calls so far, so I definitely meet the ≥30 threshold. However, the instruction says "1-call cap" and I should only use it if I have a specific reason.

Looking at the solution, I notice several double moves that might be optimizable:
- Moves 13-15: `U2 R2 U` could potentially be part of a reducible sequence
- Moves 22-29: `B2 D2 F2 R2 B2 F2 U2 F2` is a long sequence of double turns

Let me try replace_and_shorten on a tail span. I'll target moves 12-31 (the HTR finish area).

- `tool#51` **replace_and_shorten**({"slot":"main","start":12,"end":31,"axis":"UD"}) [sim=185s, wall=246s]
  → ERROR: too few tool calls remaining (29) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 52: 679 in / 365 out / 26,792 cached, ~$-0.0648, 8.5s API)_

**Turn 52 narration**:

I don't have enough tool calls remaining for replace_and_shorten. Let me submit my current 31-move solution.

Actually, wait — looking at the 25-move solution from prior attempts: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`, I notice it also starts with `R2 D' F' B` (the same EO I used!). The difference must be in the DR/HTR path. But I'm not going to chase that now since the instruction says to **COMMIT HARD** and not over-ideate. I have a working 31-move solution, which is complete and verified.

Let me verify it one more time and submit.

- `tool#52` **verify_solved**({"solution":["R2","D'","F'","B","R","B2","R'","D2","L","D2","U'","R'","U2","R2","U","B2","U","R2","U'","R2","U","B2",...) [sim=185s, wall=255s]
  → solves=True, moves=31
_(turn 53: 741 in / 304 out / 27,115 cached, ~$-0.0664, 8.3s API)_

**Turn 53 narration**:

Perfect! Verified as solving in 31 moves.

## FINAL_SOLUTION

**Solution: 31 moves**

```
R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U B2 D2 F2 R2 B2 F2 U2 F2 L2 R2
```

**Breakdown:**
- **EO (UD-axis, 4 moves):** `R2 D' F' B` — a 4-move EO on UD using the symmetric flipping pattern (F and B both flip UD bad edges)
- **DR (8 moves):** `R B2 R' D2 L D2 U' R'` — setup moves + single R' trigger to reach DR-UD
- **HTR finish (19 moves):** 9 moves of HTR reduction + 10 moves of half-turn finish through the "2-swap long-cycle" HTR subset

This solution is complete and verified. While not matching the 25-move best from prior attempts, it demonstrates the standard FMC pipeline (EO → DR → HTR → finish) executed cleanly on this scramble.

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 54: 15,349 in / 162 out / 12,867 cached, ~$0.0137, 6.0s API)_

### Turn 54 — thinking

> The user is right - I need to actually emit the FINAL_SOLUTION in the correct format. Let me do that now.

**Turn 54 narration**:

FINAL_SOLUTION: ["R2", "D'", "F'", "B", "R", "B2", "R'", "D2", "L", "D2", "U'", "R'", "U2", "R2", "U", "B2", "U", "R2", "U'", "R2", "U", "B2", "D2", "F2", "R2", "B2", "F2", "U2", "F2", "L2", "R2"]


**verify_solved** ✓ — 31 moves: `R2 D' F' B R B2 R' D2 L D2 U' R' U2 R2 U B2 U R2 U' R2 U B2 D2 F2 R2 B2 F2 U2 F2 L2 R2`
