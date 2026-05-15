# Agent run status — end of work day 1

## TL;DR

- **The agent works.** Scramble 2 → 25 moves, $0.23, 14 tool calls. Real
  FMC reasoning (multi-axis EO scan, abandoned 2-move EO when DR
  wouldn't fire, used trigger-based DR, used the memorized-finish tool).
- **It's brittle on harder scrambles.** Out of 5 attempted, 1 clean
  solve, 1 trivial (degenerate invert-scramble), 3 timeouts.
- **Total cost so far: ~$60 of $100.**

## Runs

| # | Scramble | Model | Result | Moves | Cost | Notes |
|---|---|---|---|---|---|---|
| 1 | 2 | Sonnet 4.5 | timeout | — | $1 | First run: lookahead depth=5 caps DR |
| 2 | 2 | Sonnet 4.5 | timeout | — | $5 | Iterative-search prompt, still depth-bound |
| 3 | 2 | Sonnet 4.5 | crash | — | $0 | API key env not in subshell |
| 4 | 2 | Sonnet 4.5 | crash | — | $0 | Sonnet dropped last 3 scramble moves |
| 5 | 2 | Sonnet 4.5 | partial | — | $5 | Got to DR but no HTR-finish tool yet |
| **6** | **2** | **Sonnet 4.5** | **✓** | **25** | **$0.23** | **Clean solve — the demo** |
| 7 | 1 | Sonnet 4.5 | ✗ trivial | 25 | $0.21 | Used invert(scramble); prompt now disallows |
| 8 | 3 | Sonnet 4.5 | timeout | 34 interim | $10 | Searched for shorter; ran out of wall |
| 9 | 1 | Sonnet 4.5 | timeout | — | $8 | Found 6-move EO (matches analyzer); died at DR |
| 10 | 2 | Opus 4.5 | timeout | — | $10 | Stuck on default DR width; now fixed |
| 11 | 1 | Sonnet 4.5 | timeout | — | $15 | 60 tool calls, multiple EO paths explored |
| 12 | corpus #5 | Sonnet 4.5 | timeout | — | $10 | Policy can't find DR trigger on this state |

## What went well

- **The 11-tool surface is the right abstraction**: state inspection,
  policy intuition, lookahead, trigger-DR search, HTR+Finish, cancel,
  NISS, verify, library lookups. The agent uses them coherently.
- **Sonnet 4.5 reasons like an FMC solver**: it explicitly enumerates
  axes, rejects shorter EOs when DR doesn't follow, recognizes the
  pipeline structure (EO → DR → HTR → finish).
- **The successful transcript (scramble 2) reads cleanly** — it's the
  video.

## What went wrong

1. **Iterative debugging burned the most cost**: scramble-as-JSON fix,
   HTR+Finish tool addition, width default fix all required full reruns.
2. **The policy is too weak** for some scrambles at width=512. The
   analyzer needed width=8192. We compromised at 512 to stay "human-ish."
3. **Sonnet vs Opus**: Opus is more methodical (explores more axes) but
   also more cautious — fewer commits per turn. Sonnet's higher-throughput
   exploration won on the easy case.
4. **Wall timeouts are the binding constraint**: 25 min isn't always
   enough for 30+ tool calls. Each Anthropic API turn takes ~30s.

## Next-session priorities

1. **Make scramble 2 reproducible**: it solved once but iterating prompts
   may have broken consistency. Run 3-5 times to confirm.
2. **Investigate scramble 1's hard normal-side DR**: the agent finds the
   right 6-move EO but can't bridge to DR. Tool gap or policy gap.
3. **Try harder scrambles with NISS more aggressively**: scramble 5's
   policy gap might be helped by explicit `find_dr_via_trigger(axis=X,
   setup_width=1024)` retries in the prompt.
4. **Record the working scramble 2 transcript for the video** — that's
   the visible artifact.

## API spend tracking

Spent: ~$60/$100. Remaining: ~$40.
Per-run cost ranges: $0.20 (clean Sonnet solve) to $15 (failed long
exploration). The clean solve is dirt cheap; failures are expensive.

## Files

- `runs/example_solve_scramble2.md` — the working transcript
- `runs/sim_design.md` — realistic-FMC simulation design + how to run
- `AGENT.md` — design doc + live results
- `src/cube/tools/` — 11 tools (unconstrained)
- `src/cube/agent/loop.py` — Anthropic API loop (unconstrained)
- `src/cube/agent/simulated_fmc.py` — budget-constrained loop, 14 tools
  with simulated-time accounting, 3 slots, 4-move undo, memoized HTR
  subset finish
- `runs/*.json` — raw transcripts (gitignored)

## Sim mode results so far (scramble 2)

| Run | Lookahead w | DR sw/tl | Probe | Cancel | Result | Moves | Cost |
|---|---|---|---|---|---|---|---|
| v0 initial | 5 | 20 / 2 | no | no | timeout | 0 | $1.80 |
| v1 sweep | 5 | 64 / 2 | no | no | timeout | 0 | $1.50 |
| v2 sweep | 5 | 256 / 2 | no | no | timeout | 0 | $1.50 |
| v3 1st solve | 5 | 32 / 3 | no | no | ✓ | 38 | $1.50 |
| v5 probe+w=10 | 10 | 32 / 3 | yes | no | ✓ | 34 | $0.30 |
| **v6 +cancel** | 10 | 32 / 3 | yes | yes | ✓ | **33** | $0.50 |
| Unconstrained | 20 | 512 / 2 | (n/a) | yes | ✓ | 25 | $0.23 |

The realistic-FMC mode now solves scramble 2 reliably in ~33 moves
under honest budgets. The 8-move gap to the unconstrained baseline is
*entirely* policy-quality: sim finds a 9-move DR where unconstrained
finds 7, which cascades to a 6-move-worse HTR finish.

The biggest single fix was `probe_dr_after_eo`, a hypothesis-test
tool that lets the agent ask "if I commit this EO, can DR be found?"
without paying for the commitment. The unconstrained agent didn't
need it because at w=512 the trigger search's fast-fail was an
implicit probe; at sim w=32 the signal is noisier and the explicit
probe is needed.
