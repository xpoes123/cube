# Corpus eval — `v33`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-18T00:41:09
- **Scrambles**: 3

## What changed in this version

v33: small 3,657-entry DR memory (JSON, depth-4 patterns) + brain fallback in dr_recognize. Replaces v32's no-DR-memory regression with the human-scale alternative: recognize the pattern by sight if familiar, use trained-policy intuition for unfamiliar cases (apply ONE suggested move, re-query).

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 29 | 20 | 9 | Marcin Chmielewski | 47 | 1344s | 201s | $0.15 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 26 | 20 | 6 | Marcin Chmielewski | 52 | 1674s | 195s | $0.24 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 30 | 23 | 7 | Marcin Chmielewski | 70 | 1234s | 207s | $0.29 |

**Solved**: 3/3
**Avg sim moves (solved)**: 28.3
**Avg human (WCA) (solved)**: 21.0
**Avg gap (solved)**: +7.3
**Total API cost (rough, no cache discount)**: $0.68

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt1_20260517_231551.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__attempt3_20260517_235242.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3__attempt4_20260518_002437.md)
