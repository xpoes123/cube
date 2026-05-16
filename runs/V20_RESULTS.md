# v20 — Opus 4.7 model A/B + prewarm-cache delivered

Two completions:
1. claude-opus-4-7 corpus eval (was crashing on Opus thinking API; fixed)
2. subset_finish_cache pre-warm completed (170 UD + 3 FB + 3 RL entries)

## Opus 4.7 vs Sonnet 4.5 (5-WCA-corpus)

| Iter | Model | Solved | Avg | Cost |
|------|-------|--------|-----|------|
| v18 | Sonnet 4.5 | 5/5 | 29.4 | $0.80 |
| v19 (n_best=2) | Sonnet 4.5 | 5/5 | 29.4 | $0.81 |
| **v20 (Opus 4.7)** | Opus 4.7 | **5/5** | **29.2** | **$0.65** |

### Per-scramble Sonnet vs Opus

| ID | v19 Sonnet | v20 Opus | Δ |
|----|---:|---:|---:|
| PSSS_s1 | 30 | 28 | **−2** |
| PSSS_s2 | 26 | 29 | +3 |
| PSSS_s3 | 30 | 30 | 0 |
| BackiPetrovac | 31 | 31 | 0 |
| WesternSicily | 30 | 28 | **−2** |

### Honest finding

Opus delivered a marginal -0.2 move average AND a -19% cost reduction
(fewer tokens to reach the same conclusion). Per-scramble it's a
3-2-0 trade: 2 wins (PSSS_s1, WesternSicily), 1 loss (PSSS_s2), 2 ties.

This is NOT a "5x cost for 1-2 move lift" win — it's "0.8x cost for
the same average with different per-scramble variance." Model swap
alone isn't the path to sub-25.

## Subset cache pre-warm

Built via `cube.agent.prewarm_subsets --axes UD FB RL --limit 420`,
56-min wall time. Cache: `checkpoints/subset_finish_cache.pkl` now
~20 KB with 176 entries (vs 1.3 KB / 13 entries previously).

Coverage breakdown:
- UD: 170 entries (the dominant axis humans use)
- FB: 3 entries
- RL: 3 entries

Finish lengths: avg 18.3 moves (these are DR→SOLVED, not HTR-only).
Future solves benefit by skipping the ~15s "first exposure" cost when
they hit a cached subset.

## End of overnight iteration session

| Iter | Solved | Avg | Gap | Notes |
|------|--------|-----|------|-------|
| v13  | 4/5    | 28.2 | +7.7 | BackiPetrovac DNF |
| v14a | 5/5    | 29.4 | +8.9 | r&s gated, 5/5 reliability |
| v14b | 4/5    | 28.5 | +8.0 | branch-journal thrash → DNF |
| v15  | (stacked into v16) | — | — | dr_trigger_options all 3 axes |
| **v16**  | **5/5**    | **28.2** | **+7.4** | **niss_scout, best ever** |
| v17  | 5/5    | 28.6 | +7.8 | compose_niss + quick_check |
| v18  | 5/5    | 29.4 | +8.6 | rs_recommend |
| v19  | 5/5    | 29.4 | +8.6 | best-of-2 (variance probe) |
| v20  | 5/5    | 29.2 | +8.4 | Opus 4.7 |

**Best result**: v16 at 28.2 avg with 5/5 reliability. v17-v20 added
robustness (compose_niss, quick_check, rs_recommend, prewarm cache,
n_best wrapper, Opus support) but didn't move the move-count floor.

## Where the gap to elite (20.8) goes

The +7.4 to +8.6 gap is roughly:
- ~5-6 moves: better DR/HTR quality (NISS-quality judgment, JZP
  exploitation, axis selection refinement)
- ~1-2 moves: opportunistic insertions when residual cooperates
- The corpus-research finding [[feedback-clean-dr-htr-dominant]] holds:
  this is a DR-quality gap, not an insertion gap.

## What's left for future sessions

- **dr_rescout** (deferred from v18 deliberation): now possible since
  the subset cache is warm. Should refine the EO-time DR ranking.
- **More named DR triggers** (Hitchhiker DR §triggers): extend the
  10-trigger catalog to 20+. Stronger named-recall on rare cases.
- **Retire dr_pattern_lib runtime**: clean up after dr_rescout
  proves the named-trigger flow is sufficient.
- **nissy-oracle policy retraining**: multi-day offline job; would
  improve the transformer policy that underpins lookahead.
- **N-best with N≥4**: chase the lucky run for video-shoot solves.
