# FMC Analyzer Baseline Benchmark

## Config

- **corpus**: `data/raw/wca.jsonl`
- **ckpt**: `checkpoints/policy_best.pt`
- **n**: `10`
- **seed**: `0`
- **time_budget_s**: `1200.0`
- **workers**: `1`
- **device**: `cuda`
- **eo_beam**: `256`
- **eo_depth**: `10`
- **dr_beam**: `2048`
- **dr_depth**: `10`

## Aggregate Results

- **scrambles run**: 10
- **completed (no timeout/error)**: 7 (70.0%)
- **timed out**: 3
- **errored**: 0

- **full-solve rate (top-1)**: 7/10 = **70.0%**
- **full-solve rate (any candidate)**: 7/10 = **70.0%**

### Move counts on successful solves (top-1)

- **mean**: 32.7
- **median**: 33.0
- **min / max**: 24 / 40
- **shortest-among-candidates mean**: 32.7

### Stages reached (count of scrambles)

| stages | n |
|---|---|
| 4 | 7 |

### Comparison to human reconstructions

- **scrambles with full solve + human length**: 7
- **beats human**: 2/7 (28.6%)
- **mean delta (analyzer − human)**: +3.9
- **median delta**: +9.0

### Wall time

- **mean**: 951.1s
- **median**: 935.3s
- **max**: 1200.0s

## Per-scramble Results

| # | id | human | stages | top-1 | shortest | full? | wall (s) | notes |
|---|---|---|---|---|---|---|---|---|
| 0 | `wca:3209:498:47540` | 22 | — | — | — | ✗ | 1200.0 | TIMEOUT |
| 1 | `wca:3125:635:49991` | 22 | EO→DR→HTR→F | 35 | 35 | ✓ | 773.4 |  |
| 2 | `wca:3449:629:50750` | 28 | — | — | — | ✗ | 1200.0 | TIMEOUT |
| 3 | `wca:3215:473:47420` | 22 | EO→DR→HTR→F | 40 | 40 | ✓ | 732.4 |  |
| 4 | `wca:2928:909:45348` | 50 | EO→DR→HTR→F | 29 | 29 | ✓ | 1122.9 |  |
| 5 | `wca:3002:501:45868` | 20 | EO→DR→HTR→F | 33 | 33 | ✓ | 841.2 |  |
| 6 | `wca:3207:28:47498` | 25 | — | — | — | ✗ | 1200.0 | TIMEOUT |
| 7 | `wca:3215:670:47462` | 31 | EO→DR→HTR→F | 40 | 40 | ✓ | 736.3 |  |
| 8 | `wca:2925:635:45843` | 20 | EO→DR→HTR→F | 24 | 24 | ✓ | 674.9 |  |
| 9 | `wca:3215:393:48406` | 37 | EO→DR→HTR→F | 28 | 28 | ✓ | 1029.5 |  |
