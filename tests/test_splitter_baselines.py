"""Smoke test for scripts/splitter_baselines.py (two seeds; runs in well under a minute)."""
import subprocess
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]


def test_splitter_baselines_two_seeds(tmp_path):
    out = tmp_path / "sb"
    subprocess.run([sys.executable, str(REPO / "scripts/splitter_baselines.py"), "--repo", str(REPO),
                    "--seeds", "2", "--out", str(out)], check=True)
    runs = pd.read_csv(out / "splitter_runs.csv")
    assert len(runs) == (2 * 3 + 1) * 5
    for (_, _), g in runs.groupby(["allocator", "seed"]):
        assert int(g.rows.sum()) == 2_217_778          # every pure-benign row assigned exactly once
        assert g.tv.max() < 0.03                        # far from the 0.7094 of the source-balanced allocation
    ref = pd.read_csv(REPO / "results/splitter_baselines/splitter_runs.csv")
    sub = ref[(ref.seed < 2) | (ref.seed == -1)].reset_index(drop=True)
    pd.testing.assert_series_equal(sub.tv, runs.tv, check_exact=False, rtol=1e-12)
