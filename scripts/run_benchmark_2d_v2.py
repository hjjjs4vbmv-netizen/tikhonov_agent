"""
run_benchmark_2d_v2.py
======================
Benchmark runner for benchmark_2d_v2 — three-solver 2D IHCP comparison.

Solvers
-------
    tikhonov_2d  — closed-form normal equations (NumPy)
    tsvd_2d      — truncated SVD                (NumPy)
    deepxde_2d   — Adam-optimised Tikhonov      (PyTorch)

Main benchmark axes
-------------------
    target_type  ∈ {smooth, localized, multi_spot}
    noise        ∈ {0.1, 0.5, 1.0} K
    sensor_config∈ {sparse(4), medium(9), dense(16)}
    seed         ∈ {0, 1}
    → 3 × 3 × 3 × 2 × 3 solvers = 162 solver-runs

Sensor-layout note (--layout-note)
-----------------------------------
    layout       ∈ {uniform_grid, boundary_biased, clustered}
    target_type  ∈ {smooth, localized}
    noise        ∈ {0.1, 1.0} K
    seed         = 2
    solvers      = tikhonov_2d, tsvd_2d, deepxde_2d
    → 3 × 2 × 2 × 3 solvers = 36 runs

Design for fairness
-------------------
1.  The sensitivity matrix S is built ONCE per sensor_config (layout) and
    shared across all solvers and seeds.  Only target flux and noise differ.
2.  y_obs_flat is computed ONCE per (target, noise, sensor, seed) and passed
    to all three solvers identically.
3.  Flux RMSE is evaluated on the same (ny_q × nt_q) coarse grid for all
    solvers.

Usage
-----
    cd tikhonov_agent

    # Full benchmark (162 solver-runs)
    python scripts/run_benchmark_2d_v2.py

    # Only layout note (36 runs)
    python scripts/run_benchmark_2d_v2.py --layout-note

    # Both
    python scripts/run_benchmark_2d_v2.py --all

    # Smoke test (2 cases, all solvers)
    python scripts/run_benchmark_2d_v2.py --limit 2

Outputs
-------
    reports/benchmark_2d_v2_results.csv
    reports/benchmark_2d_layout_note.csv
"""

from __future__ import annotations

import argparse
import csv
import itertools
import logging
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_HERE        = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.forward.heat2d_simulator import (   # noqa: E402
    DEFAULT_LX, DEFAULT_LY, DEFAULT_ALPHA, DEFAULT_K,
    DEFAULT_T0, DEFAULT_T_TOTAL, DEFAULT_Q_MAX,
    DEFAULT_NX, DEFAULT_NY,
    HeatConduction2DFD,
    generate_flux_2d,
    generate_sensor_grid,
)
from src.tikhonov_solver_2d import solve_2d_tikhonov   # noqa: E402
from src.tsvd_solver_2d     import solve_2d_tsvd        # noqa: E402
from src.deepxde_solver_2d  import solve_2d             # noqa: E402

log = logging.getLogger("benchmark_2d_v2")

# ---------------------------------------------------------------------------
# Benchmark parameters
# ---------------------------------------------------------------------------

TARGET_TYPES   = ["smooth", "localized", "multi_spot"]
NOISE_LEVELS   = [0.1, 0.5, 1.0]
SENSOR_CONFIGS = ["sparse", "medium", "dense"]
SEEDS          = [0, 1]

# Shared coarse flux parametrisation (same for ALL solvers)
NY_Q      = 10
NT_Q      = 20
OBS_EVERY = 5          # record every 5th internal step ≈ 36 obs per sensor

# Solver hyperparameters
LAM_TIKHONOV  = 1e-3   # regularisation for Tikhonov normal equations
TSVD_TOL      = 0.01   # relative truncation threshold for TSVD
LAM_DEEPXDE   = 1e-4   # regularisation for DeepXDE Adam solver
N_ITER_DEEPXDE= 500    # Adam iterations
LR_DEEPXDE    = 10.0   # Adam learning rate (scaled for small S entries)

# Layout note parameters
LAYOUT_NOTE_LAYOUTS     = ["uniform_grid", "boundary_biased", "clustered"]
LAYOUT_NOTE_TARGETS     = ["smooth", "localized"]
LAYOUT_NOTE_NOISES      = [0.1, 1.0]
LAYOUT_NOTE_SEED        = 2


# ---------------------------------------------------------------------------
# Sensor layout generator (for the layout note)
# ---------------------------------------------------------------------------

