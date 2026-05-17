# Corpus eval — `v32`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-17T17:27:39
- **Scrambles**: 3

## What changed in this version

v32: removed dr_pattern_library.pkl (3.2M entries) and the dr_recognize/probe_dr_pattern tools that read it. Agent's only DR tool is now dr_trigger_options (BFS over the 10 named trigger families). This is the biggest 'less computer' delta yet — 296MB of pre-computed optimal DR solutions deleted.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 28 | 20 | 8 | Marcin Chmielewski | 38 | 381s | 126s | $0.14 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 31 | 20 | 11 | Marcin Chmielewski | 51 | 1235s | 199s | $0.23 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 30 | 23 | 7 | Marcin Chmielewski | 60 | 1789s | 169s | $0.25 |

**Solved**: 3/3
**Avg sim moves (solved)**: 29.7
**Avg human (WCA) (solved)**: 21.0
**Avg gap (solved)**: +8.7
**Total API cost (rough, no cache discount)**: $0.62

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__attempt5_20260517_162423.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__attempt2_20260517_164026.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3__attempt1_20260517_170016.md)
