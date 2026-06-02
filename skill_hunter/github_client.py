"""GitHub API client for skill-hunter."""

from typing import Any


class GitHubClient:
    """Client for searching GitHub repositories, fetching metadata, and downloading files."""

    def __init__(self, token: str) -> None:
        """Initialize the client with a GitHub token.

        Args:
            token: GitHub personal access token.
        """
        self.token = token

    def search_repositories(self, query: str, max_results: int = 100) -> list[dict[str, Any]]:
        """Search GitHub repositories matching the given query.

        Args:
            query: GitHub search query string.
            max_results: Maximum number of results to return.

        Returns:
            A list of repository summary dicts.
        """
        raise NotImplementedError

    def get_repo_metadata(self, owner: str, repo: str) -> dict[str, Any]:
        """Fetch metadata for a specific repository.

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.

        Returns:
            A dict with repository metadata (stars, description, topics, etc.).
        """
        raise NotImplementedError

    def download_file(self, owner: str, repo: str, path: str) -> str:
        """Download a file from a repository.

        Args:
            owner: Repository owner (user or org).
            repo: Repository name.
            path: File path within the repository.

        Returns:
            The file contents as a string.
        """
        raise NotImplementedError
