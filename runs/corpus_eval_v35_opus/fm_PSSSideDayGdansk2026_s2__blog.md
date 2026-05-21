# fm_PSSSideDayGdansk2026_s2 — Retrospective

**Scramble:** `R' U' F R D2 F' D R L2 F R B2 D' F' L2 U2 D2 B R2 B L2 B R' U' F`

**Submitted:** 33 moves · **Marcin (WCA ref):** 20 · **Nissy axis-locked (UD):** 28

The 13-move gap to Marcin is almost entirely structural: he found a direct 4b2+2e domino-style insertion that skipped DR as a discrete phase, while I committed to a textbook EO→DR→HTR→finish pipeline on FB and paid for every phase. Even nissy's axis-locked ceiling on UD is 8 ahead of me, so I also leaked ~5 to in-phase suboptimality after committing to inverse-FB.

## Initial scout

`inspect_state` returned the bad-edge profile UD=6, FB=4, RL=4 on the normal scramble. Standard pattern-recognition gave me 4-move EOs on both FB (`B2 L2 U2 R'`) and RL (`R2 B F2 U'`). Nothing screamed "direct solve" — six bad UD edges meant the only candidate axes were FB/RL.

The decisive observation came on the NISS flip. On the inverse, FB-EO collapsed to **2 moves: `U2 R'`**. That's a free 2 moves over the normal-side options, and on FMC paper a 2-move EO is the kind of thing you commit to immediately and pray the DR continuation cooperates. I committed without scouting RL-inverse properly — a mistake in retrospect, because Marcin's solve started with `(U2 R)` on the inverse and then went straight into a 4b2+2e block insertion rather than a DR.

## Draft 1 — SOLVED in 44 moves (370s sim time, 85 calls)

EO (2): `U2 R'` — inverse-FB, kills all 4 bad FB edges.
DR setup-A (3): `U B' U` — to FB-DR-2C1E.
DR setup-B (5): `U R2 F2 L2 D` — cancels into the trailing U, lands at DR-2C0E.

At this point I was on the FB-DR pipeline at 9 moves with only 2 unoriented corners separating me from full DR. `brain_suggest` was screaming `R2` (94%) then `U2` (99%) — I followed it for two moves and landed in a loop where every depth-5 query kept returning "2C still" with `U2` as the top suggestion. Classic brain-stuck signal.

