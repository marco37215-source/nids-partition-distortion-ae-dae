# UNSW-NB15 partition lineage: what was executed and what was retained

This document lists the three UNSW-NB15 allocation regimes in order, with the evidence for each that survives in this repository.

Nothing here is reconstructed. No reimplementation of the initial or source-balanced allocator is provided. If one is ever added, it must be labelled a *reference reimplementation*, never the executed allocator.

The hashes below are copied from the frozen artefacts named in each entry.

## 1. Initial fingerprint-atomic allocation

| Item | Status |
|---|---|
| Membership file, allocator code, diagnostic manifest | **Not retained** |
| Retained evidence | Development-benign exceedance of 99.22%, from the analysis record only. This value is carried as a constant in `notebooks/reproduction/R02_Partition_Structure.ipynb` and `R03_Benign_Transfer_Analysis.ipynb`. |
| Outcome | Passed the overlap and purity audits; failed audits 3–5 |

## 2. Source-balanced allocation

| Item | Value | Source |
|---|---|---|
| Membership file SHA-256 | `3114e887aeff514be147d68a9f938d9c889d2c89a21a1ccffd6ff65fcb4a4fac` | `artifacts/unsw_nb15/partition/preformal_benign_score_smoke/smoke_fa6c777e7dfc7b7c/smoke_manifest.json` (same as `source_balanced/smoke_manifest_source_balanced.json`). It also appears as `parent_membership_sha256` in the v3 amendment. |
| Benign transfer gate | FAIL. Development-benign exceedance 0.5362635; calibration 0.0100026 | same manifest |
| Diagnostic model | `checkpoint.pt` and `training_history.csv` | `preformal_benign_score_smoke/smoke_fa6c777e7dfc7b7c/` |
| Role multiplicity profile | Development profile recomputed from `development_benign_fingerprint_level_summary.csv`. Other roles taken from the analysis record (Additional file 1, Table S8). | `results/tables/Table_3_2b_source_balanced_profile.csv` |
| Further diagnostics | Block decomposition (00C); mixed-label comparison (00D) | `artifacts/unsw_nb15/partition/source_balanced/` and `preformal_*_diagnostic/` |
| Allocator code | **Not retained in reconstructable form** | – |

## 3. Source- and multiplicity-aware allocation (version 3.4, accepted)

| Item | Value | Source |
|---|---|---|
| Amendment | `UNSW_PRE01_V3_SOURCE_MULTIPLICITY_20260919`, frozen before the membership was generated | `final_source_multiplicity_balanced/source_multiplicity_amendment.json` |
| Scientific policy hash | `17122c41630be246c40d9018a97d6f80b58d7422f438673594acb74fd4d2d3fb`, unchanged across v3.1–v3.4 | amendment and `implementation_fix_v3_*.json` |
| Partition seed | 20260914 | amendment |
| Implementations | v3.1 `milp` → v3.2 `decomposed_milp` → v3.3 `coordinated_feasibility` → v3.4 `singleton_tolerance_fix` (accepted) | `implementation_fix_v3_1.json` … `_v3_4.json` |
| Executed notebook | `PRE_01_UNSW_NB15_Source_Multiplicity_Stratified_Partitioning_V3_4_SINGLETON_TOLERANCE_FIX (1).ipynb` | `notebooks/unsw_nb15/` |
| Membership file SHA-256 | `273093382be4d417a7b45c837008b994e57644902dffa1194002d2f2d0f8d6de` | `preformal_benign_quantile_transfer_smoke/smoke_fa5c9d84995261cc/smoke_manifest.json` |
| Benign transfer gate | PASS. Development-benign exceedance 0.0100236; calibration 0.0100026 | same manifest |
| Gates | multiplicity, source, source × multiplicity, highest band, integrity | `final_source_multiplicity_balanced/*.csv`, `partition_integrity_report.json` |

## 4. Post-hoc analyses added in revision (no frozen artefact altered)

- **Splitter baselines.** `scripts/splitter_baselines.py` builds a reference distribution of role multiplicity under standard group splitters. It reads `artifacts/unsw_nb15/fingerprints/duplicate_group_manifest.csv` and writes to `results/splitter_baselines/`.
- **Role benign redundancy.** `scripts/role_benign_redundancy.py` computes the retrospective benign redundancy of the development and final-test roles. It reads the per-run summaries in `artifacts/*/{final_evaluation,model_selection}/derived_from_archives/`, which were derived from the observation-level prediction archives, and writes to `results/role_redundancy/`.
- **Test.** `tests/test_splitter_baselines.py` is a two-seed smoke test of the splitter script.
