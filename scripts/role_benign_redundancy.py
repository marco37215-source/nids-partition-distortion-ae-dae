"""Retrospective benign redundancy of the evaluation roles (development, final test), both corpora.

Added in revision. Reads the per-run summaries that were derived from the observation-level prediction
archives (one row per archive; every archive of a role covers the same rows, which the script checks)
and reports, per dataset and role:
  benign rows = n_rows - n_attack_rows (includes benign members of mixed-label groups),
  distinct benign fingerprints = n_benign_fingerprints,
  benign redundancy rate = (benign rows - distinct benign fingerprints) / benign rows.

This is a redundancy-rate audit only. The full multiplicity-band profile of the CICIDS2017 roles cannot be
reconstructed from the retained evidence, because complete role membership by fingerprint is not deposited.

Usage: python scripts/role_benign_redundancy.py [--repo .]
Output: results/role_redundancy/role_benign_redundancy.csv
"""
import argparse
from pathlib import Path

import pandas as pd

FILES = {
    "development": "model_selection/derived_from_archives/run_summary_development.csv",
    "final_test": "final_evaluation/derived_from_archives/run_summary_final_test.csv",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    a = ap.parse_args()
    repo = Path(a.repo)
    rows = []
    for ds in ("cicids2017", "unsw_nb15"):
        for role, rel in FILES.items():
            d = pd.read_csv(repo / "artifacts" / ds / rel)
            cols = ["n_rows", "n_attack_rows", "n_benign_fingerprints", "n_fingerprints", "n_mixed_label_fingerprints"]
            assert (d[cols].nunique() == 1).all(), f"{ds}/{role}: archives disagree on role composition"
            x = d.iloc[0]
            benign = int(x.n_rows - x.n_attack_rows)
            fps = int(x.n_benign_fingerprints)
            rows.append(dict(dataset=ds, role=role, archives=len(d), benign_rows=benign,
                             distinct_benign_fingerprints=fps,
                             benign_redundancy_rate=(benign - fps) / benign,
                             mixed_label_fingerprints=int(x.n_mixed_label_fingerprints),
                             largest_group_rows=int(x.largest_fingerprint_group_rows)))
    out = repo / "results" / "role_redundancy"
    out.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(out / "role_benign_redundancy.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
