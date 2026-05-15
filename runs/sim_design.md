# Realistic-FMC simulation mode

`src/cube/agent/simulated_fmc.py` is the budget-constrained sibling of
`loop.py`. It exists to answer the harder version of the video's question:
not "can an LLM orchestrate our analyzer," but "can an LLM do FMC under
the constraints a human actually faces."

## Constraints

| Constraint | Value | Why |
|---|---|---|
| Total time | 3600s simulated (real-wall cap ≤ 1hr) | WCA FMC regulation |
| Cube-state slots | 3 named | Approximates "I can hold a few alternative lines in my head" |
| Undo per slot | 4 moves | Deeper rewinds cost a full rescramble (30s simulated) |
| Per-move cost | 1s | Twisting a paper cube |
| `lookahead` budget | width=5, depth=4 | Human visualization budget |
| `find_dr_via_trigger` budget | setup_width=20, setup_depth=6 | Tighter than the analyzer's 512 |
| HTR finish | `lookup_subset_finish` (memoized) | Humans memorize ~96 subset finishes, not the 663,552-entry PDB |

## Tool surface (14 tools)

State manipulation:
- `inspect_state(slot)`, `apply_moves(slot, moves)`, `undo_moves(slot, n)`,
  `reset_slot(slot)`, `new_slot(name, copy_from)`, `niss_flip(slot)`
- `try_alg(slot, alg)` — preview without committing.

Search/intuition (budget-tightened):
- `policy_intuition(slot, k)` — single forward pass of the 91k-param policy.
- `lookahead(slot, target, axis)` — beam at w=5 d=4.
- `find_dr_via_trigger(slot, axis)` — trigger-then-tail at sw=20 sd=6.

HTR endgame (memoization model):
- `htr_subset(slot)` — name the subset (canonical-form cp).
- `lookup_subset_finish(slot, axis)` — recall the rehearsed finish. First
  time costs 15s ("learning"); after that, 1s ("memorized").

Meta:
- `verify_solved(solution)` — free.
- `budget_status()` — free.

## Time accounting model

Costs are **simulated** competition seconds, not real CPU. The wall clock
is a separate cap (also 1 hr by default) to bound API spend.

```
apply_moves: 1s per move
undo_moves: 1s per move (then deeper rewinds cost a reset)
reset_slot: 30s (solve + rescramble on paper)
new_slot: 10s
niss_flip: 5s
inspect_state: 1s
try_alg: 2s
policy_intuition: 3s
lookahead: 8s
find_dr_via_trigger: 20s
htr_subset: 2s
lookup_subset_finish: 15s (miss) / 1s (cached)
verify_solved: 0s
budget_status: 0s
```

## The subset-finish library

This is the cheating-killer. In `loop.py`, `solve_htr_and_finish_from_dr`
is A* + the 663,552-entry HTR PDB — pure brute force. Humans don't have
that. They have ~96 named subset finishes memorized.

In sim mode, `lookup_subset_finish(slot, axis)`:
1. Computes the canonical HTR-corner-subset via `dr_subset_canonical`.
2. Checks the module-level `_SUBSET_FINISH_CACHE`.
3. **Cache hit** → recalls the finish in 1s. ("I know this one.")
4. **Cache miss** → derives via the existing PDB but charges 15s. ("First
   time seeing this — I learned the finish, will remember it.")

After enough runs, the cache should converge toward the human library
size (~96 entries). The miss cost is a soft simulation of the years of
study, not the milliseconds of computation.

## What we expect to see

The unconstrained `loop.py` solves scramble 2 in 25 moves, 14 tool calls,
$0.23, 5 min wall. The sim version should:

- Probably solve scramble 2 within budget (it's the "easy" demo case
  and the tools mirror the human pipeline).
- Spend simulated time roughly: ~25s applied moves + 8-20s per
  lookahead/DR search × ~5 calls + 15s subset learn + cheap finish
  application = ~200-300s out of 3600. Plenty of headroom.
- Fail more often on harder scrambles. That's the point — that's where
  the narrative lives.

## How to run

```fish
set -x ANTHROPIC_API_KEY ...    # provide the key
uv run python -m cube.agent.simulated_fmc \
  "R' U' F B' U2 F' U2 R2 B' R2 B' R2 U2 R2 F' L U2 B D R F L2 F D' R' U' F" \
  --verbose --thinking-budget 3000 --wall-limit-s 1200
```

Output goes to `runs/sim_<timestamp>.json` with the full transcript and
the budget event trace. Distill interesting runs into `runs/sim_*.md`
markdown like we do for the unconstrained mode.

## What this does NOT do (yet)

- No "scrambled state recoverability" cost — in real FMC, after a NISS
  the agent has to re-solve to inverse on paper. We model this with
  niss_flip = 5s, but a real solver pays more like 20-30s.
- The `_SUBSET_FINISH_CACHE` is per-process — wiped between runs. A real
  human's library persists. We could pre-seed the cache for a "trained
  human" baseline vs leave it empty for a "novice" baseline.
- The 91k-param policy is the same in both modes. The realistic version
  should arguably use a worse policy (less seen data) to approximate
  "the LLM hasn't memorized as many shapes as a human champion." Open
  question: does this matter, or does the wider unconstrained policy
  already lose enough to budget caps?
