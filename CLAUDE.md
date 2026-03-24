# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Unofficial changelog and version tracker for [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official). The official repo has no releases, tags, or changelog — this project reconstructs version history from `git log` and `plugin.json` version bumps, then publishes it as a Jekyll static site on GitHub Pages.

## Commands

### Generate changelogs (requires a local clone of the official repo)

```bash
# All plugins + rollup changelog
python3 scripts/generate-changelogs.py claude-plugins-official --output-dir docs --rollup

# Single plugin
python3 scripts/generate-changelogs.py claude-plugins-official --output-dir docs --plugin external_plugins/telegram

# Update: pull latest then regenerate
cd claude-plugins-official && git pull
cd .. && python3 scripts/generate-changelogs.py claude-plugins-official --output-dir docs --rollup
```

The generator is idempotent — reruns overwrite existing files.

### Jekyll site (local preview)

```bash
cd docs && bundle install && bundle exec jekyll serve
```

## Architecture

### Key components

- **`scripts/generate-changelogs.py`** — Core generator (504 lines, no dependencies beyond stdlib + git CLI)
- **`docs/`** — Jekyll site (GitHub Pages, baseurl `/claude-plugin-directory`)
- **`.claude/commands/plugin-changelog.md`** — `/plugin-changelog` command for interactive changelog generation

### Generator data flow

```
Official repo (local clone)
  → discover_plugins()         finds all dirs with .claude-plugin/plugin.json
  → get_version_history()      walks git log of plugin.json, extracts version at each commit
  → get_all_commits()          fetches all commits touching plugin dir (skips merges)
  → group_commits_by_version() maps commits to version sections by date range
  → classify_commit()          parses conventional commit prefix → category (Added/Fixed/Changed/Security/Docs)
  → format_changelog()         writes per-plugin CHANGELOG.md (Keep a Changelog format)
  → format_rollup()            writes root CHANGELOG.md sorted by date across all plugins
  → _data/plugins.json         index consumed by Jekyll's index.md Liquid template
```

### Plugin types

Two namespaces in the official repo, mirrored in `docs/`:
- `external_plugins/` — Connector/integration plugins (GitHub, Slack, Telegram, etc.)
- `plugins/` — Internal skills and tools

### Jekyll site structure

- `docs/index.md` — Homepage; Liquid template loops `site.data.plugins` into two tables
- `docs/_data/plugins.json` — Generated index (name, path, type, version, description, last_updated, changelog link)
- `docs/<plugin-path>/CHANGELOG.md` — Per-plugin changelog (generated)
- `docs/CHANGELOG.md` — Rollup across all plugins (generated when `--rollup` flag used)

### Conventional commit categories

The classifier maps commit prefixes to changelog sections:
- `feat:` → Added
- `fix:` → Fixed
- `docs:` → Docs
- `security:` → Security
- Everything else → Changed
