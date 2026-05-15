# Simulated FMC — scramble 2, SOLVED (the narrative wedge)

Sonnet 4.5 on the same scramble. Two runs, one model, one toolset —
just different budgets.

| | Unconstrained `loop.py` | Simulated `simulated_fmc.py` |
|---|---:|---:|
| **Result** | 25 moves | **38 moves** |
| Tool calls | 14 | 42 |
| Real wall | 5 min | 8 min |
| Sim budget spent | n/a | 339 / 3600s |
| API cost | $0.23 | ~$1.50 |
| EO | 4 moves (UD axis) | 2 moves (FB axis) |
| DR setup | 7 moves | 14 moves |
| HTR finish | 15 moves (A* + 663,552-PDB) | 22 moves (cached lookup from non-canonical state) |
| DR-trigger budget | sw=512 sd=8 **tl=2** | sw=32 sd=8 **tl=3** |

**The wedge: 13 extra moves and 6.5× the cost** is what the LLM gives
up when we take away the parts of the tool surface that humans don't
have.

## The simulated solution

`U' R D2 B' L2 B U' B D' B D F2 D' R2 F D D2 F' D2 F' D2 R2 F' L2 B F2 D2 F2 D2 R2 B2 U2 L2 U2 F2 D2 F2 U2`

Verified.

## What the sim agent did differently

1. **Took the shorter EO** (2 moves on FB) instead of the unconstrained
   agent's smarter pick (4 moves on UD which led to a 7-move DR).
2. **Couldn't find DR via the policy beam** at sim budget — instead
   built a 14-move setup chain by alternating `try_alg`, `apply_moves`,
   `undo_moves`, and `policy_intuition`. This is what a human does on
   paper but it's expensive in tool calls.
3. **Got to a non-canonical DR** state. `lookup_subset_finish` had to
   walk DR → canonical HTR (~7 moves) → SOLVED via half-turns (~15
   moves) = 22 total. The unconstrained mode's `solve_htr_and_finish_from_dr`
   produced this same logical thing but reached canonical HTR via 7
   moves in a SHORTER way that happened to share moves with the EO/DR
   setup, so cancellation collapsed it to 15.

The "cheating tool" we removed wasn't actually solving HTR — it was
finding the SAME PDB walk but in a shape that allowed more
cancellation back into the solve setup. Subtle.

## The DR-trigger threshold finding (offline ablations)

Original assumption: `find_dr_via_trigger` at default `sw=512 sd=8
tail=2` finds a 7-move DR on scramble 2. The recorded transcript at
`runs/example_solve_scramble2.md` shows this.

At our current code state, this is **no longer true**. Empirical sweep
on the (scramble + EO `R B D' B`) state:

| setup_width | setup_depth | tail | found? | best_len |
|---:|---:|---:|---:|---:|
| 20 | 6 | 2 | ✗ | — |
| 64 | 8 | 2 | ✗ | — |
| 256 | 8 | 2 | ✗ | — |
| 512 | 8 | 2 | ✗ | — |
| 1024 | 8 | 2 | ✓ | 7 |
| 512 | 8 | **3** | ✓ | 7 |
| **32** | 6 | **3** | ✓ | 9 |
| 64 | 8 | 3 | ✓ | 9 |

The key inflection is `tail_length` more than `setup_width`. At tail=3,
even sw=32 surfaces a 9-move DR. The recorded transcript probably ran
under an older default of `tail_length=3`. Sim mode now defaults to
`tail=3, sw=32, sd=8`.

This is a finding worth surfacing in the video: **what looks like
"the agent picked a great DR" was partly the search budget doing the
work**. When we expose the search budget to honest accounting, the
agent's chosen DR gets longer, the cancellations get worse, the
finish gets longer — all the gains were partly procedural.

## Sim time budget spend (339s of 3600)

The agent had 91% of its competition time unused. Tool-call cap of 60
hit at 42 so plenty of headroom there too. The binding constraint is
**search budget** (would the trigger fire) and **agent strategy**
(commit to short-EO on FB vs longer-EO on UD which led to better DR).
Time / API quota are not the bottleneck at this scramble.

## Open questions

- Would Opus pick the UD-axis line that gives the shorter total?
  Worth a single Opus run on this same scramble.
- Does pre-warming `_SUBSET_FINISH_CACHE` from a corpus of unconstrained
  runs change the picture (cache hits at 1s instead of 15s "learn")?
- Is the "tail=3 vs tail=2" finding scramble-dependent? Want a 5-10
  scramble sweep at tail=2 vs 3 to know.

## Stats per phase (sim mode)

| Phase | Sim seconds spent | Wall seconds (real) |
|---|---:|---:|
| Tool calls 1-4 (EO scan + commit) | 47 | ~120 |
| Tool calls 5-15 (failed DR searches, tried NISS, reset) | 162 | ~150 |
| Tool calls 16-36 (manual DR build) | 90 | ~120 |
| Tool calls 37-42 (HTR + verify) | 40 | ~80 |
| **Total** | **339** | **468** |
