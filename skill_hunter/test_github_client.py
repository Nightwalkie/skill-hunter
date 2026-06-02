"""Tests for skill_hunter.github_client."""

from unittest.mock import MagicMock, patch

from skill_hunter.github_client import GitHubClient


# -- helpers ---------------------------------------------------------------

def _make_mock_response(json_data, status_code=200, headers=None):
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.status_code = status_code
    resp.headers = headers or {}
    resp.ok = 200 <= status_code < 300
    resp.text = ""
    return resp


# -- search_repositories ---------------------------------------------------


def test_search_repositories_returns_correct_structure():
    """search_repositories should return a list of dicts with the expected keys."""
    fake_items = [
        {
            "owner": {"login": "alice"},
            "name": "dotfiles",
            "pushed_at": "2026-05-30T12:00:00Z",
            "created_at": "2026-01-01T00:00:00Z",
            "description": "My dotfiles",
        }
    ]

    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response(
            {"items": fake_items},
            headers={"X-RateLimit-Reset": "9999999999"},
        )
        client = GitHubClient()
        results = client.search_repositories('"SKILL.md"', days_back=7)

    assert len(results) == 1
    repo = results[0]
    assert repo["owner"] == "alice"
    assert repo["repo"] == "dotfiles"
    assert repo["pushed_at"] == "2026-05-30T12:00:00Z"
    assert repo["created_at"] == "2026-01-01T00:00:00Z"
    assert repo["description"] == "My dotfiles"


def test_search_repositories_rate_limit_prints_error():
    """search_repositories should return [] and print a message on rate limit."""
    with patch("skill_hunter.github_client.requests.get") as mock_get:
        resp = _make_mock_response({}, status_code=403)
        resp.text = "API rate limit exceeded"
        resp.headers["X-RateLimit-Reset"] = "9999999999"
        mock_get.return_value = resp

        client = GitHubClient()
        results = client.search_repositories("test", days_back=1)

    assert results == []


def test_search_repositories_non_ok_status_returns_empty():
    """search_repositories should return [] for non-OK, non-rate-limit errors."""
    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response({}, status_code=500)
        client = GitHubClient()
        results = client.search_repositories("test", days_back=1)

    assert results == []


# -- get_repo_metadata -----------------------------------------------------


def test_get_repo_metadata_returns_correct_fields():
    """get_repo_metadata should return a dict with stars, pushed_at, etc."""
    fake_repo = {
        "stargazers_count": 42,
        "pushed_at": "2026-05-30T12:00:00Z",
        "created_at": "2026-01-01T00:00:00Z",
        "description": "A great project",
    }

    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response(fake_repo)
        client = GitHubClient()
        meta = client.get_repo_metadata("alice", "great-project")

    assert meta is not None
    assert meta["stars"] == 42
    assert meta["pushed_at"] == "2026-05-30T12:00:00Z"
    assert meta["created_at"] == "2026-01-01T00:00:00Z"
    assert meta["description"] == "A great project"


def test_get_repo_metadata_404_returns_none():
    """get_repo_metadata should return None on a 404."""
    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response({}, status_code=404)
        client = GitHubClient()
        meta = client.get_repo_metadata("alice", "nope")

    assert meta is None


def test_get_repo_metadata_other_error_returns_none():
    """get_repo_metadata should return None for non-404 errors."""
    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response({}, status_code=503)
        client = GitHubClient()
        meta = client.get_repo_metadata("alice", "down")

    assert meta is None


# -- download_file ---------------------------------------------------------


def test_download_file_returns_string_content_via_download_url():
    """download_file should use the download_url when present."""
    fake_item = {
        "download_url": "https://raw.example.com/foo/SKILL.md",
        "content": "",
    }

    with patch("skill_hunter.github_client.requests.get") as mock_get:
        # First call: repo contents API
        # Second call: download_url
        mock_content_resp = _make_mock_response(fake_item)
        mock_dl_resp = MagicMock()
        mock_dl_resp.ok = True
        mock_dl_resp.text = "# SKILL.md content"

        mock_get.side_effect = [mock_content_resp, mock_dl_resp]

        client = GitHubClient()
        content = client.download_file("alice", "repo", "SKILL.md")

    assert content == "# SKILL.md content"


def test_download_file_returns_string_content_via_base64():
    """download_file should decode base64 content when download_url is absent."""
    import base64

    raw_content = "print('hello')"
    encoded = base64.b64encode(raw_content.encode("utf-8")).decode("utf-8")

    fake_item = {"download_url": None, "content": encoded}

    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response(fake_item)
        client = GitHubClient()
        content = client.download_file("alice", "repo", "script.py")

    assert content == raw_content


def test_download_file_404_returns_none():
    """download_file should return None on a 404."""
    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response({}, status_code=404)
        client = GitHubClient()
        content = client.download_file("alice", "repo", "missing.md")

    assert content is None


def test_download_file_other_error_returns_none():
    """download_file should return None for non-404 errors."""
    with patch("skill_hunter.github_client.requests.get") as mock_get:
        mock_get.return_value = _make_mock_response({}, status_code=500)
        client = GitHubClient()
        content = client.download_file("alice", "repo", "broken.py")

    assert content is None


# -- auth headers ----------------------------------------------------------


def test_auth_headers_empty_when_no_token():
    """_auth_headers should be empty when no token is configured."""
    client = GitHubClient()
    assert client._auth_headers == {}


def test_auth_headers_bearer_when_token_present():
    """_auth_headers should include Bearer token when configured."""
    with patch(
        "skill_hunter.github_client.load_config",
        return_value={"github_token": "abc123", "lookback_days": 7, "max_results": 100},
    ):
        client = GitHubClient()
        assert client._auth_headers == {"Authorization": "Bearer abc123"}
