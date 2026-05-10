"""
test_deepxde_solver.py
======================
Smoke tests for the DeepXDE/PyTorch inversion solver integration.

These tests verify:
  1. The registry registers "deepxde" correctly.
  2. solve_single returns a valid SolverResult on a tiny synthetic case.
  3. Diagnostics / status fields are present.
  4. Backend/device info is visible in solve_method.

If deepxde is not installed, every test is skipped with a clear message
rather than failing.  Install `deepxde` and `torch` and set
DDE_BACKEND=pytorch to run the full suite.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Dependency check
# ---------------------------------------------------------------------------

_DEEPXDE_AVAILABLE = False
_SKIP_REASON = ""

try:
    os.environ.setdefault("DDE_BACKEND", "pytorch")
    import deepxde  # noqa: F401
    import torch  # noqa: F401
    _DEEPXDE_AVAILABLE = True
except ImportError as _exc:
    _SKIP_REASON = (
        f"deepxde or torch not installed ({_exc}). "
        "Run: pip install deepxde torch && export DDE_BACKEND=pytorch"
    )

requires_deepxde = pytest.mark.skipif(
    not _DEEPXDE_AVAILABLE,
    reason=_SKIP_REASON,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tiny_problem():
    """A tiny 4×3 synthetic inverse problem (small enough for fast CI runs)."""
    rng = np.random.default_rng(42)
    G = rng.standard_normal((4, 3))
    x_true = np.array([1.0, -0.5, 0.8])
    y = G @ x_true + rng.standard_normal(4) * 0.05
    return G, y


@pytest.fixture()
def minimal_config():
    """Minimal InversionConfig suitable for deepxde_solver."""
    from src.types import InversionConfig
    cfg = InversionConfig(
        reg_order=1,
        physical_bounds=None,
    )
    # Override deepxde iterations to keep the test fast
    cfg.deepxde_iterations = 200
    cfg.deepxde_lr = 0.05
    cfg.deepxde_optimizer = "adam"
    cfg.deepxde_device = "cpu"
    return cfg


# ---------------------------------------------------------------------------
# Registry tests (no deepxde import required)
# ---------------------------------------------------------------------------

class TestRegistry:
    def test_deepxde_in_registry(self):
        """Registry must include 'deepxde' regardless of whether deepxde is installed."""
        from src.solver_registry import get_registry
        registry = get_registry()
        assert "deepxde" in registry.available(), (
            f"'deepxde' not found in registry. Available: {registry.available()}"
        )

    def test_registry_has_all_three_solvers(self):
        from src.solver_registry import get_registry
        registry = get_registry()
        available = set(registry.available())
        assert {"tikhonov", "tsvd", "deepxde"}.issubset(available), (
            f"Registry missing solvers. Got: {available}"
        )

    def test_registry_get_returns_module(self):
        from src.solver_registry import get_registry
        registry = get_registry()
        mod = registry.get("deepxde")
        assert callable(getattr(mod, "solve_single", None))
        assert callable(getattr(mod, "solve_grid", None))


# ---------------------------------------------------------------------------
# Solver functional tests (require deepxde + torch)
# ---------------------------------------------------------------------------

class TestDeepXDESolverFunctional:
    @requires_deepxde
    def test_solve_single_returns_solver_result(self, tiny_problem, minimal_config):
        from src.solver_registry import get_registry
        from src.types import SolverResult

        G, y = tiny_problem
        registry = get_registry()
        result = registry.solve_single("deepxde", G, y, minimal_config, lam=0.1)

        assert isinstance(result, SolverResult), (
            f"Expected SolverResult, got {type(result)}"
        )

    @requires_deepxde
    def test_result_fields_present(self, tiny_problem, minimal_config):
        from src.solver_registry import get_registry

        G, y = tiny_problem
        registry = get_registry()
        result = registry.solve_single("deepxde", G, y, minimal_config, lam=0.1)

        assert result.estimated_x is not None
        assert len(result.estimated_x) == G.shape[1]
        assert result.status in ("success", "warning", "failed")
        assert np.isfinite(result.residual_norm)
        assert np.isfinite(result.regularization_norm)
        assert result.lambda_used == pytest.approx(0.1)

    @requires_deepxde
    def test_diagnostics_present(self, tiny_problem, minimal_config):
        from src.solver_registry import get_registry

        G, y = tiny_problem
        registry = get_registry()
        result = registry.solve_single("deepxde", G, y, minimal_config, lam=0.1)

        assert result.diagnostics is not None
        assert "deepxde" in result.diagnostics.solve_method.lower()
        assert result.diagnostics.timing >= 0.0

    @requires_deepxde
    def test_solve_grid_returns_list(self, tiny_problem, minimal_config):
        from src.solver_registry import get_registry

        G, y = tiny_problem
        registry = get_registry()
        lam_grid = [0.001, 0.01, 0.1]
        results = registry.solve_grid("deepxde", G, y, minimal_config, lam_grid)

        assert isinstance(results, list)
        assert len(results) == len(lam_grid)

    @requires_deepxde
    def test_solution_finite(self, tiny_problem, minimal_config):
        from src.solver_registry import get_registry

        G, y = tiny_problem
        registry = get_registry()
        result = registry.solve_single("deepxde", G, y, minimal_config, lam=0.1)

        x = np.array(result.estimated_x)
        assert np.all(np.isfinite(x)), f"Non-finite values in solution: {x}"

    @requires_deepxde
    def test_lbfgs_optimizer(self, tiny_problem, minimal_config):
        """Verify lbfgs optimizer path runs without error."""
        from src.solver_registry import get_registry

        G, y = tiny_problem
        minimal_config.deepxde_optimizer = "lbfgs"
        minimal_config.deepxde_iterations = 100
        minimal_config.deepxde_adam_iterations = 50

        registry = get_registry()
        result = registry.solve_single("deepxde", G, y, minimal_config, lam=0.1)
        assert result.status in ("success", "warning")
        assert "lbfgs" in result.diagnostics.solve_method.lower()


# ---------------------------------------------------------------------------
# Dependency-missing behaviour test
# ---------------------------------------------------------------------------

class TestDependencyMissing:
    def test_import_error_message_is_clear(self, monkeypatch):
        """When deepxde is absent the solver raises ImportError with a clear message."""
        import unittest.mock as mock

        # Patch builtins.__import__ to simulate missing deepxde
        real_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

        def fake_import(name, *args, **kwargs):
            if name == "deepxde":
                raise ImportError("No module named 'deepxde'")
            return real_import(name, *args, **kwargs)

        import src.deepxde_solver as dxs

        with pytest.raises(ImportError, match="deepxde_solver requires DeepXDE"):
            with mock.patch("builtins.__import__", side_effect=fake_import):
                # Force re-execution of the import block inside _solve_with_deepxde_torch
                from src.types import InversionConfig
                cfg = InversionConfig()
                rng = np.random.default_rng(0)
                G = rng.standard_normal((3, 2))
                y = rng.standard_normal(3)
                L = np.eye(2)
                dxs._solve_with_deepxde_torch(G, y, L, 0.1, cfg, [])