def generate_sensor_layout(
    layout: str,
    Lx: float = DEFAULT_LX,
    Ly: float = DEFAULT_LY,
) -> list[tuple[float, float]]:
    """Generate 9-sensor positions for the layout note experiment.

    Layouts
    -------
    uniform_grid     : 3×3 evenly spread interior grid  (identical to 'medium')
    boundary_biased  : 3 x-positions close to x=0, 3 y-positions uniform
                       → sensors see the unknown flux boundary more directly
    clustered        : sensors grouped into the central quadrant
                       → poor coverage of the boundary and domain edges
    """
    if layout == "uniform_grid":
        xs = np.linspace(0.10 * Lx, 0.90 * Lx, 3)
        ys = np.linspace(0.10 * Ly, 0.90 * Ly, 3)

    elif layout == "boundary_biased":
        # x biased toward x=0 (the unknown-flux boundary)
        xs = np.array([0.10, 0.20, 0.35]) * Lx
        ys = np.linspace(0.10 * Ly, 0.90 * Ly, 3)

    elif layout == "clustered":
        # Sensors bunched in the centre — poor global observability
        xs = np.linspace(0.35 * Lx, 0.65 * Lx, 3)
        ys = np.linspace(0.35 * Ly, 0.65 * Ly, 3)

    else:
        raise ValueError(f"Unknown layout {layout!r}")

    return [(float(xi), float(yj)) for xi in xs for yj in ys]


# ---------------------------------------------------------------------------
# Shared observation generator
# ---------------------------------------------------------------------------

def make_observation(
    simulator: HeatConduction2DFD,
    target_type: str,
    noise: float,
    sensor_positions: list[tuple[float, float]],
    seed: int,
) -> dict[str, Any]:
    """Generate one complete observation package.

    Returns a dict with:
        q_true_coarse : (NY_Q, NT_Q) — ground-truth on coarse eval grid
        T_obs_noisy   : (n_sensors, n_obs_times)
        T_obs_clean   : (n_sensors, n_obs_times)
        obs_times     : (n_obs_times,)
    """
    rng = np.random.default_rng(seed)

    # Ground truth on coarse grid (shared evaluation basis)
    y_q_grid = np.linspace(0.0, DEFAULT_LY, NY_Q)
    t_q_grid = np.linspace(0.0, DEFAULT_T_TOTAL, NT_Q)
    q_true_coarse = generate_flux_2d(target_type, y_q_grid, t_q_grid)

    # True flux on fine y-grid for forward simulation
    q_fine = generate_flux_2d(target_type, simulator.y_centers, t_q_grid)

    # Forward simulation → clean observations
    T_clean, obs_times = simulator.simulate(
        q_flux_2d=q_fine,
        T0=DEFAULT_T0,
        sensor_positions=sensor_positions,
        t_end=DEFAULT_T_TOTAL,
        obs_every=OBS_EVERY,
    )

    # Add Gaussian noise (only noise changes across seeds; sensor grid is fixed)
    noise_arr   = rng.normal(0.0, noise, size=T_clean.shape)
    T_noisy     = T_clean + noise_arr

    return {
        "q_true_coarse": q_true_coarse,
        "T_obs_noisy":   T_noisy,
        "T_obs_clean":   T_clean,
        "obs_times":     obs_times,
    }


# ---------------------------------------------------------------------------
# Solver dispatcher
# ---------------------------------------------------------------------------

def _base_spec(
    simulator, sensor_positions, obs_data: dict, S, y_q_grid, t_q_grid
) -> dict[str, Any]:
    """Build the shared problem_spec passed to every solver."""
    return {
        "simulator":       simulator,
        "sensor_positions": sensor_positions,
        "T_obs_noisy":     obs_data["T_obs_noisy"],
        "obs_every":       OBS_EVERY,
        "t_end":           DEFAULT_T_TOTAL,
        "ny_q":            NY_Q,
        "nt_q":            NT_Q,
        "T0":              DEFAULT_T0,
        "q_true":          obs_data["q_true_coarse"],
        # Cached sensitivity matrix (avoids rebuild inside solver)
        "S":               S,
        "y_q_grid":        y_q_grid,
        "t_q_grid":        t_q_grid,
    }


