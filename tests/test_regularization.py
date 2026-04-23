"""
test_regularization.py
Tests for regularization matrix construction.
"""

import numpy as np
import pytest
from src.regularization import (
    build_regularization_matrix,
    regularization_norm,
    regularization_norm_squared,
)


def test_order0_is_identity():
    L = build_regularization_matrix(5, 0)
    assert L.shape == (5, 5)
    np.testing.assert_array_equal(L, np.eye(5))


def test_order1_shape_and_values():
    L = build_regularization_matrix(5, 1)
    assert L.shape == (4, 5)
    # Row 0 should be [-1, 1, 0, 0, 0]
    np.testing.assert_array_equal(L[0], [-1, 1, 0, 0, 0])
    # Row 3 should be [0, 0, 0, -1, 1]
    np.testing.assert_array_equal(L[3], [0, 0, 0, -1, 1])


def test_order2_shape_and_values():
    L = build_regularization_matrix(5, 2)
    assert L.shape == (3, 5)
    # Row 0: [1, -2, 1, 0, 0]
    np.testing.assert_array_equal(L[0], [1, -2, 1, 0, 0])


def test_order1_constant_vector_gives_zero_norm():
    """First-difference of a constant vector should be zero."""
    L = build_regularization_matrix(6, 1)
    x = np.ones(6) * 3.7
    assert regularization_norm(L, x) == pytest.approx(0.0, abs=1e-12)


def test_order2_linear_vector_gives_zero_norm():
    """Second-difference of a linear vector should be zero."""
    L = build_regularization_matrix(6, 2)
    x = np.arange(6, dtype=float)
    assert regularization_norm(L, x) == pytest.approx(0.0, abs=1e-12)


def test_invalid_order_raises():
    with pytest.raises(ValueError):
        build_regularization_matrix(5, 3)


def test_too_small_n_raises():
    with pytest.raises(ValueError):
        build_regularization_matrix(1, 2)


def test_norm_squared_equals_norm_squared():
    L = build_regularization_matrix(5, 1)
    x = np.array([1.0, 2.0, 0.5, 3.0, 1.0])
    n = regularization_norm(L, x)
    n2 = regularization_norm_squared(L, x)
    assert n2 == pytest.approx(n**2, rel=1e-10)
