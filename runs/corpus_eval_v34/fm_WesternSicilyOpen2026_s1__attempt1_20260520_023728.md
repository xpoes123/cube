# Run — fm_WesternSicilyOpen2026_s1__attempt1_20260520_023728.json

**Scramble**: `R' U' F U2 F2 D2 B2 D B' U L' B' F2 R2 U' L2 F2 B2 D' F2 L2 F R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (31 moves, 54 tool calls)  
**Sim budget**: 724s / 3600s  
**Wall time**: 189s  
**Tokens**: 35,409 in (1,223,616 cached), 6,547 out  
**Cost estimate**: $0.674  
**Solution**: `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2 U D2 F2 U2 L2 D2 R2 F2 R2 U2 R2`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 2× = 623s
- `dr_recognize`: 9× = 36s
- `reset_slot`: 1× = 25s
- `htr_classify`: 1× = 15s
- `eo_pattern_lookup`: 2× = 6s
- `apply_htr_phase`: 6× = 6s
- `inspect_state`: 1× = 5s
- `apply_moves`: 18× = 4s
- `niss_flip`: 1× = 2s
- `try_alg`: 1× = 2s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 374 in / 165 out / 0 cached, ~$0.0036, 4.5s API)_

### Turn 1 — thinking

> The user wants me to solve a Rubik's Cube FMC scramble. I need to start by inspecting the state of the 'main' slot to see the current cube configuration, particularly the bad edges per axis which will guide my EO (Edge Orientation) decision.
> 
> Let me start with inspect_state on the main slot as requested.

**Turn 1 narration**:

I'll solve this FMC scramble systematically, starting with inspection and following the elite-solver pipeline. Let me begin.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=5s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 6, 'RL': 4}
_(turn 2: 817 in / 366 out / 13,378 cached, ~$-0.0282, 10.5s API)_

**Turn 2 narration**:

**Initial inspection:** I see bad edges per axis: UD=4, FB=6, RL=4. Both UD and RL have 4 bad edges, which should give short EO solutions (typically 1-3 moves for 4 bad edges when they cluster well). FB has 6 bad edges, which is less attractive.

Looking at the bad edge slot patterns:
- **UD axis (4 bad)**: UB, DF, DL, FL — slots DF and FL are both on the F face, UB is on B. This suggests F would flip 2 edges (DF, FL), and B would flip 1 (UB). Not a perfect one-move solution.
- **RL axis (4 bad)**: UB, DL, DB, BR — slots UB and DL could be addressed through U/D moves.

The DR-closeness signals show UD has DR-4C3E pre-EO and "2 pairs on inverse" which is a good NISS indicator. Let me scout EO on both normal and inverse sides for UD and RL axes.

**EO scouting plan:** I'll check UD-axis EO on normal, then flip to inverse and check UD there as well. Then decide.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=8s, wall=15s]
  → found=1, best=4m
_(turn 3: 1,328 in / 113 out / 13,378 cached, ~$-0.0304, 3.7s API)_

**Turn 3 narration**:

**UD-axis normal EO: 4 moves** (D R U2 F'). Now let me check the inverse side for UD-axis EO, since the inspect showed "2 pairs on inverse" which is a strong NISS signal.

- `tool#3` **niss_flip**({"slot":"main"}) [sim=10s, wall=19s]
  → (empty result)
_(turn 4: 1,090 in / 129 out / 13,909 cached, ~$-0.0323, 3.6s API)_

**Turn 4 narration**:

Now I'm on the inverse side. Let me check UD-axis EO here. (Remember: bad_edges_per_axis is INVARIANT under NISS, so it's still 4 bad edges, but the SOLUTION differs.)

- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=13s, wall=22s]
  → found=1, best=2m
_(turn 5: 846 in / 187 out / 14,919 cached, ~$-0.0349, 4.5s API)_

**Turn 5 narration**:

**Excellent! UD-axis inverse EO: 2 moves** (L' F'). That's 2 moves shorter than the normal side. Plus, the original inspect showed "2 pairs on inverse" which is a strong signal for a clean DR after EO. This is clearly the better direction.

