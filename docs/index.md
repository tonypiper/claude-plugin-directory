---
layout: default
title: Claude Plugin Directory
---

# Claude Plugin Directory

Unofficial changelog and version tracker for all plugins in
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official).

Last generated: {{ site.time | date: "%Y-%m-%d" }}

---

## External Plugins (Connectors)

| Plugin | Version | Last Updated | Description |
|--------|---------|--------------|-------------|
{% for plugin in site.data.plugins %}{% if plugin.type == "external_plugins" %}| [{{ plugin.name }}]({{ plugin.changelog }}) | `{{ plugin.version }}` | {{ plugin.last_updated }} | {{ plugin.description }} |
{% endif %}{% endfor %}

## Internal Plugins (Skills & Tools)

| Plugin | Version | Last Updated | Description |
|--------|---------|--------------|-------------|
{% for plugin in site.data.plugins %}{% if plugin.type == "plugins" %}| [{{ plugin.name }}]({{ plugin.changelog }}) | `{{ plugin.version }}` | {{ plugin.last_updated }} | {{ plugin.description }} |
{% endif %}{% endfor %}

---

## About

This site is generated automatically from the commit history and `plugin.json`
metadata in the official Claude Code plugins repository. It exists because the
repo has no releases, no tags, and no changelog.

Each plugin's changelog is reconstructed by walking `git log` for the plugin
directory and mapping commits to version bumps in `.claude-plugin/plugin.json`.

[View the rollup changelog](CHANGELOG.html) for a timeline view across all plugins.

### How to contribute

This project is open source. If you spot an error in a changelog or want to
improve the generator, PRs are welcome.
