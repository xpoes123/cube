# v17 — compose_niss_solution + quick_check

Targeted fixes for two v16 weak points: (1) hand-inversion of NISS
sheets (WesternSicily wasted 25 tool calls on this), (2) friction
from costly inter-phase state checks.

## Results

| Iter | Solved | Avg moves | Gap | Cost |
|------|--------|-----------|------|------|
| v16  | 5/5    | 28.2      | +7.4 | $1.09 |
| v17  | 5/5    | 28.6      | +7.8 | $0.90 |

### Per-scramble

| ID | v16 | v17 | Δ |
|----|---:|---:|---:|
| PSSS_s1 | 25 | 26 | +1 |
| PSSS_s2 | 26 | 26 | 0 |
| PSSS_s3 | 30 | 30 | 0 |
| BackiPetrovac | 29 | 31 | +2 |
| WesternSicily | 31 | 30 | **−1** ✓ |

### Net assessment

**The WesternSicily fix worked as designed** — compose_niss_solution
let the agent solve cleanly on inverse and assemble the canonical sheet
without hand-inverting. But the overall corpus regressed +0.4 moves
because **BackiPetrovac skipped its mandatory replace_and_shorten call**.
At 31 moves with 33 tool calls remaining (gate is ≥30), the v14b/v15
prompt mandated r&s — but the v17 compose_niss_solution addition
changed the closing-flow narrative ("solve → compose → submit") and
the agent treated compose_niss_solution as the implicit "done" signal.

This is a prompt-precedence issue, not a tool failure. The compose
tool's "always call this before FINAL_SOLUTION" wording is too strong;
needs to be qualified to "AFTER refinement options are exhausted."

### What works in v17

- **quick_check (free, 0s sim)**: PSSS_s1 used it 7×, replacing what
  would have been ~14s of analyze_residual. The mandatory inter-phase
  checks are now budget-friendly.
- **compose_niss_solution**: WesternSicily solved at 30 (was 31) and
  the inverse-side path is now reliable. The agent narrates "I'll
  hand the slot to the engine for assembly" instead of doing modular
  cube algebra in output tokens.

### What needs fixing

- Prompt closing-flow order: r&s must be checked BEFORE compose, not
  after. Move the r&s mandate "above" the compose step in the prompt.
- Or: make the compose tool itself surface an r&s opportunity when
  length≥27 and gates pass (tool-side reminder).

## v18 direction

Either fix the r&s ordering (simple prompt edit, expect +1 move
recovery → ~27.6) or build something larger (dr_rescout, model swap).
Going with the prompt fix first since it's a deterministic recovery.
