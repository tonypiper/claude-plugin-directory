# Claude Plugin Directory

Unofficial changelog and version tracker for all plugins in [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

The official repo has no releases, no tags, and no changelog. This project fills that gap by reconstructing version history from `git log` and `plugin.json` version bumps.

## What's here

- `docs/` — Jekyll site (served via GitHub Pages) with per-plugin changelogs and a browsable index
- `scripts/generate-changelogs.py` — Batch script that generates all changelogs from a local clone
- `.claude/commands/plugin-changelog.md` — `/plugin-changelog` command for generating changelogs interactively in Claude Code

## Quick start

```bash
# Clone the official repo
git clone https://github.com/anthropics/claude-plugins-official.git

# Generate all changelogs
python3 scripts/generate-changelogs.py claude-plugins-official --output-dir docs --rollup

# Preview the site locally
cd docs && bundle install && bundle exec jekyll serve
```

## Updating

Pull the latest from the official repo and rerun the generator:

```bash
cd claude-plugins-official && git pull
cd .. && python3 scripts/generate-changelogs.py claude-plugins-official --output-dir docs --rollup
```

The generator is idempotent — it overwrites existing changelogs with fresh data.

## Single plugin

```bash
python3 scripts/generate-changelogs.py claude-plugins-official \
  --output-dir docs \
  --plugin external_plugins/telegram
```

## License

MIT
