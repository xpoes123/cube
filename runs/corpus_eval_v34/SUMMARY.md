# Corpus eval — `v34`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-20T02:16:47
- **Scrambles**: 2

## What changed in this version

v34: killed the DR oracle (no expected_total_to_solved/jzp_eligible/top_pairs_on_inverse fields), every tool result includes a _meta block with sim/wall time remaining + urgency tier, and n_best=8 attempts now SHARE a single 3600s WCA budget per scramble (prior versions gave each attempt a fresh 3600s, i.e. 8x the realistic budget). This is the first WCA-realistic methodology run.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 30 | 20 | 10 | Marcin Chmielewski | 35 | 382s | 160s | $0.19 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 34 | 20 | 14 | Marcin Chmielewski | 58 | 1540s | 249s | $0.27 |

**Solved**: 2/2
**Avg sim moves (solved)**: 32.0
**Avg human (WCA) (solved)**: 20.0
**Avg gap (solved)**: +12.0
**Total API cost (rough, no cache discount)**: $0.47

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt4_20260520_015818.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__attempt1_20260520_020549.md)
