"""Index manager for skill-hunter - tracks known skills to detect new/updated ones."""

from typing import Any


class IndexManager:
    """Manages a local index of known skills for change detection."""

    def __init__(self, index_path: str | None = None) -> None:
        """Initialize the index manager.

        Args:
            index_path: Optional path to the index file.
        """
        self.index_path = index_path

    def load_index(self) -> dict[str, Any]:
        """Load the existing index from disk.

        Returns:
            The index data as a dict, or an empty dict if no index exists.
        """
        raise NotImplementedError

    def save_index(self, index_data: dict[str, Any]) -> None:
        """Save the index data to disk.

        Args:
            index_data: The index data to persist.
        """
        raise NotImplementedError

    def classify_candidates(self, candidates: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Classify candidate repositories as new, updated, or unchanged.

        Args:
            candidates: List of candidate repository dicts.

        Returns:
            A dict with keys 'new', 'updated', 'unchanged' mapping to lists.
        """
        raise NotImplementedError