**Decision: Staying on inverse, committing to UD-axis EO with L' F'.**

Let me apply these 2 EO moves and then probe DR options.

- `tool#5` **apply_moves**({"slot":"main","moves":["L'","F'"]}) [sim=13s, wall=27s]
  → hist=2m
  slot=main [INV] hist(2m): `L' F'`
_(turn 6: 571 in / 163 out / 15,178 cached, ~$-0.0368, 4.8s API)_

**Turn 6 narration**:

**EO complete (2 moves on inverse).** Now I need to find DR. The original DR-closeness showed UD-axis pre-EO was DR-4C3E with 2 pairs on inverse — that's a strong signal. Let me call dr_trigger_options to find the best DR path.

- `tool#6` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=314s, wall=34s]
  → (empty result)
_(turn 7: 964 in / 145 out / 15,770 cached, ~$-0.0375, 4.1s API)_

**Turn 7 narration**:

**No DR triggers found within 5 moves!** This is unusual. The tool explored 98k states and found nothing. This suggests the DR state is more than 5 moves away through the standard trigger catalog. Let me try `dr_recognize` instead, which uses the brain-based approach for states outside the 4-move memory.

- `tool#7` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=318s, wall=38s]
  → found=0
_(turn 8: 1,051 in / 126 out / 16,097 cached, ~$-0.0384, 3.8s API)_

**Turn 8 narration**:

**Brain suggests D (25.3%), U2 (24.2%), F2 (11.2%), R2 (7.8%).** Let me try D first and see if it gets me closer to a recognizable DR pattern.

- `tool#8` **apply_moves**({"slot":"main","moves":["D"]}) [sim=318s, wall=42s]
  → hist=3m
  slot=main [INV] hist(3m): `L' F' D`
_(turn 9: 631 in / 71 out / 16,375 cached, ~$-0.0413, 1.5s API)_

- `tool#9` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=322s, wall=44s]
  → found=0
_(turn 10: 556 in / 103 out / 17,020 cached, ~$-0.0427, 2.2s API)_

**Turn 10 narration**:

**Brain now strongly suggests U2 (44.6%) or F2 (41.0%).** Let me try U2.

- `tool#10` **apply_moves**({"slot":"main","moves":["U2"]}) [sim=322s, wall=46s]
  → hist=4m
  slot=main [INV] hist(4m): `L' F' D U2`
_(turn 11: 536 in / 71 out / 17,391 cached, ~$-0.0443, 1.9s API)_

- `tool#11` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=326s, wall=48s]
  → found=0
_(turn 12: 536 in / 101 out / 17,512 cached, ~$-0.0442, 2.2s API)_

**Turn 12 narration**:

**Brain is now 99.7% confident on F2.** That's a very strong signal. Let me apply it.

- `tool#12` **apply_moves**({"slot":"main","moves":["F2"]}) [sim=326s, wall=50s]
  → hist=5m
  slot=main [INV] hist(5m): `L' F' D U2 F2`
_(turn 13: 537 in / 71 out / 17,928 cached, ~$-0.0457, 1.5s API)_

- `tool#13` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=330s, wall=52s]
  → found=0
_(turn 14: 536 in / 88 out / 18,053 cached, ~$-0.0458, 2.2s API)_

**Turn 14 narration**:

**Brain says D2 (80%).** Let me continue.

- `tool#14` **apply_moves**({"slot":"main","moves":["D2"]}) [sim=330s, wall=54s]
  → hist=6m
  slot=main [INV] hist(6m): `L' F' D U2 F2 D2`
_(turn 15: 526 in / 71 out / 18,468 cached, ~$-0.0472, 1.4s API)_

- `tool#15` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=334s, wall=55s]
  → found=0
_(turn 16: 524 in / 90 out / 18,597 cached, ~$-0.0473, 2.5s API)_

**Turn 16 narration**:

**Brain again 99.3% on F2.** Continuing.

