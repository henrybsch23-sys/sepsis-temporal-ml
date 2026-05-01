from pathlib import Path
from typing import Union, Callable
import pandas as pd


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
    

def load_or_create_csv(path, create_fn: Callable[[], pd.DataFrame], force: bool = False):
    """
    Load a CSV if it exists, otherwise create it using create_fn and save it.
    """
    path = Path(path)

    if path.exists() and not force:
        return pd.read_csv(path)

    df = create_fn()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df