# Corpus eval — sim mode on 4 scrambles

Model: `claude-sonnet-4-5-20250929`
Run: 2026-05-15T06:30:19

| ID | Result | Sim moves | Analyzer baseline | Gap | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| scramble1 | ✗ | — | 30 | — | 60 | 885s | 1169s | $0.17 |
| scramble2 | ✓ | 35 | 25 | 10 | 58 | 296s | 486s | $0.22 |
| scramble3 | ✗ | — | 31 | — | 60 | 760s | 965s | $0.20 |
| scramble5 | ✓ | 33 | 33 | 0 | 58 | 1014s | 962s | $0.20 |
| random1 | ✗ | — | ? | — | 60 | 711s | 1024s | $0.19 |
| random2 | ✓ | 26 | ? | ? | 16 | 202s | 189s | $0.06 |
| random3 | ✓ | 31 | ? | ? | 19 | 346s | 393s | $0.08 |
| random4 | ✗ | — | ? | — | 60 | 528s | 564s | $0.24 |
| random5 | ✓ | 30 | ? | ? | 32 | 631s | 623s | $0.13 |
| random6 | ✗ | — | ? | — | 60 | 758s | 950s | $0.19 |

**Solved**: 5/10
**Avg sim moves (solved)**: 31.0
**Avg analyzer baseline (solved)**: 11.6
**Avg gap (solved)**: 19.4
**Total API cost (rough, no cache discount)**: $1.70

## Per-scramble narratives
- [scramble1](scramble1_20260515_042815.md)
- [scramble2](scramble2_20260515_044744.md)
- [scramble3](scramble3_20260515_045550.md)
- [scramble5](scramble5_20260515_051155.md)
- [random1](random1_20260515_052757.md)
- [random2](random2_20260515_054501.md)
- [random3](random3_20260515_054810.md)
- [random4](random4_20260515_055443.md)
- [random5](random5_20260515_060407.md)
- [random6](random6_20260515_061430.md)
