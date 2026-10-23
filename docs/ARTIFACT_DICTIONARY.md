# Artefact dictionary

`artifacts/ARTIFACT_PROVENANCE.csv` lists every frozen file with its upload name, status (`frozen` or `truncated`), number of data rows, size and SHA-256. This dictionary explains what each file is and what its columns mean. Files are grouped as in the repository.

## Conventions used throughout

| Term | Meaning |
|---|---|
| `row_id` | `<dataset>::<source file>::<10-digit 1-based source row>`, for example `UNSWNB15::UNSW-NB15_1.csv::0000000001`. Immutable identity of one source record. |
| `feature_fingerprint` | `h128:` followed by 32 hexadecimal characters. Identity of the frozen raw model-input vector; rows with the same value are identical to the model. See `docs/LIMITATIONS.md` on the effective bits for CICIDS2017. |
| `fingerprint_group_class` | `unique` (singleton), `same-label duplicate group`, or `mixed-label/conflicting group`. In membership files, `pure benign group` / `pure attack group` / `mixed-label/conflicting group` refers to the label composition of the whole group. |
| `partition` | One of `benign_weight_train`, `benign_early_stop`, `benign_threshold_calibration`, `development`, `final_test`, `attack_reserve_unused`. |
| `size_band` | Multiplicity band: `1`, `2`, `3-4`, `5-9`, `10-19`, `20-49`, `50-99`, `>=100`. |
| `binary_label`, `y_true` | 0 = benign, 1 = attack. |
| `config_hash` | SHA-256 of the canonical JSON of `effective_config` (`src/utils/hashing.py`). |
| `run_hash` | Identity of one trained run, as recorded by the notebooks. The hashing rule is not documented in the artefacts. |
| `*_hash` fields of manifests | Self-hash: SHA-256 of the canonical JSON of the manifest without the hash field and without `created_at_utc` (verified for ten manifests). |

## CICIDS2017

| File | Content |
|---|---|
| `provenance/prepartition_readiness_report.json` | PRE-00 sections 1–7: `PASS_WITH_NONBLOCKING_WARNINGS`. Records the duplicate header name `Fwd Header Length` (parser-renamed to `.1`), the fingerprint algorithm, and the upstream policy hashes. |
| `fingerprints/fingerprint_audit.json` | Corpus-level fingerprint counts. Includes the ordered model-input `column_order` (78 columns, with the original leading spaces) and `master_dataset_sha256`. |
| `fingerprints/conflicting_fingerprint_manifest.csv` | The 698 mixed-label groups: `fingerprint_group_size`, label min/max/set, first family, family set (JSON). |
| `fingerprints/row_modelview_group_mapping_first100k.csv` | **First 100,000 rows** of the row → fingerprint map: `fingerprint_group_size`, `fingerprint_group_class`, `binary_label`, `attack_family_metadata`, `future_partition_eligibility`. |
| `partition/partition_policy_manifest.json` | Frozen PRE-01 policy. Contains the benign target fractions, the 0.49 prevalence cap, the 10-step lexicographic priority order, the tie-breaking rule `SHA256(str(PARTITION_SEED) + '\|' + fingerprint)`, and the preprocessing hand-off rule. |
| `partition/partition_integrity_report.json` | 20 hard validation checks (all passed), observed allocation, deviations from targets, and the downstream hand-off. |
| `partition/attack_allocation_manifest.json` | Attack totals. Assignment of each mixed-label group, with its benign and attack rows, family vector and stable tie key; reserve reason counts. |
| `partition/benign_allocation_table.csv` | Nominal versus achieved benign rows per role. Every target was met exactly. |
| `partition/family_allocation_table.csv` | Per family: row and group support; development, final-test and reserve allocation; deviations; status. |
| `partition/partition_membership_first100k.csv` | **First 100,000 rows** of the membership file: `partition`, group classes, label, family, source file and row, reserve reason. |
| `preprocessing/preprocessing_handoff_manifest.json` | Fit rule (`benign_weight_train` only), permitted and prohibited final-test operations, model-input order, role row counts, partition manifest hashes. |
| `model_selection/selected_models_manifest.json` | Selected AE and DAE: full `effective_config`, `config_hash`, development summary, selection hierarchy, `family_metrics_used_for_selection: false`, upstream identity hashes. |
| `model_selection/top_three_configs_{AE,DAE}.json` | The three confirmation candidates per model type, with their `effective_config` and search rank. |
| `model_selection/selection_ranking.csv` | Confirmation summary per candidate (mean, median, SD and range of MCC; mean FPR, FP/1000 and PR-AUC; parameters; training time) and `selection_rank`. |
| `model_selection/confirmation_seed_results.csv` | One row per candidate × seed (101/202/303): threshold, best epoch, duration, all metrics, confusion counts. |
| `final_evaluation/final_seed_results.csv` | One row per selected model × final seed (101–505): same columns as above. In the CICIDS2017 file the metric columns are in alphabetical order. |
| `statistical_analysis/paired_seed_values.csv` | AE value, DAE value and difference per metric × seed. |
| `statistical_analysis/paired_seed_bootstrap_effects.csv` | NB-08 summary per metric: mean, median and SD of the differences, `cohen_dz`, and the 10,000-resample bootstrap CI (seed 2026). |
| `statistical_analysis/T14_*, T18_*, T19_*` | NB-08 thesis tables. T14 is the five-seed performance; T18 the paired differences by seed; T19 the t, sign and Wilcoxon tests and the bootstrap. |

