"""
run_benchmark_2d_v1.py
======================
Benchmark runner for the 2D Inverse Heat Conduction Problem (IHCP).

Benchmark axes
--------------
    target_type  ∈ {smooth, localized, multi_spot}   — solution complexity
    noise        ∈ {0.1, 0.5, 1.0} K                  — data corruption level
    sensor_config∈ {sparse(2×2), medium(3×3), dense(4×4)}  — observability
    seed         ∈ {0, 1}                              — noise realisation

Total: 3 × 3 × 3 × 2 = 54 cases.

Usage
-----
    cd tikhonov_agent
    python scripts/run_benchmark_2d_v1.py

    # Quick smoke test (first 6 cases only)
    python scripts/run_benchmark_2d_v1.py --limit 6

    # Custom output path
    python scripts/run_benchmark_2d_v1.py --output reports/my_run.csv

Output
------
    reports/benchmark_2d_v1_results.csv
        Columns: target_type, noise, sensor_config, seed,
                 solver_name, rmse, convergence_flag
"""

from __future__ import annotations

import argparse
import csv
import itertools
import logging
import sys
import time
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Path setup: run from tikhonov_agent/ or project root
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.forward.heat2d_simulator import (  # noqa: E402
    DEFAULT_LX, DEFAULT_LY, DEFAULT_ALPHA, DEFAULT_K,
    DEFAULT_T0, DEFAULT_T_TOTAL, DEFAULT_Q_MAX,
    DEFAULT_NX, DEFAULT_NY,
    HeatConduction2DFD,
    generate_flux_2d,
    generate_sensor_grid,
)
from src.deepxde_solver_2d import solve_2d  # noqa: E402

log = logging.getLogger("benchmark_2d_v1")


# ---------------------------------------------------------------------------
# Benchmark configuration
# ---------------------------------------------------------------------------

TARGET_TYPES   = ["smooth", "localized", "multi_spot"]
NOISE_LEVELS   = [0.1, 0.5, 1.0]          # K
SENSOR_CONFIGS = ["sparse", "medium", "dense"]
SEEDS          = [0, 1]

# Solver configuration
NY_Q = 10    # coarse flux grid: y-points
NT_Q = 20    # coarse flux grid: t-points
OBS_EVERY = 5  # observe every 5th internal step (≈20 observation times for 101 steps)
LAM   = 1e-4   # Tikhonov regularisation weight
N_ITER = 500   # Adam iterations per case (sufficient after warm-up)
LR    = 10.0   # Adam learning rate (scaled for the small S entries ~1e-3)


# ---------------------------------------------------------------------------
# Simulator factory (shared across cases — properties are fixed)
# ---------------------------------------------------------------------------

def _make_simulator() -> HeatConduction2DFD:
    """Create the shared 2D FD simulator with benchmark defaults."""
    return HeatConduction2DFD(
        Lx=DEFAULT_LX,
        Ly=DEFAULT_LY,
        nx=DEFAULT_NX,
        ny=DEFAULT_NY,
        alpha=DEFAULT_ALPHA,
        k=DEFAULT_K,
    )


# ---------------------------------------------------------------------------
# Per-case runner
# ---------------------------------------------------------------------------