def run_solver(
    solver_name: str,
    problem_spec: dict[str, Any],
) -> dict[str, Any]:
    """Dispatch to the named solver and return a uniform result dict."""
    t0 = time.perf_counter()

    if solver_name == "tikhonov_2d":
        spec = dict(problem_spec)
        spec["lam"]       = LAM_TIKHONOV
        spec["reg_order"] = 1
        raw = solve_2d_tikhonov(spec)

    elif solver_name == "tsvd_2d":
        spec = dict(problem_spec)
        spec["tsvd_tol"]  = TSVD_TOL
        raw = solve_2d_tsvd(spec)

    elif solver_name == "deepxde_2d":
        spec = dict(problem_spec)
        spec["lam"]       = LAM_DEEPXDE
        spec["n_iter"]    = N_ITER_DEEPXDE
        spec["lr"]        = LR_DEEPXDE
        spec["reg_order"] = 1
        # deepxde_solver_2d expects its own internal keys:
        raw = solve_2d(spec)
        # Normalise output keys to match the shared interface
        if "rmse" in raw and "flux_rmse" not in raw:
            raw["flux_rmse"] = raw["rmse"]

    else:
        raise ValueError(f"Unknown solver {solver_name!r}")

    # Ensure uniform keys
    runtime = time.perf_counter() - t0
    flux_rmse   = raw.get("flux_rmse") or raw.get("rmse")
    replay_rmse = raw.get("replay_rmse")

    # For deepxde, compute replay_rmse from residual if not present
    if replay_rmse is None and "S" in problem_spec:
        S       = np.asarray(problem_spec["S"])
        T0      = float(problem_spec.get("T0", 0.0))
        T_noisy = np.asarray(problem_spec["T_obs_noisy"])
        n_sensors = len(problem_spec["sensor_positions"])
        n_obs_times = S.shape[0] // n_sensors
        y_obs   = T_noisy[:, :n_obs_times].flatten() - T0
        q_pred  = raw["flux_pred"].flatten()
        resid   = S @ q_pred - y_obs
        replay_rmse = float(np.sqrt(np.mean(resid ** 2)))

    diag = raw.get("diagnostics", {})
    notes = "ok"
    if not raw.get("convergence_flag", True):
        notes = "diverged"
    if solver_name == "tsvd_2d" and "kept_rank" in diag:
        notes = f"rank={diag['kept_rank']}"

    return {
        "flux_rmse":        float(flux_rmse)   if flux_rmse   is not None else float("nan"),
        "replay_rmse":      float(replay_rmse) if replay_rmse is not None else float("nan"),
        "runtime_sec":      runtime,
        "convergence_flag": int(raw.get("convergence_flag", True)),
        "notes":            notes,
        "flux_pred":        raw["flux_pred"],
        "diagnostics":      diag,
    }


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

MAIN_COLUMNS = [
    "solver_name", "target_type", "noise", "sensor_config",
    "seed", "flux_rmse", "replay_rmse", "runtime_sec",
    "convergence_flag", "notes",
]

LAYOUT_COLUMNS = [
    "solver_name", "target_type", "noise", "layout",
    "seed", "flux_rmse", "replay_rmse", "runtime_sec",
    "convergence_flag", "notes",
]


def _open_csv(path: Path, columns: list[str], overwrite: bool) -> tuple:
    """Open CSV for appending (or create fresh). Return (file_handle, writer, done_keys)."""
    done_keys: set[tuple] = set()
    if not overwrite and path.exists():
        import csv as _csv
        with path.open(newline="") as fh:
            for row in _csv.DictReader(fh):
                done_keys.add(tuple(row.get(c, "") for c in columns[:6]))
        log.info("Resuming %s — skipping %d completed runs", path.name, len(done_keys))

    write_header = not path.exists() or overwrite
    if overwrite and path.exists():
        path.unlink()

    path.parent.mkdir(parents=True, exist_ok=True)
    fh     = path.open("a", newline="")
    writer = csv.DictWriter(fh, fieldnames=columns)
    if write_header:
        writer.writeheader()
        fh.flush()
    return fh, writer, done_keys


# ---------------------------------------------------------------------------
# Main benchmark (3 axes × 3 noise × 2 seeds × 3 solvers)
# ---------------------------------------------------------------------------

