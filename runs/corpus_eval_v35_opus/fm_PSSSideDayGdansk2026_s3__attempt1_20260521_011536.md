# Run — fm_PSSSideDayGdansk2026_s3__attempt1_20260521_011536.json

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-opus-4-7`  
**Result**: ✓ SOLVED (36 moves, 73 tool calls)  
**Sim budget**: 449s / 3600s  
**Wall time**: 529s  
**Tokens**: 101,906 in (3,789,708 cached), 25,893 out  
**Cost estimate**: $2.161  
**Solution**: `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2`  

**Sim-time spent by tool**:

- `dr_progress_options`: 20× = 288s
- `reset_slot`: 2× = 50s
- `replace_and_shorten`: 1× = 30s
- `inspect_state`: 3× = 15s
- `htr_classify`: 1× = 15s
- `eo_pattern_lookup`: 4× = 12s
- `niss_flip`: 5× = 10s
- `apply_moves`: 20× = 8s
- `brain_suggest`: 2× = 6s
- `apply_htr_phase`: 6× = 6s
- `try_alg`: 2× = 3s
- `restore_fork`: 1× = 3s
- `bookmark_fork`: 1× = 2s
- `compose_niss_solution`: 1× = 1s
- `undo_moves`: 1× = 0s

---

_(turn 1: 467 in / 99 out / 0 cached, ~$0.0029, 2.1s API)_

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=2s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 8, 'RL': 6}
_(turn 2: 815 in / 504 out / 18,679 cached, ~$-0.0404, 8.9s API)_

**Turn 2 narration**:

UD has 4 bad edges (lowest count). FB has 8, RL has 6. Let me look up EO patterns on UD.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=8s, wall=11s]
  → found=1, best=4m
_(turn 3: 1,500 in / 152 out / 18,679 cached, ~$-0.0437, 3.3s API)_

**Turn 3 narration**:

4-move EO on UD-normal. Let me NISS-check the inverse, then probe DR options.

- `tool#3` **niss_flip**({"slot":"main"}) [sim=10s, wall=14s]
  → (empty result)
_(turn 4: 967 in / 94 out / 19,140 cached, ~$-0.0474, 1.9s API)_

- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=13s, wall=16s]
  → found=1, best=4m
_(turn 5: 882 in / 171 out / 20,564 cached, ~$-0.0503, 2.9s API)_

**Turn 5 narration**:

Both sides have 4-move UD-EO. Let me commit UD-normal EO and probe DR.

- `tool#5` **niss_flip**({"slot":"main"}) [sim=15s, wall=19s]
  → (empty result)
_(turn 6: 892 in / 102 out / 20,897 cached, ~$-0.0522, 2.5s API)_

- `tool#6` **apply_moves**({"slot":"main","moves":["U","L","R'","B'"]}) [sim=15s, wall=22s]
  → hist=4m
  slot=main hist(4m): `U L R' B'`
_(turn 7: 856 in / 136 out / 21,435 cached, ~$-0.0533, 2.5s API)_

- `tool#7` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":6}) [sim=22s, wall=24s]
  → (empty result)
_(turn 8: 1,211 in / 465 out / 21,883 cached, ~$-0.0485, 8.4s API)_

**Turn 8 narration**:

Let me also probe DR on FB and RL axes from this same post-EO state, since EO-preserving moves on UD only excludes F/B quarters — but a different axis might reach DR faster.

- `tool#8` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":4,"k":5}) [sim=25s, wall=33s]
  → ERROR: EO not yet solved on axis FB; run eo_pattern_lookup and apply EO moves first.
_(turn 9: 1,520 in / 195 out / 22,421 cached, ~$-0.0531, 3.5s API)_

**Turn 9 narration**:

Right, UD-EO only enables UD-axis DR. Let me commit the first setup `U R D2 L` and re-query.

- `tool#9` **apply_moves**({"slot":"main","moves":["U","R","D2","L"]}) [sim=25s, wall=36s]
  → hist=8m
  slot=main hist(8m): `U L R' B' U R D2 L`
