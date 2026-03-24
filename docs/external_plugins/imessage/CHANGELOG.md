---
layout: default
render_with_liquid: false
---

# Changelog — Imessage

> iMessage channel for Claude Code — reads chat.db directly, sends via AppleScript. Built-in access control; manage pairing, allowlists, and policy via /imessage:access.

All notable changes to `external_plugins/imessage` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/imessage).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [Unreleased]

### Added
- **Regenerate imessage bun.lock without artifactory** — Regenerate imessage bun.lock without artifactory URLs
  [`12e9c01`](https://github.com/anthropics/claude-plugins-official/commit/12e9c01d5f28bcec14f69610e19352d5be5559ff) · 2026-03-23
- **Show input_preview only for Bash** — Show input_preview only for Bash in permission prompts
  [`d49d339`](https://github.com/anthropics/claude-plugins-official/commit/d49d339d1e520f450c337687035af7df0aa15144) · 2026-03-23
- **port permission-relay + lifecycle fixes** — port permission-relay + lifecycle fixes from telegram
  [`bfed463`](https://github.com/anthropics/claude-plugins-official/commit/bfed4635f5f47c2183e9a4b9b985dfe0e8cc5d73) · 2026-03-23
- **Add IMESSAGE_APPEND_SIGNATURE env var (default** — Add IMESSAGE_APPEND_SIGNATURE env var (default true)
  [`6d0053f`](https://github.com/anthropics/claude-plugins-official/commit/6d0053f69e717a8d960d8e2e4ba55878473aa2d3) · 2026-03-20

### Docs
- **Document IMESSAGE_STATE_DIR in README** — Document IMESSAGE_STATE_DIR in README
  [`9693fd7`](https://github.com/anthropics/claude-plugins-official/commit/9693fd75c307cca1fb175620819d14b143f4fe41) · 2026-03-23

## [0.0.1] — 2026-03-18

### Added
- **Add imessage channel plugin** — Add imessage channel plugin
  [`1c95fc6`](https://github.com/anthropics/claude-plugins-official/commit/1c95fc662b7df51e9200ef8c26de2a4e803e9ff4) · 2026-03-18
