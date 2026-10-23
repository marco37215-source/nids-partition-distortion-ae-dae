# Study design (Experiment 1 v2)

This is a summary for repository users. The manuscript (`manuscript/manuscript_jisa.tex`, Section 3, and Supplementary S1) is the authoritative description; section numbers below refer to manuscript.

## Research questions

1. Do raw row counts and model-view support coincide in CICIDS2017 and UNSW-NB15? (Section 4.1)
2. Does fingerprint-group atomicity, which removes overlap of identical model inputs between roles, also give structurally comparable roles? (Sections 4.2–4.5)
3. Under partitions that pass the structural audit, how do a selected DAE and a selected AE compare on known attacks within each corpus? (Section 4.7)

## Scope

* Within-dataset, binary (benign versus attack) and reconstruction-based. The two corpora are independent replications under one frozen protocol; no model, preprocessing object or threshold is transferred between them.
* Known, documented attacks only. No zero-day, unseen-family, cross-dataset, deployment or multiclass claim is made.
* Contrasts are within a corpus, ΔM = M(DAE) − M(AE). Absolute levels are not compared between corpora.

## Identity and fingerprints (Section 3.3)

* `row_id` = `<dataset>::<source file>::<10-digit source row>`. It identifies one immutable source record.
* `feature_fingerprint` (`h128:` + 32 hex characters) identifies the equivalence class of rows that are identical under the frozen, ordered, raw model view. Multiplicity *m_f* is the number of rows that share a fingerprint.
* The model view comprises 78 numerical features for CICIDS2017. For UNSW-NB15 it comprises 38 numerical features plus `proto`, `state` and `service`; `srcip`, `dstip`, `sport`, `dsport`, `Stime`, `Ltime`, the label and the attack-category fields are excluded.
* Tests: `tests/test_preprocessing_fit_scope.py` checks that the fingerprinted column order equals the model-input order. Note also the effective-bit property of the CICIDS2017 fingerprints described in `docs/LIMITATIONS.md`.

## Five experimental roles (Section 3.1)

| Role | Composition | Permitted influence |
|---|---|---|
| `benign_weight_train` | benign only | model weights, every learned preprocessing parameter |
| `benign_early_stop` | benign only | early stopping, LR-scheduler signal, best-checkpoint choice |
| `benign_threshold_calibration` | benign only | the run's threshold, T = Q0.99 of its calibration errors |
| `development` | benign and attack | configuration selection, confirmation, sensitivity analyses |
| `final_test` | benign and attack | single sealed final evaluation |

The governance-only `attack_reserve_unused` state holds pure-attack groups that could not be placed without breaking the benign-majority constraint. It was populated for CICIDS2017 only, with 11,657 singleton groups.

## Partitioning (Sections 3.5–3.6)

* **Atomicity.** Every group sits whole in one membership state. Mixed-label groups never enter benign-only roles, and in both corpora every mixed-label group was assigned to `development`.
* **Nominal benign shares.** 50 / 10 / 15 / 10 / 15 % across the five roles. Development and final test must remain benign-majority, with attack prevalence at most 0.49.
* **Structural audit.** The audit covers fingerprint overlap, role purity and accounting, source-file composition, and the multiplicity distribution over eight bands (1, 2, 3–4, 5–9, 10–19, 20–49, 50–99, ≥100). The multiplicity distribution is compared with the pure-benign pool by total-variation distance, TV_r = ½ Σ_b |p_rb − p_b|. A benign quantile-transfer gate completes the audit.
* **UNSW-NB15 history.** The corpus went through three allocation regimes:
  * the initial atomic allocation, which failed;
  * the source-balanced allocation, which failed: the gate FAILed with development-benign exceedance 53.63% and TV 0.7094;
  * the source- and multiplicity-aware MILP allocation v3.4 (HiGHS through SciPy 1.16.3), which passed: exceedance 1.0024% and TV ≈ 0.00015.

  The v3.4 amendment was frozen before the new membership existed. It reallocated pure-benign groups only, and it carried a stopping rule.
