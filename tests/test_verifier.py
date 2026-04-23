"""
test_verifier.py
Tests for the multi-criteria verifier.
"""

import numpy as np
import pytest
from src.types import (
    BoundaryConditions, Geometry, InversionConfig, Material,
    ProblemSpec, SolverDiagnostics, SolverResult,
)
from src.verifier import VerifierThresholds, verify


def _make_problem(n_sensors: int = 1, n_time: int = 30, noise_std=None) -> ProblemSpec:
    time_grid = list(np.linspace(0, 10, n_time))
    obs = [list(np.ones(n_time) * 300.0 + np.linspace(0, 5, n_time)) for _ in range(n_sensors)]
    return ProblemSpec(
        problem_type="1D_transient_IHCP",
        dimension=1,
        transient=True,
        target_name="boundary_heat_flux",
        time_grid=time_grid,
        sensor_positions=[0.01] * n_sensors,
        observations=obs,
        geometry=Geometry(length=0.05, n_cells=20),
        material=Material(density=7800, specific_heat=500, conductivity=50),
        boundary_conditions=BoundaryConditions(right_type="dirichlet", right_value=300.0),
        initial_condition=300.0,
        noise_std=noise_std,
    )


def _make_config(physical_bounds=None) -> InversionConfig:
    return InversionConfig(
        parameterization_type="piecewise_constant",
        num_parameters=10,
        reg_order=1,
        lambda_strategy="fixed",
        lambda_value=1.0,
        physical_bounds=physical_bounds,
    )


def _make_result(x, fitted_y) -> SolverResult:
    y_obs = np.array(fitted_y)
    residual = float(np.linalg.norm(np.zeros(len(y_obs))))  # perfect fit
    return SolverResult(
        estimated_x=list(x),
        fitted_y=list(fitted_y),
        residual_norm=residual,
        regularization_norm=0.1,
        objective_value=0.1,
        lambda_used=1.0,
        reg_order=1,
        status="success",
        diagnostics=SolverDiagnostics(
            matrix_shape=(30, 10), condition_estimate=1e3, solve_method="test"
        ),
    )


def test_perfect_smooth_solution_passes():
    """A smooth solution that perfectly fits the data should pass."""
    problem = _make_problem(n_sensors=1, n_time=30)
    config = _make_config()
    # Use the exact observations as fitted_y → zero residual
    y_obs = np.array(problem.observations).flatten()
    x = np.ones(10) * 50000.0   # smooth constant flux
    result = _make_result(x, y_obs)
    vr = verify(problem, config, result)
    assert vr.decision in ("pass", "weak_pass")


def test_oscillatory_solution_flagged_as_under_regularized():
    """Highly oscillatory solution should be flagged under-regularized."""
    problem = _make_problem(n_sensors=1, n_time=30)
    config = _make_config()
    y_obs = np.array(problem.observations).flatten()
    # Alternate sign in parameters → high oscillation
    x = np.array([(-1)**i * 1e5 for i in range(10)])
    result = _make_result(x, y_obs)
    thresh = VerifierThresholds(osc_fail=0.3)
    vr = verify(problem, config, result, thresholds=thresh)
    assert vr.tradeoff_label == "under_regularized"
    assert vr.oscillation_score > 0.3


def test_physical_bounds_violation_leads_to_manual_review():
    """Solution outside physical bounds → manual_review."""
    problem = _make_problem(n_sensors=1, n_time=30)
    config = _make_config(physical_bounds=(0.0, 1e4))
    y_obs = np.array(problem.observations).flatten()
    x = np.ones(10) * 2e4   # violates upper bound
    result = _make_result(x, y_obs)
    vr = verify(problem, config, result)
    assert vr.decision == "manual_review"
    assert not vr.physical_ok


def test_discrepancy_check_skipped_when_no_noise():
    problem = _make_problem(noise_std=None)
    config = _make_config()
    y_obs = np.array(problem.observations).flatten()
    result = _make_result(np.ones(10), y_obs)
    vr = verify(problem, config, result)
    assert vr.discrepancy_ok is None


def test_discrepancy_check_runs_when_noise_provided():
    problem = _make_problem(noise_std=0.3)
    config = _make_config()
    y_obs = np.array(problem.observations).flatten()
    result = _make_result(np.ones(10), y_obs)
    vr = verify(problem, config, result)
    # Just check it ran (not None)
    assert vr.discrepancy_ok is not None


def test_stability_check_skipped_without_nearby():
    problem = _make_problem()
    config = _make_config()
    y_obs = np.array(problem.observations).flatten()
    result = _make_result(np.ones(10), y_obs)
    vr = verify(problem, config, result, nearby_results=None)
    assert vr.stability_ok is None


def test_metrics_dict_populated():
    problem = _make_problem()
    config = _make_config()
    y_obs = np.array(problem.observations).flatten()
    result = _make_result(np.ones(10), y_obs)
    vr = verify(problem, config, result)
    assert "replay_rmse" in vr.metrics
    assert "oscillation_score" in vr.metrics
