# Run — fm_PSSSideDayGdansk2026_s3__attempt4_20260517_102502.json

**Scramble**: `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`  
**Model**: `claude-sonnet-4-5-20250929`  
**Result**: ✓ SOLVED (27 moves, 53 tool calls)  
**Sim budget**: 189s / 3600s  
**Wall time**: 183s  
**Tokens**: 32,123 in (857,744 cached), 6,574 out  
**Cost estimate**: $0.496  
**Solution**: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`  

**Sim-time spent by tool**:

- `apply_moves`: 11× = 40s
- `niss_flip`: 6× = 30s
- `reset_slot`: 1× = 30s
- `dr_trigger_options`: 2× = 16s
- `htr_classify`: 2× = 16s
- `inspect_state`: 3× = 15s
- `eo_pattern_lookup`: 5× = 15s
- `dr_recognize`: 4× = 12s
- `probe_dr_pattern`: 3× = 9s
- `apply_htr_phase`: 5× = 5s
- `compose_niss_solution`: 1× = 1s

---

_(turn 1: 779 in / 323 out / 12,867 cached, ~$-0.0276, 8.8s API)_

### Turn 1 — thinking

> Looking at the prior attempts, all three attempts yielded exactly 30 moves with the same solution. This suggests the solver was getting stuck in the same path. The instructions are clear: COMMIT HARD this attempt, pick a line, and drive it to a clean finish.
> 
> Let me start by inspecting the state to understand what we're working with, then I'll:
> 1. Scout EO options across axes (both normal and inverse)
> 2. Check DR options for each viable EO
> 3. Pick the joint-best EO+DR path
> 4. Drive through to HTR+finish
> 5. Apply replace_and_shorten if the solution is ≥27 moves and I have budget
> 
> The key insight from the instructions: the prior 30-move solutions suggest I should look for a DIFFERENT axis or DIFFERENT side (inverse) to break out of that pattern.
> 
> Let me start.

**Turn 1 narration**:

I'll solve this scramble by committing hard to one clean path. Looking at the prior attempts all yielding exactly 30 moves with identical solutions, I need to explore different branches this time—likely a different axis or the inverse side.

Let's begin with a thorough inspection and systematic EO scouting.

- `tool#1` **inspect_state**({"slot":"main"}) [sim=5s, wall=9s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 8, 'RL': 6}
_(turn 2: 929 in / 234 out / 12,867 cached, ~$-0.0284, 6.5s API)_

**Turn 2 narration**:

**STATE READING:**
- UD axis: 4 bad edges (UL, DR, DL, DB) — EO-favorable
- FB axis: 8 bad edges — worst EO
- RL axis: 6 bad edges
- **DR-closeness**: all axes show poor DR signatures (7C3E, 6C3E, 5C3E — none are good trigger patterns)
- **KEY SIGNAL**: `top_pairs_on_inverse: 3` on UD axis — this is a STRONG NISS switch signal per the rules

**STRATEGY**: The 3 pairs on inverse + UD having the best EO (4 bad edges) suggests I should check the INVERSE side first. Let me flip to inverse and scout EO there.

- `tool#2` **niss_flip**({"slot":"main"}) [sim=10s, wall=15s]
  → (empty result)
_(turn 3: 1,578 in / 77 out / 12,867 cached, ~$-0.0289, 2.5s API)_

**Turn 3 narration**:

Good, now I'm on the inverse side. Let me inspect the inverse state and scout EO options there.

- `tool#3` **inspect_state**({"slot":"main"}) [sim=15s, wall=18s]
  → EO: [], DR: [], bad_edges {'UD': 4, 'FB': 8, 'RL': 6}
_(turn 4: 1,327 in / 177 out / 13,961 cached, ~$-0.0311, 5.3s API)_

**Turn 4 narration**:

Interesting — the inverse side also shows 4 bad edges on UD axis (different slots though). Let me scout EO options on both normal and inverse UD axes systematically.

**SCOUTING PLAN:**
1. Check inverse-UD EO (currently flipped)
2. Flip back to normal and check normal-UD EO
3. Compare both for EO length + DR prospects
4. Commit to the joint-best path

