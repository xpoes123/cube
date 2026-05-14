# Hand-picked scramble results

All on single 4060 GPU. NISS on (default) unless noted.

## Scramble 1 — `R' U' F L' R U2 F2 L2 R U2 L B2 R' U' L2 F L' U2 R F2 R B' R' U' F`

**30 moves** via NISS rescue (entire pipeline on inverse side, since
normal-side DR is structurally >=7 moves over EO-preserving at width 8192).

```
[ EO (UD) [inv] ]  4 moves   F' B R F
[ DR (UD) [inv] ]  7 moves   B2 U F2 D' U F2 R          (+10→HTR)
[ HTR (UD) [inv] ] 10 moves  L2 U' L2 U R2 U' R2 U L2 D
[ Finish        ] 10 moves   D2 F2 U2 B2 L2 F2 L2 F2 D2 R2
```

Search time: 941s (NISS on, full).

## Scramble 2 — `R' U' F B' U2 F' U2 R2 B' R2 B' R2 U2 R2 F' L U2 B D R F L2 F D' R' U' F`

**25 moves** (cancellation saved 2 from 27 raw), normal-side baseline.

```
[ EO (UD) ]  4 moves    R B D' B'
[ DR (UD) ]  8 moves    B2 U' B2 R F2 R' F2 R     (+4→HTR)
[ HTR (UD) ]  7 moves   R2 U R2 B2 U2 L2 U
[ Finish ]   8 moves    B2 U2 F2 U2 F2 R2 D2 L2
```

Solution: `R B D' B U' B2 R F2 R' F2 R' U R2 B2 U2 L2 U B2 U2 F2 U2 F2 R2 D2 L2`

Search time: 1537s (NISS on, full).

## Scramble 3 — `R' U' F R2 B2 D2 R F2 L D2 B2 R B2 U2 R F' L D' B U B' R' F' D' R' U' F`

**31 moves** (cancellation saved 1), required multi-axis HTR fix. Best DR is on RL axis, not UD.

```
[ EO (RL) ]  5 moves    D R B L' U'
[ DR (RL) ]  8 moves    B L B' L B' R D2 F        (+5→HTR)
[ HTR (RL) ]  7 moves   U2 R' U2 F2 R D2 R
[ Finish ]  12 moves    R2 F2 R2 F2 U2 B2 U2 R2 F2 L2 F2 R2
```

Search time: 643s (NISS on, full).

## Random WCA scramble (corpus #5: `wca:3002:501:45868`)

**33 moves** with `--fast` (no NISS, dr-beam=2048, dr-depth=10).

Scramble: `R' U' F R D' B2 R2 D' L2 D2 L2 B2 U2 F U' L B R' F U F D2 R' U' F`
Human reconstruction: 20 moves.

```
[ EO (RL) ]   4 moves   U L F' U'
[ DR (RL) ]  12 moves   F' L F' F2 L' D2 R2 D2 L2 F R2 F   (+10→HTR)
[ HTR (RL) ] 10 moves   B2 R' B2 R D2 R' D2 R D2 L
[ Finish ]   8 moves    D2 L2 U2 B2 D2 B2 L2 U2
```

Search time: 317s with `--fast`. We're 13 moves above the human; expected
since human used insertions and NISS extensively. Insertions are M3 work.

## Performance summary

| Scramble | Mode | Search time | Moves |
|---|---|---|---|
| 1 (test) | NISS-on | 941s | 30 |
| 2 (test) | NISS-on | 1537s | 25 |
| 3 (test) | NISS-on | 643s | 31 |
| 5 (random) | --fast | 317s | 33 |

NISS roughly 3-5× the wall time. For routine triage `--fast` is the
working setting; for best quality, use NISS-on with a generous budget.
