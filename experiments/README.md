# Experiment Pipeline

This directory contains scripts and configs for systematic validation of the Tikhonov agent.

## Overview

The pipeline has four stages:

```
generate_cases.py → run_benchmark.py → analyze_results.py → plot_results.py
```

## Benchmark Design

### Experimental factors

| Factor | Values (benchmark_v1) |
|---|---|
| Flux family | step, ramp, single_pulse, multi_pulse, smooth_sinusoid |
| Noise level | 0.1, 0.5, 1.0 K |
| Seeds | 42, 123 |
| Sensor count | 2 |
| Time resolution | 1.0 (default 121 steps) |

Total cases: 5 × 3 × 2 = **30 cases**

### Variants compared

| Variant | Lambda | Iterations | Replanning |
|---|---|---|---|
| `fixed_solver` | Fixed λ = 1.0 | 1 | No |
| `auto_solver` | L-curve / discrepancy | 1 | No |
| `solver_plus_verifier` | Auto + bounds | 1 | No |
| `full_agent` | Auto + bounds | up to 12 | Yes |

### Ablation study (ablation_v1)

Disables one component at a time vs `full_agent_baseline`:

- `no_replanner` — single iteration, no retries
- `no_bounds` — no physical bounds clamping
- `fixed_reg_order_0/2` — no regularisation-order switching
- `fixed_lambda_ablation` — no automatic lambda selection

### Stress tests (stress_v1)

Tests harder conditions:

- `high_noise` — 2–5 K noise
- `few_sensors` — single sensor only
- `distant_sensors` — sensors near the far boundary
- `low_time_resolution` — 31 time steps instead of 121
- `high_dimension` — 50 inversion parameters
- `wrong_noise_estimate` — noise underestimated in config

## Directory Structure

```
experiments/
├── __init__.py
├── configs/
│   ├── benchmark_v1.yaml     main benchmark
│   ├── ablation_v1.yaml      ablation study
│   └── stress_v1.yaml        stress tests
├── generate_cases.py
├── run_benchmark.py
├── analyze_results.py
├── plot_results.py
├── utils.py
└── README.md

experiments/cases/benchmark_v1/
├── manifest.csv
├── case_0001/
│   ├── config.yaml
│   ├── observations.csv
│   └── truth.npz
└── ...

experiments/runs/benchmark_v1/
├── results_raw.csv
├── results_summary_by_variant.csv
├── results_summary_by_noise.csv
├── results_summary_by_flux_family.csv
├── case_0001/
│   ├── fixed_solver/
│   │   ├── run_outputs/      agent reporter output
│   │   └── run_summary.npz   arrays for plotting
│   ├── auto_solver/
│   ├── solver_plus_verifier/
│   └── full_agent/
└── figures/
    ├── qualitative_flux_reconstruction_examples.png
    └── ...
```

## How to Generate Cases

```bash
# From the tikhonov_agent/ project root:
python experiments/generate_cases.py \
    --config experiments/configs/benchmark_v1.yaml

# Regenerate (overwrite existing):
python experiments/generate_cases.py \
    --config experiments/configs/benchmark_v1.yaml \
    --overwrite
```

## How to Run the Benchmark

```bash
# All variants:
python experiments/run_benchmark.py \
    --config experiments/configs/benchmark_v1.yaml \
    --variant all

# Single variant:
python experiments/run_benchmark.py \
    --config experiments/configs/benchmark_v1.yaml \
    --variant full_agent

# Quick smoke test (first 5 cases):
python experiments/run_benchmark.py \
    --config experiments/configs/benchmark_v1.yaml \
    --variant auto_solver \
    --limit 5

# Overwrite previous results:
python experiments/run_benchmark.py \
    --config experiments/configs/benchmark_v1.yaml \
    --variant all \
    --overwrite
```

## How to Analyze Results

```bash
python experiments/analyze_results.py \
    --input experiments/runs/benchmark_v1/results_raw.csv
```

Produces:
- `results_summary_by_variant.csv`
- `results_summary_by_noise.csv`
- `results_summary_by_flux_family.csv`
- `ablation_summary.csv` (if ablation variants present)

## How to Reproduce Main Figures

```bash
python experiments/plot_results.py \
    --input experiments/runs/benchmark_v1/results_raw.csv \
    --pdf
```

Figures are written to `experiments/runs/benchmark_v1/figures/`.

## Running Tests

```bash
# From project root:
pytest tests/test_case_generation.py -v
pytest tests/test_benchmark_runner.py -v
pytest tests/test_metrics_aggregation.py -v
```

## Metric Definitions

### Reconstruction metrics (vs ground truth)

| Metric | Definition |
|---|---|
| `flux_l2_error` | ‖q_true − q_est‖₂ [W/m²] |
| `flux_relative_l2_error` | ‖q_true − q_est‖₂ / ‖q_true‖₂ |
| `flux_rmse` | √( mean((q_true − q_est)²) ) |
| `flux_peak_error` | max |q_true − q_est| |
| `flux_correlation` | Pearson r between q_true and q_est |

### Forward replay metrics (vs observations)

| Metric | Definition |
|---|---|
| `replay_rmse` | RMSE of fitted temperatures vs observations |
| `replay_relative_error` | replay_rmse / signal_range |
| `replay_max_abs_error` | max |T_obs − T_fit| |

### Regularity / physical metrics

| Metric | Definition |
|---|---|
| `roughness_l1` | Σ|Δq_est| (total variation) |
| `roughness_l2` | ‖Δq_est‖₂ |
| `oscillation_score` | fraction of Δq sign changes |
| `sign_flip_count` | number of sign changes in q_est |
| `physical_violation_count` | number of q_est values outside [q_min, q_max] |
| `within_bounds_flag` | 1 if all estimates within bounds |

### Agent workflow metrics

| Metric | Definition |
|---|---|
| `final_decision` | pass / weak_pass / manual_review / fail |
| `success_flag` | 1 if pass or weak_pass |
| `iteration_count` | number of agent loop iterations |
| `replanning_count` | number of non-terminal replanning actions |
| `runtime_sec` | wall-clock seconds |
| `initial_to_final_improvement` | (first_rmse − last_rmse) / first_rmse |
| `final_lambda` | regularisation parameter at final iteration |
| `final_reg_order` | regularisation order at final iteration |
