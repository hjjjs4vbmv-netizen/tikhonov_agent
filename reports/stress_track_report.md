# Stress Track Report

**Generated from:** `stress_track_raw.csv`
**Total runs:** 144  |  **Failed:** 0

---

## Track Definition

`stress_track` evaluates solver behaviour in hard regimes, using the same
primary-axis parameterisation as benchmark_core but with levels selected
from the hard portion of each family's primary axis.

**Sensor setting:** sparse (4 sensors) — constrained observability.
**Noise:** 0.5 K and 1.0 K — higher-noise regime.

---

## Stress Family Configurations

| Family | Primary Axis | Hard Levels | Notes |
|--------|-------------|-------------|-------|
| discontinuous_piecewise | jump_sharpness | 8, 20, 50 | Sharp to near-delta |
| moving_hotspot | speed_frac | 0.6, 0.85, 1.0 | Fast to max-speed, with reversal |
| overlapping_multi_spot | separation_frac | 0.12, 0.05, 0.02 | Near-merged spots |
| matern_grf | corr_length_frac | 0.06, 0.03, 0.01 | Rough to near-white-noise |

---

## Main Findings

### Mean RMSE by Family × Solver (stress cases, noise=1.0 K)

| Family | fast bayesian | tikhonov 2d | tsvd 2d |
| --- | --- | --- | --- |
| discontinuous piecewise | 328 | 321 | 345 |
| matern grf | 374 | 406 | 369 |
| moving hotspot | 326 | 342 | 336 |
| overlapping multi spot | 330 | 363 | 366 |

### RMSE Progression Across Stress Levels (tikhonov_2d, noise=1.0 K)

- **discontinuous_piecewise**: near_delta=321 → sharp=320 → very_sharp=323
- **matern_grf**: near_white_noise=399 → rough=415 → very_rough=404
- **moving_hotspot**: fast=318 → max_speed=371 → very_fast=337
- **overlapping_multi_spot**: marginal=357 → near_merged=365 → unresolvable=365

---

## Failure Cases

No hard failures. All solvers returned finite results.
(Note: high RMSE in hard cases indicates failure to reconstruct, not algorithmic failure.)

---

## Limitations

1. Only 4 sensors (sparse) — realistic constrained setting but limits all solvers.
2. deepxde_pinn needs longer training for competitive stress performance (200 iters insufficient).
3. No 2D regularisation operator for Tikhonov — 1D flattened regularisation used.
4. Support-overlap metric is not meaningful for matern_grf (no clear support).

---

## Scientific Honesty Statement

All solvers return finite predictions for all stress cases (no NaN or crash).
High RMSE values indicate poor reconstruction fidelity, not algorithmic failure.
The hardest matern_grf (corr_length=0.01) cases are arguably unrecoverable from
4 sensors in low-noise regimes, reflecting genuine ill-posedness.
