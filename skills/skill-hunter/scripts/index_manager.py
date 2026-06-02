"""Index manager for skill-hunter - tracks known skills to detect new/updated ones."""

import datetime
import json
import os
from typing import Any, Dict, List, Optional


class IndexManager:
    """Manages a local index of known skills for change detection."""

    def __init__(self, index_path: Optional[str] = None) -> None:
        """Initialize the index manager.

        Args:
            index_path: Optional path to the index file.
                        Defaults to skill-index.json at the project root.
        """
        if index_path is None:
            scripts_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(scripts_dir)))
            index_path = os.path.join(project_root, "skill-index.json")
        self.index_path = index_path

    def load_index(self) -> Dict[str, Any]:
        """Load the existing index from disk.

        Returns:
            The index data as a dict (keyed by "owner/repo"),
            or an empty dict if no index exists or the file is corrupt.
        """
        if not os.path.exists(self.index_path):
            return {}
        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print(
                f"Warning: skill-index.json is corrupted, "
                f"using empty index"
            )
            return {}

    def save_index(self, index: Dict[str, Any]) -> None:
        """Save the index data to disk as pretty-printed JSON.

        Args:
            index: The index data to persist.
        """
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def classify_candidates(
        self, candidates: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Classify candidate repositories as new, updated, or skipped.

        Args:
            candidates: List of candidate repository dicts with keys
                        owner, repo, pushed_at, created_at, etc.

        Returns:
            A dict with keys 'new', 'updated', 'skip' mapping to lists.
        """
        index = self.load_index()
        classification: Dict[str, List[Dict[str, Any]]] = {
            "new": [],
            "updated": [],
            "skip": [],
        }

        for candidate in candidates:
            key = f"{candidate['owner']}/{candidate['repo']}"

            if key not in index:
                classification["new"].append(candidate)
                continue

            existing = index[key]
            candidate_pushed = self._parse_iso(candidate.get("pushed_at", ""))
            index_updated = self._parse_iso(existing.get("last_update", ""))

            if candidate_pushed is not None and index_updated is not None:
                if candidate_pushed > index_updated:
                    classification["updated"].append(candidate)
                else:
                    classification["skip"].append(candidate)
            else:
                # If we can't parse dates, conservatively treat as updated
                classification["updated"].append(candidate)

        return classification

    def is_known_skill(self, owner: str, repo: str) -> bool:
        """Check if a repository exists in the index (whitelist).

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.

        Returns:
            True if the repo is in the index, False otherwise.
        """
        index = self.load_index()
        key = f"{owner}/{repo}"
        return key in index

    def add_entries(self, entries: List[Dict[str, Any]]) -> None:
        """Add or update entries in the index.

        Overwrites existing entries with the same "owner/repo" key.
        Sets last_discovered to the current UTC time.

        Args:
            entries: List of dicts with keys owner, repo, publish_date,
                     last_update, last_discovered.
        """
        index = self.load_index()
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        for entry in entries:
            key = f"{entry['owner']}/{entry['repo']}"
            index[key] = {
                "owner": entry["owner"],
                "repo": entry["repo"],
                "publish_date": entry.get("publish_date", ""),
                "last_update": entry.get("last_update", ""),
                "last_discovered": now,
            }

        self.save_index(index)

    @staticmethod
    def _parse_iso(timestamp_str: Optional[str]) -> Optional[datetime.datetime]:
        """Parse an ISO 8601 timestamp string into a datetime object.

        Returns None if the string is empty or malformed.
        """
        if not timestamp_str:
            return None
        try:
            # fromisoformat handles ISO 8601 with timezone offsets
            return datetime.datetime.fromisoformat(timestamp_str)
        except (ValueError, TypeError):
            return None
