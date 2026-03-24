---
layout: default
render_with_liquid: false
---

# Changelog — Claude-code-setup

> Analyze codebases and recommend tailored Claude Code automations such as hooks, skills, MCP servers, and subagents.

All notable changes to `plugins/claude-code-setup` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [Unreleased]

### Changed
- **Merged slash commands and skills** — Combined the plugin's slash command definitions and skill entries into a unified structure.
  [`146d478`](https://github.com/anthropics/claude-plugins-official/commit/146d4788ff321cd6e4703f9ba9c07113be7abb5c) · 2026-01-20

### Docs
- **Apache 2.0 license** — Added a `LICENSE` file to the plugin directory as part of a repo-wide open-source licensing pass across all internal plugins.
  [`aecd4c8`](https://github.com/anthropics/claude-plugins-official/commit/aecd4c852f10b466245f18383fa6aad8c0b10d57) · 2026-02-20

---

## [1.0.0] — 2026-01-16

### Added
- **Initial release** — Analyzes your codebase and recommends tailored Claude Code automations: hooks that trigger on tool events, skills for reusable workflows, MCP servers for external integrations, and subagent configurations for parallel workloads.
  [`a86e346`](https://github.com/anthropics/claude-plugins-official/commit/a86e34672c44fa1fb1ae2b2c4143abcf26612ace) · 2026-01-16

### Fixed
- **Plugin metadata corrections** — Description and marketplace entry updated on launch day to accurately reflect the plugin's scope.
  [`6efe831`](https://github.com/anthropics/claude-plugins-official/commit/6efe83162f94769e7e9bed70cb4d25178bbed0ba) · 2026-01-20 · [`7d5dcb6`](https://github.com/anthropics/claude-plugins-official/commit/7d5dcb6765ca6fcbdae0d8fcca14194b43e9a523) · 2026-01-20 · [`3c1e321`](https://github.com/anthropics/claude-plugins-official/commit/3c1e3212f6688f62f4100e630877cfc3ca7356c3) · 2026-01-20
