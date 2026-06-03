"""GitHub API client for skill-hunter."""

import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import load_config


class GitHubClient:
    """Client for searching GitHub repositories, fetching metadata, and downloading files."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        """Initialize the client from a config file.

        Args:
            config_path: Optional path to config.json.  Defaults to the
                config.json alongside this module.
        """
        config = load_config(config_path)
        self.token: str = config.get("github_token", "") or ""
        self.lookback_days: int = config.get("lookback_days", 7)
        self.max_results: int = config.get("max_results", 100)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @property
    def _auth_headers(self) -> Dict[str, str]:
        """Return Authorization header if a token is configured, else empty dict."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def _build_url(self, url: str, params: Optional[Dict] = None) -> str:
        """Build a full URL with optional query parameters."""
        if params:
            return f"{url}?{urlencode(params)}"
        return url

    def _get(
        self, url: str, params: Optional[Dict] = None, timeout: int = 30
    ) -> Optional[Dict[str, Any]]:
        """Make a GET request expecting a JSON response, with one retry on timeout.

        Returns:
            A dict with keys ``"status"``, ``"data"``, ``"headers"``,
            or None if the request could not be completed.
        """
        headers = self._auth_headers
        headers["Accept"] = "application/vnd.github.v3+json"
        headers["User-Agent"] = "skill-hunter"

        full_url = self._build_url(url, params)

        for attempt in range(2):
            try:
                req = urllib.request.Request(full_url, headers=headers)
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    data = json.loads(response.read().decode("utf-8"))
                    # Check rate limit
                    remaining = response.headers.get("X-RateLimit-Remaining")
                    if remaining is not None and int(remaining) == 0:
                        reset_time = response.headers.get(
                            "X-RateLimit-Reset", "unknown"
                        )
                        print(f"  Rate limit exceeded. Resets at: {reset_time}")
                    return {
                        "status": response.status,
                        "data": data,
                        "headers": dict(response.headers),
                    }
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8") if e.fp else ""
                if e.code == 403:
                    if "rate limit" in body.lower():
                        reset = e.headers.get("X-RateLimit-Reset", "unknown")
                        print(f"  Rate limit exceeded. Resets at: {reset}")
                        return None
                    print("  HTTP 403 Forbidden")
                    return None
                if e.code == 404:
                    return None
                print(f"  HTTP {e.code}")
                return None
            except urllib.error.URLError as e:
                if attempt == 0:
                    print("  Network timeout. Retrying once...")
                    time.sleep(1)
                    continue
                print("  GitHub API unavailable. Skipping this request.")
                return None
            except Exception as e:
                print(f"  Error: {e}")
                return None

        return None

    def _get_raw(
        self, url: str, timeout: int = 30
    ) -> Optional[Dict[str, Any]]:
        """Make a GET request expecting raw text (not JSON).

        Returns:
            A dict with keys ``"status"``, ``"text"``, ``"headers"``,
            or None on failure.
        """
        headers = self._auth_headers
        headers["User-Agent"] = "skill-hunter"

        for attempt in range(2):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    text = response.read().decode("utf-8")
                    return {
                        "status": response.status,
                        "text": text,
                        "headers": dict(response.headers),
                    }
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    return None
                print(f"  HTTP {e.code}")
                return None
            except urllib.error.URLError as e:
                if attempt == 0:
                    print("  Network timeout. Retrying once...")
                    time.sleep(1)
                    continue
                print("  GitHub API unavailable. Skipping this request.")
                return None
            except Exception as e:
                print(f"  Error: {e}")
                return None

        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search_repositories(
        self,
        query: str,
        days_back: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
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

        result = self._get(url, params=params)
        if result is None:
            return []

        if result["status"] != 200:
            print(f"search_repositories: HTTP {result['status']}")
            return []

        data = result["data"]
        results: List[Dict[str, Any]] = []
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

    def get_repo_metadata(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Fetch metadata for a specific repository.

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.

        Returns:
            A dict with keys: stars, pushed_at, created_at, description,
            or None on failure.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}"
        result = self._get(url)
        if result is None:
            return None

        if result["status"] != 200:
            print(f"get_repo_metadata: HTTP {result['status']}")
            return None

        item = result["data"]
        return {
            "stars": item["stargazers_count"],
            "pushed_at": item["pushed_at"],
            "created_at": item["created_at"],
            "description": item["description"],
        }

    def download_file(self, owner: str, repo: str, path: str) -> Optional[str]:
        """Download a file from a repository.

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.
            path: File path within the repository.

        Returns:
            The file contents as a string, or None on failure (including 404).
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        result = self._get(url)
        if result is None:
            return None

        if result["status"] != 200:
            print(f"download_file: HTTP {result['status']}")
            return None

        item = result["data"]

        # For files < 1 MB the API includes a download_url
        if item.get("download_url"):
            dl = self._get_raw(item["download_url"])
            if dl is None:
                return None
            if dl["status"] == 200:
                return dl["text"]
            print(f"download_file: download_url returned HTTP {dl['status']}")
            return None

        # Otherwise decode the base64-encoded content
        raw = item.get("content", "")
        if raw:
            return base64.b64decode(raw).decode("utf-8")

        return None
