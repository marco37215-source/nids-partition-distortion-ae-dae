# Notebooks

* `reproduction/`: Colab versions of every `.py` file in this repository (R00–R07). Use these to reproduce the manuscript's tables, figures and checks; see `reproduction/README.md`.
* `cicids2017/`, `unsw_nb15/`: the original Experiment 1 v2 notebooks, which are described below.

## Original Colab notebooks (to be added by the authors)

The notebooks that produced every artefact in `artifacts/` are kept in the authors' Google Drive and are **not yet in this repository**. Copy them in unchanged, using the names below, so that the repository holds the code of record for the stages it cannot re-run itself.

| File (same name in `cicids2017/` and `unsw_nb15/`) | Stage | Main outputs in this repository |
|---|---|---|
| `PRE_00_Governance_ModelView.ipynb` | Ingestion, `row_id`, raw model view, fingerprints, duplicate audit | `artifacts/*/fingerprints/*`, `artifacts/cicids2017/provenance/*` |
| `PRE_01_Partitioning.ipynb` | Fingerprint-atomic allocation, integrity report; UNSW-NB15 source balancing and the v3 amendment / MILP | `artifacts/*/partition/**` |
| `PRE_02_Preprocessing.ipynb` | Fit on `benign_weight_train` and transform all roles; benign quantile-transfer smoke gate (UNSW-NB15) | `artifacts/cicids2017/preprocessing/*`; UNSW-NB15 smoke manifests and ladder |
| `NB_01_AE_Search.ipynb`, `NB_02_DAE_Search.ipynb` | 20-configuration Optuna searches (seed 101) | top-three candidates |
| `NB_03_MultiSeed_Confirmation.ipynb` | Seeds 101/202/303, ranking, selection | `artifacts/*/model_selection/*`, development prediction archives |
| `NB_04_Matched_Ablation.ipynb` | Selected DAE with corruption disabled | not in the evidence set |
| `NB_05_Threshold_Sensitivity.ipynb`, `NB_06_Hyperparameter_Sensitivity.ipynb` | Sensitivity analyses | not in the evidence set |
| `NB_07_Final_Evaluation.ipynb` | Five final seeds on the sealed `final_test` | `artifacts/*/final_evaluation/final_seed_results.csv`, final prediction archives |
| `NB_08_Statistical_Analysis.ipynb` | Paired contrasts, bootstrap, tests | `artifacts/*/statistical_analysis/*` |

The UNSW-NB15 pre-formal diagnostics (00C block decomposition, 00D mixed-label diagnostic) live in a separate notebook. If so, add it under `unsw_nb15/` with a descriptive name.

The table above follows the notebook names proposed for this repository. If your Drive files are named differently, keep the original names and add a line to this table. The manifests reference stages such as "Notebook 00", "Notebook 01" and "Notebook 07", so a reader should be able to find each stage.


The library versions the notebooks ran with are in `requirements-notebooks.txt` and `artifacts/environment_records/`.
