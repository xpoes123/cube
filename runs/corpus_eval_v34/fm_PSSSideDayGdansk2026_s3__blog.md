# FMC Retrospective: PSSSideDayGdansk2026 S3 — The Triple DNF

**Scramble:** `R' U' F U2 B D' R U F R2 U F B' R' U2 D2 R2 U2 B2 D2 B2 L B2 R' U' F`

- **My submitted move count:** DNF (0/3 drafts converged)
- **WCA reference (Marcin):** 23 moves
- **Nissy axis-locked (UD):** 31 moves

The entire gap this session came from a single misread: I trusted `dr_trigger_options` returning "no trigger ≤5 moves" on every axis as a signal that this was a structurally hard scramble, when in reality Marcin's solve shows there's a 4-move EO + 7-move DR (RBR-style, hitting DR-4a2/4e directly) sitting right on the FB axis. I never went beyond depth-5 trigger surveys before flailing into brain-guided walks.

---

## Initial scout

`inspect_state` returned bad-edge counts of **UD=4, FB=8, RL=6**. Standard read:

- **UD (4 bad: UL, DR, DL, DB):** scattered, no obvious 3-mover, but 4-move EO almost guaranteed. Best axis on paper.
- **FB (8 bad):** classic all-bad, often hides a short EO via the symmetric trick. Considered as primary NISS candidate.
- **RL (6):** weakest, scout only if the other two collapse.

`eo_pattern_lookup` confirmed:
- Normal UD: `U L R' B'` (4)
- Inverse UD: `B' R' U B'` (4)
- Normal FB: `R' F D L'` (4)
- Inverse FB: `B U' R' F' L'` (5)
- Normal RL: ~5
- Inverse RL: ~5

Three different 4-move EOs to choose from. The decision tree at this point was supposed to be: probe DR on each, pick the cheapest joint EO+DR. That's where everything fell apart.

---

## Draft 1 — FAILED (max_tool_calls, 80 calls, 968s sim)

**Phase trace (such as it is):**
- EO scout UD-normal (`U L R' B'`) → `dr_trigger_options` UD: **no trigger ≤5**
- NISS → EO inverse-UD (`B' R' U B'`) → `dr_trigger_options` UD: **no trigger ≤5**
- NISS back → EO inverse-FB (`B U' R' F' L'`) → `dr_trigger_options` FB: **no trigger ≤5**
- Bailed to `dr_recognize` brain loop: `U R2 B2 L L L2` — got stuck in a fixed point
- Reset, walked policy_intuition from scratch: `U B D L U` (5-mv RL-EO discovered emergently)
- Brain-guided DR on RL: `F2 R L U2 L2 F2` — `quick_check` said "still working toward DR"
- Brain-guided HTR/finish: `L2 R2 U2 B2 D2 B2 L2 F2 U2 R2 D2 L2 U2 F2` — never solved, didn't submit

**What I was thinking:** UD looked clean on EO so I scouted it first on both sides. When both `dr_trigger_options` calls returned "no trigger ≤5", I read that as a structural property of the scramble rather than a property of my depth bound. I should have re-called with depth 6 or 7 immediately — Marcin's DR is 7 moves on FB, and even nissy's axis-locked DR is 9 moves on UD, so a depth-5 cutoff was always going to miss.

Instead I bailed to `dr_recognize`'s brain. The brain's policy distribution on this state was uninformative (top suggestion at 34%, then 16%, then 12%), but I followed it greedily and burned 12 tool calls on `R2 L2 D2 D B2` and never landed on a named substate. By the time I reset and tried policy_intuition from raw scramble, I had 30 tool calls left and no plan.

**Where this draft leaked:** Everywhere. No coherent phase decomposition existed. The final 14-move half-turn finish was guessed, not derived.

---

## Draft 2 — FAILED (max_tool_calls, 80 calls, 1571s sim)

