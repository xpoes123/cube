# v14 — research-driven DR-quality iteration

The session-overnight push: closing the 8-move gap to elite WCA-FMC
solvers by leveraging the 333.fm corpus research findings rather than
chasing slice insertions.

## TL;DR

| Iter | Description | Solved | Avg moves on solved | Gap vs human (20.5) |
|------|-------------|--------|---------------------|---------------------|
| v13  | skeleton + insertion tools | 4/5 | 28.2 | +7.7 |
| v14a | budget-aware r&s + inter-phase residual checks | 5/5 | 29.4 | +8.9 |
| v14b | + DR-quality (4C4E trap, EO inverse scout, branch journal) | 4/5 | 28.5 | +8.0 |
| v15  | + dr_trigger_options on all 3 axes (per-axis catalogs) | — | — | — |
| v16  | + niss_scout (6-row read-only normal×inverse×3-axis scout) | **5/5** | **28.2** | **+7.4** |

### v16 per-scramble

| ID | Sim moves | Human | Tool calls |
|---|---:|---:|---:|
| PSSS_s1 | 25 | 20 | 35 |
| PSSS_s2 | 26 | 20 | 32 |
| PSSS_s3 | 30 | 23 | 31 |
| BackiPetrovac | 29 | 22 | 46 |
| WesternSicily | 31 | 19 | 70 |

### Why v16 wins

`niss_scout` collapses 6 separate scouting decisions (eo_pattern_lookup
×3 + dr_trigger_options ×3 on normal vs inverse) into a single tool
call. Three downstream effects:

1. **Tool-call budget conserved**. BackiPetrovac, which DNF'd in v14b
   at 80 calls due to branch-journal overhead, solved in v16 at 46.
2. **Better axis/side selection**. PSSS_s1 dropped to 25 (matching
   v13's best — which required 3 r&s calls — now achieved cleanly).
3. **`dr_trigger_options` on FB/RL** (v15) means the scout's non-UD
   cells use the same human-shaped ranking, not the 3.25M library.

WesternSicily regressed (29 → 31) — probably the agent took a
suboptimal scout row. Worth investigating but not blocking.

### Honest accounting

**v14a fixed reliability (5/5)** but lost move-count quality (29.4 vs
v13's 28.2 on solved). The reason: v14a softened r&s from "MANDATORY"
to "MAY," and the agent skipped r&s even when budget gates would have
allowed it. PSSS_s1 regressed 25→30 because v13's 3-call r&s chain
turned into 0 r&s calls.

**v14b restored mandatory r&s** (gated to 1 call, ≥30 calls remaining)
and added DR-quality changes. PSSS_s1 recovered to 28 (delta=-3 from
the single r&s call). But the branch-journal + inter-phase residual
mandate caused BackiPetrovac to **thrash to a DNF** — 80 tool calls
exhausted on the new bookkeeping.

### Lesson

Two competing forces: r&s mandate (saves moves but consumes budget)
vs prompt complexity (causes thrashing). The v16 niss_scout fix
collapses 6 separate scouting decisions into 1 tool call, hopefully
clawing back the budget BackiPetrovac needs.

## What changed between v13 and v14

### v14a (commit b10c896, then c634b31 fix)

1. `replace_and_shorten` is now gated:
   - 1-call cap per run (per Tronto §3.10's depth-1 recursion)
   - Refuses if `tool_calls_remaining < 30` (since r&s miss-path can chew
     20+ calls rebuilding the solve — root cause of v13 BackiPetrovac DNF)
   - Plumbed via new `run_state` dict updated by the solve loop each tool call

2. Prompt mandates `analyze_residual` between every `apply_htr_phase`
   chunk. If `is_pure_corner_3cycle: true` emerges, the agent branches
   to `derive_corner_3cycle` (the dormant v13 tool finally activates).
   Saves 2-4 moves on solves where a 3c residual emerges mid-finish.

3. R&S is **mandatory** (not "optional") when the gates pass — relaxing
   this in v14a-initial regressed PSSS_s1 from 25 → 30. v14b restored it.

### v14b (commits 4752360, ad30869, c634b31)

Pivoted from "slice insertions" after a research subagent's 333.fm
corpus analysis (`runs/333fm_research_2026-05-16.md`) showed:

- Elite insertion rate: 0.7%. Long-solve insertion rate: 15.8%.
- Slice moves NEVER appear in final WCA-FMC notation (0% across all tiers).
- **DR length is the single discriminating variable.** Sub-22 has DR ≤6
  in 85.7% of solves; 0% have DR ≥10. EO is fixed ~4 moves across every tier.

So instead of building slice insertions (which would not help), v14b adds:

1. **`dr_trigger_options` ranks by `expected_total_to_solved`** (= DR
   setup moves + empirical HTR-finish per substate). The 4C4E trap
   is now visible: 1-move DR + 9-move HTR = 11 total, beaten by
   4-move 3C2E + 5-move HTR = 9 total.

   Empirical HTR per family (from corpus): 3C2E=5, 4C2E=6, 2C4E=6,
   7C8E=7, 4C4E=9, 8C8E=10.

2. **Family-rank tiebreaker inverted**: 3C2E and 4C2E now preferred
   over 4C4E and 8C8E when expected_total ties.

3. **Prompt step 1b — NISS-scout EO on inverse**: 50% of elite solves
   start on inverse; our agent never did this.

4. **Prompt POST-DR DECISION rewritten**: insertions explicitly
   deprioritized; analyze_residual stays as opportunistic shortcut only.

5. **Branch journal section**: agent must verbalize rejected candidates
   ("tried 4b2 on FB, took 2c3 on UD") — a forcing function for
   comparison-before-commitment, the elite-solver behavior.

## Per-scramble results

(filled in after both runs complete)

## Honest accounting

(filled in after both runs complete)
