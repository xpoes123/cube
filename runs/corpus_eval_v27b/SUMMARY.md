# v27b corpus eval — niss_scout removed + cross-attempt memory

Model: `claude-sonnet-4-5-20250929`
Run: 2026-05-17 (3 scrambles, n_best=4)

## Changes vs v25

1. **`niss_scout` removed entirely** from the tool list. Agent must scout
   axes manually: `inspect_state` → per-axis `eo_pattern_lookup` →
   `niss_flip` to scout inverse side → `dr_trigger_options` per candidate
   → judge joint EO+DR+finish cost yourself.
2. **Cross-attempt memory**: each attempt after the first receives a
   user-message brief of all prior attempts on this scramble (move
   counts + solution strings) plus a "beat your best, try a different
   branch" instruction. Real WCA-FMC competitors get one scramble +
   one hour with continuous memory; they don't restart blind.

## Why v26 was killed before v27b

v26 (canonical-order niss_scout, sort removed) was killed mid-run after
the user pointed out that niss_scout's rows still contained
`finish_length_actual` and `total_to_solved_actual` — even with no sort,
those numbers made the choice trivial. User's framing:
*"this is too computer like."*

## Results — 3 scrambles

| Scramble | v25 best | v27b best | delta | v27b attempt sequence |
|---|---:|---:|---:|---|
| PSSS_s1 | 25 | 29 | +4 | 30, 30, 30, 29 |
| PSSS_s2 | 26 | 26 |  0 | **26**, FAIL, FAIL, FAIL |
| PSSS_s3 | 30 | 27 | -3 | 31, 27, FAIL, FAIL |
| **avg** | 27.0 | 27.3 | +0.33 | |

## Findings

1. **niss_scout removal is roughly net-neutral.** Same 3-scramble avg
   (27.3 vs 27.0) within run-to-run variance. The "stockfish in tools"
   hypothesis is partially refuted: the agent finds comparable solutions
   through manual axis exploration. PSSS_s3 actually IMPROVED by 3 moves.

2. **Cross-attempt memory as currently written is HURTING.** On PSSS_s2
   and PSSS_s3, the agent solved on attempt 1 (no memory) but then FAILED
   on attempts 2–4 (with memory of prior attempts). The "try a DIFFERENT
   branch" instruction pushes the agent into incomplete branches that
   burn the 80 tool-call budget. Same regression pattern as v14b and v23b
   prompt additions (see `feedback_backtracking_prompt_hurts.md`).

3. **PSSS_s1 regression of 4 moves** is the only concerning data point.
   v25's 25-move solve relied on niss_scout's pre-computed
   `total_to_solved_actual` to identify the optimal branch. Manual
   exploration found a viable but longer path. Open question for v27c.

## Next directions

- Soften the memory message: "here's what you tried; feel free to repeat
  the same approach if you believe it's optimal" — let the agent decide
  whether to switch branches rather than commanding it to.
- OR: tell the agent to "commit harder to risky lines on each individual
  attempt; future iterations will explore alternatives." This biases
  individual attempts toward completion (vs. branching exploration) and
  uses n_best=4 itself as the exploration mechanism.
- PSSS_s1's manual-scout floor of 29 is the bottleneck — investigate
  whether a different prompt framing or an additional cheap recall tool
  (not a search tool) closes the gap.
