"""
lambda_selector.py
==================
Lambda (regularisation parameter) selection strategies.

Implemented strategies
----------------------
  fixed          : use the caller-supplied lambda_value directly
  grid_search    : evaluate all lambdas on a grid, return the one with
                   lowest GCV score (fallback when neither L-curve nor
                   discrepancy apply)
  lcurve         : locate the corner of the L-curve via maximum curvature
  gcv            : generalised cross-validation score minimisation
  discrepancy    : Morozov discrepancy principle  (requires noise_std)

All selectors accept the system matrices G, L, y and return a single
scalar lambda.

Notes on accuracy
-----------------
The L-curve corner heuristic here uses a simple curvature approximation
on the log-log L-curve.  Industrial implementations use more robust
corner-detection methods (e.g., Regtools by Hansen).  This is adequate
for the prototype.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import lstsq

from src.logging_utils import get_logger

log = get_logger("lambda_selector")


# ---------------------------------------------------------------------------
# Public dispatcher
# ---------------------------------------------------------------------------


def select_lambda(
    strategy: str,
    G: np.ndarray,
    L: np.ndarray,
    y: np.ndarray,
    noise_std: float | None = None,
    lambda_value: float | None = None,
    lambda_grid: list[float] | None = None,
) -> float:
    """Select a regularisation parameter using the requested strategy.

    Parameters
    ----------
    strategy    : one of "fixed", "grid_search", "lcurve", "gcv", "discrepancy"
    G           : sensitivity matrix (M, N)
    L           : regularisation matrix (p, N)
    y           : observation vector (M,)
    noise_std   : per-observation noise std dev (scalar or None)
    lambda_value: used when strategy == "fixed"
    lambda_grid : used for "grid_search", "lcurve", "gcv", "discrepancy";
                  if None, a default logarithmic grid is built.

    Returns
    -------
    lambda_selected : float
    """
    if strategy == "fixed":
        if lambda_value is None:
            raise ValueError("strategy='fixed' requires lambda_value")
        log.debug("Lambda strategy=fixed → %.3e", lambda_value)
        return lambda_value

    grid = _default_lambda_grid(G, y) if lambda_grid is None else np.asarray(lambda_grid)

    if strategy == "gcv" or strategy == "grid_search":
        lam = _gcv(G, L, y, grid)
        log.debug("Lambda strategy=%s → %.3e", strategy, lam)
        return lam

    if strategy == "lcurve":
        lam = _lcurve_corner(G, L, y, grid)
        log.debug("Lambda strategy=lcurve → %.3e", lam)
        return lam

    if strategy == "discrepancy":
        if noise_std is None:
            log.warning("discrepancy requested but noise_std=None; falling back to GCV")
            return _gcv(G, L, y, grid)
        lam = _discrepancy(G, L, y, grid, noise_std)
        log.debug("Lambda strategy=discrepancy → %.3e", lam)
        return lam

    raise ValueError(f"Unknown lambda strategy: {strategy!r}")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _default_lambda_grid(G: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Build a logarithmic lambda grid heuristically scaled to the problem."""
    # Scale by the largest singular value of G (proxy for data power)
    # to get a range that covers under- and over-regularisation.
    sigma_max = np.linalg.norm(G, ord=2)   # largest singular value estimate
    lam_min = sigma_max * 1e-6
    lam_max = sigma_max * 1e2
    return np.logspace(np.log10(lam_min), np.log10(lam_max), 60)


def _solve_tikhonov(
    G: np.ndarray, L: np.ndarray, y: np.ndarray, lam: float
) -> np.ndarray:
    """Solve  min_x ||Gx-y||^2 + lam^2 ||Lx||^2  via normal equations."""
    GtG = G.T @ G
    LtL = L.T @ L
    A = GtG + lam * LtL
    b = G.T @ y
    # Use lstsq for robustness against ill-conditioning
    x, *_ = lstsq(A, b, cond=None)
    return x