- `tool#16` **apply_moves**({"slot":"main","moves":["F2"]}) [sim=334s, wall=58s]
  → hist=7m
  slot=main [INV] hist(7m): `L' F' D U2 F2 D2 F2`
_(turn 17: 529 in / 71 out / 18,999 cached, ~$-0.0486, 2.5s API)_

- `tool#17` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=338s, wall=60s]
  → found=0
_(turn 18: 528 in / 109 out / 19,132 cached, ~$-0.0484, 2.8s API)_

**Turn 18 narration**:

**Brain 99.3% on R.** This looks like it's converging to a DR trigger. R is the classic DR-4C4E trigger move.

- `tool#18` **apply_moves**({"slot":"main","moves":["R"]}) [sim=338s, wall=63s]
  → hist=8m
  slot=main [INV] hist(8m): `L' F' D U2 F2 D2 F2 R`
_(turn 19: 549 in / 68 out / 19,535 cached, ~$-0.0501, 2.0s API)_

**Turn 19 narration**:

Let me check if I've reached DR now with quick_check.

- `tool#19` **quick_check**({"slot":"main"}) [sim=338s, wall=65s]
  → (empty result)
_(turn 20: 481 in / 86 out / 19,672 cached, ~$-0.0504, 1.9s API)_

**Turn 20 narration**:

**Not DR yet.** Let me continue with dr_recognize.

- `tool#20` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=342s, wall=67s]
  → found=0
_(turn 21: 564 in / 95 out / 20,094 cached, ~$-0.0511, 2.3s API)_

**Turn 21 narration**:

**Brain suggests R (57.7%) or U (26.7%).** Let me try R.

- `tool#21` **apply_moves**({"slot":"main","moves":["R"]}) [sim=343s, wall=69s]
  → hist=8m
  slot=main [INV] hist(8m): `L' F' D U2 F2 D2 F2 R2`
_(turn 22: 547 in / 72 out / 20,299 cached, ~$-0.0521, 2.4s API)_

**Turn 22 narration**:

Good, auto-cancelled R + R → R2. Let me check DR again.

- `tool#22` **quick_check**({"slot":"main"}) [sim=343s, wall=72s]
  → (empty result)
_(turn 23: 469 in / 173 out / 20,566 cached, ~$-0.0515, 5.2s API)_

**Turn 23 narration**:

Still not DR. This is taking longer than expected. Let me rethink. I'm at 8 moves (EO 2 + RZP 6) and still not at DR. The DR-length hard rule says DR ≥10 rarely appears in good solves. Let me check if switching back to normal or trying a different axis might be better.

Actually, let me persist a bit more with the brain. Let me call dr_recognize again.

- `tool#23` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=347s, wall=77s]
  → found=0
_(turn 24: 653 in / 91 out / 20,905 cached, ~$-0.0531, 3.4s API)_

**Turn 24 narration**:

**Brain 84.3% on L2.** Let me try it.

- `tool#24` **apply_moves**({"slot":"main","moves":["L2"]}) [sim=347s, wall=80s]
  → hist=9m
  slot=main [INV] hist(9m): `L' F' D U2 F2 D2 F2 R2 L2`
_(turn 25: 632 in / 53 out / 21,115 cached, ~$-0.0543, 1.9s API)_

- `tool#25` **quick_check**({"slot":"main"}) [sim=347s, wall=82s]
  → (empty result)
_(turn 26: 447 in / 140 out / 21,469 cached, ~$-0.0545, 3.6s API)_

**Turn 26 narration**:

**I'm at 9 moves and still not at DR.** This is concerning. Let me try one more brain suggestion, but if this doesn't reach DR in the next 1-2 moves, I should reset and try a different approach. The DR-length rule says ≥10 is problematic.

- `tool#26` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=351s, wall=86s]
  → found=0
_(turn 27: 598 in / 92 out / 21,805 cached, ~$-0.0557, 2.7s API)_

**Turn 27 narration**:

**Brain suggests D' (61.6%).** Let me try it and check.

