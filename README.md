# cube

**An LLM-orchestrated Rubik's-cube Fewest-Moves-Challenge agent.** A
Claude model (Sonnet 4.5 by default) is given a small set of
human-scale FMC tools — pattern lookups, named-trigger menus,
NISS-scout, HTR subset classifiers — and asked to solve WCA-grade
scrambles within the same cognitive constraints a strong human FMC
solver operates under.

> "Can an LLM solve a Rubik's cube as well as a human FMC champion?
> I gave Claude the same tools a human uses and watched it try."

See [`AGENT.md`](AGENT.md) for the design doc and the
"fair vs. cheating" axioms.

## Current corpus results

5 WCA-competition scrambles (from `api.333.fm`), 80-tool-call budget
per solve. Model: `claude-sonnet-4-5-20250929`.

| Iter | Headline change | Solved | Avg moves | Gap vs WCA-champion (20.8) |
|------|-----------------|--------|-----------|----------------------------|
| v13  | skeleton + insertion tools | 4/5 | 28.2 | +7.4 |
| v14a | budget-gated `replace_and_shorten` | 5/5 | 29.4 | +8.6 |
| v14b | DR-quality (4C4E trap warning) | 4/5 | 28.5 | +7.7 |
| **v16** | **`niss_scout` — 6-row scout of normal × inverse × 3 axes** | **5/5** | **28.2** | **+7.4** |
| v17  | `compose_niss_solution`, free `quick_check` | 5/5 | 28.6 | +7.8 |
| v18  | tool-side `rs_recommend` | 5/5 | 29.4 | +8.6 |
| v19  | corpus_eval `--n-best N` (variance probe) | 5/5 | 29.4 | +8.6 |
| v20  | Opus 4.7 model A/B + prewarm cache | 5/5 | 29.2 | +8.4 |
| v21+v22 | few-shot exemplars + joint EO+DR scout | 5/5 | 29.6 | +8.8 |
| **v23a** | **strip oracle recommendations** | **5/5** | **28.4** | **+7.6** |

Transcripts and per-scramble narratives in `runs/corpus_eval_*/`.
Each iter's reasoning + tradeoffs are documented in `runs/V*_RESULTS.md`.

## Key findings

1. **DR-quality dominates the move-count gap, not insertion technique.**
   A research subagent harvested 942 elite WCA-FMC submissions
   (`runs/333fm_research_2026-05-16.md`); sub-22-move solves had
   DR ≤6 moves 85.7% of the time; NONE had DR ≥10. Elite insertion
   rate is 0.7% (long-solve rate is 15.8% — insertions are a
   *failure*-mode tool). This invalidated our original v14b plan
   (slice insertions) and pivoted the agent toward better DR scouting.

2. **Tool-side recommendations were doing the LLM's work.** When the
   smarter Opus 4.7 matched Sonnet 4.5 within noise (29.2 vs 29.4),
   that was evidence the agent's *judgment* wasn't engaging — tools
   were pre-cooking the decisions via `expected_total_to_solved`,
   `niss_scout.recommendation`, `rs_recommend` fields. v23a stripped
   these oracles and the corpus average *improved* to 28.4. Tools
   should expose observable information; the LLM should judge.

3. **Move-count variance per scramble is 3-5 moves.** Single-run
   averages bounce ±1-2 moves between iterations. Prompt-strength
   tweaks within the current model + tool surface are mostly noise.
   Real gains come from capability additions (new tools, richer
   knowledge), not prompt engineering.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  LLM (Sonnet 4.5)                                    │
│  • narration + decision                              │
│  • 80-tool-call budget per scramble                  │
└──────────────────────┬───────────────────────────────┘
                       │ tool calls
┌──────────────────────┴───────────────────────────────┐
│  Agent tool layer  (src/cube/agent/simulated_fmc.py)│
│  • inspect_state, quick_check (free state class)    │
│  • niss_scout (6-12 rows, normal × inverse × axes)  │
│  • eo_pattern_lookup, dr_trigger_options            │
│  • htr_classify, apply_htr_phase                     │
│  • analyze_residual, derive_corner_3cycle           │
│  • replace_and_shorten (gated 1-call)               │
│  • compose_niss_solution                             │
│  • brain_suggest (state-conditioned, new)           │
└──────────────────────┬───────────────────────────────┘
                       │
