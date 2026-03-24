# Changelog — Discord

All notable changes to `external_plugins/discord` in
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
- **discord: port resilience fixes from** — discord: port resilience fixes from telegram
  [`aa71c24`](https://github.com/anthropics/claude-plugins-official/commit/aa71c24314ab2336e4ae55d59490180822789d49) · 2026-03-20
- **discord/telegram: guide assistant to send** — discord/telegram: guide assistant to send new reply on completion
  [`5c58308`](https://github.com/anthropics/claude-plugins-official/commit/5c58308be4c6f234a90bc93464bc2c065c4a54f0) · 2026-03-20
- **telegram/discord: make state dir configurable** — telegram/discord: make state dir configurable via env var
  [`14927ff`](https://github.com/anthropics/claude-plugins-official/commit/14927ff475758115791aceb4b53c0aadce8db4d8) · 2026-03-20
- **Merge pull request #811 from** — Merge pull request #811 from anthropics/kenneth/chmod-env-files
  [`562a27f`](https://github.com/anthropics/claude-plugins-official/commit/562a27feec2c60bc94a3b58ae1b926382ae836bf) · 2026-03-20
- **Lock telegram/discord .env files to** — Lock telegram/discord .env files to owner (chmod 600)
  [`8140fba`](https://github.com/anthropics/claude-plugins-official/commit/8140fbad22814b99ad56e1161a43ec203da669d8) · 2026-03-20

### Docs
- **README clarifications from docs walkthrough** — README clarifications from docs walkthrough testing
  [`b01fad3`](https://github.com/anthropics/claude-plugins-official/commit/b01fad339621349a2b1dd83334c66e8fd356f223) · 2026-03-19
- **Add Bun prerequisite to discord** — Add Bun prerequisite to discord and telegram plugin READMEs
  [`8938650`](https://github.com/anthropics/claude-plugins-official/commit/89386504288e6c82800f7f28e47b44f3db91fce2) · 2026-03-19

## [0.0.1] — 2026-03-19

### Added
- **Add discord channel plugin** — Add discord channel plugin
  [`4796148`](https://github.com/anthropics/claude-plugins-official/commit/4796148aceb77d37518b9c3028d6c225618ca296) · 2026-03-18 · ([#736](https://github.com/anthropics/claude-plugins-official/pull/736))

### Changed
- **Revert "Remove telegram, discord, and** — Revert "Remove telegram, discord, and fakechat plugins (#741)"
  [`7994c27`](https://github.com/anthropics/claude-plugins-official/commit/7994c270e575fa82bc86b3e99363bf8fe55292f7) · 2026-03-19 · ([#741](https://github.com/anthropics/claude-plugins-official/pull/741))
- **Remove telegram, discord, and fakechat** — Remove telegram, discord, and fakechat plugins
  [`d53f6ca`](https://github.com/anthropics/claude-plugins-official/commit/d53f6ca4cdb000c671dfdc1c181b021e97c25505) · 2026-03-18 · ([#741](https://github.com/anthropics/claude-plugins-official/pull/741))