def run_one_case(
    *,
    target_type: str,
    noise: float,
    sensor_config: str,
    seed: int,
    simulator: HeatConduction2DFD,
    q_max: float = DEFAULT_Q_MAX,
) -> dict:
    """Execute one benchmark case and return a result dict.

    Steps
    -----
    1. Generate ground-truth flux q(y, t) analytically.
    2. Run forward simulator → clean temperature field at sensors.
    3. Add Gaussian noise with the given sigma.
    4. Run deepxde_solver_2d to recover q.
    5. Compute RMSE between predicted and true flux (coarse grid).

    Parameters
    ----------
    target_type   : flux target type
    noise         : noise std-dev [K]
    sensor_config : "sparse" / "medium" / "dense"
    seed          : RNG seed for noise (sensor positions are deterministic)
    simulator     : pre-built HeatConduction2DFD instance

    Returns
    -------
    dict with benchmark result columns (matches CSV header).
    """
    t0_case = time.perf_counter()
    rng = np.random.default_rng(seed)

    # 1. Ground-truth flux on coarse (NY_Q × NT_Q) grid
    y_q_grid = np.linspace(0.0, DEFAULT_LY, NY_Q)
    t_q_grid = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)
    q_true_coarse = generate_flux_2d(
        target_type=target_type,
        y_grid=y_q_grid,
        t_grid=t_q_grid,
        Ly=DEFAULT_LY,
        T_total=DEFAULT_T_TOTAL,
        q_max=q_max,
    )  # shape (NY_Q, NT_Q)

    # Also evaluate truth on the fine grid for forward simulation
    y_fine = simulator.y_centers            # (ny,)
    t_fine = np.linspace(                   # (NT_Q,) — same nt_q time grid
        0.0, DEFAULT_T_TOTAL, NT_Q
    )
    q_true_fine = generate_flux_2d(
        target_type=target_type,
        y_grid=y_fine,
        t_grid=t_fine,
        Ly=DEFAULT_LY,
        T_total=DEFAULT_T_TOTAL,
        q_max=q_max,
    )  # shape (ny, NT_Q)

    # 2. Sensor positions (deterministic — do NOT change with seed)
    sensor_positions = generate_sensor_grid(sensor_config, DEFAULT_LX, DEFAULT_LY)

    # 3. Forward simulation → clean temperature observations
    T_clean, _ = simulator.simulate(
        q_flux_2d=q_true_fine,
        T0=DEFAULT_T0,
        sensor_positions=sensor_positions,
        t_end=DEFAULT_T_TOTAL,
        obs_every=OBS_EVERY,
    )  # T_clean shape: (n_sensors, n_obs)

    # 4. Add Gaussian noise
    noise_array = rng.normal(0.0, noise, size=T_clean.shape)
    T_noisy = T_clean + noise_array

    # 5. Inversion
    problem_spec = {
        "simulator":       simulator,
        "sensor_positions": sensor_positions,
        "T_obs_noisy":     T_noisy,
        "obs_every":       OBS_EVERY,
        "t_end":           DEFAULT_T_TOTAL,
        "ny_q":            NY_Q,
        "nt_q":            NT_Q,
        "T0":              DEFAULT_T0,
        "lam":             LAM,
        "n_iter":          N_ITER,
        "lr":              LR,
        "reg_order":       1,
        "use_lbfgs":       False,
        "q_true":          q_true_coarse,   # for RMSE computation inside solver
    }

    try:
        result = solve_2d(problem_spec)
        rmse              = result["rmse"]
        convergence_flag  = result["convergence_flag"]
        solver_name       = result["diagnostics"]["solver_name"]
    except Exception as exc:
        log.error(
            "solve_2d failed [%s / noise=%.2f / %s / seed=%d]: %s",
            target_type, noise, sensor_config, seed, exc,
        )
        rmse             = float("nan")
        convergence_flag = False
        solver_name      = "deepxde_pytorch_2d"

    elapsed = time.perf_counter() - t0_case

    log.info(
        "%-12s  noise=%.1f  %-8s  seed=%d  |  RMSE=%s  conv=%s  t=%.1fs",
        target_type, noise, sensor_config, seed,
        f"{rmse:.4f}" if rmse is not None else "  N/A",
        convergence_flag,
        elapsed,
    )

    return {
        "target_type":     target_type,
        "noise":           noise,
        "sensor_config":   sensor_config,
        "seed":            seed,
        "solver_name":     solver_name,
        "rmse":            rmse if rmse is not None else float("nan"),
        "convergence_flag": int(convergence_flag),
    }


# ---------------------------------------------------------------------------
# Benchmark driver
# ---------------------------------------------------------------------------

CSV_COLUMNS = [
    "target_type", "noise", "sensor_config", "seed",
    "solver_name", "rmse", "convergence_flag",
]


