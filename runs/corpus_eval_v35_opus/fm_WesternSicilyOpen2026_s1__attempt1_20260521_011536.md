# Run — fm_WesternSicilyOpen2026_s1__attempt1_20260521_011536.json

**Scramble**: `R' U' F U2 F2 D2 B2 D B' U L' B' F2 R2 U' L2 F2 B2 D' F2 L2 F R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: ✓ SOLVED (34 moves, 82 tool calls)  
**Sim budget**: 279s / 3600s  
**Wall time**: 683s  
**Tokens**: 124,097 in (4,257,010 cached), 23,697 out  
**Cost estimate**: $2.360  
**Solution**: `R2 F2 U2 B2 U2 B2 R2 F2 U2 R2 U2 L' F2 U2 R2 D2 R U2 R U2 B' D2 R2 U2 F' B' L' F2 L U2 L' U2 D R2`  

**Sim-time spent by tool**:

- `dr_progress_options`: 12× = 99s
- `replace_and_shorten`: 1× = 30s
- `inspect_state`: 5× = 25s
- `reset_slot`: 1× = 25s
- `try_alg`: 14× = 21s
- `brain_suggest`: 7× = 21s
- `eo_pattern_lookup`: 5× = 15s
- `htr_classify`: 1× = 15s
- `lookahead`: 1× = 8s
- `niss_flip`: 3× = 6s
- `apply_htr_phase`: 6× = 6s
- `apply_moves`: 19× = 6s
- `analyze_residual`: 1× = 2s
- `compose_niss_solution`: 1× = 1s
- `undo_moves`: 1× = 0s

---

_(turn 1: 467 in / 93 out / 0 cached, ~$0.0028, 2.4s API)_

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=2s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 6, 'RL': 4}
_(turn 2: 799 in / 1,355 out / 18,682 cached, ~$-0.0277, 20.5s API)_

**Turn 2 narration**:

EO scouting: UD=4 bad, FB=6 bad, RL=4 bad. UD and RL are the two cheap-EO candidates. Let me check eo_pattern_lookup on both.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=8s, wall=23s]
  → found=1, best=4m
- `tool#3` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=11s, wall=23s]
  → found=1, best=4m
_(turn 3: 2,570 in / 297 out / 18,682 cached, ~$-0.0383, 5.7s API)_

**Turn 3 narration**:

Both 4-move EOs. Let me probe DR cost for each by try_alg'ing the EO then peeking at dr_progress_options. Also check inverse for FB.

- `tool#4` **try_alg**({"slot":"main","alg":["D","R","U2","F'"]}) [sim=12s, wall=29s]
  → (empty result)
_(turn 4: 2,484 in / 302 out / 19,143 cached, ~$-0.0397, 6.1s API)_

- `tool#5` **try_alg**({"slot":"main","alg":["U2","F2","R","D'"]}) [sim=14s, wall=35s]
  → (empty result)
_(turn 5: 3,609 in / 408 out / 21,311 cached, ~$-0.0406, 8.0s API)_

**Turn 5 narration**:

UD-EO lands at DR-4C2E with FB-axis also showing 3C2E (interesting cross-axis structure). RL-EO lands at DR-4C2E too. Comparable. Let me commit UD-EO and probe DR.

- `tool#6` **apply_moves**({"slot":"main","moves":["D","R","U2","F'"]}) [sim=14s, wall=43s]
  → hist=4m
  slot=main hist(4m): `D R U2 F'`
_(turn 6: 2,160 in / 136 out / 22,109 cached, ~$-0.0512, 3.0s API)_

- `tool#7` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":8}) [sim=21s, wall=46s]
  → (empty result)
_(turn 7: 1,473 in / 921 out / 23,709 cached, ~$-0.0458, 15.1s API)_

**Turn 7 narration**:

No trigger lands within 4 moves. Best is 2C1E in 4 moves. Let me probe a couple of these candidates to see which has a near DR.

