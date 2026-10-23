# Frozen artefacts

This folder holds the outputs of the Experiment 1 v2 Colab notebooks that support the manuscript, together with tables derived from the prediction archives for this repository.

* **Integrity.** Every frozen file is a byte-identical copy of the notebook output. `ARTIFACT_PROVENANCE.csv` gives each file's upload name, status, row count, size and SHA-256; `tests/test_manifest_hashes.py::test_artifact_provenance_checksums` re-checks them.
* **File names.** Upload prefixes were removed and suffixes such as `__1_` replaced by descriptive names. The JSON contents are untouched; they contain their own hashes, and changing even one byte would break the record.
* **Samples.** `*_first100k.csv` files hold the **first 100,000 rows** of much larger files (full membership and row mapping). Use them for sample-level checks only.
* **Derived tables.** `derived_from_archives/` folders contain tables computed for this repository from the 36 prediction archives by `src/evaluation/archive_summary.py`. They are reproducible with `scripts/reproduce_final_statistics.py --archives DIR`.

```
artifacts/
  ARTIFACT_PROVENANCE.csv
  environment_records/        Colab library versions (the dataset is not recorded in the files)
  cicids2017/
    provenance/               PRE-00 readiness report
    fingerprints/             fingerprint audit, mixed-label manifest, row mapping (first 100k)
    partition/                policy, integrity report, allocation manifests and tables, membership (first 100k)
    preprocessing/            PRE-01 -> PRE-02 hand-off (fit scope)
    model_selection/          selected models, top-three configs, ranking, confirmation seeds (+ derived development summaries)
    final_evaluation/         NB-07 five-seed results (+ derived final-test summaries and family counts)
    statistical_analysis/     NB-08 paired values, bootstrap effects, T14/T18/T19
  unsw_nb15/
    provenance/               raw 49-column schema
    fingerprints/             fingerprint audit, same-label duplicate manifest, row mapping (first 100k)
    partition/
      initial_atomic/                       nothing retained (README)
      source_balanced/                      FAIL smoke gate, 00C/00D diagnostics, fingerprint-level development summary
      final_source_multiplicity_balanced/   amendment, solver history, v3.4 integrity report, gates, PASS smoke gate, ladder
    preprocessing/            README only (fit-scope evidence is in the smoke manifests)
    model_selection/  final_evaluation/  statistical_analysis/
```

The meaning of every file and column is given in `docs/ARTIFACT_DICTIONARY.md`, and the provenance chain in `docs/DATA_PROVENANCE.md`.