_(turn 10: 621 in / 136 out / 22,671 cached, ~$-0.0573, 3.2s API)_

- `tool#10` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":6}) [sim=32s, wall=40s]
  → (empty result)
_(turn 11: 1,330 in / 186 out / 24,200 cached, ~$-0.0586, 3.9s API)_

**Turn 11 narration**:

Down to 2C1E in 3 more moves. Let me commit `B2 U' R` and look one more time.

- `tool#11` **apply_moves**({"slot":"main","moves":["B2","U'","R"]}) [sim=32s, wall=44s]
  → hist=11m
  slot=main hist(11m): `U L R' B' U R D2 L B2 U' R`
_(turn 12: 1,289 in / 136 out / 24,523 cached, ~$-0.0603, 2.7s API)_

- `tool#12` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":6}) [sim=37s, wall=47s]
  → (empty result)
_(turn 13: 1,273 in / 235 out / 24,683 cached, ~$-0.0593, 6.4s API)_

**Turn 13 narration**:

Stuck at 2C1E at depth 4. Let me try depth 5 to see if DR is reachable.

- `tool#13` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=57s, wall=54s]
  → (empty result)
_(turn 14: 2,238 in / 581 out / 25,937 cached, ~$-0.0546, 9.6s API)_

**Turn 14 narration**:

Picks `R2 B2 R U2 R'` → DR-2C0E (only 2 misoriented corners left). Let me commit.

- `tool#14` **apply_moves**({"slot":"main","moves":["R2","B2","R","U2","R'"]}) [sim=57s, wall=64s]
  → hist=15m
  slot=main hist(15m): `U L R' B' U R D2 L B2 U' R' B2 R U2 R'`
_(turn 15: 2,044 in / 191 out / 26,108 cached, ~$-0.0615, 3.2s API)_

- `tool#15` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":6}) [sim=62s, wall=67s]
  → (empty result)
_(turn 16: 1,352 in / 200 out / 27,345 cached, ~$-0.0668, 3.2s API)_

- `tool#16` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=76s, wall=72s]
  → (empty result)
_(turn 17: 2,132 in / 2,234 out / 29,064 cached, ~$-0.0386, 35.5s API)_

**Turn 17 narration**:

Let me commit `R F2 R F2 R'` → 0C1E and continue.

