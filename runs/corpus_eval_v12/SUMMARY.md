# Corpus eval — sim mode on 5 scrambles

Model: `claude-sonnet-4-5-20250929`
Run: 2026-05-16T02:44:57

| ID | Result | Sim moves | Human (WCA) | Gap | Solver | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| fm_PSSSideDayGdansk2026_s1 | ✓ | 30 | 20 | 10 | Marcin Chmielewski | 35 | 118s | 148s | $0.14 |
| fm_PSSSideDayGdansk2026_s2 | ✓ | 30 | 20 | 10 | Marcin Chmielewski | 52 | 209s | 192s | $0.16 |
| fm_PSSSideDayGdansk2026_s3 | ✓ | 27 | 23 | 4 | Marcin Chmielewski | 36 | 117s | 125s | $0.14 |
| fm_BackiPetrovacOpen2026_s1 | ✓ | 32 | 22 | 10 | Szabolcs Szántai | 33 | 108s | 128s | $0.14 |
| fm_WesternSicilyOpen2026_s1 | ✓ | 28 | 19 | 9 | Chiara Marcucci | 39 | 116s | 154s | $0.17 |

**Solved**: 5/5
**Avg sim moves (solved)**: 29.4
**Avg human (WCA) (solved)**: 20.8
**Avg gap (solved)**: +8.6
**Total API cost (rough, no cache discount)**: $0.75

## Human reconstructions (for comparison)

### fm_PSSSideDayGdansk2026_s1 — Marcin Chmielewski (20 moves)
```
R2 D F B' L B2 R D2 L' D' L D2 F2 B2 R' U2 R2 U2 L B2
```
Annotation:
```
R2 D F B' // EO
L B2 R D2 L' D' // 2c3 2e (10)
(B2 L' U2 R2 U2 R F2 B2 D2 L') // solve directly (20)
```

### fm_PSSSideDayGdansk2026_s2 — Marcin Chmielewski (20 moves)
```
U F2 D' B2 U D B2 L2 B2 U2 L2 B' D' F' U' B2 U B' R' U2
```
Annotation:
```
(U2 R) // EO
(B U' B2 U F D B) // 4b2 2e (9)
U F2 U' // HTR (12)
L2 U2 B2 L2 B2 U2 L2 // slice (19), +1

Found in 20 minutes, didn't feel enough as the scramble was so good
Missed a fairly easy 18 from exending different 9+2 into 10+2 which I was really close finding to
```

### fm_PSSSideDayGdansk2026_s3 — Marcin Chmielewski (23 moves)
```
R F D L' F R2 U' D2 F' L2 F L2 U' R L D2 R' L' F2 U' D' F2 D
```
Annotation:
```
R F D L' // EO
F R2 U' D2 F' L2 F // DR 4a2 4e (11)
L2 U (U)  // HTR (14)
(F2 U2 R' L D2 R' L') // slice (22), +1

Not perfect but could've went much worse
```

### fm_BackiPetrovacOpen2026_s1 — Szabolcs Szántai (22 moves)
```
U F2 U D' L B2 F2 L2 Dw R2 L2 F2 U' Uw2 B2 Uw' B2 R B D' U' B'
```
Annotation:
```
(B U D B') // EO
(R'), U F2 U D' L // DR in 10 2c3 6e
(B2 U* B2 U'% F2 L2 R2 D'*) // HTR in 18
(L2 F2 B2) // slice in 21

*= w, %=E2 // +1 rewrite
```

### fm_WesternSicilyOpen2026_s1 — Chiara Marcucci (19 moves)
```
L' U2 F2 U2 L F2 L F2 U2 L2 D' R2 D L2 R' D R F L
```
Annotation:
```
(L' F') //eo (2/2)
(L' D' R L2 D' R2 D) //dr 4a1 (7/9)
L' (L2 U2 F2 L' F2 L) //htr (7/16)
(U2 F2 U2) //finish (3/19)

I only tried this EO and only this DR. 
After 10 minutes I had a 20.
```

## Per-scramble narratives
- [fm_PSSSideDayGdansk2026_s1](fm_PSSSideDayGdansk2026_s1_20260516_023229.md)
- [fm_PSSSideDayGdansk2026_s2](fm_PSSSideDayGdansk2026_s2_20260516_023457.md)
- [fm_PSSSideDayGdansk2026_s3](fm_PSSSideDayGdansk2026_s3_20260516_023809.md)
- [fm_BackiPetrovacOpen2026_s1](fm_BackiPetrovacOpen2026_s1_20260516_024015.md)
- [fm_WesternSicilyOpen2026_s1](fm_WesternSicilyOpen2026_s1_20260516_024223.md)
