# FMC Analyzer Baseline Benchmark

## Config

- **corpus**: `data/raw/wca.jsonl`
- **ckpt**: `checkpoints/policy_best.pt`
- **n**: `10`
- **seed**: `0`
- **time_budget_s**: `600.0`
- **workers**: `1`
- **device**: `cuda`
- **eo_beam**: `256`
- **eo_depth**: `10`
- **dr_beam**: `2048`
- **dr_depth**: `10`

## Aggregate Results

- **scrambles run**: 10
- **completed (no timeout/error)**: 9 (90.0%)
- **timed out**: 1
- **errored**: 0

- **full-solve rate (top-1)**: 5/10 = **50.0%**
- **full-solve rate (any candidate)**: 5/10 = **50.0%**

### Move counts on successful solves (top-1)

- **mean**: 31.0
- **median**: 31.0
- **min / max**: 27 / 36
- **shortest-among-candidates mean**: 31.0

### Stages reached (count of scrambles)

| stages | n |
|---|---|
| 1 | 4 |
| 4 | 5 |

### Comparison to human reconstructions

- **scrambles with full solve + human length**: 5
- **beats human**: 2/5 (40.0%)
- **mean delta (analyzer − human)**: +5.0
- **median delta**: +11.0

### Wall time

- **mean**: 396.5s
- **median**: 372.4s
- **max**: 600.0s

## Per-scramble Results

| # | id | human | stages | top-1 | shortest | full? | wall (s) | notes |
|---|---|---|---|---|---|---|---|---|
| 0 | `wca:3209:498:47540` | 22 | — | — | — | ✗ | 600.0 | TIMEOUT |
| 1 | `wca:3125:635:49991` | 22 | EO | 8 | — | ✗ | 307.7 |  |
| 2 | `wca:3449:629:50750` | 28 | EO→DR→HTR→F | 27 | 27 | ✓ | 560.0 |  |
| 3 | `wca:3215:473:47420` | 22 | EO | 8 | — | ✗ | 270.4 |  |
| 4 | `wca:2928:909:45348` | 50 | EO | 3 | — | ✗ | 419.1 |  |
| 5 | `wca:3002:501:45868` | 20 | EO→DR→HTR→F | 33 | 33 | ✓ | 325.7 |  |
| 6 | `wca:3207:28:47498` | 25 | EO→DR→HTR→F | 36 | 36 | ✓ | 533.7 |  |
| 7 | `wca:3215:670:47462` | 31 | EO | 8 | — | ✗ | 272.9 |  |
| 8 | `wca:2925:635:45843` | 20 | EO→DR→HTR→F | 31 | 31 | ✓ | 192.9 |  |
| 9 | `wca:3215:393:48406` | 37 | EO→DR→HTR→F | 28 | 28 | ✓ | 483.1 |  |
