# Data provenance

## Source corpora (not redistributed)

| Corpus | Provider and distribution | Files used | Merged master |
|---|---|---|---|
| CICIDS2017 | Canadian Institute for Cybersecurity, University of New Brunswick: the official *MachineLearningCSV* flow-feature files | 8 daily files: `Monday-WorkingHours.pcap_ISCX.csv`, `Tuesday-WorkingHours.pcap_ISCX.csv`, `Wednesday-workingHours.pcap_ISCX.csv`, `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv`, `Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv`, `Friday-WorkingHours-Morning.pcap_ISCX.csv`, `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv`, `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` | 2,830,743 rows (2,273,097 benign, 557,646 attack, 14 attack families); SHA-256 `b68a108f…cabd3` |
| UNSW-NB15 | UNSW Canberra at the Australian Defence Force Academy (Cyber Range Lab) | the four full flow-record files `UNSW-NB15_1.csv` … `UNSW-NB15_4.csv` (not the predefined training/testing subsets) | 2,540,047 rows (2,218,764 benign, 321,283 attack, 9 canonical families); SHA-256 `f0447e75…f9c54` |

The file names above are those that appear in the `row_id` and `source_file` fields of the frozen artefacts. The master SHA-256 values are recorded in `artifacts/*/fingerprints/fingerprint_audit.json` (`master_dataset_sha256`) and repeated in every downstream manifest. Per-source-file hashes and row counts are not part of the evidence set; `data/*/source_manifest.csv` leaves them blank for the authors to complete.

Two label details are kept exactly as they occur in the data:

* the CICIDS2017 web-attack family names contain the Unicode replacement character U+FFFD (`Web Attack � Brute Force`), where the original files hold a cp1252 en dash;
* the UNSW-NB15 alias `Backdoor` was mapped to `Backdoors` by a frozen rule before partitioning.

## How the artefacts were produced

All artefacts were produced in Google Colab by the authors' Experiment 1 v2 notebooks (`notebooks/README.md`); the timestamps in the manifests run from 14 to 22 September 2026. Every stage read only frozen, hashed outputs of earlier stages. The JSON manifests record:

* their upstream hashes;
* the master SHA-256;
* the contract hashes;
* booleans asserting that the final test was not accessed.

`tests/test_manifest_hashes.py` recomputes the self-hashes and checks the cross-references. `scripts/reproduce_partitions.py` checks the UNSW-NB15 hash chain, which runs:

source-balanced membership (`3114e887…`) → 00C/00D diagnostics → frozen amendment (`17122c41…`) → v3.4 membership (`27309338…`) → PASS gate → selection manifest.

Some manifests contain Colab paths of the form `/content/drive/MyDrive/EXPERIMENT1_V2/...`. They are kept unchanged because they are part of the hashed content, and they contain no credentials.

## What was uploaded, and what was done with it

* **Selection of artefacts.** Every artefact in `artifacts/` is a byte-identical copy of a file produced by the notebooks; `artifacts/ARTIFACT_PROVENANCE.csv` gives its upload name, SHA-256 and row count. Exact duplicates among the uploads were removed by SHA-256.
* **First-100,000-row samples.** Files with `first100k` in the name contain the first 100,000 rows of much larger files (the full membership and row-mapping files). They are samples and support only sample-level checks.
* **Excluded duplicate-group manifest.** The uploaded `duplicate_group_manifest_CICIDS.csv` is byte-identical to the UNSW-NB15 manifest (same SHA-256). It was therefore not used. The CICIDS2017 same-label group manifest is not in the evidence set.
* **Derived tables.** Files under `derived_from_archives/` were computed for this repository from the 36 prediction archives by `src/evaluation/archive_summary.py`; `reproduce_final_statistics.py --archives` regenerates them.

## Dataset assignment of ambiguous files

Several uploaded files do not name their dataset. Each was assigned by its content:

| File | Assigned to | Evidence |
|---|---|---|
| `confirmation_seed_results.csv`, `confirmation_summary.csv`, `selection_ranking.csv` (UNSW-NB15 copies) | UNSW-NB15 | 15,519 parameters (p = 79) and config hashes found in the UNSW-NB15 selection manifest |
| `8862b389-confirmation_seed_results.csv` | CICIDS2017 | 15,390 parameters (p = 78) and CICIDS2017 config hashes |
| `T14`, `T18`, `T19` tables | CICIDS2017 | values equal the CICIDS2017 `paired_seed_values.csv` |
| `attack_allocation_manifest.json`, `benign_allocation_table.csv`, `family_allocation_table.csv`, `partition_integrity_report__1_.json`, `preprocessing_handoff_manifest.json`, `prepartition_readiness_report.json`, `conflicting_fingerprint_manifest.csv` | CICIDS2017 | `dataset` field, or CICIDS2017 family names and fingerprints |
| `multiplicity_gate.csv`, the `source_*` gates, `band_ge100_role_report.csv`, `benign_quantile_ladder.csv`, `effective_config.json` | UNSW-NB15 | UNSW-NB15 source-file names; ladder q99 equals the v3.4 smoke threshold; config hash equals the v3.4 smoke manifest |
| `environment.json`, `environment_stage.json` | not assigned | the files do not record a dataset; kept under `artifacts/environment_records/` |

## Prediction archives (external)

There are 36 CSV files (5.04 GB):

* 20 final-test runs (2 corpora × 2 models × 5 seeds);
* 16 development runs:
  * the three confirmation seeds of each selected model (12 runs);
  * seed-101 runs of four non-selected UNSW-NB15 confirmation candidates (4 runs).

Each archive has the columns `row_id, y_true, reconstruction_error, threshold, y_pred, model, seed, config_hash, run_hash, attack_family, feature_fingerprint`. They exceed GitHub's 100 MB file limit and are deposited separately; see `external_artifacts/README.md`.
