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

This project sits in that gap. Given a scramble (or scramble + a partial
attempt), the engine produces:

1. A best **human-findable** continuation.
2. A tree of branches at each state, scored by **value × findability**.
3. Annotated phase breakdown: where an attempt diverged from the
   strong-solver path, what alternatives were available, what stage
   transitions were taken.

A partial attempt is treated as a **soft preference**, never a hard
constraint — FMC routinely benefits from breaking partial structure
(EO/DR/block) when a clever insertion pays off.

## Project status

| Phase | Status |
|-------|--------|
| 1. Engine + state classifier + corpus pipeline | done |
| 2. Stage segmenter + method inference | done |
| 3. Training data + non-ML baselines | done |
| 4. Findability policy v0 (transformer) | done — 65% top-5 |
| 5. Analyzer MVP (M1: full-pipeline solves) | done |
| 6. M2: leave-slice / better finishes | partial |
| **7. NISS + multi-axis HTR distance tables** | **done** |
| 8. M3: insertions, optimizer | in progress |
| 9. Calibration + 4×4 | future |

### Current capability

On the real WCA scramble `R' U' F B' U2 F' U2 R2 B' R2 B' R2 U2 R2 F' L U2 B D R F L2 F D' R' U' F`,
the analyzer produces a **27-move (25 after cancellation) full solve**:

```
[ EO (UD) ]  4 moves   →  R B D' B'
[ DR (UD) ]  8 moves   →  B2 U' B2 R F2 R' F2 R       (+4→HTR)
[ HTR (UD) ]  7 moves  →  R2 U R2 B2 U2 L2 U
[ Finish ]  8 moves    →  B2 U2 F2 U2 F2 R2 D2 L2
```

verified scramble→SOLVED by the engine. Search time ~10 minutes on a
single 4060.

### NISS (Normal-Inverse Scramble Switch)

The pipeline now searches on **both the normal and inverse scrambles**,
plus the hybrids where EO is found on one side and DR is found on the
other. Every FMC solution under 22 moves uses this switch at least once.

Mathematically: if `N` are the normal-side moves and `I` are the
inverse-side moves, the final solution is `N + invert(I)`. Stages
record which side they were found on; cancellation handles the seam.

### Multi-axis HTR

The corner+edge distance PDBs are now built per-axis (UD, RL, FB) via
`lru_cache(maxsize=3)`. Before this fix, the A\* DR→HTR heuristic
returned `None` for non-UD DRs and degraded to blind BFS — silently
killing the finish on any scramble whose best DR was on RL or FB.

---

# The ML system

The core ML object is a **transformer policy** that predicts the next move
given (cube state, history). It's used as a prior during beam search and
A\* — the algorithm explores the tree, the policy ranks branches.

This was the question that started the project: *is a transformer the
right thing for cube state?* MLP felt wrong, RNN felt slow, GNN felt
ceremony. I settled on a small Transformer encoder.

## Tokenization (it's the whole game)

The trick to making a transformer work on cube state is **picking a token
set that lines up with the symmetries you care about**.

Every example becomes a sequence of `1 + 8 + 12 + K` tokens:

```
  [CLS]  [corner_0 … corner_7]  [edge_0 … edge_11]  [hist_{K-1} … hist_0]
  └─1─┘  └─────── 8 ────────┘  └──────── 12 ──────┘  └─── K (=32) ────┘
```

- **CLS** — a learned parameter; its final hidden state is the readout.
- **Corner tokens (8)** — one per *position*. Content = sum of two
  embeddings: `cp_emb[cp[i]]` (which corner piece is here, 0–7) and
  `co_emb[co[i]]` (its twist, 0–2). The model never sees raw indices — it
  sees a vector that encodes "the piece UFL is sitting at slot 3 with
  twist 1."
- **Edge tokens (12)** — one per position. Sum of `ep_emb[ep[i]]` plus
  **three EO embeddings** (`eo`, `eo_fb`, `eo_rl`), each a 2-vocab
  embedding. Three EO arrays are tracked in parallel by the engine
  (multi-axis EO — see the algebra section); the model sees all three at
  every edge, so DR potential on any axis is first-class.
- **History tokens (K=32)** — last 32 moves, 19-entry vocab (18 face
  moves + 1 PAD). Left-padded so the rightmost token is the most recent.

A **shared learned positional embedding** is added to every token. This
lets the model distinguish "corner 3" from "edge 3" from "history slot 3"
— position encodes token *kind* (state vs. history) as well as position
within kind.

**Why three EO embeddings instead of one?** Because the cube has three
EO axes (UD, FB, RL) and any of them can be the DR target. If you
collapse to one EO array, you've committed to an axis before the model
even sees the state. The disjoint flip sets are clean: F/B quarters flip
UD-EO; L/R quarters flip FB-EO; U/D quarters flip RL-EO. Hand-derived
from Kociemba conventions, cross-validated against pycuber on 1000
random states.

## Encoder

