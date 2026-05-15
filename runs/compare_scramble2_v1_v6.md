# Compare — `scramble2_20260515_022748.json` vs `scramble2_20260515_034538.json`

**Scramble**:
`R' U' F B' U2 F' U2 R2 B' R2 B' R2 U2 R2 F' L U2 B D R F L2 F D' R' U' F`

| Metric | Left | Right |
|---|---|---|
| Result | ✓ | ✓ |
| Moves | 33 | 33 |
| Tool calls | 15 | 16 |
| Sim time | 149s | 154s |
| Wall | 276s | 282s |
| Input tokens | 77,642 | 123,650 |
| Cached tokens | 0 | 0 |
| Output tokens | 2,361 | 2,479 |
| Cost (est.) | — | $0.408 |
| Halt | — | — |

**Left solution** (33m): `R B D' B L B2 U L' U D' R D' R U L2 U R2 U2 R2 B2 U' R2 U' B2 D2 R2 B2 L2 F2 U2 R2 F2 U2`  
**Right solution** (33m): `R B D' B L B2 U L' U D' R D' R U L2 U R2 U2 R2 B2 U' R2 U' B2 D2 R2 B2 L2 F2 U2 R2 F2 U2`

## Tool-call sequences

Left: 15 calls — `inspect_state, lookahead, lookahead, lookahead, probe_dr_after_eo, probe_dr_after_eo, apply_moves, find_dr_via_trigger, apply_moves, htr_subset, lookup_subset_finish, apply_moves, cancel, verify_solved, budget_status`

Right: 16 calls — `inspect_state, lookahead, lookahead, lookahead, probe_dr_after_eo, probe_dr_after_eo, apply_moves, find_dr_via_trigger, apply_moves, htr_subset, lookup_subset_finish, apply_moves, inspect_state, cancel, verify_solved, budget_status`

**Divergence at tool #13** (1-indexed):
- Left:  `cancel({"moves":["R","B","D'","B","L","B2","U","L'","U","D'","R","D'","R","U","L2","...)`
- Right: `inspect_state({"slot":"main"})`
