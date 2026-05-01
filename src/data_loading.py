from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd


def get_patient_files(
    data_dir: str | Path,
    max_files: Optional[int] = None
) -> List[Path]:
    """
    Return sorted patient .psv files from a PhysioNet directory.

    Parameters
    ----------
    data_dir:
        Directory containing .psv patient files.
    max_files:
        Optional maximum number of files to return.

    Returns
    -------
    list[Path]
        Sorted patient file paths.
    """
    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(
            f"Data directory not found: {data_dir}. "
            "Check config.yaml and data/README.md."
        )

    files = sorted(data_dir.glob("*.psv"))

    if max_files is not None:
        files = files[:max_files]

    return files


def read_patient_file(file_path: str | Path) -> pd.DataFrame:
    """
    Read a single PhysioNet patient .psv file and attach patient_id.

    Parameters
    ----------
    file_path:
        Path to patient .psv file.

    Returns
    -------
    pd.DataFrame
        Patient hourly ICU record with patient_id column.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Patient file not found: {file_path}")

    df = pd.read_csv(file_path, sep="|")
    df["patient_id"] = file_path.stem

    return df


def summarize_patient_file(file_path: str | Path, cohort: str) -> dict:
    """
    Summarize one patient file for dataset-level understanding.

    This function does not create model features. It is only for EDA.

    Parameters
    ----------
    file_path:
        Path to patient .psv file.
    cohort:
        Cohort name, e.g. "A" or "B".

    Returns
    -------
    dict
        Patient-level summary.
    """
    df = read_patient_file(file_path)

    has_sepsis = int(df["SepsisLabel"].max()) if "SepsisLabel" in df.columns else 0

    if has_sepsis:
        onset_hour = int(df.index[df["SepsisLabel"] == 1][0])
    else:
        onset_hour = None

    return {
        "patient_id": df["patient_id"].iloc[0],
        "cohort": cohort,
        "n_hours": len(df),
        "has_sepsis": has_sepsis,
        "sepsis_onset_hour": onset_hour,
    }


def build_patient_summary(
    files: Iterable[str | Path],
    cohort: str
) -> pd.DataFrame:
    """
    Build patient-level summary table for a collection of files.

    Parameters
    ----------
    files:
        Iterable of patient file paths.
    cohort:
        Cohort name, e.g. "A" or "B".

    Returns
    -------
    pd.DataFrame
        Patient-level summary table.
    """
    rows = [summarize_patient_file(fp, cohort=cohort) for fp in files]
    return pd.DataFrame(rows)


def compute_raw_missingness(files: Iterable[str | Path]) -> pd.DataFrame:
    """
    Compute raw variable missingness across patient files.

    Parameters
    ----------
    files:
        Iterable of patient file paths.

    Returns
    -------
    pd.DataFrame
        Missingness summary with missing_count, total_count, missing_fraction.
    """
    missing_counts = None
    total_counts = None

    for fp in files:
        df = read_patient_file(fp)

        # Exclude patient_id because we added it manually.
        if "patient_id" in df.columns:
            df = df.drop(columns=["patient_id"])

        current_missing = df.isna().sum()
        current_total = pd.Series(len(df), index=df.columns)

        if missing_counts is None:
            missing_counts = current_missing
            total_counts = current_total
        else:
            missing_counts = missing_counts.add(current_missing, fill_value=0)
            total_counts = total_counts.add(current_total, fill_value=0)

    if missing_counts is None or total_counts is None:
        return pd.DataFrame(
            columns=["feature", "missing_count", "total_count", "missing_fraction"]
        )

    summary = pd.DataFrame({
        "feature": missing_counts.index,
        "missing_count": missing_counts.values,
        "total_count": total_counts.values,
    })

    summary["missing_fraction"] = (
        summary["missing_count"] / summary["total_count"]
    )

    summary = summary.sort_values("missing_fraction", ascending=False).reset_index(drop=True)

    return summary


def compute_missingness_by_cohort(
    files_a: Iterable[str | Path],
    files_b: Iterable[str | Path]
) -> pd.DataFrame:
    """
    Compute raw variable missingness separately for cohorts A and B.

    Parameters
    ----------
    files_a:
        Cohort A patient files.
    files_b:
        Cohort B patient files.

    Returns
    -------
    pd.DataFrame
        Missingness summary by cohort.
    """
    miss_a = compute_raw_missingness(files_a)
    miss_a["cohort"] = "A"

    miss_b = compute_raw_missingness(files_b)
    miss_b["cohort"] = "B"

    return pd.concat([miss_a, miss_b], ignore_index=True)