## UNSW-NB15

| File | Content |
|---|---|
| `provenance/feature_schema_1_to_49.csv` | Raw 49-column schema: position, name as stored (some names contain spaces, e.g. `ct_src_ ltm`), assigned name, published type, description. |
| `fingerprints/fingerprint_audit.json` | Corpus-level fingerprint counts and the 41-column model-view order. |
| `fingerprints/duplicate_group_manifest.csv` | All 75,768 same-label duplicate groups (56,168 benign, 19,600 attack), with size and label and family sets. |
| `fingerprints/row_modelview_group_mapping_first100k.csv` | **First 100,000 rows** of the row → fingerprint map. |
| `partition/initial_atomic/` | Nothing retained; see the README in that folder. |
| `partition/source_balanced/smoke_manifest_source_balanced.json` | Benign quantile-transfer gate on the source-balanced allocation: `FAIL`, development exceedance 0.53626, calibration 0.01000. |
| `partition/source_balanced/diagnostic_manifest_00C_block_decomposition.json` | Block-wise error decomposition. The numerical block is the leading contributor. |
| `partition/source_balanced/diagnostic_manifest_00D_mixed_label.json` | Pure versus mixed-label development-benign rows (220,890 / 986), and CT-7 median \|z\| (calibration 0.479, mixed 0.657, pure 4.471). |
| `partition/source_balanced/development_benign_fingerprint_level_summary.csv` | One row per development-benign fingerprint group (60,519): class, `benign_rows`, median and mean total MSE, `above_calibration_p99_rate` (always 0 or 1). |
| `partition/final_source_multiplicity_balanced/source_multiplicity_amendment.json` | Frozen v3 amendment: bands, tolerances, exempt cells, the >400-row weight-train rule, the stopping rule, `policy_hash`. |
| `.../implementation_fix_v3_1…v3_4.json` | Implementation history of the same frozen policy (greedy repair, monolithic MILP, low-band bridge, singleton-tolerance fix). |
| `.../coordinated_feasibility_solver_manifest.json` | The two HiGHS sub-problems: ≥100 stage (stopped at the time limit; feasible) and bands 2–99 (optimal). |
| `.../partition_integrity_report.json` | v3.4: `PASS`, role pure-benign capacities, all gates, `fingerprint_crossings: 0`, parent and new membership SHA-256. |
| `.../multiplicity_gate.csv` | Role × band target, actual, deviation, tolerance, pass (40 cells). |
| `.../band_ge100_role_report.csv` | ≥100 band per role: groups, rows, mean and largest group size. |
| `.../source_gate_actual.csv` | Pure-benign rows per role × source file. |
| `.../singleton_source_gate.csv`, `.../source_x_multiplicity_gate.csv` | Role × source (× band) targets and actuals, tolerances, exemptions, pass flags. |
| `.../partition_membership_first100k.csv` | **First 100,000 rows** of the v3.4 membership. Includes `attack_cat_original` and `attack_cat_canonical`. |
| `.../smoke_manifest_final.json` | Gate on v3.4: `PASS`, development exceedance 0.010024, calibration 0.010003, ratio 1.0021. |
| `.../benign_quantile_ladder.csv` | Calibration and development benign error quantiles at eight percentiles, and their ratio. |
| `.../smoke_effective_config.json` | Configuration of the diagnostic smoke AE (the same `config_hash` as in the PASS manifest). |
| `model_selection/*` | As for CICIDS2017. `confirmation_summary.csv` is the confirmation summary before ranking. |
| `final_evaluation/final_seed_results.csv`, `statistical_analysis/*` | As for CICIDS2017. No T14/T18/T19 tables were uploaded for UNSW-NB15. |

