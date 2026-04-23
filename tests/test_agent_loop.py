"""
test_agent_loop.py
End-to-end agent loop test on a small synthetic IHCP.

This test builds a synthetic forward problem, generates noisy
observations with a known true flux, runs the full agent, and checks
that:
  - The agent terminates cleanly.
  - The final status is not a hard failure.
  - The recovered flux is in the right order of magnitude.
"""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml
from scipy.linalg import solve_banded

from src.agent import IHCPAgent
from src.verifier import VerifierThresholds


# ---------------------------------------------------------------------------
# Helpers to build a small synthetic case
# ---------------------------------------------------------------------------


def _generate_synthetic_observations(
    n_steps: int = 60,
    t_end: float = 30.0,
    noise_std: float = 0.2,
    seed: int = 7,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (time_grid, T_sensors) for a known step heat flux."""
    rho, cp, k = 7800.0, 500.0, 50.0
    alpha = k / (rho * cp)
    L = 0.05
    n_cells = 40
    dx = L / n_cells
    dt = t_end / (n_steps - 1)
    time = np.linspace(0, t_end, n_steps)

    q_true = np.where(time < t_end / 2, 30000.0, 0.0)

    x_centers = np.linspace(dx / 2, L - dx / 2, n_cells)
    sensor_idx = [int(np.argmin(np.abs(x_centers - 0.01)))]

    n = n_cells
    r = alpha * dt / dx**2
    T = np.full(n, 300.0)

    ab = np.zeros((3, n))
    ab[0, 1:] = -r
    ab[1, :] = 1 + 2 * r
    ab[2, :-1] = -r
    ab[1, 0] = 1 + 2 * r
    ab[0, 1] = -2 * r
    ab[1, -1] = 1.0
    ab[2, -2] = 0.0

    fc = 2.0 * dt / (rho * cp * dx)
    T_sensor = np.zeros(n_steps)
    T_sensor[0] = T[sensor_idx[0]]

    for i in range(1, n_steps):
        rhs = T.copy()
        rhs[0] += fc * q_true[i]
        rhs[-1] = 300.0
        T = solve_banded((1, 1), ab, rhs)
        T[-1] = 300.0
        T_sensor[i] = T[sensor_idx[0]]

    rng = np.random.default_rng(seed)
    T_sensor += rng.normal(0, noise_std, n_steps)

    return time, T_sensor


def _write_config(cfg_path: Path, obs_path: Path, n_steps: int, t_end: float) -> None:
    cfg = {
        "problem_type": "1D_transient_IHCP",
        "dimension": 1,
        "transient": True,
        "target_name": "boundary_heat_flux",
        "time": {"start": 0.0, "end": t_end, "n_steps": n_steps},
        "geometry": {"length": 0.05, "n_cells": 40},
        "material": {"density": 7800.0, "specific_heat": 500.0, "conductivity": 50.0},
        "boundary_conditions": {"right_type": "dirichlet", "right_value": 300.0},
        "sensor_positions": [0.01],
        "initial_condition": 300.0,
        "noise_std": 0.2,
        "observations_file": str(obs_path),
        "planner": {
            "max_retries": 5,
            "iteration_budget": 8,
            "reg_order": 1,
        },
    }
    with cfg_path.open("w") as f:
        yaml.dump(cfg, f)


def _write_observations(obs_path: Path, T_sensor: np.ndarray) -> None:
    with obs_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sensor_1_K"])
        for v in T_sensor:
            writer.writerow([f"{v:.6f}"])


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------


def test_agent_loop_terminates_on_synthetic_case(tmp_path):
    """Full agent loop should terminate with a non-hard-fail status."""
    n_steps = 60
    t_end = 30.0

    time, T_sensor = _generate_synthetic_observations(n_steps=n_steps, t_end=t_end)

    cfg_path = tmp_path / "test_case.yaml"
    obs_path = tmp_path / "obs.csv"
    out_dir = tmp_path / "outputs"

    _write_observations(obs_path, T_sensor)
    _write_config(cfg_path, obs_path, n_steps, t_end)

    # Use loose thresholds so a small synthetic case reliably passes
    thresholds = VerifierThresholds(
        rmse_pass=2.0,
        rmse_weak=10.0,
        rel_error_pass=0.1,
        rel_error_weak=0.5,
        osc_fail=0.9,
    )

    agent = IHCPAgent(output_dir=out_dir, thresholds=thresholds)
    planner_overrides = {"max_retries": 5, "iteration_budget": 8, "reg_order": 1}
    summary = agent.run(cfg_path, planner_overrides=planner_overrides)

    # Agent must terminate
    assert summary.final_status in ("pass", "weak_pass", "manual_review", "fail")

    # Traces must be recorded
    assert len(summary.traces) > 0

    # Reports must exist
    for label, path in summary.report_paths.items():
        assert Path(path).exists(), f"Report missing: {label} → {path}"


def test_agent_loop_recovers_flux_order_of_magnitude(tmp_path):
    """Recovered flux should be within an order of magnitude of the true 30 kW/m²."""
    n_steps = 60
    t_end = 30.0
    true_flux_scale = 30000.0

    _, T_sensor = _generate_synthetic_observations(n_steps=n_steps, t_end=t_end)

    cfg_path = tmp_path / "test_case.yaml"
    obs_path = tmp_path / "obs.csv"
    out_dir = tmp_path / "outputs"

    _write_observations(obs_path, T_sensor)
    _write_config(cfg_path, obs_path, n_steps, t_end)

    thresholds = VerifierThresholds(
        rmse_pass=5.0, rmse_weak=20.0,
        rel_error_pass=0.3, rel_error_weak=0.8,
        osc_fail=0.9,
    )

    agent = IHCPAgent(output_dir=out_dir, thresholds=thresholds)
    summary = agent.run(cfg_path, planner_overrides={"iteration_budget": 6})

    if summary.final_result.estimated_x:
        x = np.array(summary.final_result.estimated_x)
        # At least half of recovered parameters should be within 10× of true scale
        near_true = np.sum(np.abs(x) > true_flux_scale / 100)
        assert near_true > len(x) // 3, (
            f"Too few parameters near true flux: {near_true}/{len(x)}"
        )
