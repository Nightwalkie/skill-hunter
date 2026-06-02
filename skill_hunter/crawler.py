"""Main crawler runner for skill-hunter."""

from skill_hunter.config import load_config
from skill_hunter.github_client import GitHubClient
from skill_hunter.index_manager import IndexManager


def run() -> None:
    """Entry point for the skill-hunter crawler."""
    print("Crawler started...")
    # TODO: wire up the full pipeline in subsequent issues
