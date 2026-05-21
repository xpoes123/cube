# Run — fm_PSSSideDayGdansk2026_s2__attempt1_20260521_011536.json

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: ✓ SOLVED (44 moves, 85 tool calls)  
**Sim budget**: 370s / 3600s  
**Wall time**: 526s  
**Tokens**: 131,440 in (4,191,250 cached), 27,388 out  
**Cost estimate**: $2.439  
**Solution**: `U2 R2 F2 U2 L2 F2 U2 B2 U2 L2 F2 D' F2 U2 R2 U' F2 U2 R2 U' B2 L' D2 F2 U2 B2 R' D' U' B R2 F2 D' L2 R2 U' F D' F' R2 D U2 R U2`  

**Sim-time spent by tool**:

- `dr_progress_options`: 12× = 180s
- `htr_classify`: 3× = 45s
- `inspect_state`: 7× = 35s
- `replace_and_shorten`: 1× = 30s
- `try_alg`: 14× = 21s
- `eo_pattern_lookup`: 6× = 18s
- `brain_suggest`: 4× = 12s
- `lookahead`: 1× = 8s
- `niss_flip`: 3× = 6s
- `apply_htr_phase`: 6× = 6s
- `apply_moves`: 17× = 6s
- `bookmark_fork`: 1× = 2s
- `undo_moves`: 4× = 1s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 467 in / 97 out / 0 cached, ~$0.0029, 2.1s API)_

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=2s]
  → EO: [], DR: [], bad_edges {'UD': 6, 'FB': 4, 'RL': 4}
_(turn 2: 799 in / 664 out / 18,669 cached, ~$-0.0380, 10.8s API)_

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=13s]
  → found=1, best=4m
- `tool#3` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=11s, wall=13s]
  → found=1, best=4m
_(turn 3: 1,881 in / 264 out / 18,669 cached, ~$-0.0408, 5.0s API)_

**Turn 3 narration**:

Both axes have 4-move EOs. Let me also check inverse-side for these to find the cleanest joint EO+DR.

- `tool#4` **niss_flip**({"slot":"main"}) [sim=13s, wall=18s]
  → (empty result)
_(turn 4: 1,293 in / 169 out / 19,130 cached, ~$-0.0452, 4.8s API)_

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=16s, wall=23s]
  → found=1, best=2m
- `tool#6` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=19s, wall=23s]
  → found=1, best=4m
_(turn 5: 1,222 in / 193 out / 20,696 cached, ~$-0.0493, 3.9s API)_

**Turn 5 narration**:

Excellent — inverse-FB has a **2-move EO** (U2 R'). That dominates. Committing.

- `tool#7` **apply_moves**({"slot":"main","moves":["U2","R'"]}) [sim=19s, wall=27s]
  → hist=2m
  slot=main [INV] hist(2m): `U2 R'`
_(turn 6: 880 in / 66 out / 21,378 cached, ~$-0.0541, 1.7s API)_

- `tool#8` **inspect_state**({"slot":"main"}) [sim=24s, wall=28s]
  → EO: ['FB'], DR: [], bad_edges {'UD': 6, 'FB': 0, 'RL': 4}
_(turn 7: 1,082 in / 253 out / 22,073 cached, ~$-0.0526, 5.0s API)_

**Turn 7 narration**:

EO complete (FB axis solved). DR-FB shows 5C2E — let me search DR options.

- `tool#9` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":4,"k":6}) [sim=31s, wall=34s]
  → (empty result)
_(turn 8: 1,952 in / 224 out / 22,726 cached, ~$-0.0521, 4.5s API)_

**Turn 8 narration**:

Going with `U B' U` (3 moves) to DR-2C1E, then re-query for the final approach.

- `tool#10` **apply_moves**({"slot":"main","moves":["U","B'","U"]}) [sim=31s, wall=38s]
  → hist=5m
  slot=main [INV] hist(5m): `U2 R' U B' U`
_(turn 9: 1,435 in / 136 out / 22,867 cached, ~$-0.0554, 2.7s API)_

- `tool#11` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":4,"k":6}) [sim=37s, wall=41s]
  → (empty result)
_(turn 10: 1,252 in / 220 out / 23,964 cached, ~$-0.0576, 4.1s API)_

**Turn 10 narration**:

Depth 4 doesn't reduce. Try depth 5.

- `tool#12` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":6}) [sim=60s, wall=47s]
  → (empty result)
_(turn 11: 2,036 in / 1,217 out / 25,110 cached, ~$-0.0434, 19.2s API)_

**Turn 11 narration**:

The 5-mv options start with `U` which cancel-merges with my trailing `U` (saves 1 move). Picking `U R2 F2 L2 D` → lands at DR-2C0E.

- `tool#13` **apply_moves**({"slot":"main","moves":["U","R2","F2","L2","D"]}) [sim=61s, wall=66s]
  → hist=9m
  slot=main [INV] hist(9m): `U2 R' U B' U2 R2 F2 L2 D`
_(turn 12: 2,473 in / 136 out / 25,261 cached, ~$-0.0587, 2.4s API)_

- `tool#14` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":6}) [sim=75s, wall=70s]
  → (empty result)
_(turn 13: 1,276 in / 399 out / 26,483 cached, ~$-0.0617, 6.4s API)_

- `tool#15` **brain_suggest**({"slot":"main","step":"dr","k":8}) [sim=78s, wall=76s]
  → (empty result)
- `tool#16` **inspect_state**({"slot":"main"}) [sim=83s, wall=76s]
  → EO: ['FB', 'RL'], DR: [], bad_edges {'UD': 6, 'FB': 0, 'RL': 0}
_(turn 14: 2,426 in / 204 out / 28,651 cached, ~$-0.0670, 4.2s API)_

**Turn 14 narration**:

Brain strongly suggests `R2`. Apply and check.

- `tool#17` **try_alg**({"slot":"main","alg":["R2"]}) [sim=84s, wall=80s]
  → (empty result)
_(turn 15: 2,805 in / 188 out / 28,818 cached, ~$-0.0666, 3.6s API)_

- `tool#18` **apply_moves**({"slot":"main","moves":["R2"]}) [sim=84s, wall=84s]
  → hist=10m
  slot=main [INV] hist(10m): `U2 R' U B' U2 R2 F2 L2 D R2`
_(turn 16: 1,834 in / 110 out / 30,219 cached, ~$-0.0744, 2.3s API)_

- `tool#19` **brain_suggest**({"slot":"main","step":"dr","k":6}) [sim=87s, wall=86s]
  → (empty result)
_(turn 17: 567 in / 92 out / 31,585 cached, ~$-0.0822, 2.7s API)_

- `tool#20` **apply_moves**({"slot":"main","moves":["U2"]}) [sim=87s, wall=89s]
  → hist=11m
  slot=main [INV] hist(11m): `U2 R' U B' U2 R2 F2 L2 D R2 U2`
_(turn 18: 553 in / 110 out / 32,966 cached, ~$-0.0857, 2.0s API)_

- `tool#21` **brain_suggest**({"slot":"main","step":"dr","k":6}) [sim=90s, wall=91s]
  → (empty result)
_(turn 19: 570 in / 193 out / 33,326 cached, ~$-0.0854, 4.7s API)_

- `tool#22` **inspect_state**({"slot":"main"}) [sim=95s, wall=96s]
  → EO: ['FB', 'RL'], DR: [], bad_edges {'UD': 6, 'FB': 0, 'RL': 0}
_(turn 20: 1,271 in / 850 out / 33,721 cached, ~$-0.0745, 14.1s API)_

- `tool#23` **try_alg**({"slot":"main","alg":["R","U2","R'"]}) [sim=97s, wall=110s]
  → (empty result)
- `tool#24` **try_alg**({"slot":"main","alg":["F2","R","U2","R'","F2"]}) [sim=98s, wall=110s]
  → (empty result)
_(turn 21: 4,610 in / 2,503 out / 33,989 cached, ~$-0.0404, 38.8s API)_

**Turn 21 narration**:

Brain looping on U2 — that's a stuck signal. Let me undo the R2 U2 and try a different DR setup direction.

- `tool#25` **undo_moves**({"slot":"main","n":2}) [sim=99s, wall=149s]
  → hist=9m
  slot=main [INV] hist(9m): `U2 R' U B' U2 R2 F2 L2 D`
_(turn 22: 5,719 in / 208 out / 34,383 cached, ~$-0.0726, 4.4s API)_

- `tool#26` **bookmark_fork**({"slot":"main","name":"post-EO-2C0E","description":"9 moves in (EO+5mv setup), at DR-2C0E on FB. Need short corner-tw...) [sim=101s, wall=153s]
  → (empty result)
_(turn 23: 631 in / 382 out / 36,221 cached, ~$-0.0902, 7.4s API)_

- `tool#27` **lookahead**({"slot":"main","target":"solved","axis":"FB"}) [sim=109s, wall=161s]
  → found=0
_(turn 24: 711 in / 189 out / 41,690 cached, ~$-0.1076, 3.9s API)_

**Turn 24 narration**:

Let me back up further to the 2C1E state and try alternate DR setups.

- `tool#28` **undo_moves**({"slot":"main","n":4}) [sim=109s, wall=165s]
  → hist=5m
  slot=main [INV] hist(5m): `U2 R' U B' U2`
_(turn 25: 474 in / 462 out / 41,842 cached, ~$-0.1046, 7.6s API)_

- `tool#29` **inspect_state**({"slot":"main"}) [sim=114s, wall=173s]
  → EO: ['FB'], DR: [], bad_edges {'UD': 6, 'FB': 0, 'RL': 4}
_(turn 26: 1,485 in / 188 out / 42,232 cached, ~$-0.1068, 4.7s API)_

- `tool#30` **undo_moves**({"slot":"main","n":1}) [sim=114s, wall=177s]
  → hist=4m
  slot=main [INV] hist(4m): `U2 R' U B'`
_(turn 27: 1,119 in / 91 out / 42,951 cached, ~$-0.1112, 1.9s API)_

- `tool#31` **apply_moves**({"slot":"main","moves":["U"]}) [sim=114s, wall=179s]
  → hist=5m
  slot=main [INV] hist(5m): `U2 R' U B' U`
_(turn 28: 377 in / 136 out / 43,088 cached, ~$-0.1132, 2.4s API)_

- `tool#32` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=137s, wall=183s]
  → (empty result)
_(turn 29: 1,589 in / 766 out / 44,347 cached, ~$-0.1035, 12.8s API)_

**Turn 29 narration**:

Let me back up to the pure post-EO state and search DR at depth 5 directly (skip the 2C1E intermediate).

- `tool#33` **undo_moves**({"slot":"main","n":3}) [sim=138s, wall=196s]
  → hist=2m
  slot=main [INV] hist(2m): `U2 R'`
_(turn 30: 2,194 in / 136 out / 44,669 cached, ~$-0.1120, 2.5s API)_

- `tool#34` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=170s, wall=202s]
  → (empty result)
_(turn 31: 1,612 in / 512 out / 44,912 cached, ~$-0.1087, 8.7s API)_

**Turn 31 narration**:

Excellent — depth-5 finds `U2 D' R2 F D` (5 moves) landing at **DR-0C2E** (only 2 slice edges off, no corner twists). Much better than the 2C0E branch. Committing.

- `tool#35` **apply_moves**({"slot":"main","moves":["U2","D'","R2","F","D"]}) [sim=170s, wall=210s]
  → hist=7m
  slot=main [INV] hist(7m): `U2 R' U2 D' R2 F D`
_(turn 32: 1,933 in / 136 out / 47,116 cached, ~$-0.1194, 2.5s API)_

- `tool#36` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=184s, wall=214s]
  → (empty result)
