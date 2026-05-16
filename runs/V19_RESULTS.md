# v19 — N-best solving (variance probe)

Added `--n-best N` to corpus_eval: run each scramble N times sequentially,
keep the shortest solve. Cost scales linearly. Per
[[feedback-corpus-variance-ceiling]], single-run averages have ~1-2 move
swing due to LLM nondeterminism; N-best is a deterministic floor.

## Results (n_best=2)

| Iter | Solved | Avg | Gap | Notes |
|------|--------|-----|------|------|
| v16  | 5/5    | 28.2 | +7.4 | best ever (single-run, possibly lucky) |
| v17  | 5/5    | 28.6 | +7.8 | compose_niss + quick_check |
| v18  | 5/5    | 29.4 | +8.6 | rs_recommend |
| v19  | 5/5    | **29.4** | +8.6 | best-of-2 |

### Per-scramble (v19 best-of-2)

| ID | v16 single | v19 best-of-2 | v19 att1 | v19 att2 |
|----|---:|---:|---:|---:|
| PSSS_s1 | 25 | 30 | 30 | 30 |
| PSSS_s2 | 26 | 26 | 26 | 26 |
| PSSS_s3 | 30 | 30 | 30 | 30 |
| BackiPetrovac | 29 | 31 | 31 | 31 |
| WesternSicily | 31 | 30 | (best) | (best) |

## Honest finding

**N-best with N=2 didn't move the average.** Both attempts on
every scramble converged to nearly identical move counts. This means
the LLM with Sonnet 4.5 + current toolkit is more deterministic at
this temperature than expected — variance between v16/v17/v18 was
likely caused by prompt-flow differences (compose_niss-then-submit
vs r&s-then-submit), not raw LLM stochasticity.

**v16's 28.2 was indeed a lucky single-run.** PSSS_s1 at 25 there
was an outlier; the modal answer with the current prompt is 30.

## Path-to-sub-25 implications

To move below the 29-move floor in this setup, we'd need:
1. **Opus model swap** — different reasoning altogether, not just
   more samples.
2. **Larger N (N=4 or N=8)** — chase the lucky run. ~$4-8 for one
   eval.
3. **Knowledge enrichment** — pre-warmed HTR finishes (Task #68,
   currently building), more named DR triggers.
4. **Different prompt structure** that pushes a different solve
   path (less obvious how to design).

## Status of overnight tasks

- **Prewarm subset cache (Task #68)**: still running at ~50 min CPU.
  420 subsets × 3 axes is more compute than the Plan agent estimated.
  May not finish overnight.
- **N-best wrapper**: shipped; available for future use.