- `tool#8` **try_alg**({"slot":"main","alg":["U2","R","U","R'"]}) [sim=23s, wall=61s]
  → (empty result)
- `tool#9` **try_alg**({"slot":"main","alg":["U'","F2","R"]}) [sim=24s, wall=61s]
  → (empty result)
_(turn 8: 5,073 in / 179 out / 26,024 cached, ~$-0.0524, 3.6s API)_

**Turn 8 narration**:

Going with U2 R U R' → 2C1E. Commit and re-query.

- `tool#10` **apply_moves**({"slot":"main","moves":["U2","R","U","R'"]}) [sim=25s, wall=65s]
  → hist=8m
  slot=main hist(8m): `D R U2 F' U2 R U R'`
_(turn 9: 3,588 in / 136 out / 26,171 cached, ~$-0.0579, 2.8s API)_

- `tool#11` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":8}) [sim=31s, wall=68s]
  → (empty result)
_(turn 10: 1,436 in / 517 out / 28,226 cached, ~$-0.0641, 7.9s API)_

**Turn 10 narration**:

2C0E in 4 moves available. Let me try if known 2C triggers hit DR directly from the current 2C1E state first.

- `tool#12` **try_alg**({"slot":"main","alg":["R","U2","R'"]}) [sim=32s, wall=76s]
  → (empty result)
- `tool#13` **try_alg**({"slot":"main","alg":["R","U","R'"]}) [sim=34s, wall=76s]
  → (empty result)
- `tool#14` **try_alg**({"slot":"main","alg":["R","U'","R'"]}) [sim=35s, wall=76s]
  → (empty result)
_(turn 11: 6,060 in / 350 out / 31,560 cached, ~$-0.0618, 6.8s API)_

**Turn 11 narration**:

Commit D2 L' U' L → 2C0E.

- `tool#15` **apply_moves**({"slot":"main","moves":["D2","L'","U'","L"]}) [sim=36s, wall=83s]
  → hist=12m
  slot=main hist(12m): `D R U2 F' U2 R U R' D2 L' U' L`
_(turn 12: 5,291 in / 136 out / 31,721 cached, ~$-0.0677, 2.4s API)_

- `tool#16` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":8}) [sim=40s, wall=85s]
  → (empty result)
_(turn 13: 1,429 in / 488 out / 33,243 cached, ~$-0.0781, 9.1s API)_

**Turn 13 narration**:

Depth 4 doesn't reach DR. Let me look depth 5.

- `tool#17` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=54s, wall=95s]
  → (empty result)
_(turn 14: 2,512 in / 315 out / 38,268 cached, ~$-0.0911, 6.0s API)_

**Turn 14 narration**:

Depth 5 still can't fix 2C0E — these corners need a longer EO-preserving alg. Let me consult brain.

- `tool#18` **brain_suggest**({"slot":"main","step":"dr","k":8}) [sim=57s, wall=101s]
  → (empty result)
_(turn 15: 1,789 in / 132 out / 38,444 cached, ~$-0.0965, 3.0s API)_

- `tool#19` **apply_moves**({"slot":"main","moves":["U'"]}) [sim=57s, wall=104s]
  → hist=13m
  slot=main hist(13m): `D R U2 F' U2 R U R' D2 L' U' L U'`
_(turn 16: 749 in / 110 out / 40,081 cached, ~$-0.1043, 2.7s API)_

- `tool#20` **brain_suggest**({"slot":"main","step":"dr","k":5}) [sim=60s, wall=107s]
  → (empty result)
_(turn 17: 546 in / 92 out / 41,408 cached, ~$-0.1088, 2.5s API)_

- `tool#21` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=60s, wall=110s]
  → hist=14m
  slot=main hist(14m): `D R U2 F' U2 R U R' D2 L' U' L U' R'`
_(turn 18: 532 in / 110 out / 41,732 cached, ~$-0.1094, 2.1s API)_

- `tool#22` **brain_suggest**({"slot":"main","step":"dr","k":5}) [sim=63s, wall=112s]
  → (empty result)