## Derived from the prediction archives (`*/derived_from_archives/`)

Produced by `src/evaluation/archive_summary.py` and regenerated by `scripts/reproduce_final_statistics.py --archives DIR`.

| File | Columns |
|---|---|
| `final_evaluation/derived_from_archives/run_summary_final_test.csv` and `model_selection/derived_from_archives/run_summary_development.csv` | One row per archive. The columns fall into these groups:<br>• identity: `archive_file`, `archive_sha256`, `archive_bytes`, `dataset`, `role`, `model`, `seed`, `config_hash`, `run_hash`, `n_rows`, `n_attack_rows`;<br>• integrity: `threshold_unique_values`, `prediction_rule_consistent` (y_pred = error > threshold), `row_id_unique`, `n_fingerprints_with_varying_prediction`;<br>• the 15 frozen metric columns;<br>• fingerprint level: `n_fingerprints`, `n_mixed_label_fingerprints`, `n_attack_fingerprints`, `recall_per_attack_fingerprint`, `n_benign_fingerprints`, `fpr_per_benign_fingerprint`, `n_attack_fingerprints_with_several_families`, `attack_rows_in_several_family_fingerprints`, `largest_fingerprint_group_rows`, `largest_fingerprint_group_families`;<br>• score geometry: `benign_median_error`, `missed_attack_median_error_over_threshold`, `missed_attack_p90_error_over_threshold`, `attack_share_below_benign_median`, `attack_share_at_or_below_threshold`;<br>• mixed-label groups: `MCC_excluding_mixed_label_groups`, `mixed_label_rows`, `mixed_label_attack_rows`, `mixed_label_attack_rows_detected`. |
| `final_evaluation/derived_from_archives/family_detection_final_test.csv` | Per run × attack family: `rows`, `detected_rows`, `fingerprints` (distinct fingerprints carrying that family), `detected_fingerprints`. |
| `fingerprints/derived_from_archives/mixed_label_group_composition.csv` | Every mixed-label group: `rows`, `benign_rows`, `attack_rows`, `attack_families`, `role`. It is identical in every development archive; for CICIDS2017 it also equals `attack_allocation_manifest.json`. |
| `../external_artifacts/prediction_archive_manifest.csv` | File name, SHA-256, size, rows, dataset, role, model, seed, config and run hash of each of the 36 archives. |

## Environment records

`artifacts/environment_records/environment.json` and `environment_stage.json` give the Python and library versions of two Colab executions on 15 September 2026. The files do not name the dataset they belong to.
