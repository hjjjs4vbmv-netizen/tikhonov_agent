"""
generate_summaries.py
=====================
Automatically generate summary CSVs from raw results.

All summaries are derived from raw CSVs — never hand-written.

Outputs
-------
    reports/benchmark_core_summary.csv
    reports/sensor_layout_track_summary.csv
    reports/stress_track_summary.csv
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

_HERE         = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


SUMMARY_METRICS = [
    "rmse_flux", "ssim_flux", "peak_localization_error",
    "band_error_scalar", "support_overlap", "runtime_seconds",
]

GROUPBY_CORE = ["family_name", "primary_axis_name", "primary_axis_level",
                "primary_axis_value", "solver_name", "noise_sigma"]

GROUPBY_LAYOUT = ["family_name", "primary_axis_level", "primary_axis_value",
                  "solver_name", "sensor_config", "noise_sigma"]

GROUPBY_STRESS = ["family_name", "primary_axis_level", "primary_axis_value",
                  "secondary_axis_level", "solver_name", "noise_sigma"]


def load_raw(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _safe_float(v: str) -> float | None:
    try:
        f = float(v)
        return f if np.isfinite(f) else None
    except (ValueError, TypeError):
        return None


def group_and_summarise(
    rows: list[dict],
    groupby: list[str],
    metrics: list[str],
) -> list[dict]:
    """Group rows by key fields, compute mean/std/count per metric."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(k, "") for k in groupby)
        groups[key].append(row)

    summary_rows: list[dict] = []
    for key, grp in groups.items():
        base = dict(zip(groupby, key))
        base["n_runs"] = len(grp)
        base["n_success"] = sum(int(r.get("success", 0)) for r in grp)

        for metric in metrics:
            vals = [_safe_float(r.get(metric, "")) for r in grp]
            vals = [v for v in vals if v is not None]
            if vals:
                base[f"{metric}_mean"] = float(np.mean(vals))
                base[f"{metric}_std"]  = float(np.std(vals))
                base[f"{metric}_min"]  = float(np.min(vals))
                base[f"{metric}_max"]  = float(np.max(vals))
            else:
                for suf in ("_mean", "_std", "_min", "_max"):
                    base[f"{metric}{suf}"] = float("nan")

        summary_rows.append(base)

    # Sort for readability
    summary_rows.sort(key=lambda r: (
        r.get("family_name", ""),
        str(r.get("primary_axis_level", "")),
        r.get("solver_name", ""),
    ))
    return summary_rows


def write_summary(rows: list[dict], path: Path) -> None:
    if not rows:
        print(f"  No rows for {path.name}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"  Written {len(rows)} rows → {path.name}")


def main() -> None:
    reports = _PROJECT_ROOT / "reports"

    print("Generating benchmark_core_summary.csv …")
    core_rows = load_raw(reports / "benchmark_core_raw.csv")
    core_summary = group_and_summarise(core_rows, GROUPBY_CORE, SUMMARY_METRICS)
    write_summary(core_summary, reports / "benchmark_core_summary.csv")

    print("Generating sensor_layout_track_summary.csv …")
    layout_rows = load_raw(reports / "sensor_layout_track_raw.csv")
    layout_summary = group_and_summarise(layout_rows, GROUPBY_LAYOUT, SUMMARY_METRICS)
    write_summary(layout_summary, reports / "sensor_layout_track_summary.csv")

    print("Generating stress_track_summary.csv …")
    stress_rows = load_raw(reports / "stress_track_raw.csv")
    stress_summary = group_and_summarise(stress_rows, GROUPBY_STRESS, SUMMARY_METRICS)
    write_summary(stress_summary, reports / "stress_track_summary.csv")

    print("Done.")


if __name__ == "__main__":
    main()
