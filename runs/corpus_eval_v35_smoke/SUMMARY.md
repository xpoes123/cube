# Corpus eval — `v35_smoke`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-20T03:11:36
- **Scrambles**: 1

## What changed in this version

v35 SMOKE TEST: 1 scramble (PSSS_s1), n_best=3 sharing 3600s budget. Validates dr_progress_options, bookmark_fork/restore_fork/list_bookmarks, and the richer cross-attempt handoff (prior_bookmarks + prior_narrative_excerpts).

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 36 | 20 | 16 | Marcin Chmielewski | 40 | 145s | 209s | $0.33 |

**Solved**: 1/1
**Avg sim moves (solved)**: 36.0
**Avg human (WCA) (solved)**: 20.0
**Avg gap (solved)**: +16.0
**Total API cost (rough, no cache discount)**: $0.33

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt2_20260520_030321.md)
