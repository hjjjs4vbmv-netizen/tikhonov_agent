"""
test_metrics_aggregation.py
===========================
Tests for experiments/analyze_results.py — verify grouped summary tables
are created correctly and contain the expected aggregation columns.
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

from experiments.analyze_results import (
    compute_ablation_summary,
    run_analysis,
    summarize_by_flux_family,
    summarize_by_noise,
    summarize_by_variant,
)
from experiments.utils import compute_flux_metrics, compute_regularity_metrics


# ---------------------------------------------------------------------------
# Synthetic dataframe fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_results_df():
    """Synthetic results DataFrame mimicking results_raw.csv."""
    rng = np.random.default_rng(0)
    n = 60   # 4 variants × 3 flux families × 5 rows each

    variants = ["fixed_solver", "auto_solver", "solver_plus_verifier", "full_agent"]
    families = ["step", "ramp", "single_pulse"]
    noise_levels = [0.1, 0.5, 1.0]

    rows = []
    for i in range(n):
        v = variants[i % len(variants)]
        f = families[i % len(families)]
        nl = noise_levels[i % len(noise_levels)]
        rows.append({
            "case_id": f"case_{i:04d}",
            "variant_name": v,
            "flux_family": f,
            "noise_level": nl,
            "seed": 42,
            "sensor_count": 2,
            "sensor_layout": "0.01,0.03",
            "time_resolution": 1.0,
            # Flux metrics
            "flux_l2_error": rng.uniform(100, 5000),
            "flux_relative_l2_error": rng.uniform(0.01, 0.5),
            "flux_rmse": rng.uniform(100, 3000),
            "flux_peak_error": rng.uniform(200, 8000),
            "flux_correlation": rng.uniform(0.5, 1.0),
            # Replay metrics
            "replay_rmse": rng.uniform(0.1, 3.0),
            "replay_relative_error": rng.uniform(0.01, 0.3),
            "replay_max_abs_error": rng.uniform(0.5, 5.0),
            # Regularity
            "roughness_l1": rng.uniform(0, 5),
            "roughness_l2": rng.uniform(0, 3),
            "oscillation_score": rng.uniform(0, 1),
            "sign_flip_count": rng.integers(0, 10),
            "physical_violation_count": rng.integers(0, 5),
            "within_bounds_flag": rng.choice([0, 1]),
            # Agent metrics
            "final_decision": rng.choice(["pass", "weak_pass", "fail"]),
            "success_flag": rng.choice([0, 1]),
            "weak_pass_flag": rng.choice([0, 1]),
            "manual_review_flag": 0,
            "failure_flag": rng.choice([0, 1]),
            "iteration_count": rng.integers(1, 8),
            "replanning_count": rng.integers(0, 5),
            "runtime_sec": rng.uniform(0.5, 10.0),
            "initial_to_final_improvement": rng.uniform(-0.1, 0.5),
            "final_lambda": rng.uniform(1e-5, 10.0),
            "final_reg_order": rng.choice([1, 2]),
            "final_variant_name": v,
        })
    return pd.DataFrame(rows)


@pytest.fixture
def ablation_df():
    """Synthetic DataFrame with ablation variants."""
    rng = np.random.default_rng(1)
    ablation_variants = [
        "full_agent_baseline", "no_replanner", "no_bounds",
        "fixed_lambda_ablation", "fixed_reg_order_0",
    ]
    rows = []
    for v in ablation_variants:
        for _ in range(5):
            rows.append({
                "variant_name": v,
                "flux_family": "step",
                "noise_level": 0.5,
                "flux_rmse": rng.uniform(100, 5000),
                "replay_rmse": rng.uniform(0.1, 3.0),
                "success_flag": rng.choice([0, 1]),
                "failure_flag": rng.choice([0, 1]),
                "weak_pass_flag": 0,
                "manual_review_flag": 0,
                "final_lambda": rng.uniform(0.01, 10.0),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Metric function unit tests
# ---------------------------------------------------------------------------

class TestMetricFunctions:
    def test_flux_metrics_perfect(self):
        q = np.linspace(0, 50_000, 50)
        metrics = compute_flux_metrics(q, q)
        assert metrics["flux_l2_error"] == pytest.approx(0.0, abs=1e-6)
        assert metrics["flux_correlation"] == pytest.approx(1.0)

    def test_flux_metrics_shape_mismatch(self):
        with pytest.raises(ValueError, match="Shape mismatch"):
            compute_flux_metrics(np.ones(10), np.ones(20))

    def test_regularity_metrics_keys(self):
        q = np.sin(np.linspace(0, 4 * np.pi, 50)) * 20_000 + 40_000
        metrics = compute_regularity_metrics(q, physical_bounds=(-5e5, 5e5))
        required = [
            "roughness_l1", "roughness_l2", "oscillation_score",
            "sign_flip_count", "physical_violation_count", "within_bounds_flag",
        ]
        for k in required:
            assert k in metrics, f"Missing key: {k}"

    def test_regularity_bounds_violation(self):
        q = np.array([1e6, -1e6, 1e6])  # definitely out of [-5e5, 5e5]
        metrics = compute_regularity_metrics(q, physical_bounds=(-5e5, 5e5))
        assert metrics["physical_violation_count"] > 0
        assert metrics["within_bounds_flag"] is False


# ---------------------------------------------------------------------------
# Aggregation function tests
# ---------------------------------------------------------------------------

class TestAggregationFunctions:
    def test_summarize_by_variant_has_rows(self, mock_results_df):
        tbl = summarize_by_variant(mock_results_df)
        assert len(tbl) > 0
        assert "variant_name" in tbl.columns

    def test_summarize_by_variant_all_variants_present(self, mock_results_df):
        tbl = summarize_by_variant(mock_results_df)
        present = set(tbl["variant_name"].tolist())
        expected = {"fixed_solver", "auto_solver", "solver_plus_verifier", "full_agent"}
        assert expected == present

    def test_summarize_by_noise_grouped_correctly(self, mock_results_df):
        tbl = summarize_by_noise(mock_results_df)
        assert "variant_name" in tbl.columns
        assert "noise_level" in tbl.columns

    def test_summarize_by_flux_family_grouped_correctly(self, mock_results_df):
        tbl = summarize_by_flux_family(mock_results_df)
        assert "flux_family" in tbl.columns

    def test_ablation_summary_detected(self, ablation_df):
        tbl = compute_ablation_summary(ablation_df)
        assert tbl is not None
        assert "variant_name" in tbl.columns
        assert len(tbl) > 0

    def test_ablation_summary_none_without_ablation_variants(self, mock_results_df):
        # mock_results_df has no ablation variants → should return None
        tbl = compute_ablation_summary(mock_results_df)
        assert tbl is None


# ---------------------------------------------------------------------------
# End-to-end run_analysis test
# ---------------------------------------------------------------------------

class TestRunAnalysis:
    def test_run_analysis_creates_all_tables(self, mock_results_df, tmp_path):
        raw_csv = tmp_path / "results_raw.csv"
        mock_results_df.to_csv(raw_csv, index=False)

        run_analysis(raw_csv, tmp_path)

        assert (tmp_path / "results_summary_by_variant.csv").exists()
        assert (tmp_path / "results_summary_by_noise.csv").exists()
        assert (tmp_path / "results_summary_by_flux_family.csv").exists()

    def test_run_analysis_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            run_analysis(tmp_path / "nonexistent.csv", tmp_path)

    def test_summary_by_variant_not_empty(self, mock_results_df, tmp_path):
        raw_csv = tmp_path / "results_raw.csv"
        mock_results_df.to_csv(raw_csv, index=False)
        run_analysis(raw_csv, tmp_path)

        df = pd.read_csv(tmp_path / "results_summary_by_variant.csv")
        assert len(df) == 4   # four variants in mock_results_df

    def test_ablation_csv_created_when_present(self, ablation_df, tmp_path):
        raw_csv = tmp_path / "results_raw.csv"
        ablation_df.to_csv(raw_csv, index=False)
        run_analysis(raw_csv, tmp_path)
        assert (tmp_path / "ablation_summary.csv").exists()
