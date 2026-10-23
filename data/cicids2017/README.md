# CICIDS2017

* Distribution: the official *MachineLearningCSV* flow-feature files (eight daily CSVs) from the Canadian Institute for Cybersecurity.
* Merged master: 2,830,743 rows. There are 2,273,097 benign and 557,646 attack rows, in 14 attack families plus BENIGN. The model view has 78 numerical features; only the label is excluded.
* Master SHA-256 (PRE-00): `b68a108f6fe44082a051e2ab81a4bd8859cb3ccd417ff60623871155d51cabd3`.
* The raw header contains the name ` Fwd Header Length` twice. The parser renamed the second occurrence ` Fwd Header Length.1`, and the frozen model view keeps both (`artifacts/cicids2017/provenance/prepartition_readiness_report.json`).
* The web-attack labels contain a cp1252 en dash, which appears as U+FFFD in the frozen artefacts.

To verify my merged master, replace `MASTER_FILENAME` in `SHA256SUMS.txt` with the name of my file and run `sha256sum -c SHA256SUMS.txt` in the folder that contains it.