def run_benchmark(
    output_csv: Path,
    limit: int | None = None,
    overwrite: bool = False,
) -> None:
    """Run all 54 benchmark cases and write results to CSV.

    Parameters
    ----------
    output_csv : destination CSV path
    limit      : if set, stop after this many cases (smoke test)
    overwrite  : if False and CSV exists, skip already-completed cases
    """
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # Load existing results to support resume
    done_keys: set[tuple] = set()
    if not overwrite and output_csv.exists():
        import csv as _csv
        with output_csv.open(newline="") as fh:
            reader = _csv.DictReader(fh)
            for row in reader:
                key = (
                    row["target_type"],
                    float(row["noise"]),
                    row["sensor_config"],
                    int(row["seed"]),
                )
                done_keys.add(key)
        log.info("Loaded %d previously completed cases; will skip them.", len(done_keys))

    # Write CSV header if starting fresh
    write_header = not output_csv.exists() or overwrite
    if overwrite and output_csv.exists():
        output_csv.unlink()
    fh = output_csv.open("a", newline="")
    writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
    if write_header:
        writer.writeheader()
        fh.flush()

    # Build shared simulator (expensive setup is minimal for explicit FD)
    simulator = _make_simulator()
    log.info(
        "Simulator: Lx=%.2fm Ly=%.2fm  nx=%d ny=%d  dt=%.4fs",
        simulator.Lx, simulator.Ly, simulator.nx, simulator.ny, simulator.dt,
    )

    combinations = list(itertools.product(
        TARGET_TYPES, NOISE_LEVELS, SENSOR_CONFIGS, SEEDS
    ))
    total = len(combinations)
    if limit is not None:
        combinations = combinations[:limit]
        log.info("Running %d / %d cases (--limit %d)", len(combinations), total, limit)
    else:
        log.info("Running all %d cases", total)

    completed = 0
    failed = 0

    for target_type, noise, sensor_config, seed in combinations:
        key = (target_type, float(noise), sensor_config, int(seed))
        if key in done_keys:
            log.debug("Skipping %s (already done)", key)
            completed += 1
            continue

        row = run_one_case(
            target_type=target_type,
            noise=noise,
            sensor_config=sensor_config,
            seed=seed,
            simulator=simulator,
        )

        if not np.isfinite(row["rmse"]):
            failed += 1

        writer.writerow(row)
        fh.flush()
        completed += 1

    fh.close()
    log.info(
        "Benchmark complete.  Cases=%d  Failed=%d  Output=%s",
        completed, failed, output_csv,
    )

    # Print sample output
    _print_sample(output_csv)


def _print_sample(csv_path: Path, n: int = 5) -> None:
    """Print the first n rows of the results CSV to stdout."""
    if not csv_path.exists():
        return
    import csv as _csv
    with csv_path.open(newline="") as fh:
        reader = _csv.reader(fh)
        rows = list(reader)
    print(f"\n--- First {n} rows of {csv_path} ---")
    for row in rows[: n + 1]:  # +1 for header
        print(",".join(str(v) for v in row))
    print("---")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="2D IHCP benchmark runner (benchmark_2d_v1).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  # Full run
  python scripts/run_benchmark_2d_v1.py

  # Quick smoke test
  python scripts/run_benchmark_2d_v1.py --limit 6

  # Custom output
  python scripts/run_benchmark_2d_v1.py --output reports/my_run.csv

  # Re-run everything (overwrite)
  python scripts/run_benchmark_2d_v1.py --overwrite
""",
    )
    parser.add_argument(
        "--output",
        default="reports/benchmark_2d_v1_results.csv",
        metavar="CSV",
        help="Output CSV path (default: reports/benchmark_2d_v1_results.csv)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Run only the first N cases (smoke test)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing results instead of resuming",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )

    # Resolve output path relative to project root
    output_csv = Path(args.output)
    if not output_csv.is_absolute():
        output_csv = _PROJECT_ROOT / output_csv

    log.info("Output CSV: %s", output_csv)
    run_benchmark(output_csv=output_csv, limit=args.limit, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