- `tool#17` **apply_moves**({"slot":"main","moves":["R","F2","R","F2","R'"]}) [sim=76s, wall=107s]
  → hist=18m
  slot=main hist(18m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R'`
_(turn 18: 3,500 in / 228 out / 29,251 cached, ~$-0.0651, 3.7s API)_

**Turn 18 narration**:

Cancelled 2 moves — now at 18. Let me check DR options.

- `tool#18` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":6}) [sim=80s, wall=111s]
  → (empty result)
_(turn 19: 1,399 in / 620 out / 30,307 cached, ~$-0.0683, 11.1s API)_

- `tool#19` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":10}) [sim=91s, wall=123s]
  → (empty result)
_(turn 20: 2,796 in / 380 out / 33,809 cached, ~$-0.0772, 7.1s API)_

- `tool#20` **inspect_state**({"slot":"main"}) [sim=96s, wall=130s]
  → EO: ['UD'], DR: [], bad_edges {'UD': 0, 'FB': 2, 'RL': 4}
_(turn 21: 2,365 in / 527 out / 34,236 cached, ~$-0.0774, 8.4s API)_

- `tool#21` **brain_suggest**({"slot":"main","step":"dr","k":5}) [sim=99s, wall=139s]
  → (empty result)
_(turn 22: 1,592 in / 130 out / 35,100 cached, ~$-0.0880, 3.4s API)_

- `tool#22` **try_alg**({"slot":"main","alg":["L'"]}) [sim=100s, wall=142s]
  → (empty result)
_(turn 23: 1,874 in / 2,057 out / 36,894 cached, ~$-0.0631, 32.7s API)_

**Turn 23 narration**:

Let me bookmark and try inverse side — DR-0C1E with odd parity is awkward.

- `tool#23` **bookmark_fork**({"slot":"main","name":"UD-0C1E-normal","description":"Post-EO+partial-DR at 18 moves, stuck at DR-0C1E. Exploring inv...) [sim=102s, wall=175s]
  → (empty result)
_(turn 24: 3,730 in / 66 out / 38,085 cached, ~$-0.0906, 2.1s API)_

- `tool#24` **niss_flip**({"slot":"main"}) [sim=104s, wall=177s]
  → (empty result)
  slot=main [INV] hist(18m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R'`
_(turn 25: 1,077 in / 136 out / 38,866 cached, ~$-0.0997, 2.4s API)_

- `tool#25` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":6}) [sim=107s, wall=179s]
  → ERROR: EO not yet solved on axis UD; run eo_pattern_lookup and apply EO moves first.
_(turn 26: 935 in / 126 out / 42,544 cached, ~$-0.1102, 2.5s API)_

- `tool#26` **inspect_state**({"slot":"main"}) [sim=112s, wall=182s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 6, 'RL': 6}
_(turn 27: 1,126 in / 705 out / 42,726 cached, ~$-0.1014, 12.2s API)_

- `tool#27` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=115s, wall=194s]
  → found=1, best=4m
_(turn 28: 1,810 in / 496 out / 43,463 cached, ~$-0.1045, 9.0s API)_

**Turn 28 narration**:

NISS on inverse needs another EO. Let me revert and continue on normal — push through the awkward 0C1E.

- `tool#28` **niss_flip**({"slot":"main"}) [sim=117s, wall=203s]
  → (empty result)
  slot=main hist(18m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R'`
_(turn 29: 1,400 in / 468 out / 43,727 cached, ~$-0.1068, 10.2s API)_

**Turn 29 narration**:

Brain top is L' — let me commit and see if subsequent depth-4 finds DR.

- `tool#29` **apply_moves**({"slot":"main","moves":["L'"]}) [sim=118s, wall=213s]
  → hist=19m
  slot=main hist(19m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R' L'`
_(turn 30: 1,409 in / 136 out / 44,725 cached, ~$-0.1145, 2.6s API)_

- `tool#30` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=139s, wall=217s]
  → (empty result)
_(turn 31: 1,476 in / 565 out / 46,160 cached, ~$-0.1117, 10.9s API)_

- `tool#31` **undo_moves**({"slot":"main","n":1}) [sim=139s, wall=228s]
  → hist=18m
  slot=main hist(18m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R'`
_(turn 32: 1,793 in / 1,262 out / 47,299 cached, ~$-0.1034, 22.5s API)_

**Turn 32 narration**:

Let me commit L and search deeper — L stays at 0C1E count-wise but moves to a different position in that class.

- `tool#32` **apply_moves**({"slot":"main","moves":["L"]}) [sim=139s, wall=251s]
  → hist=19m
  slot=main hist(19m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R' L`
_(turn 33: 1,648 in / 136 out / 47,501 cached, ~$-0.1213, 3.5s API)_

- `tool#33` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":10}) [sim=161s, wall=256s]
  → (empty result)
_(turn 34: 1,636 in / 1,180 out / 48,681 cached, ~$-0.1088, 21.4s API)_

**Turn 34 narration**:

The 0C1E path will need ≥6 more moves. Let me restore and try a different axis instead. Reset and try FB.

- `tool#34` **restore_fork**({"name":"UD-0C1E-normal"}) [sim=164s, wall=277s]
  → (empty result)
_(turn 35: 2,569 in / 655 out / 50,693 cached, ~$-0.1193, 13.8s API)_

- `tool#35` **apply_moves**({"slot":"main","moves":["R2","L","D2"]}) [sim=164s, wall=291s]
  → hist=20m
  slot=main hist(20m): `U L R' B' U R D2 L B2 U' R' B2 R U2 F2 R F2 R L D2`
_(turn 36: 1,118 in / 305 out / 50,894 cached, ~$-0.1295, 4.9s API)_

- `tool#36` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=189s, wall=299s]
  → (empty result)
_(turn 37: 1,582 in / 476 out / 53,417 cached, ~$-0.1323, 9.0s API)_

**Turn 37 narration**:

This branch is deeply stuck on parity. Let me restore and instead undo to right after EO, then try a different DR setup.

- `tool#37` **reset_slot**({"slot":"main"}) [sim=214s, wall=308s]
  → (empty result)
_(turn 38: 1,659 in / 458 out / 53,599 cached, ~$-0.1329, 8.0s API)_

**Turn 38 narration**:

Let me start on inverse this time — the EO was also 4 moves and DR substate might be different.

- `tool#38` **niss_flip**({"slot":"main"}) [sim=216s, wall=315s]
  → (empty result)
_(turn 39: 1,175 in / 103 out / 54,459 cached, ~$-0.1420, 3.0s API)_

- `tool#39` **apply_moves**({"slot":"main","moves":["B'","R'","U","B'"]}) [sim=217s, wall=318s]
  → hist=4m
  slot=main [INV] hist(4m): `B' R' U B'`
_(turn 40: 858 in / 136 out / 56,313 cached, ~$-0.1474, 2.5s API)_

- `tool#40` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=250s, wall=324s]
  → (empty result)
_(turn 41: 1,403 in / 505 out / 56,882 cached, ~$-0.1418, 8.3s API)_

**Turn 41 narration**:

Inverse looks more tractable — 2C1E in 4. Committing `R' U D2 R`.

- `tool#41` **apply_moves**({"slot":"main","moves":["R'","U","D2","R"]}) [sim=250s, wall=332s]
  → hist=8m
  slot=main [INV] hist(8m): `B' R' U B' R' U D2 R`
_(turn 42: 1,786 in / 136 out / 57,420 cached, ~$-0.1476, 2.9s API)_

- `tool#42` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":8}) [sim=276s, wall=337s]
  → (empty result)
_(turn 43: 1,510 in / 585 out / 57,672 cached, ~$-0.1424, 9.8s API)_

- `tool#43` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":4,"k":8}) [sim=282s, wall=348s]
  → (empty result)
_(turn 44: 2,705 in / 708 out / 59,432 cached, ~$-0.1417, 10.8s API)_

**Turn 44 narration**:

Committing `U2 D' L U L'` (5 moves) → DR-2C0E.

- `tool#44` **apply_moves**({"slot":"main","moves":["U2","D'","L","U","L'"]}) [sim=283s, wall=358s]
  → hist=13m
  slot=main [INV] hist(13m): `B' R' U B' R' U D2 R U2 D' L U L'`
_(turn 45: 1,901 in / 136 out / 59,594 cached, ~$-0.1532, 2.9s API)_

- `tool#45` **dr_progress_options**({"slot":"main","axis":"UD","max_depth":5,"k":10}) [sim=296s, wall=362s]
  → (empty result)
_(turn 46: 1,639 in / 1,258 out / 60,838 cached, ~$-0.1405, 21.1s API)_

**Turn 46 narration**:

The 2C0E/0C1E parity is fundamental to this scramble's UD axis. Let me reset and try FB-axis EO from the start.

- `tool#46` **reset_slot**({"slot":"main"}) [sim=321s, wall=383s]
  → (empty result)
_(turn 47: 2,584 in / 94 out / 63,144 cached, ~$-0.1613, 1.9s API)_

- `tool#47` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=324s, wall=385s]
  → found=1, best=4m
_(turn 48: 453 in / 166 out / 63,324 cached, ~$-0.1671, 3.9s API)_

- `tool#48` **apply_moves**({"slot":"main","moves":["R'","F","D","L'"]}) [sim=325s, wall=389s]
  → hist=4m
  slot=main hist(4m): `R' F D L'`
_(turn 49: 495 in / 136 out / 65,934 cached, ~$-0.1745, 3.0s API)_

- `tool#49` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=353s, wall=395s]
  → (empty result)
_(turn 50: 1,591 in / 817 out / 66,044 cached, ~$-0.1613, 13.6s API)_

**Turn 50 narration**:

5 moves to 3C0E or 0C3E. Let me try the 3C0E path — committing `U' F D B U`.

- `tool#50` **apply_moves**({"slot":"main","moves":["U'","F","D","B","U"]}) [sim=353s, wall=408s]
  → hist=9m
  slot=main hist(9m): `R' F D L' U' F D B U`
_(turn 51: 2,288 in / 136 out / 66,319 cached, ~$-0.1702, 2.8s API)_

- `tool#51` **dr_progress_options**({"slot":"main","axis":"FB","max_depth":5,"k":10}) [sim=370s, wall=412s]
  → (empty result)
_(turn 52: 1,708 in / 575 out / 66,633 cached, ~$-0.1662, 11.9s API)_

- `tool#52` **brain_suggest**({"slot":"main","step":"dr","k":8}) [sim=373s, wall=424s]
  → (empty result)
_(turn 53: 2,201 in / 136 out / 68,894 cached, ~$-0.1774, 2.9s API)_

- `tool#53` **try_alg**({"slot":"main","alg":["D2"]}) [sim=374s, wall=427s]
  → (empty result)
_(turn 54: 1,742 in / 684 out / 69,057 cached, ~$-0.1710, 10.8s API)_

**Turn 54 narration**:

Both FB AND RL are EO-solved! Let me explore RL DR.

- `tool#54` **dr_progress_options**({"slot":"main","axis":"RL","max_depth":5,"k":10}) [sim=394s, wall=440s]
  → (empty result)
_(turn 55: 3,271 in / 239 out / 70,496 cached, ~$-0.1769, 5.1s API)_

**Turn 55 narration**:

5-move DR-solved on RL axis! Total 14 moves to DR.

- `tool#55` **apply_moves**({"slot":"main","moves":["B'","L'","U2","L","B"]}) [sim=394s, wall=445s]
  → hist=14m
  slot=main hist(14m): `R' F D L' U' F D B U B' L' U2 L B`
_(turn 56: 1,862 in / 65 out / 71,394 cached, ~$-0.1862, 2.2s API)_

- `tool#56` **quick_check**({"slot":"main"}) [sim=394s, wall=447s]
  → (empty result)
_(turn 57: 574 in / 140 out / 73,498 cached, ~$-0.1946, 3.2s API)_

**Turn 57 narration**:

DR on RL achieved! Now HTR classify.

- `tool#57` **htr_classify**({"slot":"main","axis":"RL"}) [sim=409s, wall=475s]
  → subset=[1, 0, 4, 3, 2, 7, 6, 5]
_(turn 58: 785 in / 257 out / 75,041 cached, ~$-0.1964, 4.5s API)_

**Turn 58 narration**:

22 move HTR finish — long. Let me apply HTR reduction and see.

- `tool#58` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"htr_reduction"}) [sim=410s, wall=480s]
  → (empty result)
_(turn 59: 984 in / 103 out / 75,222 cached, ~$-0.1986, 2.3s API)_

- `tool#59` **apply_moves**({"slot":"main","moves":["D2","R","D2","R'"]}) [sim=411s, wall=482s]
  → hist=18m
  slot=main hist(18m): `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R'`
_(turn 60: 632 in / 119 out / 75,648 cached, ~$-0.2006, 2.3s API)_

- `tool#60` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"htr_reduction"}) [sim=412s, wall=485s]
  → (empty result)
