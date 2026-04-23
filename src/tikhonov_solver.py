"""
tikhonov_solver.py
==================
Tikhonov inversion solver.

Solves:
    min_x  ||G x - y||_2^2  +  lambda * ||L x||_2^2

via the normal equations:
    (G^T G + lambda L^T L) x = G^T y

Uses scipy.linalg.lstsq for numerical stability (handles near-singular
systems more gracefully than np.linalg.solve).

The solver can operate in two modes:
  1. Single-lambda solve   : ``solve_single``
  2. Grid scan             : ``solve_grid`` (evaluates many lambdas and
                             returns all results; the agent selects the best)
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import lstsq

from src.logging_utils import get_logger
from src.regularization import (
    build_regularization_matrix,
    regularization_norm,
    regularization_norm_squared,
)
from src.types import InversionConfig, SolverDiagnostics, SolverResult
from src.utils import Timer

log = get_logger("tikhonov_solver")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def solve_single(
    G: np.ndarray,
    y: np.ndarray,
    config: InversionConfig,
    lam: float,
) -> SolverResult:
    """Solve the Tikhonov problem for a single regularisation parameter.

    Parameters
    ----------
    G      : sensitivity matrix, shape (M, N)
    y      : observation vector, shape (M,)
    config : inversion config (supplies reg_order, physical_bounds)
    lam    : regularisation parameter (already selected)

    Returns
    -------
    SolverResult with diagnostics
    """
    N = G.shape[1]
    L = build_regularization_matrix(N, config.reg_order)
    warnings: list[str] = []

    with Timer() as t:
        x, diag = _solve_normal_equations(G, L, y, lam, warnings)

    # Apply physical bounds if provided
    if config.physical_bounds is not None:
        lo, hi = config.physical_bounds
        x_clamped = np.clip(x, lo, hi)
        if not np.allclose(x, x_clamped):
            warnings.append(
                f"Solution clamped to physical bounds [{lo}, {hi}]; "
                f"{int(np.sum(x != x_clamped))} parameters affected"
            )
        x = x_clamped

    diag.timing = t.elapsed
    diag.warnings = warnings

    fitted_y = G @ x
    residual_norm = float(np.linalg.norm(y - fitted_y))
    reg_norm = regularization_norm(L, x)
    obj = residual_norm**2 + lam * reg_norm**2

    status: str
    if diag.condition_estimate > 1e12:
        warnings.append(f"Ill-conditioned system: cond ≈ {diag.condition_estimate:.2e}")
        status = "warning"
    else:
        status = "success"

    log.debug(
        "solve_single: lambda=%.3e, residual=%.4f, reg_norm=%.4f, cond=%.2e",
        lam, residual_norm, reg_norm, diag.condition_estimate,
    )

    return SolverResult(
        estimated_x=x.tolist(),
        fitted_y=fitted_y.tolist(),
        residual_norm=residual_norm,
        regularization_norm=reg_norm,
        objective_value=obj,
        lambda_used=lam,
        reg_order=config.reg_order,
        status=status,  # type: ignore[arg-type]
        diagnostics=diag,
    )


def solve_grid(
    G: np.ndarray,
    y: np.ndarray,
    config: InversionConfig,
    lambda_grid: list[float],
) -> list[SolverResult]:
    """Solve for every lambda in *lambda_grid* and return all results.

    The caller (agent or lambda_selector) is responsible for choosing
    the best result from the returned list.
    """
    results = []
    for lam in lambda_grid:
        results.append(solve_single(G, y, config, lam))
    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _solve_normal_equations(
    G: np.ndarray,
    L: np.ndarray,
    y: np.ndarray,
    lam: float,
    warnings: list[str],
) -> tuple[np.ndarray, SolverDiagnostics]:
    """Form and solve the normal equations.

    Returns (x, diagnostics).
    """
    GtG = G.T @ G
    LtL = L.T @ L
    A = GtG + lam * LtL
    b = G.T @ y

    # Condition estimate via ratio of largest/smallest eigenvalue of A
    try:
        eigvals = np.linalg.eigvalsh(A)
        eigvals_pos = np.abs(eigvals)
        cond_est = float(eigvals_pos.max() / (eigvals_pos.min() + 1e-300))
    except np.linalg.LinAlgError:
        cond_est = float("inf")
        warnings.append("Eigenvalue computation failed; condition estimate unavailable")

    # Solve using lstsq for robustness
    try:
        x, residuals, rank, sv = lstsq(A, b, cond=None)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"lstsq failed: {exc}; returning zeros")
        x = np.zeros(G.shape[1])
        rank = 0
        sv = np.array([])

    diag = SolverDiagnostics(
        matrix_shape=A.shape,
        condition_estimate=cond_est,
        solve_method="lstsq_normal_equations",
        warnings=warnings,
    )
    return x, diag
