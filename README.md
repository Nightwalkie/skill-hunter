# Skill Hunter

![License](https://img.shields.io/github/license/Nightwalkie/skill-hunter)
![Stars](https://img.shields.io/github/stars/Nightwalkie/skill-hunter)
![Forks](https://img.shields.io/github/forks/Nightwalkie/skill-hunter)
![Release](https://img.shields.io/github/v/release/Nightwalkie/skill-hunter)
![Last Commit](https://img.shields.io/github/last-commit/Nightwalkie/skill-hunter)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

Automatically discover new Claude Code Skills published on GitHub each week, with AI-generated bilingual descriptions.

## What it does

Skill Hunter searches GitHub for newly published or updated Claude Code Skill repositories, downloads their README files, and uses AI to filter genuine skill repos and generate Chinese + English descriptions. The result is a clean Markdown report sorted by stars.

1. **Search** — Queries GitHub for repos mentioning "SKILL.md" and "claude code", pushed in the last 7 days
2. **Validate** — Verifies your GitHub token has the required permissions
3. **Download** — Fetches README.md from each candidate repository
4. **Filter** — AI reads each README and judges whether it's a genuine skill repository
5. **Describe** — AI generates natural Chinese and English descriptions of the skills
6. **Report** — Writes a timestamped `Github Report YYYY-MM-DD HH-MM.md` to your project root

## Prerequisites

- Python 3.8+ (standard library only — no pip install needed)
- GitHub Personal Access Token with `public_repo` scope ([create one here](https://github.com/settings/tokens))

## Installation

```bash
npx skills add Nightwalkie/skill-hunter -g
```

## Usage

Run `/skill-hunter` in Claude Code.

On first run, add your GitHub token to `skills/skill-hunter/scripts/config.json`:
```json
{
  "github_token": "ghp_xxxxxxxxxxxx",
  "lookback_days": 7,
  "max_results": 100
}
```

The token is validated before each run and never leaves your machine.

Output:
- `Github Report YYYY-MM-DD HH-MM.md` — Human-readable report with bilingual skill descriptions
- `skill-index.json` — Persistent index tracking discovered repos (skips unchanged repos on subsequent runs)

## How it works

### Search

Uses the GitHub Repository Search API with the query `"SKILL.md" "claude code" pushed:>YYYY-MM-DD` to find repos that mention both terms and were recently updated. The date range is configurable via `lookback_days`.

### Download

For each candidate not already in the local index, downloads the repository's `README.md` file and metadata (stars, dates). Repos already in the index are skipped unless they've been updated since the last discovery.

### AI Processing

The downloaded README files are passed to Claude, which:
- **Filters out** non-skill repos (tutorials, tools, templates, etc.)
- **Generates** a 2-4 sentence English description and a 2-4 sentence Chinese description for each confirmed skill
- **Writes** a timestamped report sorted by star count

## Configuration

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `github_token` | Yes | — | GitHub Personal Access Token with `public_repo` scope |
| `lookback_days` | No | 7 | Number of days to look back for new repos |
| `max_results` | No | 100 | Maximum search results to process |

## Output

| File | Description |
|------|-------------|
| `Github Report YYYY-MM-DD HH-MM.md` | Human-readable report with author, stars, bilingual descriptions for each discovered skill |
| `skill-index.json` | Machine-readable index tracking all discovered repos (enables deduplication across runs) |

## License

MIT © [Nightwalkie](https://github.com/Nightwalkie)

## Author

[Nightwalkie](https://github.com/Nightwalkie)