_(turn 19: 549 in / 136 out / 42,045 cached, ~$-0.1098, 3.9s API)_

- `tool#23` **inspect_state**({"slot":"main"}) [sim=68s, wall=116s]
  → EO: ['UD'], DR: [], bad_edges {'UD': 0, 'FB': 4, 'RL': 4}
_(turn 20: 1,203 in / 1,030 out / 42,410 cached, ~$-0.0954, 18.1s API)_

**Turn 20 narration**:

That broke things — went from 2C0E to 5C2E. Let me undo and try a different tack.

- `tool#24` **undo_moves**({"slot":"main","n":2}) [sim=68s, wall=134s]
  → hist=12m
  slot=main hist(12m): `D R U2 F' U2 R U R' D2 L' U' L`
_(turn 21: 2,005 in / 650 out / 42,687 cached, ~$-0.0995, 13.1s API)_

**Turn 21 narration**:

Trusting the brain may need a longer 2-twist alg. Let me brain-walk a few more moves but watch closely.

- `tool#25` **apply_moves**({"slot":"main","moves":["U'","R'"]}) [sim=68s, wall=147s]
  → hist=14m
  slot=main hist(14m): `D R U2 F' U2 R U R' D2 L' U' L U' R'`
_(turn 22: 1,085 in / 110 out / 43,051 cached, ~$-0.1113, 2.3s API)_

- `tool#26` **brain_suggest**({"slot":"main","step":"dr","k":3}) [sim=71s, wall=149s]
  → (empty result)
_(turn 23: 600 in / 304 out / 45,031 cached, ~$-0.1152, 5.8s API)_

- `tool#27` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=72s, wall=155s]
  → hist=14m
  slot=main hist(14m): `D R U2 F' U2 R U R' D2 L' U' L U' R2`
_(turn 24: 697 in / 66 out / 45,843 cached, ~$-0.1207, 2.2s API)_

- `tool#28` **inspect_state**({"slot":"main"}) [sim=77s, wall=157s]
  → EO: ['UD', 'FB'], DR: [], bad_edges {'UD': 0, 'FB': 0, 'RL': 4}
_(turn 25: 1,039 in / 360 out / 46,027 cached, ~$-0.1158, 6.7s API)_

**Turn 25 narration**:

Now UD is at 2C0E and FB is also EO-solved! Brain-walk one more.

- `tool#29` **brain_suggest**({"slot":"main","step":"dr","k":5}) [sim=80s, wall=164s]
  → (empty result)
_(turn 26: 1,402 in / 91 out / 46,345 cached, ~$-0.1196, 2.1s API)_

- `tool#30` **apply_moves**({"slot":"main","moves":["D"]}) [sim=80s, wall=166s]
  → hist=15m
  slot=main hist(15m): `D R U2 F' U2 R U R' D2 L' U' L U' R2 D`
_(turn 27: 644 in / 110 out / 46,834 cached, ~$-0.1229, 2.8s API)_

- `tool#31` **brain_suggest**({"slot":"main","step":"dr","k":3}) [sim=83s, wall=169s]
  → (empty result)
_(turn 28: 505 in / 266 out / 48,049 cached, ~$-0.1242, 4.9s API)_

- `tool#32` **inspect_state**({"slot":"main"}) [sim=88s, wall=174s]
  → EO: ['UD', 'FB'], DR: [], bad_edges {'UD': 0, 'FB': 0, 'RL': 2}
_(turn 29: 1,248 in / 536 out / 48,302 cached, ~$-0.1186, 7.8s API)_

- `tool#33` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":4,"k":8}) [sim=94s, wall=182s]
  → (empty result)
- `tool#34` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":8}) [sim=99s, wall=182s]
  → (empty result)
_(turn 30: 3,462 in / 536 out / 48,581 cached, ~$-0.1127, 10.9s API)_

**Turn 30 narration**:

Both DRs stuck at 2-twist. Let me try NISS to see what the inverse state looks like.

