"""
metrics.py
==========
Evaluation metrics for 2D inverse heat-flux reconstruction.

Provides five metrics:

1. rmse_flux
   Standard RMSE between predicted and ground-truth flux fields.

2. ssim_flux
   Structural Similarity Index (SSIM) applied directly to the flux field.
   Uses the true value range (not the plotting colormap range) for
   consistent normalisation across all solver comparisons.

3. peak_localization_error  [applicable: localised / multi-spot families]
   Average Euclidean distance (in normalised coordinates) between predicted
   and ground-truth peak locations.  Uses Hungarian optimal matching for
   multi-peak cases.  Returns np.nan when not applicable.

4. band_energy_error  [always applicable]
   Relative energy deviation between predicted and true flux fields in three
   frequency bands (low / mid / high), computed via 2D FFT.
   Also returns a scalar summary = mean absolute relative error across bands.

5. support_overlap  [applicable: localised / multi-spot / stress families]
   Dice coefficient between predicted and true active-support regions,
   where "active" is defined as |q| > threshold_frac * max|q_true|.
   Returns np.nan when the true support is trivially zero everywhere.

Diagnostic fields returned by compute_all_metrics():
    runtime_seconds
    success
    failure_reason  (empty string if no failure)
    selected_reg_param
    selected_rank
    selected_n_modes
    posterior_uncertainty_mean
    solver_notes     (free-form string)

Public API
----------
    compute_all_metrics(
        q_pred, q_true,
        family_name=None,
        diag_dict=None,     # solver diagnostics dict
    ) -> dict

    Also exported individually:
        compute_rmse_flux
        compute_ssim_flux
        compute_peak_localization_error
        compute_band_energy_error
        compute_support_overlap
"""

from __future__ import annotations

import warnings
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# 1. RMSE
# ---------------------------------------------------------------------------

def compute_rmse_flux(q_pred: np.ndarray, q_true: np.ndarray) -> float:
    """Root-mean-square error between predicted and true flux fields."""
    q_pred = np.asarray(q_pred, dtype=float)
    q_true = np.asarray(q_true, dtype=float)
    return float(np.sqrt(np.mean((q_pred - q_true) ** 2)))


# ---------------------------------------------------------------------------
# 2. SSIM
# ---------------------------------------------------------------------------

def compute_ssim_flux(
    q_pred: np.ndarray,
    q_true: np.ndarray,
    data_range: float | None = None,
) -> float:
    """Structural Similarity Index on the 2D flux field.

    Parameters
    ----------
    q_pred, q_true : (ny, nt) flux arrays
    data_range     : value range for SSIM normalisation.  If None, uses
                     max(|q_true|) * 2 to avoid scale dependency.
                     This is independent of any plotting colour scale.

    Returns
    -------
    ssim : float in [-1, 1] (1 = identical)
    """
    q_pred = np.asarray(q_pred, dtype=float)
    q_true = np.asarray(q_true, dtype=float)

    if data_range is None:
        q_abs_max = np.max(np.abs(q_true))
        if q_abs_max < 1e-12:
            # Degenerate: true field is zero
            return 1.0 if np.max(np.abs(q_pred)) < 1e-12 else 0.0
        data_range = 2.0 * q_abs_max

    try:
        from skimage.metrics import structural_similarity as sk_ssim  # type: ignore
        ssim_val = sk_ssim(
            q_true, q_pred,
            data_range=data_range,
        )
        return float(ssim_val)
    except ImportError:
        # Fall back to manual SSIM computation (window = full image)
        return _ssim_manual(q_pred, q_true, data_range)


