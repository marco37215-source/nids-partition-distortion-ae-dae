# UNSW-NB15

* Distribution: the four full flow-record files `UNSW-NB15_1.csv` … `UNSW-NB15_4.csv`, which have no header. The 49 column names are in `artifacts/unsw_nb15/provenance/feature_schema_1_to_49.csv`. The predefined training/testing subsets were **not** used.
* Merged master: 2,540,047 rows. There are 2,218,764 benign and 321,283 attack rows, in nine canonical families; the alias `Backdoor` was mapped to `Backdoors` before partitioning. The manuscript notes that this is three rows more than a commonly cited count of 2,540,044; the three rows were not identified.
* Model view: 38 numerical features plus `proto`, `state` and `service`. Excluded are `srcip`, `sport`, `dstip`, `dsport`, `Stime`, `Ltime`, `Label` and `attack_cat`.
* Master SHA-256 (PRE-00): `f0447e754fa9ed939ed785e2a8a4d47f3719da2d1fb445134bcb5daf66cf9c54`.

To verify my merged master, replace `MASTER_FILENAME` in `SHA256SUMS.txt` with the name of my file and run `sha256sum -c SHA256SUMS.txt`.