* **CICIDS2017** was not amended. It passed 20 hard integrity checks, and its benign transfer was checked retrospectively.

## Preprocessing (Section 3.7)

Preprocessing was fitted on `benign_weight_train` only and applied unchanged to all roles.

* **CICIDS2017** (78 dimensions): infinite values set to missing, median imputation, standardisation.
* **UNSW-NB15** (79 dimensions): the 38 numerical inputs receive structural-missing normalisation, median imputation and standardisation. The three categorical inputs are one-hot encoded with a vocabulary learned from the training role only, with rare, missing and unknown tokens.

## Models, search and selection (Section 3.9)

* **Architectures.** A, B and C are symmetric, fully connected autoencoders with ReLU hidden layers and a linear output. B is p → 64 → 32 → z → 32 → 64 → p. `src/models/architecture.py` reproduces the recorded parameter counts of all twelve confirmation candidates.
* **Training.** AdamW, at most 150 epochs, early-stopping patience 12, gradient clipping at 1.0.
* **DAE corruption.** Numerical masking in both corpora. UNSW-NB15 adds grouped categorical masking.
* **Search.** 20 Optuna configurations per corpus and model type, trained with seed 101. The top three were confirmed at seeds 101, 202 and 303.
* **Selection hierarchy.**
  1. Mean development MCC, descending.
  2. Mean FPR, ascending.
  3. Mean PR-AUC, descending.
  4. MCC SD, ascending.
  5. Parameter count, ascending.
  6. Training time, ascending.

  Family metrics were not used. `scripts/reproduce_final_statistics.py` recomputes the ranking from the confirmation seeds.

## Final evaluation and statistics (Section 3.10)

* **Seeds.** Five common final seeds (101, 202, 303, 404, 505). Seeds 101–303 are shared with confirmation.
* **Score and threshold.** The score is the mean squared reconstruction error over the transformed dimensions. A row is flagged when its score is strictly greater than the run's threshold.
* **Metrics.** MCC, recall, F1, precision, PR-AUC (trapezoidal area under the PR curve), FPR, FP per 1,000 benign, and balanced accuracy.
* **Paired contrasts.** For each pair of runs on the same seed, the summaries are:
  * the mean paired difference;
  * sign consistency across seeds;
  * d_z = mean / SD of the paired differences;
  * a 95% percentile bootstrap interval over seed pairs. With five pairs, the 3,125 ordered resamples are enumerated exactly. This repository's 10,000-resample Monte-Carlo bootstrap (seed 2026) gives the same limits to six decimals for every bound but one.
* **Limits of inference with five pairs.** Exact sign and signed-rank tests cannot reach p < 0.0625. A percentile interval excludes zero by construction whenever all five differences share a sign.

## Stage map: notebook → artefacts in this repository

| Stage (Colab notebook) | Frozen artefacts here |
|---|---|
| PRE-00 governance, model view, fingerprints | `artifacts/*/fingerprints/fingerprint_audit.json`, `duplicate_group_manifest.csv` (UNSW-NB15), `conflicting_fingerprint_manifest.csv` (CICIDS2017), `row_modelview_group_mapping_first100k.csv`, `artifacts/cicids2017/provenance/prepartition_readiness_report.json` |
| PRE-01 partitioning | `artifacts/*/partition/**` (policies, integrity reports, gates, membership first-100k rows, amendment, solver manifests) |
| PRE-02 preprocessing and benign smoke gate | `artifacts/cicids2017/preprocessing/preprocessing_handoff_manifest.json`; UNSW-NB15 smoke manifests, diagnostics, quantile ladder |
| NB-01/02 search, NB-03 confirmation | `artifacts/*/model_selection/**` |
| NB-04 matched ablation, NB-05/06 sensitivity | not in the evidence set used here |
| NB-07 final evaluation | `artifacts/*/final_evaluation/final_seed_results.csv`; prediction archives (external) |
| NB-08 statistical analysis | `artifacts/*/statistical_analysis/**` |