- `tool#4` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=18s, wall=23s]
  → found=1, best=4m
_(turn 5: 942 in / 94 out / 14,793 cached, ~$-0.0357, 2.9s API)_

**Turn 5 narration**:

Inverse-UD EO is 4 moves: `B' R' U B'`. Now let me flip back to normal side and check normal-UD EO.

- `tool#5` **niss_flip**({"slot":"main"}) [sim=23s, wall=26s]
  → (empty result)
_(turn 6: 776 in / 74 out / 15,286 cached, ~$-0.0378, 2.0s API)_

- `tool#6` **eo_pattern_lookup**({"slot":"main","axis":"UD"}) [sim=26s, wall=28s]
  → found=1, best=4m
_(turn 7: 671 in / 215 out / 16,061 cached, ~$-0.0381, 5.0s API)_

**Turn 7 narration**:

**EO COMPARISON:**
- **Normal-UD**: `U L R' B'` (4 moves)
- **Inverse-UD**: `B' R' U B'` (4 moves)

Both are 4 moves. Now I need to check DR prospects for each. The inspect_state showed poor DR-closeness (7C3E) on both sides, so let me probe DR for both EO candidates to see which gives a better DR path.

- `tool#7` **probe_dr_pattern**({"slot":"main","eo_alg":["U","L","R'","B'"],"axis":"UD"}) [sim=29s, wall=33s]
  → found=1
_(turn 8: 441 in / 184 out / 16,244 cached, ~$-0.0398, 3.6s API)_

**Turn 8 narration**:

Normal-UD EO gives DR in 8 moves total (4 EO + 4 RZP to DR). Now let me probe inverse-UD:

- `tool#8` **niss_flip**({"slot":"main"}) [sim=34s, wall=37s]
  → (empty result)
- `tool#9` **probe_dr_pattern**({"slot":"main","eo_alg":["B'","R'","U","B'"],"axis":"UD"}) [sim=37s, wall=37s]
  → found=1
_(turn 9: 986 in / 262 out / 16,663 cached, ~$-0.0381, 6.0s API)_

**Turn 9 narration**:

**DR PROBE RESULTS:**
- **Normal-UD**: EO=4, DR total=8 (so 4 moves RZP after EO)
- **Inverse-UD**: EO=4, DR total=9 (so 5 moves RZP after EO)

The normal-UD path is 1 move shorter to DR (8 vs 9). However, I should also check the DR trigger options to see what SUBSTATE each reaches — a longer DR with a better substate might win. Let me commit to normal-UD EO first and check dr_trigger_options.

- `tool#10` **niss_flip**({"slot":"main"}) [sim=42s, wall=43s]
  → (empty result)
- `tool#11` **apply_moves**({"slot":"main","moves":["U","L","R'","B'"]}) [sim=46s, wall=43s]
  → hist=4m
  slot=main hist(4m): `U L R' B'`
_(turn 10: 1,484 in / 132 out / 17,037 cached, ~$-0.0396, 3.1s API)_

**Turn 10 narration**:

Good! I've committed the normal-UD EO: `U L R' B'` (4 moves). Now let me check DR trigger options on the UD axis.

- `tool#12` **dr_trigger_options**({"slot":"main","axis":"UD","max_setup":5}) [sim=54s, wall=48s]
  → (empty result)
_(turn 11: 1,030 in / 122 out / 17,195 cached, ~$-0.0415, 3.8s API)_

**Turn 11 narration**:

**PROBLEM**: No DR trigger options found within 5 moves of setup! This suggests the DR path here is quite long or doesn't fit the named trigger families. Let me try dr_recognize to see what the actual DR pattern is.

- `tool#13` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=57s, wall=52s]
  → found=0
_(turn 12: 483 in / 183 out / 18,005 cached, ~$-0.0444, 4.2s API)_

**Turn 12 narration**:

The DR from this EO is 8 moves total (4 more moves after the 4-move EO), which matches the probe. Let me apply the 4 setup moves and continue.

