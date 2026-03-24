---
layout: default
title: Full Changelog
permalink: /changelog/
---

{% capture changelog %}{% include_relative CHANGELOG.md %}{% endcapture %}
{{ changelog | markdownify }}
