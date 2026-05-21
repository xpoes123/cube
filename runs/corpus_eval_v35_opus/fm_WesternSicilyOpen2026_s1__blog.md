# fm_WesternSicilyOpen2026_s1 — Retrospective

**Scramble:** `R' U' F U2 F2 D2 B2 D B' U L' B' F2 R2 U' L2 F2 B2 D' F2 L2 F R' U' F`

- **Submitted:** 34 moves
- **WCA reference (Marcucci):** 19 moves
- **Nissy axis-locked (UD):** 33 moves

The 15-move gap to Marcucci is almost entirely about phase structure: she solved this with a 2-move EO and a 7-move DR-4a1 leaving a 10-move skeleton that finished in `L · U2 F2 U2` — i.e. she essentially skipped HTR and did a direct 2c3+2e finish out of DR. I committed to a full EO→DR→HTR→finish pipeline on the RL axis and paid the full nissy-ceiling tax plus one extra move for a sub-optimal HTR subset.

---

## Initial scout

`inspect_state` returned bad-edge counts UD=4, FB=6, RL=4. FB was immediately out — 6 bad edges almost never gives a sub-5 EO. The cheap candidates were:

- **UD-EO normal:** `D R U2 F'` (4)
- **RL-EO normal:** `U2 F2 R D'` (4)

I noted I should NISS-check both, because FB=6 on normal often means the inverse has very low bad-edge counts on the cheap axes — which turned out to be the key observation, just not on the draft I scouted it on.

---

## Draft 1 — SOLVED in 34, 279s, 82 tool calls

**Phase decomposition (final, inverse-frame composition):**

- EO (2): `R2 D'` — RL axis, inverse
- DR setup (12): `U2 L U2 B · B' L' F2 L B · F U2 R2 D2 B` — three chunks through 2C1E → 0C1E → DR-RL, with the `B · B'` cancelling at the chunk boundary giving the effective `U2 L U2 L' F2 L B F U2 R2 D2 B`
- HTR reduction (9): `U2 R' U2 R' D2 R2 U2 F2 L` — 2-swap long-cycle subset
- Finish (11): `U2 R2 U2 F2 R2 B2 U2 B2 U2 F2 R2`

Total 34.

**What I was thinking.** I started normal-side on UD because both UD and RL had identical 4-move EOs and `eo_pattern_lookup` returned `D R U2 F'` immediately. After committing, `dr_progress_options` showed best 2C1E in 4. I picked `U2 R U R'` (2C1E) and then `D2 L' U' L` (2C0E), and then ran into the classic 2C0E corner-twist well — no DR within depth-4 EO-preserving moves, and depth-5 didn't reach either.

I tried the brain hint sequence (`U' R'`) which broke EO and forced a 2-move rewind, then `U' R2 D` got me to UD=0/FB=0/RL=2 but DR was still 2 twists short. At that point I NISS-checked: the inverse showed UD-EO=2 (`L' F'`) and RL-EO=2 (`R2 D'`). That was the moment I knew the branch was dead. I tried three known 2C0E-fix algs (`R2 U2 R' F2 R U2 R' F2 R'` and friends) — all 7+ extra moves. Reset to scramble.

Fresh start, inverse side. `R2 D'` was the obvious commit: 2-move RL-EO landing at DR-4C2E with cross-axis ARM showing C=3,E=3. Probed `U R2 U2 R2` and `U2 L U2 B`, picked the latter for 2C1E. Then `B' L' F2 L B` to 0C1E (one slice edge off, the `B · B'` boundary cancels into the previous chunk), then `F U2 R2 D2 B` finished DR-RL at 14 inverse moves.

`recognize_htr_subset` returned **2-swap long-cycle** — heavy 20-move tail (9 reduction + 11 finish). No 3-cycle residual available for insertion. I ran the canonical chunked reduction/finish, hit 34, and the mandatory `replace_and_shorten` micro-scramble for span [4:34] failed to find a DR — cap hit, submitted.

