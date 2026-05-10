"""
deepxde_solver.py
=================
DeepXDE/PyTorch-backend inversion solver.

Solves the same regularised linear inverse problem as the Tikhonov solver:

    min_x  ||G x - y||_2^2 + lambda * ||L x||_2^2

Instead of forming normal equations, this module treats x as a trainable
variable and optimises the objective with the DeepXDE-selected PyTorch backend.
This is useful when you later want to extend the inverse model with nonlinear
DeepXDE/PINN residuals while keeping the same SolverRegistry interface.

Public API
----------
    solve_single(G, y, config, lam) -> SolverResult
    solve_grid(G, y, config, lambda_grid) -> list[SolverResult]

Expected optional config attributes
-----------------------------------
These are read with getattr(..., default), so InversionConfig does not need to
already define them.

    deepxde_iterations      : int, default 5000
    deepxde_lr              : float, default 1e-2
    deepxde_optimizer       : str, default "adam"; supports "adam" or "lbfgs"
    deepxde_adam_iterations : int, default 2000; warm start steps before LBFGS
    deepxde_device          : str, default "cpu"; e.g. "cuda" when available
    deepxde_init            : str, default "zeros"; "zeros" or "lstsq"

Notes
-----
DeepXDE has several supported backends. This implementation intentionally uses
its PyTorch backend because direct vector optimisation is concise and stable.
Set the backend before importing DeepXDE, for example:

    export DDE_BACKEND=pytorch

or in Python before importing this module:

    import os
    os.environ["DDE_BACKEND"] = "pytorch"
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import numpy as np

from src.logging_utils import get_logger
from src.regularization import build_regularization_matrix, regularization_norm
from src.types import InversionConfig, SolverDiagnostics, SolverResult
from src.utils import Timer

if TYPE_CHECKING:
    import torch

log = get_logger("deepxde_solver")


# ---------------------------------------------------------------------------
# Public API: mirrors tikhonov_solver / tsvd_solver
# ---------------------------------------------------------------------------


def solve_single(
    G: np.ndarray,
    y: np.ndarray,
    config: InversionConfig,
    lam: float,
) -> SolverResult:
    """Solve the inverse problem for a single regularisation parameter.

    Parameters
    ----------
    G      : sensitivity matrix, shape (M, N)
    y      : observation vector, shape (M,)
    config : inversion config. Existing fields used: reg_order,
             physical_bounds. Optional DeepXDE fields are read via getattr.
    lam    : regularisation weight, same meaning as in Tikhonov.

    Returns
    -------
    SolverResult with diagnostics compatible with other solvers.
    """
    warnings: list[str] = []
    G = np.asarray(G, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1)
    N = G.shape[1]
    L = build_regularization_matrix(N, config.reg_order)

    if G.ndim != 2:
        raise ValueError(f"G must be 2-D, got shape {G.shape}")
    if y.shape[0] != G.shape[0]:
        raise ValueError(f"y length {y.shape[0]} does not match G rows {G.shape[0]}")
    if lam < 0:
        warnings.append(f"Negative lambda {lam} received; using abs(lambda)")
        lam = abs(lam)

    with Timer() as t:
        x, final_loss, n_iter, opt_name = _solve_with_deepxde_torch(
            G=G,
            y=y,
            L=L,
            lam=lam,
            config=config,
            warnings=warnings,
        )

    # Apply physical bounds after optimisation, mirroring existing solvers.
    if config.physical_bounds is not None:
        lo, hi = config.physical_bounds
        x_clamped = np.clip(x, lo, hi)
        if not np.allclose(x, x_clamped):
            warnings.append(
                f"Solution clamped to physical bounds [{lo}, {hi}]; "
                f"{int(np.sum(x != x_clamped))} parameters affected"
            )
        x = x_clamped

    fitted_y = G @ x
    residual_norm = float(np.linalg.norm(y - fitted_y))
    reg_norm = regularization_norm(L, x)
    obj = residual_norm**2 + lam * reg_norm**2

    cond_est = _condition_estimate(G, L, lam, warnings)
    status: str
    if not np.isfinite(final_loss):
        warnings.append("DeepXDE optimisation produced a non-finite loss")
        status = "warning"
    elif cond_est > 1e12:
        warnings.append(f"Ill-conditioned system: cond ≈ {cond_est:.2e}")
        status = "warning"
    else:
        status = "success"

    diag = SolverDiagnostics(
        matrix_shape=G.shape,
        condition_estimate=cond_est,
        solve_method=f"deepxde_{opt_name}_iters{n_iter}",
        timing=t.elapsed,
        warnings=warnings,
    )

    log.debug(
        "deepxde_solve_single: lambda=%.3e, residual=%.4f, reg_norm=%.4f, "
        "loss=%.4f, cond=%.2e",
        lam,
        residual_norm,
        reg_norm,
        final_loss,
        cond_est,
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
    """Solve for every lambda in *lambda_grid* and return all results."""
    return [solve_single(G, y, config, lam) for lam in lambda_grid]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _solve_with_deepxde_torch(
    G: np.ndarray,
    y: np.ndarray,
    L: np.ndarray,
    lam: float,
    config: InversionConfig,
    warnings: list[str],
) -> tuple[np.ndarray, float, int, str]:
    """Optimise x with the DeepXDE PyTorch backend.

    Returns
    -------
    x, final_loss, iterations_used, optimizer_name
    """
    # Prefer PyTorch backend when the caller has not already selected one.
    os.environ.setdefault("DDE_BACKEND", "pytorch")

    try:
        import deepxde as dde  # noqa: F401  # imported to initialise/check backend
        from deepxde.backend import backend_name
        import torch
    except Exception as exc:  # noqa: BLE001
        raise ImportError(
            "deepxde_solver requires DeepXDE with the PyTorch backend. "
            "Install deepxde and torch, and set DDE_BACKEND=pytorch."
        ) from exc

    if backend_name != "pytorch":
        raise RuntimeError(
            "deepxde_solver currently supports DDE_BACKEND=pytorch only; "
            f"current DeepXDE backend is {backend_name!r}. Set DDE_BACKEND=pytorch "
            "before importing deepxde."
        )

    device = getattr(config, "deepxde_device", "cpu")
    dtype = torch.float64

    G_t = torch.as_tensor(G, dtype=dtype, device=device)
    y_t = torch.as_tensor(y, dtype=dtype, device=device)
    L_t = torch.as_tensor(L, dtype=dtype, device=device)

    x0 = _initial_guess(G, y, config, warnings)
    x = torch.nn.Parameter(torch.as_tensor(x0, dtype=dtype, device=device))

    optimizer_name = str(getattr(config, "deepxde_optimizer", "adam")).lower()
    iterations = int(getattr(config, "deepxde_iterations", 5000))
    lr = float(getattr(config, "deepxde_lr", 1e-2))

    if iterations <= 0:
        warnings.append("deepxde_iterations <= 0; returning initial guess")
        return x.detach().cpu().numpy(), float("nan"), 0, "none"

    def loss_fn() -> torch.Tensor:
        residual = G_t.matmul(x) - y_t
        reg = L_t.matmul(x)
        return torch.sum(residual * residual) + float(lam) * torch.sum(reg * reg)

    final_loss = float("nan")
    n_iter = 0

    if optimizer_name == "lbfgs":
        warmup = int(getattr(config, "deepxde_adam_iterations", min(2000, iterations)))
        if warmup > 0:
            adam = torch.optim.Adam([x], lr=lr)
            for _ in range(warmup):
                adam.zero_grad()
                loss = loss_fn()
                loss.backward()
                adam.step()
            n_iter += warmup

        lbfgs_steps = max(iterations - warmup, 1)
        lbfgs = torch.optim.LBFGS(
            [x],
            lr=1.0,
            max_iter=lbfgs_steps,
            line_search_fn="strong_wolfe",
        )

        def closure() -> torch.Tensor:
            lbfgs.zero_grad()
            loss = loss_fn()
            loss.backward()
            return loss

        loss = lbfgs.step(closure)
        final_loss = float(loss.detach().cpu())
        n_iter += lbfgs_steps
        opt_used = "adam_lbfgs" if warmup > 0 else "lbfgs"
    elif optimizer_name == "adam":
        adam = torch.optim.Adam([x], lr=lr)
        for _ in range(iterations):
            adam.zero_grad()
            loss = loss_fn()
            loss.backward()
            adam.step()
        final_loss = float(loss_fn().detach().cpu())
        n_iter = iterations
        opt_used = "adam"
    else:
        raise ValueError("deepxde_optimizer must be 'adam' or 'lbfgs'")

    return x.detach().cpu().numpy(), final_loss, n_iter, opt_used


def _initial_guess(
    G: np.ndarray,
    y: np.ndarray,
    config: InversionConfig,
    warnings: list[str],
) -> np.ndarray:
    """Build the initial vector for DeepXDE optimisation."""
    init = str(getattr(config, "deepxde_init", "zeros")).lower()
    N = G.shape[1]

    if init == "zeros":
        return np.zeros(N)
    if init == "lstsq":
        try:
            x0, *_ = np.linalg.lstsq(G, y, rcond=None)
            return np.asarray(x0, dtype=float)
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"lstsq initialisation failed: {exc}; using zeros")
            return np.zeros(N)

    warnings.append(f"Unknown deepxde_init={init!r}; using zeros")
    return np.zeros(N)


def _condition_estimate(
    G: np.ndarray,
    L: np.ndarray,
    lam: float,
    warnings: list[str],
) -> float:
    """Estimate cond(G^T G + lambda L^T L), matching Tikhonov diagnostics."""
    try:
        A = G.T @ G + lam * (L.T @ L)
        eigvals = np.linalg.eigvalsh(A)
        eigvals_abs = np.abs(eigvals)
        return float(eigvals_abs.max() / (eigvals_abs.min() + 1e-300))
    except np.linalg.LinAlgError:
        warnings.append("Eigenvalue computation failed; condition estimate unavailable")
        return float("inf")
