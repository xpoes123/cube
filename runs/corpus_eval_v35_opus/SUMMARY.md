# Corpus eval — `v35_opus`

- **Model**: `claude-opus-4-7`
- **Run**: 2026-05-21T01:32:44
- **Scrambles**: 3

## What changed in this version

v35 full corpus (Opus 4.7). dr_progress_options + bookmark_fork/restore_fork + cross-attempt narrative handoff. Inverse-of-scramble harness rejection in place. n_best=3 sharing 3600s budget per scramble. All 5 scrambles run in parallel.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 31 | 20 | 11 | Marcin Chmielewski | 31 | 175s | 192s | $0.28 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 33 | 20 | 13 | Marcin Chmielewski | 40 | 130s | 214s | $0.33 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 33 | 23 | 10 | Marcin Chmielewski | 23 | 49s | 91s | $0.13 |

**Solved**: 3/3
**Avg sim moves (solved)**: 32.3
**Avg human (WCA) (solved)**: 21.0
**Avg gap (solved)**: +11.3
**Total API cost (rough, no cache discount)**: $0.74

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt3_20260521_012653.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__attempt2_20260521_012423.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3__attempt2_20260521_012425.md)