- `tool#35` **niss_flip**({"slot":"main"}) [sim=101s, wall=193s]
  → (empty result)
  slot=main [INV] hist(15m): `D R U2 F' U2 R U R' D2 L' U' L U' R2 D`
_(turn 31: 3,450 in / 136 out / 48,898 cached, ~$-0.1196, 2.5s API)_

- `tool#36` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":8}) [sim=104s, wall=195s]
  → ERROR: EO not yet solved on axis UD; run eo_pattern_lookup and apply EO moves first.
_(turn 32: 967 in / 124 out / 50,476 cached, ~$-0.1315, 4.0s API)_

- `tool#37` **inspect_state**({"slot":"main"}) [sim=109s, wall=199s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 6, 'RL': 6}
_(turn 33: 1,113 in / 796 out / 53,163 cached, ~$-0.1283, 13.5s API)_

- `tool#38` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=112s, wall=213s]
  → found=1, best=4m
_(turn 34: 1,838 in / 402 out / 53,798 cached, ~$-0.1337, 7.3s API)_

- `tool#39` **niss_flip**({"slot":"main"}) [sim=114s, wall=220s]
  → (empty result)
  slot=main hist(15m): `D R U2 F' U2 R U R' D2 L' U' L U' R2 D`
_(turn 35: 1,219 in / 110 out / 54,062 cached, ~$-0.1407, 2.2s API)_

- `tool#40` **lookahead**({"slot":"main","target":"solved","axis":"UD"}) [sim=122s, wall=223s]
  → found=0
_(turn 36: 893 in / 1,602 out / 55,047 cached, ~$-0.1219, 26.1s API)_

**Turn 36 narration**:

Let me try brain again from current state — might be a longer alg.

- `tool#41` **brain_suggest**({"slot":"main","step":"dr","k":5}) [sim=125s, wall=249s]
  → (empty result)
_(turn 37: 2,003 in / 195 out / 56,024 cached, ~$-0.1423, 3.8s API)_

- `tool#42` **apply_moves**({"slot":"main","moves":["D'"]}) [sim=125s, wall=253s]
  → hist=14m
  slot=main hist(14m): `D R U2 F' U2 R U R' D2 L' U' L U' R2`
_(turn 38: 745 in / 1,741 out / 57,062 cached, ~$-0.1257, 26.9s API)_

**Turn 38 narration**:

Let me try some known 2-twist DR-preserving algs.

- `tool#43` **try_alg**({"slot":"main","alg":["R2","U2","R'","F2","R","U2","R'","F2","R'"]}) [sim=126s, wall=280s]
  → (empty result)
- `tool#44` **try_alg**({"slot":"main","alg":["R","U2","R'","F2","R","U2","R'","F2"]}) [sim=128s, wall=280s]
  → (empty result)
- `tool#45` **try_alg**({"slot":"main","alg":["F2","R","U2","R'","F2","L'","U2","L"]}) [sim=129s, wall=280s]
  → (empty result)
_(turn 39: 6,295 in / 900 out / 58,922 cached, ~$-0.1267, 15.7s API)_

**Turn 39 narration**:

Stuck in a 2C0E well that needs 7+ extra moves. Let me reset and try a different DR path. Budget is ample.

- `tool#46` **reset_slot**({"slot":"main"}) [sim=154s, wall=295s]
  → (empty result)
_(turn 40: 5,699 in / 326 out / 59,175 cached, ~$-0.1378, 6.3s API)_

**Turn 40 narration**:

Fresh start. Let me try inverse-side EO this time — the inverse perspective showed potentially better DR substates.

- `tool#47` **niss_flip**({"slot":"main"}) [sim=156s, wall=302s]
  → (empty result)
_(turn 41: 1,031 in / 169 out / 61,091 cached, ~$-0.1593, 3.4s API)_

- `tool#48` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=159s, wall=305s]
  → found=1, best=2m
- `tool#49` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=162s, wall=305s]
  → found=1, best=2m