**Where this draft leaked.** Nowhere catastrophic vs the nissy UD-ceiling, actually — this draft beats nissy's 33 only if you grant the inverse-axis swap; on its own terms it's 1 move over the RL-equivalent nissy ceiling, lost in the 9-move HTR reduction (an optimal 2-swap long-cycle subset on this state is 8). The first half of the draft (40+ tool calls burned on the normal-UD dead end) was sim-time waste but didn't affect the submitted length.

---

## Draft 2 — SOLVED in 34, 116s, 36 tool calls

This is the same solution as draft 1. Identical move list, identical phase decomposition. The only difference is I had the prior draft's reconnaissance as input, so I went **straight to NISS-check** rather than burning 40 calls on the UD-normal dead end.

The structure:

- EO (2): `R2 D'` (inverse, RL)
- DR (12): `U2 L U2 L' F2 L B F U2 R2 D2 B`
- HTR reduction (9): `U2 R' U2 R' D2 R2 U2 F2 L`
- Finish (11): `U2 R2 U2 F2 R2 B2 U2 B2 U2 F2 R2`

I noted the chunked apply pattern hit the same `quick_check`-confirmed HTR state at move 23, then the 11-move finish. Same `replace_and_shorten` failure on span [4:34]. Submitted identically.

**Why both drafts converged.** Once you commit to RL-axis EO `R2 D'` and the DR-4a1-style path through `U2 L U2 B`, the DR completion essentially has one efficient route at the 2C1E → 0C1E → DR ladder, and the 2-swap long-cycle HTR subset is forced from there. There was no daylight between drafts because there was no alternative DR-finish to find without dropping back to a different 2C1E candidate at move 6.

---

## Draft 3 — FAILED, 106s, 33 tool calls

No narrative captured. 33 tool calls in 106s suggests an early-phase exploration that didn't reach a finish before the time/call envelope closed. Doesn't affect submission.

---

## Winning-draft analysis

Walking the submitted 34-move solution as a normal-frame sequence:

`R2 F2 U2 B2 U2 B2 R2 F2 U2 R2 U2` (11) `L' F2 U2 R2 D2 R U2 R U2` (9) `B' D2 R2 U2 F'` (5) `B' L' F2 L U2 L' U2 D R2` (9)

Reading it correctly, though, requires the inverse frame in which it was built:

- **Inverse EO (2):** `R2 D'`. The two cheapest EO axes on the inverse were UD-EO=`L' F'` and RL-EO=`R2 D'`. Both 2 moves. I picked RL because `try_alg` showed it landed at DR-4C2E with a 3C3E cross-axis ARM, vs UD-EO which I didn't fully probe but whose DR cost looked comparable. In hindsight `L' F'` would have been worth a parallel probe — but the savings are likely in HTR-subset roulette, not in DR length, and I had no reason to expect a better subset.
- **Inverse DR (12):** `U2 L U2 B B' L' F2 L B F U2 R2 D2 B` reducing to `U2 L U2 L' F2 L B F U2 R2 D2 B` after the obvious `B B'` cancellation. The three sub-phases were 4+5+5 = 14 raw moves, becoming 12 after cancellation. The alternative DR I shortlisted was `U R2 U2 R2`-prefixed, which `try_alg` showed leaving 2C2E rather than 2C1E — worse, rejected.
- **HTR reduction (9):** `U2 R' U2 R' · D2 R2 U2 F2 · L`. The 2-swap long-cycle subset is one of the heavier substates; nissy on the equivalent state gives an 8-move optimum, so I leaked exactly 1 move here. The chunked apply pattern (4+4+1) makes that leak likely — a single-shot DR-to-HTR query would have caught it.
- **Finish (11):** `U2 R2 U2 F2 · R2 B2 U2 B2 · U2 F2 R2`. Matches nissy's 11-move finish ceiling exactly.

Cancellation savings totalled exactly the one `B B'` boundary in the DR chunking. No inter-phase cancellations between DR→HTR or HTR→finish.

---

## Three-way comparison

### vs Marcucci (19)

Marcucci's commentary is the lesson here. Her decomposition:

- `(L' F')` — EO inverse UD (2/2). **Same starting EO axis I rejected** in favour of RL on the inverse.
- `(L' D' R L2 D' R2 D)` — DR 4a1 (7/9). On UD, the same axis I'd dismissed at the probe stage.
- `L' (L2 U2 F2 L' F2 L)` — HTR (7/16). This is the critical move — she did a 1-move normal + 6-move inverse HTR using a direct 2c3+2e skeleton, not a generic HTR-subset reduction.
- `(U2 F2 U2)` — 3-move finish.

She won 15 moves on three fronts: (a) UD-inverse EO over RL-inverse EO put her into a much friendlier DR substate (the post-DR cube was clearly close to a 2c3+2e residual); (b) she stopped the pipeline at DR and did a direct skeleton solve instead of forcing through HTR-subset machinery, saving the 9-move reduction entirely; (c) her finish was 3 moves vs my 11 because the skeleton landed in a 3-move-finishable state.

The thing I most need to internalise: **on a low-bad-edge inverse scramble where both UD and RL show 2-move EOs, the UD axis is often the one with the cleaner post-DR skeleton residual, because the FB=6 normal state's structure tends to leave RL-DR with awkward corner cycles.** I didn't probe deeply enough at the EO-axis selection step.

### vs nissy axis-locked UD (33)

Nissy on UD gives 4+10+8+11 = 33. My RL-axis solve gave 2+12+9+11 = 34. The NISS+axis switch was worth roughly 2 moves on EO (4→2) and cost roughly 2 moves on DR (10→12) and 1 on HTR (8→9), for a net +1 — i.e. my axis pick was slightly worse than just executing nissy's UD pipeline. If I had probed inverse-UD instead of inverse-RL the comparison would likely have flipped the other way.

### vs prior LLM versions

| Version | Moves | Notes |
|---|---|---|
| v19 | 30 | Long DR-style solve with a 4-move EO `U2 B2 U2 L2`-prefix wedge |
| v24_n4 | 31 | DR-style; lost moves in HTR-finish |
| v25 | 29 | Best prior — clearly found a sharper DR or skeleton |
| v34 | 29 | Tied for best prior, 38 tool calls |
| **this version** | **34** | **Regression of 5 vs best prior** |

This is a hard regression. v25 and v34 both shipped 29 — that's only 10 over Marcucci, and within 4 of the nissy axis-locked ceiling, suggesting they found either a better DR substate, a 2c3+2e direct skeleton, or a much lighter HTR finish. The pattern here was that I locked into the chunked HTR-reduction+finish pipeline without ever probing a direct DR-skeleton solve, while v25/v34 apparently did.

---

## What I'd change

1. **Add a "skip HTR" probe immediately after DR.** Once at DR, before recognising the HTR subset, do a depth-search for direct 2c3+2e or 3c2e skeleton finishes within ~12 moves with NISS-on-tail. On this scramble that probe would have caught something like Marcucci's `L · L2 U2 F2 L' F2 L · U2 F2 U2` 10-move post-DR skeleton, saving ~10 moves. The current pipeline always pays the full HTR-reduction tax even when the DR state is finish-friendly.

2. **Probe BOTH 2-move EO axes on the inverse when bad-edge counts are 4/6/4-style.** I committed to RL the moment I saw `R2 D'` give a clean 4C2E and didn't even `try_alg` the UD-`L' F'` candidate's DR landing. Marcucci's solve proves UD was the right axis. The cost of one extra `try_alg` is trivial relative to a potential 5-move improvement.

3. **Single-shot HTR-reduction query instead of chunked apply.** The 9-move reduction `U2 R' U2 R' D2 R2 U2 F2 L` is 1 over the 8-move optimum; chunking 4+4+1 from greedy lookups is a known leak vector. A direct DR-to-HTR optimiser call would have closed that gap.

Both drafts converged on the same 34-move solution, which says the pipeline is consistent — but consistency at +15 vs the human reference means the pipeline itself is missing the skeleton-finish branch, and that's the fix that matters.
