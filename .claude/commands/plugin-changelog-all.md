# Plugin Changelog Generator — All Plugins

Generate intelligent changelogs for all plugins using a 3-tier approach: the Python generator
handles simple plugins for free (zero tokens), AI rewrites are reserved for complex/medium
plugins with meaningful history.

## Prerequisites

Requires a local clone of the official repo. If not present:

```bash
git clone https://github.com/anthropics/claude-plugins-official.git
```

Default expected location: `../claude-plugins-official` (sibling of this repo).
If the clone is elsewhere, ask the user for the path.

---

## Step 1: Pull latest and gather all data

```bash
cd <repo-path> && git pull --ff-only
python3 scripts/gather-plugin-data.py <repo-path>
```

The gather script writes one file per plugin to `/tmp/claude-changelog-data/<plugin-safe-name>.txt`
(where `/` in the plugin path is replaced with `__`, e.g. `external_plugins__telegram.txt`).
It takes ~5–10 seconds for the full repo and is safe to re-run.

## Step 2: Run generator for ALL plugins (baseline)

```bash
python3 scripts/generate-changelogs.py <repo-path> --output-dir docs
```

This writes all 36 per-plugin changelogs using commit subjects + bodies. For Tier 3 plugins
(simple history) this is the **final output** — do not reprocess them.

## Step 3: Classify plugins into tiers

For each `/tmp/claude-changelog-data/*.txt` file, count:
- **V** = number of lines in the `=== VERSION HISTORY ===` section
- **C** = number of `COMMIT ` lines in the `=== COMMITS ===` section

Classify:
- **Tier 1 — Complex** (V ≥ 4 OR C ≥ 15): process individually, full AI rewrite
- **Tier 2 — Medium** (V ≥ 2 OR C ≥ 6): process in batches of 3
- **Tier 3 — Simple** (everything else): generator output is final — **do not read these data files**

## Step 4: Check staleness for Tier 1 and Tier 2 plugins

Before rewriting a Tier 1/2 changelog, check if the most recent commit SHA from its data
file already appears in the existing `docs/<plugin>/CHANGELOG.md`. If present → already
up to date, skip. If absent → needs rewrite.

```bash
# Extract the most recent commit SHA from the data file
grep '^COMMIT ' /tmp/claude-changelog-data/<plugin-safe-name>.txt | head -1 | awk '{print $2}' | cut -c1-7
# Check if it's already in the changelog
grep "<short-sha>" docs/<plugin-path>/CHANGELOG.md
```

## Step 5: AI rewrites — Tier 1 individually, Tier 2 in batches of 3

For each plugin needing a rewrite:

```bash
cat /tmp/claude-changelog-data/<plugin-safe-name>.txt
```

Read the full data file and write `docs/<plugin-path>/CHANGELOG.md` using the format below.
This overwrites the generator output for that plugin only.

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

## Step 6: Regenerate rollup and index ONLY

After all AI rewrites are done, regenerate the rollup changelog and plugin index without
touching any per-plugin files:

```bash
python3 scripts/generate-changelogs.py <repo-path> --output-dir docs --rollup-only
```

Verify `docs/CHANGELOG.md` has `render_with_liquid: false` in its front matter.

## Step 7: Commit

```bash
git add -A
git commit -m "Regenerate all changelogs with intelligent summarisation"
git push
```

## Notes

- **Do not read Tier 3 data files.** The generator output is the final answer for these plugins.
- **Step 6 uses `--rollup-only`.** This never touches per-plugin changelogs, so AI-written
  changelogs are safe from being overwritten.
- Token budget: ~0 for routine runs with no Tier 1/2 activity; ~8–10K to rewrite a single
  updated Tier 1 plugin; ~35K for a full first run.
- If a plugin's history is too large to process in one context pass, read only the version
  history section first to understand the structure, then read commits section by section.
