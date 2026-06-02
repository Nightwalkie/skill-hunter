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
                     Defaults to ``{project_root}/skill_hunter/config.json``.

    Returns:
        A dict with the merged configuration.
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

    config = dict(DEFAULT_CONFIG)

    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        return config

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            file_config = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: config.json is corrupted, using defaults")
        return config

    config.update(file_config)
    return config
