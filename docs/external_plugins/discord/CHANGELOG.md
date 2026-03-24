---
layout: default
render_with_liquid: false
---

# Changelog — Discord

> Discord channel for Claude Code — messaging bridge with built-in access control. Manage pairing, allowlists, and policy via /discord:access.

All notable changes to `external_plugins/discord` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [0.0.4] — 2026-03-23

### Changed
- **Compact permission messages with expandable details** — Permission approval messages now show only the tool name by default, with a "See more" button that expands inline to show the full description and input preview JSON. This reduces noise for routine approvals while keeping full context one tap away.
  [`4b1e2a2`](https://github.com/anthropics/claude-plugins-official/commit/4b1e2a28ceab32b49b447d6255d6f3c4fa8774de) · 2026-03-23 · ([#952](https://github.com/anthropics/claude-plugins-official/pull/952))

---

## [0.0.3] — 2026-03-23

### Added
- **Inline approval buttons** — Permission requests now show native Discord buttons (Discord.js `ButtonBuilder`) so you can approve or deny with one tap instead of typing a 5-character reply ID. After a decision the message updates to show the outcome and the buttons are removed. The text-reply path is kept as a fallback.
  [`b3a0714`](https://github.com/anthropics/claude-plugins-official/commit/b3a0714d7ffc4dec08b8d0dad2aa3dc09b000e98) · 2026-03-23 · ([#945](https://github.com/anthropics/claude-plugins-official/pull/945))

---

## [0.0.2] — 2026-03-20

### Added
- **Permission relay** — Claude can now send tool-permission requests over Discord and wait for your approval before running a tool. Outbound requests are fanned out to all allowlisted DMs; inbound "yes/no \<id\>" replies are intercepted before reaching Claude and emitted as structured permission events. Guild channels are excluded — only DMs, per single-user-mode policy.
  [`daa84c9`](https://github.com/anthropics/claude-plugins-official/commit/daa84c99c815fb2832ecb5df80613e2088af0191) · 2026-03-20 · ([#833](https://github.com/anthropics/claude-plugins-official/pull/833))
- **New-reply on task completion** — System instructions now steer the assistant to use message edits for progress updates (silent) and send a *new* reply when the task completes. Message edits don't trigger push notifications, so without this you'd miss the "done" signal on your device.
  [`5c58308`](https://github.com/anthropics/claude-plugins-official/commit/5c58308be4c6f234a90bc93464bc2c065c4a54f0) · 2026-03-20

### Changed
- **Configurable state directory** — `DISCORD_STATE_DIR` lets you specify where allowlist and state files live, instead of always writing to `~/.claude/channels/discord/`. Enables multiple bots on one machine with separate tokens and allowlists.
  [`14927ff`](https://github.com/anthropics/claude-plugins-official/commit/14927ff475758115791aceb4b53c0aadce8db4d8) · 2026-03-20

### Fixed
- **Resilience improvements** — Added process-level `unhandledRejection`/`uncaughtException` handlers, `client.on('error')` logging, `.unref()` on the approval-check interval, and a clean `SIGTERM`/`stdin EOF` shutdown path to prevent zombie processes and silent crashes. (Discord.js auto-reconnects, so this is less critical than for Telegram, but the gaps were still there.)
  [`aa71c24`](https://github.com/anthropics/claude-plugins-official/commit/aa71c24314ab2336e4ae55d59490180822789d49) · 2026-03-20

### Security
- **Lock .env to owner permissions** — The bot token `.env` file is now `chmod 600` on load, preventing other users on the same machine from reading the credential. Pre-existing files are tightened on startup; the configure skill also runs `chmod` after writing.
  [`8140fba`](https://github.com/anthropics/claude-plugins-official/commit/8140fbad22814b99ad56e1161a43ec203da669d8) · 2026-03-20 · ([#811](https://github.com/anthropics/claude-plugins-official/pull/811))

---

## [0.0.1] — 2026-03-19

> **Note:** The plugin was removed from the repository on 2026-03-18 ([#741](https://github.com/anthropics/claude-plugins-official/pull/741)) along with the Telegram and fakechat plugins, then restored two days later ([#753](https://github.com/anthropics/claude-plugins-official/pull/753)).

### Added
- **Initial Discord channel plugin** — A local MCP server connecting Claude Code to Discord's Gateway via a bot token you create. Inbound messages are gated by an allowlist (default: pairing mode); guild channels require opt-in and @mention. Runs as a TypeScript/Bun process launched by `.mcp.json`. The `/discord:access` skill manages pairing, allowlists, and policy.
  [`4796148`](https://github.com/anthropics/claude-plugins-official/commit/4796148aceb77d37518b9c3028d6c225618ca296) · 2026-03-18 · ([#736](https://github.com/anthropics/claude-plugins-official/pull/736))

### Docs
- **Bun prerequisite** — Added a Prerequisites section to the README so users know Bun is required to run the MCP server, preventing a confusing missing-runtime error on first setup.
  [`8938650`](https://github.com/anthropics/claude-plugins-official/commit/89386504288e6c82800f7f28e47b44f3db91fce2) · 2026-03-19
- **README corrections** — Removed reference to `/reload-plugins` (redundant; you restart with `--channels`), corrected the token save path to `~/.claude/channels/`, and clarified that the bot only responds after the channel is running.
  [`b01fad3`](https://github.com/anthropics/claude-plugins-official/commit/b01fad339621349a2b1dd83334c66e8fd356f223) · 2026-03-19
