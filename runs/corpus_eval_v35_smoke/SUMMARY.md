# Corpus eval — `v35_smoke`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-20T03:30:29
- **Scrambles**: 1

## What changed in this version

v35 smoke test (2nd pass): tool-call wall 80→150, brain_suggest discouraged for DR navigation, dr_progress_options is the canonical DR tool.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 24 | 20 | 4 | Marcin Chmielewski | 117 | 557s | 505s | $0.68 |

**Solved**: 1/1
**Avg sim moves (solved)**: 24.0
**Avg human (WCA) (solved)**: 20.0
**Avg gap (solved)**: +4.0
**Total API cost (rough, no cache discount)**: $0.68

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt1_20260520_031147.md)
