# Overnight progress (2026-05-15) — FINAL

Worked while you slept. v7 finished cleanly.

## Headline: 5/10 SOLVED 🎉

**v7 (the headline experiment) finished at 5/10 solved.** Up from v6's
1/10. The combination of BFS escape hatch + prompt caching turned the
project from "demo on scramble 2 only" to "solves half of random WCA
scrambles." See [FINAL_RESULTS.md](FINAL_RESULTS.md) for the full
writeup.

## Headline (old)

- **Mirror-aug retrain shipped**: val top1 0.261 → **0.285** (+9.3%),
  test top5 0.635 → **0.668** (+5.2%). Old checkpoint backed up to
  `checkpoints/policy_best_pre_mirror.pt`.
- **Algorithmic EO theory** in the prompt: explicit per-axis flipping-
  move map, by-bad-edge-count procedure, slot-level reading. Plus
  `inspect_state` now returns `bad_edge_slots_per_axis` so the agent
  sees WHICH edges are bad, not just how many.
- **Comprehensive logging upgrade**: every run now captures per-turn
  input/output/cache tokens, API wall time, slot snapshot after each
  tool call, cost estimate with cache discount. Plus `runs/INDEX.md`
  auto-rebuilt after every corpus eval — dashboard of every run with
  links to JSON + narrative.
- **3 new tools/utilities**:
  - `cube.agent.scramble_gen` — deterministic WCA-style scramble
    generator (used by corpus_eval `--extra-random N`).
  - `cube.agent.prewarm_subsets` — offline computation of canonical
    HTR finishes, pickled to `checkpoints/subset_finish_cache.pkl`.
    Sim mode loads on import. 60 of 420 subsets covered.
  - `cube.agent.compare_runs` — side-by-side diff of two transcripts
    for the video.
- **v4 (ship rule) result**: 1/4 (scramble 2 at 33 moves). Theory was
  injected in v3 and caused the agent to abandon working 34-move
  solutions to chase 25-move ones — perfectionism timeout. SHIP RULE
  fixed it.
- **v5 (algorithmic EO)**: in progress as of writing. Scramble 1
  failed, scramble 2 ✓ 33 moves, scrambles 3 + 5 to come.
- **v6 (10 scrambles, mirror-aug policy, prewarmed cache)**: just
  kicked off. The headline experiment. Will report when done.

## What I didn't touch

- **nissy/mallard integration** — explicit user said "potentially
  eventually." Memory note saved at `project_nissy_mallard_training.md`
  in your auto-memory. Auto-mode classifier blocks untrusted-tool
  install without your confirmation.
- **Random-scramble pretraining** — would take 8+ hours of analyzer
  CPU per the existing speed. Tagged in memory; suitable for
  another session.
- **Larger model retrain** — mirror-aug closed enough of the gap
  that this is no longer the top priority. Will revisit if v6
  doesn't show gains.
- **Noisy memorization via genuine PDB-suboptimal walks** — naive
  cancellable padding doesn't work (cancel undoes it). Real
  implementation needs A* with perturbed heuristic; deferred.

## File map (new this session)

```
src/cube/agent/
├── simulated_fmc.py     UPGRADED (per-turn logging, bad-edge slots in inspect, algorithmic EO prompt, ship rule, FMC theory, cache loader)
├── render_narrative.py  UPGRADED (sim-time-by-tool, per-turn $, slot history inline)
├── corpus_eval.py       UPGRADED (--extra-random N, auto INDEX regen)
├── build_index.py       NEW
├── scramble_gen.py      NEW
├── prewarm_subsets.py   NEW
└── compare_runs.py      NEW

src/cube/tools/state.py  inspect_state now returns bad_edge_slots_per_axis

runs/
├── INDEX.md             NEW — dashboard of every transcript
├── VIDEO_SCRIPT.md      NEW — 10-15 min video outline (3-act)
├── MORNING_REPORT.md    NEW — this doc
├── corpus_eval_v2/      v1 + HTR-prompt-fix       1/4
├── corpus_eval_v3_theory/ +FMC theory             0/4 (perfectionism!)
├── corpus_eval_v4_ship/ +SHIP RULE                1/4 (scramble 2 back)
├── corpus_eval_v5_algoEO/ +algorithmic EO         in progress
└── corpus_eval_v6_full/   +mirror policy +10scr   in progress

checkpoints/
├── policy_best.pt            mirror-aug retrained
├── policy_best_pre_mirror.pt backup of pre-retrain
└── subset_finish_cache.pkl   60 HTR-subset finishes (will grow with runs)
```

## Key empirical findings (for the video)

1. **Scramble 2 is the lucky one**. Its 4-move UD EO is policy-findable;
   1/3/5 aren't even at lookahead w=50 d=7. The policy is the binding
   constraint, not the strategy or tools.

2. **Theory in the prompt is a double-edged sword**. Without "SHIP RULE",
   the FMC-theory injection made the agent perfectionist — it found
   working solutions and threw them away to chase shorter ones. Theory
   tells the model what's *possible*; the SHIP RULE tells it what's
   *enough for today*.

3. **Probe before commit was the biggest single fix**. Adding
   `probe_dr_after_eo` (test "would this EO lead to DR?" without
   committing) collapsed scramble 2's solve from 38 moves down to 34.
   Most of the gap to unconstrained closed at this step.

4. **Mirror-aug retrain**: validated 9% policy improvement. Expected
   to give the same EO-findability gain on scrambles 1/3/5 (TBD when
   v6 finishes).

5. **The 8-move sim-vs-unconstrained gap on scramble 2** decomposes:
   - 2 moves: longer DR (sim 9 vs unconstrained 7) because sw=32 vs 512
   - 6 moves: longer HTR finish because the worse DR lands in a worse
     subset that doesn't cancel against setup

## Cost ticker

Roughly **$30 of $100** spent through this session.
v5 + v6 will add ~$15 more. Plenty of headroom.

## Open / next session

- Land genuine noisy-memorization (suboptimal-PDB-walk).
- Pre-warm with the actually-encountered subsets (post-v6).
- Try Opus on the 4 hand-picked scrambles + 1-2 random.
- Random-scramble pretraining via the analyzer's own pipeline (~8hr).
- nissy oracle integration (when you authorize it).
- Possibly add `random_setup` tool for the EO-not-findable case — let
  the agent try 1-2 random setup moves followed by EO re-scan, the
  realistic "let me just try something" fallback humans use when their
  intuition fails.