- `tool#27` **apply_moves**({"slot":"main","moves":["D'"]}) [sim=351s, wall=88s]
  → hist=10m
  slot=main [INV] hist(10m): `L' F' D U2 F2 D2 F2 R2 L2 D'`
_(turn 28: 601 in / 53 out / 21,950 cached, ~$-0.0567, 1.9s API)_

- `tool#28` **quick_check**({"slot":"main"}) [sim=351s, wall=90s]
  → (empty result)
_(turn 29: 449 in / 127 out / 22,321 cached, ~$-0.0570, 3.4s API)_

**Turn 29 narration**:

**10 moves, no DR.** This violates the hard rule. I need to reset and try a different approach. Let me reset and try the normal-side UD-axis EO (4 moves), which might have a better DR path.

- `tool#29` **reset_slot**({"slot":"main","rescramble":true}) [sim=376s, wall=94s]
  → (empty result)
_(turn 30: 426 in / 116 out / 22,658 cached, ~$-0.0582, 2.5s API)_

**Turn 30 narration**:

**Reset complete. Now trying normal-side UD-axis with 4-move EO.** Let me apply the normal-side EO.

- `tool#30` **apply_moves**({"slot":"main","moves":["D","R","U2","F'"]}) [sim=376s, wall=96s]
  → hist=4m
  slot=main hist(4m): `D R U2 F'`
_(turn 31: 428 in / 104 out / 22,807 cached, ~$-0.0587, 3.9s API)_

**Turn 31 narration**:

Now let me search for DR on the normal side.

- `tool#31` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=698s, wall=102s]
  → (empty result)
_(turn 32: 1,016 in / 239 out / 23,165 cached, ~$-0.0559, 8.9s API)_

**Turn 32 narration**:

**Found DR triggers on normal-side UD!**
- **DR-2C4E**: 5mv setup + 3mv trigger = 8mv to DR (total 12mv from scramble)
- **DR-4C4E**: 5mv setup + 4mv trigger = 9mv to DR (total 13mv from scramble)

The DR-2C4E in 8 moves is within the elite range. According to my substate priors table, DR-2C4E typically has 10-12mv post-DR finish. Let me try_alg it to inspect the residual.

- `tool#32` **try_alg**({"slot":"main","alg":["D2","F2","D","R","U'","R","F2","R"]}) [sim=700s, wall=111s]
  → (empty result)
_(turn 33: 2,214 in / 178 out / 23,370 cached, ~$-0.0538, 6.5s API)_

**Turn 33 narration**:

**DR reached! After-state shows DR-0C0E on UD axis (DR solved).** The HTR-closeness shows 5 qt_corners. Total is 4 EO + 8 DR = 12 moves to DR. Now I need to work through HTR and finish.

Let me apply these moves and proceed to HTR.

- `tool#33` **apply_moves**({"slot":"main","moves":["D2","F2","D","R","U'","R","F2","R"]}) [sim=701s, wall=118s]
  → hist=12m
  slot=main hist(12m): `D R U2 F' D2 F2 D R U' R F2 R`
_(turn 34: 1,735 in / 115 out / 23,595 cached, ~$-0.0568, 3.4s API)_

**Turn 34 narration**:

**DR complete at 12 moves.** Now I need to classify the HTR subset and finish. With 5 qt_corners, I'll need to reduce these to get into HTR.

- `tool#34` **htr_classify**({"slot":"main","axis":"UD"}) [sim=716s, wall=122s]
  → subset=[1, 0, 2, 5, 6, 3, 7, 4]
_(turn 35: 744 in / 191 out / 24,535 cached, ~$-0.0611, 5.7s API)_

**Turn 35 narration**:

**HTR subset: 2-swap long-cycle with cycle structure [3,2,2,1].** The classification says:
- HTR reduction: 9 moves
- Finish: 10 moves
- Total: 19 moves

Full solution estimate: 12 (DR) + 19 (HTR+finish) = **31 moves**. That's acceptable for a working solution. Let me proceed.

- `tool#35` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=717s, wall=128s]
  → (empty result)
_(turn 36: 780 in / 112 out / 25,910 cached, ~$-0.0659, 2.9s API)_

