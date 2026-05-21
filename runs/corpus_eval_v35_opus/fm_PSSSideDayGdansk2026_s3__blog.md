# fm_PSSSideDayGdansk2026_s3 — Retrospective

**Scramble:** `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`

- **Submitted:** 33 moves
- **Marcin (WCA reference):** 23 moves
- **Nissy axis-locked (UD):** 31 moves
- **Prior LLM best (v27b/v29/v30/v31):** 27 moves

The 10-move gap to Marcin came almost entirely from the back half: I found his exact EO start (`R' F D L'`) but then committed to a full DR→HTR→finish pipeline on the RL axis instead of taking the direct 2c3+2e-type solve Marcin used out of EO. The HTR-subset I landed in ("2-swap 2-cycle") demanded a 10+12 reduction/finish that nothing was ever going to recover from.

---

## Initial scout

`inspect_state` on the normal frame: UD=4, FB=8, RL=6 bad edges. UD obviously dominant by count, and I recognized the 4-mover on UD-normal as `U L R' B'` immediately. NISS check on the inverse: also a 4-move UD EO (`B' R' U B'`). Two equally cheap UD-EOs — promising.

I did not initially scout FB-EO from inspection; it was 8 bad and I dismissed it without checking the length. That was the actual mistake of the session: Marcin's `R' F D L'` is a 4-move FB-EO despite the 8-bad count, because pairs of bad edges are cheaply flipped together on this scramble. I only stumbled into it in attempt 1 after the UD branch died.

---

## Draft 1 — SOLVED 36mv, 448s, 73 calls

**Phase decomposition:**
- EO-FB (4): `R' F D L'` — kills the 8 FB-bad edges in 4
- EO-bonus / DR setup (5): `U' F D B U` — lands in a state where *both* FB and RL are EO
- DR-RL (5): `B' L' U2 L B` — DR locked on RL, total 14 to DR
- HTR reduction (10): `D2 R D2 R' F2 R U2 R' D2 R` — 2-swap 2-cycle subset reduction
- HT finish (12): `B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2`

### What I was thinking

I opened on UD because the count was lowest. Committed `U L R' B'` (4) on normal, then probed DR. `dr_trigger_options(axis='UD')` style scout returned a chain that reached 2C1E in 3 (`U R D2 L`), then continued to 2C0E at depth 5 (`R2 B2 R U2 R'`), then to **0C1E** after `R F2 R F2 R'`. That's 18 moves and I was sitting on a single mis-oriented edge with odd parity — a parity-stuck UD-DR neighborhood.

I NISS'd to the inverse to look for an escape, got told the inverse would need its own fresh 4-move EO, and decided that wasn't worth it. Tried `L'` and `L` as the brain's top picks (53% / 36%); both stayed in the 0C1E class. Estimated ≥6 more moves to clear the parity. Reset.

Restarted from the scramble, NISS'd to inverse: `B' R' U B'` (4) → `R' U D2 R` (4 more, 2C1E) → `U2 D' L U L'` (5 more, 2C0E). Same wall — the UD-DR endgame on this scramble has a fundamental parity issue. Reset again.

Then finally tried FB: `R' F D L'` is 4 moves and lands in 3C0E. Pushed `U' F D B U` (5) — and the after-state had **both FB and RL fully EO'd**. That's the dual-EO state Marcin's solve was built on (he saw it 5 moves earlier, going directly to DR from EO without the bridge). My brain offered D2 (62%) as the top DR continuation but I noticed RL was clean and pivoted to RL-DR with `B' L' U2 L B` (5).

`htr_classify` on the DR-RL state: **2-swap 2-cycle**. That's a bad subset — 10+12 reduction/finish, total 22 moves from DR. I knew it was long but I'd already burned 60+ tool calls thrashing on UD; committed and pushed through. The full HTR phase came out clean (no cancellations between chunks) and finished at 36.

