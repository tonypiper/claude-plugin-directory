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
- **Permission relay** — Brings iMessage to parity with the Telegram/Discord permission system: Claude fans out permission requests to allowlisted DM chats and your self-chat, then intercepts "yes/no \<id\>" replies and emits structured permission events instead of forwarding them as chat messages. Groups are excluded per single-user-mode policy.
  [`bfed463`](https://github.com/anthropics/claude-plugins-official/commit/bfed4635f5f47c2183e9a4b9b985dfe0e8cc5d73) · 2026-03-23
- **Configurable state directory** — `IMESSAGE_STATE_DIR` lets you override where allowlist and state files are written, consistent with the Telegram/Discord env vars.
  [`bfed463`](https://github.com/anthropics/claude-plugins-official/commit/bfed4635f5f47c2183e9a4b9b985dfe0e8cc5d73) · 2026-03-23
- **Append-signature toggle** — `IMESSAGE_APPEND_SIGNATURE=false` suppresses the "Sent via Claude Code" tag that is appended to outbound messages by default.
  [`6d0053f`](https://github.com/anthropics/claude-plugins-official/commit/6d0053f69e717a8d960d8e2e4ba55878473aa2d3) · 2026-03-20

### Changed
- **Input preview limited to Bash** — Permission messages for Write/Edit tools no longer include the full input preview (which could be many kilobytes of file content). Only Bash shows the command preview, where seeing the actual input matters most for safety.
  [`d49d339`](https://github.com/anthropics/claude-plugins-official/commit/d49d339d1e520f450c337687035af7df0aa15144) · 2026-03-23

### Fixed
- **Bun lockfile regenerated without private registry URLs** — The initial lockfile was generated behind a private Anthropic registry (`artifactory.infra.ant.dev`), causing `bun install` to fail with 401s for external users. Regenerated against `registry.npmjs.org`.
  [`12e9c01`](https://github.com/anthropics/claude-plugins-official/commit/12e9c01d5f28bcec14f69610e19352d5be5559ff) · 2026-03-23 · ([#957](https://github.com/anthropics/claude-plugins-official/pull/957))
- **Clean shutdown and zombie prevention** — Added process-level `unhandledRejection`/`uncaughtException` handlers, `.unref()` on both polling intervals, and a `SIGTERM`/`SIGINT`/`stdin EOF` handler that closes the `chat.db` connection and exits cleanly.
  [`bfed463`](https://github.com/anthropics/claude-plugins-official/commit/bfed4635f5f47c2183e9a4b9b985dfe0e8cc5d73) · 2026-03-23

### Docs
- **Document `IMESSAGE_STATE_DIR`** — Added the env var to the README so users know how to relocate the state directory.
  [`9693fd7`](https://github.com/anthropics/claude-plugins-official/commit/9693fd75c307cca1fb175620819d14b143f4fe41) · 2026-03-23

---

## [0.0.1] — 2026-03-18

### Added
- **Initial iMessage channel plugin** — A local MCP server that reads `~/Library/Messages/chat.db` directly for message history and new-message polling, and sends replies via AppleScript to Messages.app. macOS only. Inbound messages are gated by an allowlist (default: self-chat only); the `/imessage:access` skill manages allowlists and policy. Requires Full Disk Access and Automation TCC grants (prompted by macOS on first use). Runs as a TypeScript/Bun process launched by `.mcp.json`.
  [`1c95fc6`](https://github.com/anthropics/claude-plugins-official/commit/1c95fc662b7df51e9200ef8c26de2a4e803e9ff4) · 2026-03-18 · ([#737](https://github.com/anthropics/claude-plugins-official/pull/737))
