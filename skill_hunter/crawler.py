"""Main crawler runner for skill-hunter."""

import json
import os

from skill_hunter.config import load_config, validate_token
from skill_hunter.github_client import GitHubClient
from skill_hunter.index_manager import IndexManager


def run() -> None:
    """Entry point for the skill-hunter crawler pipeline.

    Pipeline steps:
        1. Load config and validate GitHub token (mandatory).
        2. Search GitHub for repos containing SKILL.md + claude code.
        3. Classify results via IndexManager (new / updated / skip).
        4. Combine new + updated candidates; discard skipped.
        5. Download README.md and enrich metadata for each candidate.
        6. Write results to raw-data.json in the project root.
    """
    try:
        config = load_config()

        # 1. Validate GitHub token (mandatory)
        github_token: str = config.get("github_token", "") or ""
        if not github_token:
            print(
                "Error: No GitHub token found in skill_hunter/config.json. "
                "Add a Personal Access Token with 'public_repo' scope from "
                "https://github.com/settings/tokens"
            )
            return

        print("Validating GitHub token...")
        token_result = validate_token(github_token)
        if not token_result["valid"]:
            print(f"Token validation failed: {token_result['error']}")
            return

        print(f"Token validated (user: {token_result['user']})")

        lookback_days = config["lookback_days"]
        max_results = config["max_results"]

        # 2. Search GitHub
        client = GitHubClient()
        print("Searching GitHub...")
        search_results = client.search_repositories(
            '"SKILL.md" "claude code"',
            days_back=lookback_days,
            max_results=max_results,
        )

        if not search_results:
            print("No repositories found. Try a different search query or date range.")
            return

        print(f"Found {len(search_results)} repositories.")

        # 3. Classify with index
        index_mgr = IndexManager()
        classification = index_mgr.classify_candidates(search_results)
        new_count = len(classification["new"])
        updated_count = len(classification["updated"])
        skip_count = len(classification["skip"])
        print(
            f"Checking index... {new_count} new, "
            f"{updated_count} updated, {skip_count} skipped."
        )

        # 4. Prepare candidates
        candidates = classification["new"] + classification["updated"]

        if not candidates:
            print("No new or updated skills found this week.")
            return

        print(f"Processing {len(candidates)} candidates...")
        total = len(candidates)

        # 5. Download README.md and enrich metadata
        output = []
        for i, candidate in enumerate(candidates, start=1):
            owner = candidate["owner"]
            repo = candidate["repo"]
            label = f"{owner}/{repo}"

            print(f"Downloading README.md ({i}/{total}): {label}...")

            file_content = client.download_file(owner, repo, "README.md")
            if file_content is None:
                print(f"  (no README.md found for {label}, skipping)")
                continue

            metadata = client.get_repo_metadata(owner, repo)
            if metadata is None:
                metadata = {}

            output.append(
                {
                    "owner": owner,
                    "repo": repo,
                    "publish_date": candidate["created_at"],
                    "last_update": candidate["pushed_at"],
                    "stars": metadata.get("stars", 0),
                    "readme_content": file_content,
                    "index_status": (
                        "new" if candidate in classification["new"] else "updated"
                    ),
                }
            )

        # 6. Write raw-data.json
        skill_hunter_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(skill_hunter_dir)
        output_path = os.path.join(project_root, "raw-data.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"Wrote {len(output)} entries to raw-data.json.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run()