def run_main_benchmark(
    output_csv: Path,
    simulator: HeatConduction2DFD,
    overwrite: bool = False,
    limit: int | None = None,
    solvers: list[str] | None = None,
) -> None:
    if solvers is None:
        solvers = ["tikhonov_2d", "tsvd_2d", "deepxde_2d"]

    fh, writer, done_keys = _open_csv(output_csv, MAIN_COLUMNS, overwrite)

    # Pre-build sensitivity matrices for each sensor_config (shared across seeds)
    S_cache: dict[str, tuple] = {}

    combinations = list(itertools.product(
        TARGET_TYPES, NOISE_LEVELS, SENSOR_CONFIGS, SEEDS
    ))
    if limit:
        combinations = combinations[:limit]

    log.info("Main benchmark: %d data cases × %d solvers = %d runs",
             len(combinations), len(solvers), len(combinations) * len(solvers))

    completed = 0
    for target_type, noise, sensor_config, seed in combinations:
        sensor_positions = generate_sensor_grid(sensor_config)

        # Build / retrieve cached S
        if sensor_config not in S_cache:
            log.info("Building S for sensor_config=%s …", sensor_config)
            t_s = time.perf_counter()
            S, obs_times, y_q_grid, t_q_grid = simulator.build_sensitivity_matrix(
                sensor_positions=sensor_positions,
                t_end=DEFAULT_T_TOTAL, ny_q=NY_Q, nt_q=NT_Q,
                obs_every=OBS_EVERY,
            )
            log.info("  S built in %.1fs, shape %s", time.perf_counter() - t_s, S.shape)
            S_cache[sensor_config] = (S, obs_times, y_q_grid, t_q_grid)

        S, obs_times, y_q_grid, t_q_grid = S_cache[sensor_config]

        # Generate observations once (shared across solvers)
        obs_data = make_observation(simulator, target_type, noise,
                                    sensor_positions, seed)

        base_spec = _base_spec(simulator, sensor_positions, obs_data,
                               S, y_q_grid, t_q_grid)

        for solver_name in solvers:
            key = (solver_name, target_type, str(noise), sensor_config,
                   str(seed), "")[:6]
            if key in done_keys:
                completed += 1
                continue

            try:
                result = run_solver(solver_name, base_spec)
            except Exception as exc:
                log.error("%s / %s / noise=%.1f / %s / seed=%d FAILED: %s",
                          solver_name, target_type, noise, sensor_config, seed, exc)
                result = {
                    "flux_rmse": float("nan"), "replay_rmse": float("nan"),
                    "runtime_sec": 0.0, "convergence_flag": 0,
                    "notes": f"error: {exc!s}", "flux_pred": None, "diagnostics": {},
                }

            row = {
                "solver_name":     solver_name,
                "target_type":     target_type,
                "noise":           noise,
                "sensor_config":   sensor_config,
                "seed":            seed,
                "flux_rmse":       result["flux_rmse"],
                "replay_rmse":     result["replay_rmse"],
                "runtime_sec":     result["runtime_sec"],
                "convergence_flag": result["convergence_flag"],
                "notes":           result["notes"],
            }
            writer.writerow(row)
            fh.flush()

            log.info(
                "%-12s %-12s  noise=%.1f  %-8s  seed=%d  |"
                "  flux_rmse=%.1f  replay=%.4f  t=%.1fs  [%s]",
                solver_name, target_type, noise, sensor_config, seed,
                result["flux_rmse"], result["replay_rmse"],
                result["runtime_sec"], result["notes"],
            )
            completed += 1

    fh.close()
    log.info("Main benchmark complete.  %d runs → %s", completed, output_csv)


# ---------------------------------------------------------------------------
# Sensor layout note (fixed medium count, 3 layouts)
# ---------------------------------------------------------------------------

