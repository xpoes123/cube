# Corpus eval — `v29`

- **Model**: `claude-sonnet-4-5-20250929`
- **Run**: 2026-05-17T02:09:33
- **Scrambles**: 3 (n_best=8)
- **Total API cost**: $0.57

## What changed in this version

Stack of five changes vs v27b:
1. **DR substate-family priors table** in system prompt (3C2E ~6-8mv post-DR
   finish, 4C2E ~9-11, 2C4E ~10-12, 4C4E ~12-14). Replaces the v25-era
   `expected_total_to_solved` tool-side oracle with memorized human heuristics.
2. **JZP weighting amplified**: `jzp_eligible` halves post-DR cost; prefer
   JZP-eligible DRs even at +4-5mv DR length.
3. **`subset_finish_cache.pkl` → `data/memory/subset_finish.md`** (170
   entries, hand-editable markdown for a top-level FMC reviewer to extend).
4. **Auto-cancel at every `apply_moves` boundary** — free mechanical moves
   a human writes on paper without thinking.
5. **n_best bumped 4 → 8.**

## Results

| Scramble | v25 best | v27b best | **v29 best** | Δ vs v25 | attempt seq (8) |
|---|---:|---:|---:|---:|---|
| PSSS_s1 | 25 | 29 | **25** |  0 | 30, **25**, 29, 29, 31, 28, 28, 31 |
| PSSS_s2 | 26 | 26 | **27** | +1 | 33, **27**, 30, **27**, 32, 30, 30, 32 |
| PSSS_s3 | 30 | 27 | **27** | −3 | 30, 30, 30, 34, 30, 30, 30, **27** |
| **avg** | 27.0 | 27.3 | **26.3** | −0.7 | |

v29 is the new best — half a move better than v25, and a full move better
than v27b. PSSS_s1 fully recovered from v27b's regression (29 → 25).
PSSS_s3 holds the v27b improvement (30 → 27).

## Headline findings

- **The "stockfish" hypothesis is now mostly refuted.** v27b removed
  niss_scout and showed a small overall regression (27.0 → 27.3). v29
  added human-shape substate priors + JZP weighting and improved past v25.
  The agent has real joint-cost reasoning given the right memorized
  heuristics — same shape as how elite humans operate.
- **PSSS_s2 is the holdout** at 27 vs 26. Likely benefits from the
  approach that found the v25 26-move (which used niss_scout's exact
  finish-length numbers). Subject to corpus variance; n_best=16 might
  recover it.
- **Auto-cancel didn't hurt and probably helped.** Several attempts
  had `auto_cancelled_saved > 0` in the apply_moves return.

## Next directions

- **v30 — strip the wide DR/EO libraries** (currently 3.2M and 6,144
  entries; the elite-human equivalent is ~100). Cap EO library to ≤4-move
  patterns, restrict DR enumeration to the named-trigger catalog. Forces
  more "discover via apply_moves + brain" rather than "menu lookup."
- **Brain v4 (overnight)** — retrain on 500K scrambles to bump DR top-1
  accuracy from 66% → ~72-75%, making brain_suggest a reliable tiebreaker.
- **n_best=16** as a final-showcase config once code is stable.

## Per-scramble narratives

- [PSSS_s1 best attempt #2 (25mv)](fm_PSSSideDayGdansk2026_s1__attempt2_20260517_010156.md)
- [PSSS_s2 best attempt #2 (27mv)](fm_PSSSideDayGdansk2026_s2__attempt2_20260517_012623.md)
- [PSSS_s3 best attempt #8 (27mv)](fm_PSSSideDayGdansk2026_s3__attempt8_20260517_020603.md)
