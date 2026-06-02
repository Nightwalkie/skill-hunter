"""Tests for IndexManager."""
import json
import os
import tempfile

from skill_hunter.index_manager import IndexManager


def test_empty_index_returns_all_new():
    """Empty index -> all candidates are new."""
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "skill-index.json")
        mgr = IndexManager(index_path=index_path)

        candidates = [
            {"owner": "alice", "repo": "project-a", "pushed_at": "2025-01-01T00:00:00Z"},
            {"owner": "bob", "repo": "project-b", "pushed_at": "2025-01-02T00:00:00Z"},
            {"owner": "carol", "repo": "project-c", "pushed_at": "2025-01-03T00:00:00Z"},
        ]

        result = mgr.classify_candidates(candidates)

        assert len(result["new"]) == 3
        assert len(result["updated"]) == 0
        assert len(result["skip"]) == 0

        assert result["new"][0]["owner"] == "alice"
        assert result["new"][1]["owner"] == "bob"
        assert result["new"][2]["owner"] == "carol"


def test_existing_no_updates_skipped():
    """Existing index -> repos with no new updates are skip."""
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "skill-index.json")

        # Pre-create an index with known entries
        existing_index = {
            "alice/project-a": {
                "owner": "alice",
                "repo": "project-a",
                "publish_date": "2024-01-01T00:00:00Z",
                "last_update": "2025-02-01T00:00:00Z",
                "last_discovered": "2025-02-01T00:00:00Z",
            },
            "bob/project-b": {
                "owner": "bob",
                "repo": "project-b",
                "publish_date": "2024-01-01T00:00:00Z",
                "last_update": "2025-02-01T00:00:00Z",
                "last_discovered": "2025-02-01T00:00:00Z",
            },
        }
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(existing_index, f)

        mgr = IndexManager(index_path=index_path)

        candidates = [
            # Matches index exactly - no update
            {"owner": "alice", "repo": "project-a", "pushed_at": "2025-02-01T00:00:00Z"},
            # Older than index - no update
            {"owner": "bob", "repo": "project-b", "pushed_at": "2025-01-15T00:00:00Z"},
        ]

        result = mgr.classify_candidates(candidates)

        assert len(result["new"]) == 0
        assert len(result["updated"]) == 0
        assert len(result["skip"]) == 2

        assert result["skip"][0]["owner"] == "alice"
        assert result["skip"][1]["owner"] == "bob"


def test_existing_with_updates():
    """Existing index -> repos with newer pushed_at are updated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "skill-index.json")

        # Pre-create index with old last_update
        existing_index = {
            "alice/project-a": {
                "owner": "alice",
                "repo": "project-a",
                "publish_date": "2024-01-01T00:00:00Z",
                "last_update": "2025-01-01T00:00:00Z",
                "last_discovered": "2025-01-01T00:00:00Z",
            },
        }
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(existing_index, f)

        mgr = IndexManager(index_path=index_path)

        candidates = [
            # Newer pushed_at than index's last_update
            {"owner": "alice", "repo": "project-a", "pushed_at": "2025-06-01T00:00:00Z"},
        ]

        result = mgr.classify_candidates(candidates)

        assert len(result["new"]) == 0
        assert len(result["updated"]) == 1
        assert len(result["skip"]) == 0

        assert result["updated"][0]["owner"] == "alice"


def test_round_trip():
    """Write index -> read back -> data matches."""
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "skill-index.json")
        mgr = IndexManager(index_path=index_path)

        test_index = {
            "alice/project-a": {
                "owner": "alice",
                "repo": "project-a",
                "publish_date": "2024-01-01T00:00:00Z",
                "last_update": "2025-01-01T00:00:00Z",
                "last_discovered": "2025-01-01T00:00:00Z",
            },
            "bob/project-b": {
                "owner": "bob",
                "repo": "project-b",
                "publish_date": "2024-06-01T00:00:00Z",
                "last_update": "2025-03-01T00:00:00Z",
                "last_discovered": "2025-03-01T00:00:00Z",
            },
        }

        mgr.save_index(test_index)
        loaded = mgr.load_index()

        assert loaded.keys() == test_index.keys()
        for key in test_index:
            assert loaded[key] == test_index[key]