_(turn 33: 1,677 in / 430 out / 47,242 cached, ~$-0.1161, 8.1s API)_

- `tool#37` **brain_suggest**({"slot":"main","step":"dr","k":8}) [sim=187s, wall=222s]
  → (empty result)
_(turn 34: 2,025 in / 2,240 out / 49,152 cached, ~$-0.0930, 35.3s API)_

**Turn 34 narration**:

Top option "F' U R2 L2 D" lands at 0C1E. Let me commit and continue.

- `tool#38` **apply_moves**({"slot":"main","moves":["F'","U","R2","L2","D"]}) [sim=188s, wall=257s]
  → hist=12m
  slot=main [INV] hist(12m): `U2 R' U2 D' R2 F D F' U R2 L2 D`
_(turn 35: 2,739 in / 136 out / 49,311 cached, ~$-0.1229, 2.7s API)_

- `tool#39` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=200s, wall=261s]
  → (empty result)
_(turn 36: 1,597 in / 377 out / 50,721 cached, ~$-0.1265, 7.5s API)_

- `tool#40` **inspect_state**({"slot":"main"}) [sim=205s, wall=269s]
  → EO: ['FB'], DR: [], bad_edges {'UD': 4, 'FB': 0, 'RL': 2}
_(turn 37: 2,343 in / 854 out / 53,713 cached, ~$-0.1252, 13.6s API)_

