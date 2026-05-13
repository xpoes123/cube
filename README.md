# cube

An FMC (Fewest Moves Challenge) analysis engine calibrated to **human
findability** rather than theoretical optimum. Fills the gap between Cube
Explorer (optimal, brute-force, method-agnostic) and human FMC solvers
(bounded search, method-driven).

> "Find the best solution that was actually findable."

## Why

Optimal solvers are useless to humans: they suggest 24-move solutions that
no person could reproduce because they require search depth no human has.
Existing FMC tutors are prescriptive — they teach a method, not a way to
think about a specific scramble.

This project sits in that gap. Given a scramble (or a scramble + a partial
attempt), the engine produces:

1. A best **human-findable** continuation — a solution a strong FMC solver
   would plausibly have found, not the theoretical optimum.
2. A tree of branches at each state, colored by **value × findability**:
   - **Green** — high value AND human-likely (consider this)
   - **Yellow** — high value but computer-only (study, don't expect)
   - **Red** — low value
   - **Gray** — expandable on demand
3. Annotated phase breakdown of an attempt: where it diverged from the
   strong-solver path, what stage transitions were taken, alternatives that
   were available.

A partial attempt is treated as a **soft preference**, never a hard
constraint — FMC routinely benefits from breaking partial structure
(EO/DR/block) when a clever insertion pays off. The model conditions on
your history but is allowed to recommend abandoning it.

## Project status

| Phase | Status |
|-------|--------|
| 1. Engine + state classifier + corpus pipeline | done |
| 2. Stage segmenter + method inference | done |
| 3. Training data pipeline + non-ML baselines | done |
| **4. Findability policy v0 (this work)** | **in progress** |
| 5. Analyzer MVP | next |
| 6. Calibration + 4×4 | future |

## Architecture overview

```
                    ┌────────────────────────────────────────┐
                    │ cube/engine                            │
                    │   - State (cubie coords, multi-axis EO)│
                    │   - Move, Face, Turn, parse_alg        │
                    │   - facelet ↔ cubie (validated)        │
                    └────────────────────────────────────────┘
                                  ▲
                                  │
        ┌─────────────────────────┼──────────────────────────┐
        │                         │                          │
┌───────┴────────┐    ┌───────────┴──────────┐    ┌──────────┴─────────┐
│ cube/classifier│    │ cube/corpus          │    │ cube/segmenter     │
│  rule-based    │    │  parse/validate WCA  │    │  per-move phase    │
│  EO/DR/HTR/    │    │  reconstructions     │    │  labels (comment   │
│  blocks state  │    │  from api.333.fm     │    │  + state fallback) │
└───────┬────────┘    └──────────┬───────────┘    └─────────┬──────────┘
        │                        │                          │
        └────────────────────────┼──────────────────────────┘
                                 │
                  ┌──────────────┴────────────────┐
                  │ cube/training                 │
                  │   loader → TrainingExample    │
                  │   encoding (flat / indices)   │
                  │   split (content-addressed)   │
                  │   baselines (freq, bigram…)   │
                  │   model (transformer policy)  │ ← v0
                  │   torchdata / train (next)    │
                  └───────────────────────────────┘
```

### The cube engine

`cube/engine/state.py` defines `State`: cubie-coordinate representation
with corner permutation (`cp`), corner orientation (`co`), edge permutation
(`ep`), and **three parallel edge-orientation arrays** (`eo`, `eo_fb`,
`eo_rl`) — one per axis. The flip sets are disjoint by construction:

- UD-axis EO uses FB-flip — F/B quarter turns flip 4 edges each
- FB-axis EO uses LR-flip — L/R quarter turns flip 4 edges each
- RL-axis EO uses UD-flip — U/D quarter turns flip 4 edges each

Each face quarter turn flips exactly one of the three EO arrays, so all
three track independently. This is essential for DR analysis since modern
FMC routinely scans multiple DR axes per scramble. Hand-derived from
Kociemba conventions, cross-validated against pycuber on 1000 random
states.

### The corpus

2439 WCA-competition FMC reconstructions ingested from `api.333.fm`,
parsed into a canonical JSONL format with scramble, normal-side solution,
inverse-side solution, and per-phase labels (when the author provided
them). API responses cached at `data/cache/333fm/` so re-ingest is free.

### The segmenter

Each move in a reconstruction is labeled with a phase enum (EO, DR, HTR,
BLOCK, F2L, LL, SKELETON, INSERTION, UNKNOWN). Primary signal is the
author's comments (parsed with rules like `// EO`, `// DR on UD`); fallback
is state-based detection using the classifier (e.g., "EO ends when all
eo[i] == 0").

### Training data

`cube/training/dataset.py` produces one `TrainingExample` per move:

```python
@dataclass(frozen=True, slots=True)
class TrainingExample:
    source_id: str            # solve id, for split grouping
    move_index: int           # position in flat solution
    state_before: State       # cube state before this move
    target_move: Move         # the move actually taken
    history: tuple[Move, ...] # all moves played so far
    phase: Phase | None       # author's phase label (or None past skeleton)
    raw_label: str | None     # author's exact label text
    method: Method            # CFOP, ZZ, Roux, Petrus, blockbuilding, …
```

The flat solution is `normal + invert(inverse)` — a standard FMC trick
that flattens NISS into a single linear move sequence. This is what the
model trains on; "skeleton vs. insertion" structure is recovered later in
v2.

`split.py` partitions by `source_id` with a stable content-addressed hash:
new solves added later don't reshuffle existing assignments. All moves
from a single solve stay in the same split — no leak from later moves of
a solve appearing in train while earlier moves are in val.

### Baselines (the bar to beat)

Top-1 / top-5 on val, partial-corpus run:

| Model | top-1 | top-5 |
|-------|-------|-------|
| Frequency (global) | 0.078 | 0.390 |
| Frequency (per-phase) | 0.059 | 0.363 |
| Bigram (P(move \| prev_move)) | **0.114** | **0.464** |
| Bigram + phase | 0.101 | 0.441 |

Bigram is the bar. Anything below this isn't worth shipping.

Target for the transformer: **top-1 ≥ 0.25, top-5 ≥ 0.70**.

## The transformer policy (v0)

`cube/training/model.py`. Built specifically for this task — small, single
encoder stack, predicts next move only (value head is v1).

### Token stream

Every example becomes a sequence of `1 + 8 + 12 + K` tokens:

```
  [CLS]  [corner_0 … corner_7]  [edge_0 … edge_11]  [hist_{K-1} … hist_0]
  └─1─┘  └─────── 8 ────────┘  └──────── 12 ──────┘  └─── K (=32) ────┘
```

- **CLS** — a learned parameter; its final hidden state is the readout.
- **Corner tokens (8)** — one per corner position. Content is the sum of
  two embeddings: `cp_emb[cp[i]]` (which corner piece is here, 0-7) and
  `co_emb[co[i]]` (its twist, 0-2).
- **Edge tokens (12)** — one per edge position. Sum of `ep_emb[ep[i]]` +
  three EO embeddings, one per axis (`eo_emb`, `eo_fb_emb`, `eo_rl_emb`),
  each a 2-vocab embedding.
- **History tokens (K=32)** — the last 32 moves played, embedded with a
  19-entry vocab (18 face-quarter moves + 1 PAD for solves shorter than
  K). Padding goes on the left so the rightmost token is always the most
  recent move.

A **shared learned positional embedding** is added to every token,
indexed by token position in the stream. This gives the model a way to
distinguish "corner 3" from "edge 3" from "history slot 3" — the position
embedding effectively encodes token *kind* (state vs history) as well as
position within kind.

### Why this tokenization

Three properties matter:

1. **Permutation-aware via attention.** The cube state isn't a fixed
   feature vector — relationships between pieces (this corner solved + this
   edge in slot) matter more than absolute identities. Self-attention over
   pieces lets the model learn "look at the UF edge's orientation when
   reasoning about the F2L pair at the FR slot."
2. **Multi-axis EO is first-class.** All three EO arrays are summed into
   the edge token, so the model sees DR potential on any axis without us
   pre-committing to one.
3. **History conditioning matters.** A context-free model can't even
   structurally match bigram (which has access to the previous move).
   Putting recent moves in the same token stream as the state lets
   attention learn things like "after R2 setup, expect a U-face move" or
   "when finishing F2L blocks, the next move usually preserves
   orientation."

### Encoder

Pre-norm Transformer encoder, configurable. v0 default:

| param | value |
|-------|-------|
| `d_model` | 96 |
| layers | 3 |
| heads | 4 |
| FFN | 288 (3× d_model) |
| dropout | 0.1 |
| history_len `K` | 32 |
| activation | GELU |
| norm | pre-LN |

Roughly 200-300k parameters. Single forward pass over ~61 tokens — fast on
CPU, trivial on the 4060.

### Readout

After encoding, the CLS hidden state is layer-normed and projected to 18
logits with a single linear layer. Training loss is cross-entropy against
`target_move` index. Top-k metrics are computed at eval time.

### What this model can and can't do

**Can:**

- Condition on full state + recent history simultaneously.
- Learn "structure-aware" patterns like "this edge is bad EO under UD,
  good under FB — propose an F-axis turn next."
- Output calibrated distributions (we keep softmax output, not argmax) —
  matters for the eventual tree explorer where node coloring requires
  P(move) not just top-1.

**Can't (yet):**

- Estimate solution length. That's a value head, added in v1.
- Look more than 32 moves back. FMC solves are usually 25-30 moves, so
  K=32 covers full history for nearly all examples — but the model has no
  global "solve plan" representation either way.
- Plan. It's a one-step policy, not an MCTS engine. Tree search comes
  later, with the model as the policy prior.

## Running it

```bash
uv sync
uv run pytest                       # 140 tests + 1 network-gated
uv run cube ingest                  # populate / refresh corpus (cached)
# training entry point lands in src/cube/training/train.py
```

## Repo layout

```
src/cube/
  engine/        State, moves, notation, facelet ↔ cubie
  classifier/    rule-based EO/DR/HTR/block detection
  corpus/        parser, validator, 333.fm adapter
  segmenter/     per-move phase labels (comment + state fallback)
  training/      TrainingExample, encoding, split, baselines, model
  cli.py         `cube ingest`, `cube ...`
tests/           pytest, mirrors src layout
data/raw/        gitignored — JSONL corpus
data/cache/      gitignored — 333.fm API cache
```