def _ssim_manual(
    q_pred: np.ndarray,
    q_true: np.ndarray,
    data_range: float,
) -> float:
    """Manual global-window SSIM as fallback when skimage is unavailable."""
    C1 = (0.01 * data_range) ** 2
    C2 = (0.03 * data_range) ** 2
    mu_p = float(np.mean(q_pred))
    mu_t = float(np.mean(q_true))
    var_p = float(np.var(q_pred))
    var_t = float(np.var(q_true))
    cov   = float(np.mean((q_pred - mu_p) * (q_true - mu_t)))
    num = (2 * mu_p * mu_t + C1) * (2 * cov + C2)
    den = (mu_p**2 + mu_t**2 + C1) * (var_p + var_t + C2)
    return float(num / (den + 1e-300))


# ---------------------------------------------------------------------------
# 3. Peak Localization Error
# ---------------------------------------------------------------------------

def compute_peak_localization_error(
    q_pred: np.ndarray,
    q_true: np.ndarray,
    n_peaks: int = 1,
    threshold_frac: float = 0.3,
    domain_shape: tuple[float, float] = (1.0, 1.0),
) -> float:
    """Average distance between predicted and true peak locations.

    Parameters
    ----------
    q_pred, q_true  : (ny, nt) flux arrays
    n_peaks         : expected number of peaks (default 1)
    threshold_frac  : fraction of max to define a candidate peak region
    domain_shape    : (Ly, T_total) physical extents for distance normalisation

    Returns
    -------
    error : float — mean matched peak distance in normalised coords [0,1]
            np.nan if no peaks detected in either field
    """
    q_pred = np.asarray(q_pred, dtype=float)
    q_true = np.asarray(q_true, dtype=float)
    ny, nt = q_pred.shape

    def find_peaks(q: np.ndarray, n: int) -> list[tuple[float, float]]:
        """Return up to n peak locations as (y_norm, t_norm)."""
        q_abs = np.abs(q)
        thresh = threshold_frac * np.max(q_abs)
        if thresh < 1e-12:
            return []
        peaks = []
        # Simple non-max suppression: find local maxima above threshold
        # Flatten and take top-n locations
        flat_idx = np.argsort(q_abs.ravel())[::-1]
        found: list[tuple[int, int]] = []
        min_sep = max(1, min(ny, nt) // (2 * n + 2))   # min separation in cells
        for idx in flat_idx:
            if q_abs.ravel()[idx] < thresh:
                break
            yi = idx // nt
            ti = idx % nt
            # Check separation from already-found peaks
            too_close = False
            for (fy, ft) in found:
                if abs(yi - fy) < min_sep and abs(ti - ft) < min_sep:
                    too_close = True
                    break
            if not too_close:
                found.append((yi, ti))
            if len(found) >= n:
                break
        for (yi, ti) in found:
            peaks.append((float(yi) / (ny - 1), float(ti) / (nt - 1)))
        return peaks

    peaks_pred = find_peaks(q_pred, n_peaks)
    peaks_true = find_peaks(q_true, n_peaks)

    if not peaks_pred or not peaks_true:
        return float("nan")

    # Hungarian matching minimising total distance
    try:
        from scipy.optimize import linear_sum_assignment  # type: ignore
        np_pred = np.array(peaks_pred)
        np_true = np.array(peaks_true)
        # Cost matrix: pairwise Euclidean distance in normalised [0,1]² coords
        diff = np_pred[:, None, :] - np_true[None, :, :]  # (np, nt, 2)
        cost = np.sqrt(np.sum(diff ** 2, axis=2))          # (np, nt)
        row_ind, col_ind = linear_sum_assignment(cost)
        distances = [cost[r, c] for r, c in zip(row_ind, col_ind)]
        return float(np.mean(distances))
    except ImportError:
        # Fall back: nearest-neighbour matching
        total = 0.0
        for pp in peaks_pred:
            dists = [np.sqrt((pp[0] - pt[0])**2 + (pp[1] - pt[1])**2)
                     for pt in peaks_true]
            total += float(min(dists))
        return total / len(peaks_pred)


# ---------------------------------------------------------------------------
# 4. Band Energy Error
# ---------------------------------------------------------------------------

def compute_band_energy_error(
    q_pred: np.ndarray,
    q_true: np.ndarray,
    n_bands: int = 3,
) -> dict[str, float]:
    """Relative energy deviation between predicted and true flux in frequency bands.

    Computes 2D FFT of both fields, splits frequency content into
    low / mid / high bands, and reports the relative energy error per band.

    Parameters
    ----------
    q_pred, q_true : (ny, nt) flux arrays
    n_bands        : number of equal-width bands (default 3 → low/mid/high)

    Returns
    -------
    dict with keys:
        band_{i}_true_energy    : float — true energy in band i  (i=0..n_bands-1)
        band_{i}_pred_energy    : float — pred energy in band i
        band_{i}_rel_error      : float — |E_pred - E_true| / (E_true + eps)
        band_error_scalar       : float — mean absolute relative error across bands
                                  (scalar for ranking)
    """
    q_pred = np.asarray(q_pred, dtype=float)
    q_true = np.asarray(q_true, dtype=float)

    # 2D FFT (magnitude spectrum)
    F_pred = np.abs(np.fft.fft2(q_pred)) ** 2   # power spectrum
    F_true = np.abs(np.fft.fft2(q_true)) ** 2

    ny, nt = q_pred.shape
    total_cells = ny * nt

    # Radial frequency grid (normalised: 0 = DC, 1 = Nyquist corner)
    fy = np.fft.fftfreq(ny)  # (ny,)
    ft = np.fft.fftfreq(nt)  # (nt,)
    FY, FT = np.meshgrid(fy, ft, indexing="ij")  # (ny, nt)
    freq_rad = np.sqrt(FY**2 + FT**2)             # (ny, nt) in [0, ~0.71]

    # Band boundaries
    f_max = np.max(freq_rad)
    band_edges = np.linspace(0.0, f_max, n_bands + 1)

    result: dict[str, float] = {}
    rel_errors: list[float] = []

    for i in range(n_bands):
        f_lo = band_edges[i]
        f_hi = band_edges[i + 1]
        if i == 0:
            mask = freq_rad <= f_hi
        elif i == n_bands - 1:
            mask = freq_rad > f_lo
        else:
            mask = (freq_rad > f_lo) & (freq_rad <= f_hi)

        e_true = float(np.sum(F_true[mask]))
        e_pred = float(np.sum(F_pred[mask]))
        eps    = 1e-10 * (float(np.sum(F_true)) + 1.0)
        rel_err = abs(e_pred - e_true) / (e_true + eps)

        label = ["low", "mid", "high"][i] if n_bands == 3 else str(i)
        result[f"band_{label}_true_energy"] = e_true
        result[f"band_{label}_pred_energy"] = e_pred
        result[f"band_{label}_rel_error"]   = rel_err
        rel_errors.append(rel_err)

    result["band_error_scalar"] = float(np.mean(rel_errors))
    return result


# ---------------------------------------------------------------------------
# 5. Support Overlap (Dice coefficient)
# ---------------------------------------------------------------------------

def compute_support_overlap(
    q_pred: np.ndarray,
    q_true: np.ndarray,
    threshold_frac: float = 0.10,
) -> float:
    """Dice coefficient between predicted and true active-support regions.

    The active region is defined as: |q| > threshold_frac * max(|q_true|).
    The threshold is applied to BOTH fields using the SAME absolute threshold
    derived from q_true (to avoid biasing the comparison).

    Rule: threshold = threshold_frac * max(|q_true|)
    This is documented and fixed — it does not depend on q_pred.

    Returns
    -------
    dice : float in [0, 1]  (1 = perfect overlap)
           np.nan if true support is empty (degenerate case)
    """
    q_pred = np.asarray(q_pred, dtype=float)
    q_true = np.asarray(q_true, dtype=float)

    q_max = float(np.max(np.abs(q_true)))
    if q_max < 1e-12:
        # Degenerate: both fields should be zero → undefined
        return float("nan")

    threshold = threshold_frac * q_max
    support_true = np.abs(q_true) > threshold
    support_pred = np.abs(q_pred) > threshold

    n_true = float(np.sum(support_true))
    n_pred = float(np.sum(support_pred))
    n_inter = float(np.sum(support_true & support_pred))

    if n_true + n_pred < 0.5:
        return 1.0   # both empty — perfect match
    if n_true < 0.5:
        return float("nan")   # true support empty

    dice = 2.0 * n_inter / (n_true + n_pred)
    return float(dice)


# ---------------------------------------------------------------------------
# Master function
# ---------------------------------------------------------------------------

# Families where peak localization is meaningful
_PEAK_FAMILIES = {
    "gaussian_localized",
    "overlapping_multi_spot",
    "moving_hotspot",
    "discontinuous_piecewise",
}

# Families where support overlap is meaningful
_SUPPORT_FAMILIES = {
    "gaussian_localized",
    "overlapping_multi_spot",
    "moving_hotspot",
    "discontinuous_piecewise",
    "matern_grf",
}


def compute_all_metrics(
    q_pred: np.ndarray,
    q_true: np.ndarray,
    family_name: str | None = None,
    diag_dict: dict[str, Any] | None = None,
    n_peaks: int = 1,
) -> dict[str, Any]:
    """Compute all five metrics plus diagnostic fields.

    Parameters
    ----------
    q_pred      : (ny_q, nt_q) predicted flux
    q_true      : (ny_q, nt_q) ground-truth flux
    family_name : heat-flux family name (used to gate per-family metrics)
    diag_dict   : solver diagnostics dict (for extracting reg_param, rank, etc.)
    n_peaks     : number of expected peaks (for peak_localization_error)

    Returns
    -------
    Flat dict with all metric values and diagnostic fields.
    """
    if diag_dict is None:
        diag_dict = {}

    result: dict[str, Any] = {}

    # --- Core metrics (always computed) ---
    try:
        result["rmse_flux"] = compute_rmse_flux(q_pred, q_true)
    except Exception as e:
        result["rmse_flux"] = float("nan")
        result["rmse_flux_error"] = str(e)

    try:
        result["ssim_flux"] = compute_ssim_flux(q_pred, q_true)
    except Exception as e:
        result["ssim_flux"] = float("nan")
        result["ssim_flux_error"] = str(e)

    try:
        band_results = compute_band_energy_error(q_pred, q_true)
        result.update(band_results)
    except Exception as e:
        result["band_error_scalar"] = float("nan")
        result["band_energy_error_error"] = str(e)

    # --- Peak localization (gated by family) ---
    if family_name is None or family_name in _PEAK_FAMILIES:
        try:
            result["peak_localization_error"] = compute_peak_localization_error(
                q_pred, q_true, n_peaks=n_peaks
            )
        except Exception as e:
            result["peak_localization_error"] = float("nan")
            result["peak_localization_error_error"] = str(e)
    else:
        result["peak_localization_error"] = float("nan")

    # --- Support overlap (gated by family) ---
    if family_name is None or family_name in _SUPPORT_FAMILIES:
        try:
            result["support_overlap"] = compute_support_overlap(q_pred, q_true)
        except Exception as e:
            result["support_overlap"] = float("nan")
            result["support_overlap_error"] = str(e)
    else:
        result["support_overlap"] = float("nan")

    # --- Diagnostic fields ---
    result["success"] = (
        np.isfinite(result.get("rmse_flux", float("nan")))
        and np.all(np.isfinite(np.asarray(q_pred)))
    )
    result["failure_reason"]     = "" if result["success"] else "non-finite prediction"
    result["selected_reg_param"] = diag_dict.get("lam", float("nan"))
    result["selected_rank"]      = diag_dict.get("kept_rank", diag_dict.get("rank_used", float("nan")))
    result["selected_n_modes"]   = diag_dict.get("n_modes_selected", float("nan"))
    result["posterior_uncertainty_mean"] = diag_dict.get("posterior_uncertainty_mean", float("nan"))
    result["solver_notes"]       = diag_dict.get("solver_name", "")

    return result
