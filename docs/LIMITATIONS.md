# Limitations

This file has three parts:

1. What this repository cannot reproduce.
2. The scientific limitations stated in the manuscript, summarised so that repository users do not over-read the results.
3. Corrections identified while reproducing every number, with the evidence and suggested wording.

## 1. Limits of the evidence in this repository

### Pipeline stages that are not re-run

These stages need the raw corpora, the authors' Colab notebooks and, for training, a GPU:

* model-view fingerprint hashing (PRE-00);
* partition construction, including the MILP (PRE-01);
* preprocessing fit (PRE-02);
* model search, training and scoring (NB-01–NB-07).

The repository checks their recorded outputs instead. The scripts recompute the counts, gates, hashes and statistics from those outputs, and the tests check internal consistency.

### Values that come from the analysis record only

No artefact in the evidence set supports the following values. They are labelled in the tables and figures and flagged `NOT_REPRODUCIBLE_HERE` in `results/claims_check/`:

| Value | Where | Why it cannot be recomputed |
|---|---|---|
| 99.22% initial-allocation development-benign exceedance | Abstract; Sections 4.3 and 4.5; Table 8; Fig. 6 | No manifest was retained for the initial allocation (`artifacts/unsw_nb15/partition/initial_atomic/README.md`) |
| Full-record duplicates 480,633 (and 480,632), 568,843; the 42,552 difference | Abstract; Section 4.1; Table 6 | Requires the raw master CSV |
| Singleton shares of four roles in the source-balanced allocation (100.00 / 47.49 / 96.09 / 95.23%) and their ≥100 shares | Table 7 | Source-balanced membership not in the evidence set. Only the development and pool rows are recomputed. |
| Multiplicity-only feasibility bound 3.94 × 10⁻⁶ | Section 4.2 | Feasibility audit not in the evidence set |
| Frozen-record TV 0.000149 | Abstract; Section 4.5 | The gate table recomputes to 0.000150 (0.0001498), as the manuscript already states |
| Redundancy rates of the three benign-only v3.4 roles (12.583 / 12.666 / 12.521%) | Section 4.5 | Per-role group counts outside the ≥100 band not in the evidence set |
| UNSW-NB15 source attack prevalence range 3.17–22.49% | Section 4.3 | Per-source attack counts not in the evidence set |
| CICIDS2017 retrospective transfer check: 1.0001%, 0.9186% and eight quantile ratios | Section 4.6; Fig. 7b | Calibration and development scores of the search-stage AE not retained |
| CICIDS2017 early-stopping role: 55,372 distinct vectors (75.64% redundant) | Section 4.6 | Full membership not in the evidence set |
| Matched-ablation contrasts (−0.004998, +0.001036, d_z −0.155; +0.010377, d_z 1.755) | Section 4.7 | NB-04 outputs not in the evidence set |
| Threshold and hyperparameter sensitivity analyses | Methods | NB-05 and NB-06 outputs not in the evidence set |
| McNemar tests | Methods | Per-seed test outputs not in the evidence set; the paired predictions in the archives would allow them, but no reported value exists to check against |

### Other limits of the evidence

* **Truncated samples.** The membership and row-mapping files hold only their first 100,000 rows. Checks on them (no fingerprint crossing, role purity, agreement between files) are sample checks; the full-population statements rest on the frozen integrity reports and, with the archives, on the development/final-test disjointness test.
* **Missing contract files.** The five protocol contracts and several policies (feature, taxonomy, preprocessing, the base UNSW-NB15 partition policy) are recorded only by their hashes. `configs/README.md` explains how to add them; `tests/test_configs.py` then verifies them.

## 2. Scientific limitations (summary of the manuscript, Section 5)

* **Number of seeds.** There are five seed pairs per corpus. Exact sign and signed-rank tests cannot reach p < 0.0625, and a percentile bootstrap interval excludes zero whenever all five differences share a sign. Seeds 101–303 were also used for confirmation, so the final estimates are not independent of selection at the seed level.
* **Confounding in the multiplicity gradient.** The false-positive gradient by multiplicity (Fig. 5) was measured in one allocation, in which multiplicity was confounded with role: weight training held no repeated benign vector. It is an association, not a causal effect, and every row in that analysis is benign.
* **The gate is not independent validation.** The benign transfer gate that v3.4 passed is the diagnostic that motivated the amendment. It compares calibration with development under one diagnostic model and does not examine the early-stopping role.
* **The CICIDS2017 boundary condition is weaker evidence.** It rests on a retrospective check of a search-stage model, not on a prospective gate.
* **Fingerprints capture exact duplication only.** Near-duplicate, session, host and temporal dependence are not captured. Fingerprint counts are not effective sample sizes.
* **The AE–DAE contrasts do not isolate denoising.** They compare independently selected configurations. The UNSW-NB15 AE stopped at a mean best epoch of 149.0 out of 150, so its contrast may include a training-budget component.
* **Prevalence is fixed by design.** Precision, F1, MCC and PR-AUC depend on the attack prevalence of the evaluation roles, which the partition design fixed. It is not an operational base rate.
* **Scope.** No zero-day, cross-dataset, deployment or covariate-shift claim is made.

