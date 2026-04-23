"""
test_replanner.py
Tests for the rule-based replanner.
"""

import numpy as np
import pytest
from src.replanner import replan, is_terminal
from src.types import (
    InversionConfig, SolverDiagnostics, SolverResult, VerificationResult,
)


def _make_config(**kwargs) -> InversionConfig:
    defaults = dict(
        parameterization_type="piecewise_constant",
        num_parameters=20,
        reg_order=1,
        lambda_strategy="fixed",
        lambda_value=1.0,
        max_retries=6,
        iteration_budget=10,
    )
    defaults.update(kwargs)
    return InversionConfig(**defaults)


def _make_verification(
    decision="fail",
    tradeoff="well_regularized",
    osc=0.1,
    rmse=3.0,
    rel_err=0.1,
    phys_ok=True,
    stab_ok=None,
    suggested=None,
) -> VerificationResult:
    return VerificationResult(
        decision=decision,
        replay_rmse=rmse,
        relative_replay_error=rel_err,
        roughness_l1=1.0,
        roughness_l2=0.5,
        oscillation_score=osc,
        physical_ok=phys_ok,
        discrepancy_ok=None,
        stability_ok=stab_ok,
        tradeoff_label=tradeoff,
        reasons=[],
        suggested_actions=suggested or [],
        metrics={},
    )


def test_pass_returns_stop_success():
    config = _make_config()
    vr = _make_verification(decision="pass")
    action, _ = replan(config, vr, iteration=0)
    assert action == "stop_success"
    assert is_terminal(action)


def test_manual_review_returns_stop_manual_review():
    config = _make_config()
    vr = _make_verification(decision="manual_review")
    action, _ = replan(config, vr, iteration=0)
    assert action == "stop_with_manual_review"
    assert is_terminal(action)


def test_max_retries_triggers_stop():
    config = _make_config(max_retries=3)
    vr = _make_verification(decision="fail")
    action, _ = replan(config, vr, iteration=3)  # iteration == max_retries
    assert action == "stop_with_failure"


def test_under_regularized_increases_reg_order():
    config = _make_config(reg_order=1)
    vr = _make_verification(decision="fail", tradeoff="under_regularized", osc=0.5)
    action, new_config = replan(config, vr, iteration=0)
    assert action == "switch_reg_order_to_2"
    assert new_config.reg_order == 2


def test_under_regularized_at_max_order_increases_lambda():
    config = _make_config(reg_order=2, lambda_value=1.0)
    vr = _make_verification(decision="fail", tradeoff="under_regularized", osc=0.5)
    action, new_config = replan(config, vr, iteration=0)
    assert action == "increase_lambda"
    assert new_config.lambda_value > 1.0


def test_over_regularized_decreases_lambda():
    config = _make_config(lambda_value=10.0)
    vr = _make_verification(decision="fail", tradeoff="over_regularized")
    action, new_config = replan(config, vr, iteration=0)
    assert action == "decrease_lambda"
    assert new_config.lambda_value < 10.0


def test_stability_failure_reduces_dimension():
    config = _make_config(num_parameters=20)
    vr = _make_verification(decision="fail", stab_ok=False)
    action, new_config = replan(config, vr, iteration=0)
    assert action == "reduce_parameter_dimension"
    assert new_config.num_parameters < 20


def test_lambda_clamped_to_max():
    config = _make_config(lambda_value=1e9)
    vr = _make_verification(tradeoff="under_regularized", osc=0.9, decision="fail")
    config.reg_order = 2  # already at max
    _, new_config = replan(config, vr, iteration=0)
    assert new_config.lambda_value <= 1e10


def test_lambda_clamped_to_min():
    config = _make_config(lambda_value=1e-11)
    vr = _make_verification(tradeoff="over_regularized", decision="fail")
    _, new_config = replan(config, vr, iteration=0)
    assert new_config.lambda_value >= 1e-12
