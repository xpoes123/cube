# Corpus eval — sim mode on 4 scrambles

Model: `claude-sonnet-4-5-20250929`
Run: 2026-05-15T19:53:01

| ID | Result | Sim moves | Analyzer baseline | Gap | Tool calls | Sim time | Wall | Cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| scramble1 | ✗ | — | 30 | — | 60 | 357s | 909s | $0.21 |
| scramble2 | ✓ | 32 | 25 | 7 | 16 | 152s | 357s | $0.07 |
| scramble3 | ✓ | 27 | 31 | -4 | 31 | 241s | 609s | $0.14 |
| scramble5 | ✓ | 35 | 33 | 2 | 16 | 155s | 303s | $0.07 |
| random1 | ✗ | — | ? | — | 60 | 658s | 1180s | $0.20 |
| random2 | ✓ | 26 | ? | ? | 16 | 132s | 234s | $0.06 |
| random3 | ✗ | — | ? | — | 60 | 430s | 896s | $0.20 |
| random4 | ✗ | — | ? | — | 60 | 427s | 799s | $0.20 |
| random5 | ✓ | 31 | ? | ? | 16 | 137s | 257s | $0.07 |
| random6 | ✗ | — | ? | — | 60 | 442s | 986s | $0.20 |

**Solved**: 5/10
**Avg sim moves (solved)**: 30.2
**Avg analyzer baseline (solved)**: 17.8
**Avg gap (solved)**: 12.4
**Total API cost (rough, no cache discount)**: $1.42

## Per-scramble narratives
- [scramble1](scramble1_20260515_180411.md)
- [scramble2](scramble2_20260515_181920.md)
- [scramble3](scramble3_20260515_182517.md)
- [scramble5](scramble5_20260515_183526.md)
- [random1](random1_20260515_184029.md)
- [random2](random2_20260515_190009.md)
- [random3](random3_20260515_190403.md)
- [random4](random4_20260515_191859.md)
- [random5](random5_20260515_193218.md)
- [random6](random6_20260515_193635.md)