- `tool#14` **apply_moves**({"slot":"main","moves":["F2","D'","R'","U'"]}) [sim=61s, wall=56s]
  → hist=8m
  slot=main hist(8m): `U L R' B' F2 D' R' U'`
- `tool#15` **dr_recognize**({"slot":"main","axis":"UD"}) [sim=64s, wall=56s]
  → found=1
_(turn 13: 629 in / 106 out / 18,719 cached, ~$-0.0471, 3.2s API)_

**Turn 13 narration**:

Wait, something is wrong here. dr_recognize says the DR from THIS state (after 8 moves) is only 4 more moves. But I already applied 4 moves and it's still not DR. Let me check current state:

- `tool#16` **inspect_state**({"slot":"main"}) [sim=69s, wall=59s]
  → EO: ['UD'], DR: [], bad_edges {'UD': 0, 'FB': 8, 'RL': 4}
_(turn 14: 1,105 in / 328 out / 18,962 cached, ~$-0.0430, 7.9s API)_

**Turn 14 narration**:

Good! UD-axis EO is now solved (0 bad edges on UD). Current DR-closeness shows:
- UD: DR-7C4E (bad — would need many moves)
- **RL: DR-4C2E** (this is a GOOD trigger pattern! `R U2 R'` family, typical post-DR 9-11 moves)

But wait — I'm committed to UD axis. The dr_recognize output says I need 4 more moves: `F2 L' D'` setup + `R'` trigger. But that doesn't make sense on UD axis when the signature is 7C4E. 

Let me re-read: the dr_recognize is still looking at UD axis and says the trigger is a "single inverse" (R'). The setup is F2 L' D'. Total 4 moves. Let me apply these:

- `tool#17` **apply_moves**({"slot":"main","moves":["F2","L'","D'","R'"]}) [sim=73s, wall=67s]
  → hist=12m
  slot=main hist(12m): `U L R' B' F2 D' R' U' F2 L' D' R'`
- `tool#18` **quick_check**({"slot":"main"}) [sim=73s, wall=67s]
  → (empty result)
_(turn 15: 1,288 in / 166 out / 19,201 cached, ~$-0.0455, 5.2s API)_

**Turn 15 narration**:

Perfect! I've reached DR on the UD axis in 12 moves total: `U L R' B' F2 D' R' U' F2 L' D' R'`. 

That's 4 EO + 8 DR = 12 moves to DR. This is slightly high (elite target is ≤11) but acceptable. Now I need to proceed through HTR and finish.

- `tool#19` **htr_classify**({"slot":"main","axis":"UD"}) [sim=74s, wall=73s]
  → subset=[0, 4, 1, 5, 6, 2, 7, 3]
_(turn 16: 1,000 in / 323 out / 19,578 cached, ~$-0.0450, 9.8s API)_

**Turn 16 narration**:

**HTR SUBSET**: 4-swap long-cycle with a 7-cycle structure. This is a tough subset:
- HTR reduction: 8 moves
- Finish: 11 moves
- Total post-DR: 19 moves

**PROJECTED TOTAL**: 12 (to DR) + 19 (HTR+finish) = **31 moves**

This is WORSE than the prior 30-move attempts! The long-cycle subset is very expensive. Let me reconsider — maybe I should backtrack and try the RL axis instead, which showed DR-4C2E (a much better trigger).

However, the instructions say "COMMIT HARD" and "do NOT abandon a path halfway through." But I'm only 12 moves in and I can see this will exceed 30 moves. Let me check if there's an opportunistic 3-cycle residual that might appear during the finish.

Actually, let me take a step back. The prior 30-move solutions all used the same path. Maybe I need to try a COMPLETELY different approach — like starting from the inverse side with a different axis, or trying FB/RL axis from the start.

Let me reset and try a different axis path. The cost is 30s but I have budget.

- `tool#20` **budget_status**({}) [sim=74s, wall=82s]
  → sim=74s
_(turn 17: 878 in / 114 out / 20,473 cached, ~$-0.0509, 3.6s API)_

**Turn 17 narration**:

I have plenty of budget (3526s remaining). Let me reset and try the RL axis path, which showed DR-4C2E signature — that's a MUCH better substate.

- `tool#21` **reset_slot**({"slot":"main","rescramble":true}) [sim=104s, wall=86s]
  → (empty result)
_(turn 18: 598 in / 108 out / 20,929 cached, ~$-0.0531, 3.3s API)_

**Turn 18 narration**:

**RESET COMPLETE**. Now let me scout RL-axis EO options. From the initial inspect, RL had 6 bad edges.

- `tool#22` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=107s, wall=89s]
  → found=1, best=4m
_(turn 19: 375 in / 144 out / 21,508 cached, ~$-0.0548, 3.2s API)_

**Turn 19 narration**:

RL-axis EO is 5 moves (4 visible + 1 more). Let me also check inverse-RL to compare:

- `tool#23` **niss_flip**({"slot":"main"}) [sim=112s, wall=93s]
  → (empty result)
- `tool#24` **eo_pattern_lookup**({"slot":"main","axis":"RL"}) [sim=115s, wall=93s]
  → found=1, best=4m
_(turn 20: 962 in / 153 out / 21,759 cached, ~$-0.0536, 6.5s API)_

**Turn 20 narration**:

Both normal and inverse RL axes need 5-move EO. That's longer than the 4-move UD EO I tried earlier. Let me also check FB axis for completeness:

- `tool#25` **niss_flip**({"slot":"main"}) [sim=120s, wall=99s]
  → (empty result)
- `tool#26` **eo_pattern_lookup**({"slot":"main","axis":"FB"}) [sim=123s, wall=99s]
  → found=1, best=4m
_(turn 21: 1,422 in / 162 out / 21,897 cached, ~$-0.0524, 3.9s API)_

**Turn 21 narration**:

**FB-axis EO is 4 moves!** `R' F D L'` — this is interesting because FB had 8 bad edges but the EO is only 4 moves. Let me probe DR for this FB-axis option:

- `tool#27` **probe_dr_pattern**({"slot":"main","eo_alg":["R'","F","D","L'"],"axis":"FB"}) [sim=126s, wall=103s]
  → found=1
_(turn 22: 918 in / 222 out / 22,114 cached, ~$-0.0536, 5.7s API)_

**Turn 22 narration**:

**FB-axis**: EO=4, DR total=7 (so 3 moves RZP after EO). This is BETTER than the UD path I tried (which was 8 total to DR). Let me commit to this FB-axis path and check DR trigger options.

- `tool#28` **apply_moves**({"slot":"main","moves":["R'","F","D","L'"]}) [sim=130s, wall=109s]
  → hist=4m
  slot=main hist(4m): `R' F D L'`
- `tool#29` **dr_trigger_options**({"slot":"main","axis":"FB","max_setup":5}) [sim=138s, wall=111s]
  → (empty result)
_(turn 23: 662 in / 84 out / 22,855 cached, ~$-0.0585, 2.5s API)_

**Turn 23 narration**:

No trigger options found. Let me use dr_recognize instead:

- `tool#30` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=141s, wall=113s]
  → found=0
_(turn 24: 626 in / 170 out / 23,618 cached, ~$-0.0593, 4.0s API)_

**Turn 24 narration**:

The DR is 7 moves total from this EO (3 more after these 4 setup moves). Let me apply the setup and continue:

- `tool#31` **apply_moves**({"slot":"main","moves":["B'","D","F'","U'"]}) [sim=145s, wall=117s]
  → hist=8m
  slot=main hist(8m): `R' F D L' B' D F' U'`
- `tool#32` **dr_recognize**({"slot":"main","axis":"FB"}) [sim=148s, wall=117s]
  → found=1
_(turn 25: 565 in / 140 out / 23,830 cached, ~$-0.0605, 3.5s API)_

**Turn 25 narration**:

Good! 3 more moves to DR: `B L2 D'`. Let me apply these:

- `tool#33` **apply_moves**({"slot":"main","moves":["B","L2","D'"]}) [sim=151s, wall=121s]
  → hist=11m
  slot=main hist(11m): `R' F D L' B' D F' U' B L2 D'`