_(turn 42: 1,166 in / 329 out / 66,566 cached, ~$-0.1713, 6.2s API)_

**Turn 42 narration**:

2-move EOs on inverse! Big improvement. Let me try both candidates.

- `tool#50` **try_alg**({"slot":"main","alg":["L'","F'"]}) [sim=164s, wall=311s]
  → (empty result)
- `tool#51` **try_alg**({"slot":"main","alg":["R2","D'"]}) [sim=165s, wall=311s]
  → (empty result)
_(turn 43: 4,033 in / 436 out / 67,003 cached, ~$-0.1623, 8.0s API)_

**Turn 43 narration**:

R2 D' lands at DR-4C2E on RL — clean trigger family. Committing.

- `tool#52` **apply_moves**({"slot":"main","moves":["R2","D'"]}) [sim=165s, wall=319s]
  → hist=2m
  slot=main [INV] hist(2m): `R2 D'`
_(turn 44: 3,966 in / 136 out / 67,699 cached, ~$-0.1688, 3.1s API)_

- `tool#53` **dr_progress_options**({"slot":"main","axis":"RL","max_depth":4,"k":8}) [sim=172s, wall=323s]
  → (empty result)
_(turn 45: 1,483 in / 301 out / 68,345 cached, ~$-0.1756, 5.1s API)_

- `tool#54` **try_alg**({"slot":"main","alg":["U","R2","U2","R2"]}) [sim=174s, wall=328s]
  → (empty result)
- `tool#55` **try_alg**({"slot":"main","alg":["U2","L","U2","B"]}) [sim=175s, wall=328s]
  → (empty result)
_(turn 46: 4,540 in / 152 out / 72,083 cached, ~$-0.1787, 3.0s API)_

- `tool#56` **apply_moves**({"slot":"main","moves":["U2","L","U2","B"]}) [sim=176s, wall=331s]
  → hist=6m
  slot=main [INV] hist(6m): `R2 D' U2 L U2 B`
_(turn 47: 3,531 in / 136 out / 72,224 cached, ~$-0.1824, 2.4s API)_

- `tool#57` **dr_progress_options**({"slot":"main","axis":"RL","max_depth":4,"k":8}) [sim=182s, wall=334s]
  → (empty result)
_(turn 48: 1,304 in / 188 out / 73,770 cached, ~$-0.1924, 3.3s API)_

- `tool#58` **dr_progress_options**({"slot":"main","axis":"RL","max_depth":5,"k":8}) [sim=205s, wall=339s]
  → (empty result)
_(turn 49: 2,336 in / 323 out / 76,900 cached, ~$-0.1958, 5.5s API)_

**Turn 49 narration**:

5-move setup to 0C1E — excellent! Just 1 slice edge off. Commit and re-query.

- `tool#59` **apply_moves**({"slot":"main","moves":["B'","L'","F2","L","B"]}) [sim=206s, wall=344s]
  → hist=9m
  slot=main [INV] hist(9m): `R2 D' U2 L U2 L' F2 L B`
_(turn 50: 1,626 in / 202 out / 77,208 cached, ~$-0.2006, 3.4s API)_

- `tool#60` **dr_progress_options**({"slot":"main","axis":"RL","max_depth":4,"k":5}) [sim=210s, wall=348s]
  → (empty result)
_(turn 51: 1,267 in / 598 out / 78,356 cached, ~$-0.1988, 10.6s API)_

- `tool#61` **dr_progress_options**({"slot":"main","axis":"RL","max_depth":5,"k":5}) [sim=223s, wall=359s]
  → (empty result)
_(turn 52: 2,193 in / 651 out / 80,004 cached, ~$-0.1997, 10.9s API)_

**Turn 52 narration**:

DR in 5 more moves! Total DR = 14 inverse-moves. Committing.

