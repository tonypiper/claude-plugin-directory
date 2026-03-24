---
layout: default
render_with_liquid: false
---

# Changelog — Telegram

> Telegram channel for Claude Code — messaging bridge with built-in access control. Manage pairing, allowlists, and policy via /telegram:access.

All notable changes to `external_plugins/telegram` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [0.0.4] — 2026-03-23

### Changed
- **Compact permission messages with expandable details** — Permission approval messages are now collapsed by default with expandable detail sections, reducing noise for routine approvals while keeping full context accessible.
  [`4b1e2a2`](https://github.com/anthropics/claude-plugins-official/commit/4b1e2a28ceab32b49b447d6255d6f3c4fa8774de) · 2026-03-23 · ([#952](https://github.com/anthropics/claude-plugins-official/pull/952))

---

## [0.0.3] — 2026-03-23

### Added
- **Inline approval buttons for permission requests** — Tool permission prompts now include inline Telegram buttons so you can approve or deny directly from your phone without typing a reply.
  [`b3a0714`](https://github.com/anthropics/claude-plugins-official/commit/b3a0714d7ffc4dec08b8d0dad2aa3dc09b000e98) · 2026-03-23 · ([#945](https://github.com/anthropics/claude-plugins-official/pull/945))

---

## [0.0.2] — 2026-03-20

### Added
- **Permission relay** — Claude Code tool permission prompts are now forwarded to Telegram, completing the bidirectional channel. Approve or deny tool use from your phone.
  [`daa84c9`](https://github.com/anthropics/claude-plugins-official/commit/daa84c99c815fb2832ecb5df80613e2088af0191) · 2026-03-20

- **All inbound file types + `download_attachment` tool** — The bot now accepts any file type (photos, documents, audio, video, stickers) and exposes a `download_attachment` tool so Claude can fetch and read attachments.
  [`a9bc23d`](https://github.com/anthropics/claude-plugins-official/commit/a9bc23da6f263eddd73379c764b5dba091be29ba) · 2026-03-20

- **Bot commands: `/start`, `/help`, `/status`** — Standard Telegram bot commands for onboarding, usage guidance, and connection status. `/start` correctly acknowledges `dmPolicy === 'disabled'` rather than misleading the user.
  [`521f858`](https://github.com/anthropics/claude-plugins-official/commit/521f858e112d7e4e0854abe08d5a34631509d475) · 2026-03-20

- **MarkdownV2 formatting** — Replies and message edits now use Telegram's MarkdownV2 parse mode for richer text output.
  [`a7cb39c`](https://github.com/anthropics/claude-plugins-official/commit/a7cb39c269de4c32436c02a0b46cec3dae7df79f) · 2026-03-20

- **Configurable state directory** — The state directory (allowlists, pairing codes) is now configurable via `TELEGRAM_STATE_DIR`, allowing multiple bots with separate tokens on the same machine.
  [`14927ff`](https://github.com/anthropics/claude-plugins-official/commit/14927ff475758115791aceb4b53c0aadce8db4d8) · 2026-03-20

### Fixed
- **Silent polling death** — The bot would silently stop delivering messages after the first middleware error. grammy's default handler calls `bot.stop()` on any throw, and `void bot.start()` swallows rejections with no log. Error handlers added to surface and recover from failures.
  [`9f2a4fe`](https://github.com/anthropics/claude-plugins-official/commit/9f2a4feab937324f57e0e0096dbfd58600fefbf9) · 2026-03-20

- **409 Conflict on startup** — During `/mcp reload` or when a zombie from a previous session still holds the polling slot, the new process died immediately on 409 Conflict. Now retries with backoff until the slot frees — typically within a second or two.
  [`1daff5f`](https://github.com/anthropics/claude-plugins-official/commit/1daff5f2242e93a31fe734475caba9d19770ec43) · 2026-03-20

- **Zombie process on Claude Code exit** — When the MCP stdio transport closed, the bot kept polling Telegram as a zombie, holding the token and causing 409 Conflict for the next session. Now listens for stdin close and SIGTERM/SIGINT to exit cleanly.
  [`2aa90a8`](https://github.com/anthropics/claude-plugins-official/commit/2aa90a83876b548c5db2e3ecae22d93088e6e0e5) · 2026-03-20

- **Setup phase abort crash** — `bot.stop()` called during `bot.start()`'s setup phase (deleteWebhook/getMe) caused an unhandled 'Aborted delay' rejection. Now returns silently as expected.
  [`3d8042f`](https://github.com/anthropics/claude-plugins-official/commit/3d8042f259f80248da94b8e07a906c78c49d3501) · 2026-03-20

- **Push notifications lost on task completion** — Message edits don't trigger push notifications on mobile. System instructions and `edit_message` tool description updated to steer Claude toward edit-for-progress + new reply on completion.
  [`5c58308`](https://github.com/anthropics/claude-plugins-official/commit/5c58308be4c6f234a90bc93464bc2c065c4a54f0) · 2026-03-20 · ([#786](https://github.com/anthropics/claude-plugins-official/pull/786))

### Security
- **Sanitize user-controlled filenames** — File names from inbound attachments are stripped of `<>[]\r\n;` before use in `<channel>` notifications, preventing delimiter injection that could break tag structure or forge meta entries.
  [`1636fed`](https://github.com/anthropics/claude-plugins-official/commit/1636fedbd46691ece874fcf7425e2178da47ddc5) · 2026-03-20

- **Restrict bot commands to DMs** — `/status` in a group would leak the sender's pending pairing code to other group members. Bot commands are now DM-only to prevent pairing code exposure and spam.
  [`9a101ba`](https://github.com/anthropics/claude-plugins-official/commit/9a101ba34c8d58410beaaad7f053ba9434fc6953) · 2026-03-20

- **Lock `.env` to owner permissions** — The bot token is a credential. `.env` files are now `chmod 600` on load. No-op on Windows.
  [`8140fba`](https://github.com/anthropics/claude-plugins-official/commit/8140fbad22814b99ad56e1161a43ec203da669d8) · 2026-03-20

### Docs
- **Document Bun prerequisite** — Both MCP servers run on Bun but this wasn't documented. Added a Prerequisites section with the install command to prevent missing-runtime errors on first setup.
  [`8938650`](https://github.com/anthropics/claude-plugins-official/commit/89386504288e6c82800f7f28e47b44f3db91fce2) · 2026-03-19

- **README clarifications** — Removed redundant `/reload-plugins` step, fixed token save path (`.claude/channels/` not `~/.claude/channels/`), clarified the bot only responds once the channel is running.
  [`b01fad3`](https://github.com/anthropics/claude-plugins-official/commit/b01fad339621349a2b1dd83334c66e8fd356f223) · 2026-03-19

---

## [0.0.1] — 2026-03-19

> **Note:** The plugin was briefly removed on 2026-03-18 ([#741](https://github.com/anthropics/claude-plugins-official/pull/741)) and restored the following day ([#753](https://github.com/anthropics/claude-plugins-official/pull/753)).

### Added
- **Telegram messaging bridge with access control** — Local MCP server connecting Claude Code to the Telegram Bot API via a user-created bot token. Supports sending and receiving messages, pairing via 6-character codes, and an allowlist-based access policy. Access management via the `/telegram:access` skill. Built on grammy + Bun.
  [`1b33c1d`](https://github.com/anthropics/claude-plugins-official/commit/1b33c1d9f979980c2a8897c31b047725d14280d1) · 2026-03-18 · ([#735](https://github.com/anthropics/claude-plugins-official/pull/735))
