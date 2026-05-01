from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(config_path: str | Path = "config.yaml") -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    config_path:
        Path to the YAML config file.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if config is None:
        raise ValueError(f"Config file is empty: {config_path}")

    return config


def get_project_root() -> Path:
    """
    Return the project root assuming this file lives inside src/.

    Returns
    -------
    Path
        Project root directory.
    """
    return Path(__file__).resolve().parents[1]