"""
planner.py
==========
Rule-based initial inversion planner.

The planner inspects the ProblemSpec and produces an InversionConfig
that represents a reasonable first attempt.  All decisions are explicit
and logged so the research trace is auditable.

Planning rules (deterministic)
-------------------------------
1. Parameterisation:
   - Always use piecewise_constant for Version 1.
   - num_parameters = round(N_t / 5), clamped to [5, 50].

2. Regularisation order:
   - Default: reg_order = 1  (promotes smoothness in q'(t))

3. Lambda strategy:
   - If noise_std is available  → discrepancy principle
   - Else                       → L-curve

4. Physical bounds:
   - Use caller-provided bounds from the YAML config if present.
   - Otherwise: None (no clamping).

5. Max retries and budget: configurable via the YAML, with sensible
   defaults.

Extension note
--------------
A future version could use a local LLM to suggest initial
configurations based on domain descriptions.  The planner interface
remains unchanged; the LLM would be an optional advice source.
"""

from __future__ import annotations

from src.logging_utils import get_logger, log_decision
from src.types import InversionConfig, ProblemSpec

log = get_logger("planner")

# --- Tuneable constants ---------------------------------------------------
_DEFAULT_MAX_RETRIES = 6
_DEFAULT_ITERATION_BUDGET = 10
_DEFAULT_STOP_TOLERANCE = 1e-3
_PARAM_DIVISOR = 5          # num_parameters ≈ N_t / _PARAM_DIVISOR
_PARAM_MIN = 5
_PARAM_MAX = 50


def make_initial_plan(
    problem: ProblemSpec,
    overrides: dict | None = None,
) -> InversionConfig:
    """Produce the initial InversionConfig from the ProblemSpec.

    Parameters
    ----------
    problem   : parsed problem specification
    overrides : optional dict that may supply "physical_bounds",
                "max_retries", "iteration_budget", "reg_order", etc.

    Returns
    -------
    InversionConfig
    """
    overrides = overrides or {}
    notes: list[str] = []

    # --- 1. Parameterisation ---
    n_params = _choose_num_params(problem.n_time, notes)

    # --- 2. Regularisation order ---
    reg_order: int = int(overrides.get("reg_order", 1))
    notes.append(f"reg_order={reg_order} (default first-difference smoothness)")

    # --- 3. Lambda strategy ---
    if problem.noise_std is not None:
        lambda_strategy = "discrepancy"
        notes.append("noise_std provided → using discrepancy principle for lambda")
    else:
        lambda_strategy = "lcurve"
        notes.append("noise_std not available → using L-curve for lambda")

    # Allow explicit override from config
    if "lambda_strategy" in overrides:
        lambda_strategy = overrides["lambda_strategy"]
        notes.append(f"lambda_strategy overridden to '{lambda_strategy}' from config")

    # --- 4. Fixed lambda or grid ---
    lambda_value: float | None = overrides.get("lambda_value")
    lambda_grid: list[float] | None = overrides.get("lambda_grid")
    if lambda_value is not None:
        lambda_strategy = "fixed"
        notes.append(f"lambda_value={lambda_value} supplied → strategy forced to 'fixed'")

    # --- 5. Physical bounds ---
    physical_bounds: tuple[float, float] | None = None
    if "physical_bounds" in overrides:
        pb = overrides["physical_bounds"]
        if pb is not None:
            physical_bounds = (float(pb[0]), float(pb[1]))
            notes.append(f"physical_bounds={physical_bounds} applied")

    # --- 6. Budget / tolerance ---
    max_retries = int(overrides.get("max_retries", _DEFAULT_MAX_RETRIES))
    iteration_budget = int(overrides.get("iteration_budget", _DEFAULT_ITERATION_BUDGET))
    stop_tolerance = float(overrides.get("stop_tolerance", _DEFAULT_STOP_TOLERANCE))

    # --- 7. Verifier bypass (ablation) ---
    skip_verifier = bool(overrides.get("skip_verifier", False))

    # --- 8. Solver selection ---
    solver_name = str(overrides.get("solver_name", "tikhonov"))
    if solver_name != "tikhonov":
        notes.append(f"solver_name='{solver_name}' from config overrides")

    # TSVD guard: the L-curve / discrepancy strategies select lambda values
    # in the range 1e-12 – 1e-6 that are designed for Tikhonov normal
    # equations.  TSVD interprets lambda as a truncation *threshold fraction*,
    # so a Tikhonov-optimal value of 1e-9 would keep 99.9999 % of singular
    # values — essentially no regularization.  Force a sensible default.
    if solver_name == "tsvd" and lambda_value is None and "lambda_strategy" not in overrides:
        lambda_strategy = "fixed"
        lambda_value = 0.01   # keep singular values ≥ 1 % of s_max
        notes.append(
            "solver_name='tsvd' with no explicit lambda: "
            "lambda_strategy forced to 'fixed', lambda_value=0.01 "
            "(truncation threshold; override via planner.lambda_value)"
        )

    config = InversionConfig(
        parameterization_type="piecewise_constant",
        num_parameters=n_params,
        reg_order=reg_order,  # type: ignore[arg-type]
        lambda_strategy=lambda_strategy,  # type: ignore[arg-type]
        lambda_value=lambda_value,
        lambda_grid=lambda_grid,
        max_retries=max_retries,
        physical_bounds=physical_bounds,
        planner_notes=notes,
        stop_tolerance=stop_tolerance,
        iteration_budget=iteration_budget,
        skip_verifier=skip_verifier,
        solver_name=solver_name,
    )

    log_decision(log, "PLANNER", {
        "n_params": n_params,
        "reg_order": reg_order,
        "lambda_strategy": lambda_strategy,
        "physical_bounds": physical_bounds,
        "solver_name": solver_name,
    })
    return config


def _choose_num_params(n_time: int, notes: list[str]) -> int:
    """Select a number of inversion parameters proportional to time grid length."""
    raw = max(_PARAM_MIN, n_time // _PARAM_DIVISOR)
    clamped = min(raw, _PARAM_MAX)
    if clamped != raw:
        notes.append(f"num_parameters clamped from {raw} to {clamped} (max={_PARAM_MAX})")
    else:
        notes.append(f"num_parameters={clamped} (≈ N_t/{_PARAM_DIVISOR})")
    return clamped
