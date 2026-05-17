# Run — fm_PSSSideDayGdansk2026_s3__attempt4_20260517_152555.json

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (27 moves, 56 tool calls)  
**Sim budget**: 924s / 3600s  
**Wall time**: 170s  
**Tokens**: 46,231 in (848,930 cached), 6,655 out  
**Cost estimate**: $0.535  
**Solution**: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`  

**Sim-time spent by tool**:

- `dr_trigger_options`: 3× = 796s
- `reset_slot`: 2× = 50s
- `dr_recognize`: 7× = 21s
- `htr_classify`: 3× = 17s
- `eo_pattern_lookup`: 3× = 9s
- `probe_dr_pattern`: 3× = 9s
- `niss_flip`: 3× = 6s
- `apply_moves`: 15× = 5s
- `inspect_state`: 1× = 5s
- `apply_htr_phase`: 5× = 5s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 764 in / 295 out / 12,982 cached, ~$-0.0283, 8.0s API)_

### Turn 1 — thinking

> Looking at the prior attempts, I've hit 27 moves three times with the exact same solution. This suggests I'm converging on a good path but need to either:
> 1. Find a better initial EO/DR axis choice
> 2. Optimize the HTR/finish phase
> 3. Use replace_and_shorten effectively
> 
> The instructions emphasize: COMMIT HARD this attempt. Pick a line and drive it clean. Don't over-ideate.
> 
> Let me start by inspecting the state, then systematically scout EO options on both normal and inverse frames. I'll compare EO+DR jointly before committing.
> 
> The scramble is:
> R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F
> 
> Let me begin.

**Turn 1 narration**:

I'll solve this scramble systematically, learning from the 27-move plateau. Let me start by inspecting the state to understand the EO landscape.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=8s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 8, 'RL': 6}
_(turn 2: 901 in / 230 out / 12,982 cached, ~$-0.0289, 6.0s API)_

**Turn 2 narration**:

Good! I see:
- **UD: 4 bad edges** (UL, DR, DL, DB) — most promising for EO
- **FB: 8 bad edges** — likely harder
- **RL: 6 bad edges** — middle ground
- **UD has 3 pairs on inverse** — strong NISS signal

**Key insight**: The prior 27-move attempts likely started on UD-normal. With `top_pairs_on_inverse: 3`, I should check the inverse frame first. NISS-first rule applies here.

Let me scout both UD-normal and UD-inverse EO, then compare their DR options.

- `tool#2` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=8s, wall=14s]
  → found=1, best=4m
_(turn 3: 1,218 in / 146 out / 12,982 cached, ~$-0.0292, 2.8s API)_

**Turn 3 narration**:

**UD-normal EO: 4 moves** (U L R' B'). Now let me check the inverse frame for UD-axis:

- `tool#3` **niss_flip**({"slot":"main"}) [sim=10s, wall=17s]
  → (empty result)
- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=13s, wall=17s]
  → found=1, best=4m
_(turn 4: 1,013 in / 169 out / 14,033 cached, ~$-0.0323, 3.3s API)_

**Turn 4 narration**:

**UD-inverse EO: also 4 moves** (B' R' U B'). Same length! Now I need to compare DR options for both. With 3 pairs on inverse, the inverse frame should give a better DR. Let me probe DR for both:

- `tool#5` **probe_dr_pattern**({"slot":"main","eo_alg":["B'","R'","U","B'"],"axis":"UD"}) [sim=16s, wall=20s]
  → found=1
_(turn 5: 930 in / 186 out / 14,861 cached, ~$-0.0345, 7.3s API)_

**Turn 5 narration**:

**UD-inverse: EO 4mv + DR 9mv = 13mv to DR** — not bad! Now let me check the normal side (need to flip back first):

- `tool#6` **niss_flip**({"slot":"main"}) [sim=18s, wall=27s]
  → (empty result)
- `tool#7` **probe_dr_pattern**({"slot":"main","eo_alg":["U","L","R'","B'"],"axis":"UD"}) [sim=21s, wall=27s]
  → found=1
_(turn 6: 947 in / 207 out / 15,038 cached, ~$-0.0347, 5.1s API)_

**Turn 6 narration**:

Interesting! **UD-normal: EO 4mv + DR 8mv = 12mv to DR** — 1 move better than inverse! But with 3 pairs on inverse, the POST-DR cost (HTR+finish) is likely cheaper on inverse. Let me commit to **UD-normal** first since it's 1mv shorter to DR, then I can evaluate the HTR substate quality.

**Decision**: Going with UD-normal EO (U L R' B'), then exploring DR options with dr_trigger_options.

- `tool#8` **apply_moves**({"slot":"main","moves":["U","L","R'","B'"]}) [sim=21s, wall=32s]
  → hist=4m
  slot=main hist(4m): `U L R' B'`
_(turn 7: 979 in / 121 out / 15,810 cached, ~$-0.0379, 2.6s API)_

**Turn 7 narration**:

Good! EO on UD is now solved (4 moves). Now let me examine DR options with dr_trigger_options:

- `tool#9` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":6}) [sim=253s, wall=37s]
  → (empty result)
_(turn 8: 776 in / 125 out / 15,972 cached, ~$-0.0389, 3.3s API)_

**Turn 8 narration**:

**No DR triggers found within 5-move setup!** This is unexpected. The probe said 8 moves total to DR, so there should be a path. Let me fall back to dr_recognize to see what the raw DR pattern looks like:

- `tool#10` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=256s, wall=40s]
  → found=0