┌──────────────────────┴───────────────────────────────┐
│  Knowledge layer                                     │
│  • EO pattern library (6144 entries)                 │
│  • DR pattern library (3.25M — being retired)       │
│  • HTR subset cache (176 entries, pre-warmed)       │
│  • 432-entry corner-3-cycle commutator table         │
│  • named DR trigger catalog (10 per axis)            │
│  • brain models — eo/dr/htr/finish (~86k params each)│
└──────────────────────────────────────────────────────┘
```

## The brain (v1, training-stage)

Replaces the legacy 91k history-conditioned transformer policy. The
new brain is **state-conditioned**: the model sees the cube state
(cubie permutations + orientations), not a sequence of past moves.
Per-step output heads predict the next move from each step's legal
alphabet:

| Step   | Alphabet | Trained val-loss | Val top-1 acc |
|--------|----------|------------------|---------------|
| EO     | 18 face moves | 1.625 | 57% |
| DR     | 14 EO-preserving | 2.178 | 31% |
| HTR    | 10 DR-preserving | 1.264 | 55% |
| Finish | 6 half-turns | 1.138 | 57% |

Trained on per-step optimal-move distributions extracted from
[nissy](https://sebastiano.tronto.net/nissy/) via
`cube.brain.gen_training_data`. v1 used 1000 scrambles × ~36
records/scramble; planned scaling: 10K-100K scrambles.

Architecture: small transformer over 20 cubie tokens (8 corner +
12 edge), each token a sum of `slot_emb + cubie_emb + orient_emb`.
2 encoder layers, d_model=64, ~86k params per step model. See
`src/cube/brain/{state_encoder,model,train,infer}.py`.

DR top-1 is the weakest (31%) — large alphabet + many equally-optimal
first moves at any state. KL-divergence loss reflects distribution
fit better than argmax accuracy for soft targets.

# The algebra

This section is for readers who like cosets. Skip if you don't.

## The cube group G

`G` is the group generated by 6 face moves (3 turns each = 18
generators). `|G| = 43,252,003,274,489,856,000 ≈ 4.3 × 10^19`. Far too
big to enumerate.

To search effectively, FMC uses a chain of subgroups:

```
G  ⊇  EO  ⊇  DR  ⊇  HTR  ⊇  {e}
```

Each reduction "removes degrees of freedom" so the next layer's search
space is small.

## EO: edge orientation

A state is in `EO_UD` if every edge has its UD-axis orientation correct
(no F or B quarter would flip it). Concretely: 4-bit-per-edge parity is
zero on all 12 edges.

`|G : EO_UD| = 2^11 = 2048` (one EO bit is parity-determined; 11 are
free).

## DR: domino reduction

A DR-UD state is in `EO_UD` AND every corner is **UD-axis oriented**
(its U/D sticker points up or down). Equivalently: only `⟨U, D, R², L²,
F², B²⟩` moves are needed from here on. This is the "domino" subgroup
because the cube reduces to a 2-layer puzzle.

## HTR: half-turn reduction

**HTR group** = `⟨U², D², R², L², F², B²⟩`. Generated by 6 half-turns.
Has exactly **663,552 elements**. Diameter (worst case) = **15
half-turns**. We've enumerated all of it via BFS from SOLVED and stored
a parent-pointer PDB:

```python
# cube/classifier/htr.py
def htr_pdb() -> dict[StateKey, (distance, parent_move)]:
    # multi-source BFS, 6 half-turn moves
```

`663,552 = 96 · 6912 = |HTR_corner| · |HTR_edge|`. Both factors are
themselves cosets of the symmetric/alternating groups.

### The 96 HTR corner classes

Half-turns act on corner permutations as a subgroup of `S_8` of order
96. These 96 perms are the corner perms reachable from solved via
half-turns only.

### DR-corner-set ⊃ HTR-corner-set

The DR group `⟨U, D, R², L², F², B²⟩` acting on corners reaches the
**full S_8 = 40,320**. So:

```
DR_corner_perms (40320)
  ⊇  HTR_corner_perms (96)
```

Index `[DR : HTR] = 40,320 / 96 = 420` corner cosets. These 420 cosets
are what the FMC community calls "subsets" — `4a1`, `4b2`, `2c3`, etc.

# Running it

## Single solve

```bash
ANTHROPIC_API_KEY=sk-... PYTHONPATH=src uv run python -m cube.agent.simulated_fmc \
  "R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F"