_(turn 61: 528 in / 103 out / 76,330 cached, ~$-0.2030, 3.5s API)_

- `tool#61` **apply_moves**({"slot":"main","moves":["F2","R","U2","R'"]}) [sim=412s, wall=488s]
  → hist=22m
  slot=main hist(22m): `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R'`
_(turn 62: 527 in / 119 out / 76,541 cached, ~$-0.2033, 2.2s API)_

- `tool#62` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"htr_reduction"}) [sim=413s, wall=490s]
  → (empty result)
_(turn 63: 499 in / 95 out / 76,841 cached, ~$-0.2045, 2.2s API)_

- `tool#63` **apply_moves**({"slot":"main","moves":["D2","R"]}) [sim=413s, wall=493s]
  → hist=24m
  slot=main hist(24m): `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R`
_(turn 64: 482 in / 65 out / 77,172 cached, ~$-0.2059, 3.5s API)_

- `tool#64` **quick_check**({"slot":"main"}) [sim=413s, wall=496s]
  → (empty result)
_(turn 65: 504 in / 170 out / 77,487 cached, ~$-0.2052, 4.0s API)_

**Turn 65 narration**:

HTR reached at 24 moves. Now finish.

- `tool#65` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"finish"}) [sim=414s, wall=500s]
  → (empty result)
