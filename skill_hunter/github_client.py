"""GitHub API client for skill-hunter."""

import base64
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

from .config import load_config


class GitHubClient:
    """Client for searching GitHub repositories, fetching metadata, and downloading files."""

    def __init__(self, config_path: str | None = None) -> None:
        """Initialize the client from a config file.

        Args:
            config_path: Optional path to config.json.  Defaults to the
                config.json alongside this module.
        """
        config = load_config(config_path)
        self.token: str = config.get("github_token", "") or ""
        self.lookback_days: int = config.get("lookback_days", 7)
        self.max_results: int = config.get("max_results", 100)
        self._no_token_warned = False

        if not self.token and not self._no_token_warned:
            print(
                "Tip: add a GitHub token to skill_hunter/config.json "
                "for higher rate limits (60 req/hr → 5000 req/hr)"
            )
            self._no_token_warned = True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @property
    def _auth_headers(self) -> dict[str, str]:
        """Return Authorization header if a token is configured, else empty dict."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search_repositories(
        self,
        query: str,
        days_back: int | None = None,
        max_results: int | None = None,
    ) -> list[dict[str, Any]]:
        """Search GitHub repositories matching the given query.

        Args:
            query: GitHub search query string (e.g. '"SKILL.md" "claude code"').
            days_back: Only consider repos pushed to within this many days.
                Falls back to ``self.lookback_days`` from config.
            max_results: Maximum results to return.
                Falls back to ``self.max_results`` from config.

        Returns:
            A list of repository summary dicts with keys:
            owner, repo, pushed_at, created_at, description.
        """
        if days_back is None:
            days_back = self.lookback_days
        if max_results is None:
            max_results = self.max_results

        since_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime(
            "%Y-%m-%d"
        )

        full_query = f"{query} pushed:>{since_date}"
        url = "https://api.github.com/search/repositories"
        params = {
            "q": full_query,
            "sort": "updated",
            "order": "desc",
            "per_page": max_results,
        }

        resp = requests.get(url, headers=self._auth_headers, params=params)

        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_ts = resp.headers.get("X-RateLimit-Reset")
            reset_msg = ""
            if reset_ts:
                reset_time = datetime.fromtimestamp(int(reset_ts))
                reset_msg = f" Resets at {reset_time}"
            print(f"GitHub rate limit exceeded.{reset_msg}")
            return []

        if not resp.ok:
            print(f"search_repositories: HTTP {resp.status_code}")
            return []

        data = resp.json()
        results: list[dict[str, Any]] = []
        for item in data.get("items", []):
            results.append(
                {
                    "owner": item["owner"]["login"],
                    "repo": item["name"],
                    "pushed_at": item["pushed_at"],
                    "created_at": item["created_at"],
                    "description": item["description"],
                }
            )
        return results

    def get_repo_metadata(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Fetch metadata for a specific repository.

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.

        Returns:
            A dict with keys: stars, pushed_at, created_at, description,
            or None on failure.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}"
        resp = requests.get(url, headers=self._auth_headers)

        if resp.status_code == 404:
            return None

        if not resp.ok:
            print(f"get_repo_metadata: HTTP {resp.status_code}")
            return None

        item = resp.json()
        return {
            "stars": item["stargazers_count"],
            "pushed_at": item["pushed_at"],
            "created_at": item["created_at"],
            "description": item["description"],
        }

    def download_file(self, owner: str, repo: str, path: str) -> str | None:
        """Download a file from a repository.

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.
            path: File path within the repository.

        Returns:
            The file contents as a string, or None on failure (including 404).
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        resp = requests.get(url, headers=self._auth_headers)

        if resp.status_code == 404:
            return None

        if not resp.ok:
            print(f"download_file: HTTP {resp.status_code}")
            return None

        item = resp.json()

        # For files < 1 MB the API includes a download_url
        if item.get("download_url"):
            dl = requests.get(item["download_url"], headers=self._auth_headers)
            if dl.ok:
                return dl.text
            print(f"download_file: download_url returned HTTP {dl.status_code}")
            return None

        # Otherwise decode the base64-encoded content
        raw = item.get("content", "")
        if raw:
            return base64.b64decode(raw).decode("utf-8")

        return None
