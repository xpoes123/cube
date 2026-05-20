# Corpus eval — `v35_smoke_opus`

- **Model**: `claude-opus-4-7`
- **Run**: 2026-05-20T04:05:31
- **Scrambles**: 1

## What changed in this version

v35 smoke (Opus 4.7) — same setup as Sonnet smoke v2 but with Opus as the solver. Inverse-of-scramble harness rejection is in place. Tests whether the DR-wall failure is a model-capability issue or an architecture issue.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 31 | 20 | 11 | Marcin Chmielewski | 52 | 215s | 334s | $0.45 |

**Solved**: 1/1
**Avg sim moves (solved)**: 31.0
**Avg human (WCA) (solved)**: 20.0
**Avg gap (solved)**: +11.0
**Total API cost (rough, no cache discount)**: $0.45

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt1_20260520_034832.md)
