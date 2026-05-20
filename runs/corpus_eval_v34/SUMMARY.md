# Corpus eval — `v34`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-20T02:05:49
- **Scrambles**: 1

## What changed in this version

v34: killed the DR oracle (no expected_total_to_solved/jzp_eligible/top_pairs_on_inverse fields), every tool result includes a _meta block with sim/wall time remaining + urgency tier, and n_best=8 attempts now SHARE a single 3600s WCA budget per scramble (prior versions gave each attempt a fresh 3600s, i.e. 8x the realistic budget). This is the first WCA-realistic methodology run.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 30 | 20 | 10 | Marcin Chmielewski | 35 | 382s | 160s | $0.19 |

**Solved**: 1/1
**Avg sim moves (solved)**: 30.0
**Avg human (WCA) (solved)**: 20.0
**Avg gap (solved)**: +10.0
**Total API cost (rough, no cache discount)**: $0.19

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt4_20260520_015818.md)