_(turn 66: 595 in / 104 out / 77,774 cached, ~$-0.2066, 3.3s API)_

- `tool#66` **apply_moves**({"slot":"main","moves":["B2","L2","B2","U2"]}) [sim=415s, wall=503s]
  → hist=28m
  slot=main hist(28m): `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2`
_(turn 67: 660 in / 115 out / 78,088 cached, ~$-0.2071, 2.9s API)_

- `tool#67` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"finish"}) [sim=416s, wall=506s]
  → (empty result)
_(turn 68: 555 in / 104 out / 78,544 cached, ~$-0.2088, 2.8s API)_

- `tool#68` **apply_moves**({"slot":"main","moves":["F2","U2","F2","L2"]}) [sim=416s, wall=509s]
  → hist=32m
  slot=main hist(32m): `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2 F2 U2 F2 L2`
_(turn 69: 560 in / 115 out / 78,748 cached, ~$-0.2092, 2.1s API)_

- `tool#69` **apply_htr_phase**({"slot":"main","axis":"RL","phase":"finish"}) [sim=417s, wall=511s]
  → (empty result)
_(turn 70: 535 in / 104 out / 79,087 cached, ~$-0.2104, 2.1s API)_

- `tool#70` **apply_moves**({"slot":"main","moves":["R2","U2","R2","U2"]}) [sim=418s, wall=513s]
  → hist=36m
  slot=main hist(36m): `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2`
