"""
solver_registry.py
==================
Solver registry and dispatch layer for the IHCP agent.

Provides a minimal protocol-based abstraction so that:
  - The agent loop calls ``registry.solve_single(name, G, y, config, lam)``
    without importing solver modules directly.
  - New solvers are added by registering a module — no changes to agent.py.
  - Both Tikhonov and TSVD (and future solvers) share the same interface.

Solver interface (informal protocol)
-------------------------------------
Each registered solver module must expose:

    def solve_single(
        G: np.ndarray,
        y: np.ndarray,
        config: InversionConfig,
        lam: float,
    ) -> SolverResult: ...

    def solve_grid(
        G: np.ndarray,
        y: np.ndarray,
        config: InversionConfig,
        lambda_grid: list[float],
    ) -> list[SolverResult]: ...

Currently registered solvers
------------------------------
  "tikhonov" : Tikhonov normal-equation solver (src/tikhonov_solver.py)
  "tsvd"     : Truncated SVD solver           (src/tsvd_solver.py)

Usage in the agent
------------------
    from src.solver_registry import get_registry
    registry = get_registry()
    result = registry.solve_single(config.solver_name, G, y, config, lam)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from src.types import InversionConfig, SolverResult


class SolverRegistry:
    """Registry mapping solver names to solver modules."""

    def __init__(self) -> None:
        self._solvers: dict[str, Any] = {}

    def register(self, name: str, module: Any) -> None:
        """Register a solver module under *name*.

        Parameters
        ----------
        name   : short identifier, e.g. "tikhonov" or "tsvd"
        module : any object with ``solve_single`` and ``solve_grid`` callables
        """
        if not (callable(getattr(module, "solve_single", None)) and
                callable(getattr(module, "solve_grid", None))):
            raise TypeError(
                f"Solver module '{name}' must expose solve_single() and solve_grid()"
            )
        self._solvers[name] = module

    def available(self) -> list[str]:
        """Return sorted list of registered solver names."""
        return sorted(self._solvers.keys())

    def get(self, name: str) -> Any:
        """Return the registered module for *name*, or raise KeyError."""
        if name not in self._solvers:
            raise KeyError(
                f"Unknown solver '{name}'. Available: {self.available()}"
            )
        return self._solvers[name]

    # ------------------------------------------------------------------
    # Convenience dispatch methods
    # ------------------------------------------------------------------

    def solve_single(
        self,
        name: str,
        G: np.ndarray,
        y: np.ndarray,
        config: "InversionConfig",
        lam: float,
    ) -> "SolverResult":
        """Dispatch a single-lambda solve to the named solver."""
        return self.get(name).solve_single(G, y, config, lam)

    def solve_grid(
        self,
        name: str,
        G: np.ndarray,
        y: np.ndarray,
        config: "InversionConfig",
        lambda_grid: list[float],
    ) -> "list[SolverResult]":
        """Dispatch a grid solve to the named solver."""
        return self.get(name).solve_grid(G, y, config, lambda_grid)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------


def _build_default_registry() -> SolverRegistry:
    """Build the default registry with Tikhonov and TSVD registered."""
    import src.tikhonov_solver as _tikhonov
    import src.tsvd_solver as _tsvd

    reg = SolverRegistry()
    reg.register("tikhonov", _tikhonov)
    reg.register("tsvd", _tsvd)
    return reg


_registry: SolverRegistry | None = None


def get_registry() -> SolverRegistry:
    """Return the module-level solver registry (lazy singleton)."""
    global _registry
    if _registry is None:
        _registry = _build_default_registry()
    return _registry
