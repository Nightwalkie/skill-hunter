---
name: skill-hunter
description: Search GitHub for newly published or updated Claude Code Skills from the past week, filter them with AI, and generate a bilingual report with detailed descriptions.
---

# skill-hunter

This skill defines the Agent workflow for `/skill-hunter`. The crawler script handles searching GitHub and downloading raw data. The Agent handles judgment, description generation, and report writing.

## Workflow

**Path definitions for this run:**
- `SKILL_DIR` = directory containing this SKILL.md
- `SCRIPTS` = `SKILL_DIR/scripts/`
- `CWD` = the user's current working directory (where they invoked the skill)
- Output files (`raw-data.json`, `skill-index.json`, reports) appear under `<CWD>/`

**Critical rules for the Agent:**
- Process entries ONE AT A TIME. Never read the full raw-data.json.
- Do NOT spawn sub-agents or background tasks for filtering/describing.
- Do NOT write temporary Python scripts for report generation — use Bash append (>>) or inline Python.
- Keep all work in the main session. Batch processing is slower, not faster.

Follow these steps in order. Stop at any step if a required condition is not met.

### Step 0 — Ensure config.json exists and token is valid

Check if `<SCRIPTS>/config.json` exists by reading it.

**If config.json does not exist:**
1. Tell the user: "skill-hunter needs a GitHub Personal Access Token to search. Get one at https://github.com/settings/tokens — click 'Generate new token (classic)', check 'public_repo', and paste the token here."
2. Wait for the user to provide the token.
3. Create `<SCRIPTS>/config.json` with:
   ```json
   {
     "github_token": "<user's token>",
     "lookback_days": 7,
     "max_results": 100
   }
   ```
4. Continue to Step 1.

**If config.json exists but github_token is empty:**
1. Tell the user: "config.json exists but no token is set. Please provide your GitHub Personal Access Token (with public_repo scope) from https://github.com/settings/tokens"
2. Wait for the user to provide the token.
3. Update `<SCRIPTS>/config.json` with the new token.
4. Continue to Step 1.

**If config.json exists with a non-empty token:**
Just continue to Step 1. The crawler will validate the token — if it's expired or invalid, the crawler will report the specific error.

**If the crawler reports token is invalid or expired (in Step 1):**
1. Tell the user: "Your GitHub token appears to be invalid or expired. Please generate a new one at https://github.com/settings/tokens (check 'public_repo') and paste it here."
2. Wait for the user to provide the new token.
3. Update `<SCRIPTS>/config.json` with the new token.
4. Re-run: `python "<SCRIPTS>/crawler.py"`

### Step 1: Run the Crawler

Execute the crawler script:

```bash
python "<SCRIPTS>/crawler.py"
```

The crawler will:
- Search GitHub for repos containing `SKILL.md` and `claude code` published/updated within the configured lookback window (`<SCRIPTS>/config.json` -> `lookback_days`, default 7 days).
- Classify candidates against `<CWD>/skill-index.json` as **new**, **updated**, or **skip**.
- Download `README.md` content and repo metadata for each candidate.
- Write the results to `<CWD>/raw-data.json`.

If the script fails (non-zero exit code), report the error to the user and **stop here**.

### Step 2: Check raw-data.json exists

Use a lightweight check to confirm `<CWD>/raw-data.json` exists and is non-empty:

```bash
python -c "
import json, os
path = r"<CWD>/raw-data.json"
if not os.path.exists(path):
    print('MISSING')
else:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not data:
        print('EMPTY')
    else:
        print(f'OK:{len(data)}')
"
```

If the file is missing or the array is empty, tell the user:

> No new skills found this week.

Then **stop here**. The crawler already printed "No new or updated skills found this week." in this case, but confirm it for the user.

### Step 3 — Extract metadata summary (lightweight)

Run a Python one-liner to print a compact list of all entries WITHOUT the README content:

```bash
python -c "
import json, sys
with open(r"<CWD>/raw-data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f'Total entries: {len(data)}')
for i, entry in enumerate(data):
    print(f'{i}|{entry[\"owner\"]}/{entry[\"repo\"]}|stars={entry[\"stars\"]}|status={entry[\"index_status\"]}|published={entry[\"publish_date\"][:10]}')
"
```

Read this compact list to understand what you are working with. This gives you the index, owner/repo, star count, status, and publish date for every entry — without any README content.

### Step 4 — Initialize the report

Declare the report file path and write the header:

```bash
REPORT_FILE="<CWD>/Github Report $(date +%Y-%m-%d) $(date +%H-%M).md"
echo "# Github Report $(date +%Y-%m-%d) $(date +%H-%M)" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## New Skills" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
```

Use `$REPORT_FILE` in all subsequent commands that append to the report.

### Step 5 — Process one by one

**CRITICAL RULES:**
- Process entries ONE at a time. Do NOT read the full raw-data.json.
- For each entry, use Python to extract ONLY that entry's data.
- Judge it immediately, write to the report immediately.
- Do NOT spawn sub-agents or background tasks for this — do it in the main session.
- Do NOT batch entries together.