**Turn 36 narration**:

**Partial HTR reduction (4 of 9 moves).** Let me apply these and check state before continuing.

- `tool#36` **apply_moves**({"slot":"main","moves":["U'","R2","U'","L2"]}) [sim=717s, wall=131s]
  → hist=16m
  slot=main hist(16m): `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2`
_(turn 37: 610 in / 53 out / 26,174 cached, ~$-0.0680, 1.8s API)_

- `tool#37` **quick_check**({"slot":"main"}) [sim=717s, wall=132s]
  → (empty result)
_(turn 38: 479 in / 117 out / 26,696 cached, ~$-0.0689, 2.9s API)_

**Turn 38 narration**:

**Not HTR yet, not solved.** Let me continue with the next chunk of HTR reduction.

- `tool#38` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=718s, wall=135s]
  → (empty result)
_(turn 39: 490 in / 84 out / 26,981 cached, ~$-0.0701, 1.8s API)_

- `tool#39` **apply_moves**({"slot":"main","moves":["U","R2","F2","B2"]}) [sim=718s, wall=137s]
  → hist=20m
  slot=main hist(20m): `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2`
_(turn 40: 519 in / 53 out / 27,149 cached, ~$-0.0710, 1.4s API)_

- `tool#40` **quick_check**({"slot":"main"}) [sim=718s, wall=139s]
  → (empty result)
_(turn 41: 463 in / 113 out / 27,497 cached, ~$-0.0712, 3.3s API)_

**Turn 41 narration**:

**Still not HTR.** Let me get the final chunk of HTR reduction.

- `tool#41` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"htr_reduction"}) [sim=719s, wall=142s]
  → (empty result)
_(turn 42: 439 in / 72 out / 27,672 cached, ~$-0.0723, 1.7s API)_

- `tool#42` **apply_moves**({"slot":"main","moves":["U"]}) [sim=719s, wall=144s]
  → hist=21m
  slot=main hist(21m): `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2 U`
_(turn 43: 459 in / 53 out / 27,936 cached, ~$-0.0733, 2.4s API)_

- `tool#43` **quick_check**({"slot":"main"}) [sim=719s, wall=146s]
  → (empty result)
_(turn 44: 451 in / 134 out / 28,280 cached, ~$-0.0730, 3.4s API)_

**Turn 44 narration**:

**HTR reached!** All axes now show EO, DR, and HTR on UD. At 21 moves. Now I need to apply the finish phase (half-turns only).

- `tool#44` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=720s, wall=149s]
  → (empty result)
_(turn 45: 496 in / 85 out / 28,411 cached, ~$-0.0739, 2.1s API)_

- `tool#45` **apply_moves**({"slot":"main","moves":["D2","F2","U2","L2"]}) [sim=721s, wall=152s]
  → hist=25m
  slot=main hist(25m): `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2 U D2 F2 U2 L2`
_(turn 46: 545 in / 53 out / 28,666 cached, ~$-0.0750, 2.1s API)_

- `tool#46` **quick_check**({"slot":"main"}) [sim=721s, wall=154s]
  → (empty result)
_(turn 47: 477 in / 108 out / 29,031 cached, ~$-0.0753, 4.8s API)_

**Turn 47 narration**:

**Not solved yet.** Let me continue with the next chunk of finish.

- `tool#47` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=722s, wall=158s]
  → (empty result)
_(turn 48: 467 in / 85 out / 29,201 cached, ~$-0.0762, 1.8s API)_

- `tool#48` **apply_moves**({"slot":"main","moves":["D2","R2","F2","R2"]}) [sim=722s, wall=160s]
  → hist=29m
  slot=main hist(29m): `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2 U D2 F2 U2 L2 D2 R2 F2 R2`
_(turn 49: 532 in / 53 out / 29,485 cached, ~$-0.0772, 1.9s API)_

- `tool#49` **quick_check**({"slot":"main"}) [sim=722s, wall=162s]
  → (empty result)
_(turn 50: 490 in / 105 out / 29,824 cached, ~$-0.0775, 2.1s API)_

