"""
test_solver.py
Tests for the Tikhonov solver on small synthetic systems.
"""

import numpy as np
import pytest
from src.regularization import build_regularization_matrix
from src.tikhonov_solver import solve_single, solve_grid
from src.types import InversionConfig


def _make_config(**kwargs) -> InversionConfig:
    defaults = dict(
        parameterization_type="piecewise_constant",
        num_parameters=8,
        reg_order=1,
        lambda_strategy="fixed",
        lambda_value=1e-2,
    )
    defaults.update(kwargs)
    return InversionConfig(**defaults)


def _make_system(n: int = 8, m: int = 20, noise: float = 0.05, seed: int = 0):
    rng = np.random.default_rng(seed)
    G = rng.standard_normal((m, n))
    x_true = np.sin(np.linspace(0, np.pi, n)) * 3.0
    y = G @ x_true + rng.standard_normal(m) * noise
    return G, y, x_true


def test_solve_single_returns_correct_shape():
    n = 8
    G, y, _ = _make_system(n=n)
    config = _make_config(num_parameters=n, lambda_value=1.0)
    result = solve_single(G, y, config, lam=1.0)
    assert len(result.estimated_x) == n
    assert len(result.fitted_y) == len(y)


def test_solve_single_residual_is_consistent():
    G, y, _ = _make_system()
    config = _make_config()
    result = solve_single(G, y, config, lam=0.1)
    x = np.array(result.estimated_x)
    expected_res = np.linalg.norm(y - G @ x)
    assert result.residual_norm == pytest.approx(expected_res, rel=1e-6)


def test_solve_single_small_lambda_fits_better():
    """Smaller lambda → better data fit (lower residual norm)."""
    G, y, _ = _make_system()
    config = _make_config()
    result_large = solve_single(G, y, config, lam=1e3)
    result_small = solve_single(G, y, config, lam=1e-6)
    assert result_small.residual_norm < result_large.residual_norm


def test_solve_single_large_lambda_smoother():
    """Larger lambda → smoother solution (larger regularisation norm)."""
    G, y, _ = _make_system()
    config = _make_config(reg_order=1)
    result_large = solve_single(G, y, config, lam=1e3)
    result_small = solve_single(G, y, config, lam=1e-6)
    assert result_large.regularization_norm < result_small.regularization_norm


def test_objective_value_matches_components():
    G, y, _ = _make_system()
    config = _make_config(lambda_value=0.5)
    lam = 0.5
    result = solve_single(G, y, config, lam)
    expected_obj = result.residual_norm**2 + lam * result.regularization_norm**2
    assert result.objective_value == pytest.approx(expected_obj, rel=1e-6)


def test_solve_grid_length():
    G, y, _ = _make_system()
    config = _make_config()
    grid = [1e-3, 1e-2, 1e-1]
    results = solve_grid(G, y, config, grid)
    assert len(results) == 3


def test_physical_bounds_clamping():
    G, y, _ = _make_system()
    # Force solution into a very tight range
    config = _make_config(physical_bounds=(0.0, 1.0))
    result = solve_single(G, y, config, lam=1e-8)
    x = np.array(result.estimated_x)
    assert np.all(x >= 0.0)
    assert np.all(x <= 1.0)


def test_order0_and_order2_run_without_error():
    G, y, _ = _make_system()
    for order in [0, 2]:
        config = _make_config(reg_order=order)
        result = solve_single(G, y, config, lam=0.1)
        assert result.status in ("success", "warning")
