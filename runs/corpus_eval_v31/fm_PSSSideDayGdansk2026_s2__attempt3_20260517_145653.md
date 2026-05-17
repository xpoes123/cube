# Run — fm_PSSSideDayGdansk2026_s2__attempt3_20260517_145653.json

**Scramble**: `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (30 moves, 56 tool calls)  
**Sim budget**: 725s / 3600s  
**Wall time**: 198s  
**Tokens**: 26,547 in (1,163,929 cached), 6,559 out  
**Cost estimate**: $0.566  
**Solution**: `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 2× = 568s
- `reset_slot`: 2× = 50s
- `htr_classify`: 3× = 45s
- `dr_recognize`: 6× = 18s
- `eo_pattern_lookup`: 5× = 15s
- `probe_dr_pattern`: 3× = 9s
- `apply_htr_phase`: 6× = 6s
- `apply_moves`: 16× = 6s
- `inspect_state`: 1× = 5s
- `niss_flip`: 1× = 2s
- `compose_niss_solution`: 1× = 1s
- `undo_moves`: 1× = 0s

---

_(turn 1: 716 in / 186 out / 12,972 cached, ~$-0.0301, 4.0s API)_

### Turn 1 — thinking

> Let me start by inspecting the state to see what we're working with. This is a fresh attempt, but I have context from two prior solves:
> - Attempt 1: 33 moves
> - Attempt 2: 31 moves
> 
> The instruction is clear: COMMIT HARD to one line, don't over-ideate, finish cleanly. Let me start with inspect_state to see the bad edges per axis and other key information.

**Turn 1 narration**:

I'll solve this scramble systematically. Let me start by inspecting the cube state to understand what I'm working with.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=4s]
  → EO: [], DR: [], bad_edges {'UD': 6, 'FB': 4, 'RL': 4}
_(turn 2: 774 in / 287 out / 12,972 cached, ~$-0.0284, 8.0s API)_

**Turn 2 narration**:

Good starting state. I see:
- **FB and RL axes both have 4 bad edges** (best EO candidates)
- **UD axis has 6 bad edges** (feasible but longer)
- **UD axis has 3 pairs on inverse** (strong NISS signal per Wen's pairs-tracing)
- **FB: DR-7C2E**, **RL: DR-6C2E** — both are reasonable starting points

Given the prior attempts reached 31-33 moves, I'll commit to one path and drive it cleanly. Let me scout EO on the normal side first for FB and RL (the 4-bad-edge axes), then check inverse if needed.

**FB-axis EO scouting** (4 bad edges on DR, DL, FR, BL):
FB-axis flipping moves are L, L', R, R'. Let me look at the pattern:

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=8s, wall=12s]
  → found=1, best=4m
_(turn 3: 1,150 in / 119 out / 12,972 cached, ~$-0.0298, 2.4s API)_

**Turn 3 narration**:

**RL-axis EO scouting** (4 bad edges on UL, DR, DF, FR):
RL-axis flipping moves are U, U', D, D'.

- `tool#3` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=11s, wall=14s]
  → found=1, best=4m
_(turn 4: 587 in / 106 out / 13,866 cached, ~$-0.0341, 3.1s API)_

**Turn 4 narration**:

Both FB and RL give 4-move EOs. Now let me check **inverse** for both axes since the UD axis showed 3 pairs on inverse (strong NISS signal). Let me flip and check FB on inverse:

- `tool#4` **niss_flip**({"slot":"main"}) [sim=13s, wall=17s]
  → (empty result)
_(turn 5: 718 in / 92 out / 14,733 cached, ~$-0.0362, 2.6s API)_

**Turn 5 narration**:

Now I'm on the inverse. Let me check FB-axis EO on inverse:

- `tool#5` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=16s, wall=20s]
  → found=1, best=2m
_(turn 6: 683 in / 152 out / 14,942 cached, ~$-0.0360, 3.8s API)_

**Turn 6 narration**:

**Excellent!** FB-axis on inverse gives a **2-move EO** (U2 R'). This is 2 moves shorter than the normal-side 4-move EOs. Combined with the 3 pairs on inverse signal, this is a strong candidate.

Let me also check RL-axis on inverse for completeness:

- `tool#6` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=19s, wall=24s]
  → found=1, best=4m
_(turn 7: 454 in / 207 out / 15,137 cached, ~$-0.0364, 4.4s API)_

**Turn 7 narration**:

RL on inverse is 5 moves (partial shown). So:
- **FB-inverse: 2-move EO** ✓
- **RL-inverse: 5-move EO**
- **FB-normal: 4-move EO**
- **RL-normal: 4-move EO**

Now let me probe DR options for the FB-inverse 2-move EO to see if the joint EO+DR is favorable:

- `tool#7` **probe_dr_pattern**({"slot":"main","eo_alg":["U2","R'"],"axis":"FB"}) [sim=22s, wall=28s]
  → found=1
_(turn 8: 545 in / 149 out / 15,632 cached, ~$-0.0383, 4.2s API)_

**Turn 8 narration**:

**FB-inverse: 2 EO + 7 DR = 9 total to DR** — that's good, but let me commit to the 2-move EO and then use dr_trigger_options to see the specific trigger families and substates. Applying the 2-move FB-inverse EO:

- `tool#8` **apply_moves**({"slot":"main","moves":["U2","R'"]}) [sim=22s, wall=33s]
  → hist=2m
  slot=main [INV] hist(2m): `U2 R'`
_(turn 9: 468 in / 126 out / 15,866 cached, ~$-0.0395, 3.1s API)_

**Turn 9 narration**:

Good. Now I'm EO-solved on FB-axis (on inverse side). Let me call dr_trigger_options to see what DR options I have:

- `tool#9` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=319s, wall=39s]
  → (empty result)
_(turn 10: 710 in / 165 out / 16,202 cached, ~$-0.0391, 4.4s API)_

**Turn 10 narration**:

**No DR trigger options found within 5 moves** on FB-inverse. This suggests the FB-axis might not be the best choice, or the DR is beyond the standard trigger families. Let me backtrack and try a different approach.

Given that the prior attempts reached 31-33 moves, let me try the **UD-axis on inverse** since it showed 3 pairs on inverse. Let me undo and test:

- `tool#10` **undo_moves**({"slot":"main","n":2}) [sim=319s, wall=43s]
  → hist=0m
_(turn 11: 708 in / 97 out / 16,409 cached, ~$-0.0407, 8.7s API)_

**Turn 11 narration**:

I'm back at the inverse scramble start. Let me check UD-axis EO on inverse:

- `tool#11` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=322s, wall=52s]
  → found=1, best=4m
_(turn 12: 385 in / 137 out / 16,591 cached, ~$-0.0416, 3.4s API)_

**Turn 12 narration**:

**UD-inverse: 4-move EO** (B R2 U F'). Let me probe DR for this:

- `tool#12` **probe_dr_pattern**({"slot":"main","eo_alg":["B","R2","U","F'"],"axis":"UD"}) [sim=325s, wall=55s]
  → found=1
_(turn 13: 383 in / 144 out / 17,137 cached, ~$-0.0430, 3.2s API)_

**Turn 13 narration**:

**UD-inverse: 4 EO + 4 DR = 8 total to DR** — this is better than FB-inverse (2 EO + 7 DR = 9). Let me commit to UD-inverse and apply the EO:

- `tool#13` **apply_moves**({"slot":"main","moves":["B","R2","U","F'"]}) [sim=326s, wall=58s]
  → hist=4m
  slot=main [INV] hist(4m): `B R2 U F'`
_(turn 14: 403 in / 124 out / 17,273 cached, ~$-0.0436, 3.9s API)_

**Turn 14 narration**:

Good! EO is solved on UD-axis (inverse side). Now let me call dr_trigger_options to see the specific trigger families:

- `tool#14` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=597s, wall=65s]
  → (empty result)