- `tool#34` **quick_check**({"slot":"main"}) [sim=151s, wall=121s]
  → (empty result)
_(turn 26: 760 in / 135 out / 24,208 cached, ~$-0.0611, 4.0s API)_

**Turn 26 narration**:

Perfect! I've reached DR on FB axis in **11 moves**: `R' F D L' B' D F' U' B L2 D'`. This is 1 move better than the UD path (which was 12). Now let me classify the HTR subset:

- `tool#35` **htr_classify**({"slot":"main","axis":"FB"}) [sim=166s, wall=125s]
  → subset=[2, 0, 4, 7, 1, 6, 3, 5]
_(turn 27: 775 in / 219 out / 24,433 cached, ~$-0.0604, 5.0s API)_

**Turn 27 narration**:

**HTR SUBSET**: 4-swap long-cycle with [4, 4] cycle structure:
- HTR reduction: 8 moves
- Finish: 9 moves
- Total post-DR: 17 moves

**PROJECTED TOTAL**: 11 (to DR) + 17 (HTR+finish) = **28 moves**

This is **2 moves better** than the prior 30-move attempts! Let me proceed with the HTR reduction and check for any opportunistic 3-cycle residuals along the way.

- `tool#36` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=167s, wall=130s]
  → (empty result)
_(turn 28: 719 in / 157 out / 24,800 cached, ~$-0.0624, 3.4s API)_

**Turn 28 narration**:

HTR reduction is 8 moves (partial, 4 visible). Let me apply the first 4 and check if there's an opportunistic residual:

- `tool#37` **apply_moves**({"slot":"main","moves":["D2","F2","R2","U2"]}) [sim=171s, wall=133s]
  → hist=14m
  slot=main hist(14m): `R' F D L' B' D F' U' B L2 D F2 R2 U2`
- `tool#38` **quick_check**({"slot":"main"}) [sim=171s, wall=133s]
  → (empty result)
_(turn 29: 739 in / 143 out / 25,219 cached, ~$-0.0637, 4.2s API)_

**Turn 29 narration**:

Good, 1 move saved by auto-cancel (D' + D2 = D). Current count is 14 moves. Not solved yet, not at HTR. Let me continue with the rest of HTR reduction:

- `tool#39` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"htr_reduction"}) [sim=172s, wall=138s]
  → (empty result)
_(turn 30: 629 in / 120 out / 25,698 cached, ~$-0.0657, 2.9s API)_

- `tool#40` **apply_moves**({"slot":"main","moves":["F'","U2","L2","B"]}) [sim=176s, wall=140s]
  → hist=18m
  slot=main hist(18m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B`
- `tool#41` **quick_check**({"slot":"main"}) [sim=176s, wall=140s]
  → (empty result)
_(turn 31: 608 in / 145 out / 25,933 cached, ~$-0.0660, 3.6s API)_

**Turn 31 narration**:

Excellent! I'm now at HTR (is_htr_ud: true) in 18 moves. The HTR reduction was actually 7 moves (11 → 18), not 8. Now let me apply the finish phase:

- `tool#42` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=177s, wall=144s]
  → (empty result)
_(turn 32: 635 in / 121 out / 26,371 cached, ~$-0.0675, 2.7s API)_

- `tool#43` **apply_moves**({"slot":"main","moves":["R2","U2","B2","R2"]}) [sim=181s, wall=147s]
  → hist=22m
  slot=main hist(22m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2`
- `tool#44` **quick_check**({"slot":"main"}) [sim=181s, wall=147s]
  → (empty result)
_(turn 33: 653 in / 111 out / 26,572 cached, ~$-0.0681, 3.0s API)_

**Turn 33 narration**:

Still not solved after 22 moves. Let me continue with the next chunk of the finish:

- `tool#45` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=182s, wall=150s]
  → (empty result)
_(turn 34: 617 in / 121 out / 26,991 cached, ~$-0.0692, 2.8s API)_