_(turn 71: 540 in / 65 out / 79,407 cached, ~$-0.2118, 2.2s API)_

- `tool#71` **quick_check**({"slot":"main"}) [sim=418s, wall=515s]
  → SOLVED
_(turn 72: 552 in / 266 out / 79,762 cached, ~$-0.2097, 4.8s API)_

**Turn 72 narration**:

Solved at 36 moves. Gates pass for replace_and_shorten. Let me run it on a large tail.

- `tool#72` **replace_and_shorten**({"slot":"main","start":4,"end":36,"axis":"RL"}) [sim=448s, wall=523s]
  → ERROR: could not solve micro-scramble for span [4:36]: no DR found
_(turn 73: 615 in / 136 out / 80,046 cached, ~$-0.2122, 3.0s API)_

**Turn 73 narration**:

R&S used and failed. Let me submit the 36-move solve.

- `tool#73` **compose_niss_solution**({"slot":"main"}) [sim=449s, wall=526s]
  → solves=True
_(turn 74: 724 in / 169 out / 80,417 cached, ~$-0.2124, 3.1s API)_

**Turn 74 narration**:

Solution verified at 36 moves. Submitting.

FINAL_SOLUTION: ["R'", "F", "D", "L'", "U'", "F", "D", "B", "U", "B'", "L'", "U2", "L", "B", "D2", "R", "D2", "R'", "F2", "R", "U2", "R'", "D2", "R", "B2", "L2", "B2", "U2", "F2", "U2", "F2", "L2", "R2", "U2", "R2", "U2"]


**verify_solved** ✓ — 36 moves: `R' F D L' U' F D B U B' L' U2 L B D2 R D2 R' F2 R U2 R' D2 R B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2`