_(turn 9: 740 in / 184 out / 16,791 cached, ~$-0.0404, 3.8s API)_

**Turn 9 narration**:

Ah! The DR is 8 moves but the trigger isn't visible yet. I see 4 moves of setup (F2 D' R' U'). Let me apply these and continue:

- `tool#11` **apply_moves**({"slot":"main","moves":["F2","D'","R'","U'"]}) [sim=256s, wall=44s]
  → hist=8m
  slot=main hist(8m): `U L R' B' F2 D' R' U'`
- `tool#12` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=260s, wall=44s]
  → found=1
_(turn 10: 637 in / 262 out / 16,974 cached, ~$-0.0400, 6.9s API)_

**Turn 10 narration**:

Great! I see the remaining DR: setup F2 L' D', trigger R'. That's 4 more moves. Total DR: 4 (EO) + 4 (first setup) + 4 (final setup+trigger) = **12 moves to DR**.

Wait, that's 12 moves to DR, but the probe said 8. Let me check — ah, I already applied 4 moves of setup, so I'm at 8 moves history. The remaining is 4 moves, giving 12 total. That's longer than the 8 the probe reported. Let me verify by applying:

- `tool#13` **apply_moves**({"slot":"main","moves":["F2","L'","D'","R'"]}) [sim=260s, wall=51s]
  → hist=12m
  slot=main hist(12m): `U L R' B' F2 D' R' U' F2 L' D' R'`
- `tool#14` **quick_check**({"slot":"main"}) [sim=260s, wall=51s]
  → (empty result)
_(turn 11: 918 in / 102 out / 17,482 cached, ~$-0.0429, 5.0s API)_

**Turn 11 narration**:

Perfect! DR on UD is reached in 12 moves. Now let me classify the HTR substate to understand the finish cost:

- `tool#15` **htr_classify**({"slot":"main","axis":"UD"}) [sim=261s, wall=56s]
  → subset=[0, 4, 1, 5, 6, 2, 7, 3]
_(turn 12: 876 in / 192 out / 17,722 cached, ~$-0.0423, 4.8s API)_

**Turn 12 narration**:

**HTR substate: 4-swap long-cycle**
- HTR reduction: 8 moves
- Finish: 11 moves
- **Total post-DR: 19 moves**

**Current total: 12 (to DR) + 19 (finish) = 31 moves** — that's worse than my 27-move best!

This path isn't optimal. Let me backtrack and try the inverse frame instead, which had 3 pairs preserved. Let me reset and try UD-inverse:

- `tool#16` **reset_slot**({"slot":"main","rescramble":true}) [sim=286s, wall=61s]
  → (empty result)
_(turn 13: 581 in / 138 out / 18,219 cached, ~$-0.0454, 3.4s API)_

**Turn 13 narration**:

Now let me go to inverse and apply the 4-move EO:

- `tool#17` **niss_flip**({"slot":"main"}) [sim=288s, wall=64s]
  → (empty result)
- `tool#18` **apply_moves**({"slot":"main","moves":["B'","R'","U","B'"]}) [sim=288s, wall=64s]
  → hist=4m
  slot=main [INV] hist(4m): `B' R' U B'`
_(turn 14: 877 in / 109 out / 18,611 cached, ~$-0.0460, 2.9s API)_

