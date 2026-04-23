"""
forward_model.py
================
Simplified 1D transient heat conduction forward model.

Problem statement
-----------------
Domain:  rod of length L, uniform material properties.
Spatial: finite-difference (implicit Euler / backward Euler).
Time:    uniform time steps dt.

Boundary conditions
-------------------
  x = 0  (left):  Neumann  →  -k * dT/dx = q(t)   (inversion target)
  x = L  (right): Dirichlet T = T_right  OR  Neumann q_right = 0

Initial condition:  T(x, 0) = T0  (uniform)

The forward model is intentionally simple to keep the prototype
readable.  The interface is designed so that the forward model can be
replaced by a higher-fidelity solver (e.g. FEniCS) without changing the
solver or agent code.

Extension notes
---------------
- Replace `HeatConductionFD` with a class that satisfies the same
  interface to swap in any forward solver.
- The sensitivity matrix approach (unit-impulse superposition) works for
  any *linear* forward model.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import solve_banded

from src.types import BoundaryConditions, Geometry, Material


class HeatConductionFD:
    """1D transient heat conduction solver – implicit finite differences.

    The spatial domain is divided into ``n_cells`` cells of width
    ``dx = L / n_cells``.  Cell centres are at ``x_j = (j + 0.5) * dx``
    for j = 0, …, n_cells-1.

    The left boundary node is a *half-cell* at x = 0, handled via a
    ghost-node / energy-balance approach to apply the Neumann condition
    exactly at the boundary face.

    Parameters
    ----------
    geometry:    rod geometry (L, n_cells)
    material:    density, specific heat, conductivity
    bc:          right-boundary type and value
    time_grid:   1-D array of time points [s]
    """

    def __init__(
        self,
        geometry: Geometry,
        material: Material,
        bc: BoundaryConditions,
        time_grid: list[float],
    ) -> None:
        self.geometry = geometry
        self.material = material
        self.bc = bc
        self.time_grid = np.asarray(time_grid, dtype=float)

        n = geometry.n_cells
        self.n = n
        self.dx = geometry.length / n
        self.x_centers = np.linspace(self.dx / 2, geometry.length - self.dx / 2, n)

        # Pre-compute the tridiagonal system coefficients (constant in time
        # because material properties are constant in this version).
        self._build_system()

    # ------------------------------------------------------------------
    # System assembly
    # ------------------------------------------------------------------

    def _build_system(self) -> None:
        """Pre-compute banded-matrix coefficients for the implicit scheme.

        The system at each time step is:
          A * T^{n+1} = T^n + RHS_flux_term

        A is tridiagonal and constant (linear PDE, constant properties).
        We store it in scipy's banded format (shape 3 × n) so that
        solve_banded can reuse it at every time step without LU refactor.
        """
        n = self.n
        alpha = self.material.diffusivity
        dt = self.time_grid[1] - self.time_grid[0]  # assumed uniform
        dx = self.dx
        r = alpha * dt / dx**2   # Fourier number

        # Banded storage: row 0 = super-diagonal, row 1 = diagonal, row 2 = sub-diagonal
        ab = np.zeros((3, n))

        # Interior nodes (j = 1 … n-2)
        # Equation: -r * T_{j-1} + (1 + 2r) * T_j - r * T_{j+1} = T_j^n
        ab[0, 1:] = -r           # super-diagonal (upper)
        ab[1, :] = 1 + 2 * r    # diagonal
        ab[2, :-1] = -r          # sub-diagonal (lower)

        # Left boundary (j=0): Neumann  –k dT/dx|_{x=0} = q(t)
        # Half-cell energy balance gives:
        #   rho*cp*(dx/2) * (T_0^{n+1} - T_0^n)/dt
        #     = q(t) / 1   (inward flux at face)
        #     + k*(T_1^{n+1} - T_0^{n+1}) / dx   (flux to interior)
        #
        # Rearranging (multiply by dt / (rho*cp*dx/2)):
        #   (1 + 2r) * T_0 - 2r * T_1 = T_0^n + 2*dt*q / (rho*cp*dx)
        #
        # Note: the factor of 2 comes from the half-cell width.
        ab[1, 0] = 1 + 2 * r
        ab[0, 1] = -2 * r       # coupling to T_1 from the left BDF node
        # (sub-diagonal entry at j=0 is unused)

        # Right boundary (j=n-1)
        if self.bc.right_type == "dirichlet":
            # Dirichlet: fix T_{n-1} = T_right by replacing the last equation
            # with the identity  1 * T_{n-1} = T_right.
            #
            # In scipy banded storage with (kl=1, ku=1):
            #   ab[0, j] = A[j-1, j]  (super-diagonal, element in row j-1 col j)
            #   ab[1, j] = A[j, j]    (main diagonal)
            #   ab[2, j] = A[j+1, j]  (sub-diagonal, element in row j+1 col j)
            #
            # For the LAST row (n-1):
            #   identity diagonal:         ab[1, n-1] = 1.0
            #   no coupling below:         ab[2, n-2] = A[n-1, n-2] = 0   ← clears row n-1 col n-2
            #
            # Do NOT touch ab[0, n-1] = A[n-2, n-1].  That element lives in row
            # n-2, not row n-1, and must remain -r so that node n-2 correctly
            # "sees" the Dirichlet boundary temperature in its own equation.
            ab[1, n - 1] = 1.0
            ab[2, n - 2] = 0.0   # clear coupling from last row to second-to-last col
        else:
            # Neumann (insulated): q_right = 0  →  T_{n-1} = T_{n-2}
            # Half-cell balance with zero outward flux:
            #   (1 + 2r) * T_{n-1} - 2r * T_{n-2} = T_{n-1}^n
            ab[1, n - 1] = 1 + 2 * r
            ab[2, n - 2] = -2 * r

        self._ab = ab
        self._r = r
        self._dt = dt
        # Pre-factor: multiplier for q(t) on the right-hand side at node 0
        # = 2*dt / (rho * cp * dx)    from half-cell energy balance
        self._flux_coeff = 2.0 * dt / (self.material.density * self.material.specific_heat * self.dx)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def simulate(
        self,
        q_flux: np.ndarray,
        T0: float,
        sensor_indices: list[int],
    ) -> np.ndarray:
        """Run the forward model for a given heat-flux time series.

        Parameters
        ----------
        q_flux : shape (N_t,)  boundary heat flux at each time step [W/m^2]
        T0     : uniform initial temperature [K]
        sensor_indices : spatial indices of sensor nodes

        Returns
        -------
        T_sensors : shape (len(sensor_indices), N_t)
            Temperature at each sensor over time.
        """
        N_t = len(self.time_grid)
        n = self.n
        T = np.full(n, T0, dtype=float)
        T_sensors = np.zeros((len(sensor_indices), N_t))

        # Record initial condition
        for k, si in enumerate(sensor_indices):
            T_sensors[k, 0] = T[si]

        for i in range(1, N_t):
            rhs = T.copy()
            # Left-boundary flux contribution (half-cell node)
            rhs[0] += self._flux_coeff * q_flux[i]
            # Right-boundary Dirichlet override
            if self.bc.right_type == "dirichlet":
                rhs[-1] = self.bc.right_value

            T = solve_banded((1, 1), self._ab, rhs)

            # Clamp Dirichlet boundary exactly (numerical drift guard)
            if self.bc.right_type == "dirichlet":
                T[-1] = self.bc.right_value

            for k, si in enumerate(sensor_indices):
                T_sensors[k, i] = T[si]

        return T_sensors

    def sensor_indices_from_positions(self, sensor_positions: list[float]) -> list[int]:
        """Map physical sensor positions to nearest cell-centre indices."""
        indices = []
        for xp in sensor_positions:
            idx = int(np.argmin(np.abs(self.x_centers - xp)))
            indices.append(idx)
        return indices
