# Configurations and frozen contracts

Experiment 1 v2 was governed by a set of frozen JSON contracts and policies, written before the stage they govern. Every downstream manifest records their SHA-256, so any copy can be checked against the run that used it.

## Included here

These are byte-for-byte copies of frozen artefacts. `tests/test_configs.py` checks that each copy is identical to its artefact.

| File | Copy of | What it fixes |
|---|---|---|
| `cicids2017/partition_policy.json` | `artifacts/cicids2017/partition/partition_policy_manifest.json` | Benign shares, the prevalence cap, the 10-step priority order, the tie-breaking rule, the partition seed 20260914 and the preprocessing hand-off rule |
| `unsw_nb15/multiplicity_policy.json` | `artifacts/unsw_nb15/partition/final_source_multiplicity_balanced/source_multiplicity_amendment.json` | Eight bands, the tolerances, exempt source × band cells, the >400-row weight-training rule and the stopping rule |
| `cicids2017/selected_models.json`, `unsw_nb15/selected_models.json` | `artifacts/*/model_selection/selected_models_manifest.json` | The selected AE and DAE `effective_config` blocks |


## Contract files
| `artifact_contract.json` | `066d18e1991f` |
| `metric_contract.json` | `0143747db518` |
| `model_search_contract.json` | `a18e50927764` |
| `seed_schedule.json` | `e9c16b79cfb3` |
| `threshold_contract.json` | `72ce1b512a8f` |
| `experiment_protocol.json` (global protocol) | `55713fd82c01` |
| `cicids2017/feature_policy.json` (raw feature policy) | `3cae0d0bb613` |
| `cicids2017/taxonomy_policy.json` | `e4290a4c91d6` |
| `cicids2017/row_identity_specification.json` | `75d07ee35961` |
| `cicids2017/preprocessing_policy.json` | `2a2096b1d219` |
| `unsw_nb15/preprocessing_policy.json` (v3.4 refit) | `610c536ba782` |
| `unsw_nb15/feature_policy.json`, `taxonomy_policy.json`, `partition_policy.json` | no hash in the evidence set; copy them for completeness |

Full 64-digit hashes are in `EXPECTED_HASHES.csv`.