**Turn 14 narration**:

Good! Now on inverse with EO done. Let me check DR options:

- `tool#19` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":6}) [sim=596s, wall=70s]
  → (empty result)
_(turn 15: 1,147 in / 95 out / 19,059 cached, ~$-0.0466, 3.0s API)_

**Turn 15 narration**:

Again, no triggers found. The inverse side also needs a longer DR setup. Let me use dr_recognize:

- `tool#20` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=599s, wall=73s]
  → found=0
_(turn 16: 695 in / 188 out / 19,160 cached, ~$-0.0468, 5.4s API)_

**Turn 16 narration**:

The inverse path has a 9-move DR (vs 8 on normal). This matches the probe earlier (inverse was 13mv to DR = 4 EO + 9 DR). Let me continue with this setup:

- `tool#21` **apply_moves**({"slot":"main","moves":["L","R'","D","L'"]}) [sim=600s, wall=79s]
  → hist=8m
  slot=main [INV] hist(8m): `B' R' U B' L R' D L'`
- `tool#22` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=603s, wall=79s]
  → found=0
_(turn 17: 613 in / 152 out / 19,853 cached, ~$-0.0495, 2.3s API)_

**Turn 17 narration**:

Still 5 more moves to go. Let me continue:

- `tool#23` **apply_moves**({"slot":"main","moves":["U'","L'","D","U'"]}) [sim=603s, wall=81s]
  → hist=12m
  slot=main [INV] hist(12m): `B' R' U B' L R' D L' U' L' D U'`
- `tool#24` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=606s, wall=81s]
  → found=1
_(turn 18: 782 in / 153 out / 20,331 cached, ~$-0.0503, 2.9s API)_

**Turn 18 narration**:

Perfect! Just 1 more move (R') to reach DR. Total: 4 (EO) + 9 (DR) = **13 moves to DR** (on inverse).

- `tool#25` **apply_moves**({"slot":"main","moves":["R'"]}) [sim=606s, wall=84s]
  → hist=13m
  slot=main [INV] hist(13m): `B' R' U B' L R' D L' U' L' D U' R'`
- `tool#26` **quick_check**({"slot":"main"}) [sim=606s, wall=84s]
  → (empty result)
_(turn 19: 781 in / 108 out / 20,573 cached, ~$-0.0516, 2.8s API)_

**Turn 19 narration**:

Great! DR reached in 13 moves on inverse. Now let me classify the HTR substate to see if the 3 pairs preserved give a better finish:

- `tool#27` **htr_classify**({"slot":"main","axis":"UD"}) [sim=621s, wall=87s]
  → subset=[1, 0, 2, 7, 4, 3, 6, 5]
_(turn 20: 798 in / 248 out / 20,948 cached, ~$-0.0504, 6.1s API)_

**Turn 20 narration**:

**Inverse HTR substate: 2-swap mostly-axial**
- HTR reduction: 10 moves
- Finish: 8 moves
- **Total post-DR: 18 moves**

**Inverse total: 13 (to DR) + 18 (finish) = 31 moves** — same as normal!

Both paths are giving 31 moves. My prior attempts were 27 moves, so something's different. Let me try a different EO axis. Let me check FB axis:

- `tool#28` **reset_slot**({"slot":"main","rescramble":true}) [sim=646s, wall=93s]
  → (empty result)
- `tool#29` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=649s, wall=93s]
  → found=1, best=4m
_(turn 21: 795 in / 140 out / 21,339 cached, ~$-0.0531, 3.4s API)_

**Turn 21 narration**:

**FB-normal EO: 4 moves** (R' F D L'). Same length as UD! Let me probe DR for FB:

- `tool#30` **probe_dr_pattern**({"slot":"main","eo_alg":["R'","F","D","L'"],"axis":"FB"}) [sim=652s, wall=96s]
  → found=1
_(turn 22: 608 in / 199 out / 21,739 cached, ~$-0.0539, 3.9s API)_

**Turn 22 narration**:

**FB-normal: EO 4mv + DR 7mv = 11mv to DR** — that's 1 move better than UD! Let me commit to this path:

- `tool#31` **apply_moves**({"slot":"main","moves":["R'","F","D","L'"]}) [sim=653s, wall=100s]
  → hist=4m
  slot=main hist(4m): `R' F D L'`
- `tool#32` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":6}) [sim=909s, wall=103s]
  → (empty result)
