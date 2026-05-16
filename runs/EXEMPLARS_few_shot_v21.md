# Few-Shot Exemplars v21 — Elite FMC Reasoning Patterns

Three condensed narration exemplars distilled from elite WCA-FMC solver transcripts,
embedded to prime the agent's compare-before-commit / branch-journal / NISS-scout
behaviors. Each narrates ~one minute of expert thinking. Use the same voice when
solving: tool calls + terse rationale + explicit rejection of inferior branches.

---

## EXEMPLAR A — Multi-side EO scouting before committing
*(adapted from Levi Gibson's WR-16 walkthrough, S1xLyAFxPLE)*

> Scramble loaded. I'll scout EO on both directions before locking one in.
>
> `eo_pattern_lookup(axis=FB, side=normal)` → 4 bad edges, cheapest reduction is 3 moves (`l2 U' F'`).
> Switch with NISS: `eo_pattern_lookup(axis=FB, side=inverse)` → I have a D-move that flips two bad edges and, after NISS-tracing, the remaining 4 bad edges all land on the D-face. That means `D / NISS / D'` solves EO in **2 moves** instead of 3.
>
> Picking the inverse branch. Cost saved: 1 move, but more importantly the post-EO substate has 7 bad corners → too many for direct DR. Spend one move on RZP: `F` drops me to 4 bad corners (matches the DR-trigger precondition).
>
> Note: I did NOT take the EO line that gave a free pseudo-slot. Blocks during EO are a trap — they constrain DR axis choice. Keep EO clean, let DR do the structural work.

---

## EXEMPLAR B — Picking the longer DR for a cleaner substate
*(adapted from Alexandros Vakanas's 25-move solve and Tommy Kipriallis's 20-move solve, yod7OCvJPI8)*

> Post-EO. `dr_trigger_options(axis=UD)` returns three candidates.
>
> - **A**: DR in 9 moves, substate is 4c4e with two unmatched corners on opposite faces. HTR estimate from this state: 7-9 moves. Total projection ~25.
> - **B**: DR in 13 moves, substate is `4c2e` (the "DR minus 2e4c" sub-case), already only 3 moves from HTR via the `D' F2 D` trigger. HTR cost: 3. Total projection ~22.
> - **C**: DR in 11 moves with a generic substate, HTR cost ~6. Total projection ~22 but the finish leaves a 2e2e — needs an insertion.
>
> Taking **B** despite being 4 moves longer than A. The substate is blocky: one full bar already sits on the R face, and `apply_htr_phase` confirms zero setup moves needed. Length of DR is a red herring — what matters is `dr_moves + htr_moves + finish_moves`, and B wins net.
>
> Rule of thumb I'm internalizing: a `4c2e` DR substate is worth ~3 moves of "credit" against any longer-DR comparison.

---

## EXEMPLAR C — Branch journal with explicit rejection rationale
*(adapted from the 23-move FMC PB reconstruction, CEfB4NG0MLI, and Marcin Chmielewski's corpus comments)*

> Logging branches as I scout. EO done in 3 (`l2 U' F'` on inverse, FB axis).
>
> **Branch 1 — UD axis DR:** `dr_trigger_options` finds a 4-move setup (`d L'`) to RZP, then `r U2 R` gives DR in 11 total. Substate: 1 quarter-turn corner, decent. HTR estimate via `apply_htr_phase`: 5 moves. Finish: leaves 2e2e (1-move insertion). Projected total: **20-21**. Bookmarking this.
>
> **Branch 2 — RL axis DR (scouted from same EO):** holding Branch 1 aside, I re-examine the post-EO cube on the RL axis. `dr_trigger_options(axis=RL)` returns nothing under 7 moves — corner orientation is wrong-parity for this axis. **Reject:** 7+ move DR with a bad substate dominates Branch 1.
>
> **Branch 3 — FB axis DR:** would require redoing EO. **Reject** without scouting; cost of re-EO not recoverable.
>
> Committing to Branch 1. Finishing the skeleton, then `replace_and_shorten` on the 2e2e to cancel the trailing D2 / leading B2 — found a 6-5 insertion saving 1 move. Final: 23.
>
> Lesson worth re-encoding: when a branch is rejected, write *why* (parity, length, substate quality), not just that it lost. Future me re-scouting this scramble shouldn't re-try Branch 2.
