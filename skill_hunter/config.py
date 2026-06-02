"""Config module for skill-hunter."""

import json
import os
from typing import Any

import requests

DEFAULT_CONFIG: dict[str, Any] = {
    "github_token": "",
    "lookback_days": 7,
    "max_results": 100,
}


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load configuration from config.json, falling back to defaults.

    Does NOT auto-create config.json — the token must be set by the user.

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
        print("Warning: config.json not found, using defaults (no token)")
        return config

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            file_config = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: config.json is corrupted, using defaults")
        return config

    config.update(file_config)
    return config


def validate_token(token: str) -> dict[str, Any]:
    """Validate a GitHub Personal Access Token via the GitHub API.

    Args:
        token: The GitHub PAT to validate.

    Returns:
        A dict with keys: valid, error, scopes, user.
    """
    if not token or not token.strip():
        return {
            "valid": False,
            "error": "Token is empty.",
            "scopes": [],
            "user": None,
        }

    try:
        resp = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
    except requests.Timeout:
        return {
            "valid": False,
            "error": "Could not reach GitHub to validate token. Check your network.",
            "scopes": [],
            "user": None,
        }
    except requests.ConnectionError:
        return {
            "valid": False,
            "error": "Could not reach GitHub to validate token. Check your network.",
            "scopes": [],
            "user": None,
        }

    if resp.status_code == 401:
        return {
            "valid": False,
            "error": (
                "Token is invalid or expired. Please generate a new one at "
                "https://github.com/settings/tokens"
            ),
            "scopes": [],
            "user": None,
        }

    data = resp.json()
    scopes_header = resp.headers.get("X-OAuth-Scopes", "")
    scopes = [s.strip() for s in scopes_header.split(",") if s.strip()]

    if "public_repo" not in scopes and "repo" not in scopes:
        return {
            "valid": False,
            "error": (
                "Token lacks 'public_repo' scope. "
                "Add it at https://github.com/settings/tokens"
            ),
            "scopes": scopes,
            "user": data.get("login"),
        }

    return {
        "valid": True,
        "error": None,
        "scopes": scopes,
        "user": data.get("login"),
    }
