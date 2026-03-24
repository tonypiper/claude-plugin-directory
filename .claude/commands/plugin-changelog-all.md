# Plugin Changelog Generator — All Plugins

Generate intelligent changelogs for all plugins in the official repo using parallel subagents,
one per plugin, to avoid context exhaustion.

## Prerequisites

Requires a local clone of the official repo. If not present:

```bash
git clone https://github.com/anthropics/claude-plugins-official.git
```

Default expected location: `../claude-plugins-official` (sibling of this repo).
If the clone is elsewhere, ask the user for the path.

## Step 1: Discover all plugins

```bash
find <repo-path> -name "plugin.json" -path "*/.claude-plugin/*" | sort
```

This gives the full list of plugins. Extract the plugin path (e.g. `external_plugins/telegram`)
from each result by stripping `/.claude-plugin/plugin.json`.

## Step 2: Assess complexity

For each plugin, quickly check how many version bumps and commits it has:

```python
import subprocess, json

repo = "<repo-path>"
for plugin_path in plugins:
    versions = subprocess.run(
        ["git", "-C", repo, "log", "--oneline", "--", f"{plugin_path}/.claude-plugin/plugin.json"],
        capture_output=True, text=True
    ).stdout.strip().split("\n")

    commits = subprocess.run(
        ["git", "-C", repo, "log", "--oneline", "--no-merges", "--", plugin_path],
        capture_output=True, text=True
    ).stdout.strip().split("\n")

    print(f"{plugin_path}: {len(versions)} version commits, {len(commits)} total commits")
```

Use this to decide batching:
- **Simple** (1 version, ≤5 commits): batch up to 6 per agent
- **Medium** (2-3 versions, ≤15 commits): 2-3 per agent
- **Complex** (4+ versions or rich commit bodies like Telegram): 1 per agent

## Step 3: Launch agents in parallel

Use the Agent tool to launch multiple subagents simultaneously. Each agent receives:

1. The list of plugin paths it is responsible for
2. The repo path
3. The output directory path (`docs/` in this repo)
4. The full changelog format spec (below)

**Important:** Pass all agents in a single message to run them in parallel.

## Agent prompt template

Use this as the prompt for each subagent:

---

You are generating CHANGELOG.md files for Claude Code plugins by manually analysing git history.
Do NOT use any Python generator script. Use git commands directly.

**Repo path:** `<repo-path>`
**Output base:** `<output-dir>`
**Plugins to process:** `<plugin-path-1>`, `<plugin-path-2>`, ...

For each plugin:

### 1. Get version history

```bash
python3 -c "
import subprocess, json
repo = '<repo-path>'
plugin = '<plugin-path>'
result = subprocess.run(['git', '-C', repo, 'log', '--pretty=format:%h\t%ai\t%s', '--', f'{plugin}/.claude-plugin/plugin.json'], capture_output=True, text=True)
for line in result.stdout.strip().split('\n'):
    sha, date, subject = line.split('\t', 2)
    content = subprocess.run(['git', '-C', repo, 'show', f'{sha}:{plugin}/.claude-plugin/plugin.json'], capture_output=True, text=True)
    try: version = json.loads(content.stdout).get('version', 'deleted')
    except: version = 'deleted'
    print(f'{sha}  {version}  {date[:10]}  {subject}')
"
```

### 2. Get all commits with bodies

```bash
python3 -c "
import subprocess
repo = '<repo-path>'
plugin = '<plugin-path>'
result = subprocess.run(['git', '-C', repo, 'log', '--pretty=format:%h\t%ai\t%s\t%b', '--no-merges', '--', plugin], capture_output=True, text=True)
print(result.stdout)
"
```

Read the commit bodies carefully — they often contain the real explanation of why a change was made.

### 3. Group commits by version

Map each commit to a version section based on date ranges between version bumps:
- Commits after the latest version bump → `[Unreleased]`
- Commits between two version bumps → the newer version
- Commits before the first version bump → the initial version

### 4. Classify each commit

- `feat:` / `add:` / new capability → **Added**
- `fix:` / bug / crash / error handling → **Fixed**
- refactor / config / behaviour change → **Changed**
- permission / sanitize / credential / security → **Security**
- `docs:` / README → **Docs**

Skip merge commits. When a commit touches both plugins (e.g. telegram+discord together),
include it in both changelogs with appropriate descriptions.

### 5. Write the CHANGELOG.md

Write to `<output-dir>/<plugin-path>/CHANGELOG.md`. Use this format:

```markdown
---
layout: default
render_with_liquid: false
---

# Changelog — <Plugin Name>

All notable changes to `<plugin-path>` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/<plugin-path>).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [X.Y.Z] — YYYY-MM-DD

### Added
- **Short name** — Plain-English explanation of what it does and why it matters.
  [`abc1234`](https://github.com/anthropics/claude-plugins-official/commit/<full-sha>) · YYYY-MM-DD · ([#NNN](https://github.com/anthropics/claude-plugins-official/pull/NNN))
```

Rules:
- Title: read `name` from plugin.json, capitalise first letter only
- Descriptions must explain the *why*, not just restate the commit subject
- Read commit bodies for context — they often explain the root cause or motivation
- Group by version newest-first, then by category (Added, Changed, Fixed, Security, Docs)
- If a plugin was deleted and restored, add a `> **Note:**` blockquote in that version
- For plugins with no version field, use `[Unreleased]` for all commits
- Do NOT invent version numbers

Write each file, then confirm the path written.

---

## Step 4: Generate updated rollup

After all agents complete, regenerate `docs/CHANGELOG.md` by running the Python script
with `--rollup` only (this part is mechanical and doesn't need summarisation):

```bash
python3 scripts/generate-changelogs.py <repo-path> --output-dir docs --rollup
```

Then manually check the rollup file has proper front matter (`render_with_liquid: false`).

## Step 5: Commit and push

```bash
git add -A
git commit -m "Regenerate all changelogs with intelligent summarisation"
git push
```
