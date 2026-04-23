"""
types.py
========
Core dataclasses for the IHCP agent system.

All scientific data structures are defined here to keep other modules
import-clean and to make serialization / inspection straightforward.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


# ---------------------------------------------------------------------------
# Physical / problem-specification structures
# ---------------------------------------------------------------------------


@dataclass
class Geometry:
    """1D rod geometry."""
    length: float          # [m]  rod length
    n_cells: int           # number of spatial finite-difference cells


@dataclass
class Material:
    """Homogeneous isotropic material properties (constant in this version)."""
    density: float         # rho  [kg/m^3]
    specific_heat: float   # cp   [J/(kg·K)]
    conductivity: float    # k    [W/(m·K)]

    @property
    def diffusivity(self) -> float:
        """Thermal diffusivity alpha = k / (rho * cp)  [m^2/s]."""
        return self.conductivity / (self.density * self.specific_heat)


@dataclass
class BoundaryConditions:
    """Boundary conditions for the 1D problem.

    Left boundary (x=0): Neumann – the *unknown* boundary heat flux q(t).
    Right boundary (x=L): Dirichlet or Neumann.
    """
    right_type: Literal["dirichlet", "neumann"]   # type at x=L
    right_value: float                             # T_right [K] or q_right [W/m^2]
    # Left boundary value is the inversion target (unknown q(t));
    # it is not stored here but reconstructed from the inversion result.


@dataclass
class ProblemSpec:
    """Normalised specification of a 1D transient IHCP instance.

    Produced by the Parser and consumed by everything else.
    All arrays are plain Python lists or numpy arrays; callers must not
    mutate them after construction.
    """

    # Problem taxonomy
    problem_type: str                      # e.g. "1D_transient_IHCP"
    dimension: int                         # 1
    transient: bool                        # True
    target_name: str                       # e.g. "boundary_heat_flux"

    # Discretisation
    time_grid: list[float]                 # [s]  length N_t
    sensor_positions: list[float]          # [m]  sensor x-coordinates

    # Observations  shape (N_sensors, N_t)
    observations: list[list[float]]

    # Physical description
    geometry: Geometry
    material: Material
    boundary_conditions: BoundaryConditions
    initial_condition: float               # uniform initial temperature [K]

    # Noise estimate (optional; enables discrepancy principle)
    noise_std: float | None = None

    # Free-form metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------------------------
    # Derived helpers
    # -----------------------------------------------------------------------

    @property
    def n_time(self) -> int:
        return len(self.time_grid)

    @property
    def n_sensors(self) -> int:
        return len(self.sensor_positions)

    @property
    def dt(self) -> float:
        if len(self.time_grid) < 2:
            raise ValueError("time_grid must have at least 2 points")
        return self.time_grid[1] - self.time_grid[0]

    @property
    def total_time(self) -> float:
        return self.time_grid[-1] - self.time_grid[0]


# ---------------------------------------------------------------------------
# Inversion / planning structures
# ---------------------------------------------------------------------------

ParameterizationType = Literal["piecewise_constant", "piecewise_linear"]
LambdaStrategy = Literal["fixed", "lcurve", "gcv", "discrepancy", "grid_search"]
RegOrder = Literal[0, 1, 2]


@dataclass
class InversionConfig:
    """Solver configuration produced by the Planner and potentially revised by the Replanner."""

    parameterization_type: ParameterizationType = "piecewise_constant"
    num_parameters: int = 20
    reg_order: RegOrder = 1
    lambda_strategy: LambdaStrategy = "lcurve"
    lambda_value: float | None = None       # used when strategy == "fixed"
    lambda_grid: list[float] | None = None  # used when strategy == "grid_search"
    max_retries: int = 6
    physical_bounds: tuple[float, float] | None = None  # (q_min, q_max) [W/m^2]
    planner_notes: list[str] = field(default_factory=list)
    stop_tolerance: float = 1e-3            # relative improvement threshold
    iteration_budget: int = 10             # hard cap on agent loop iterations
    skip_verifier: bool = False             # ablation: bypass all verification, accept any result
    solver_name: str = "tikhonov"           # registered solver to use (e.g. "tikhonov", "tsvd")


# ---------------------------------------------------------------------------
# Solver structures
# ---------------------------------------------------------------------------


@dataclass
class SolverDiagnostics:
    """Low-level solver diagnostics (for debugging and traceability)."""

    matrix_shape: tuple[int, int]
    condition_estimate: float
    solve_method: str
    warnings: list[str] = field(default_factory=list)
    timing: float = 0.0                    # wall-clock seconds


@dataclass
class SolverResult:
    """Output of a single Tikhonov inversion attempt."""

    estimated_x: list[float]              # recovered q(t) parameters
    fitted_y: list[float]                 # predicted observations (flattened)
    residual_norm: float                  # ||Gx - y||_2
    regularization_norm: float            # ||Lx||_2
    objective_value: float                # residual^2 + lambda * reg^2
    lambda_used: float
    reg_order: int
    status: Literal["success", "warning", "failed"]
    diagnostics: SolverDiagnostics | None = None


# ---------------------------------------------------------------------------
# Verification structures
# ---------------------------------------------------------------------------

VerificationDecision = Literal["pass", "weak_pass", "fail", "manual_review"]


@dataclass
class VerificationResult:
    """Multi-criteria verification result – the scientific core of the agent."""

    decision: VerificationDecision

    # Fit quality
    replay_rmse: float
    relative_replay_error: float

    # Solution smoothness / regularity
    roughness_l1: float                    # sum |Δ^1 x|
    roughness_l2: float                    # ||Δ^1 x||_2
    oscillation_score: float               # fraction of sign-changes in Δx

    # Physical and methodological consistency
    physical_ok: bool
    discrepancy_ok: bool | None            # None when noise_std not available
    stability_ok: bool | None              # None when single-lambda solve

    # Regularization diagnosis
    tradeoff_label: Literal[
        "under_regularized", "well_regularized", "over_regularized", "unknown"
    ]

    # Human-readable explanations
    reasons: list[str] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)

    # Full numeric metrics dict (for JSON export)
    metrics: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Agent-loop structures
# ---------------------------------------------------------------------------


@dataclass
class AgentTrace:
    """Record of a single agent iteration."""

    iteration: int
    config: InversionConfig
    solver_result: SolverResult
    verification: VerificationResult
    replanning_action: str                 # action label taken after this step
    notes: list[str] = field(default_factory=list)


@dataclass
class RunSummary:
    """Complete record of an agent run (for JSON export and reporting)."""

    final_status: Literal["pass", "weak_pass", "manual_review", "fail"]
    final_config: InversionConfig
    final_result: SolverResult
    traces: list[AgentTrace] = field(default_factory=list)
    report_paths: dict[str, str] = field(default_factory=dict)
    summary_notes: list[str] = field(default_factory=list)
