---
layout: default
render_with_liquid: false
---

# Changelog — Ralph-loop

All notable changes to `plugins/ralph-loop` in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop).

Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.
This changelog was compiled from the merged PR and commit history on the `main` branch.

---

## [Unreleased]

### Added
- **address review: bound grep to** — address review: bound grep to tail -n 100; restore explicit error paths
  [`028eccf`](https://github.com/anthropics/claude-plugins-official/commit/028eccf5447b1f226f5c98a575dad6ee704b2bca) · 2026-03-04
- **Add Apache 2.0 LICENSE files** — Add Apache 2.0 LICENSE files to all internal plugins
  [`aecd4c8`](https://github.com/anthropics/claude-plugins-official/commit/aecd4c852f10b466245f18383fa6aad8c0b10d57) · 2026-02-20

### Changed
- **updates(staging): merge staging additions into** — updates(staging): merge staging additions into main
  [`78497c5`](https://github.com/anthropics/claude-plugins-official/commit/78497c524da3762865d47377357c30af5b50d522) · 2026-03-17 · ([#677](https://github.com/anthropics/claude-plugins-official/pull/677))
- **Rename ralph-wiggum plugin to ralph-loop** — Rename ralph-wiggum plugin to ralph-loop per legal guidance
  [`44328be`](https://github.com/anthropics/claude-plugins-official/commit/44328beed48874d8e00da6c4ca5daaa5f0f3183c) · 2026-01-06 · ([#142](https://github.com/anthropics/claude-plugins-official/pull/142))

### Fixed
- **isolate loop state to the** — isolate loop state to the session that started it
  [`8644df9`](https://github.com/anthropics/claude-plugins-official/commit/8644df9ad51fe1dadc5d067e806c3c686efeafff) · 2026-03-02
- **stop hook fails when last** — stop hook fails when last assistant block is tool_use
  [`adfc379`](https://github.com/anthropics/claude-plugins-official/commit/adfc3796639cd0c5d892fb05303b4b2cddfe6e12) · 2026-03-02