_(turn 23: 885 in / 84 out / 22,213 cached, ~$-0.0561, 3.0s API)_

**Turn 23 narration**:

No triggers on FB either. Let me use dr_recognize:

- `tool#33` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=912s, wall=106s]
  → found=0
_(turn 24: 871 in / 151 out / 22,567 cached, ~$-0.0561, 3.7s API)_

**Turn 24 narration**:

7 moves total to DR on FB. Let me continue:

- `tool#34` **apply_moves**({"slot":"main","moves":["B'","D","F'","U'"]}) [sim=912s, wall=109s]
  → hist=8m
  slot=main hist(8m): `R' F D L' B' D F' U'`
- `tool#35` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=915s, wall=109s]
  → found=1
_(turn 25: 551 in / 159 out / 22,756 cached, ~$-0.0574, 3.3s API)_

**Turn 25 narration**:

Good! 3 more moves to DR (B L2 D'). Total FB: 4 (EO) + 7 (DR) = **11 moves to DR**.

- `tool#36` **apply_moves**({"slot":"main","moves":["B","L2","D'"]}) [sim=915s, wall=113s]
  → hist=11m
  slot=main hist(11m): `R' F D L' B' D F' U' B L2 D'`
- `tool#37` **quick_check**({"slot":"main"}) [sim=915s, wall=113s]
  → (empty result)
_(turn 26: 765 in / 94 out / 23,397 cached, ~$-0.0595, 2.5s API)_

**Turn 26 narration**:

Perfect! DR on FB reached in 11 moves. Now let me classify the HTR substate:

- `tool#38` **htr_classify**({"slot":"main","axis":"FB"}) [sim=916s, wall=115s]
  → subset=[2, 0, 4, 7, 1, 6, 3, 5]
_(turn 27: 754 in / 208 out / 23,603 cached, ~$-0.0583, 4.5s API)_

**Turn 27 narration**:

**FB HTR substate: 4-swap long-cycle**
- HTR reduction: 8 moves
- Finish: 9 moves
- **Total post-DR: 17 moves**

**FB total: 11 (to DR) + 17 (finish) = 28 moves** — still 1 move worse than 27!

But wait, this is closer. Let me check if there are cancellations possible. Let me apply the HTR phases and look for opportunities:

- `tool#39` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=917s, wall=120s]
  → (empty result)
_(turn 28: 668 in / 158 out / 23,989 cached, ~$-0.0604, 2.9s API)_

**Turn 28 narration**:

HTR reduction is 8 moves, I see the first 4 (D2 F2 R2 U2). Let me apply and check state:

- `tool#40` **apply_moves**({"slot":"main","moves":["D2","F2","R2","U2"]}) [sim=918s, wall=123s]
  → hist=14m
  slot=main hist(14m): `R' F D L' B' D F' U' B L2 D F2 R2 U2`
- `tool#41` **quick_check**({"slot":"main"}) [sim=918s, wall=123s]
  → (empty result)
_(turn 29: 735 in / 120 out / 24,367 cached, ~$-0.0618, 2.5s API)_

**Turn 29 narration**:

Good! 1 move already cancelled (D' + D2 became D). Let me continue the HTR reduction:

- `tool#42` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=919s, wall=125s]
  → (empty result)
_(turn 30: 613 in / 120 out / 24,830 cached, ~$-0.0634, 2.0s API)_

- `tool#43` **apply_moves**({"slot":"main","moves":["F'","U2","L2","B"]}) [sim=919s, wall=127s]
  → hist=18m
  slot=main hist(18m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B`
- `tool#44` **quick_check**({"slot":"main"}) [sim=919s, wall=127s]
  → (empty result)
_(turn 31: 591 in / 115 out / 25,066 cached, ~$-0.0642, 2.9s API)_

**Turn 31 narration**:

Great! HTR is reached in 18 moves (saved 1 from cancellation). Now the finish:

- `tool#45` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=920s, wall=130s]
  → (empty result)
_(turn 32: 611 in / 121 out / 25,481 cached, ~$-0.0652, 2.1s API)_

- `tool#46` **apply_moves**({"slot":"main","moves":["R2","U2","B2","R2"]}) [sim=921s, wall=132s]
  → hist=22m
  slot=main hist(22m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2`
- `tool#47` **quick_check**({"slot":"main"}) [sim=921s, wall=132s]
  → (empty result)
_(turn 33: 629 in / 90 out / 25,682 cached, ~$-0.0661, 1.8s API)_

- `tool#48` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=922s, wall=134s]
  → (empty result)