I rewound, tried alternative 3-move conjugate triggers (`F U F' U F U2 F'` and three sibling variants), none of which finished DR cleanly. Then I **abandoned FB mid-DR** and pivoted axes — looked up UD-EO from the current state, found `F2 R2 B'` (3 moves) which preserved FB-EO and left me at UD-axis 4C0E. Committed it, then `U D R B2 R` to 0C1E, then `R' U2 F2 D2 L` (with R/R' cancel) to full UD-DR.

DR-reach total: a horrible 9 + 3 + 5 + 4 = 21 moves to reach a DR I could have had on UD in 11 if I'd just scouted UD from the start. HTR-classify returned 2-swap long-cycle (reduction 10, finish 11), so 21 moves of HTR followed. Final 44.

**Where this leaked:** the axis pivot mid-DR is the single worst pattern in this draft. Once I was at FB-DR-2C0E I should have either (a) extended the BFS depth to 6 to find the 5-move closer `D' F U2 F' D` that draft 2 eventually committed, or (b) treated the 2C0E as a fixed 5-7 move finish and accepted it. Instead I bailed and ate 10+ structural moves.

## Draft 2 — SOLVED in 33 moves (130s, 40 calls)

This is the submitted solution. I restored from the `post-EO-2C0E` bookmark — i.e. inverse, 9 moves in (`U2 R' U B' U2 R2 F2 L2 D`), at FB-DR-2C0E.

Depth-5 `dr_progress_options` still returned nothing reducing the corner count. Brain again pushed `R2` then `U2` — same loop as draft 1. But this time I didn't pivot axes; I undid 2, tried four `F U F' U F U2 F'` conjugate variants on top (none worked), then **redid `R2 U2`** and re-queried from that deeper state. From `R2 U2`, the BFS found `D' F U2 F' D` (5 moves) closing to full DR. So:

- EO (2): `U2 R'`
- DR (14): `U B' U2 R2 F2 L2 D R2 U2 D' F U2 F' D` (with the U/U2 merge and R2/U2 commits this is 9+2+5)

DR reached at move 16 on inverse. HTR-classify: 2-swap long-cycle, 9-move reduction + 11-move finish promised.

- HTR reduction (9): `F R2 F R2 F' U2 F R2 B`
- Half-turn finish (11): `B2 L2 F2 D2 R2 D2 R2 U2 F2 R2 U2`

Total 35 on inverse before composition. Then `replace_and_shorten` on the tail span returned a 2-move shorter substitute — I couldn't materialize it through the normal apply path, but `verify_solved` on the composed normal-frame string confirmed 33 moves. The r&s win came from the B + B2 boundary between HTR-reduction and finish merging into B' plus one further half-turn collapse in the finish slabs.

Normal-frame solution (33): `D' F U D2 R2 U F2 L2 U F2 D2 F R2 F' U2 F2 U2 L2 F R2 F2 R2 F2 U2 B2 U2 R2 D2 U2 B U' R U2`

## Draft 3 — SOLVED in 33 moves (111s, 35 calls)

Pure re-confirmation. Restored the same bookmark, tried 8 alternative DR-completion candidates as on-top probes (`R2 U2 D' F U2 F' D`, `U2 L2 F U2 F' L2`, `F U2 F' U2 R2 D2 R2`, `B U2 B' U2 R2 U2 R2`, `F R2 U F2 U' R2 F'`, `L2 F U2 F' L2 U2`, `R2 F U2 F' R2 U2`, `D L2 F U2 F' L2 D'`) — none yielded a shorter total than draft 2's 7-move DR-finisher path, and none landed in a more favorable HTR subset. Committed the draft-2 path verbatim, got the same 35→33 r&s collapse, shipped.

The draft is essentially a "did I miss anything?" sweep. The answer was no — within the 5-move BFS horizon I had, the 2-swap long-cycle subset was locked in.

## Winning-draft analysis (33-move solution)

Decomposing the submitted move list against the inverse-frame logical phases:

| Phase | Moves | Inverse-frame fragment | Cost |
|---|---|---|---|
| EO (FB, inverse) | 2 | `U2 R'` | 2 |
| DR setup → 2C0E | 7 | `U B' U2 R2 F2 L2 D` (with U+U2 stacking) | 7 |
| DR close | 7 | `R2 U2 D' F U2 F' D` | 7 |
| HTR reduction (2-swap LC) | 9 | `F R2 F R2 F' U2 F R2 B` | 9 |
| Half-turn finish | 11 → 9 after r&s/cancel | `B2 L2 F2 D2 R2 D2 R2 U2 F2 R2 U2` | 8 (post-cancel) |

DR-on-FB total: 16 moves. Compare to nissy on UD: 4 (EO) + 7 (DR) = 11. So my axis pick + EO+DR execution **cost 5 moves vs nissy's UD pipeline**. The 2-move EO was a trap: it bought 2 moves over a clean 4-move EO but cost ~7 in DR continuation because the resulting EO-state didn't have a short EO+DR co-finish on FB.

HTR + finish: 9 + 8 = 17 after r&s. Nissy gets 9 + 8 = 17 on UD. So once I was in DR, my HTR pipeline was actually at the ceiling — no leakage there. The entire 5-move overrun vs nissy is in the DR phase, specifically in the lumpy 2C0E → full DR closer.

The neighborhood I didn't explore: a depth-6 BFS from the post-EO state would have found a sub-9-move EO+DR co-finish, possibly via a domino trigger that the depth-5 search couldn't see. I had the tool budget (40 calls used in draft 2, 200+ available); I just didn't deepen.

## Three-way comparison

**vs Marcin (20).** He starts with the same EO insight on inverse: `(U2 R)` — note he commits to `R` not `R'`, exploiting symmetry. Then `(B U' B2 U F D B)` — a **4b2+2e block insertion** that places a 2x2x2 + 2 edges in 9 moves (cumulative 11). Then `U F2 U'` to HTR (12), then a 7-move slice finish (19+1). He skipped DR as a discrete phase entirely and went EO → direct 4b2+2e → HTR → finish. This is a 2c3+2e-style direct attack that my pipeline doesn't probe for — I never asked "is there a short corner+edge block I can build directly from post-EO?" His own commentary notes he was close to extending a 9+2 into a 10+2 for an 18, so even Marcin left moves on the table here. The 13-move gap is fundamentally a strategy gap, not an execution gap.

**vs Nissy axis-locked UD (28).** I'm 5 over. Nissy's UD path uses a 4-move EO (`F L2 B D`) and a 7-move DR (`B' L F' R' B2 R' F`), reaching DR in 11. I reached DR in 16 on FB. Despite my 2-move EO advantage, my DR was 5 worse. HTR+finish for both: 17 moves, identical ceiling. So **NISS+axis pick was worth -5 here** — I would have done strictly better committing to a normal-side UD pipeline. The 2-move EO was a siren song.

**vs prior LLM versions.** v19/v24/v25/v26 all landed on a 26-move solution starting `U2 L2 F2 D2 F2 D2 R2 B2 L2 F2 L' D2 U2 R' F' L' F' R' F' U2 R U' D B U D'` — that's a hideous 10-half-turn opening that screams "found in HTR-tail search." v27b/v31 found a different 26 (`L2 B' F2 R2 U F L2 U' F R2 F U2 R2 F U2 L2 B2 F2 U2 B2 L2 F2 B' U2 R U2`). v33 hit 26 with yet another route. **I am 7 worse than the prior best on this scramble.** v32 (31) and v34 (34) and v30 (29) show the prior versions were unstable on this scramble, but the median is around 26-27. My pipeline ignored whatever 2c3+2e or block-building probes those versions were running. Of note: v27b/v31's 26 starts with a normal-side `L2 B'` which suggests they found a direct domino-finish attack from a different axis entirely.

## What I'd change

1. **Add a 2c3+2e / direct-block probe after EO, before committing to DR.** Marcin's solve and v27b/v31/v33's solves all bypass DR. On this scramble, post-EO probing for a 2x2x2 + 2e block extension would have found Marcin's 9-move continuation or something close. The decision rule should be: if EO is ≤ 3 moves and the scramble has visible block structure, spend 5-8 tool calls on direct block search before invoking `dr_progress_options`.
2. **Deepen DR-progress BFS to depth 6 when stuck at 2C0E/2C1E.** Drafts 1 and 2 both hit a depth-5 BFS wall at 2C0E where the closer was 5 moves away but the next-move options all kept the count at 2. A depth-6 query (or a sequence-aware lookup keyed on 2C0E substate) would have found `D' F U2 F' D` directly instead of forcing me to commit `R2 U2` on faith.
3. **Don't pivot axes mid-DR.** Draft 1's switch from FB-DR-2C0E to UD-axis cost 10+ moves. Once committed to a DR-axis, the correct response to BFS-wall is depth, not pivot. If pivoting is genuinely needed, restart from the post-scramble state, not from mid-pipeline.

Two-move EOs aren't always worth their face value — this scramble cost me 5 moves of DR leakage for 2 moves of EO savings, and I should have scouted the post-EO state across all three axes before committing.
