"""
reporter.py
===========
Structured reporting: JSON summary + Markdown report + iteration trace.

Outputs
-------
  outputs/<run_id>/summary.json     machine-readable run summary
  outputs/<run_id>/report.md        human-readable markdown report
  outputs/<run_id>/trace.json       iteration-by-iteration decision trace

The reporter is intentionally separated from the agent so that report
format can be changed (or extended with plots) without touching the
scientific core.

Optional LLM hook
-----------------
If a ReportWriterLLM adapter is supplied, it is called to generate the
narrative sections of the markdown report.  The structured data is
always written first so the report is still useful without an LLM.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any

from src.logging_utils import get_logger
from src.sensitivity import params_to_flux
from src.types import ProblemSpec, RunSummary
from src.utils import dataclass_to_dict, write_json

log = get_logger("reporter")


class Reporter:
    """Writes all output artefacts for a completed agent run."""

    def __init__(self, output_dir: Path, llm_writer: Any | None = None) -> None:
        self.output_dir = Path(output_dir)
        self.llm_writer = llm_writer

    def write(self, summary: RunSummary, problem: ProblemSpec) -> dict[str, str]:
        """Write all reports and return a dict of ``{label: path}``."""
        run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = self.output_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        paths: dict[str, str] = {}

        # 1. JSON summary
        json_path = run_dir / "summary.json"
        self._write_json_summary(summary, json_path)
        paths["json_summary"] = str(json_path)

        # 2. Trace JSON
        trace_path = run_dir / "trace.json"
        self._write_trace(summary, trace_path)
        paths["trace_json"] = str(trace_path)

        # 3. Markdown report
        md_path = run_dir / "report.md"
        self._write_markdown(summary, problem, md_path)
        paths["markdown_report"] = str(md_path)

        log.info("Reports written to: %s", run_dir)
        return paths

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    def _write_json_summary(self, summary: RunSummary, path: Path) -> None:
        data = {
            "final_status": summary.final_status,
            "solver_name": summary.final_config.solver_name,
            "final_lambda": summary.final_result.lambda_used,
            "final_reg_order": summary.final_result.reg_order,
            "final_residual_norm": summary.final_result.residual_norm,
            "final_reg_norm": summary.final_result.regularization_norm,
            "n_iterations": len(summary.traces),
            "summary_notes": summary.summary_notes,
            "final_config": dataclass_to_dict(summary.final_config),
            "final_result": {
                "estimated_x": summary.final_result.estimated_x,
                "fitted_y": summary.final_result.fitted_y,
                "status": summary.final_result.status,
            },
        }
        write_json(path, data)

    def _write_trace(self, summary: RunSummary, path: Path) -> None:
        trace_list = []
        for t in summary.traces:
            trace_list.append({
                "iteration": t.iteration,
                "lambda_used": t.solver_result.lambda_used,
                "reg_order": t.solver_result.reg_order,
                "residual_norm": t.solver_result.residual_norm,
                "solver_status": t.solver_result.status,
                "verification_decision": t.verification.decision,
                "replay_rmse": t.verification.replay_rmse,
                "tradeoff": t.verification.tradeoff_label,
                "replanning_action": t.replanning_action,
                "reasons": t.verification.reasons,
                "suggested": t.verification.suggested_actions,
                "notes": t.notes,
            })
        write_json(path, trace_list)

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    def _write_markdown(
        self, summary: RunSummary, problem: ProblemSpec, path: Path
    ) -> None:
        lines: list[str] = []

        lines += [
            "# IHCP Inversion Report",
            "",
            f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
            f"**Status:** `{summary.final_status}`  ",
            f"**Iterations:** {len(summary.traces)}  ",
            "",
        ]

        # Problem summary
        lines += [
            "## Problem Summary",
            "",
            f"- Type: `{problem.problem_type}`",
            f"- Inversion target: `{problem.target_name}`",
            f"- Time horizon: {problem.time_grid[-1]:.2f} s "
            f"({problem.n_time} steps, dt={problem.dt:.4f} s)",
            f"- Sensors: {problem.n_sensors} at positions {problem.sensor_positions} m",
            f"- Geometry: L={problem.geometry.length} m, "
            f"{problem.geometry.n_cells} cells",
            f"- Material: k={problem.material.conductivity} W/(m·K), "
            f"rho={problem.material.density} kg/m³",
            f"- Noise std: {problem.noise_std if problem.noise_std else 'not provided'}",
            "",
        ]

        # Final configuration
        cfg = summary.final_config
        lines += [
            "## Final Inversion Configuration",
            "",
            f"- Solver: `{cfg.solver_name}`",
            f"- Parameterisation: `{cfg.parameterization_type}` "
            f"({cfg.num_parameters} parameters)",
            f"- Regularisation order: {cfg.reg_order}",
            f"- Lambda: `{summary.final_result.lambda_used:.4e}`",
            f"- Lambda strategy: `{cfg.lambda_strategy}`",
            f"- Physical bounds: {cfg.physical_bounds}",
            "",
        ]

        # Solver results
        res = summary.final_result
        lines += [
            "## Solver Results",
            "",
            f"- Status: `{res.status}`",
            f"- Residual norm: `{res.residual_norm:.6f}`",
            f"- Regularisation norm: `{res.regularization_norm:.6f}`",
            f"- Objective value: `{res.objective_value:.6f}`",
            "",
            "### Estimated Parameters",
            "",
            "```",
        ]
        for j, v in enumerate(res.estimated_x):
            lines.append(f"  x[{j:3d}] = {v:+.4f}")
        lines += ["```", ""]

        # Iteration trace
        lines += ["## Iteration Trace", ""]
        for t in summary.traces:
            v = t.verification
            lines.append(
                f"**Iter {t.iteration}** | λ={t.solver_result.lambda_used:.3e} | "
                f"RMSE={v.replay_rmse:.4f} | {v.tradeoff_label} | "
                f"→ {t.replanning_action}"
            )
            for r in v.reasons:
                lines.append(f"  - {r}")
            lines.append("")

        # Warnings
        all_warnings: list[str] = []
        for t in summary.traces:
            if t.solver_result.diagnostics:
                all_warnings.extend(t.solver_result.diagnostics.warnings)
        if all_warnings:
            lines += ["## Warnings", ""]
            for w in set(all_warnings):
                lines.append(f"- {w}")
            lines.append("")

        # Summary notes
        if summary.summary_notes:
            lines += ["## Notes", ""]
            for note in summary.summary_notes:
                lines.append(f"- {note}")
            lines.append("")

        # Optional LLM narrative
        if self.llm_writer is not None:
            try:
                narrative = self.llm_writer.write_report_narrative(summary, problem)
                lines += ["## AI-Assisted Narrative", "", narrative, ""]
            except Exception as exc:  # noqa: BLE001
                lines += [f"<!-- LLM report generation failed: {exc} -->", ""]

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
        log.info("Markdown report written: %s", path)