_(turn 15: 708 in / 106 out / 17,498 cached, ~$-0.0435, 2.8s API)_

**Turn 15 narration**:

Again no options within 5 moves. This is challenging. Let me use dr_recognize instead as a fallback to get the DR pattern beyond the trigger catalog:

- `tool#15` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=600s, wall=68s]
  → found=0
_(turn 16: 717 in / 114 out / 17,707 cached, ~$-0.0439, 3.4s API)_

**Turn 16 narration**:

The DR is 8 moves total (4 setup shown). Let me apply these 4 setup moves and then query again:

- `tool#16` **apply_moves**({"slot":"main","moves":["D'","U'","L2","R'"]}) [sim=601s, wall=71s]
  → hist=8m
  slot=main [INV] hist(8m): `B R2 U F' D' U' L2 R'`
_(turn 17: 401 in / 71 out / 17,893 cached, ~$-0.0460, 1.8s API)_

- `tool#17` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=604s, wall=73s]
  → found=1
_(turn 18: 357 in / 160 out / 18,382 cached, ~$-0.0462, 3.5s API)_

**Turn 18 narration**:

Good! The remaining DR is 4 moves (3 setup + 1 trigger). So total to DR is 8 + 4 = **12 moves** on UD-inverse. That's higher than the 8-move estimate, which means the probe was optimistic. Let me apply these final 4 DR moves:

- `tool#18` **apply_moves**({"slot":"main","moves":["U'","L'","U2","R'"]}) [sim=604s, wall=76s]
  → hist=12m
  slot=main [INV] hist(12m): `B R2 U F' D' U' L2 R' U' L' U2 R'`
_(turn 19: 418 in / 104 out / 18,606 cached, ~$-0.0474, 2.6s API)_

**Turn 19 narration**:

I'm now at DR on UD-axis (12 moves so far on inverse). Let me check the HTR state and classify the subset:

- `tool#19` **htr_classify**({"slot":"main","axis":"UD"}) [sim=619s, wall=79s]
  → subset=[2, 0, 3, 6, 1, 4, 5, 7]
_(turn 20: 609 in / 170 out / 18,687 cached, ~$-0.0461, 5.4s API)_

**Turn 20 narration**:

**This is concerning**: the HTR finish is 21 moves (11 reduction + 10 finish). Combined with 12 to DR, that's **33 total moves** — matching the first prior attempt. This path isn't better.

Let me reconsider. I'll reset and try the **normal side** instead. The prior attempts might have been on normal RL or FB. Let me reset and explore normal-side options more carefully:

- `tool#20` **reset_slot**({"slot":"main","rescramble":true}) [sim=644s, wall=85s]
  → (empty result)
_(turn 21: 554 in / 138 out / 19,017 cached, ~$-0.0476, 3.6s API)_

**Turn 21 narration**:

I'm back to the normal scramble. Let me try **RL-normal 4-move EO** and probe its DR:

- `tool#21` **probe_dr_pattern**({"slot":"main","eo_alg":["R2","B","F2","U'"],"axis":"RL"}) [sim=647s, wall=88s]
  → found=1
_(turn 22: 393 in / 133 out / 19,215 cached, ~$-0.0487, 3.3s API)_

**Turn 22 narration**:

**RL-normal: 4 EO + 4 DR = 8 total to DR** — same as UD-inverse. Let me commit to RL-normal and see if the finish is better:

- `tool#22` **apply_moves**({"slot":"main","moves":["R2","B","F2","U'"]}) [sim=647s, wall=92s]
  → hist=4m
  slot=main hist(4m): `R2 B F2 U'`
_(turn 23: 388 in / 71 out / 19,646 cached, ~$-0.0508, 1.9s API)_

- `tool#23` **dr_recognize**({"slot":"main","axis":"RL"}) [sim=650s, wall=93s]
  → found=0
_(turn 24: 364 in / 85 out / 19,814 cached, ~$-0.0511, 2.1s API)_

