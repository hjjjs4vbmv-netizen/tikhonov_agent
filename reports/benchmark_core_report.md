# Benchmark Core Track Report

**Generated from:** `benchmark_core_raw.csv`
**Total runs:** 192  |  **Successful:** 192  |  **Failed:** 0

---

## Track Definition

`benchmark_core` is the main comparative study across four heat-flux families.
Each family's **primary axis** is swept across 3 levels (easy → hard) while
secondary axes are held at representative mid-level values.

---

## Families

| Family | Support Type | Primary Axis | Level 0 | Level 1 | Level 2 |
|--------|-------------|--------------|---------|---------|---------|
| fourier_kl_smooth | global | n_modes | 2 | 4 | 8 |
| gaussian_localized | localised | sigma_y_frac | 0.05 (sharp) | 0.15 | 0.30 (broad) |
| overlapping_multi_spot | multi-peak | separation_frac | 0.45 (separated) | 0.20 | 0.07 (merged) |
| matern_grf | stochastic | corr_length_frac | 0.30 (smooth) | 0.12 | 0.04 (rough) |

**Secondary axes:** fixed at mid level for all benchmark_core runs.

---

## Solver Definitions

| Solver | Type | Auto Parameter |
|--------|------|----------------|
| tikhonov_2d | Tikhonov normal equations | λ via L-curve heuristic |
| tsvd_2d | Truncated SVD | rank via 85% energy threshold |
| fast_bayesian | Analytical Gaussian posterior on KL/POD basis | n_modes via 90% energy threshold |
| deepxde_pinn | DeepXDE-based PINN (FNN + PDE residual) | fixed budget: 200 iters, lr=5e-3 |

**Note:** deepxde_pinn is the only solver that does NOT use the pre-computed
sensitivity matrix. It trains a neural network T_NN(x,y,t) jointly with
flux parameters q(y,t), enforcing the PDE residual via autograd.

---

## Metrics Definitions

| Metric | Description |
|--------|-------------|
| rmse_flux | Root-mean-square error between predicted and true q [W/m²] |
| ssim_flux | Structural similarity index on the flux field (1=identical, range-normalised to max|q_true|) |
| peak_localization_error | Avg. matched peak distance in normalised coords (np.nan for smooth families) |
| band_error_scalar | Mean relative energy error across low/mid/high frequency bands |
| support_overlap | Dice coefficient of active-support regions (threshold=10% of max|q_true|) |

---

## Main Findings

### RMSE by Family × Solver (mean across noise=0.1 K)

| Family | deepxde pinn | fast bayesian | tikhonov 2d | tsvd 2d |
| --- | --- | --- | --- | --- |
| fourier kl smooth | 432 | 231 | 383 | 243 |
| gaussian localized | 253 | 49.3 | 159 | 85.5 |
| matern grf | 388 | 376 | 396 | 379 |
| overlapping multi spot | 338 | 113 | 223 | 144 |

### SSIM by Family × Solver (mean across noise=0.1 K)

| Family | deepxde pinn | fast bayesian | tikhonov 2d | tsvd 2d |
| --- | --- | --- | --- | --- |
| fourier kl smooth | 0.00739 | 0.775 | 0.23 | 0.78 |
| gaussian localized | 0.000898 | 0.943 | 0.605 | 0.88 |
| matern grf | 0.00386 | 0.142 | 0.0448 | 0.0883 |
| overlapping multi spot | 0.00123 | 0.891 | 0.632 | 0.835 |

### RMSE Trend Across Primary-Axis Levels (tikhonov_2d, noise=0.1 K)

- **fourier_kl_smooth**: level0=396 → level1=388 → level2=364
- **gaussian_localized**: level0=78 → level1=168 → level2=231
- **matern_grf**: level0=396 → level1=410 → level2=381
- **overlapping_multi_spot**: level0=177 → level1=234 → level2=257

### Best Solver by Family (lowest mean RMSE, noise=0.1 K)

- **fourier_kl_smooth**: fast_bayesian
- **gaussian_localized**: fast_bayesian
- **matern_grf**: fast_bayesian
- **overlapping_multi_spot**: fast_bayesian

---

## Failure Cases

No failures recorded.

---

## Limitations

1. **PINN training budget**: deepxde_pinn uses 200 Adam iterations (≈3s/call on CPU).
   Longer training would improve results. The PINN is included to demonstrate the
   PINN approach and its current limitation vs. direct linear solvers.
2. **Grid resolution**: NY_Q=8, NT_Q=10 provides fast experiments; higher resolution
   would improve reconstruction fidelity for all solvers.
3. **Secondary axis study**: Not conducted in benchmark_core (fixed at mid level).
   Secondary-axis variation is studied in sensor_layout_track.
4. **No 3D extension**: all experiments are 2D (y, t) boundary flux recovery.

---

## Recommended Next Steps

1. Run with `--solvers deepxde_pinn` and longer PINN budget (n_iter=1000+) for competitive PINN results.
2. Extend to higher-resolution grids (NY_Q=16, NT_Q=20).
3. Study secondary-axis effects via the sensor_layout_track secondary-axis config.
4. Add cross-validation lambda selection for Tikhonov (currently L-curve heuristic).