For each entry index `N` (starting from 0):

#### 5a. Extract this entry's README content

```bash
python -c "
import json
with open(r"<CWD>/raw-data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
entry = data[N]
print(f'OWNER: {entry[\"owner\"]}')
print(f'REPO: {entry[\"repo\"]}')
print(f'STARS: {entry[\"stars\"]}')
print(f'STATUS: {entry[\"index_status\"]}')
print(f'PUBLISHED: {entry[\"publish_date\"][:10]}')
print('---README---')
print(entry['readme_content'][:3000])
"
```

Truncate to 3000 chars for reading — the full README is in raw-data.json if needed.

#### 5b. Whitelist check

If the entry's `index_status` is `"updated"`, this repo is already in the skill index. SKIP the AI filter step — it is a known skill. Jump to step 5c to generate descriptions directly.

If the status is `"new"`, judge whether this is a genuine Claude Code Skill repo based on the README content:
- README describes skills available in the repo
- Mentions Claude Code or AI coding agents
- Explains how to install/use the skills
- Has sections listing skills or commands
- Is NOT a tutorial, template, library, tool, or generic project that only mentions "skill" in passing

#### 5c. If confirmed as a genuine skill repo

Generate:
- `description_en`: 2-4 English sentences summarizing what skills this repo offers
- `description_zh`: 2-4 Chinese sentences (natural Chinese, not stiff translation)

Then append to the report using Python (safest for entries that may contain backticks, `$`, or special characters):

```bash
python -c "
entry = '''### {owner}/{repo}
- **Author**: {owner}
- **Stars**: {stars}
- **Discovered**: {today's date}
- **First Published**: {publish_date}
- **Status**: {index_status}

**English Description**: {description_en}

**中文描述**: {description_zh}

---
'''
import os
report_file = os.environ.get('REPORT_FILE', r"<CWD>/Github Report fallback.md")
with open(report_file, 'a', encoding='utf-8') as f:
    f.write(entry)
"
```

Replace `{owner}`, `{repo}`, `{stars}`, `{today's date}`, `{publish_date}`, `{index_status}`, `{description_en}`, and `{description_zh}` with the actual values. Use `$REPORT_FILE` environment variable or the known report path.

#### 5d. If NOT a genuine skill repo

Print: `Skipping {owner}/{repo} — not a skill repo` and continue to the next entry.

#### 5e. Move to next entry

Repeat 5a-5d for entry N+1, N+2, etc., until all entries are processed.

### Step 6 — Finalize report

After all entries are processed, add the "Updated Skills" section:

```bash
echo "" >> "$REPORT_FILE"
echo "## Updated Skills" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
```

If there were entries with `index_status: "updated"`, they have already been written in the loop above. If none were processed, write "None this week.":

```bash
echo "None this week." >> "$REPORT_FILE"
```

### Step 7 — Update the index

Add all confirmed skills to `<CWD>/skill-index.json` using the `IndexManager.add_entries()` method. Collect the entries you confirmed during Step 5 and pass them as a Python list:

```python
import json, sys
from datetime import datetime, timezone
sys.path.insert(0, r"<SCRIPTS>")
from index_manager import IndexManager

im = IndexManager()

# Collect all confirmed entries from Step 5 (both new and updated).
# Each dict must have: owner, repo, publish_date, last_update.
entries = [
    {'owner': '...', 'repo': '...', 'publish_date': '...', 'last_update': '...'},
    # ... more entries
]

if entries:
    im.add_entries(entries)
    print(f'Index updated with {len(entries)} entries.')
else:
    print('No new entries to add.')
```

Replace the `entries` list with the actual confirmed entries from Step 5. The `add_entries()` method sets `last_discovered` to the current UTC time automatically.

**Do NOT re-run the crawler.** This step only updates the index to track which skills have been processed, so they are recognized as "known" on the next run.

### Step 8 — Done

Tell the user where the report file is located and provide a summary:

> Found X new skills, Y updated skills. Report: $REPORT_FILE

(Replace X and Y with the actual counts from your processing, and `$REPORT_FILE` with the actual report path.)

## Important Notes

- **Crawler's job:** Searching, downloading `README.md` files, classifying against the existing index (`new` / `updated` / `skip`), and writing `<CWD>/raw-data.json`.
- **Agent's job:** AI filtering (Step 5b), generating descriptions (Step 5c), writing the report (Steps 4-6), and updating the index (Step 7).
- **One-by-one processing:** Use inline Python one-liners to extract a single entry at a time. Never load the full raw-data.json into the Agent's Read tool — it can be 500KB+ and will cause wasteful behavior.
- **No sub-agents:** Do not spawn sub-agents or background tasks for filtering or describing. All processing happens in the main session, one entry at a time.
- **CLAUDE.md compliance:** Delegate Python execution work to scripts (crawler, inline IndexManager snippet). The Agent makes judgment calls (filtering, descriptions) and writes the report.
- **HITL gate:** After writing the report, do NOT commit or push. The user reviews the report before any git operations.
