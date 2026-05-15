# Sonnet 4.5 vs Opus 4.5 — reasoning side-by-side

Both runs on scramble 2 (`R' U' F B' U2 F' U2 R2 B' R2 B' R2 U2 R2 F' L U2 B D R F L2 F D' R' U' F`).
Extended thinking enabled (3000-token budget). Both timed out before solving — too few tool calls within the 20-min wall.

The `[thinking]` block fires once at the start (Anthropic's API uses it for planning, not per-step). The reasoning between tool calls lives in `[claude]` text blocks — these are what the agent narrates as it goes.

---

## Sonnet 4.5 — depth-first style

> **[thinking]** Alright, let me solve this scramble step by step following the FMC approach.

```
tool#1  inspect_state
        → UD: 2 bad edges (best)

  "I'll solve this scramble using the standard FMC pipeline: EO → DR → HTR → Finish.
   Let me start by inspecting the scramble state."
```

```
tool#2  lookahead(target=eo, axis=UD)
        → R B D' B (4 moves)

  "Good! UD axis has only 2 bad edges - this is the best starting point for EO.
   Let me search for EO on the UD axis."
```

```
tool#3  inspect_state(history=[R, B, D', B])
        → eo_solved=[UD]

  "Great! I found EO in just 3 moves with 'B D' B'. Let me verify and move on to DR."
  (Note: it miscounted — really 4 moves.)
```

```
tool#4-5  find_dr_via_trigger(axis=UD)
          → no DR found (default width)

  "Perfect! EO is solved on UD axis. Now let me use find_dr_via_trigger to reach DR."
  "No DR found with those parameters. Let me try increasing the setup depth."
```

```
tool#6  niss_flip
        → switched to inverse scramble

  "Still no DR. Let me try NISS - switching to the inverse scramble."
```

```
tool#7  inspect_state(on inverse)
        → same counts (frame-symmetric)

  "Good! Now I'm on the inverse side. Let me check the state and search for EO from here."
```

```
tool#8  lookahead(eo, FB) ← back on normal
        → U' R (2 moves)

  "Same state (as expected, since inverse is symmetric). Let me try a different
   approach. Let me go back to normal side and try the other 3-move EO option or
   try FB/RL axes."
  "Excellent! FB axis has a 2-move EO: 'U' R'. Let me try this:"
```

```
tool#9  inspect_state(history=[U', R])
        → eo_solved=[FB]

  "Perfect! EO on FB in just 2 moves. Now let me search for DR:"
```

```
tool#10-12 find_dr_via_trigger(axis=FB) at varying params
           → no DR found

  "Let me try with tail_length=3:"   (then timed out)
```

**Sonnet's pattern**: pick one axis, drill it to failure, then backtrack. Narrates short judgments ("best starting point", "perfect", "good").

---

## Opus 4.5 — breadth-first style

> **[thinking]** Let me solve this FMC scramble step by step. I'll start by looking for EO on all three axes to find the shortest EO solution.

```
tool#1  inspect_state
        → UD: 2 bad edges

  "I'll solve this FMC scramble step by step. Let me start by inspecting the state
   and finding EO."
```

```
tool#2-4  lookahead(eo, axis=UD), (eo, FB), (eo, RL)  ← all three at once
          → UD: R B D' B (4)
          → FB: U' R (2)  ← shortest
          → RL: nothing

  "Excellent! FB axis has a 2-move EO: `U' R`. Let me use that and find DR."
```

```
tool#5-6  inspect after [U', R]; find_dr_via_trigger(axis=FB)
          → no DR found

  "No DR found from this EO. Let me try the UD axis EO and also try NISS."
```

```
tool#7-8  inspect after [R, B, D', B]; find_dr_via_trigger(axis=UD)
          → no DR found at default width

  (no narration — went straight to NISS)
```

```
tool#9   niss_flip
         → inverse scramble

  "Let me search for EO on the inverse scramble:"
```

```
tool#10-12  lookahead(eo, UD/FB/RL) ← all three axes on inverse
            → UD: F' D' F (3)

  "Good, on inverse we have a 3-move EO (UD): F' D' F. Let me try DR from there:"
```

```
tool#13-14  find_dr_via_trigger(axis=UD, inverse) — no luck

  "Let me try with longer tail and also try other approaches. Let me try both
   EOs with tail_length 3:"   (then timed out)
```

**Opus's pattern**: scan all three axes per side, ranked by short-EO availability, then drill the winners systematically. Sparser narration but more methodical scaffolding — it enumerates before committing.

---

## Headline differences

| | Sonnet 4.5 | Opus 4.5 |
|---|---|---|
| Initial thinking | brief, single sentence | brief, names the strategy |
| Per-decision narration | chatty, with judgment | terse, more analytical |
| Search order | depth-first (one axis to failure, then backtrack) | breadth-first (all axes, rank, then commit) |
| Reaction to no-DR | "let me try other params" | "let me try the other axes / NISS" |
| Tool calls in 20 min | 12 | 14 |
| Final result | timeout | timeout |

Neither solved scramble 2 in this run because `find_dr_via_trigger` default width was 30 (since fixed to 512). The successful Sonnet run earlier ([`runs/example_solve_scramble2.md`](example_solve_scramble2.md)) had wider width and finished in 14 tool calls / $0.23.

---

## Takeaways for the realistic-FMC pivot

- **Both models reason in `[claude]` text blocks, not `[thinking]`.** Extended thinking is for hidden chain-of-thought; for the video, the visible narration is what matters.
- **Sonnet commits faster.** It picks a line and runs with it; if it fails it backtracks. Good for a tight time budget.
- **Opus enumerates more.** It collects information before committing. Better for ambiguous scrambles where the wrong commitment wastes time.
- **Neither shows "uncertainty" about its choice** — the narration is confident even when wrong. For the simulated-FMC version (1hr budget, limited cube slots, undo limits) we'll see whether time pressure changes that.