**Phase trace:**
- Same UD-normal and inverse-UD scouts → same depth-5 misses
- FB-normal EO `R' F D L'` → `dr_trigger_options` FB: **no trigger ≤5**
- RL scouts also failed
- Committed to FB-normal anyway, drove `dr_recognize` brain: `R2 L2 D2 D B2` (5 more moves)
- `inspect_state`: FB-EO **broken** (8 bad on UD, 0 on FB → wait, FB-EO still solved; the brain walk went into DR-5C3E)
- Brain walk continued: `R' B2 R R` → FB-EO broken again (4 bad on FB), but landed in DR-4C2E
- Re-fixed EO: `L2 F2 R'` (3 moves) → at 13 moves with no DR, depth-5 trigger still empty
- Switched to `policy_intuition`, started hammering: `D2 B2 B F2 F2 L2 D2 R2 B D' B D' B D'`
- `inspect_state` at move 24: FB-EO solved, RL=2 bad, **DR-6C1E on FB**
- Brain still couldn't close: `F2 U D U' U L2 D F2 D F2 D F2 D F2 D F2 L2 F2 U F2 D F2 U F2 D F2 U F2`
- Hit 50 moves, never solved, never submitted

**What I was thinking:** "Commit hard" became "commit to a doomed line." The actual fatal moment: after the brain walk landed me in DR-5C3E with broken EO, I should have realized this was diagnostic — the EO-preserving DR was deeper than 5 moves and the brain was finding a *non-EO-preserving* path. That's actually fine in principle (DR-Xs / co-DR territory), but I had no tool to navigate it cleanly.

The 14-move tail of half-turns (`D F2 D F2 D F2 ...`) was pure panic. I was at DR-6C1E — one slice edge away from a real DR — and I knew it, but every brain query just kept suggesting the same family of half-turns that never closed the cycle.

**Where this draft leaked:** Same root cause as Draft 1, but worse: I spent 13 moves getting back to where Draft 1 was at move 9, then chained another 37 moves of guesswork.

---

## Draft 3 — FAILED (sim_budget, 24 calls, 1159s sim)

**Phase trace:**
- UD-normal EO `U L R' B'` → trigger depth 5 empty
- NISS → inverse-UD EO `B' R' U B'` → trigger depth 5 empty
- Reset, FB-normal EO `R' F D L'` → trigger depth 5 empty
- `dr_recognize` brain walk: `R2 L2 D2 D` (cancelled to `D'`)
- **Finally** raised depth: `dr_trigger_options(axis='FB', depth=6)` → **`U F2 L2 U` setup + 4-mv trigger, lands in DR-4C2E in 9 total**
- Ran out of sim budget before applying it.

**What I was thinking:** By draft 3 I had finally diagnosed the problem — depth 5 was too shallow. The depth-6 call returned exactly what I needed: a **DR-4C4E setup `U F2 L2 U` followed by a 4-move trigger reaching DR-4C2E**. This is *the same DR substate Marcin reached* (4a2/4e in his notation), and from there a ~12-move HTR+finish would have put me at ~25 moves total — within 2 moves of his solve.

But by the time the tool returned, sim_budget was already gone. I had 0 moves submitted.

**Where this draft leaked:** Pure latency. The depth-6 `dr_trigger_options` took ~200s of sim time. Three of those depth-5 misses earlier in the draft were a sunk cost I shouldn't have paid — I already knew from drafts 1 and 2 that depth 5 was empty on every axis.

---

## Winning-draft analysis

There is no winning draft. For completeness, here's what the depth-6 result *should* have unfolded into:

- **EO (4):** `R' F D L'` — FB-normal, kills 8 bad edges
- **DR setup + trigger (~7):** `U F2 L2 U` setup + 4-mv trigger to DR-4C2E (totals to 11 cumulative)
- **HTR (~3-5):** DR-4C2E with 4qt corners + 2 slice edges — Marcin solved this in 3 moves (`L2 U U` with the final U merged on inverse)
- **Finish (~8):** half-turn finish, possibly with a slice insertion saving cancellations