_(turn 34: 602 in / 121 out / 26,071 cached, ~$-0.0668, 2.8s API)_

- `tool#49` **apply_moves**({"slot":"main","moves":["F2","U2","B2","D2"]}) [sim=922s, wall=137s]
  → hist=26m
  slot=main hist(26m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2`
- `tool#50` **quick_check**({"slot":"main"}) [sim=922s, wall=137s]
  → (empty result)
_(turn 35: 619 in / 90 out / 26,300 cached, ~$-0.0678, 2.1s API)_

- `tool#51` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=923s, wall=139s]
  → (empty result)
_(turn 36: 573 in / 109 out / 26,592 cached, ~$-0.0684, 2.9s API)_

- `tool#52` **apply_moves**({"slot":"main","moves":["F2"]}) [sim=923s, wall=142s]
  → hist=27m
  slot=main hist(27m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
- `tool#53` **quick_check**({"slot":"main"}) [sim=923s, wall=142s]
  → SOLVED
_(turn 37: 566 in / 181 out / 26,909 cached, ~$-0.0682, 4.1s API)_

**Turn 37 narration**:

**SOLVED in 27 moves!** This matches my previous best. The solution is:

R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2

Now, let me try to optimize with replace_and_shorten. I have 27 moves and plenty of budget (30 tool calls). Let me see if I can improve this:

- `tool#54` **compose_niss_solution**({"slot":"main"}) [sim=924s, wall=146s]
  → solves=True
_(turn 38: 779 in / 66 out / 27,217 cached, ~$-0.0702, 2.2s API)_

**Turn 38 narration**:

Perfect! The solution is verified. Now let me try replace_and_shorten on a large tail to see if I can save moves:

- `tool#55` **budget_status**({}) [sim=924s, wall=148s]
  → sim=924s
_(turn 39: 619 in / 141 out / 27,478 cached, ~$-0.0702, 2.8s API)_

**Turn 39 narration**:

Good! I have plenty of budget. Let me try replace_and_shorten on the tail of the solution (say from move 4 onward):

- `tool#56` **replace_and_shorten**({"slot":"main","start":4,"end":27,"axis":"FB"}) [sim=924s, wall=151s]
  → ERROR: too few tool calls remaining (24) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 40: 461 in / 497 out / 27,969 cached, ~$-0.0667, 11.7s API)_

**Turn 40 narration**:

I don't have enough tool calls remaining for replace_and_shorten (need 30, have 24). Let me submit the current 27-move solution. This matches my previous best, and I've verified it solves correctly.

Let me compose the final solution:

**FINAL_SOLUTION**: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]

## Solution Summary

**Total: 27 moves** (matches previous best)

**Breakdown:**
- **EO on FB axis**: R' F D L' (4 moves) — chose FB over UD because it had a shorter path to DR (11mv vs 12mv)
- **DR on FB**: B' D F' U' B L2 D' (7 moves, with 1 cancellation D'+D2→D)
- **HTR reduction**: D F2 R2 U2 F' U2 L2 B (8 moves, after cancellation)
- **HTR finish**: R2 U2 B2 R2 F2 U2 B2 D2 F2 (9 moves)

**Key decisions:**
1. Compared UD-normal (12mv to DR), UD-inverse (13mv to DR), and FB-normal (11mv to DR)
2. Committed to FB-normal as it gave the shortest path to DR
3. The 4-swap long-cycle HTR substate required 17 moves post-DR (8 reduction + 9 finish)
4. One move saved via automatic cancellation (D' + D2 → D)

The solution reached the same 27-move count as my previous three attempts. Without enough budget for replace_and_shorten, this is the best I can deliver on this attempt.

> **user**: You stopped without calling tools or emitting FINAL_SOLUTION. Either continue with tools, or output FINAL_SOLUTION: ["...", ...].

_(turn 41: 15,963 in / 281 out / 12,982 cached, ~$0.0171, 7.1s API)_

### Turn 41 — thinking

> You're right - I summarized but didn't actually emit the FINAL_SOLUTION in the required format. I need to output it now.
> 
> I already have a verified 27-move solution from compose_niss_solution:
> ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]
> 
> Let me emit this as the final solution.

**Turn 41 narration**:

FINAL_SOLUTION: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]


**verify_solved** ✓ — 27 moves: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
