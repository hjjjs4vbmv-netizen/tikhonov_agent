"""
test_benchmark_runner.py
========================
Tests for experiments/run_benchmark.py — verify that the runner writes
result rows with required columns and that at least one variant runs end-to-end.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from experiments.utils import (
    build_time_grid,
    get_variant_overrides,
    save_result_row,
)
from experiments.generate_cases import generate_case
from experiments.run_benchmark import run_one
from src.types import BoundaryConditions, Geometry, Material


# ---------------------------------------------------------------------------
# Required columns in the results CSV
# ---------------------------------------------------------------------------

REQUIRED_COLUMNS = [
    # Metadata
    "case_id", "flux_family", "noise_level", "sensor_count",
    "sensor_layout", "time_resolution", "seed", "variant_name",
    # Flux metrics
    "flux_l2_error", "flux_relative_l2_error", "flux_rmse",
    "flux_peak_error", "flux_correlation",
    # Replay metrics
    "replay_rmse", "replay_relative_error", "replay_max_abs_error",
    # Regularity
    "roughness_l1", "roughness_l2", "oscillation_score",
    "sign_flip_count", "physical_violation_count", "within_bounds_flag",
    # Agent metrics
    "final_decision", "success_flag", "weak_pass_flag",
    "manual_review_flag", "failure_flag", "iteration_count",
    "replanning_count", "runtime_sec", "initial_to_final_improvement",
    "final_lambda", "final_reg_order", "final_variant_name",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tiny_case(tmp_path):
    """Create a minimal benchmark case and return its files."""
    geometry = Geometry(length=0.05, n_cells=20)
    material = Material(density=7800.0, specific_heat=500.0, conductivity=50.0)
    bc = BoundaryConditions(right_type="dirichlet", right_value=300.0)
    time_grid = build_time_grid(0.0, 10.0, 21)   # small: 21 steps
    sensor_positions = [0.01, 0.03]

    case_dir = tmp_path / "cases" / "case_0001"
    rng = np.random.default_rng(42)
    generate_case(
        case_dir=case_dir,
        time_grid=time_grid,
        geometry=geometry,
        material=material,
        bc=bc,
        initial_condition=300.0,
        sensor_positions=sensor_positions,
        flux_family="step",
        flux_params={"q_base": 0.0, "q_step": 50_000.0, "t_on_frac": 0.3},
        noise_level=0.3,
        noise_std_in_config=None,
        rng=rng,
    )

    manifest_row = pd.Series({
        "case_id": "case_0001",
        "config_path": str((case_dir / "config.yaml").resolve()),
        "obs_path": str((case_dir / "observations.csv").resolve()),
        "truth_path": str((case_dir / "truth.npz").resolve()),
        "flux_family": "step",
        "noise_level": 0.3,
        "sensor_count": 2,
        "sensor_layout": "0.01,0.03",
        "time_resolution": 1.0,
        "seed": 42,
    })
    return manifest_row, tmp_path


# ---------------------------------------------------------------------------
# Variant override tests
# ---------------------------------------------------------------------------

class TestVariantOverrides:
    def test_fixed_solver_overrides(self):
        cfg = {"lambda_value": 1.0, "iteration_budget": 1, "max_retries": 1}
        overrides = get_variant_overrides("fixed_solver", cfg)
        assert overrides["lambda_value"] == 1.0
        assert overrides["iteration_budget"] == 1

    def test_full_agent_overrides(self):
        cfg = {"reg_order": 1, "max_retries": 8, "iteration_budget": 12,
               "physical_bounds": [-5e5, 5e5]}
        overrides = get_variant_overrides("full_agent", cfg)
        assert overrides["max_retries"] == 8
        assert overrides["physical_bounds"] == [-5e5, 5e5]

    def test_unknown_keys_filtered(self):
        cfg = {"lambda_value": 1.0, "not_a_real_key": "ignored"}
        overrides = get_variant_overrides("x", cfg)
        assert "not_a_real_key" not in overrides
        assert overrides["lambda_value"] == 1.0


# ---------------------------------------------------------------------------
# End-to-end run_one test
# ---------------------------------------------------------------------------

class TestRunOne:
    def test_run_one_auto_solver(self, tiny_case, tmp_path):
        """auto_solver completes and result row has all required columns."""
        manifest_row, base_dir = tiny_case
        run_dir = tmp_path / "runs" / "case_0001" / "auto_solver"
        output_csv = tmp_path / "runs" / "results_raw.csv"

        variant_overrides = {"iteration_budget": 1, "max_retries": 1, "reg_order": 1}
        row = run_one(
            case_row=manifest_row,
            variant_name="auto_solver",
            variant_overrides=variant_overrides,
            run_dir=run_dir,
            output_csv=output_csv,
        )

        assert row is not None, "run_one returned None (run failed)"

        missing = [c for c in REQUIRED_COLUMNS if c not in row]
        assert missing == [], f"Missing result columns: {missing}"

    def test_run_one_fixed_solver(self, tiny_case, tmp_path):
        """fixed_solver (lambda_value=1.0) completes and returns a row."""
        manifest_row, _ = tiny_case
        run_dir = tmp_path / "runs" / "case_0001" / "fixed_solver"
        output_csv = tmp_path / "runs" / "results_raw.csv"

        overrides = {"lambda_value": 1.0, "iteration_budget": 1, "max_retries": 1}
        row = run_one(
            case_row=manifest_row,
            variant_name="fixed_solver",
            variant_overrides=overrides,
            run_dir=run_dir,
            output_csv=output_csv,
        )

        assert row is not None
        assert row["final_lambda"] == pytest.approx(1.0)

    def test_run_one_writes_csv(self, tiny_case, tmp_path):
        """run_one appends a row to the output CSV file."""
        manifest_row, _ = tiny_case
        run_dir = tmp_path / "runs" / "case_0001" / "auto_solver"
        output_csv = tmp_path / "runs" / "results_raw.csv"

        overrides = {"iteration_budget": 1, "max_retries": 1}
        run_one(
            case_row=manifest_row,
            variant_name="auto_solver",
            variant_overrides=overrides,
            run_dir=run_dir,
            output_csv=output_csv,
        )

        assert output_csv.exists()
        df = pd.read_csv(output_csv)
        assert len(df) >= 1

    def test_run_one_writes_npz(self, tiny_case, tmp_path):
        """run_one saves run_summary.npz for plotting."""
        manifest_row, _ = tiny_case
        run_dir = tmp_path / "runs" / "case_0001" / "auto_solver"
        output_csv = tmp_path / "runs" / "results_raw.csv"

        overrides = {"iteration_budget": 1, "max_retries": 1}
        run_one(
            case_row=manifest_row,
            variant_name="auto_solver",
            variant_overrides=overrides,
            run_dir=run_dir,
            output_csv=output_csv,
        )

        npz_path = run_dir / "run_summary.npz"
        assert npz_path.exists()
        data = np.load(npz_path)
        for key in ("q_true", "q_est", "y_obs", "y_fit", "time_grid"):
            assert key in data, f"Missing key '{key}' in run_summary.npz"

    def test_full_agent_terminates(self, tiny_case, tmp_path):
        """full_agent terminates and returns a valid final status."""
        manifest_row, _ = tiny_case
        run_dir = tmp_path / "runs" / "case_0001" / "full_agent"
        output_csv = tmp_path / "runs" / "results_raw.csv"

        overrides = {
            "reg_order": 1, "max_retries": 4, "iteration_budget": 6,
            "physical_bounds": [-5e5, 5e5],
        }
        row = run_one(
            case_row=manifest_row,
            variant_name="full_agent",
            variant_overrides=overrides,
            run_dir=run_dir,
            output_csv=output_csv,
        )

        assert row is not None
        assert row["final_decision"] in ("pass", "weak_pass", "manual_review", "fail")
