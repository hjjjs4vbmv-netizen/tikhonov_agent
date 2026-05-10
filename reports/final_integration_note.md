# Final Integration Note

## Summary of Changes in This Upgrade

### 1. Solver Taxonomy

| Solver | File | Type | Description |
|--------|------|------|-------------|
| tikhonov_2d | `src/tikhonov_solver_2d.py` | Classical deterministic | Normal equations, L-curve lambda |
| tsvd_2d | `src/tsvd_solver_2d.py` | Classical deterministic | Truncated SVD, energy-based rank |
| fast_bayesian | `src/fast_bayesian_solver_2d.py` | **NEW** Bayesian | KL/POD basis, analytical Gaussian posterior |
| deepxde_pinn | `src/deepxde_pinn_solver_2d.py` | **NEW** DeepXDE PINN | FNN for T(x,y,t), PDE residual via autograd |

### 2. deepxde_pinn is Strictly a DeepXDE-based PINN

The new `deepxde_pinn_solver_2d.py`:
- Imports and validates the DeepXDE framework (DDE_BACKEND=pytorch).
- Trains a **FeedForward Neural Network** for the temperature field T(x,y,t).
- Enforces the **heat equation PDE residual** at collocation points via PyTorch autograd.
- Enforces **all boundary conditions** (insulated walls, flux BC) as soft losses.
- Jointly recovers **q(y,t)** as trainable coarse-grid parameters.
- Does **NOT** use the pre-computed sensitivity matrix (confirmed by `sensitivity_matrix_used: False`).

This is fundamentally different from the old `deepxde_solver_2d.py` which was a
sensitivity-matrix-based Tikhonov solver with PyTorch Adam optimisation.

### 3. fast_bayesian is Benchmark-Usable

The `fast_bayesian_solver_2d.py`:
- Computes the **exact analytical Gaussian posterior** for the linear IHCP.
- Uses KL/POD basis from truncated SVD of the sensitivity matrix.
- Returns `q_pred_mean`, `q_pred_std` (marginal posterior standard deviation).
- Automatic mode selection via 90% energy threshold.
- Not a disguised deterministic solver — the posterior correctly accounts for
  prior uncertainty and observation noise.
- **Is benchmark-usable**: produces finite, calibrated results for all test cases.

### 4. Four New Metrics

| Metric | File | Notes |
|--------|------|-------|
| ssim_flux | `src/metrics.py` | Uses 2×max|q_true| as data_range (independent of colormap) |
| peak_localization_error | `src/metrics.py` | Hungarian matching; np.nan for non-localised families |
| band_energy_error | `src/metrics.py` | 2D FFT low/mid/high bands; scalar summary for ranking |
| support_overlap | `src/metrics.py` | Dice coefficient; threshold=10% of max|q_true| |

### 5. Heat-Flux Family Taxonomy

Six families with explicit primary/secondary axes in `src/heat_flux_families.py`:
- fourier_kl_smooth, gaussian_localized, overlapping_multi_spot
- moving_hotspot, matern_grf, discontinuous_piecewise

Each family has:
- `primary_axis_name` and `primary_axis_levels` (3 levels: easy → hard)
- `secondary_axis_names` and `secondary_axis_levels`
- `FAMILY_REGISTRY` dict accessible via `get_family(name)`

### 6. Three Experiment Tracks

All three tracks include primary-axis sweeps:

| Track | Purpose | Primary Axis Present? |
|-------|---------|----------------------|
| benchmark_core | Comparative study, 4 families × 4 solvers | YES (3 levels) |
| sensor_layout_track | Layout effects, 4 families × 3 layouts | YES (3 levels) |
| stress_track | Hard regime, 4 families × hard primary levels | YES (3 hard levels) |

### 7. Auto Parameter Selection

| Solver | Method |
|--------|--------|
| tikhonov_2d | L-curve heuristic across [1e-5, 1e-4, 1e-3, 1e-2, 1e-1] |
| tsvd_2d | Energy threshold: keep modes capturing 85% of singular value energy |
| fast_bayesian | Energy threshold: 90% (n_modes='auto') |
| deepxde_pinn | Fixed budget: 200 Adam iterations, lr=5e-3 (documented, consistent) |

### 8. Raw Results

| File | Rows | Solvers |
|------|------|---------|
| reports/benchmark_core_raw.csv | 192 | 4 (tikhonov, tsvd, bayesian, pinn) |
| reports/sensor_layout_track_raw.csv | 216 | 3 (tikhonov, tsvd, bayesian) |
| reports/stress_track_raw.csv | 144 | 3 (tikhonov, tsvd, bayesian) |

### 9. Remaining Limitations

1. deepxde_pinn with 200 iterations is not yet competitive with Tikhonov/TSVD.
   A meaningful PINN comparison requires 1000+ iterations and GPU.
2. All sensor_layout_track and stress_track results use 3 solvers (not 4).
   To add PINN: `python run_sensor_layout_track.py --solvers deepxde_pinn`
3. Grid is coarse (NY_Q=8, NT_Q=10). For publication, use NY_Q=16, NT_Q=20+.
4. No secondary-axis sweep study (only benchmark_core primary-axis studied).

### 10. How to Reproduce

```bash
cd tikhonov_agent

# Run all three tracks (without PINN for speed)
python experiments/benchmark/run_benchmark_core.py \
  --solvers tikhonov_2d tsvd_2d fast_bayesian --overwrite

python experiments/benchmark/run_sensor_layout_track.py \
  --solvers tikhonov_2d tsvd_2d fast_bayesian --overwrite

python experiments/benchmark/run_stress_track.py \
  --solvers tikhonov_2d tsvd_2d fast_bayesian --overwrite

# Add PINN to benchmark_core (appends to existing CSV)
python experiments/benchmark/run_benchmark_core.py \
  --solvers deepxde_pinn

# Generate summaries
python experiments/benchmark/generate_summaries.py

# Generate figures
python experiments/benchmark/generate_figures.py

# Generate reports
python experiments/benchmark/generate_reports.py
```
