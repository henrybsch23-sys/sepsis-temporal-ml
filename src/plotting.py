from pathlib import Path
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import pandas as pd

from src.utils import save_figure


def plot_sample_patient_timeseries(
    df: pd.DataFrame,
    cols: Iterable[str],
    save_path: Optional[str | Path] = None
):
    """
    Plot selected time-series columns for one patient.

    Parameters
    ----------
    df:
        Patient DataFrame.
    cols:
        Columns to plot.
    save_path:
        Optional path to save figure.

    Returns
    -------
    matplotlib.figure.Figure
    """
    cols = [c for c in cols if c in df.columns]

    fig, axes = plt.subplots(
        len(cols),
        1,
        figsize=(10, 2.2 * len(cols)),
        sharex=True
    )

    if len(cols) == 1:
        axes = [axes]

    for ax, col in zip(axes, cols):
        ax.plot(df.index, df[col], marker="o", linewidth=1)
        ax.set_title(col)
        ax.set_ylabel("Value")
        ax.grid(alpha=0.3)

    axes[-1].set_xlabel("Hour")
    fig.suptitle("Sample Patient Time-Series", y=1.02)
    fig.tight_layout()

    if save_path is not None:
        save_figure(fig, save_path)

    return fig


def plot_icu_length_distribution(
    patient_summary: pd.DataFrame,
    save_path: Optional[str | Path] = None
):
    """
    Plot distribution of ICU stay lengths.

    Parameters
    ----------
    patient_summary:
        DataFrame with n_hours column.
    save_path:
        Optional path to save figure.

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(patient_summary["n_hours"], bins=40)
    ax.set_title("ICU Stay Length Distribution")
    ax.set_xlabel("Number of hourly records")
    ax.set_ylabel("Number of patients")
    ax.grid(alpha=0.3)

    fig.tight_layout()

    if save_path is not None:
        save_figure(fig, save_path)

    return fig


def plot_sepsis_onset_distribution(
    patient_summary: pd.DataFrame,
    save_path: Optional[str | Path] = None
):
    """
    Plot distribution of sepsis onset hour among septic patients.

    Parameters
    ----------
    patient_summary:
        DataFrame with sepsis_onset_hour column.
    save_path:
        Optional path to save figure.

    Returns
    -------
    matplotlib.figure.Figure
    """
    septic = patient_summary[patient_summary["has_sepsis"] == 1].copy()

    fig, ax = plt.subplots(figsize=(8, 5))

    if len(septic) > 0:
        ax.hist(septic["sepsis_onset_hour"].dropna(), bins=40)
    else:
        ax.text(
            0.5,
            0.5,
            "No septic patients found",
            ha="center",
            va="center",
            transform=ax.transAxes
        )

    ax.set_title("Sepsis Onset Hour Distribution")
    ax.set_xlabel("First hour with SepsisLabel = 1")
    ax.set_ylabel("Number of patients")
    ax.grid(alpha=0.3)

    fig.tight_layout()

    if save_path is not None:
        save_figure(fig, save_path)

    return fig


def plot_missingness_top_n(
    missing_summary: pd.DataFrame,
    top_n: int = 20,
    save_path: Optional[str | Path] = None
):
    """
    Plot top N most missing variables.

    Parameters
    ----------
    missing_summary:
        DataFrame with feature and missing_fraction columns.
    top_n:
        Number of variables to plot.
    save_path:
        Optional path to save figure.

    Returns
    -------
    matplotlib.figure.Figure
    """
    top_missing = (
        missing_summary
        .head(top_n)
        .sort_values("missing_fraction", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(top_missing["feature"], top_missing["missing_fraction"])
    ax.set_title(f"Top {top_n} Most Missing Raw Variables")
    ax.set_xlabel("Missing fraction")
    ax.set_ylabel("Feature")
    ax.grid(axis="x", alpha=0.3)

    fig.tight_layout()

    if save_path is not None:
        save_figure(fig, save_path)

    return fig


def plot_class_balance(
    patient_summary: pd.DataFrame,
    save_path: Optional[str | Path] = None
):
    """
    Plot patient-level sepsis class balance.

    Parameters
    ----------
    patient_summary:
        DataFrame with has_sepsis column.
    save_path:
        Optional path to save figure.

    Returns
    -------
    matplotlib.figure.Figure
    """
    counts = patient_summary["has_sepsis"].value_counts().sort_index()
    labels = ["No sepsis", "Sepsis"]
    values = [counts.get(0, 0), counts.get(1, 0)]

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(labels, values)
    ax.set_title("Patient-Level Sepsis Class Balance")
    ax.set_ylabel("Number of patients")
    ax.grid(axis="y", alpha=0.3)

    for i, value in enumerate(values):
        ax.text(i, value, str(value), ha="center", va="bottom")

    fig.tight_layout()

    if save_path is not None:
        save_figure(fig, save_path)

    return fig