- `tool#41` **try_alg**({"slot":"main","alg":["F","R","L","F'"]}) [sim=206s, wall=282s]
  → (empty result)
- `tool#42` **try_alg**({"slot":"main","alg":["B","R","L","B'"]}) [sim=208s, wall=282s]
  → (empty result)
- `tool#43` **try_alg**({"slot":"main","alg":["F2","R","L","F2"]}) [sim=209s, wall=282s]
  → (empty result)
_(turn 38: 6,467 in / 995 out / 53,890 cached, ~$-0.1112, 15.8s API)_

**Turn 38 narration**:

Let me try NISS flipping — the current 0C1E might resolve cleanly on the other side.

- `tool#44` **niss_flip**({"slot":"main"}) [sim=211s, wall=298s]
  → (empty result)
  slot=main hist(12m): `U2 R' U2 D' R2 F D F' U R2 L2 D`
_(turn 39: 6,606 in / 136 out / 55,202 cached, ~$-0.1272, 2.5s API)_

- `tool#45` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=214s, wall=300s]
  → ERROR: EO not yet solved on axis FB; run eo_pattern_lookup and apply EO moves first.
_(turn 40: 946 in / 140 out / 57,132 cached, ~$-0.1493, 4.2s API)_

- `tool#46` **inspect_state**({"slot":"main"}) [sim=219s, wall=305s]
  → EO: [], DR: [], bad_edges {'UD': 6, 'FB': 4, 'RL': 4}
_(turn 41: 1,107 in / 411 out / 63,042 cached, ~$-0.1607, 7.0s API)_

- `tool#47` **niss_flip**({"slot":"main"}) [sim=221s, wall=312s]
  → (empty result)
  slot=main [INV] hist(12m): `U2 R' U2 D' R2 F D F' U R2 L2 D`
_(turn 42: 1,865 in / 919 out / 63,656 cached, ~$-0.1525, 14.6s API)_

- `tool#48` **try_alg**({"slot":"main","alg":["U","R2","U'","L2"]}) [sim=223s, wall=326s]
  → (empty result)
- `tool#49` **try_alg**({"slot":"main","alg":["D","L2","D'","R2"]}) [sim=224s, wall=326s]
  → (empty result)
- `tool#50` **try_alg**({"slot":"main","alg":["U2","R2","D2","L2"]}) [sim=226s, wall=326s]
  → (empty result)
_(turn 43: 5,967 in / 962 out / 63,920 cached, ~$-0.1403, 16.4s API)_

**Turn 43 narration**:

Switching strategy — UD has 4 bad edges and is only 2C2E for DR. Cheaper to do UD-EO + UD-DR than continue FB. Let me lookup UD EO.

- `tool#51` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=229s, wall=343s]
  → found=1, best=3m
- `tool#52` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=232s, wall=343s]
  → found=1, best=3m
_(turn 44: 5,982 in / 482 out / 64,899 cached, ~$-0.1501, 7.9s API)_

- `tool#53` **try_alg**({"slot":"main","alg":["F2","R2","B'"]}) [sim=233s, wall=351s]
  → (empty result)
- `tool#54` **try_alg**({"slot":"main","alg":["D","F'","D'"]}) [sim=235s, wall=351s]
  → (empty result)
_(turn 45: 4,012 in / 1,274 out / 66,751 cached, ~$-0.1491, 18.7s API)_

**Turn 45 narration**:

Path A (`F2 R2 B'`) is brilliant — solves UD-EO without breaking FB-EO, leaving us at **UD-axis 4C0E** (4 unoriented corners, 0 slice edges off — essentially JZP-ready). Apply it.

- `tool#55` **apply_moves**({"slot":"main","moves":["F2","R2","B'"]}) [sim=235s, wall=369s]
  → hist=15m
  slot=main [INV] hist(15m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B'`
_(turn 46: 4,503 in / 136 out / 72,155 cached, ~$-0.1793, 4.0s API)_

- `tool#56` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":10}) [sim=257s, wall=375s]
  → (empty result)
_(turn 47: 1,701 in / 384 out / 73,132 cached, ~$-0.1866, 5.9s API)_

- `tool#57` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":8}) [sim=268s, wall=382s]
  → (empty result)
_(turn 48: 2,678 in / 714 out / 77,356 cached, ~$-0.1901, 10.4s API)_

- `tool#58` **try_alg**({"slot":"main","alg":["R","F2","R'"]}) [sim=270s, wall=392s]
  → (empty result)
- `tool#59` **try_alg**({"slot":"main","alg":["L","F2","L'"]}) [sim=271s, wall=392s]
  → (empty result)
- `tool#60` **try_alg**({"slot":"main","alg":["R","U2","L","F2","L'","U2","R'"]}) [sim=273s, wall=392s]
  → (empty result)
_(turn 49: 5,932 in / 775 out / 77,545 cached, ~$-0.1800, 13.7s API)_

**Turn 49 narration**:

Let me commit the 5-move setup `U D R B2 R` → 0C1E and continue.

- `tool#61` **apply_moves**({"slot":"main","moves":["U","D","R","B2","R"]}) [sim=273s, wall=406s]
  → hist=20m
  slot=main [INV] hist(20m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 R`
_(turn 50: 5,362 in / 136 out / 78,955 cached, ~$-0.1951, 2.7s API)_

- `tool#62` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":10}) [sim=286s, wall=409s]
  → (empty result)
_(turn 51: 1,628 in / 568 out / 80,970 cached, ~$-0.2052, 9.1s API)_

**Turn 51 narration**:

🎯 **DR FOUND!** `R' U2 F2 D2 L` reaches DR. And since my last move was `R`, the leading `R'` cancels — saving 1 move (net 4 moves to DR).

- `tool#63` **apply_moves**({"slot":"main","moves":["R'","U2","F2","D2","L"]}) [sim=286s, wall=419s]
  → hist=23m
  slot=main [INV] hist(23m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L`
_(turn 52: 1,967 in / 89 out / 86,047 cached, ~$-0.2251, 2.1s API)_

- `tool#64` **htr_classify**({"slot":"main","axis":"UD"}) [sim=301s, wall=445s]
  → subset=[1, 0, 3, 5, 2, 4, 7, 6]
_(turn 53: 826 in / 496 out / 86,252 cached, ~$-0.2230, 8.2s API)_

**Turn 53 narration**:

HTR is 21 moves — total ~44. Too long. Let me check the other axes' HTR subset to see if any is cheaper.

- `tool#65` **htr_classify**({"slot":"main","axis":"FB"}) [sim=316s, wall=453s]
  → ERROR: could not compute HTR phases for this subset.
- `tool#66` **htr_classify**({"slot":"main","axis":"RL"}) [sim=331s, wall=453s]
  → ERROR: could not compute HTR phases for this subset.
_(turn 54: 1,168 in / 230 out / 88,138 cached, ~$-0.2310, 4.8s API)_

**Turn 54 narration**:

UD is our only DR axis. Apply HTR reduction.

- `tool#67` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=332s, wall=458s]
  → (empty result)
_(turn 55: 863 in / 103 out / 88,355 cached, ~$-0.2344, 2.6s API)_

- `tool#68` **apply_moves**({"slot":"main","moves":["B2","U","R2","U2"]}) [sim=333s, wall=461s]
  → hist=27m
  slot=main [INV] hist(27m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L B2 U R2 U2`
_(turn 56: 668 in / 65 out / 89,272 cached, ~$-0.2381, 2.2s API)_

- `tool#69` **quick_check**({"slot":"main"}) [sim=333s, wall=463s]
  → (empty result)
_(turn 57: 518 in / 119 out / 89,843 cached, ~$-0.2392, 2.4s API)_

- `tool#70` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=334s, wall=466s]
  → (empty result)
_(turn 58: 551 in / 103 out / 90,054 cached, ~$-0.2399, 2.4s API)_

- `tool#71` **apply_moves**({"slot":"main","moves":["F2","U","R2","U2"]}) [sim=334s, wall=468s]
  → hist=31m
  slot=main [INV] hist(31m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L B2 U R2 U2 F2 U R2 U2`
_(turn 59: 563 in / 119 out / 90,390 cached, ~$-0.2406, 3.0s API)_

- `tool#72` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=335s, wall=471s]
  → (empty result)
_(turn 60: 535 in / 95 out / 90,675 cached, ~$-0.2418, 2.3s API)_

- `tool#73` **apply_moves**({"slot":"main","moves":["F2","D"]}) [sim=335s, wall=473s]
  → hist=33m
  slot=main [INV] hist(33m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L B2 U R2 U2 F2 U R2 U2 F2 D`
_(turn 61: 518 in / 65 out / 91,006 cached, ~$-0.2432, 2.0s API)_

- `tool#74` **quick_check**({"slot":"main"}) [sim=335s, wall=475s]
  → (empty result)
_(turn 62: 540 in / 202 out / 91,357 cached, ~$-0.2420, 3.8s API)_

**Turn 62 narration**:

HTR reached. Apply finish phase.

- `tool#75` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=336s, wall=479s]
  → (empty result)
_(turn 63: 627 in / 104 out / 91,644 cached, ~$-0.2440, 2.3s API)_

- `tool#76` **apply_moves**({"slot":"main","moves":["F2","L2","U2","B2"]}) [sim=337s, wall=481s]
  → hist=37m
  slot=main [INV] hist(37m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L B2 U R2 U2 F2 U R2 U2 F2 D F2 L2 U2 B2`
_(turn 64: 696 in / 65 out / 91,994 cached, ~$-0.2453, 2.6s API)_

- `tool#77` **quick_check**({"slot":"main"}) [sim=337s, wall=484s]
  → (empty result)
_(turn 65: 556 in / 115 out / 92,482 cached, ~$-0.2463, 2.2s API)_

- `tool#78` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=338s, wall=486s]
  → (empty result)
_(turn 66: 540 in / 104 out / 92,686 cached, ~$-0.2471, 2.2s API)_

- `tool#79` **apply_moves**({"slot":"main","moves":["U2","F2","L2","U2"]}) [sim=338s, wall=488s]
  → hist=41m
  slot=main [INV] hist(41m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L B2 U R2 U2 F2 U R2 U2 F2 D F2 L2 U2 B2 U2 F2 L2 U2`
_(turn 67: 596 in / 115 out / 93,061 cached, ~$-0.2478, 2.8s API)_

- `tool#80` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=339s, wall=491s]
  → (empty result)
_(turn 68: 567 in / 100 out / 93,346 cached, ~$-0.2488, 2.4s API)_

- `tool#81` **apply_moves**({"slot":"main","moves":["F2","R2","U2"]}) [sim=339s, wall=494s]
  → hist=44m
  slot=main [INV] hist(44m): `U2 R' U2 D' R2 F D F' U R2 L2 D F2 R2 B' U D R B2 U2 F2 D2 L B2 U R2 U2 F2 U R2 U2 F2 D F2 L2 U2 B2 U2 F2 L2 U2 F2 R2 U2`
_(turn 69: 564 in / 65 out / 93,666 cached, ~$-0.2502, 2.1s API)_

- `tool#82` **quick_check**({"slot":"main"}) [sim=339s, wall=496s]
  → SOLVED
_(turn 70: 584 in / 334 out / 94,057 cached, ~$-0.2472, 7.4s API)_

**Turn 70 narration**:

Solved at 44 moves on inverse — way too long. Let me try replace_and_shorten on the lumpy DR setup span.

- `tool#83` **compose_niss_solution**({"slot":"main"}) [sim=340s, wall=503s]
  → solves=True
_(turn 71: 918 in / 134 out / 94,337 cached, ~$-0.2499, 2.8s API)_

- `tool#84` **replace_and_shorten**({"slot":"main","start":4,"end":44,"axis":"UD"}) [sim=370s, wall=508s]
  → ERROR: could not solve micro-scramble for span [4:44]: no DR found
_(turn 72: 697 in / 479 out / 94,736 cached, ~$-0.2465, 8.5s API)_

**Turn 72 narration**:

R&S failed (1-call cap used). 44 moves it is — within the 50-move acceptability threshold. Verify and ship.

- `tool#85` **verify_solved**({"solution":["U2","R2","F2","U2","L2","F2","U2","B2","U2","L2","F2","D'","F2","U2","R2","U'","F2","U2","R2","U'","B2"...) [sim=370s, wall=517s]
  → solves=True, moves=44
_(turn 73: 713 in / 524 out / 95,356 cached, ~$-0.2475, 9.7s API)_

**Turn 73 narration**:

Verified. The solve narrative:
- **EO** (2 mv, inverse-FB): `U2 R'`
- **DR setup** (5 mv, lumpy because the 2C0E branch was sticky): `U2 D' R2 F D`
- **More DR setup** (5 mv to 0C1E): `F' U R2 L2 D`
- **Pivot to UD-axis** (3 mv solving UD-EO without breaking FB-EO): `F2 R2 B'`
- **UD-DR reach** (8 mv after cancellation): `U D R B2 U2 F2 D2 L`
- **HTR reduction** (10 mv) + **finish** (11 mv): half-turn slabs

44 moves is long — the DR phase was inefficient because the 0C1E "1 misplaced slice edge" substate doesn't reduce within the depth-5 BFS horizon. A cleaner DR path would have saved 8–10 moves but the search-and-commit loop committed before I saw the trap.

FINAL_SOLUTION: ["U2", "R2", "F2", "U2", "L2", "F2", "U2", "B2", "U2", "L2", "F2", "D'", "F2", "U2", "R2", "U'", "F2", "U2", "R2", "U'", "B2", "L'", "D2", "F2", "U2", "B2", "R'", "D'", "U'", "B", "R2", "F2", "D'", "L2", "R2", "U'", "F", "D'", "F'", "R2", "D", "U2", "R", "U2"]


**verify_solved** ✓ — 44 moves: `U2 R2 F2 U2 L2 F2 U2 B2 U2 L2 F2 D' F2 U2 R2 U' F2 U2 R2 U' B2 L' D2 F2 U2 B2 R' D' U' B R2 F2 D' L2 R2 U' F D' F' R2 D U2 R U2`
