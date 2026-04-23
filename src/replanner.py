"""
replanner.py
============
Rule-based replanner: revises InversionConfig based on VerificationResult.

Design rationale
----------------
The replanner is the failure-recovery backbone of the agent loop.
It translates verifier diagnostics into concrete config modifications,
creating a tight feedback loop:

    solve → verify → replan → solve → …

Rules are deterministic and explicit.  Each rule is a named function
that returns an ``(action_label, updated_config)`` pair.  The first
applicable rule fires; the rest are skipped.  This makes the decision
process auditable in the agent trace.

Supported actions
-----------------
  increase_lambda          : multiply lambda by a step factor
  decrease_lambda          : divide lambda by a step factor
  switch_reg_order_to_0    : change to zero-order regularisation
  switch_reg_order_to_1    : change to first-order regularisation
  switch_reg_order_to_2    : change to second-order regularisation
  reduce_parameter_dimension   : halve num_parameters
  increase_parameter_dimension : double num_parameters
  inspect_data_quality     : soft warning, no config change
  stop_with_manual_review  : abort loop, escalate to human
  stop_with_failure        : abort loop, record failure

Lambda adjustment factor
------------------------
The lambda stepping is multiplicative (factor = 5.0 by default).
This means a series of increases / decreases traces through orders
of magnitude quickly.
"""

from __future__ import annotations

import copy

from src.logging_utils import get_logger, log_decision
from src.types import InversionConfig, VerificationResult

log = get_logger("replanner")

_LAMBDA_STEP = 5.0          # multiplicative step for lambda adjustment
_LAMBDA_MIN = 1e-12         # safety floor
_LAMBDA_MAX = 1e10          # safety ceiling

# Actions that terminate the loop
_TERMINAL_ACTIONS = {"stop_with_manual_review", "stop_with_failure"}


def replan(
    config: InversionConfig,
    verification: VerificationResult,
    iteration: int,
) -> tuple[str, InversionConfig]:
    """Produce the next InversionConfig based on the verification result.

    Parameters
    ----------
    config       : current inversion config
    verification : result from verifier
    iteration    : current iteration number (0-indexed)

    Returns
    -------
    (action_label, new_config)
        action_label : string describing what was done
        new_config   : revised config (or unchanged copy for terminal actions)
    """
    new = copy.deepcopy(config)
    decision = verification.decision
    tradeoff = verification.tradeoff_label
    suggested = verification.suggested_actions

    # --- Terminal conditions ---
    if decision == "pass":
        action = "stop_success"
        return action, new

    if decision == "manual_review":
        action = "stop_with_manual_review"
        log_decision(log, "REPLANNER", {"action": action, "iter": iteration})
        return action, new

    # --- Retry budget check ---
    if iteration >= config.max_retries:
        action = "stop_with_failure"
        new.planner_notes.append(f"Max retries ({config.max_retries}) reached")
        log_decision(log, "REPLANNER", {"action": action, "iter": iteration})
        return action, new

    # --- Under-regularisation ---
    # Only act on under-regularisation if oscillation is actually significant.
    # Thresholds match VerifierThresholds.osc_* (normalized second-diff energy).
    osc_significant = verification.oscillation_score > 1.0
    if (tradeoff == "under_regularized" or verification.oscillation_score > 4.0) and osc_significant:
        if config.reg_order < 2:
            # Prefer higher-order regularisation for oscillatory solutions
            new_order = config.reg_order + 1
            action = f"switch_reg_order_to_{new_order}"
            new.reg_order = new_order  # type: ignore[assignment]
            new.planner_notes.append(
                f"iter{iteration}: oscillatory solution → increase reg_order to {new_order}"
            )
        else:
            # Already at max order; just increase lambda
            action = "increase_lambda"
            new = _adjust_lambda(new, factor=_LAMBDA_STEP, direction="increase", iter_=iteration)
        log_decision(log, "REPLANNER", {"action": action, "osc": verification.oscillation_score})
        return action, new

    # --- Over-regularisation ---
    if tradeoff == "over_regularized":
        # If already at order 0, just decrease lambda
        action = "decrease_lambda"
        new = _adjust_lambda(new, factor=_LAMBDA_STEP, direction="decrease", iter_=iteration)
        log_decision(log, "REPLANNER", {"action": action, "tradeoff": tradeoff})
        return action, new

    # --- Stability failure ---
    if verification.stability_ok is False:
        # Reduce dimension to stabilise
        if config.num_parameters > 5:
            action = "reduce_parameter_dimension"
            new.num_parameters = max(5, config.num_parameters // 2)
            new.planner_notes.append(
                f"iter{iteration}: stability failure → reduce n_params to {new.num_parameters}"
            )
        else:
            action = "stop_with_manual_review"
            new.planner_notes.append(f"iter{iteration}: stable reduction impossible; manual review")
        log_decision(log, "REPLANNER", {"action": action, "n_params": new.num_parameters})
        return action, new

    # --- Weak pass: try gentle lambda decrease to improve fit ---
    if decision == "weak_pass":
        # Only attempt if fit is clearly improvable
        if verification.relative_replay_error > 0.05:
            action = "decrease_lambda"
            new = _adjust_lambda(new, factor=2.0, direction="decrease", iter_=iteration)
        else:
            # Fit is borderline but acceptable; stop
            action = "stop_success_weak_pass"
        log_decision(log, "REPLANNER", {"action": action, "rel_err": verification.relative_replay_error})
        return action, new

    # --- Generic fail: try adjusting lambda based on residual ---
    if decision == "fail":
        if verification.replay_rmse > 5.0:
            # Large residual → try less regularisation
            action = "decrease_lambda"
            new = _adjust_lambda(new, factor=_LAMBDA_STEP, direction="decrease", iter_=iteration)
        else:
            # Moderate residual → try more regularisation
            action = "increase_lambda"
            new = _adjust_lambda(new, factor=_LAMBDA_STEP, direction="increase", iter_=iteration)
        log_decision(log, "REPLANNER", {"action": action, "rmse": verification.replay_rmse})
        return action, new

    # Fallback (should not be reached)
    log.warning("Replanner reached fallback; stopping with manual review")
    return "stop_with_manual_review", new


def is_terminal(action: str) -> bool:
    """Return True if *action* should terminate the agent loop."""
    return action in _TERMINAL_ACTIONS or action.startswith("stop_")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _adjust_lambda(
    config: InversionConfig,
    factor: float,
    direction: str,
    iter_: int,
) -> InversionConfig:
    """Return *config* with lambda_value adjusted.

    If lambda_value is None (i.e., strategy is not 'fixed'), switch to
    'fixed' mode with an initial estimate and then adjust.  The initial
    estimate is a coarse heuristic (1.0) which will be refined in
    subsequent iterations.

    The strategy is forced to "fixed" once we start manually adjusting
    lambda so that subsequent solves use exactly the adjusted value.
    """
    current = config.lambda_value if config.lambda_value is not None else 1.0

    if direction == "increase":
        new_lam = min(current * factor, _LAMBDA_MAX)
    else:
        new_lam = max(current / factor, _LAMBDA_MIN)

    config.lambda_value = new_lam
    config.lambda_strategy = "fixed"  # type: ignore[assignment]
    config.planner_notes.append(
        f"iter{iter_}: lambda {direction}d to {new_lam:.3e} (factor={factor})"
    )
    return config
