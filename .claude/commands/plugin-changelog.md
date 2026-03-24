# Plugin Changelog Generator

Generate a well-structured CHANGELOG.md for Claude Code plugins by reconstructing version
history from the local git log and plugin.json version bumps.

## Prerequisites

This command requires a local clone of the repo:

```bash
git clone https://github.com/anthropics/claude-plugins-official.git
cd claude-plugins-official
```

If the user already has a clone or fork, use that. Make sure you're on the `main` branch
and up to date (`git pull`).

## Why this approach works

The claude-plugins-official repo has no releases, no tags, and no changelog. But it does have
two reliable signals: the `version` field in `.claude-plugin/plugin.json` gets bumped with each
logical release, and merged PRs use conventional commit prefixes (`feat`, `fix`, `docs`). By
walking the commit history of the version file, you can identify exactly when each version was
cut, then group all commits in that plugin's directory between version bumps to build the
changelog entries.

## Workflow

### Step 1: Identify the plugin

Ask the user which plugin they want a changelog for (or infer it from context). Plugins live at:
- `external_plugins/<name>/` (community/partner plugins)
- `plugins/<name>/` (internal skills and tools)

Confirm the path exists in the local clone:
```bash
ls <repo-path>/<plugin-path>/.claude-plugin/plugin.json
```

### Step 2: Gather git data

Run the gather script for the single plugin:

```bash
python3 scripts/gather-plugin-data.py <repo-path> --plugin <plugin-path>
```

This writes a single file to `/tmp/claude-changelog-data/<plugin-safe-name>.txt`
(where `/` is replaced with `__`, e.g. `external_plugins__telegram.txt`).

Read that file — it contains:
- The current `plugin.json` (name, description, version)
- Version history: every SHA that touched `plugin.json`, with the version value at that SHA
- All non-merge commits touching the plugin directory, newest first, with full bodies

```bash
cat /tmp/claude-changelog-data/<plugin-safe-name>.txt
```

**Important version edge cases:**
- If a commit returns `"deleted"` or `"deleted/parse-error"`, that commit removed or broke
  the version field. Do not treat it as a version boundary.
- If the version field was removed entirely at some point (as happened with the Slack plugin),
  use `[Unreleased]` for changes after the last known version.
- Never invent or guess version numbers that don't appear in the version history.

### Step 3: Group commits by version

Working backwards from the newest version using the VERSION HISTORY section:

1. Find the SHA where each version was introduced
2. All commits between version N-1 and version N belong to version N
3. All commits after the latest version-bump SHA belong to `[Unreleased]`
4. All commits on or before the first version-bump SHA belong to the initial release

### Step 4: Classify changes

Use the commit message prefixes and PR titles to classify each change:

- **Added** — `feat:`, `add:`, new functionality
- **Fixed** — `fix:`, bug fixes, error handling improvements
- **Changed** — refactors, behaviour changes, config changes
- **Security** — permission changes, sanitisation, access control
- **Docs** — `docs:`, README changes

Merge commits that roll up feature branches (e.g., "Merge remote-tracking branch 'origin/kenneth/...'")
should not appear as separate entries. Instead, use the individual commits they contain, or
summarise the branch's purpose from its name and the non-merge commits within it.

When a single PR contains multiple distinct changes (common with rollup PRs), break them out as
separate bullet points rather than lumping them into one entry.

### Step 7: Write the CHANGELOG.md

Follow [Keep a Changelog](https://keepachangelog.com/) conventions:

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
- **Feature name** — description of what it does and why it matters.
  [`abc1234`](https://github.com/anthropics/claude-plugins-official/commit/abc1234) · YYYY-MM-DD ·
  ([#NNN](https://github.com/anthropics/claude-plugins-official/pull/NNN))

### Fixed
- **Bug name** — what was broken and how it's fixed.
  [`abc1234`](https://github.com/anthropics/claude-plugins-official/commit/abc1234) · YYYY-MM-DD ·
  ([#NNN](https://github.com/anthropics/claude-plugins-official/pull/NNN))
```

Deriving the title:
- Read the `name` field from the plugin's `.claude-plugin/plugin.json` and use it as the
  `<Plugin Name>`. For example, if the name is "telegram", title it "Changelog — Telegram".
  Capitalise the first letter. Do NOT append "Channel Plugin", "Skill", or any other suffix
  unless it's part of the actual name field.

Key formatting rules:
- Each entry starts with a bold short name, followed by an em dash and a plain-English description
- Every entry includes a commit reference line below the description with: short SHA (linked), commit date, and PR link
- Format: `` [`sha`](commit-url) · YYYY-MM-DD · ([#NNN](pr-url)) ``
- The commit date makes staleness visible — readers can see at a glance how long changes have been sitting unreleased
- The version header date (## [X.Y.Z] — YYYY-MM-DD) should use the date of the version-bump commit
- For [Unreleased], omit the date from the header but individual entries still show their commit dates
- Group by version, newest first
- Within each version, group by change type (Added, Fixed, Changed, Security, Docs)
- If a version has a notable event (like being temporarily removed and restored), add a **Note** section
- The initial release should describe the core capabilities, not just say "initial release"

### Step 8: Repo-level rollup changelog (if generating for multiple plugins)

If the user asks for changelogs across multiple plugins, or for the whole repo, generate
per-plugin changelogs first (one CHANGELOG.md per plugin directory), then create a repo-level
`CHANGELOG.md` at the root that serves as a summary timeline.

The repo-level changelog groups entries by date, with one-line summaries per plugin version
that link to the detailed per-plugin changelog:

```markdown
---
layout: default
render_with_liquid: false
---

# Changelog — Claude Code Plugins

Summary of all plugin releases in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).
See each plugin's CHANGELOG.md for full details.

---

## 2026-03-24

### telegram → [0.0.4](external_plugins/telegram/CHANGELOG.html)
Compact permission messages, inline approval buttons.

### discord → [0.0.4](external_plugins/discord/CHANGELOG.html)
Compact permission messages, inline approval buttons.
```

The one-line summary should capture the headline feature(s) of that version — think of it as
the commit message for the version. Keep it under 80 characters.

To build this, iterate over all plugins that have `.claude-plugin/plugin.json`, generate their
individual changelogs, then merge the version dates into a single timeline sorted newest-first.

### Step 9: Deliver

Save per-plugin changelogs as `<plugin-path>/CHANGELOG.md` and regenerate the rollup using
`--rollup-only` so other per-plugin changelogs are not overwritten:

```bash
python3 scripts/generate-changelogs.py <repo-path> --output-dir docs --rollup-only
```

Every CHANGELOG.md must include the Jekyll front matter block at the top
(layout + render_with_liquid). If the user only asked for a single plugin, just deliver
that one file (skip the rollup step).

If the user wants to submit this as a PR, note that they'll need to fork the repo and create
the PR themselves (or use `gh` CLI if they have it installed).

## Edge cases

- **No plugin.json versions**: Some older plugins may not have version bumps, or the version
  field may have been removed. In this case, use `[Unreleased]` for changes after the last
  known version, or group all changes under a single initial version if only one version
  ever existed. Never fabricate version numbers — only use versions that actually appeared
  in plugin.json at some point in the commit history.
- **Rollup PRs**: Large PRs that merge multiple feature branches should be decomposed into
  their constituent changes. Look at the individual commits within the PR, not just the merge
  commit message.
- **Deleted and restored plugins**: If a plugin was removed and re-added (as happened with
  the channel plugins), note this in the changelog but don't treat the removal as a version.
- **Large repos**: For plugins with very long histories, use `git log` ranges (Step 5) to
  avoid processing the entire repo history when you only need a subset.