- `tool#62` **apply_moves**({"slot":"main","moves":["F","U2","R2","D2","B"]}) [sim=223s, wall=370s]
  → hist=14m
  slot=main [INV] hist(14m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B`
_(turn 53: 1,640 in / 65 out / 80,170 cached, ~$-0.2106, 2.4s API)_

- `tool#63` **quick_check**({"slot":"main"}) [sim=223s, wall=373s]
  → (empty result)
_(turn 54: 577 in / 178 out / 81,163 cached, ~$-0.2147, 3.7s API)_

**Turn 54 narration**:

DR on RL! Time for HTR.

- `tool#64` **htr_classify**({"slot":"main","axis":"RL"}) [sim=238s, wall=401s]
  → subset=[0, 2, 1, 5, 3, 7, 4, 6]
_(turn 55: 809 in / 278 out / 83,217 cached, ~$-0.2181, 4.7s API)_

**Turn 55 narration**:

20-move finish is rough. Let me start applying and check for early shortcuts.

- `tool#65` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"htr_reduction"}) [sim=239s, wall=406s]
  → (empty result)
_(turn 56: 992 in / 104 out / 83,401 cached, ~$-0.2206, 4.0s API)_

- `tool#66` **apply_moves**({"slot":"main","moves":["U2","R'","U2","R'"]}) [sim=240s, wall=410s]
  → hist=18m
  slot=main [INV] hist(18m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B U2 R' U2 R'`
_(turn 57: 638 in / 119 out / 83,865 cached, ~$-0.2227, 3.5s API)_

- `tool#67` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"htr_reduction"}) [sim=241s, wall=414s]
  → (empty result)
_(turn 58: 533 in / 104 out / 84,554 cached, ~$-0.2251, 2.6s API)_

- `tool#68` **apply_moves**({"slot":"main","moves":["D2","R2","U2","F2"]}) [sim=241s, wall=416s]
  → hist=22m
  slot=main [INV] hist(22m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B U2 R' U2 R' D2 R2 U2 F2`
_(turn 59: 534 in / 119 out / 84,766 cached, ~$-0.2255, 2.2s API)_

- `tool#69` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"htr_reduction"}) [sim=242s, wall=419s]
  → (empty result)
_(turn 60: 500 in / 91 out / 85,071 cached, ~$-0.2268, 207.1s API)_

- `tool#70` **apply_moves**({"slot":"main","moves":["L"]}) [sim=242s, wall=626s]
  → hist=23m
  slot=main [INV] hist(23m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B U2 R' U2 R' D2 R2 U2 F2 L`
_(turn 61: 475 in / 65 out / 85,403 cached, ~$-0.2282, 1.9s API)_

- `tool#71` **quick_check**({"slot":"main"}) [sim=242s, wall=628s]
  → (empty result)
_(turn 62: 505 in / 183 out / 85,724 cached, ~$-0.2272, 3.9s API)_

**Turn 62 narration**:

At HTR. Let me check for a 3-cycle residual before running finish.

- `tool#72` **analyze_residual**({"slot":"main"}) [sim=244s, wall=631s]
  → (empty result)
_(turn 63: 706 in / 212 out / 86,007 cached, ~$-0.2269, 5.0s API)_

**Turn 63 narration**:

Just run the finish.

- `tool#73` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"finish"}) [sim=245s, wall=636s]
  → (empty result)
_(turn 64: 788 in / 104 out / 86,318 cached, ~$-0.2291, 2.4s API)_

- `tool#74` **apply_moves**({"slot":"main","moves":["U2","R2","U2","F2"]}) [sim=246s, wall=639s]
  → hist=27m
  slot=main [INV] hist(27m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B U2 R' U2 R' D2 R2 U2 F2 L U2 R2 U2 F2`
_(turn 65: 661 in / 115 out / 86,787 cached, ~$-0.2306, 2.9s API)_

- `tool#75` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"finish"}) [sim=247s, wall=642s]
  → (empty result)
_(turn 66: 556 in / 104 out / 87,302 cached, ~$-0.2325, 2.3s API)_

- `tool#76` **apply_moves**({"slot":"main","moves":["R2","B2","U2","B2"]}) [sim=247s, wall=644s]
  → hist=31m
  slot=main [INV] hist(31m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B U2 R' U2 R' D2 R2 U2 F2 L U2 R2 U2 F2 R2 B2 U2 B2`
_(turn 67: 561 in / 115 out / 87,506 cached, ~$-0.2329, 2.3s API)_

- `tool#77` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"finish"}) [sim=248s, wall=646s]
  → (empty result)
_(turn 68: 532 in / 100 out / 87,846 cached, ~$-0.2341, 2.7s API)_

- `tool#78` **apply_moves**({"slot":"main","moves":["U2","F2","R2"]}) [sim=248s, wall=649s]
  → hist=34m
  slot=main [INV] hist(34m): `R2 D' U2 L U2 L' F2 L B F U2 R2 D2 B U2 R' U2 R' D2 R2 U2 F2 L U2 R2 U2 F2 R2 B2 U2 B2 U2 F2 R2`
_(turn 69: 529 in / 65 out / 88,166 cached, ~$-0.2355, 2.2s API)_

- `tool#79` **quick_check**({"slot":"main"}) [sim=248s, wall=651s]
  → SOLVED
_(turn 70: 549 in / 207 out / 88,522 cached, ~$-0.2343, 4.1s API)_

**Turn 70 narration**:

Solved at 34 moves. Compose and verify.

- `tool#80` **compose_niss_solution**({"slot":"main"}) [sim=249s, wall=656s]
  → solves=True
_(turn 71: 751 in / 385 out / 88,802 cached, ~$-0.2317, 11.3s API)_

**Turn 71 narration**:

Gates pass for replace_and_shorten. Running on the large tail.

- `tool#81` **replace_and_shorten**({"slot":"main","start":4,"end":34,"axis":"RL"}) [sim=279s, wall=670s]
  → ERROR: could not solve micro-scramble for span [4:34]: no DR found
_(turn 72: 908 in / 280 out / 89,166 cached, ~$-0.2338, 4.2s API)_

**Turn 72 narration**:

R&S failed and cap hit. Submitting 34-move solution.

- `tool#82` **verify_solved**({"solution":["R2","F2","U2","B2","U2","B2","R2","F2","U2","R2","U2","L'","F2","U2","R2","D2","R","U2","R","U2","B'","...) [sim=279s, wall=674s]
  → solves=True, moves=34
_(turn 73: 649 in / 479 out / 89,659 cached, ~$-0.2329, 9.1s API)_

**Turn 73 narration**:

Verified 34-move solve. Shipping.

**Summary of the solve**:
- Started normal-side, hit a 2C0E stuck position (UD-DR-2-twist with no slice off, hard to escape in ≤5 EO-preserving moves). Reset.
- Switched to **inverse-side**, found 2-move RL-EO: `R2 D'` (vs 4-move normal).
- DR built incrementally: 4-move setup `U2 L U2 B` → 2C1E, then 5-move `B' L' F2 L B` → 0C1E (with 2 cancellations), then 5-move `F U2 R2 D2 B` → DR (RL-axis, 14 moves total).
- HTR-classify: "2-swap long-cycle" subset — heavy 20-move finish (9 reduction + 11 finish), no clean 3-cycle for insertion.
- `replace_and_shorten` micro-scramble timed out finding DR on the tail — accepted 34 as final.

FINAL_SOLUTION: ["R2", "F2", "U2", "B2", "U2", "B2", "R2", "F2", "U2", "R2", "U2", "L'", "F2", "U2", "R2", "D2", "R", "U2", "R", "U2", "B'", "D2", "R2", "U2", "F'", "B'", "L'", "F2", "L", "U2", "L'", "U2", "D", "R2"]


**verify_solved** ✓ — 34 moves: `R2 F2 U2 B2 U2 B2 R2 F2 U2 R2 U2 L' F2 U2 R2 D2 R U2 R U2 B' D2 R2 U2 F' B' L' F2 L U2 L' U2 D R2`
