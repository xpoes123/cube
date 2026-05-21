# Corpus eval — `v35_opus`

- **Model**: `claude-opus-4-7`
- **Run**: 2026-05-21T01:32:50
- **Scrambles**: 5

## What changed in this version

v35 full corpus (Opus 4.7). dr_progress_options + bookmark_fork/restore_fork + cross-attempt narrative handoff. Inverse-of-scramble harness rejection in place. n_best=3 sharing 3600s budget per scramble. All 5 scrambles run in parallel.

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 31 | 20 | 11 | Marcin Chmielewski | 31 | 175s | 192s | $0.28 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 33 | 20 | 13 | Marcin Chmielewski | 40 | 130s | 214s | $0.33 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 33 | 23 | 10 | Marcin Chmielewski | 23 | 49s | 91s | $0.13 |
| fm_BackiPetrovacOpen2026_s1 | ✗ | — | 22 | — | Szabolcs Szántai | 138 | 595s | — | — |
| fm_WesternSicilyOpen2026_s1 | ✓ | 34 | 19 | 15 | Chiara Marcucci | 82 | 279s | 683s | $0.40 |

**Solved**: 4/5
**Avg sim moves (solved)**: 32.8
**Avg human (WCA) (solved)**: 20.5
**Avg gap (solved)**: +12.3
**Total API cost (rough, no cache discount)**: ~$1.40

> Note: Backi DNF is a real result (both attempts hit the 150-tool-call
> wall navigating DR). WSicily's 34mv is a real legit solve from attempt 1
> — the corpus_eval process pool crashed during the per-scramble synth
> step due to credit exhaustion, leaving the auto-summary incorrectly
> marking this scramble ✗. Result restored from the on-disk JSON.

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1__blog.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2__blog.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3__blog.md)
- [fm_BackiPetrovacOpen2026_s1](fm_BackiPetrovacOpen2026_s1__blog.md)
- [fm_WesternSicilyOpen2026_s1](fm_WesternSicilyOpen2026_s1__blog.md)
