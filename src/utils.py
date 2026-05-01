from pathlib import Path
from typing import Union


PathLike = Union[str, Path]


def ensure_dir(path: PathLike) -> Path:
    """
    Create a directory if it does not exist.

    Parameters
    ----------
    path:
        Directory path.

    Returns
    -------
    Path
        The created/existing directory path.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_dataframe(df, path: PathLike, index: bool = False) -> None:
    """
    Save a pandas DataFrame to CSV, creating parent folders if needed.

    Parameters
    ----------
    df:
        DataFrame to save.
    path:
        Output CSV path.
    index:
        Whether to save the DataFrame index.
    """
    path = Path(path)
    ensure_dir(path.parent)
    df.to_csv(path, index=index)


def save_figure(fig, path: PathLike, dpi: int = 150) -> None:
    """
    Save a matplotlib figure, creating parent folders if needed.

    Parameters
    ----------
    fig:
        Matplotlib figure.
    path:
        Output image path.
    dpi:
        Image resolution.
    """
    path = Path(path)
    ensure_dir(path.parent)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")