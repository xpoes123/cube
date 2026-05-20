# fm_PSSSideDayGdansk2026_s1 — Retrospective

**Scramble:** `R' U' F U2 L2 U2 D' F L2 B' D' R' F' U2 D2 R' U2 D2 R2 B2 U' R' U' F`

**Submitted:** 31 moves. **Marcin (WCA reference):** 20 moves. **Nissy axis-locked (UD):** 35 moves.

The gap is almost entirely a strategy gap, not an execution gap: Marcin skipped DR entirely and finished from a 2c3+2e EO state with a 10-move direct insertion. I committed to the UD DR pipeline, executed it roughly on-par with nissy's ceiling (31 vs 35), and never even considered the direct-solve branch.

---

## Initial scout

`inspect_state` on normal: **UD=8, FB=6, RL=6**. The 8-bad UD count is misleading — UD turned out to support a 4-move EO (`R2 D' B' F'`), tying FB and RL on raw count but with a much cleaner pattern. I pattern-matched all three:

- FB axis: 4-move EO starting `R2 B' L' U2…` → 5mv total
- RL axis: 4-move EO starting `L U L2 R…` → 5mv total
- UD axis: `R2 D' B' F'` → **4mv**

I NISS-flipped to check the inverse for UD and saw 4mv there too (`B' D' L' R'`) — no improvement, so I flipped back and committed UD on normal. FB/RL never got serious consideration past this point. In hindsight, with 6-bad on FB/RL, the 2c3+2e direct-solve probe Marcin used would have been more naturally hosted on one of those — but I didn't have a tool habit for "after EO, try direct insertion before going to DR."

---

## Draft 1 — SOLVED in 31, 215s sim time

### EO (4): `R2 D' B' F'`
UD axis, kills all 8 bad edges. No alternatives worth weighing — this was the obvious commit.

### DR exploration (false start)
After EO I queried DR triggers and saw 3-move setups landing at **DR-2C1E** (3 bad pieces). I committed `L2 U' R` (running 7), then re-queried. Depth 4 returned nothing; depth 5 gave **DR-0C1E** via `L U' R2 U L`. I committed (running 12) and then discovered the trap: 0C1E with odd slice-edge parity is unreachable from EO-preserving moves alone. I tried a NISS escape, realized NISS mid-DR doesn't fix a parity problem of this shape, and rewound 8 moves back to the post-EO state.

This was the main time sink of the draft. The lesson here is one I should have already internalized: when depth-N DR options bottom out at odd-parity XCYE states like 0C1E, **the parity is structural**, not search-depth-limited. Don't commit a setup that lands on it.

