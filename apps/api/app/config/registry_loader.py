from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).parent


def load_yaml(filename: str) -> list[dict[str, Any]]:
    """Load a YAML registry file."""

    path = CONFIG_DIR / filename

    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, list):
        raise ValueError(f"Registry file {filename} must contain a list.")

    return data


def load_organizations() -> list[dict[str, Any]]:
    """Load organization registry entries."""

    return load_yaml("organizations.yaml")


def load_sources() -> list[dict[str, Any]]:
    """Load source registry entries."""

    return load_yaml("sources.yaml")
