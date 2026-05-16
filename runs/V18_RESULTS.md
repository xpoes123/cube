# v18 — tool-side r&s recommendation (mixed result)

Surgical fix for v17 BackiPetrovac regression: compose_niss_solution
returns rs_recommend={reason, suggested_start, suggested_end} when the
solve passes the r&s gates. Agent reads it at decision time.

## Results

| Iter | Solved | Avg | Gap | Cost |
|------|--------|-----|------|------|
| v16  | 5/5    | **28.2** | **+7.4** | $1.09 |
| v17  | 5/5    | 28.6 | +7.8 | $0.90 |
| v18  | 5/5    | 29.4 | +8.6 | $0.80 |

### Per-scramble

| ID | v16 | v17 | v18 |
|----|---:|---:|---:|
| PSSS_s1 | 25 | 26 | 30 |
| PSSS_s2 | 26 | 26 | 26 |
| PSSS_s3 | 30 | 30 | 30 |
| BackiPetrovac | 29 | 31 | 31 |
| WesternSicily | 31 | 30 | 30 |

## Honest assessment

**v18's mechanism worked but didn't deliver.** PSSS_s1 v18: agent saw
the rs_recommend, called replace_and_shorten on span [4:30]. But the
substitute was the same length (26 moves, delta=0). So r&s fired
correctly — the underlying solve just happened to not have a lumpy
sub-span to shorten.

This is **agent run-to-run variance**, not a v18 bug. Looking across
v13-v18, per-scramble min/max shows 3-5 move variance per scramble.
With 5 scrambles, the corpus average naturally swings ±1-2 moves
between iterations.

### Implication

v16 (28.2) was the best run — possibly lucky. v17/v18 added real
capabilities (compose_niss_solution, quick_check, rs_recommend) that
should make the agent MORE robust, but the prompt-engineering
iteration loop is capped by run-to-run variance.

To move below 28 reliably we need either:
- A more powerful model (Opus 4.7) — actual reasoning lift
- A richer knowledge base the agent can recall (more named triggers,
  pre-warmed HTR finishes — Task #68, currently being built)
- N-best solving: run each scramble 3× and pick the shortest

## v19 plan

Pre-warm the HTR-finish cache to 96+ entries (currently 13). This was
already running as a background build during the v18 eval.
Expected delta: small (the cache miss penalty is ~14s, not ~3 moves),
but unlocks dr_rescout (Plan agent's v18 recommendation, deferred).

## Lessons logged for memory

- Prompt tweaks within the current model + tool surface have ~1-2 move
  variance ceiling per iteration.
- v16's niss_scout + all-3-axes triggers were the LAST real move-count
  win. Everything since has been infrastructure that *should* compound
  later but doesn't show up in 5-scramble averages.
