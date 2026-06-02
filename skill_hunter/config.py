"""Config module for skill-hunter."""

import json
import os
from typing import Dict, Any

DEFAULT_CONFIG: Dict[str, Any] = {
    "github_token": "",
    "lookback_days": 7,
    "max_results": 100,
}


def load_config(config_path: str | None = None) -> Dict[str, Any]:
    """Load configuration from config.json, falling back to defaults.

    Args:
        config_path: Optional path to a config.json file.
                     Defaults to config.json in the same directory as this module.

    Returns:
        A dict with the merged configuration.
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

    config = dict(DEFAULT_CONFIG)

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            file_config = json.load(f)
            config.update(file_config)

    return config
