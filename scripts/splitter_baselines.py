"""Reference distribution of role multiplicity profiles under standard group splitters (UNSW-NB15).

Added in revision. The analysis asks whether the multiplicity distortion observed in the
source-balanced UNSW-NB15 allocation (weight training 100% singleton; development TV 0.7094)
is what ordinary group-aware splitting produces on this corpus, or whether it was specific to
the allocator used in the study.

Input  : artifacts/unsw_nb15/fingerprints/duplicate_group_manifest.csv  (frozen; pure-benign groups
         have binary_label_max == 0) plus the 1,882,245 pure-benign singleton fingerprints recorded
         in the accepted multiplicity gate. Together: 1,938,413 groups covering 2,217,778 rows.
Output : results/splitter_baselines/splitter_runs.csv     one line per allocator x seed x role
         results/splitter_baselines/splitter_summary.csv  per allocator and role
         results/splitter_baselines/splitter_max_tv.csv   maximum-over-roles TV per allocator

No model is trained and no label other than the benign/attack flag of the manifest is read.
Source-file composition is not simulated, because the manifest carries no per-group source file.

Allocators (role shares 50/10/15/10/15 for weight_train, early_stop, calibration, development, final_test):
  A  independent random assignment of each group to a role with the role shares as probabilities;
  B  random permutation of groups, cut where the cumulative row share reaches each role boundary;
  C  random permutation of groups, cut by group count (the semantics of a GroupShuffleSplit-type split);
  D  scikit-learn GroupKFold with 20 folds mapped to roles 10/2/3/2/3 (deterministic; one run).

Usage: python scripts/splitter_baselines.py [--seeds 1000] [--repo .]
Runtime: about 9 minutes for 1,000 seeds on one CPU core.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import GroupKFold

PURE_BENIGN_SINGLETONS = 1_882_245  # accepted multiplicity gate (band m = 1)
ROLES = ["weight_train", "early_stop", "calibration", "development", "final_test"]
SHARE = np.array([0.50, 0.10, 0.15, 0.10, 0.15])
BAND_EDGES = [1, 2, 3, 5, 10, 20, 50, 100, 10**9]  # bands 1, 2, 3-4, 5-9, 10-19, 20-49, 50-99, >=100


def load_sizes(repo: Path) -> np.ndarray:
    m = pd.read_csv(repo / "artifacts/unsw_nb15/fingerprints/duplicate_group_manifest.csv")
    dup = m.loc[m.binary_label_max == 0, "fingerprint_group_size"].to_numpy(dtype=np.int64)
    sizes = np.concatenate([np.ones(PURE_BENIGN_SINGLETONS, dtype=np.int64), dup])
    assert len(sizes) == 1_938_413 and sizes.sum() == 2_217_778, (len(sizes), sizes.sum())
    return sizes


def role_metrics(assign, sizes, band, pool_p):
    out = []
    for r, name in enumerate(ROLES):
        msk = assign == r
        rows_by_band = np.bincount(band[msk], weights=sizes[msk], minlength=8)
        n = rows_by_band.sum()
        p = rows_by_band / n
        out.append(dict(role=name, rows=n, row_share=n / sizes.sum(),
                        tv=0.5 * np.abs(p - pool_p).sum(),
                        singleton_share=p[0], ge100_rows=rows_by_band[7]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--seeds", type=int, default=1000)
    ap.add_argument("--out", default="results/splitter_baselines")
    a = ap.parse_args()
    repo, out = Path(a.repo), Path(a.repo) / a.out
    out.mkdir(parents=True, exist_ok=True)

    sizes = load_sizes(repo)
    band = np.digitize(sizes, BAND_EDGES[1:-1], right=False)
    pool = np.bincount(band, weights=sizes, minlength=8)
    pool_p = pool / pool.sum()
    G, total, cum = len(sizes), sizes.sum(), np.cumsum(SHARE)
    print(f"groups {G}, rows {total}, scikit-learn {sklearn.__version__}")

    rows = []
    for s in range(a.seeds):
        rng = np.random.default_rng(s)
        assign = rng.choice(5, size=G, p=SHARE)
        rows += [dict(allocator="A_random_group_assignment", seed=s, **d) for d in role_metrics(assign, sizes, band, pool_p)]
        perm = rng.permutation(G)
        cs = np.cumsum(sizes[perm]) / total
        assign = np.empty(G, dtype=np.int64)
        assign[perm] = np.searchsorted(cum, cs, side="left").clip(0, 4)
        rows += [dict(allocator="B_permutation_cut_by_rows", seed=s, **d) for d in role_metrics(assign, sizes, band, pool_p)]
        perm = rng.permutation(G)
        pos = (np.arange(G) + 0.5) / G
        assign = np.empty(G, dtype=np.int64)
        assign[perm] = np.searchsorted(cum, pos, side="left").clip(0, 4)
        rows += [dict(allocator="C_permutation_cut_by_groups", seed=s, **d) for d in role_metrics(assign, sizes, band, pool_p)]

    grp = np.repeat(np.arange(G), sizes)
    fold = np.empty(len(grp), dtype=np.int64)
    for k, (_, te) in enumerate(GroupKFold(n_splits=20).split(np.zeros((len(grp), 1)), groups=grp)):
        fold[te] = k
    gfold = np.empty(G, dtype=np.int64)
    gfold[grp] = fold
    assign = np.repeat(np.arange(5), [10, 2, 3, 2, 3])[gfold]
    rows += [dict(allocator="D_sklearn_GroupKFold_20folds", seed=-1, **d) for d in role_metrics(assign, sizes, band, pool_p)]

    df = pd.DataFrame(rows)
    df.to_csv(out / "splitter_runs.csv", index=False)
    summ = df.groupby(["allocator", "role"]).agg(
        runs=("seed", "nunique"), tv_median=("tv", "median"), tv_max=("tv", "max"),
        singleton_share_min=("singleton_share", "min"), singleton_share_max=("singleton_share", "max"),
        ge100_rows_min=("ge100_rows", "min"), ge100_rows_max=("ge100_rows", "max"),
        row_share_min=("row_share", "min"), row_share_max=("row_share", "max")).reset_index()
    summ.to_csv(out / "splitter_summary.csv", index=False)
    mx = df.groupby(["allocator", "seed"]).tv.max().groupby("allocator").agg(
        median="median", p95=lambda x: x.quantile(0.95), maximum="max").reset_index()
    mx.to_csv(out / "splitter_max_tv.csv", index=False)
    pd.set_option("display.width", 200)
    print(summ.to_string())
    print(mx.to_string())


if __name__ == "__main__":
    main()
