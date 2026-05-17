# Corpus eval — `v31`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-17T15:41:13
- **Scrambles**: 3

## What changed in this version

DR search now BFS depth-5 with 0.003 s/state cost penalty (no hard state cap; saturated ~300s sim). 10 TPS move cost (was 1.0/move). Tighter cost model overall. Brain v4 active.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 28 | 20 | 8 | Marcin Chmielewski | 36 | 374s | 138s | $0.17 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 26 | 20 | 6 | Marcin Chmielewski | 47 | 424s | 151s | $0.20 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 27 | 23 | 4 | Marcin Chmielewski | 37 | 343s | 124s | $0.13 |

**Solved**: 3/3
**Avg sim moves (solved)**: 27.0
**Avg human (WCA) (solved)**: 21.0
**Avg gap (solved)**: +6.0
**Total API cost (rough, no cache discount)**: $0.50

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt2_20260517_142449.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__attempt5_20260517_150415.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3__attempt1_20260517_151730.md)
