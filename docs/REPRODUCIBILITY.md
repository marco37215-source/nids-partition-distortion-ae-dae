# Reproducibility

## 1. Environment

| Component | Version used to verify this repository | Version recorded by the Colab analysis (`artifacts/environment_records/`) |
|---|---|---|
| Python | 3.13.16 (Linux) | 3.13.15 (Linux, Colab) |
| numpy | 2.1.3 | 2.1.3 |
| pandas | 2.2.3 | 2.2.3 |
| scipy | 1.16.3 | 1.16.3 |
| scikit-learn | 1.6.1 | 1.6.1 |
| matplotlib | 3.10.0 | 3.10.0 |
| pytest | 8.3.5 | — |
| torch, optuna, pyarrow, joblib | not needed | 2.11.0+cu128, 4.9.0, 23.0.1, 1.6.0 (notebooks only; `requirements-notebooks.txt`) |

Create the environment with:

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The scripts use no GPU, no network access and no random numbers. The only randomised step is the comparison Monte-Carlo bootstrap, which uses `numpy.random.default_rng(2026)`. Outputs are therefore identical on every run.

## 2. Level 1 — repository only

```bash
python scripts/reproduce_all.py
pytest
```

`reproduce_all.py` runs the five scripts in order. Each script writes its tables to `results/tables/`, its figure data to `results/figure_source_data/`, and its comparisons to `results/claims_check/<script>.csv`. `reproduce_figures.py` writes the figures to `results/figures/`.

| Script | What it recomputes | Main inputs |
|---|---|---|
| `reproduce_fingerprints.py` | Table 6 and Section 4.1 (redundancy, pure-benign reconciliation, error floors, expected cross-side sharing, tie-break keys) | fingerprint audits, duplicate manifest, v3.4 gate, allocation manifest, mixed-group composition |
| `reproduce_partitions.py` | Tables 7, 8, S2 and Sections 4.2, 4.5, 4.6 (TV distances, gates, solver status, provenance hash chain, CICIDS2017 integrity) | UNSW-NB15 gate tables and manifests, source-balanced fingerprint summary, CICIDS2017 integrity report |
| `reproduce_transfer_analysis.py` | Sections 4.3–4.5 and Figs. 5–7 data (exceedances, band and group false-positive rates, CT-7 diagnostics, quantile ladder) | smoke manifests, 00C/00D diagnostics, fingerprint summary, ladder |
| `reproduce_final_statistics.py` | Tables 9, 10, S3 and Section 4.7 (selection ranking, levels, paired contrasts, tests, per-fingerprint recall, score geometry, development versus final) | selection manifests, confirmation and final seed results, NB-08 tables, archive-derived summaries |
| `reproduce_figures.py` | Figs. 4–8 (PNG at 300 dpi and PDF) | `results/figure_source_data/*.csv` |

A check passes when the recomputed value lies within half a unit of the last decimal place printed in the manuscript. Integer counts must match exactly. A check that cannot be made is recorded as a **note** with the status `NOT_REPRODUCIBLE_HERE`, `FROZEN_TABLE_DISCREPANCY`, `CORRECTION_NEEDED` or `INFO`; a note is never counted as a pass.

Verified result on 19 October 2026, from a fresh copy in a new virtual environment built from `requirements.txt`: 462 checks passed, 0 failed, 14 notes. `pytest` gave 82 passed and 15 skipped. The skipped tests are 4 that need the archives and 11 that verify contract files not yet copied into `configs/`.

### Level 1 in Google Colab

`notebooks/reproduction/` holds a self-contained Colab notebook for every `.py` file (R00 runs them all). They were executed end to end on 20 October 2026 from a fresh copy whose `results/` folder had been deleted. They produced every file in `results/` byte-identical to the script outputs: 462 checks passed, and the notebook test runner gave 82 passed and 15 skipped. In archive mode, R04 gave 311 passing checks (0 failed) and the test runner gave no failures. Instructions are in `notebooks/reproduction/README.md`.

## 3. Level 2 — with the prediction archives

Download the 36 archives (see `external_artifacts/README.md`) into one folder, then run:

```bash
python scripts/reproduce_all.py --archives /path/to/archives --workers 2
pytest --archives=/path/to/archives        # or: export NIDS_PREDICTION_ARCHIVES=/path/to/archives
```

`reproduce_final_statistics.py --archives` does three things:

1. It summarises every archive with `src/evaluation/archive_summary.py`. For each archive this covers:
   * the integrity flags;
   * the confusion matrix and all 11 frozen metrics;
   * fingerprint-level recall and FPR;
   * the score geometry;
   * per-family detection counts;
   * the mixed-group composition.
2. It compares every regenerated table with the committed tables under `artifacts/*/*/derived_from_archives/` and `external_artifacts/prediction_archive_manifest.csv`. Numerical columns must agree to 1e-12; text columns must agree exactly.
3. It checks the SHA-256 of every archive against the manifest.

Verified on 19 October 2026: 472 checks passed, 0 failed (log: `results/claims_check/reproduce_final_statistics__with_archives.csv`). With the archives, `pytest --archives=DIR` gave 86 passed and 11 skipped (the contract-file tests). It additionally checks that every run of a role scored the identical row-to-fingerprint assignment and that development and final-test fingerprints are disjoint.

The archive-derived metrics also equal the frozen NB-07 table (`final_seed_results.csv`) for all 20 final runs, and the frozen NB-03 table (`confirmation_seed_results.csv`) for all 16 development runs. Thresholds and confusion counts agree exactly. Floating-point metrics agree to within 6 × 10⁻¹⁵, i.e. in the last stored digit.

## 4. Level 3 — re-running the pipeline

The Colab notebooks (`notebooks/README.md`) produced every artefact here from the raw corpora. Re-running them needs:

* the raw files listed in `data/*/source_manifest.csv`;
* the frozen contracts (`configs/README.md`);
* Google Drive paths of the form `/content/drive/MyDrive/EXPERIMENT1_V2/...`;
* a CUDA GPU for training.

Two checks link a re-run to this repository. First, the merged master's SHA-256 must equal the value in `data/*/SHA256SUMS.txt`. Second, re-run outputs can be compared with the frozen artefacts using the hash conventions in `src/utils/hashing.py`:

* `config_hash` is the SHA-256 of the canonical JSON of `effective_config`;
* a manifest self-hash is the canonical JSON of the manifest without its hash field and without `created_at_utc`.

Training on GPU is not bit-for-bit deterministic in general. Exact agreement of re-trained models with the archives is therefore not expected, even though the archives record the seeds used.

## 5. Practical notes

* Prediction archives are read with pandas' default C float parser, the parser with which the frozen metrics were reproduced. Committed tables are read with `float_precision="round_trip"`, so that they compare exactly.
* Every `read_csv` of a frozen artefact goes through `src/utils/io_utils.py`.
* Running `reproduce_all.py` overwrites `results/`. The committed `results/` is exactly what the scripts produce, so `git status` should show no change after a run. The only exception is `results/claims_check/reproduce_final_statistics.csv`, which gains 10 extra rows in archive mode; restore it with `git checkout results/claims_check/reproduce_final_statistics.csv`.
* `results/archive_recomputation/` (written in archive mode) is git-ignored.