Marcin's 23 was essentially this pipeline with a 7-move slice insertion `F2 U2 R' L D2 R' L'` on inverse cancelling into the htr+finish boundary. I would not have found the slice insertion, but a clean 26-27 was reachable.

---

## Three-way comparison

**vs Marcin (23 moves):** He won by recognizing that **FB-normal EO `R F D L'` had a direct 7-move DR to 4a2/4e**, no NISS-shopping, no axis-hopping. His commentary explicitly names the substate: "DR 4a2 4e (11)." Then a 3-move HTR (`L2 U` with the final `U` lifted to inverse), and the killer was a 7-move slice insertion `F2 U2 R' L D2 R' L'` on inverse that cancelled 2 moves with the EO+DR junction. He saved ~8 moves over nissy's axis-locked solve by **skipping DR-as-a-discrete-phase** — his DR phase *is* the trigger, no setup. I needed the depth-6 trigger survey to see this, and I never ran it until draft 3 was already dead.

**vs nissy axis-locked (31, UD):** Nissy commits to UD and pays 5+9+8+9. Marcin's 23 on FB beats nissy by 8 moves entirely through axis choice + EO+DR merger. So **axis choice and trigger-not-phase recognition was worth 8 moves** on this scramble. I left all 8 of those on the table — and an additional infinity, since I DNFed.

**vs prior LLM versions:** The relevant comparison is v27b/v29/v30/v31, all of which landed on **27 moves** with the *same* solution: `R' F D L' B' D F' U' B L2 D F2 R2 U2 F' U2 L2 B R2 U2 B2 R2 F2 U2 B2 D2 F2`. Parsing this: EO `R' F D L'` (4), DR setup+trigger `B' D F' U' B L2` (6 → 10), then a long HTR+finish tail (17). v27b found the same FB-EO entry and a working DR path in 6 moves — just one move worse than Marcin's 7-mover that lands directly in 4a2/4e (v27b lands in a slightly worse substate).

Versions v32 and v33 regressed back to 30. The session I just ran is *worse than both regressed runs* — they at least submitted. My triple-DNF is the worst result on file for this scramble.

The pattern across prior versions: every version that submitted **trusted FB-normal EO `R' F D L'` and committed to driving DR from there**, even when depth-5 triggers came up empty. I did not. I treated depth-5 empty as terminal information instead of as "raise depth."

---

## What I'd change

1. **Default `dr_trigger_options` depth to 7, not 5.** Marcin's DR is 7 moves on this scramble; nissy's is 9. A depth-5 cutoff is a faulty oracle that wastes 2-3 tool calls per axis on false negatives. The sim-time cost of depth 7 is real but the information-per-second is dramatically better than the depth-5→brain-loop fallback I kept doing.

2. **Cache the depth-5 empty result and never re-query it across NISS flips.** I called depth-5 `dr_trigger_options` on UD-normal, inverse-UD, FB-normal, RL-normal, and inverse-FB across the three drafts — that's 5+ identical empty results burning ~25 tool calls cumulatively. Once depth 5 is empty on an axis from one side, NISS doesn't change DR distance — flip the depth bound, not the side.

3. **When `dr_recognize`'s top suggestion is <50% probability, do not greedy-walk.** The brain returned 34%/16%/12% on the first DR query of draft 1. That's a uniform-ish distribution, meaning the brain has no signal. Walking it greedily compounds error every move. The correct response is to fall back to `dr_trigger_options` at higher depth, not to apply the 34%-confident move and re-query.

The diagnostic was sitting in plain sight from move 8 of draft 1; I just needed to read it.

---

A triple-DNF on a scramble where the prior LLM has a stable 27-move solve is a regression caused entirely by trusting a single tool's default depth parameter as a structural verdict instead of a hyperparameter to tune.
