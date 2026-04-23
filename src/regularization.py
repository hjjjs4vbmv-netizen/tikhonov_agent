"""
regularization.py
=================
Regularisation matrix construction for Tikhonov inversion.

Supported orders
----------------
  0  →  L = I             (zero-order / Tikhonov ridge)
  1  →  L = first-difference operator  (promotes smoothness in q'(t))
  2  →  L = second-difference operator (promotes smoothness in q''(t))

All matrices are returned as dense numpy arrays.  For the prototype
sizes involved (n_params typically 10–50) this is perfectly adequate.
Sparse versions can be swapped in for larger problems by changing the
return type to ``scipy.sparse.csr_matrix``.
"""

from __future__ import annotations

import numpy as np


def build_regularization_matrix(n: int, order: int) -> np.ndarray:
    """Build the regularisation matrix L for Tikhonov regularisation.

    Parameters
    ----------
    n     : number of inversion parameters
    order : 0, 1, or 2

    Returns
    -------
    L : ndarray, shape determined by order
        order=0  →  (n, n)  identity
        order=1  →  (n-1, n) first-difference
        order=2  →  (n-2, n) second-difference

    Raises
    ------
    ValueError  if order not in {0, 1, 2} or n is too small for the order.
    """
    if order not in (0, 1, 2):
        raise ValueError(f"reg_order must be 0, 1, or 2; got {order}")
    if n < order + 1:
        raise ValueError(
            f"n={n} too small for reg_order={order}; need n >= {order + 1}"
        )

    if order == 0:
        return np.eye(n)

    if order == 1:
        # First-difference: L[i,i] = -1,  L[i,i+1] = 1
        L = np.zeros((n - 1, n))
        for i in range(n - 1):
            L[i, i] = -1.0
            L[i, i + 1] = 1.0
        return L

    # order == 2: second-difference
    # L[i,i] = 1,  L[i,i+1] = -2,  L[i,i+2] = 1
    L = np.zeros((n - 2, n))
    for i in range(n - 2):
        L[i, i] = 1.0
        L[i, i + 1] = -2.0
        L[i, i + 2] = 1.0
    return L


def regularization_norm(L: np.ndarray, x: np.ndarray) -> float:
    """Compute ||Lx||_2."""
    return float(np.linalg.norm(L @ x))


def regularization_norm_squared(L: np.ndarray, x: np.ndarray) -> float:
    """Compute ||Lx||_2^2  (used in the objective function)."""
    Lx = L @ x
    return float(Lx @ Lx)