def _gcv(G: np.ndarray, L: np.ndarray, y: np.ndarray, grid: np.ndarray) -> float:
    """GCV score: minimise  ||Gy-hat - y||^2 / (1 - h_ii)^2  heuristic.

    The closed-form GCV for Tikhonov regularisation is:
        GCV(lam) = ||r(lam)||^2 / trace(I - G A_lam^{-1} G^T)^2

    where A_lam = G^T G + lam * L^T L.

    For speed we use the SVD of the augmented system.
    """
    M, N = G.shape
    # SVD of G for efficient computation
    U, s, Vt = np.linalg.svd(G, full_matrices=False)

    scores = []
    for lam in grid:
        # Filter factors  d_i^2 / (d_i^2 + lam * ||L v_i||^2)
        # Simplified: use identity L (order=0) approximation for the
        # influence matrix trace when L != I, then correct residuals.
        # For a rigorous GCV with general L, one would use the
        # generalised SVD (GSVD).  That is out of scope for the prototype;
        # we compute residuals directly.
        x_lam = _solve_tikhonov(G, L, y, lam)
        r = y - G @ x_lam
        res_sq = float(r @ r)

        # Effective degrees of freedom: trace of hat matrix
        # Using the identity:  tr(H) = sum  s_i^2 / (s_i^2 + lam)
        # (exact only when L=I, approximate otherwise)
        h_trace = float(np.sum(s**2 / (s**2 + lam)))
        dof = M - h_trace
        if dof <= 0:
            scores.append(np.inf)
        else:
            scores.append(res_sq / dof**2)

    best = int(np.argmin(scores))
    return float(grid[best])


def _lcurve_corner(
    G: np.ndarray, L: np.ndarray, y: np.ndarray, grid: np.ndarray
) -> float:
    """Select lambda at the corner of the L-curve.

    The L-curve plots log ||r|| vs log ||Lx|| for varying lambda.
    The corner (maximum curvature point) balances fit and regularity.

    Curvature is estimated using finite differences on the log-log curve.
    """
    log_res = []
    log_reg = []

    for lam in grid:
        x_lam = _solve_tikhonov(G, L, y, lam)
        r = y - G @ x_lam
        log_res.append(np.log(max(np.linalg.norm(r), 1e-20)))
        log_reg.append(np.log(max(np.linalg.norm(L @ x_lam), 1e-20)))

    eta = np.array(log_res)
    xi = np.array(log_reg)

    # Estimate curvature via second-order finite differences on the L-curve
    # Parameterize by index; curvature ≈ (eta'' * xi' - eta' * xi'') / (eta'^2 + xi'^2)^(3/2)
    if len(eta) < 3:
        return float(grid[len(grid) // 2])

    deta = np.gradient(eta)
    dxi = np.gradient(xi)
    d2eta = np.gradient(deta)
    d2xi = np.gradient(dxi)

    num = deta * d2xi - d2eta * dxi
    den = (deta**2 + dxi**2) ** 1.5 + 1e-30
    curvature = num / den

    # Corner = maximum curvature (most negative curvature in signed sense)
    # We look for the index with the largest magnitude in the region where
    # the L-curve transitions from steep to shallow.
    corner_idx = int(np.argmax(np.abs(curvature)))
    return float(grid[corner_idx])


def _discrepancy(
    G: np.ndarray,
    L: np.ndarray,
    y: np.ndarray,
    grid: np.ndarray,
    noise_std: float,
) -> float:
    """Morozov discrepancy principle: find lambda such that ||Gx - y|| ≈ sqrt(M) * noise_std.

    The target residual norm is:
        delta = sqrt(M) * noise_std

    We scan the grid and return the lambda whose residual norm is
    closest to delta.
    """
    M = len(y)
    delta = np.sqrt(M) * noise_std

    res_norms = []
    for lam in grid:
        x_lam = _solve_tikhonov(G, L, y, lam)
        r = y - G @ x_lam
        res_norms.append(np.linalg.norm(r))

    res_norms = np.array(res_norms)
    best_idx = int(np.argmin(np.abs(res_norms - delta)))
    return float(grid[best_idx])