Pre-norm Transformer encoder. v0 default:

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

~91k parameters. Single forward pass over ~61 tokens. CLS hidden state is
layer-normed and projected to 18 logits with a single linear layer.
Trained with cross-entropy against the actual next move.

## Training data: the corpus

2,439 WCA-competition FMC reconstructions ingested from `api.333.fm`. Each
gets parsed into `(scramble, normal_solution, inverse_solution, per_move
phase labels)`. The **flat solution** is `normal + invert(inverse)` —
NISS gets unrolled into a single linear sequence. This way the model
trains on every move in solver order, regardless of which side it was
originally found on.

`split.py` partitions by `source_id` with a stable content-addressed
hash: new solves don't reshuffle existing splits, and all moves from one
solve stay together. No leak from later moves in train appearing earlier
in val.

## LR-mirror augmentation

This is the small but real ML lift. The cube has a left-right symmetry:
mirror through the FB plane and `(R, L, U, D, F, B)` → `(L, R, U, D, F,
B)` with appropriate twist sign flips. Every training example has an
LR-mirrored partner that's semantically identical. We feed both, **with
the same loss**, doubling effective dataset size at zero risk of leakage
(both moves are still ground-truth labels).

UD-mirror and FB-mirror also exist but were not used — the EO axis
conventions break cleanly under LR-mirror but get tangled under the
others.

## Performance

Top-1 / top-5 on val, partial corpus:

| Model | top-1 | top-5 |
|-------|-------|-------|
| Frequency (global) | 0.078 | 0.390 |
| Frequency (per-phase) | 0.059 | 0.363 |
| Bigram (P(move \| prev_move)) | 0.114 | 0.464 |
| Bigram + phase | 0.101 | 0.441 |
| **Transformer v0** | **0.288** | **0.650** |

The transformer is the bar by a large margin. ~2.5× the bigram baseline
on both metrics; absolute top-5 of 0.65 means "the right next move is in
the top 5 candidates two-thirds of the time," which is what makes
policy-guided beam search actually work.

## How the policy is used in search

The analyzer is **not** an autoregressive sampler. The policy is a
**prior** that ranks expansions; search is structured:

- **Beam search** (EO stage, DR triggers): keep top-W states by
  `Σ log π(move | state, history)`. Beam=256 for EO, beam=8192 for DR.
- **A\*** (DR → HTR, HTR → Finish): cost = depth + heuristic; the
  policy is a soft tiebreaker via `policy_weight`. Empirically the
  combined corner+edge PDB heuristic is tight enough that
  `policy_weight=0` (pure A\*) is fastest — the policy added model-eval
  overhead without improving solution quality.

The lesson: **the policy matters where there's no admissible heuristic
(EO, DR), and is dispensable where there is one (HTR, Finish)**.

---

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

Reaching EO from any scramble: 3–8 moves typically. Beam search finds it.

## DR: domino reduction

A DR-UD state is in `EO_UD` AND every corner is **UD-axis oriented**
(its U/D sticker points up or down). Equivalently: only `⟨U, D, R², L²,
F², B²⟩` moves are needed from here on. This is the "domino" subgroup
because the cube reduces to a 2-layer puzzle.

`|EO_UD : DR_UD| = 2^7 · 3^7 / something` — computed as 256 corner-CO
states times some edge constraint. We don't need the exact index because
we use the **DR-group action** directly as a search alphabet.

## HTR: half-turn reduction

The most algebraically rich stage.

**HTR group** = `⟨U², D², R², L², F², B²⟩`. Generated by 6 half-turns. Has
exactly **663,552 elements**. Diameter (worst case) = **15 half-turns**.
We've enumerated all of it via BFS from SOLVED and stored a parent-pointer
PDB:

```python
# cube/classifier/htr.py
def htr_pdb() -> dict[StateKey, (distance, parent_move)]:
    # multi-source BFS, 6 half-turn moves
    ...
```

`663,552 = 96 · 6912 = |HTR_corner| · |HTR_edge|`. Both factors are
themselves cosets of the symmetric/alternating groups.

### The 96 HTR corner classes

Half-turns act on corner permutations as a subgroup of `S_8` of order
96. (`A_8` would be order 20,160, so this is much smaller — half-turn
corner cycles are 2-cycles and pairs of 2-cycles, never 3-cycles or
4-cycles.) These 96 perms are the corner perms reachable from solved
via half-turns only.

### DR-corner-set ⊃ HTR-corner-set

The DR group `⟨U, D, R², L², F², B²⟩` acting on corners reaches the
**full S_8 = 40,320**. (Not A_8 — U/D quarters generate odd cycles in
combination with half-turn 2-cycles.)

So we have a coset structure:
```
DR_corner_perms (40320)
  ⊇  HTR_corner_perms (96)
```

Index `[DR : HTR] = 40,320 / 96 = 420` corner cosets.

These 420 cosets are what the FMC community calls "subsets" — `4a1`,
`4b2`, `2c3`, etc. Each subset has a known approximate HTR-completion
length.