- `tool#46` **apply_moves**({"slot":"main","moves":["F2","U2","B2","D2"]}) [sim=186s, wall=153s]
  → hist=26m
  slot=main hist(26m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2`
- `tool#47` **quick_check**({"slot":"main"}) [sim=186s, wall=153s]
  → (empty result)
_(turn 35: 634 in / 106 out / 27,220 cached, ~$-0.0700, 2.6s API)_

**Turn 35 narration**:

26 moves, still not solved. Let me get the final chunk:

- `tool#48` **apply_htr_phase**({"slot":"main","axis":"FB","phase":"finish"}) [sim=187s, wall=155s]
  → (empty result)
_(turn 36: 583 in / 109 out / 27,621 cached, ~$-0.0712, 3.3s API)_

- `tool#49` **apply_moves**({"slot":"main","moves":["F2"]}) [sim=188s, wall=159s]
  → hist=27m
  slot=main hist(27m): `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
- `tool#50` **quick_check**({"slot":"main"}) [sim=188s, wall=159s]
  → SOLVED
_(turn 37: 576 in / 97 out / 27,850 cached, ~$-0.0720, 5.4s API)_

**Turn 37 narration**:

**SOLVED in 27 moves!** This is **3 moves better** than the prior 30-move attempts! Let me compose the final NISS solution and verify it:

- `tool#51` **compose_niss_solution**({"slot":"main"}) [sim=189s, wall=164s]
  → solves=True
_(turn 38: 689 in / 91 out / 28,262 cached, ~$-0.0729, 4.4s API)_

**Turn 38 narration**:

Perfect! The solution is verified. Now, since the solution is ≥27 moves and I have plenty of budget remaining, I should try replace_and_shorten once to see if I can shorten it further. Let me check my budget first:

- `tool#52` **budget_status**({}) [sim=189s, wall=168s]
  → sim=189s
_(turn 39: 554 in / 159 out / 28,435 cached, ~$-0.0727, 4.2s API)_

**Turn 39 narration**:

I have 3411s remaining and plenty of tool calls available. Let me try replace_and_shorten on a substantial tail portion of the solution. I'll target the HTR+finish section (from around move 11 onward):

- `tool#53` **replace_and_shorten**({"slot":"main","start":11,"end":27,"axis":"FB"}) [sim=189s, wall=173s]
  → ERROR: too few tool calls remaining (27) for replace_and_shorten; need ≥30 (the miss path can require 20+ recovery calls). Ship your current solve as FINAL_SOLUTION instead.
_(turn 40: 498 in / 443 out / 28,842 cached, ~$-0.0697, 10.4s API)_

**Turn 40 narration**:

The tool refuses because I need ≥30 tool calls remaining. I have 27 left. That's unfortunate, but I have a valid 27-move solution which is better than the 30-move prior attempts. Let me submit this solution:

**FINAL SOLUTION BREAKDOWN:**
- **EO (FB-axis)**: `R' F D L'` (4 moves) — 8 bad edges on FB solved efficiently
- **DR (FB-axis)**: `B' D F' U' B L2 D'` (7 moves) — RZP setup + single inverse trigger
- **HTR reduction**: `D F2 R2 U2 F' U2 L2 B` (8 moves, with 1 cancel) — corner orbit reduction
- **HTR finish**: `R2 U2 B2 R2 F2 U2 B2 D2 F2` (9 moves) — half-turn solve to completion

**Total: 27 moves** (3 moves better than prior 30-move attempts)

The key improvement came from choosing the FB axis (which had 8 bad edges but a compact 4-move EO pattern) instead of the UD axis. The FB path reached DR in 11 moves (vs 12 for UD) and had a slightly better HTR subset that finished in 16 moves post-DR (vs 19 for UD).

FINAL_SOLUTION: ["R'", "F", "D", "L'", "B'", "D", "F'", "U'", "B", "L2", "D", "F2", "R2", "U2", "F'", "U2", "L2", "B", "R2", "U2", "B2", "R2", "F2", "U2", "B2", "D2", "F2"]


**verify_solved** ✓ — 27 moves: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`