## 3. Corrections identified during reproduction

Each item is recorded in `results/claims_check/*.csv` with the status `CORRECTION_NEEDED` or `FROZEN_TABLE_DISCREPANCY`. The manuscript files in `manuscript/` are kept as prepared (v4); apply the corrections there before submission.

### 3.1 CICIDS2017 fingerprints have 64 effective bits, not 128

**Evidence.**

* In every CICIDS2017 fingerprint in the membership and mapping files, and in all 589,082 distinct fingerprints of a final-test archive, the first 16 hexadecimal digits equal the last 16. No UNSW-NB15 fingerprint in the membership sample has this property.
* `pandas.util.hash_pandas_object` applies `hash_key` only to object (string) columns. The CICIDS2017 model view is entirely numerical, so the two "independently keyed" 64-bit hashes are identical. `tests/test_fingerprint_determinism.py` demonstrates this.

**Consequence.** The fingerprint audit's `effective_candidate_bits: 128` and the manuscript text overstate the key length for CICIDS2017. **The group counts are unaffected**, for two reasons:

* every candidate group was verified by byte-level equality of the canonical raw values;
* a 64-bit key can only merge distinct vectors, which that verification would have split. The audit records zero resolved collisions, and the expected number of 64-bit collisions among 2,521,664 distinct vectors is about 1.7 × 10⁻⁷.

**Where.** Methods, Section 3.3 ("a deterministic, versioned hash of 128 effective bits") and Supplementary S1 ("In both executions … giving 128 effective bits").

**Suggested wording (S1):** "For UNSW-NB15 the two keyed 64-bit row hashes differ and the candidate key has 128 effective bits. For CICIDS2017, whose model view is entirely numerical, the row hash does not use the key, so the two halves coincide and the candidate key has 64 effective bits. Because every candidate group was confirmed by byte-level equality of the canonical raw values, and no collision occurred, the group counts do not depend on the key length."

### 3.2 Two bounds of the frozen NB-08 bootstrap table are inconsistent with the paired values

**Evidence.** The exact enumeration of all 3,125 resamples of the frozen `paired_seed_values.csv` reproduces every frozen interval bound to six decimals except two:

* UNSW-NB15 precision lower bound: −0.001263, against −0.001201 frozen;
* UNSW-NB15 FP/1,000 upper bound: +0.733, against +0.709 frozen. The frozen value is also inconsistent with the frozen FPR bound of +0.000733.

The frozen precision upper bound also differs, by 3.8 × 10⁻⁷, which does not change its printed value.

**Status.** Both are already corrected in Table 10 (notes 1–2). For precision, the note attributes the recomputation to the prediction archives; the frozen paired values give the same −0.001263.

**Suggested wording (Table 10 caption):** "Intervals are 95% percentile intervals of the exact paired bootstrap distribution over seed pairs (all 3,125 ordered resamples)." This matches what Table 10 reports. This repository's 10,000-resample Monte-Carlo bootstrap gives the same bounds except the CICIDS2017 PR-AUC upper bound (−0.007701, against −0.007694).

### 3.3 Six UNSW-NB15 development archives carry a different run hash

**Evidence.** For the six seed-101 development archives of UNSW-NB15 (all three AE and all three DAE confirmation candidates), the stored `run_hash` differs from the `run_hash` in `confirmation_seed_results.csv`. All 15 metric columns and the threshold nevertheless agree exactly. Run hashes agree for all 20 final-test archives and all 6 CICIDS2017 development archives. The cause is not recorded; one possibility, not verified, is that these archives were written by the search-stage run of the same configuration and seed.

**Where.** Supplementary S1, "Each archive was matched to its model, seed and configuration by its stored configuration and run hashes."

**Suggested wording:** "Each archive was matched by its configuration hash and seed. The stored run hash agreed with the corresponding results table for every final-test archive and every CICIDS2017 development archive. It differed for the six UNSW-NB15 seed-101 development archives, whose metrics nevertheless reproduced the confirmation table exactly."

### 3.4 UNSW-NB15 attack fingerprints that carry several attack families

**Evidence.** In the UNSW-NB15 final test, 1,283 of the 46,798 distinct attack fingerprints (24,312 rows) carry more than one attack-family label. As a result, the per-family vector counts of Table S3 sum to 52,792. CICIDS2017 has no such fingerprint.

**Consequence.** The Table S3 vector columns overlap across families, and "share of distinct attack vectors" figures must use the 46,798 total as denominator, as the manuscript does for Generic (24.2%).

**Suggested wording (Table S3 note):** "In UNSW-NB15, 1,283 distinct attack vectors (24,312 rows) carry more than one family label and are counted under each, so the vector column sums to more than the 46,798 distinct attack vectors."

### 3.5 Rounding

The UNSW-NB15 DAE final-minus-development MCC at the confirmation seeds is 0.0040736. Section 4.7 prints +0.004073; it should be **+0.004074**.