### Pattern databases

Two PDBs, each built by reverse BFS:

1. **Corner→HTR distance**: 40,320 entries, diameter 11. Reverse BFS from
   the 96 HTR corner perms (multi-source), expanding via DR-group moves.
   Lookup is O(1) by cp tuple.

2. **Edge→HTR distance**: 967,680 entries (8! · 6 = 967680 actually no:
   it's the orbit under DR-group of solved edge perm), diameter 7. Same
   reverse-BFS construction.

The admissible heuristic for A\* DR→HTR is:

```
h(s) = max( corner_dist[s.cp], edge_dist[s.ep_signature] )
```

(Max of two PDBs is admissible because every move advances by at most
one in either; one PDB always lower-bounds; max preserves admissibility.)

This h is **tight enough that pure A\* finds DR→HTR in <0.1s** on every
scramble we've tested. The transformer policy adds no value here.

### Left vs right cosets: a subtle bug we caught

A natural conjecture: distance-to-HTR is constant on each "HTR coset" of
DR. But which coset — left `Hπ` or right `πH`?

The Cayley graph with **right**-multiplication generators is
**right**-translation invariant: `d(πg, Hg) = d(π, H)` for any `g ∈ G`.
This means distance depends only on the **LEFT** coset `Hπ`. We
initially wrote the test assuming right cosets and got failures — fixed
by switching to left cosets and the invariant holds for all 420 cosets:

```python
# tests/classifier/test_htr.py::test_distance_constant_within_left_coset
for canonical, distances in by_coset.items():
    assert len(distances) == 1
```

The FMC community's "subset" labeling is actually the **right** coset
`πH` (which states are reachable from `π` via HTR moves) — this cuts
across distance classes. We use per-cp distance for ranking;
right-coset partition is for naming.

## The leave-slice idea

After HTR, you finish with half-turns only (`htr_solve` looks up the
PDB and walks back). But the canonical FMC technique is **leave a
slice**: target a state with everything solved except the E-slice (4
middle edges), then patch the slice with one slice-quarter (`M`, `M'`,
or `M²`).

Group-theoretically: leave-slice-solved = `{cp = e, ep_{0..7} = e,
ep_{8..11} ∈ S_4 (constrained)}`. Multi-source BFS from these targets
gives a PDB whose distances are shorter than `htr_solve`'s — but the
slice fix adds 0–2 face moves, and the canonical `M = R' L` slice
approximation in pure face-turn notation **disturbs the U/D layers**.
True `M` slice as a 1-STM primitive would make this a clean win; in
pure face-turn metric, leave-slice's value is mostly in cancellation
opportunities with the surrounding skeleton.

The PDB is built (663,552 reachable states, diameter 12) and the
infrastructure is in place for the slice-primitive lift.

---

# The search pipeline

```
scramble ─► EO (beam, multi-axis)
            ├─► DR  (beam→trigger + DFS tail, multi-axis)
            │   └─► A* DR→HTR (pure heuristic, DR-group moves)
            │       └─► PDB finish (lookup)
            │
            └─► cancellation across all stage boundaries
```

**Multi-axis everything.** EO is tried on UD/FB/RL axes; the top 5 EO
candidates per axis are kept. Each EO seeds a DR search on the matching
axis. Best skeletons across axes are returned ranked by expected total.

**Trigger-based DR.** Direct DR search is too deep for beam. Instead we
beam-search to a "trigger state" — one that's within 2 moves of DR by
DFS — and then enumerate the short tail explicitly. This mirrors how
humans find DR (recognize a setup, complete the trigger).

**Cancellation.** Stage boundaries often have same-face moves on either
side (`U2 U` → `U'`). Through-commute is also handled (`U D U` → `D
U²`). The cancelled length is what gets ranked; raw length is reported
in parentheses.

**Skeleton ranking.**
1. Solved skeletons beat partial.
2. More stages beat fewer.
3. Lower `total_moves + htr_distance` (expected total length).
4. Lower `total_moves` (cancelled).
5. Higher policy log-prob.

---

# Running it

```bash
uv sync
uv run pytest                                        # 209 tests
uv run python -m cube.analyzer.skeleton_cli "SCRAMBLE..."
```

Optional flags: `--dr-beam`, `--dr-depth`, `--top`, `--device`.

# Repo layout

```
src/cube/
  engine/        State, moves, notation, facelet ↔ cubie, cancellation
  classifier/    rule-based EO/DR/HTR, PDBs, leave-slice scaffolding
  corpus/        parse/validate WCA reconstructions from 333.fm
  segmenter/     per-move phase labels
  training/      transformer policy, encoding, baselines
  analyzer/      EO → DR → HTR → Finish pipeline, beam/A* search
  cli.py
tests/           pytest, mirrors src layout
data/raw/        gitignored — JSONL corpus
data/cache/      gitignored — 333.fm API cache
checkpoints/     gitignored — model weights
```