`replace_and_shorten` on `[4:36]` failed: "no DR found" on the micro-scramble (the sub-search couldn't reproduce a DR from move 4 onward in budget). Shipped 36.

### Where this draft fell short

Two things. First, ~30 wasted tool calls thrashing the UD branch instead of recognizing within 2-3 probes that the 0C1E parity wall was real and pivoting. Second, once in HTR-2-swap-2-cycle, I never queried for an alternative DR axis or a `2c3+2e` direct probe from the post-EO state.

---

## Draft 2 — SOLVED 33mv, 49s, 23 calls (SUBMITTED)

**Phase decomposition:**
- EO-FB (4): `R' F D L'`
- DR setup + DR-RL (10): `U' F D B U B' L' U2 L B` — total 14 to DR-RL
- HTR reduction (10): `D2 R D2 R' F2 R U2 R' D2 R` — 24 to HTR
- HT finish (12 raw): `B2 L2 B2 U2 F2 U2 F2 L2 R2 U2 R2 U2` — 36 raw

Then `replace_and_shorten` on the tail saved 2; cancellation of `R2 R'` → `R'` saved 1 more. **33 final.**

### What I was thinking

Direct replay of the winning DR path from draft 1. The 14-move DR was confirmed good and I had a budget. The whole point of this draft was to keep the front end and attack the back end harder.

I knew going in that the 22-move HTR finish was the problem. I considered re-classifying after each chunk to catch an early HTR-residual collapse — `quick_check` between chunks during reduction is cheap. It did show "in HTR" partway through the finish (after `B2 L2 B2 U2`), but residual class was "mixed" meaning I was already in a known finish line, not on a shortcut.

After the raw 36, I called `replace_and_shorten` on the full tail span. Gates passed (≥27 moves remaining, ≥30 calls left). The tool returned a substitute 2 moves shorter for the post-EO segment, with the new history containing `R2 R'` at the seam. Cancelled that pair to `R'` and verified solved at 33.

The substitute reorganized the HTR-reduction + finish into the compact form
`D2 R2 B2 D2 F2 B2 R F2 R B2 R2 D2 R' F2 R F2 R' F' U2 F' U2 F D2 R` — note the conjugated `F' U2 F' U2 F` finish chunk which the original brute decomposition didn't see.

### Where this draft fell short

It's the submitted one, but it still lost 10 to Marcin and 6 to v27b. The leak is structural, not a missed optimization in this draft — the leak is the entire decision to go through DR-RL into a 2-swap-2-cycle HTR subset, when the post-EO state admits a direct slice-style finish in much less.

---

## Draft 3 — SOLVED 33mv, 75s, 23 calls

Identical to draft 2 by design — "commit the proven path and try harder on the finish." Used the same EO+DR, same HTR reduction chunks, same raw 36, same `replace_and_shorten` saving 2, same `R2 R'`→`R'` cancellation to 33. Two attempts at exactly the same line do not produce two different finishes; the redundancy was wasted budget.

---

## Winning-draft analysis (draft 2, 33 moves)

Final move list (canonical, normal frame):

```
R' F D L'              (4)   EO-FB
U' F D B U             (9)   pre-DR setup, lands at dual FB+RL EO
D2 R2 B2 D2 F2 B2      (15)  DR-RL + early HTR-reduction fusion
R F2 R B2 R2 D2        (21)  HTR-reduction continued
R' F2 R F2 R'          (26)  setup for finish conjugate
F' U2 F' U2 F          (31)  3-move-corner-cycle commutator dressed as conjugate
D2 R                   (33)  finish
```

Notes:

- The first 9 are forced — there's no shorter way I scouted to reach the dual-EO state, and Marcin reached DR in 11 from `R' F D L'` so his savings start at move 5, not at the EO.
- After the `replace_and_shorten` substitution, the boundary between DR-completion and HTR-reduction blurs. The original draft had a clean `B' L' U2 L B` to lock DR-RL; the substitute fuses that lock-in with the reduction directly into the `D2 R2 B2 D2 F2 B2` block. This is the kind of cross-phase optimization that's hard to find by hand and exactly what `replace_and_shorten` is for.
- The `F' U2 F' U2 F` insert is a corner-3-cycle setup that doesn't appear in any of my chunked phase outputs — the tool's micro-search found it.
- `R2 R'` → `R'` at the seam was a free 1-move save on top of the tool's 2.

The neighborhood alternatives I didn't explore: post-EO at move 4, after `R' F D L'`, a direct-to-solve probe (skipping DR entirely) or a 2c3+2e probe was never queried. This is what Marcin did and what cost me the 10 moves.

---

## Three-way comparison

### vs Marcin (23 moves, −10)

Marcin's decomposition from his commentary:
- EO (4): `R F D L'` — same EO as mine, just on the inverse / different frame, equivalent
- DR 4a2 4e (7): `F R2 U' D2 F' L2 F` — reaches DR in 11 total
- HTR (3): `L2 U` (his count includes a setup move), HTR at 14
- Slice finish (9): `(F2 U2 R' L D2 R' L') ... F2 U' D' F2 D` — 9-move slice-y finish, +1 over optimum by his own admission

His killer move: **DR in 11 from the same EO**, hitting a `4a2 4e` substate that admits a 3-move HTR reduction and a slice finish. My DR took 14 (an extra `U' F D B U` setup chunk to expose RL-EO that he didn't need), and my HTR subset was `2-swap 2-cycle` (10+12) versus his `4a2 4e` (3+9). The subset choice is worth at least 10 moves on this scramble.

I never recognized that the post-EO state Marcin sits in is a 7-move DR on UD. My `dr_trigger_options` on UD got stuck in 2C1E/0C1E parity hell because I was searching UD-DR from a 9-move setup (`R' F D L' U' F D B U`), not from the bare 4-move EO. Had I scouted UD-DR directly from the EO-only state I'd likely have seen something close to his 7-mover.

### vs Nissy axis-locked UD (31 moves, −2)

Nissy's UD pipeline: 5+9+8+9 = 31. My 33 beats nissy on EO/DR (4+10 = 14 vs 5+9 = 14, tied) but loses 2 to nissy's clean 8+9 = 17 HTR+finish, where I'm at 10+9 = 19 even after `replace_and_shorten`. So my axis pivot to FB-EO + RL-DR was worth 0 moves vs nissy's pure UD pipeline (both at 14 to DR), and I leaked 2 in the back end. Marcin's strategy of *skipping DR entirely* is what breaks past the nissy ceiling.

### vs prior LLM versions

- v19/v24/v25/v26: all in the 29-30 range, all UD-axis-based finishes. Worse than mine.
- **v27b/v29/v30/v31: 27 moves** — `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`. Same EO (`R' F D L'`), then a totally different continuation `B' D F' U' B L2 D` that reaches some intermediate state in 11, followed by a 16-move half-turn tail. This is much closer to Marcin's strategy — they're hitting a good DR or quasi-DR substate from the same EO and finishing in slice/half-turn. v27b's solver was finding the same dual-EO observation I made but exploiting it correctly.
- v32/v33: regressed to 30 with very different EO. Worse front-end choice.

So I'm 6 moves *behind* v27b, on the same scramble, with the same first 4 moves found. The regression is entirely in the post-EO decision: v27b probed direct continuations from the bare EO state; I jumped into a setup-into-RL-DR detour.

---

## What I'd change

1. **After any short EO (≤4), call a direct-finish or 2c3+2e probe before committing to a DR setup.** On this scramble, post-`R' F D L'` admits a 7-move continuation to a near-solve substate that nothing in my workflow ever queried. A `dr_trigger_options` call on UD *from the bare EO state* (not from my 9-move setup) would likely have surfaced Marcin's 7-mover.

2. **Treat `htr_classify` returning `2-swap 2-cycle` as a hard reroute trigger.** That subset's 10+12 is essentially guaranteed loss vs a re-pick. The moment I saw it on RL-DR I should have NISS-probed or re-scouted DR on UD/FB instead of committing.

3. **Don't burn 30+ calls thrashing UD parity walls.** The 0C1E with odd parity I hit on attempt 1's UD branch was diagnosable in 2-3 probes; I spent 10× that. A cheap heuristic: if two consecutive depth-5 DR searches stay in the same residual class, abandon the axis.

A clean front end found on its own merit, then thrown away by committing to the wrong DR axis and the wrong HTR subset.
