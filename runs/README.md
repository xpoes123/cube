# runs/ — the LLM-FMC experiment log

This directory is the project's deliverable: every transcript, every
narrative, every comparison. The video plays from these files.

## Where to start

- **[MORNING_REPORT.md](MORNING_REPORT.md)** — overnight progress
  summary. Read this first.
- **[VIDEO_SCRIPT.md](VIDEO_SCRIPT.md)** — 10–15 min video outline,
  3-act structure with the through-lines.
- **[INDEX.md](INDEX.md)** — auto-generated dashboard of every
  transcript (~40 runs). Sortable by directory.
- **[STATUS.md](STATUS.md)** — high-level project status (older,
  but the foundational table is still good).

## The corpus evals

Each version had a specific change. Each has a `SUMMARY.md` and per-
scramble narrative markdown.

| Dir | Change | Solved | Notes |
|---|---|---:|---|
| `corpus_eval/` | v1: initial sim, ship rule absent | 1/4 | scramble 2 only |
| `corpus_eval_v2/` | + HTR-prompt fix | 1/4 | same — HTR wasn't the bottleneck |
| `corpus_eval_v3_theory/` | + FMC theory in prompt | **0/4** | perfectionism timeout |
| `corpus_eval_v4_ship/` | + SHIP RULE | 1/4 | scramble 2 restored at 33m |
| `corpus_eval_v5_algoEO/` | + algorithmic EO + slot exposure | TBD | (running) |
| `corpus_eval_v6_full/` | + mirror-aug policy + 10 scrambles | TBD | (running) |

## The decisive single-scramble runs

- **[example_solve_scramble2.md](example_solve_scramble2.md)** — the
  unconstrained loop solving scramble 2 in 25 moves, $0.23.
- **[sim_design.md](sim_design.md)** — the realistic-FMC design doc.
- **[sim_scramble2_first.md](sim_scramble2_first.md)** — first sim run
  on scramble 2 (failed at v0 budgets).
- **[sim_scramble2_solved.md](sim_scramble2_solved.md)** — the
  successful 33-move sim solve (post-fixes).
- **[sim_scramble2_v7_narrative.md](sim_scramble2_v7_narrative.md)** —
  the cleanest sim narrative (with human-like time costs).
- **[reasoning_compare_sonnet_vs_opus.md](reasoning_compare_sonnet_vs_opus.md)**
  — model-style comparison (older, from the unconstrained mode).

## Tools to know

```bash
# Re-render any transcript:
uv run python -m cube.agent.render_narrative <path.json>

# Compare two runs side by side:
uv run python -m cube.agent.compare_runs <left.json> <right.json>

# Regenerate INDEX.md after new runs:
uv run python -m cube.agent.build_index

# Run a fresh sim:
uv run python -m cube.agent.simulated_fmc "<scramble>" --verbose

# Run the corpus eval (4 default + N extra random):
uv run python -m cube.agent.corpus_eval --extra-random 6
```

## Cost / budget tracker

| Phase | Cost (rough) |
|---|---:|
| Initial development + iterations 1-7 | $11 |
| Corpus eval v1-v4 | $13 |
| Mirror-aug retrain (no API) | $0 |
| Corpus eval v5 + v6 + Opus | ~$25 |
| **Total session** | **~$50** |
| **Budget** | **$100** |

## Key files outside this dir

```
src/cube/
├── agent/
│   ├── simulated_fmc.py     <- the agent loop with 18 tools
│   ├── loop.py              <- unconstrained version (comparison baseline)
│   ├── corpus_eval.py       <- batch driver
│   ├── render_narrative.py  <- transcript -> readable markdown
│   ├── compare_runs.py      <- side-by-side run comparison
│   ├── build_index.py       <- runs/INDEX.md generator
│   ├── scramble_gen.py      <- WCA-style scramble generator
│   └── prewarm_subsets.py   <- offline subset finish builder
├── tools/
│   ├── state.py             <- inspect_state (with bad-edge slots)
│   ├── search.py            <- lookahead / find_dr_via_trigger
│   ├── policy.py            <- 91k-param transformer interface
│   ├── library.py           <- htr_subset, commutators
│   ├── algebra.py           <- cancel, NISS, invert
│   └── eo_bfs.py            <- algorithmic EO finder (no policy)
└── training/                <- 91k-param transformer training pipeline
                                 (mirror-aug retrain landed)

checkpoints/
├── policy_best.pt              <- mirror-aug policy
├── policy_best_pre_mirror.pt   <- backup
└── subset_finish_cache.pkl     <- pickled HTR subset finishes
```