- `tool#24` **apply_moves**({"slot":"main","moves":["L'","B'","L'","R2"]}) [sim=651s, wall=95s]
  → hist=8m
  slot=main hist(8m): `R2 B F2 U' L' B' L' R2`
_(turn 25: 331 in / 71 out / 20,013 cached, ~$-0.0520, 1.7s API)_

- `tool#25` **dr_recognize**({"slot":"main","axis":"RL"}) [sim=654s, wall=97s]
  → found=1
_(turn 26: 321 in / 84 out / 20,079 cached, ~$-0.0520, 7.1s API)_

- `tool#26` **apply_moves**({"slot":"main","moves":["U2","B","R2","F'"]}) [sim=654s, wall=104s]
  → hist=12m
  slot=main hist(12m): `R2 B F2 U' L' B' L' R2 U2 B R2 F'`
_(turn 27: 334 in / 95 out / 20,260 cached, ~$-0.0523, 2.7s API)_

**Turn 27 narration**:

I'm at DR on RL-axis (12 moves). Let me classify the HTR subset:

- `tool#27` **htr_classify**({"slot":"main","axis":"RL"}) [sim=669s, wall=108s]
  → subset=[1, 0, 4, 2, 3, 5, 7, 6]
_(turn 28: 529 in / 126 out / 20,424 cached, ~$-0.0517, 3.8s API)_

**Turn 28 narration**:

Again **21-move finish** (10 + 11), giving **33 total** (12 + 21). This is the same as UD-inverse. Let me try **FB-normal** to see if it's any better:

- `tool#28` **reset_slot**({"slot":"main","rescramble":true}) [sim=694s, wall=111s]
  → (empty result)
_(turn 29: 506 in / 85 out / 20,596 cached, ~$-0.0528, 1.9s API)_

- `tool#29` **apply_moves**({"slot":"main","moves":["B2","L2","U2","R'"]}) [sim=695s, wall=113s]
  → hist=4m
  slot=main hist(4m): `B2 L2 U2 R'`
_(turn 30: 286 in / 70 out / 20,866 cached, ~$-0.0544, 1.7s API)_

- `tool#30` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=698s, wall=115s]
  → found=0
_(turn 31: 307 in / 84 out / 21,265 cached, ~$-0.0552, 1.7s API)_

- `tool#31` **apply_moves**({"slot":"main","moves":["R2","B'","D","L2"]}) [sim=698s, wall=117s]
  → hist=7m
  slot=main hist(7m): `B2 L2 U2 R B' D L2`
_(turn 32: 315 in / 93 out / 21,298 cached, ~$-0.0552, 2.5s API)_

**Turn 32 narration**:

There was an auto-cancel (R' + R2 = R). Good! Let me continue:

- `tool#32` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=701s, wall=119s]
  → found=1
_(turn 33: 329 in / 84 out / 21,447 cached, ~$-0.0557, 2.9s API)_

- `tool#33` **apply_moves**({"slot":"main","moves":["U","B2","F'","U'"]}) [sim=701s, wall=122s]
  → hist=11m
  slot=main hist(11m): `B2 L2 U2 R B' D L2 U B2 F' U'`
_(turn 34: 343 in / 96 out / 21,625 cached, ~$-0.0559, 2.5s API)_

**Turn 34 narration**:

I'm at DR in **11 moves** (1 move saved from cancel). Let me classify HTR:

- `tool#34` **htr_classify**({"slot":"main","axis":"FB"}) [sim=716s, wall=128s]
  → subset=[0, 1, 2, 5, 4, 3, 6, 7]
_(turn 35: 538 in / 158 out / 21,873 cached, ~$-0.0551, 6.2s API)_

**Turn 35 narration**:

**Better!** HTR finish is 19 moves (10 + 9), giving **30 total** (11 + 19). This is 1 move better than the prior best attempt (31). Let me proceed with the HTR finish and then see if I can optimize further:

- `tool#35` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=717s, wall=136s]
  → (empty result)
_(turn 36: 635 in / 84 out / 21,976 cached, ~$-0.0562, 2.1s API)_

- `tool#36` **apply_moves**({"slot":"main","moves":["F'","R2","F","L2"]}) [sim=718s, wall=138s]
  → hist=15m
  slot=main hist(15m): `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2`
_(turn 37: 433 in / 74 out / 22,242 cached, ~$-0.0576, 2.3s API)_

**Turn 37 narration**:

Let me do a quick_check to see if I've already reached an insertable residual:

- `tool#37` **quick_check**({"slot":"main"}) [sim=718s, wall=140s]
  → (empty result)
_(turn 38: 358 in / 113 out / 22,693 cached, ~$-0.0585, 2.6s API)_

**Turn 38 narration**:

Still in DR on FB, not yet HTR. Let me continue the HTR reduction:

- `tool#38` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=719s, wall=143s]
  → (empty result)
_(turn 39: 396 in / 85 out / 22,809 cached, ~$-0.0591, 1.9s API)_

- `tool#39` **apply_moves**({"slot":"main","moves":["F'","U2","R2","F'"]}) [sim=719s, wall=145s]
  → hist=19m
  slot=main hist(19m): `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F'`
_(turn 40: 403 in / 53 out / 23,068 cached, ~$-0.0603, 1.7s API)_

- `tool#40` **quick_check**({"slot":"main"}) [sim=719s, wall=146s]
  → (empty result)
_(turn 41: 351 in / 104 out / 23,304 cached, ~$-0.0603, 1.9s API)_

**Turn 41 narration**:

Still not HTR yet. Let me continue:

- `tool#41` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=720s, wall=148s]
  → (empty result)
_(turn 42: 322 in / 76 out / 23,421 cached, ~$-0.0611, 1.5s API)_

- `tool#42` **apply_moves**({"slot":"main","moves":["L2","B"]}) [sim=720s, wall=150s]
  → hist=21m
  slot=main hist(21m): `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B`
_(turn 43: 348 in / 53 out / 23,626 cached, ~$-0.0620, 1.6s API)_

- `tool#43` **quick_check**({"slot":"main"}) [sim=720s, wall=151s]
  → (empty result)
_(turn 44: 346 in / 114 out / 23,903 cached, ~$-0.0618, 2.5s API)_

**Turn 44 narration**:

Great! I'm now at **HTR** (21 moves). Now let me apply the finish phase:

- `tool#44` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=721s, wall=154s]
  → (empty result)
_(turn 45: 364 in / 85 out / 23,979 cached, ~$-0.0624, 1.8s API)_

- `tool#45` **apply_moves**({"slot":"main","moves":["U2","L2","U2","R2"]}) [sim=722s, wall=156s]
  → hist=25m
  slot=main hist(25m): `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2`
_(turn 46: 415 in / 53 out / 24,182 cached, ~$-0.0633, 2.0s API)_

- `tool#46` **quick_check**({"slot":"main"}) [sim=722s, wall=158s]
  → (empty result)
_(turn 47: 368 in / 101 out / 24,469 cached, ~$-0.0634, 2.2s API)_

**Turn 47 narration**:

Still not solved. Let me continue the finish:

- `tool#47` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=723s, wall=160s]
  → (empty result)
_(turn 48: 348 in / 85 out / 24,580 cached, ~$-0.0640, 2.0s API)_

- `tool#48` **apply_moves**({"slot":"main","moves":["B2","D2","U2","L2"]}) [sim=723s, wall=162s]
  → hist=29m
  slot=main hist(29m): `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2`
_(turn 49: 415 in / 53 out / 24,808 cached, ~$-0.0649, 1.5s API)_

- `tool#49` **quick_check**({"slot":"main"}) [sim=723s, wall=163s]
  → (empty result)
_(turn 50: 381 in / 90 out / 25,082 cached, ~$-0.0652, 1.8s API)_

