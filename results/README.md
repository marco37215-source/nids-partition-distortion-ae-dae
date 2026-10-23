# Results

Everything in this folder is produced by `scripts/` and can be regenerated with `python scripts/reproduce_all.py`.

## Tables (`tables/`)

| File | Manuscript | Content |
|---|---|---|
| `Table_3_1_model_view_redundancy.csv` | Table 6 | Rows, groups, redundancy, pure-benign rows and groups, error floor, largest group |
| `Table_3_2_UNSW_structural_validation.csv` | Table 8 | Three UNSW-NB15 allocation regimes: overlap, development TV, exceedances (with source labels) |
| `Table_3_2b_source_balanced_profile.csv` | Table 7 | Singleton share and ≥100 rows by role (development and pool recomputed; other rows from the analysis record) |
| `Table_3_2c_role_tv_distances.csv` | Section 4.5 | TV distance to the pool and singleton share of every v3.4 role |
| `Table_3_3_ge100_band_extract.csv` | Table S2 (≥100 row) | ≥100 band per role: target, actual, tolerance, groups, mean and largest group |
| `Table_S2_role_by_band_allocation.csv` | Table S2 | Full v3.4 role × band gate |
| `Table_3_4_AE_DAE_contrasts.csv` | Table 10 | Paired DAE − AE contrasts: mean, median, SD, d_z, consistency, exact and Monte-Carlo bootstrap bounds, and the frozen NB-08 bounds for comparison |
| `Table_3_5_selected_configurations.csv` | Table 9 | Selected configurations, recomputed development MCC mean and SD, training time |
| `Table_3_6_final_test_levels.csv` | Section 4.7 | Five-seed means and SDs per model (reference only; not compared between corpora) |
| `Table_3_7_statistical_tests.csv` | Section 4.7 | Paired t (with interval), exact sign and Wilcoxon p-values |
| `Table_3_8_denominator_and_score_geometry.csv` | Section 4.7 | Per-row versus per-fingerprint recall, per-vector contrast and interval, score geometry of missed attacks |
| `Table_3_9_development_vs_final.csv` | Section 4.7 | Development versus final MCC, raw and excluding mixed-label groups |
| `Table_3_10_selection_ranking_reproduced.csv` | Section 3.9 | Selection ranking recomputed from the confirmation seeds |
| `Table_S3_family_recall.csv` | Table S3 | Family recall per row and per vector; share of misses |

## Figure source data (`figure_source_data/`) and figures (`figures/`)

| Source data | Figure (PNG 300 dpi + PDF) | Manuscript |
|---|---|---|
| `Figure_3_1_data.csv` | `Figure_3_1_rows_vs_fingerprints` | Fig. 4 |
| `Figure_3_3_data.csv` | `Figure_3_3_fp_rate_by_multiplicity_band` | Fig. 5 |
| `Figure_3_2_data.csv` | `Figure_3_2_benign_transfer_progression` | Fig. 6 |
| `Figure_3_4_data.csv` | `Figure_3_4_quantile_transfer` | Fig. 7 |
| `Figure_3_5_data.csv` | `Figure_3_5_paired_metric_differences` | Fig. 8 |

`figures/manuscript_numbering/Figure_4.pdf` … `Figure_8.pdf` are the same figures named by journal number. `tests/test_reproduction_scripts.py` checks that the plotted values equal those logged when the submitted figures were drawn (`manuscript/figures/figure_values_log.json`).

## Claim checks (`claims_check/`)

There is one CSV per script. Each row gives:

* the manuscript location;
* a description;
* the value as printed;
* the recomputed value;
* the source file;
* a status: `PASS`, `FAIL`, `NOT_REPRODUCIBLE_HERE`, `FROZEN_TABLE_DISCREPANCY`, `CORRECTION_NEEDED` or `INFO`.

`reproduce_final_statistics__with_archives.csv` is the log of the archive-mode run (Level 2), which contains 10 additional archive checks.
