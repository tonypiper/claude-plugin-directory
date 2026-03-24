---
layout: default
render_with_liquid: false
---

# Changelog — Telegram

All notable changes to `external_plugins/telegram` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [0.0.4] — 2026-03-23

### Added
- **compact permission messages with expandable** — compact permission messages with expandable details
  [`4b1e2a2`](https://github.com/anthropics/claude-plugins-official/commit/4b1e2a28ceab32b49b447d6255d6f3c4fa8774de) · 2026-03-23 · ([#952](https://github.com/anthropics/claude-plugins-official/pull/952))

## [0.0.3] — 2026-03-23

### Added
- **inline buttons for permission approval** — inline buttons for permission approval
  [`b3a0714`](https://github.com/anthropics/claude-plugins-official/commit/b3a0714d7ffc4dec08b8d0dad2aa3dc09b000e98) · 2026-03-23 · ([#945](https://github.com/anthropics/claude-plugins-official/pull/945))

## [0.0.2] — 2026-03-20

### Added
- **permission-relay capability + bidirectional handlers** — permission-relay capability + bidirectional handlers
  [`daa84c9`](https://github.com/anthropics/claude-plugins-official/commit/daa84c99c815fb2832ecb5df80613e2088af0191) · 2026-03-20
- **Sanitize user-controlled filenames and download** — Sanitize user-controlled filenames and download path components
  [`1636fed`](https://github.com/anthropics/claude-plugins-official/commit/1636fedbd46691ece874fcf7425e2178da47ddc5) · 2026-03-20
- **Tighten /start and /help copy** — Tighten /start and /help copy
  [`ea382ec`](https://github.com/anthropics/claude-plugins-official/commit/ea382ec6a43f18478df6acb8b7026fae72eda02a) · 2026-03-20
- **Restrict bot commands to DMs** — Restrict bot commands to DMs (security)
  [`9a101ba`](https://github.com/anthropics/claude-plugins-official/commit/9a101ba34c8d58410beaaad7f053ba9434fc6953) · 2026-03-20
- **telegram: handle all inbound file** — telegram: handle all inbound file types + download_attachment tool
  [`a9bc23d`](https://github.com/anthropics/claude-plugins-official/commit/a9bc23da6f263eddd73379c764b5dba091be29ba) · 2026-03-20
- **telegram: add /start /help /status** — telegram: add /start /help /status bot commands
  [`521f858`](https://github.com/anthropics/claude-plugins-official/commit/521f858e112d7e4e0854abe08d5a34631509d475) · 2026-03-20
- **telegram: add MarkdownV2 parse_mode to** — telegram: add MarkdownV2 parse_mode to reply/edit_message
  [`a7cb39c`](https://github.com/anthropics/claude-plugins-official/commit/a7cb39c269de4c32436c02a0b46cec3dae7df79f) · 2026-03-20
- **discord/telegram: guide assistant to send** — discord/telegram: guide assistant to send new reply on completion
  [`5c58308`](https://github.com/anthropics/claude-plugins-official/commit/5c58308be4c6f234a90bc93464bc2c065c4a54f0) · 2026-03-20
- **Silently return when bot.stop() aborts** — Silently return when bot.stop() aborts the setup phase
  [`3d8042f`](https://github.com/anthropics/claude-plugins-official/commit/3d8042f259f80248da94b8e07a906c78c49d3501) · 2026-03-20
- **telegram/discord: make state dir configurable** — telegram/discord: make state dir configurable via env var
  [`14927ff`](https://github.com/anthropics/claude-plugins-official/commit/14927ff475758115791aceb4b53c0aadce8db4d8) · 2026-03-20
- **telegram: exit when Claude Code** — telegram: exit when Claude Code closes the connection
  [`2aa90a8`](https://github.com/anthropics/claude-plugins-official/commit/2aa90a83876b548c5db2e3ecae22d93088e6e0e5) · 2026-03-20
- **telegram: add error handlers to** — telegram: add error handlers to stop silent polling death
  [`9f2a4fe`](https://github.com/anthropics/claude-plugins-official/commit/9f2a4feab937324f57e0e0096dbfd58600fefbf9) · 2026-03-20
- **Merge pull request #811 from** — Merge pull request #811 from anthropics/kenneth/chmod-env-files
  [`562a27f`](https://github.com/anthropics/claude-plugins-official/commit/562a27feec2c60bc94a3b58ae1b926382ae836bf) · 2026-03-20
- **Lock telegram/discord .env files to** — Lock telegram/discord .env files to owner (chmod 600)
  [`8140fba`](https://github.com/anthropics/claude-plugins-official/commit/8140fbad22814b99ad56e1161a43ec203da669d8) · 2026-03-20

### Fixed
- **telegram: retry on 409 Conflict** — telegram: retry on 409 Conflict instead of crashing
  [`1daff5f`](https://github.com/anthropics/claude-plugins-official/commit/1daff5f2242e93a31fe734475caba9d19770ec43) · 2026-03-20

### Docs
- **README clarifications from docs walkthrough** — README clarifications from docs walkthrough testing
  [`b01fad3`](https://github.com/anthropics/claude-plugins-official/commit/b01fad339621349a2b1dd83334c66e8fd356f223) · 2026-03-19
- **Add Bun prerequisite to discord** — Add Bun prerequisite to discord and telegram plugin READMEs
  [`8938650`](https://github.com/anthropics/claude-plugins-official/commit/89386504288e6c82800f7f28e47b44f3db91fce2) · 2026-03-19

## [0.0.1] — 2026-03-19

### Added
- **Add telegram channel plugin** — Add telegram channel plugin
  [`1b33c1d`](https://github.com/anthropics/claude-plugins-official/commit/1b33c1d9f979980c2a8897c31b047725d14280d1) · 2026-03-18 · ([#735](https://github.com/anthropics/claude-plugins-official/pull/735))

### Changed
- **Revert "Remove telegram, discord, and** — Revert "Remove telegram, discord, and fakechat plugins (#741)"
  [`7994c27`](https://github.com/anthropics/claude-plugins-official/commit/7994c270e575fa82bc86b3e99363bf8fe55292f7) · 2026-03-19 · ([#741](https://github.com/anthropics/claude-plugins-official/pull/741))
- **Remove telegram, discord, and fakechat** — Remove telegram, discord, and fakechat plugins
  [`d53f6ca`](https://github.com/anthropics/claude-plugins-official/commit/d53f6ca4cdb000c671dfdc1c181b021e97c25505) · 2026-03-18 · ([#741](https://github.com/anthropics/claude-plugins-official/pull/741))
