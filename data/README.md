# Data

The raw data are not included in this repository.

This project uses the PhysioNet/Computing in Cardiology Challenge 2019 dataset.

To reproduce the analysis, download the dataset from PhysioNet and place it under:

```text
data/raw/challenge-2019/training/training_setA/
data/raw/challenge-2019/training/training_setB/
```

Expected file format:
```
data/raw/challenge-2019/training/training_setA/p000001.psv
data/raw/challenge-2019/training/training_setA/p000002.psv
...
data/raw/challenge-2019/training/training_setB/p100001.psv
...
```

The data/raw/ and data/processed/ folders are ignored by Git.

This repository may include a small optional sample under data/sample/ for demonstration purposes, but the full raw dataset should be downloaded separately.