```

Transcripts emit to `runs/sim_TIMESTAMP.json` (full tool-call trace +
narration) and a `.md` rendering alongside.

## Corpus eval

```bash
# 5-WCA-scramble corpus eval (current standard benchmark)
ANTHROPIC_API_KEY=sk-... PYTHONPATH=src uv run python -m cube.agent.corpus_eval \
  --corpus-333fm data/corpus_333fm.json \
  --out-dir runs/corpus_eval_v24 \
  --max-tool-calls 80 \
  --wall-limit-s 1500

# Beat-the-variance (run each scramble N times, keep best)
... --n-best 2

# Opus A/B
... --model claude-opus-4-7
```

## Training the brain

```bash
# 1. Install nissy: see https://sebastiano.tronto.net/nissy/
nissy gen   # ~90 min, builds the optimal-solver pruning tables

# 2. Generate training data via the nissy oracle (~1.5s/scramble)
PYTHONPATH=src uv run python -m cube.brain.gen_training_data \
  --n 10000 --out data/brain_training

# 3. Train each step model (~5 min/step on CUDA)
for step in eo dr htr finish; do
  PYTHONPATH=src uv run python -m cube.brain.train --step $step --epochs 30
done

# 4. Pre-warm HTR subset finish cache (optional, ~1 hour)
PYTHONPATH=src uv run python -m cube.agent.prewarm_subsets --axes UD FB RL
```

Checkpoints land in `checkpoints/brain_{step}.pt`. The agent's
`brain_suggest` tool auto-detects them and falls back to the legacy
policy otherwise.

# Repo layout

```
src/cube/
  engine/        State, moves, notation, cancellation
  classifier/    rule-based EO/DR/HTR, PDBs, leave-slice scaffolding
  corpus/        parse/validate WCA reconstructions from 333.fm
  brain/         NEW — state-conditioned move predictor (v1)
    state_encoder.py    State → 20 cubie tokens
    model.py            BrainStepModel (small transformer)
    gen_training_data.py  nissy oracle → JSONL per step
    train.py            supervised training, KL loss
    infer.py            policy_suggest() — agent-facing API
  agent/         LLM-orchestrated agent
    simulated_fmc.py    main agent (~1900 lines: tools + prompt + loop)
    corpus_eval.py      multi-scramble eval CLI with --n-best
    prewarm_subsets.py  HTR subset finish cache builder
  tools/         agent's tool layer
    eo_pattern_lib.py       6144-entry EO library
    dr_trigger_options.py   named DR triggers, all 3 axes (v15)
    niss_scout.py           6-12 row joint scout (v16+v22)
    insertion_tools.py      analyze_residual / derive_corner_3cycle / r&s
    nissy_oracle.py         nissy subprocess wrapper (v23)
    dr_pattern_lib.py       legacy 3.25M-entry library (being retired)
  analyzer/      legacy unconstrained pipeline (now a baseline)

tests/           pytest, mirrors src layout
data/            corpus_333fm.json + brain_training/ + cache (gitignored)
checkpoints/     model weights (gitignored except brain_*.pt)
runs/            per-iter eval transcripts + V*_RESULTS.md writeups
```

# Honest accounting

The agent is at ~28 moves on a 5-WCA-scramble corpus vs WCA-champion
20.8. That ~7-move gap is roughly:

- 5-6 moves: DR-quality (axis selection, NISS-quality judgment, JZP
  exploitation) — what the brain v1 is being scaled to address
- 1-2 moves: opportunistic insertions when residual cooperates

The original premise — "this is human-shape solving with human-scale
tools" — is partially compromised: the 3.25M-entry `dr_pattern_lib`
is not human-scale, and was carrying real load on solve quality. v23a
(stripping tool-side oracle recommendations) showed the LLM itself
reasons better when not given pre-cooked judgments. The honest path
forward is closing the DR-quality gap via the brain (trained on
nissy-optimal moves at scale), retiring `dr_pattern_lib`, and
expanding `dr_trigger_options` to ~20-40 named human-recall triggers.

See `runs/OVERNIGHT_SUMMARY_2026-05-16.md` for the full v14a→v20
iteration arc, plus `runs/V23a_RESULTS.md` (pending) for the oracle-
stripping experiment.
