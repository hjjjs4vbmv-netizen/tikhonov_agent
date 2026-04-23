"""
tsvd_solver.py
==============
Truncated SVD (TSVD) inversion solver.

Solves the inverse problem  G x ≈ y  via truncated SVD:

    G = U S V^T   (full SVD)
    x_k = V_k  S_k^{-1}  U_k^T  y

where the subscript k denotes keeping only the k largest singular values
(those above a threshold relative to the maximum singular value).

Regularisation parameter interpretation
---------------------------------------
The ``lam`` argument is reused as the *truncation threshold fraction*:

    keep singular value s_j  iff  s_j / s_max  ≥  lam

- lam → 0  : keep all (or most) singular values → less regularization
- lam → 1  : keep very few singular values      → heavy regularization
- Default practical range: 1e-4 to 0.1

This mapping lets TSVD participate in the same agent loop and lambda-
selection infrastructure as the Tikhonov solver.  When ``strategy="fixed"``
is used, the caller directly controls the truncation level.

Compatibility note
------------------
TSVD accepts the same ``(G, y, config, lam)`` signature as
``tikhonov_solver.solve_single``, making it a drop-in alternative through
the SolverRegistry without any changes to the agent loop.

The L-curve / GCV / discrepancy lambda selectors are Tikhonov-specific and
may not be meaningful for TSVD; use ``lambda_strategy: "fixed"`` when
running TSVD for predictable behaviour.
"""

from __future__ import annotations

import numpy as np

from src.logging_utils import get_logger
from src.regularization import regularization_norm
from src.types import InversionConfig, SolverDiagnostics, SolverResult
from src.utils import Timer

log = get_logger("tsvd_solver")


# ---------------------------------------------------------------------------
# Public API  (mirrors tikhonov_solver.solve_single / solve_grid interface)
# ---------------------------------------------------------------------------


def solve_single(
    G: np.ndarray,
    y: np.ndarray,
    config: InversionConfig,
    lam: float,
) -> SolverResult:
    """Solve the inverse problem for a single truncation threshold.

    Parameters
    ----------
    G      : sensitivity matrix, shape (M, N)
    y      : observation vector, shape (M,)
    config : inversion config (supplies physical_bounds; reg_order used
             only for the regularization_norm diagnostic)
    lam    : truncation threshold fraction in (0, 1].
             Singular values below  lam * s_max  are discarded.

    Returns
    -------
    SolverResult  (same structure as tikhonov_solver output)
    """
    warnings: list[str] = []
    N = G.shape[1]

    with Timer() as t:
        x, k_kept, s_max, s_min_kept, diag = _solve_tsvd(G, y, lam, N, warnings)

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

    from src.regularization import build_regularization_matrix
    L = build_regularization_matrix(N, config.reg_order)

    fitted_y = G @ x
    residual_norm = float(np.linalg.norm(y - fitted_y))
    reg_norm = regularization_norm(L, x)
    # For TSVD, `lam` is a truncation threshold fraction, not a Tikhonov
    # regularization weight.  Reporting lam * reg_norm**2 would be
    # dimensionally inconsistent.  objective_value is set to residual_norm**2
    # (the data-fit term alone); the number of kept singular values (encoded
    # in solve_method) is the regularization descriptor.
    obj = residual_norm**2

    status: str
    if k_kept == 0:
        warnings.append("TSVD: zero singular values kept — solution is zero vector")
        status = "warning"
    elif diag.condition_estimate > 1e12:
        warnings.append(f"TSVD: effective condition ≈ {diag.condition_estimate:.2e}")
        status = "warning"
    else:
        status = "success"

    log.debug(
        "tsvd_solve_single: threshold=%.3e, k_kept=%d, residual=%.4f, cond=%.2e",
        lam, k_kept, residual_norm, diag.condition_estimate,
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
    """Solve for every threshold in *lambda_grid* and return all results."""
    return [solve_single(G, y, config, lam) for lam in lambda_grid]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _solve_tsvd(
    G: np.ndarray,
    y: np.ndarray,
    threshold: float,
    N: int,
    warnings: list[str],
) -> tuple[np.ndarray, int, float, float, SolverDiagnostics]:
    """Compute the TSVD solution.

    Returns (x, k_kept, s_max, s_min_kept, diagnostics).
    """
    try:
        U, s, Vt = np.linalg.svd(G, full_matrices=False)
    except np.linalg.LinAlgError as exc:
        warnings.append(f"SVD failed: {exc}; returning zero solution")
        diag = SolverDiagnostics(
            matrix_shape=G.shape,
            condition_estimate=float("inf"),
            solve_method="tsvd_svd_failed",
            warnings=warnings,
        )
        return np.zeros(N), 0, 0.0, 0.0, diag

    s_max = float(s[0]) if len(s) > 0 else 0.0

    # Determine truncation rank
    if s_max < 1e-300:
        warnings.append("TSVD: all singular values are numerically zero")
        k_kept = 0
    else:
        cutoff = threshold * s_max
        mask = s >= cutoff
        k_kept = int(np.sum(mask))

    if k_kept == 0:
        diag = SolverDiagnostics(
            matrix_shape=G.shape,
            condition_estimate=float("inf"),
            solve_method="tsvd",
            warnings=warnings,
        )
        return np.zeros(N), 0, s_max, 0.0, diag

    # Truncated solution: x = V_k @ diag(1/s_k) @ U_k^T @ y
    U_k = U[:, :k_kept]
    s_k = s[:k_kept]
    Vt_k = Vt[:k_kept, :]

    x = Vt_k.T @ (np.diag(1.0 / s_k) @ (U_k.T @ y))

    s_min_kept = float(s_k[-1])
    cond_est = s_max / s_min_kept if s_min_kept > 1e-300 else float("inf")

    diag = SolverDiagnostics(
        matrix_shape=G.shape,
        condition_estimate=cond_est,
        solve_method=f"tsvd_k{k_kept}",
        warnings=warnings,
    )
    return x, k_kept, s_max, s_min_kept, diag
