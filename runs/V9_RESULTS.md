# v9 corpus eval — DR pattern library

The 9th iteration. v8 closed the EO bottleneck with the EO pattern
library (5/10 solved). v9 closes the DR bottleneck with a same-shape
DR pattern library (1.08M entries × 3 axes, forward BFS in 79 sec).

## TL;DR

**10/10 solved, avg 29.9 moves, $0.65 total.**

Every scramble that had never solved in v1–v8 now solves cleanly in
16 tool calls and ~$0.06 each. The agent runs the canonical FMC pipeline
end-to-end as recall-not-search: EO library × 3 axes → DR probe × 3 →
pick shortest total → DR library → HTR subset → memorized finish →
cancel → ship.

| | v6 | v7 | v8 | **v9** |
|---|---:|---:|---:|---:|
| Solved | 1/10 | 5/10 | 5/10 | **10/10** |
| Avg moves (solved) | 35.0 | 31.0 | 30.2 | **29.9** |
| Avg cost | $1.49 | $0.17 | $0.14 | **$0.06** |
| Avg tool calls | 50+ | 35+ | 16 | **16** |

## Per-scramble

| ID | v9 | v8 | Δ | Baseline | Gap |
|---|---:|---:|---:|---:|---:|
| scramble1 | **30** ✓ | DNF | **NEW** | 30 | **0** (tied) |
| scramble2 | **30** ✓ | 32 | −2 | 25 | +5 |
| scramble3 | 30 ✓ | 27 | +3 | 31 | −1 |
| scramble5 | **33** ✓ | 35 | −2 | 33 | **0** (tied) |
| random1 | **30** ✓ | DNF | **NEW** | — | — |
| random2 | 31 ✓ | 26 | +5 | — | — |
| random3 | **30** ✓ | DNF | **NEW** | — | — |
| random4 | **28** ✓ | DNF | **NEW** | — | — |
| random5 | 30 ✓ | 30 | 0 | — | — |
| random6 | **27** ✓ | DNF | **NEW** | — | — |

**5 new solves** (scramble1, random1, random3, random4, random6).
**3 strict improvements** (scramble2, scramble5, random6/r4 implicitly).
Avg gap to analyzer on the 4 baselined: **+1.0 move**.

## The clean v9 pipeline

Every solving run shows the same 16-tool-call pattern:

1. `inspect_state(main)` — count bad edges per axis
2. `eo_pattern_lookup(main, axis=UD/FB/RL)` × 3 — recall optimal EO
3. `probe_dr_pattern(main, eo_alg=[..], axis=X)` × 3 — preview DR
4. `apply_moves(EO sequence)` — commit best (EO+DR) total
5. `dr_pattern_lookup(main, axis=X)` — recall DR completion
6. `apply_moves(DR sequence)`
7. `htr_subset(main)` — identify subset
8. `lookup_subset_finish(main, axis=X)` — recall finish
9. `apply_moves(finish)`
10. `cancel(full_solution)` — collapse repeated face moves
11. `verify_solved(solution)`
12. SHIP

No BFS escape hatches. No NISS frame churn. No try_alg grinding.
Like a champion running through their memorized lines.

## Why the DR library landed

Same shape as the EO library, deeper. For each reachable
(corner-orient, slice-membership) reduced state within the EO-preserving
subgroup on each axis, we precompute an optimal-length completion to DR.

**Reduced state space**: 3^7 × C(12, 4) = 1,082,565 per axis.
Forward BFS from DR-solved with EO-preserving moves enumerates every
reachable pre-image. ~80s total build, 282 MB pickle, max depth 10.

The corner-orientation array under each axis transforms locally:
`new_co_ax[dst] = co_ax[src] + (face_pos_slot[dst] - face_pos_slot[src]
- dco_ud[i]) mod 3` — a closed-form per-axis delta table derived from
the existing UD-axis turn data. Sanity-checked against full-State
applications across 10 random sequences × 3 axes.

## The new bottleneck

Move count, not solvability. Avg 29.9 is competitive with strong amateur
FMC; analyzer baseline averages 29.75 on the 4 hand-picked. To close
the remaining gap to the analyzer (which uses depth-12 A* + 663k PDB),
we'd need:

1. **Multi-option libraries** — store top-K shortest EO/DR per pattern
   so the agent can pick (eo_len, dr_len, finish_len) joint-min instead
   of greedy EO+DR-min.
2. **NISS-aware library**: precompute the inverse-frame patterns too
   so the agent can choose the cheaper frame per scramble.
3. **More human-shaped tools**: break the DR/HTR phases into named
   trigger-applications instead of monolithic 8/19-move recalls. Same
   solve quality, much richer transcript narrative for the video.

## File map

- `src/cube/tools/dr_pattern_lib.py` — library + lookup
- `src/cube/agent/build_dr_library.py` — offline builder
- `checkpoints/dr_pattern_library.pkl` — pickled library (282 MB,
  gitignored)
- `runs/corpus_eval_v9/` — the 10 transcripts

## Cost summary

Total session cost so far: ~$73 + $0.65 = $73.65 of $100 budget.
$26 of headroom for whatever comes next.

## Next open work

1. **Decompose the DR + HTR steps for richer human-shaped narration**.
   Currently `dr_pattern_lookup` returns 8 moves wholesale and
   `lookup_subset_finish` returns 19 moves wholesale. Refactor into
   `dr_recognize` + `apply_dr_trigger`, and `htr_classify` +
   `apply_finish_phase`. Forces the LLM to name what it sees and
   compose the rehearsed pieces — closer to how a champion verbalizes
   their solve.
2. **Multi-option libraries** — top-3 per pattern, joint-min over
   (EO + DR + finish) instead of greedy EO+DR.
3. **The video** — material is overwhelmingly ready. v9 transcripts
   read as 16-tool-call clean champion-shaped solves at $0.06 each.