def run_layout_note(
    output_csv: Path,
    simulator: HeatConduction2DFD,
    overwrite: bool = False,
    solvers: list[str] | None = None,
) -> None:
    if solvers is None:
        solvers = ["tikhonov_2d", "tsvd_2d", "deepxde_2d"]

    fh, writer, done_keys = _open_csv(output_csv, LAYOUT_COLUMNS, overwrite)

    # Pre-build S per layout
    S_cache: dict[str, tuple] = {}

    combinations = list(itertools.product(
        LAYOUT_NOTE_LAYOUTS, LAYOUT_NOTE_TARGETS, LAYOUT_NOTE_NOISES
    ))
    seed = LAYOUT_NOTE_SEED

    log.info("Layout note: %d data cases × %d solvers = %d runs",
             len(combinations), len(solvers), len(combinations) * len(solvers))

    for layout, target_type, noise in combinations:
        sensor_positions = generate_sensor_layout(layout)

        if layout not in S_cache:
            log.info("Building S for layout=%s …", layout)
            t_s = time.perf_counter()
            S, obs_times, y_q_grid, t_q_grid = simulator.build_sensitivity_matrix(
                sensor_positions=sensor_positions,
                t_end=DEFAULT_T_TOTAL, ny_q=NY_Q, nt_q=NT_Q,
                obs_every=OBS_EVERY,
            )
            log.info("  S built in %.1fs", time.perf_counter() - t_s)
            S_cache[layout] = (S, obs_times, y_q_grid, t_q_grid)

        S, obs_times, y_q_grid, t_q_grid = S_cache[layout]

        obs_data = make_observation(simulator, target_type, noise,
                                    sensor_positions, seed)
        base_spec = _base_spec(simulator, sensor_positions, obs_data,
                               S, y_q_grid, t_q_grid)

        for solver_name in solvers:
            key = (solver_name, target_type, str(noise), layout, str(seed), "")[:6]
            if key in done_keys:
                continue

            try:
                result = run_solver(solver_name, base_spec)
            except Exception as exc:
                log.error("%s / %s FAILED: %s", solver_name, target_type, exc)
                result = {
                    "flux_rmse": float("nan"), "replay_rmse": float("nan"),
                    "runtime_sec": 0.0, "convergence_flag": 0,
                    "notes": f"error: {exc!s}", "flux_pred": None, "diagnostics": {},
                }

            row = {
                "solver_name":     solver_name,
                "target_type":     target_type,
                "noise":           noise,
                "layout":          layout,
                "seed":            seed,
                "flux_rmse":       result["flux_rmse"],
                "replay_rmse":     result["replay_rmse"],
                "runtime_sec":     result["runtime_sec"],
                "convergence_flag": result["convergence_flag"],
                "notes":           result["notes"],
            }
            writer.writerow(row)
            fh.flush()

            log.info(
                "%-12s %-12s  noise=%.1f  %-20s  |"
                "  flux_rmse=%.1f  t=%.1fs  [%s]",
                solver_name, target_type, noise, layout,
                result["flux_rmse"], result["runtime_sec"], result["notes"],
            )

    fh.close()
    log.info("Layout note complete → %s", output_csv)


# ---------------------------------------------------------------------------
# Summary printer
# ---------------------------------------------------------------------------

def print_summary(csv_path: Path, n: int = 5) -> None:
    if not csv_path.exists():
        return
    import csv as _csv
    with csv_path.open(newline="") as fh:
        rows = list(_csv.reader(fh))
    print(f"\n--- First {n} rows of {csv_path.name} ---")
    for row in rows[: n + 1]:
        print(",".join(str(v) for v in row))
    print("---")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="benchmark_2d_v2 — three-solver 2D IHCP comparison",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples
--------
  python scripts/run_benchmark_2d_v2.py           # main benchmark (162 runs)
  python scripts/run_benchmark_2d_v2.py --layout-note   # layout note (36 runs)
  python scripts/run_benchmark_2d_v2.py --all     # both
  python scripts/run_benchmark_2d_v2.py --limit 2 # smoke test
  python scripts/run_benchmark_2d_v2.py --solvers tikhonov_2d tsvd_2d  # skip DeepXDE
""",
    )
    p.add_argument("--main-csv",    default="reports/benchmark_2d_v2_results.csv")
    p.add_argument("--layout-csv",  default="reports/benchmark_2d_layout_note.csv")
    p.add_argument("--layout-note", action="store_true",
                   help="Run layout note experiment instead of main benchmark")
    p.add_argument("--all",         action="store_true",
                   help="Run main benchmark AND layout note")
    p.add_argument("--overwrite",   action="store_true")
    p.add_argument("--limit",       type=int, default=None, metavar="N",
                   help="Run only first N data-cases (smoke test)")
    p.add_argument("--solvers",     nargs="+",
                   default=["tikhonov_2d", "tsvd_2d", "deepxde_2d"],
                   choices=["tikhonov_2d", "tsvd_2d", "deepxde_2d"])
    p.add_argument("--log-level",   default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return p.parse_args()


def main() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout, force=True,
    )

    main_csv   = (_PROJECT_ROOT / args.main_csv  ).resolve()
    layout_csv = (_PROJECT_ROOT / args.layout_csv).resolve()

    simulator = HeatConduction2DFD()
    log.info("Simulator: dt=%.4fs  nx=%d  ny=%d",
             simulator.dt, simulator.nx, simulator.ny)

    run_main   = not args.layout_note or args.all
    run_layout = args.layout_note     or args.all

    if run_main:
        log.info("=== Main benchmark ===")
        run_main_benchmark(
            main_csv, simulator,
            overwrite=args.overwrite, limit=args.limit,
            solvers=args.solvers,
        )
        print_summary(main_csv)

    if run_layout:
        log.info("=== Sensor layout note ===")
        run_layout_note(
            layout_csv, simulator,
            overwrite=args.overwrite,
            solvers=args.solvers,
        )
        print_summary(layout_csv)


if __name__ == "__main__":
    main()
