# Simulated FMC — scramble 2, first run (FAILED)

Sonnet 4.5 on the same scramble that the unconstrained agent solved in
25 moves (see [`example_solve_scramble2.md`](example_solve_scramble2.md)).

**Result**: didn't finish. 0 moves submitted. 60 tool calls. 418s of
3600s simulated budget spent. 179s real wall. ~565k input tokens, 5.7k
output tokens — roughly $1.50–2 at Sonnet prices.

This is the negative result the video needs. Same model, same scramble,
same pipeline shape — what changed was the **search budgets** and the
**HTR finish substitution**. Move-count-wise the LLM doesn't know more
or less than it did before; under realistic constraints, it just can't
get past EO.

---

## What happened

```
tool#1  inspect_state                       → UD: 2 bad edges (cheapest)
tool#2  lookahead(eo, axis=UD, w=5 d=4)     → no EO found
tool#3  lookahead(eo, axis=FB, w=5 d=4)     → "U' R" (2 moves, FB)
tool#4  apply_moves(["U'", "R"])            → EO solved on FB
tool#5  find_dr_via_trigger(axis=FB)        → NO DR found ✗
        (sim budget: setup_width=20, setup_depth=6)
tool#6  niss_flip                            → switch to inverse
tool#7  inspect_state                        → all axes have many bad edges on inverse
tool#8-15  scan inverse for EO/DR             → nothing within budget
tool#16 reset_slot                           → back to scramble
tool#17-46 every combination of axis × EO × DR-trigger    → nothing
tool#47-60  manual move-by-move exploration   → drifting, hit undo limit confusion
```

Agent halt: `max_tool_calls` (60). It would have kept thrashing.

---

## Why it failed: the `find_dr_via_trigger` budget

The unconstrained version uses `setup_width=512`. The sim version uses
`setup_width=20`. On scramble 2 after `U' R` (EO on FB solved), DR is
roughly 7 moves away. The 91k-param policy isn't strong enough at
width=20 to find a trigger state inside that depth — the unconstrained
analyzer needed width=8192 originally; we compromised at 512 for
"closer to human"; 20 is too aggressive.

What this tells us about the original "fair vs cheating" framing
(see `project_cube_engine.md`'s CURRENT DIRECTION): **`find_dr_via_trigger`
at width=512 wasn't just "wider than a human" — width=512 is doing
the heavy lifting that makes the agent look competent at all.** When
we drop to width=20 to actually match human enumeration, the agent
cannot bridge EO → DR on this scramble.

This is the most important finding so far. Two ways to read it:

1. **The policy is the bottleneck.** A stronger policy (LR-mirror
   augmentation, random-scramble pretraining, value head, more data)
   might let width=20 work. That would mean we ARE testing "can the
   LLM do FMC" — and the current LLM-on-91k-policy combo can't, yet.

2. **The LLM's search-orchestration strategy is wrong.** A human at
   this point would not give up on DR after one failed trigger search.
   They'd build a longer EO setup, try cancellation, plan a 3-stage
   bridge. The agent does try this (tool#47-60) but with no structure —
   it's running policy_intuition and committing one move at a time,
   then asking lookahead for DR each time.

Probably both.

---

## What worked

- The slot/undo/budget mechanics held up cleanly. No crashes, no
  invalid states. Sonnet correctly used `reset_slot` to back out of
  bad commitments, and called `budget_status` only when relevant.
- 418s of 3600s sim budget spent on 60 tool calls — even with all
  this thrashing, the agent had budget for another ~5 hours of
  competition time. The binding constraint is the API/tool-call
  budget, not the simulated time.
- Sonnet narrated its hypotheses honestly ("OK, this scramble is
  definitely hard. The lookahead depth of 4 isn't finding anything.").
  Great video material.

## What didn't work

- One bug surfaced: at tool#58 the agent said "Wait, I've reached the
  undo limit (5 > 4)." The undo limit is on undo_moves, NOT
  apply_moves — there is no apply-cap. The system prompt should be
  clearer that you can apply as many moves as you want but only
  unwind 4 at a time.

- The agent didn't try `try_alg` for multi-move setup chains until
  very late. The system prompt should highlight try_alg as the
  cheap probe (2s simulated) when lookahead's budget runs out.

- Sonnet never reached `lookup_subset_finish` — never got to DR.
  We couldn't test the memoization story on this run at all.

---

## Next iterations

1. **Bump `find_dr_via_trigger` budget a little** — try sw=64, sd=8.
   Test on this same scramble. If 64 finds DR, the "human-scale" knob
   sits somewhere between 20 and 512; pick the smallest value that
   still solves and document why.

2. **Improve the prompt** to address the two confusions above
   (apply vs undo limit, when to use try_alg over lookahead).

3. **Pre-warm `_SUBSET_FINISH_CACHE`** — run a sweep that solves
   scramble 2 in the unconstrained mode 20 times to populate the
   cache, then re-run sim mode. The agent's first DR will hit a
   cached subset → 1s recall instead of 15s learn. This simulates
   "a human champion who's seen this subset before."

4. **Better failure-mode visibility for the video**: log the
   `budget_events` trace to a tiny ASCII timeline so we can show
   where the 418s went.

---

## Stats

| Metric | Unconstrained (working) | Simulated (failed) |
|---|---:|---:|
| Result | 25-move solve | no solve |
| Tool calls | 14 | 60 |
| Real wall | 5 min | 3 min |
| Sim budget spent | n/a | 418 / 3600s |
| Estimated cost | $0.23 | ~$1.80 |
| Search budget (DR) | sw=512 sd=8 | sw=20 sd=6 |
| HTR finish | A* + 663,552-PDB | (never reached) |

The cost went up 8× and the result went from solved to unsolved.
That's the wedge.
