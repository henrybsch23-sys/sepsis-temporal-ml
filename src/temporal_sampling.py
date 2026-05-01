from typing import List, Optional

import pandas as pd


def get_sepsis_onset_hour(df: pd.DataFrame) -> Optional[int]:
    """
    Return the first hour where SepsisLabel == 1.

    Parameters
    ----------
    df:
        Patient DataFrame.

    Returns
    -------
    Optional[int]
        First sepsis onset index, or None if patient never becomes septic.
    """
    if "SepsisLabel" not in df.columns:
        raise KeyError("DataFrame must contain 'SepsisLabel' column.")

    positive_idx = df.index[df["SepsisLabel"] == 1].tolist()

    if len(positive_idx) == 0:
        return None

    return int(min(positive_idx))


def label_future_sepsis(
    df: pd.DataFrame,
    t: int,
    horizon: int
) -> Optional[int]:
    """
    Create a prospective early sepsis label.

    The label is:
    - None if patient is already septic at or before time t
    - 1 if sepsis starts within (t, t + horizon]
    - 0 otherwise

    Parameters
    ----------
    df:
        Patient DataFrame.
    t:
        Prediction time index.
    horizon:
        Future prediction horizon in hours.

    Returns
    -------
    Optional[int]
        Future sepsis label or None if sample should be excluded.
    """
    onset = get_sepsis_onset_hour(df)

    if onset is not None and onset <= t:
        return None

    if onset is not None and t < onset <= t + horizon:
        return 1

    return 0


def generate_prediction_times(
    n_hours: int,
    min_history: int,
    step: int = 1
) -> List[int]:
    """
    Generate valid prediction times for a patient trajectory.

    Parameters
    ----------
    n_hours:
        Number of hourly rows for the patient.
    min_history:
        Minimum number of observed hours required.
    step:
        Step size in hours.

    Returns
    -------
    list[int]
        Prediction time indices.
    """
    if n_hours < min_history:
        return []

    return list(range(min_history - 1, n_hours - 1, step))