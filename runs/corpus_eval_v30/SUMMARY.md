# Corpus eval — `v30`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-17T10:39:22
- **Scrambles**: 3

## What changed in this version

Same code as v29; only brain checkpoints replaced (v4: 100K corpus, DR 66→68%, Finish 89→93%). Tests whether brain accuracy improvements translate to move-count reductions.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 25 | 20 | 5 | Marcin Chmielewski | 51 | 243s | 228s | $0.18 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 29 | 20 | 9 | Marcin Chmielewski | 44 | 203s | 174s | $0.15 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 27 | 23 | 4 | Marcin Chmielewski | 53 | 189s | 183s | $0.19 |

**Solved**: 3/3
**Avg sim moves (solved)**: 27.0
**Avg human (WCA) (solved)**: 21.0
**Avg gap (solved)**: +6.0
**Total API cost (rough, no cache discount)**: $0.52

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt1_20260517_091947.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__attempt2_20260517_095459.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3__attempt4_20260517_102502.md)
