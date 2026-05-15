# Video script outline — "Can an LLM solve a Rubik's Cube as well as a human FMC champion?"

Working title. ~10-15 min target. Audience: 5k–50k coders / cubers / AI-curious viewers.

## Pitch

I gave Claude the same tools a strong FMC solver uses — a learned cube
intuition (a small transformer), a one-page commutator library, a notion of
HTR subsets you memorize. Then I built a simulator that forces the model to
play by competition rules: 1 hour, 3 cube "slots", 4-move undo buffer,
per-move time costs.

It can solve some scrambles. It can't solve others. The reasoning trace
is the show.

## Three-act structure

### Act 1 — The setup (3 min)
- Show the unconstrained mode first: 25-move solve on scramble 2 in 5
  minutes for $0.23. Looks magical.
- Reveal the cheating: `solve_htr_and_finish_from_dr` is A* + a 663,552-
  entry pattern database. `find_dr_via_trigger` at width=512 enumerates
  more setups than any human ever could.
- Pose the question: "If we make the tools honest, does the LLM still
  do FMC?"

### Act 2 — The build (5 min)
- The 14 tools of sim mode:
  - The honest ones (inspect_state, try_alg, apply_moves, cancel)
  - The intuition tool (policy_intuition — one forward pass of a 91k-
    param transformer, the agent's "trained eye")
  - The bounded search (lookahead w=10 d=5, find_dr_via_trigger w=32)
  - The memory tool (htr_subset + lookup_subset_finish, cached like a
    human's rehearsed library)
  - The state mgmt (slots, undo, NISS flip)
- The human limitations we baked in:
  - Inspection costs time (5s to count bad edges on the cube)
  - Subset recognition costs time (10s to name the HTR subset)
  - Working-memory cap: inspect_state only shows the last 20 moves
  - Top-3 trigger options (humans don't enumerate 5+ alternatives)
  - Per-subset memory_quality hint ("rehearsed" vs "rarely-seen")
- The FMC theory injection: 1200 words of strategic reference. RZP,
  JZP, ARM, DR-Xs, HTR subset names (4a1, 4b2, 2c3, 2c4...), insertion
  patterns. Plus an algorithmic EO procedure: per-axis flip moves,
  by-bad-edge-count guidance, slot-level reading.

### Act 3 — Running the experiment (6 min)
- Scramble 2 (the lucky one):
  - Unconstrained: 25 moves
  - Sim v6 (after fixes): 33 moves
  - The 8-move gap explained: shorter DR via wider beam in unconstrained
    cascades into a better HTR subset that allows cancellation
- Scrambles 1, 3, 5 (the hard ones):
  - Sim mode: timeout, no solve
  - Why: at sim-budget widths the 91k-param policy can't surface their
    short EOs. Even at w=50 d=7 they're invisible. NISS to inverse
    doesn't help.
  - This is the binding constraint: not the strategy, not the tools,
    not the time — the policy's intuition isn't sharp enough on hard
    scrambles. Mirror-aug retrain helped (val top1 0.26→0.28) but
    didn't close the gap.
- The honest closer: "The LLM, under realistic FMC constraints, with
  a learned intuition at champion-level training would do champion-
  level FMC. Our intuition is novice-level. The wedge is the policy."

## Key numbers to put on screen

| | Unconstrained | Sim mode (v6) | Sim mode (v4) | Sim mode (v1) |
|---|---:|---:|---:|---:|
| Scramble 2 result | 25 | 33 | 33 | TIMEOUT |
| Tool calls | 14 | 16-21 | 21 | 60 |
| Cost | $0.23 | ~$0.30 | ~$0.50 | $1.80 |
| Wall clock | 5 min | 5-8 min | 6 min | 3 min |

| Scramble | Unconstrained baseline | Sim mode best | Gap |
|---|---:|---:|---:|
| 1 | 30 | DNF | — |
| 2 | 25 | 33 | +8 |
| 3 | 31 | DNF | — |
| 5 | 33 | DNF | — |

| Iteration | Change | Solved | Notes |
|---|---|---:|---|
| v0 | Initial sim, tail=2, w=5 | 0/4 | DR-trigger fails at tail=2 |
| v3 | tail=3, w=5 | 1/4 | scramble 2 only |
| v5 | + probe_dr_after_eo + w=10 | 1/4 | strategy fixed but EO still policy-bound |
| v6 | + cancel | 1/4 | 33 vs 34 |
| v7 | + human-time costs | 1/4 | 33, cheaper |
| v8 | + FMC theory | 0/4 | perfectionism timeout |
| v9 | + SHIP RULE | 1/4 | scramble 2 back |
| v10 | + algorithmic EO | 1/4 | hard scrambles still timeout |
| v11 | + mirror-aug policy + prewarmed cache | TBD | the run we'll show |

## The talking points

1. **"Hold the LLM to human standards."** Most LLM-with-tools demos give
   the model an oracle and call the orchestration impressive. We don't.
   sim mode hides the brute-force tools and exposes only what a human
   has — intuition (the transformer), memorized vocabulary (the subset
   library), bounded look-ahead, and time pressure.

2. **"Watch the model reason."** Every run produces a turn-by-turn
   narrative with the model's own narration. Show 30 seconds of
   scramble 2 v6: the agent enumerating EOs on 3 axes, probing DR
   feasibility, recognizing that FB has no DR despite the shorter EO,
   committing to UD, looking up the subset finish, shipping.

3. **"It fails the right way."** Sonnet doesn't make absurd moves;
   it makes the moves a strong-but-not-champion human makes. The
   failure modes (axis-selection bias, getting stuck in manual DR
   exploration when the policy beam returns empty, occasionally
   forgetting to cancel) are recognizable.

4. **"The wedge is the policy, not the LLM."** This is what the
   data shows. The mirror-aug retrain bumped val top1 from 0.26 to
   0.29 — closing maybe 10% of the gap. To get champion-level we'd
   need either much more data (nissy oracle) or auxiliary signals
   (value head, multi-task losses).

5. **"What this is and isn't."** It's not a state-of-the-art solver
   (cubelib/mallard exist). It's not a tool people would use. It's
   a way to ask "what part of FMC is intuition and what part is
   search?" — and the answer is, more than you'd think, it's
   intuition.

## Material we have

- 4 scramble × ~8 sim runs each = 32 transcripts, all in runs/
- Per-turn token usage and cost
- Slot-history evolution captured per tool call
- INDEX.md dashboard
- Two side-by-side reasoning compares (Sonnet vs Opus on unconstrained,
  plus implicit comparisons across iterations)
- The 6 sim_*.md and sim_scramble2_*.md narrative writeups

## Material to capture if filming

- Screen recording of the unconstrained solve (the "magical" demo)
- Screen recording of the sim mode on scramble 2 (the realistic one)
- Screen recording of an attempted hard scramble where it gives up
- The corpus_eval SUMMARY.md being generated in real time
- The INDEX.md scrolling through 30+ runs
- The /thinking/ blocks rendered cleanly

## Cuts & B-roll ideas

- Tronto's nissy in the corner showing the optimal as ground truth
- A real cube on the desk for tactile illustration
- The 91k-param transformer training curve (val top1 going up with
  mirror aug)
- An ASCII diagram of the 96 HTR subsets
- The cost ticker rising in real time during a run