### DR setup (13, with cancel): `F2 L F2 U R · R U2 F2 D2 L · R U2 F2 D2 L`
Restarting from post-EO, I went after **DR-0C2E in 5** with `F2 L F2 U R` (even slice-edge parity, escapable). Cancellation against the EO tail saved 1 move (F'·F2 → F), landing at running 8. Then `R U2 F2 D2 L` to drive toward 0C1E with JZP-eligibility, and another `R U2 F2 D2 L` to actually finish DR.

Final DR state at 17 moves: UD=0, FB=0, RL=2, qt_corners=4. This is what nissy would call a fairly heavy DR — 14 moves of HTR+finish work ahead.

In canonical form after all the cancellation, the DR phase reads: `U2 R2 U2 L2 U2 R2 F2 R2 B2` (9 moves) — a long axial chunk that absorbed the two `R U2 F2 D2 L` repeats and the intermediate `F2 L F2 U R`.

### HTR reduction (9): `U R2 U L2 U' F2 R2 U' D` (in canonical form: `U R2 U L2 U' F2 R2 U' L2`)
Classified the DR state as **2-swap mostly-axial** — first time seeing this exact subset, per the tool. Reduction came out in 9 moves, applied in three chunks (`B2 U L2 F2`, `U L2 U' B2`, `D`) with verification between each.

### Finish (10 raw): `D2 F2 D2 R2 D2 F2 U2 R2 F2 L2`
Standard half-turn finish. Got there at 35 raw moves.

### Tail refinement: replace_and_shorten saved 3, cancellation saved 1
At 35 moves, gates passed for `replace_and_shorten` on the tail. The substitute trimmed the HTR-finish tail from 19 moves to 16, putting the canonical solution at 32. One more cancellation merge at the splice point dropped it to 31.

The final tail (what `replace_and_shorten` returned) in the submitted solution is: `U R U R' L' D R D L'` — a 9-move finish that includes the conjugated 3-cycle `R U R'` and a setup-corner-commutator-style closer `L' D R D L'`. That's not a standard half-turn finish at all; the tool found a 3-cycle insertion into the late tail that bypassed the last few half-turns entirely. Good outcome from a tool I usually treat as last-resort.

### Where this draft leaked vs the reference
Everywhere after EO. Marcin's 16-move tail from post-EO (`L B2 R D2 L' D' L D2 F2 B2 R' U2 R2 U2 L B2`) included a 2c3+2e direct-solve phase that I never probed. My 27-move tail from post-EO did the full DR → HTR → finish pipeline plus a salvage refinement. The 11-move difference is *strategy*, not execution.

---

## Draft 2 — FAILED, 60s sim time

No narrative captured. 14 tool calls, no submission. Likely an EO/DR scout that ran into the budget wall before committing — given draft 1 was already banked at 31, this was a low-stakes exploration that didn't pan out.

---

## Winning-draft deep dive

The submitted solution in canonical form:

```
R2 D' B' F                                  // EO-UD (4)
U2 R2 U2 L2 U2 R2 F2 R2 B2                  // DR-UD (13)
U R2 U L2 U' F2 R2 U'                       // HTR (21)
L2 U' R U R' L' D R D L'                    // finish (31)
```

Phase splits: 4 / 9 / 8 / 10.

**EO (4):** Optimal. Nissy's axis-locked path uses 5 (`L U R L2 D`) because it's optimizing the full UD pipeline jointly — my 4-move EO sets up a worse DR. This is the classic EO-DR tradeoff: a shorter EO can leave you with a heavier DR setup. Here it cost me: nissy's DR-from-EO is 10, mine after cancellation is 9 — roughly tied — but nissy's HTR+finish is 20 total, and I needed the tail-refinement trick just to get to 18.

**DR (9):** `U2 R2 U2 L2 U2 R2 F2 R2 B2`. This is an all-axial chunk after the cancellations resolve. The reason this works out is the double `R U2 F2 D2 L` pattern I committed — two consecutive 5-move setups, with `F2 L F2 U R` between them, all collapsing through cancellation against the preceding EO tail. The structural read: I was driving qt_corners down in 5-move increments, and the U/D-only EO meant every F2/L/R-axis move stayed EO-preserving.

Alternatives in the neighborhood: the depth-5 DR-0C1E branch I aborted (`L U' R2 U L`, parity-trapped). The depth-5 DR-0C2E branch I took. I never queried a depth-6 or depth-7 direct-to-DR search because the 5-move JZP-eligible candidate looked good enough.

**HTR (8):** `U R2 U L2 U' F2 R2 U'`. The 2-swap mostly-axial subset. Comparable to nissy's 10-move HTR (`U R2 L2 U L2 U' L2 U R2 U`) — I came out 2 ahead here, which is the one phase where I clearly outperformed the axis-locked ceiling. The corner-reduction tool nailed this.

**Finish (10):** `L2 U' R U R' L' D R D L'`. NOT a half-turn finish. After `replace_and_shorten` replaced the original `D2 F2 D2 R2 D2 F2 U2 R2 F2 L2` (10 half-turns) plus part of the HTR tail with a shorter sequence containing quarter turns, the canonical compose ended up with a 3-cycle-flavored closer. Net savings vs nissy's finish (10 half-turns): 0 raw, but the substitution merged cleanly with HTR to save 3.

The cancellation/refinement budget breakdown:
- EO/DR splice: 1 move (F'·F2 → F)
- `replace_and_shorten` on tail: 3 moves
- Final cancellation pass: 1 move
- **Total salvage: 5 moves** from a 35-raw to 31-submitted.

Without salvage, this would have been a 35-move solve — exactly tied with nissy's axis-locked optimum. The salvage is what made it competitive (within its branch).

---

## Three-way comparison

### vs Marcin (20mv)
Marcin's decomposition from his commentary:
- EO (4): `R2 D F B'` — same axis as mine, mirror of mine, also 4 moves.
- 2c3+2e (6): `L B2 R D2 L' D'` — landing at a 2-corner-3-cycle + 2-edge state at 10 moves total.
- Direct solve (10): `(B2 L' U2 R2 U2 R F2 B2 D2 L')` on inverse — a 10-move sequence that solves the 2c3+2e remainder directly.

Marcin **skipped DR/HTR entirely**. His 2c3+2e is a state I have a name for but no tool habit for probing after EO. The 10-move direct-solve insertion on inverse is the kind of thing I'd need either a coset-table lookup or a much more aggressive `replace_and_shorten` window to find.

**Where he won:** 11 moves, all in the post-EO branch. He bet on the direct-solve path being short (it was — 16 moves from EO to solved), and it paid off because the EO state left a clean 2c3+2e shape that's well-known to have ~10mv solutions.

### vs nissy axis-locked (35mv on UD)
I beat axis-locked by 4. The accounting:
- EO: I used 4, nissy used 5 → +1 for me on EO
- DR: I used 9, nissy used 10 → +1 for me on DR
- HTR: I used 8, nissy used 10 → +2 for me on HTR
- Finish: I used 10, nissy used 10 → tied

So execution-wise, the **EO+DR axis pick + the 2-swap mostly-axial HTR subset** were each worth a move or two against the axis-locked ceiling. That's a real win at the phase level. The `replace_and_shorten` salvage didn't actually beat nissy's pipeline — it just brought my raw 35 down to 31 by merging across phase boundaries, which is exactly the kind of thing a phase-by-phase optimizer can't do.

### vs prior LLM versions
- **v35_smoke** got 24mv with 117 tool calls — that's the only prior version that beat 25. It almost certainly probed a 2c3+2e or direct-solve branch given the tool-call budget.
- **v24/v25/v26/v29/v30** all converged on the same 25mv solution: `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2 L2 U' B2 U' F2 U R U L2 D L D' L'`. That solution has the same 4-move UD EO (mirrored: `R2 D' F' B`), then a long axial block, then a quarter-turn-rich tail very similar in shape to what `replace_and_shorten` gave me. Those versions were finding the 25mv path natively — I'm getting 31 with the same EO start.
- **v19/v34** got 30mv with the *exact same* prefix as mine: `R2 D' B' F' U' R' L2 U F2 R U2 R' U F2 U' R2 U L2 U2 R2 F2 U' B2 F2 L2 B2 L2 U2 B2 R2`. That's the dead-end branch I aborted in this run! v19 and v34 committed to it and pushed through; I rewound and took a different DR path. I came out 1 worse than them.

So I'm regressing vs the 25mv consensus that v24-v30 found. The most likely cause: my DR search committed too early on `L2 U' R` and then got tangled in the 0C1E parity trap, costing me time and forcing the second-best DR route. The 25mv lineage seems to have found a DR setup that merges more cleanly into the finish.

---

## What I'd change

1. **Add a 2c3+2e / direct-solve probe after every EO.** After committing EO, before going into the DR pipeline, query "can this state be directly finished in ≤16 moves on either frame?" This is exactly the branch Marcin took and v35_smoke probably explored. Even a coarse depth-12 IDA on the post-EO state would have surfaced something close to his 16-move tail.

2. **Recognize and reject 0C1E parity traps without committing.** When `dr_trigger_options` returns an XCYE state with odd corner+edge parity at depth N, *don't commit the setup* — go straight to depth N+1 looking for an even-parity target. I burned ~30s of sim time and 4 moves of commit/rewind on a structurally-doomed path.

3. **Trust the v24-v30 lineage's DR shape.** The repeated 25mv solution across six prior versions starts `R2 D' F' B R2 F2 R2 U2 F2 D2 R2 D2…` — a 4-move EO followed by a giant 8-move axial DR block. I should add a heuristic that, after a UD 4-move EO, *first* searches for axial-only DR sequences of length 6-10 before going to quarter-turn JZP setups. The axial path seems to merge with the finish much better on this scramble family.

---

I shipped 31 with the right EO and a phase-execution win against axis-locked nissy, but lost 11 moves to a strategy I never probed — the direct-solve branch is the obvious next addition to the playbook.
