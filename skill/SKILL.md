---
name: plugin-changelog
description: >
  Generate a CHANGELOG.md for any plugin in the anthropics/claude-plugins-official repository
  by analysing merged PRs, commit history, and version bumps in plugin.json. Use this skill
  whenever the user asks to create, update, or compile a changelog for a Claude Code plugin,
  or wants to understand what changed between plugin versions. Also trigger when the user
  mentions "release notes", "version history", or "what shipped" in the context of Claude Code
  plugins. Works for any plugin under external_plugins/ or plugins/ in the official repo.
---

# Plugin Changelog Generator

Generate a well-structured CHANGELOG.md for Claude Code plugins by reconstructing version
history from the local git log and plugin.json version bumps.

## Prerequisites

This skill requires a local clone of the repo:

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
ls <plugin-path>/.claude-plugin/plugin.json
```

### Step 2: Get the version history

Use `git log` to fetch the commit history for the plugin's version file. This tells you when
each version was cut and by whom.

```bash
git log --pretty=format:'%h  %ai  %an  %s' -- <plugin-path>/.claude-plugin/plugin.json
```

This gives you a list of every commit that touched plugin.json, with short SHA, author date,
author name, and subject line.

### Step 3: Get the version value at each commit

For each commit that touched plugin.json, read the file content at that commit to extract the
actual version number:

```bash
git show <sha>:<plugin-path>/.claude-plugin/plugin.json | python3 -c "import json,sys; print(json.load(sys.stdin).get('version','unknown'))"
```

This gives you a mapping of: version → commit SHA → date → commit message.

**Important version edge cases:**
- If a commit returns `"unknown"` or the version field is absent, that commit changed the
  plugin metadata without bumping the version (e.g., description edits, keyword changes).
  Do not treat these as version boundaries.
- If the version field was removed entirely from plugin.json at some point (as happened with
  the Slack plugin), note this in the changelog but don't invent a version number. Use
  `[Unreleased]` for changes that occurred after the last known version.
- If plugin.json has never contained a version field, or the plugin only has a single version,
  use the actual version found (e.g., `[0.0.1]`) for the initial release and `[Unreleased]`
  for any subsequent changes. Never invent or guess version numbers that don't appear in the
  version file history.

### Step 4: Get all commits for the plugin directory

Fetch the full commit history for the plugin directory. This includes all changes, not just
version bumps:

```bash
git log --pretty=format:'%H  %h  %ai  %an  %s' -- <plugin-path>
```

This returns the full SHA (for linking), short SHA, author date, author name, and subject.

To extract PR numbers from merge commit messages:
```bash
git log --pretty=format:'%h  %ai  %s' -- <plugin-path> | grep -oP '\(#\K[0-9]+(?=\))'
```

Or parse them inline — PR numbers appear as `(#NNN)` in merge commit subjects.

If commits reference PRs but the PR number isn't in the subject, you can check the commit body:
```bash
git log --pretty=format:'%h  %ai  %s%n%b' -- <plugin-path>
```

### Step 5: Group commits by version

Working backwards from the newest version:

1. Find the commit where each version was introduced (from Step 3)
2. All commits between version N-1 and version N belong to version N
3. All commits after the latest version bump belong to `[Unreleased]`
4. All commits before the first version bump belong to the initial release (0.0.1 or whatever it is)

Use `git log` ranges to isolate commits per version:
```bash
# Commits between two version bumps
git log --pretty=format:'%h  %ai  %s' <older-version-sha>..<newer-version-sha> -- <plugin-path>

# Commits after the latest version bump (unreleased)
git log --pretty=format:'%h  %ai  %s' <latest-version-sha>..HEAD -- <plugin-path>

# Commits up to and including the first version (initial release)
git log --pretty=format:'%h  %ai  %s' <first-version-sha> -- <plugin-path>
```

### Step 6: Classify changes

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

All notable changes to `<plugin-path>` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

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

## 2026-03-23

### telegram → [0.0.3](external_plugins/telegram/CHANGELOG.html)
Permission-relay — approve tool use from your phone.

### discord → [0.0.3](external_plugins/discord/CHANGELOG.html)
Permission-relay — approve tool use from your phone.

## 2026-03-20

### telegram → [0.0.2](external_plugins/telegram/CHANGELOG.html)
All file types, bot commands, MarkdownV2, resilience fixes.

### discord → [0.0.2](external_plugins/discord/CHANGELOG.html)
Edit notification guidance, state dir config, resilience fixes.
```

The one-line summary should capture the headline feature(s) of that version — think of it as
the commit message for the version. Keep it under 80 characters.

To build this, iterate over all plugins that have `.claude-plugin/plugin.json`, generate their
individual changelogs, then merge the version dates into a single timeline sorted newest-first.

### Step 9: Deliver

Save per-plugin changelogs as `<plugin-path>/CHANGELOG.md` and the repo-level changelog as
`CHANGELOG.md` in the outputs folder. Every CHANGELOG.md must include the Jekyll front matter
block at the top (layout + render_with_liquid). If the user only asked for a single plugin,
just deliver that one file.

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
