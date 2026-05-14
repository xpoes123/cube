# FMC Analyzer Baseline Benchmark

## Config

- **corpus**: `data/raw/wca.jsonl`
- **ckpt**: `checkpoints/policy_best.pt`
- **n**: `10`
- **seed**: `0`
- **time_budget_s**: `300.0`
- **workers**: `4`
- **device**: `cpu`
- **eo_beam**: `256`
- **eo_depth**: `10`
- **dr_beam**: `8192`
- **dr_depth**: `14`

## Aggregate Results

- **scrambles run**: 10
- **completed (no timeout/error)**: 3 (30.0%)
- **timed out**: 7
- **errored**: 0

- **full-solve rate (top-1)**: 0/10 = **0.0%**
- **full-solve rate (any candidate)**: 0/10 = **0.0%**

### Stages reached (count of scrambles)

| stages | n |
|---|---|
| 1 | 2 |
| 2 | 1 |

### Wall time

- **mean**: 282.2s
- **median**: 300.0s
- **max**: 300.0s

## Per-scramble Results

| # | id | human | stages | top-1 | shortest | full? | wall (s) | notes |
|---|---|---|---|---|---|---|---|---|
| 0 | `wca:3209:498:47540` | 22 | — | — | — | ✗ | 300.0 | TIMEOUT |
| 1 | `wca:3125:635:49991` | 22 | — | — | — | ✗ | 300.0 | TIMEOUT |
| 2 | `wca:3449:629:50750` | 28 | — | — | — | ✗ | 300.0 | TIMEOUT |
| 3 | `wca:3215:473:47420` | 22 | EO | 8 | — | ✗ | 287.1 |  |
| 4 | `wca:2928:909:45348` | 50 | — | — | — | ✗ | 300.0 | TIMEOUT |
| 5 | `wca:3002:501:45868` | 20 | — | — | — | ✗ | 300.0 | TIMEOUT |
| 6 | `wca:3207:28:47498` | 25 | — | — | — | ✗ | 300.0 | TIMEOUT |
| 7 | `wca:3215:670:47462` | 31 | EO | 8 | — | ✗ | 272.4 |  |
| 8 | `wca:2925:635:45843` | 20 | EO→DR | 14 | — | ✗ | 162.9 |  |
| 9 | `wca:3215:393:48406` | 37 | — | — | — | ✗ | 300.0 | TIMEOUT |
