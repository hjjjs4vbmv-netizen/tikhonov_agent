"""
agent.py
========
Main orchestration loop: Parser → Planner → Solver → Verifier → Replanner.

This module assembles all scientific components into a coherent
agentic workflow.  The loop is intentionally explicit and inspectable:
every iteration is recorded in the AgentTrace list.

The agent is NOT an LLM agent.  It is a deterministic, rule-based
scientific agent whose decisions are fully traceable and reproducible.

Stop conditions (explicit)
--------------------------
  PASS           : verifier decision == "pass"
  WEAK_PASS      : verifier decision == "weak_pass" + no further improvement
  MANUAL_REVIEW  : physical implausibility or stability failure
  FAIL           : max retries exceeded OR repeated failure
  HARD_FAIL      : solver breakdown, malformed input
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from src.forward_model import HeatConductionFD
from src.lambda_selector import select_lambda
from src.logging_utils import get_logger
from src.parser import parse_problem
from src.planner import make_initial_plan
from src.replanner import is_terminal, replan
from src.reporter import Reporter
from src.sensitivity import build_sensitivity_matrix
from src.solver_registry import get_registry
from src.types import (
    AgentTrace,
    InversionConfig,
    ProblemSpec,
    RunSummary,
    SolverResult,
)
from src.verifier import VerifierThresholds, verify

log = get_logger("agent")


class IHCPAgent:
    """Rule-based scientific agent for 1D transient IHCP.

    Usage
    -----
        agent = IHCPAgent(output_dir="outputs/run_001")
        summary = agent.run(config_path="configs/example_case.yaml")
    """

    def __init__(
        self,
        output_dir: str | Path = "outputs",
        thresholds: VerifierThresholds | None = None,
        llm_hooks: Any | None = None,
    ) -> None:
        self.output_dir = Path(output_dir)
        self.thresholds = thresholds or VerifierThresholds()
        self.llm_hooks = llm_hooks
        self.reporter = Reporter(self.output_dir)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(
        self,
        config_path: str | Path,
        observations_path: str | Path | None = None,
        planner_overrides: dict | None = None,
    ) -> RunSummary:
        """Run the full agent loop and return a RunSummary.

        Parameters
        ----------
        config_path        : path to YAML problem config
        observations_path  : path to CSV observations (overrides YAML path)
        planner_overrides  : dict of planner settings to override

        Returns
        -------
        RunSummary with all iteration traces and report paths
        """
        # --- 1. Parse ---
        log.info("=== IHCP Agent starting ===")
        log.info("Config: %s", config_path)

        llm_parser = getattr(self.llm_hooks, "parser", None) if self.llm_hooks else None
        problem = parse_problem(config_path, observations_path, llm_parser)

        # --- 2. Build forward model (shared across iterations) ---
        model = HeatConductionFD(
            geometry=problem.geometry,
            material=problem.material,
            bc=problem.boundary_conditions,
            time_grid=problem.time_grid,
        )
        sensor_indices = model.sensor_indices_from_positions(problem.sensor_positions)
        log.info("Sensor indices: %s", sensor_indices)

        # Prepare flattened observation vector (sensor-major)
        y_obs = np.array(problem.observations).flatten()

        # --- 3. Initial plan ---
        config = make_initial_plan(problem, planner_overrides)
        log.info("Initial plan: %s", config)

        # --- 4. Agent loop ---
        traces: list[AgentTrace] = []
        final_result: SolverResult | None = None
        final_status = "fail"

        for iteration in range(config.iteration_budget):
            log.info("--- Iteration %d ---", iteration)

            # --- 4a. Build G and y_0 ---
            try:
                G, y_0 = build_sensitivity_matrix(problem, config, model, sensor_indices)
                y = y_obs - y_0   # residualised observations
            except Exception as exc:  # noqa: BLE001
                log.error("Sensitivity matrix build failed: %s", exc)
                summary = self._make_failure_summary(
                    config, traces, f"Sensitivity build error: {exc}"
                )
                self.reporter.write(summary, problem)
                return summary

            # --- 4b. Lambda selection ---
            try:
                lam = self._select_lambda(config, G, y_0, y, problem)
                config.lambda_value = lam
                log.info("Lambda selected: %.4e", lam)
            except Exception as exc:  # noqa: BLE001
                log.error("Lambda selection failed: %s", exc)
                lam = 1.0
                config.lambda_value = lam

            # --- 4c. Solve ---
            try:
                solver_name = config.solver_name
                result = get_registry().solve_single(solver_name, G, y, config, lam)
            except Exception as exc:  # noqa: BLE001
                log.error("Solver failed: %s", exc)
                summary = self._make_failure_summary(
                    config, traces, f"Solver error: {exc}"
                )
                self.reporter.write(summary, problem)
                return summary

            # fitted_y from the solver is G@x in residual space (y_obs - y_0).
            # Translate back to absolute temperature space for the verifier
            # and reporter so that RMSE is computed against raw observations.
            result.fitted_y = (y_0 + np.array(result.fitted_y)).tolist()
            final_result = result

            # --- 4d. Verify ---
            if config.skip_verifier:
                # Ablation: bypass all verification checks.
                # Construct a minimal synthetic VerificationResult that the
                # replanner will treat as an unconditional "pass", causing the
                # loop to stop after a single iteration.
                from src.types import VerificationResult as _VR
                y_fit_arr = np.array(result.fitted_y)
                residuals = y_obs - y_fit_arr
                replay_rmse = float(np.sqrt(np.mean(residuals**2)))
                verification = _VR(
                    decision="pass",
                    replay_rmse=replay_rmse,
                    relative_replay_error=0.0,
                    roughness_l1=0.0,
                    roughness_l2=0.0,
                    oscillation_score=0.0,
                    physical_ok=True,
                    discrepancy_ok=None,
                    stability_ok=None,
                    tradeoff_label="well_regularized",
                    reasons=["skip_verifier=True: verification bypassed (ablation)"],
                    suggested_actions=[],
                    metrics={},
                )
            else:
                verification = verify(
                    problem, config, result,
                    thresholds=self.thresholds,
                )
            log.info(
                "Verification: %s | rmse=%.4f | tradeoff=%s",
                verification.decision, verification.replay_rmse, verification.tradeoff_label,
            )

            # --- 4e. Replan ---
            action, next_config = replan(config, verification, iteration)
            log.info("Replanner action: %s", action)

            # Record trace
            trace = AgentTrace(
                iteration=iteration,
                config=config,
                solver_result=result,
                verification=verification,
                replanning_action=action,
                notes=list(config.planner_notes),
            )
            traces.append(trace)

            # --- 4f. Stop check ---
            if is_terminal(action):
                if action.startswith("stop_success") or verification.decision in ("pass", "weak_pass"):
                    final_status = verification.decision
                elif action == "stop_with_manual_review":
                    final_status = "manual_review"
                else:
                    final_status = "fail"
                break

            config = next_config

        else:
            # Loop exhausted without terminal action
            log.warning("Iteration budget exhausted without terminal action")
            final_status = "fail"
            if final_result is None:
                return self._make_failure_summary(config, traces, "Iteration budget exhausted")

        # --- 5. Report ---
        assert final_result is not None  # guaranteed by the loop structure
        summary = RunSummary(
            final_status=final_status,  # type: ignore[arg-type]
            final_config=config,
            final_result=final_result,
            traces=traces,
            summary_notes=[f"Completed in {len(traces)} iteration(s)"],
        )
        report_paths = self.reporter.write(summary, problem)
        summary.report_paths = report_paths

        log.info("=== Run complete: status=%s ===", final_status)
        return summary

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _select_lambda(
        self,
        config: InversionConfig,
        G: np.ndarray,
        y_0: np.ndarray,
        y: np.ndarray,
        problem: ProblemSpec,
    ) -> float:
        """Dispatch to lambda_selector based on config strategy."""
        from src.lambda_selector import select_lambda as _sel

        return _sel(
            strategy=config.lambda_strategy,
            G=G,
            L=self._get_L(config, G.shape[1]),
            y=y,
            noise_std=problem.noise_std,
            lambda_value=config.lambda_value,
            lambda_grid=config.lambda_grid,
        )

    @staticmethod
    def _get_L(config: InversionConfig, N: int) -> np.ndarray:
        from src.regularization import build_regularization_matrix
        return build_regularization_matrix(N, config.reg_order)

    def _make_failure_summary(
        self,
        config: InversionConfig,
        traces: list[AgentTrace],
        reason: str,
    ) -> RunSummary:
        """Construct a failure RunSummary when no valid result is available."""
        from src.types import SolverDiagnostics

        dummy_result = SolverResult(
            estimated_x=[],
            fitted_y=[],
            residual_norm=float("inf"),
            regularization_norm=float("inf"),
            objective_value=float("inf"),
            lambda_used=0.0,
            reg_order=config.reg_order,
            status="failed",
            diagnostics=SolverDiagnostics(
                matrix_shape=(0, 0),
                condition_estimate=float("inf"),
                solve_method="none",
                warnings=[reason],
            ),
        )
        return RunSummary(
            final_status="fail",
            final_config=config,
            final_result=dummy_result,
            traces=traces,
            summary_notes=[reason],
        )