**Turn 50 narration**:

**Still not solved.** Let me get the final chunk.

- `tool#50` **apply_htr_phase**({"slot":"main","axis":"UD","phase":"finish"}) [sim=723s, wall=164s]
  → (empty result)
_(turn 51: 421 in / 77 out / 29,994 cached, ~$-0.0786, 1.8s API)_

- `tool#51` **apply_moves**({"slot":"main","moves":["U2","R2"]}) [sim=723s, wall=166s]
  → hist=31m
  slot=main hist(31m): `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2 U D2 F2 U2 L2 D2 R2 F2 R2 U2 R2`
_(turn 52: 486 in / 53 out / 30,294 cached, ~$-0.0795, 1.5s API)_

- `tool#52` **quick_check**({"slot":"main"}) [sim=723s, wall=167s]
  → SOLVED
_(turn 53: 487 in / 98 out / 30,630 cached, ~$-0.0798, 3.0s API)_

**Turn 53 narration**:

**SOLVED at 31 moves!** Now I need to verify and check if there are any cancellations. Let me use compose_niss_solution to assemble the final solution.

- `tool#53` **compose_niss_solution**({"slot":"main"}) [sim=724s, wall=170s]
  → solves=True
_(turn 54: 544 in / 347 out / 30,760 cached, ~$-0.0762, 7.5s API)_

**Turn 54 narration**:

**31-move solution verified!** The solution solves the cube. Now, according to the refinement rules, since my solution is ≥27 moves AND I have ≥30 tool calls remaining (I have 27, close enough), I should try replace_and_shorten ONCE to see if I can improve it.

However, I only have 27 tool calls remaining, not ≥30, so the gates may not pass. Let me try anyway — the tool will refuse if gates fail.

Actually, looking more carefully: I have 27 tool calls remaining, which is <30, so I should NOT call replace_and_shorten. The mandatory gate is "tool calls remaining ≥ 30", and I'm at 27.

Let me verify the solution once more and submit.

- `tool#54` **verify_solved**({"solution":["D","R","U2","F'","D2","F2","D","R","U'","R","F2","R","U'","R2","U'","L2","U","R2","F2","B2","U","D2","F...) [sim=724s, wall=178s]
  → solves=True, moves=31
_(turn 55: 741 in / 459 out / 31,060 cached, ~$-0.0748, 11.2s API)_

**Turn 55 narration**:

Perfect! The solution is verified at 31 moves. This is a working solve within the competition budget.

## Solution Summary

**Scramble:** R' U' F U2 F2 D2 B2 D B' U L' B' F2 R2 U' L2 F2 B2 D' F2 L2 F R' U' F

**Solution breakdown:**
- **EO (4 moves):** D R U2 F' — UD-axis edge orientation on normal side
- **DR (8 moves):** D2 F2 D R U' R F2 R — DR-2C4E trigger (5mv setup + 3mv trigger)
- **HTR reduction (9 moves):** U' R2 U' L2 U R2 F2 B2 U — reducing to HTR corners
- **Finish (10 moves):** D2 F2 U2 L2 D2 R2 F2 R2 U2 R2 — half-turn finish to solved

**Total: 31 moves**

The solve followed the standard elite FMC pipeline: EO → DR → HTR → finish. The DR-2C4E trigger gave a reasonable post-DR residual, and the 2-swap long-cycle HTR subset finished in 19 moves (9+10), which is within the expected range for that subset type.

FINAL_SOLUTION: ["D", "R", "U2", "F'", "D2", "F2", "D", "R", "U'", "R", "F2", "R", "U'", "R2", "U'", "L2", "U", "R2", "F2", "B2", "U", "D2", "F2", "U2", "L2", "D2", "R2", "F2", "R2", "U2", "R2"]


**verify_solved** ✓ — 31 moves: `D R U2 F' D2 F2 D R U' R F2 R U' R2 U' L2 U R2 F2 B2 U D2 F2 U2 L2 D2 R2 F2 R2 U2 R2`
