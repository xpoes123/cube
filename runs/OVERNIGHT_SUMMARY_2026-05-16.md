# Overnight session — 2026-05-16, v13 → v20

Started at ~3:30 AM with v13 results: 4/5 solved, avg 28.2, BackiPetrovac DNF.

Ended at ~6:25 AM with v20: 5/5 solved, avg 29.2, gap +8.4 (Opus 4.7), with v16 still holding the move-count crown at avg 28.2 (Sonnet 4.5).

## What shipped (8 iterations + a research subagent + a multi-hour offline build)

| Iter | Headline change | Solved | Avg | Δ vs v13 |
|------|-----------------|--------|-----|----------|
| v14a | Budget gates on replace_and_shorten | **5/5** | 29.4 | +1.2 mv, but +DNF→solve |
| v14b | DR-quality + branch journal (333.fm research-driven) | 4/5 | 28.5 | +0.3, regressed reliability |
| v15  | dr_trigger_options on all 3 axes | (stacked into v16) | — | — |
| v16  | **niss_scout — single biggest move-count win** | **5/5** | **28.2** | **same avg, +DNF→solve** |
| v17  | compose_niss_solution + quick_check | 5/5 | 28.6 | +0.4 (prompt-flow regression) |
| v18  | Tool-side rs_recommend in compose | 5/5 | 29.4 | +1.2 |
| v19  | corpus_eval --n-best N wrapper | 5/5 | 29.4 | (variance probe; no lift) |
| v20  | Opus 4.7 model A/B + prewarm cache | 5/5 | 29.2 | (Opus -0.2 vs Sonnet) |

## What changed in capability

1. **`niss_scout`** (`src/cube/tools/niss_scout.py`): 6-row read-only
   scout of normal × inverse × {UD/FB/RL}, sorted by expected_total_to_solved.
2. **`dr_trigger_options` on all 3 axes**: per-axis catalogs by cube
   symmetry from the UD reference. Removed dr_pattern_lib dependence
   on FB/RL.
3. **`compose_niss_solution`**: engine-side NISS-sheet assembly. Fixes
   the WesternSicily-style hand-inversion failures.
4. **`quick_check`**: free 0s state classifier. Replaces analyze_residual
   for the common case.
5. **rs_recommend**: surfaced inside compose_niss when r&s gates pass.
6. **`replace_and_shorten` gates**: 1-call cap + ≥30 tool-calls remaining
   (prevents v13-style BackiPetrovac DNFs).
7. **corpus_eval `--n-best N`**: deterministic variance probe.
8. **Opus 4.7 support**: adaptive thinking API.
9. **subset_finish_cache pre-warm**: 13 → 176 entries (Task #68 since v8).

## Knowledge artifacts

- **`runs/333fm_research_2026-05-16.md`** (115 lines): empirical analysis
  of 942 WCA-FMC submissions. Key finding: DR length is THE single
  discriminating variable (sub-22 has DR ≤6 in 85.7%). Insertions are
  a failure-mode tool (0.7% elite, 15.8% long). Slice moves never appear
  in final notation. This research drove the v14b/v15/v16 pivot away
  from slice insertions.
- **`runs/V14_RESULTS.md` through `V20_RESULTS.md`**: per-iteration
  writeups with honest accounting of what worked, what regressed, why.
- **Memory updates** in `~/.claude/projects/-home-david-code-cube/memory/`:
  - `project_v20_state.md` (was v16) — current state
  - `feedback_corpus_variance_ceiling.md` — 3-5 move per-scramble variance
    documented; prompt tweaks within current model+tools can't reliably
    move averages below this floor
  - `feedback_prompt_format_braces.md` — literal `{UD, FB, RL}` in
    `.format()` templates crashes silently

## Where we are vs human champions

- Sim avg: 28.2 (v16) — 29.4 (v18/v19)
- WCA-champion avg: 20.5
- Gap: +7.4 to +8.9

Per the research, this gap is roughly:
- 5-6 moves: DR/HTR quality (NISS judgment, JZP exploitation, axis selection refinement)
- 1-2 moves: opportunistic insertions when residual cooperates

## Open future iterations

1. **dr_rescout**: leverage the now-warm cache to refresh DR ranking with
   actual HTR-finish lengths after EO commit (deferred v18 plan).
2. **More named DR triggers** (Hitchhiker DR §triggers): extend the
   10-trigger catalog to 20+. Stronger named-recall on rare cases.
3. **Retire dr_pattern_lib runtime**: once dr_rescout + expanded triggers
   cover the same cases.
4. **N-best with N≥4**: chase the lucky run for video-shoot solves. ~$4-8 per eval.
5. **nissy-oracle policy retraining** (Task #72): multi-day GPU job.

## Cost spent

Across all corpus runs in this session: ~$8-10 from the $100 budget.
Plenty left.

## Honest verdict

v16 (niss_scout) was the only iteration that delivered both a
move-count gain AND a reliability gain in one shot. Everything since
has been infrastructure that compounds robustness (5/5 holds) but
doesn't reliably move move-count past 28-29 with current tools.

To push below 25 cleanly would need:
- New tools the agent can use (named DR triggers expansion, dr_rescout)
- Or a better policy (nissy-oracle retraining)
- Or much larger N-best
- Or a fundamentally different approach (e.g., letting the agent search
  EO candidates branching from each side — but that flirts with the
  no-A* constraint)
