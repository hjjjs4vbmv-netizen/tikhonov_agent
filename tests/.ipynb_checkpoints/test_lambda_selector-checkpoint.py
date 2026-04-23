"""
test_lambda_selector.py
Tests for lambda selection strategies.
"""

import numpy as np
import pytest
from src.lambda_selector import select_lambda


def _make_small_system(seed: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (G, L, y) for a small well-conditioned test system."""
    rng = np.random.default_rng(seed)
    n = 10
    G = rng.standard_normal((20, n))
    L = np.eye(n)
    x_true = np.ones(n) * 2.0
    y = G @ x_true + rng.standard_normal(20) * 0.1
    return G, L, y


def test_fixed_returns_given_lambda():
    G, L, y = _make_small_system()
    lam = select_lambda("fixed", G, L, y, lambda_value=0.5)
    assert lam == pytest.approx(0.5)


def test_fixed_requires_lambda_value():
    G, L, y = _make_small_system()
    with pytest.raises(ValueError):
        select_lambda("fixed", G, L, y)


def test_gcv_returns_positive_scalar():
    G, L, y = _make_small_system()
    lam = select_lambda("gcv", G, L, y)
    assert lam > 0


def test_lcurve_returns_positive_scalar():
    G, L, y = _make_small_system()
    lam = select_lambda("lcurve", G, L, y)
    assert lam > 0


def test_discrepancy_returns_positive_scalar():
    G, L, y = _make_small_system()
    lam = select_lambda("discrepancy", G, L, y, noise_std=0.1)
    assert lam > 0


def test_discrepancy_falls_back_to_gcv_when_no_noise():
    """discrepancy without noise_std should fall back to GCV (no error)."""
    G, L, y = _make_small_system()
    lam = select_lambda("discrepancy", G, L, y, noise_std=None)
    assert lam > 0


def test_unknown_strategy_raises():
    G, L, y = _make_small_system()
    with pytest.raises(ValueError):
        select_lambda("magic", G, L, y)


def test_larger_noise_gives_larger_lambda_discrepancy():
    """Higher noise should push the discrepancy lambda toward larger values."""
    G, L, y = _make_small_system(seed=1)
    lam_low = select_lambda("discrepancy", G, L, y, noise_std=0.01)
    lam_high = select_lambda("discrepancy", G, L, y, noise_std=5.0)
    # Not guaranteed to be monotone in general but should hold for this simple case
    assert lam_high >= lam_low
