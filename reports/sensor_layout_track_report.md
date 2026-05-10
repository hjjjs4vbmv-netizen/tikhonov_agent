# Sensor Layout Track Report

**Generated from:** `sensor_layout_track_raw.csv`
**Total runs:** 216  |  **Failed:** 0

---

## Track Definition

`sensor_layout_track` studies how sensor placement affects reconstruction
quality **across the full primary-axis range of each family**.

Layout is the track-level variable, but the **primary-axis sweep is mandatory**
— each family is still swept over 3 primary-axis levels at each layout.

---

## Families

gaussian_localized, matern_grf, moving_hotspot, overlapping_multi_spot

## Layouts

| Layout | Count | Description |
|--------|-------|-------------|
| uniform | 9 | 3×3 evenly-spaced interior grid |
| boundary_biased | 9 | x-positions biased toward flux boundary (x≈0) |
| clustered | 9 | sensors bunched in central quadrant |

---

## Main Findings

### RMSE by Layout × Family (mean across primary-axis levels, noise=0.1 K, tikhonov_2d)

| Family | boundary_biased | clustered | uniform |
| --- | --- | --- | --- |
| gaussian localized | 160 | 201 | 159 |
| matern grf | 422 | 391 | 427 |
| moving hotspot | 289 | 320 | 292 |
| overlapping multi spot | 209 | 324 | 223 |

### Layout Sensitivity: RMSE ratio (clustered / uniform)

- **gaussian_localized**: 1.26× (clustered / uniform)
- **matern_grf**: 0.92× (clustered / uniform)
- **moving_hotspot**: 1.10× (clustered / uniform)
- **overlapping_multi_spot**: 1.45× (clustered / uniform)

---

## Limitations

1. Sensor count is fixed at 9 across layouts (fair comparison).
2. Layout positions are deterministic; no random placement study conducted.
3. deepxde_pinn layout sensitivity requires separate run (not included here).
