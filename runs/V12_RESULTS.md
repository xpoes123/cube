# v12 corpus eval — closeness heuristics + DR triggers + NISS-first

The "champion's view" version of the agent. v11 forced 4-move recall but
still let the agent see only counts (bad_edges_per_axis). v12 surfaces
the structured FMC-vocabulary heuristics — DR-XCYE labels, JZP flag,
pairs-on-inverse, qt_corners — that real WCA champions actually read
off the cube.

Grounded in two research subagents that read the project's Hitchhiker's
Guide to FMC + Hitchhiker's Guide to DR + DR-Xs docs and quoted them
directly.

## TL;DR

**5/5 solved on the same 5 WCA scrambles, avg 29.4 vs human 20.8, gap +8.6**
vs v11's +9.4. WesternSicily dropped 4 moves (32 → 28). $0.75 total.

The narration texture is now genuinely FMC-champion-shaped:
> *"UD axis: 8 bad edges (all-bad case), DR-6C3E, 2 pairs on inverse.
> The 8-bad UD case typically needs a NISS approach. Let me check the
> inverse side since there were 2 pairs preserved."*

## Per-scramble vs v11

| Scramble | v12 | v11 | Human | v12 vs human | Δ vs v11 |
|---|---:|---:|---:|---:|---:|
| PSSSideDayGdansk2026 s1 | 30 | 31 | 20 | +10 | −1 |
| PSSSideDayGdansk2026 s2 | 30 | 30 | 20 | +10 | 0 |
| PSSSideDayGdansk2026 s3 | 27 | 27 | 23 | +4 | 0 |
| BackiPetrovacOpen2026 s1 | 32 | 31 | 22 | +10 | +1 |
| WesternSicilyOpen2026 s1 | **28** | 32 | 19 | **+9** | **−4** |

Avg 29.4 (was 30.2). Best gap (s3): +4 — within striking distance of champion.

## What v12 added

### inspect_state heuristic block

For each axis, the LLM now sees:
- `misoriented_corners` ("C") and `misplaced_slice_edges` ("E"): the DR-XCYE
  label champions recite
- `jzp_eligible` (UD): boolean — JZP states have dramatically shorter DR
- `top_pairs_on_inverse` (UD): Wen's pairs-tracing count
- `arm_other_axis`: ARM (Axial Reduction Minus) signal for post-NISS axis
- `qt_corners` (post-DR): primary HTR-distance signal (0-5)
- `solved_corner_columns`: floppy-reduction signal
- `solved_corners_count`, `solved_edges_count`: progress tracking

These are COUNTS AND LABELS, never exact distances. The agent applies
probabilistic FMC reasoning instead of being handed "DR is 7 moves away."

### `dr_trigger_options` tool

For an EO-solved state on UD axis, returns a ranked menu of NAMED
trigger families (DR-4C4E "R", DR-3C2E "R U R'", DR-4C2E "R U2 R'",
DR-7C8E "R U L", etc.) with setup_moves, total_to_dr, jzp_eligible,
top_pairs_on_inverse per option.

Ranking: shortest total → JZP-eligible first → family preference
(4C4E > 3C2E > 4C2E > 7C8E). Implemented via reduced-state BFS in
(co_tuple, slice_marker) space (the same faithful quotient used by the
DR library), so max_setup=5 finds ~10 options in 2 seconds.

The LLM picks by FAMILY and FLAG, not by raw moves:
> "I'll take the R-U2-R' DR-4C2E option because it's JZP-eligible with
> a clean 3-move setup."

### NISS-FIRST prompt rule

After the initial EO scan, the agent ALWAYS checks the inverse frame.
Pairs_on_inverse ≥ 2 OR EO ≥1 move shorter on inverse → use inverse.
This converted NISS from "occasionally tried" to "default first check."

In the v12 PSSS_s1 transcript, the agent used `niss_flip` 2× to compare
frames, exactly as Hitchhiker DR §pairs prescribes.

## What this proves about LLM-FMC

The agent IS doing real FMC reasoning when given proper vocabulary:
1. It NAMES what it sees ("DR-6C3E", "2 pairs on inverse", "4-swap axial subset")
2. It WEIGHS options by structural flag (JZP) AND total length
3. It SWITCHES frames when the heuristics say so (NISS)
4. It NARRATES the technique it's applying

The remaining +8.6 gap to WCA champions is the **skeleton+insertion**
gap. Every elite WCA solver in the transcripts (Levi Gibson, Marcin
Chmielewski, Alexandros Volkanos, Cyprian Kalbacik, etc.) finds an
intermediate "skeleton" leaving 3 corners or 2e2e unsolved, then
finds a commutator insertion that cancels heavily with surrounding
moves — saving 5-8 moves. The agent doesn't have skeleton+insertion
tools yet. That's v13.

## File map

- `src/cube/classifier/dr_heuristics.py` — all the new heuristic functions
- `src/cube/tools/dr_trigger_options.py` — the trigger-menu tool
- `src/cube/tools/state.py` — inspect_state enrichment
- `data/hitchhiker_fmc.txt`, `data/hitchhiker_dr.txt`, `data/drxs.txt` — the
  source docs the heuristics were derived from

## Cost summary

Session total so far: ~$76.50 of $100 budget. v12 cost $0.75 for 5
scrambles. About 35-50 tool calls per scramble.

## Next: v13 — skeletons + insertions

The +8.6 gap is almost entirely the skeleton+insertion technique.
Concrete v13:
1. `find_skeleton(target_leftover)` — search for skeletons leaving 3c,
   3c1t, 2e2e — the typical insertion targets
2. `find_insertion(skeleton, slot_index, comm_template)` — for a given
   skeleton, search positions and commutators with high cancellation
3. The LLM picks the skeleton target and ranks insertion candidates
4. Multi-NISS workflow (Levi Gibson does 3-4 NISS switches per WR solve)
5. N-tracing tool (predict post-NISS state without committing)

Expected impact: drop avg from 29.4 → 23-25. Brings the agent into
"strong human FMC competitor" range.