- `tool#50` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=724s, wall=165s]
  → (empty result)
_(turn 51: 290 in / 73 out / 25,193 cached, ~$-0.0661, 1.6s API)_

- `tool#51` **apply_moves**({"slot":"main","moves":["U2"]}) [sim=724s, wall=167s]
  → hist=30m
  slot=main hist(30m): `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`
_(turn 52: 349 in / 53 out / 25,437 cached, ~$-0.0668, 2.0s API)_

- `tool#52` **quick_check**({"slot":"main"}) [sim=724s, wall=169s]
  → SOLVED
_(turn 53: 370 in / 102 out / 25,613 cached, ~$-0.0665, 3.3s API)_

**Turn 53 narration**:

**Excellent!** The cube is solved in **30 moves**. This is 1 move better than the prior best (31). Now let me apply cancellation to see if I can save any moves:

- `tool#53` **compose_niss_solution**({"slot":"main"}) [sim=725s, wall=172s]
  → solves=True
_(turn 54: 436 in / 102 out / 25,767 cached, ~$-0.0667, 4.3s API)_

**Turn 54 narration**:

The solution is already cancelled and verified at **30 moves**. Now, since I have a 30-move solution (≥27) and haven't called replace_and_shorten yet, let me try to apply it once to see if I can improve further. The tool will check the gates automatically:

- `tool#54` **budget_status**({}) [sim=725s, wall=176s]
  → sim=725s
_(turn 55: 567 in / 159 out / 26,003 cached, ~$-0.0661, 9.6s API)_

**Turn 55 narration**:

I have plenty of budget. Let me try replace_and_shorten on a suspicious span. Looking at the solution, the tail has many double moves which might be optimizable. Let me try the span from move 4 to the end:

- `tool#55` **replace_and_shorten**({"slot":"main","start":4,"end":30,"axis":"FB"}) [sim=725s, wall=186s]
  → ERROR: too few tool calls remaining (25) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 56: 494 in / 215 out / 26,278 cached, ~$-0.0662, 3.7s API)_

**Turn 56 narration**:

The tool gate blocks me because I don't have enough tool calls remaining. That's fine — I have a solid **30-move solution** which is 1 move better than the prior best. Let me verify and submit:

- `tool#56` **verify_solved**({"solution":["B2","L2","U2","R","B'","D","L2","U","B2","F'","U'","F'","R2","F","L2","F'","U2","R2","F'","L2","B","U2"...) [sim=725s, wall=190s]
  → solves=True, moves=30
_(turn 57: 426 in / 343 out / 26,581 cached, ~$-0.0653, 8.0s API)_

**Turn 57 narration**:

Perfect! The solution is verified. Let me submit it:

## FINAL_SOLUTION: ["B2", "L2", "U2", "R", "B'", "D", "L2", "U", "B2", "F'", "U'", "F'", "R2", "F", "L2", "F'", "U2", "R2", "F'", "L2", "B", "U2", "L2", "U2", "R2", "B2", "D2", "U2", "L2", "U2"]

**Solution summary:**
- **30 moves total** (1 move improvement over prior best of 31)
- **Approach:** FB-axis normal-side solve
  - **EO:** 4 moves (B2 L2 U2 R')
  - **DR:** 7 moves (with 1 cancel) → 11 moves total to DR
  - **HTR subset:** 2-swap mostly-axial
  - **HTR reduction:** 10 moves → 21 moves total to HTR
  - **Finish:** 9 moves → 30 moves total

The FB-normal axis gave the shortest overall path by producing a better HTR subset (19-move finish vs 21-move on other axes). The key was selecting the axis not just by shortest EO, but by the joint EO+DR+finish length, which FB-normal optimized best.


**verify_solved** ✓ — 30 moves: `B2 L2 U2 R B' D L2 U B2 F' U' F' R2 F L2 F' U2 R2 F' L2 B U2 L2 U2 R2 B2 D2 U2 L2 U2`
