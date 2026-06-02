---
name: skill-hunter
description: Search GitHub for newly published or updated Claude Code Skills from the past week, filter them with AI, and generate a bilingual report with detailed descriptions.
---

# skill-hunter

This skill defines the Agent workflow for `/skill-hunter`. The crawler script (`skill_hunter/crawler.py`) handles searching GitHub and downloading raw data. The Agent handles judgment, description generation, and report writing.

## Workflow

Follow these steps in order. Stop at any step if a required condition is not met.

### Step 1: Run the Crawler

Execute the crawler script from the project root:

```bash
python skill_hunter/crawler.py
```

The crawler will:
- Search GitHub for repos containing `SKILL.md` and `claude code` published/updated within the configured lookback window (`config.json` -> `lookback_days`, default 7 days).
- Classify candidates against `skill-index.json` as **new**, **updated**, or **skip**.
- Download `SKILL.md` content and repo metadata for each candidate.
- Write the results to `raw-data.json` in the project root.

If the script fails (non-zero exit code), report the error to the user and **stop here**.

### Step 2: Read raw-data.json

Use the Read tool to load `raw-data.json` from the project root. Do NOT use `cat` or shell commands to read it.

If the file is missing, the JSON array is empty (`[]`), or the array contains no entries, tell the user:

> No new skills found this week.

Then **stop here**. The crawler already printed "No new or updated skills found this week." in this case, but confirm it for the user.

### Step 3: Filter Candidates with AI

For each entry in `raw-data.json`, inspect the `skill_md_content` field to determine whether it is a genuine Claude Code Skill.

**Whitelist rule (skip AI filter):** If `index_status` is `"updated"`, the skill is already confirmed in `skill-index.json`. Trust it as genuine and skip AI judgment.

**For `index_status: "new"` entries**, apply these checks:

1. **YAML frontmatter:** Does the `skill_md_content` start with `---` and contain `name:` and `description:` fields? Skills MUST have both.
2. **Skill document structure:** Does the content read like a Claude Code skill instruction document? Look for typical sections such as:
   - `what-to-do` / `workflow` / `process` / `steps` / `instructions`
   - `supporting-info` / `context` / `guidelines`
   - Any structured workflow or step-by-step guidance for an AI agent
3. **Discard** entries that are NOT real skills — for example, a generic `SKILL.md` that describes a project's own build steps, or a markdown file that happens to be named `SKILL.md` but has no Claude Code skill structure.

After filtering, print a summary to the user:

> AI filtering: N confirmed skills, M discarded

### Step 4: Generate Bilingual Descriptions

For each **confirmed** skill (both new and updated entries that pass Step 3), read the full `skill_md_content` and produce two descriptions:

- **`description_en`**: 2-4 English sentences summarizing what the skill does, when to use it, and what problem it solves. Write naturally — this is not a translation of the Chinese version.
- **`description_zh`**: 2-4 Chinese sentences covering the same information, written naturally in Chinese. Not a stiff word-for-word translation of the English version.

**Multi-skill repos:** Some repositories contain more than one `SKILL.md` (e.g., in subdirectories). The `skill_md_content` field will already contain all of them concatenated (the crawler handles this). When generating descriptions, summarize all skills in the repo together — describe the collection as a whole rather than each individual file.

### Step 5: Write the Report

Create `Github Report YYYY-MM-DD.md` in the project root, using the current date (e.g., `Github Report 2026-06-02.md`). Use this exact format:

```markdown
# Github Report YYYY-MM-DD

## New Skills

### owner/repo
- **Author**: owner
- **Stars**: N
- **Discovered**: YYYY-MM-DD
- **First Published**: YYYY-MM-DD
- **Status**: new

**English Description**: <description_en>

**中文描述**: <description_zh>

---

### owner/repo
(follow same format)

## Updated Skills

### owner/repo
- **Author**: owner
- **Stars**: N
- **Discovered**: YYYY-MM-DD
- **First Published**: YYYY-MM-DD
- **Status**: updated

**English Description**: <description_en>

**中文描述**: <description_zh>

---
```

**Rules:**
- Separate **New Skills** and **Updated Skills** into their own sections.
- Sort new skills first, then updated skills. Within each section, order by `stars` descending.
- If a section has no entries, write: `None this week.`
- The `owner/repo` heading links to `https://github.com/owner/repo`.
- **`Discovered`**: Use **today's date** (the date this report is generated, the date the crawler actually ran). Format: `YYYY-MM-DD`.
- **`First Published`**: Use the `publish_date` field from `raw-data.json` (when the repo was first created on GitHub, i.e., `created_at`). Only include this line if `publish_date` differs from today's date.
- **`Stars`**: Use the `stars` field from `raw-data.json`.

**Field meanings in raw-data.json:**
- `publish_date`: When the repo was first created on GitHub (`created_at`). This is the repo's original publication date, NOT the discovery date.
- `last_update`: When the repo was last pushed to (`pushed_at`).
- `Discovered` in the report: Today's date (when the crawler found and processed it).

### Step 6: Update the Index

Add all confirmed skills to `skill-index.json` using the `IndexManager.add_entries()` method. Run this as a small inline Python snippet from the project root:

```python
import json, sys
sys.path.insert(0, ".")
from skill_hunter.index_manager import IndexManager

entries = <paste the list of confirmed entry dicts here as a Python literal>

IndexManager().add_entries(entries)
print("Index updated.")
```

Replace `<paste the list...>` with an actual Python list of dicts. Each dict must have these keys: `owner`, `repo`, `publish_date`, `last_update`. The `add_entries()` method sets `last_discovered` to the current UTC time automatically.

**Do NOT re-run the crawler.** This step only updates the index to track which skills have been processed, so they are recognized as "known" on the next run.

### Step 7: Done

Tell the user where the report file is located and provide a summary:

> Found N new skills and M updated skills. Report: Github Report YYYY-MM-DD.md

## Important Notes

- **Crawler's job:** Searching, downloading `SKILL.md` files, classifying against the existing index (`new` / `updated` / `skip`), and writing `raw-data.json`.
- **Agent's job:** AI filtering (Step 3), generating descriptions (Step 4), writing the report (Step 5), and updating the index (Step 6).
- **Read tool:** Always use the Read tool to read `raw-data.json` — do not shell out to `cat`/`grep`/`jq`.
- **CLAUDE.md compliance:** Delegate Python execution work to scripts (crawler, inline IndexManager snippet). The Agent makes judgment calls (filtering, descriptions) and writes the report.
- **HITL gate:** After writing the report, do NOT commit or push. The user reviews the report before any git operations.
