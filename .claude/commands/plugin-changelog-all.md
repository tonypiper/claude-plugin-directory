# Plugin Changelog Generator — All Plugins

Generate intelligent changelogs for all plugins by using a shell script to gather git data
in parallel, then processing each plugin in the main session to write well-described changelogs.

This approach avoids subagents needing Bash permission (which requires interactive approval
per-agent and breaks parallel workflows). All git work happens in one shell pass; all analysis
and writing happens in the main Claude session.

## Prerequisites

Requires a local clone of the official repo. If not present:

```bash
git clone https://github.com/anthropics/claude-plugins-official.git
```

Default expected location: `../claude-plugins-official` (sibling of this repo).
If the clone is elsewhere, ask the user for the path.

## Step 1: Pull latest and discover plugins

```bash
cd <repo-path> && git pull --ff-only
find <repo-path> -name "plugin.json" -path "*/.claude-plugin/*" | sort
```

Extract the plugin path (e.g. `external_plugins/telegram`) from each result by stripping
the repo prefix and `/.claude-plugin/plugin.json` suffix.

## Step 2: Gather all git data in one pass

Run the gather script to dump version history, commits, and plugin.json content for every
plugin into temp files:

```bash
python3 scripts/gather-plugin-data.py <repo-path>
```

This writes one file per plugin to `/tmp/claude-changelog-data/<plugin-safe-name>.txt`
(where `/` in the plugin path is replaced with `__`, e.g. `external_plugins__telegram.txt`).

Each file contains everything needed to write the changelog without any further git calls.
The script takes ~5–10 seconds for the full repo.

## Step 3: Assess complexity and decide processing order

Read a few of the gathered data files to understand the landscape. For each plugin, count:
- **Version bumps** — lines in the `=== VERSION HISTORY ===` section
- **Commits** — count `COMMIT ` lines in the `=== COMMITS ===` section

Prioritise:
- **Complex** (4+ versions OR 15+ commits): process individually, write carefully
- **Medium** (2–3 versions, up to 15 commits): process in batches of 3–4
- **Simple** (1 version, ≤5 commits): batch up to 6 at once

Process complex plugins first — they benefit most from careful descriptions.

## Step 4: Process each plugin (or batch)

For each plugin (or batch), read the gathered data file(s) and write the changelog.

```bash
cat /tmp/claude-changelog-data/<plugin-safe-name>.txt
```

Where `<plugin-safe-name>` replaces `/` with `__` (e.g. `external_plugins__telegram.txt`).

Then write `docs/<plugin-path>/CHANGELOG.md` using the format below.

**Important:** Read the full commit bodies — they explain *why* changes were made and are
the key difference between an intelligent changelog and one that just restates commit subjects.

### Changelog format

```markdown
---
layout: default
render_with_liquid: false
---

# Changelog — <Plugin Name>

> <description from plugin.json>

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

### Writing rules

- **Title:** read `name` from plugin.json, capitalise first letter only. No suffix ("Plugin", "Skill", etc.)
- **Descriptions:** explain the *why*, not just restate the commit subject. Use commit bodies.
- **Grouping:** newest version first, then by category within each version: Added → Changed → Fixed → Security → Docs
- **Version date:** use the date of the version-bump commit
- **[Unreleased]:** omit the date from the header; individual entries still show their commit dates
- **Deleted/restored plugins:** add a `> **Note:**` blockquote in the affected version section
- **No invented versions:** only use version numbers that actually appeared in plugin.json
- **PR links:** extract from `(#NNN)` in commit subjects — `([#NNN](https://github.com/anthropics/claude-plugins-official/pull/NNN))`; omit if absent
- **Commit deduplication:** when a commit touches multiple plugins (common for telegram+discord), include it in both with appropriate per-plugin descriptions
- **Skip** true merge commits (subject starts with "Merge pull request" or "Merge branch") that add no content of their own

### Grouping commits by version

Working backwards from newest:
- Commits dated **after** the latest version-bump SHA → `[Unreleased]`
- Commits dated **between** two consecutive version-bump SHAs → the newer version
- Commits dated **on or before** the first version-bump SHA → the initial version

The version-bump SHA itself belongs to the version it introduced.

## Step 5: Generate updated rollup

After all per-plugin changelogs are written, regenerate the rollup:

```bash
python3 scripts/generate-changelogs.py <repo-path> --output-dir docs --rollup
```

Check that `docs/CHANGELOG.md` has `render_with_liquid: false` in its front matter.

## Step 6: Commit

```bash
git add -A
git commit -m "Regenerate all changelogs with intelligent summarisation"
git push
```

## Notes

- The data-gathering script (Step 2) runs in ~5–10 seconds for the full repo and is safe
  to re-run — it just overwrites the temp files.
- If a plugin's history is too large to process in one context pass, read only the version
  history section first to understand the structure, then read commits section by section.
- Plugins that were recently added but have no interesting commits (just "initial scaffolding"
  type entries) are fine to describe briefly — don't pad them with filler.
