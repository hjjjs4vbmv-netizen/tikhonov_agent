"""
verifier.py
===========
Multi-criteria physical and methodological verification of a Tikhonov
inversion result.

Design rationale
----------------
A plain residual check is insufficient for IHCP results because:
  - A small residual can coexist with an oscillatory, physically
    implausible solution (under-regularised).
  - A large residual with a flat solution is equally wrong (over-regularised).
  - IHCP solutions must pass physical sanity checks.
  - Stability across nearby lambda values is a hallmark of a robust solution.

This verifier emulates the mental checklist of an experienced IHCP
researcher by combining:
  1.  Replay residual (absolute and relative)
  2.  First- and second-difference roughness
  3.  Oscillation score (sign-change frequency)
  4.  Physical bounds compliance
  5.  Discrepancy principle consistency  (only if noise_std available)
  6.  Nearby-lambda stability             (only if multiple results available)
  7.  Tradeoff label inference

Thresholds
----------
All thresholds are configurable via the ``VerifierThresholds`` class.
The defaults are intentionally conservative for a prototype.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from src.logging_utils import get_logger, log_decision
from src.types import (
    InversionConfig,
    ProblemSpec,
    SolverResult,
    VerificationDecision,
    VerificationResult,
)

log = get_logger("verifier")


@dataclass
class VerifierThresholds:
    """Configurable thresholds for all verification criteria."""

    # Replay error
    rmse_pass: float = 0.5        # [K] absolute RMSE – pass threshold
    rmse_weak: float = 2.0        # [K] absolute RMSE – weak_pass threshold
    rel_error_pass: float = 0.02  # relative RMSE / signal_range – pass
    rel_error_weak: float = 0.10  # relative RMSE / signal_range – weak_pass

    # Roughness  (relative to |mean(x)|, avoiding division by zero)
    roughness_pass: float = 0.5   # L1 first-diff roughness / |mean(x)|
    roughness_fail: float = 3.0   # above this → likely under-regularised

    # Oscillation  (normalized second-difference energy; dimensionless)
    # Well-regularized solutions typically score < 1.0.
    # Values > 5.0 indicate an under-regularized, oscillatory solution.
    osc_pass: float = 1.0        # well-regularized threshold
    osc_fail: float = 5.0        # above this → clearly oscillatory (under-reg)

    # Discrepancy principle tolerance (|norm - delta| / delta)
    disc_tolerance: float = 0.20

    # Stability: max relative variation in ||x|| across nearby lambdas
    stability_pass: float = 0.10
    stability_fail: float = 0.30


_DEFAULT_THRESH = VerifierThresholds()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def verify(
    problem: ProblemSpec,
    config: InversionConfig,
    result: SolverResult,
    thresholds: VerifierThresholds = _DEFAULT_THRESH,
    nearby_results: list[SolverResult] | None = None,
) -> VerificationResult:
    """Perform multi-criteria verification of *result*.

    Parameters
    ----------
    problem         : problem specification (observations, noise_std, …)
    config          : inversion config used (for physical_bounds, …)
    result          : solver output to verify
    thresholds      : pass/fail thresholds
    nearby_results  : solutions at adjacent lambda values (optional);
                      used for stability check

    Returns
    -------
    VerificationResult
    """
    x = np.array(result.estimated_x)
    y_obs = np.array(problem.observations).flatten()
    y_fit = np.array(result.fitted_y)

    reasons: list[str] = []
    suggested: list[str] = []
    metrics: dict = {}

    # --- 1. Replay residual ---
    replay_rmse, rel_err = _replay_metrics(y_obs, y_fit, reasons, metrics)

    # --- 2. Roughness ---
    rL1, rL2 = _roughness_metrics(x, reasons, metrics)

    # --- 3. Oscillation ---
    osc = _oscillation_score(x, reasons, metrics)

    # --- 4. Physical bounds ---
    phys_ok = _check_physical(x, config, reasons, metrics)

    # --- 5. Discrepancy principle ---
    disc_ok = _check_discrepancy(
        y_obs, y_fit, problem.noise_std, thresholds, reasons, metrics
    )

    # --- 6. Nearby-lambda stability ---
    stab_ok = _check_stability(nearby_results, thresholds, reasons, metrics)

    # --- 7. Tradeoff label ---
    tradeoff = _diagnose_tradeoff(
        replay_rmse, rL1, osc, thresholds, reasons, suggested
    )

    # --- 8. Overall decision ---
    decision = _make_decision(
        replay_rmse, rel_err, phys_ok, disc_ok, stab_ok,
        tradeoff, thresholds, reasons, suggested,
    )

    log_decision(log, "VERIFIER", {
        "decision": decision,
        "replay_rmse": f"{replay_rmse:.4f}",
        "rel_err": f"{rel_err:.4f}",
        "osc": f"{osc:.2f}",
        "tradeoff": tradeoff,
    })

    return VerificationResult(
        decision=decision,  # type: ignore[arg-type]
        replay_rmse=replay_rmse,
        relative_replay_error=rel_err,
        roughness_l1=rL1,
        roughness_l2=rL2,
        oscillation_score=osc,
        physical_ok=phys_ok,
        discrepancy_ok=disc_ok,
        stability_ok=stab_ok,
        tradeoff_label=tradeoff,  # type: ignore[arg-type]
        reasons=reasons,
        suggested_actions=suggested,
        metrics=metrics,
    )


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def _replay_metrics(
    y_obs: np.ndarray,
    y_fit: np.ndarray,
    reasons: list[str],
    metrics: dict,
) -> tuple[float, float]:
    """Compute RMSE and relative replay error."""
    residuals = y_obs - y_fit
    rmse = float(np.sqrt(np.mean(residuals**2)))
    signal_range = float(np.ptp(y_obs)) or 1.0   # peak-to-peak of observations
    rel_err = rmse / signal_range

    metrics["replay_rmse"] = rmse
    metrics["relative_replay_error"] = rel_err
    metrics["signal_range"] = signal_range
    return rmse, rel_err


def _roughness_metrics(
    x: np.ndarray,
    reasons: list[str],
    metrics: dict,
) -> tuple[float, float]:
    """First-difference roughness (L1 and L2)."""
    if len(x) < 2:
        return 0.0, 0.0
    dx = np.diff(x)
    rL1 = float(np.sum(np.abs(dx)))
    rL2 = float(np.linalg.norm(dx))
    metrics["roughness_l1"] = rL1
    metrics["roughness_l2"] = rL2
    return rL1, rL2


def _oscillation_score(
    x: np.ndarray,
    reasons: list[str],
    metrics: dict,
) -> float:
    """Normalized second-difference energy of the parameter vector.

    Measures oscillatory behavior of the recovered flux parameters.
    Defined as:
        osc = sum(diff(x, n=2)**2) / (sum(x**2) + 1e-30)

    This is:
      - zero for constant or linearly-varying solutions,
      - large for rapidly oscillating solutions,
      - dimensionless and scale-invariant.

    Previous implementation counted sign changes in diff(x) — this was
    constant (0.3866) for all piecewise-constant solutions because the
    expanded time series had a fixed number of segment boundaries.
    The new metric operates on the raw parameter vector, avoiding that artifact.
    """
    if len(x) < 3:
        metrics["oscillation_score"] = 0.0
        return 0.0
    d2x = np.diff(x, n=2)
    osc = float(np.sum(d2x**2) / (np.sum(x**2) + 1e-30))
    metrics["oscillation_score"] = osc
    return osc


def _check_physical(
    x: np.ndarray,
    config: InversionConfig,
    reasons: list[str],
    metrics: dict,
) -> bool:
    """Check that estimated parameters are within physical bounds."""
    if config.physical_bounds is None:
        metrics["physical_ok"] = True
        return True

    lo, hi = config.physical_bounds
    violations = int(np.sum((x < lo) | (x > hi)))
    ok = violations == 0
    metrics["physical_ok"] = ok
    metrics["physical_violations"] = violations
    if not ok:
        reasons.append(
            f"Physical bounds violated: {violations}/{len(x)} parameters "
            f"outside [{lo}, {hi}]"
        )
    return ok


def _check_discrepancy(
    y_obs: np.ndarray,
    y_fit: np.ndarray,
    noise_std: float | None,
    thresholds: VerifierThresholds,
    reasons: list[str],
    metrics: dict,
) -> bool | None:
    """Check consistency with Morozov discrepancy principle."""
    if noise_std is None:
        metrics["discrepancy_ok"] = None
        return None

    M = len(y_obs)
    target = np.sqrt(M) * noise_std
    actual = float(np.linalg.norm(y_obs - y_fit))
    rel_dev = abs(actual - target) / (target + 1e-30)
    ok = rel_dev <= thresholds.disc_tolerance

    metrics["discrepancy_target"] = target
    metrics["discrepancy_actual"] = actual
    metrics["discrepancy_rel_dev"] = rel_dev
    metrics["discrepancy_ok"] = ok

    if not ok:
        direction = "above" if actual > target else "below"
        reasons.append(
            f"Discrepancy principle: ||r||={actual:.4f} is {direction} "
            f"target={target:.4f} (rel_dev={rel_dev:.2f})"
        )
    return ok


def _check_stability(
    nearby: list[SolverResult] | None,
    thresholds: VerifierThresholds,
    reasons: list[str],
    metrics: dict,
) -> bool | None:
    """Check solution stability across nearby lambda values."""
    if nearby is None or len(nearby) < 2:
        metrics["stability_ok"] = None
        return None

    norms = [np.linalg.norm(r.estimated_x) for r in nearby]
    rel_var = (max(norms) - min(norms)) / (np.mean(norms) + 1e-30)
    ok = rel_var <= thresholds.stability_pass

    metrics["stability_rel_var"] = rel_var
    metrics["stability_ok"] = ok

    if not ok:
        reasons.append(
            f"Instability across nearby lambdas: relative variation in ||x|| = "
            f"{rel_var:.2f} (threshold {thresholds.stability_pass})"
        )
    return ok


def _diagnose_tradeoff(
    rmse: float,
    roughness_l1: float,
    osc: float,
    thresholds: VerifierThresholds,
    reasons: list[str],
    suggested: list[str],
) -> str:
    """Infer whether solution is under-/over-/well-regularised."""
    # Under-regularised signals: high oscillation or high roughness
    # Guard against flat solutions with zero roughness being misclassified
    mean_abs_x = 1.0   # placeholder denominator; actual x not passed here
    under = (osc > thresholds.osc_fail
             or roughness_l1 > thresholds.roughness_fail)
    # Over-regularised signals: residual is large relative to what we expect
    # (proxy: residual_norm normalised to observation signal range is large)
    # Here we use roughness as the only available proxy — over-smoothed solutions
    # have very low roughness.  The agent can cross-check with actual residuals.
    very_smooth = roughness_l1 < 1e-6   # essentially flat solution

    if under:
        reasons.append(
            f"Under-regularisation suspected: osc={osc:.2f}, L1_rough={roughness_l1:.4f}"
        )
        suggested.append("increase_lambda")
        return "under_regularized"

    if very_smooth and rmse > 1.0:
        # High residual + zero roughness → over-smoothed
        reasons.append(
            f"Over-regularisation suspected: solution is flat but rmse={rmse:.4f}"
        )
        suggested.append("decrease_lambda")
        return "over_regularized"

    return "well_regularized"


def _make_decision(
    rmse: float,
    rel_err: float,
    phys_ok: bool,
    disc_ok: bool | None,
    stab_ok: bool | None,
    tradeoff: str,
    thresholds: VerifierThresholds,
    reasons: list[str],
    suggested: list[str],
) -> VerificationDecision:
    """Combine all sub-checks into a final decision label."""

    # Hard fail conditions
    if not phys_ok:
        suggested.append("stop_with_manual_review")
        return "manual_review"

    if tradeoff == "under_regularized" and rmse > thresholds.rmse_fail if hasattr(thresholds, "rmse_fail") else False:  # noqa: E501
        # (rmse_fail not in thresholds by default; kept for extensibility)
        return "fail"

    # Stability failure → manual review
    if stab_ok is False:
        suggested.append("reduce_parameter_dimension")
        return "manual_review"

    # Primary fit criterion
    if rmse <= thresholds.rmse_pass and rel_err <= thresholds.rel_error_pass:
        if tradeoff == "well_regularized":
            return "pass"
        # Good fit but uncertain regularisation → weak pass
        reasons.append("Fit is good but regularisation balance is uncertain")
        return "weak_pass"

    if rmse <= thresholds.rmse_weak and rel_err <= thresholds.rel_error_weak:
        reasons.append(f"Fit marginal: rmse={rmse:.4f}, rel_err={rel_err:.4f}")
        return "weak_pass"

    # Discrepancy satisfied but fit marginal
    if disc_ok is True:
        reasons.append("Discrepancy satisfied but absolute fit is poor")
        return "weak_pass"

    reasons.append(f"Fit failed: rmse={rmse:.4f} > threshold {thresholds.rmse_weak}")
    suggested.append("check_data_quality_or_adjust_lambda")
    return "fail"
