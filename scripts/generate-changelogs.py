#!/usr/bin/env python3
"""
Generate CHANGELOG.md files for all plugins in the claude-plugins-official repo.

Usage:
    python3 generate-changelogs.py /path/to/claude-plugins-official [--output-dir /path/to/output]

Requires: a local clone of https://github.com/anthropics/claude-plugins-official
Output:  one CHANGELOG.md per plugin + a repo-level CHANGELOG.md rollup
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


REPO_URL = "https://github.com/anthropics/claude-plugins-official"


@dataclass
class Commit:
    full_sha: str
    short_sha: str
    date: str  # YYYY-MM-DD
    author: str
    subject: str
    pr_number: Optional[str] = None

    def __post_init__(self):
        # Extract PR number from subject like "feat: something (#123)"
        match = re.search(r'\(#(\d+)\)', self.subject)
        if match:
            self.pr_number = match.group(1)


@dataclass
class VersionBoundary:
    version: str
    sha: str
    date: str


@dataclass
class ChangeEntry:
    category: str  # Added, Fixed, Changed, Security, Docs
    title: str
    description: str
    commit: Commit


@dataclass
class VersionSection:
    version: str  # e.g. "0.0.4" or "Unreleased"
    date: Optional[str]  # YYYY-MM-DD or None for Unreleased
    entries: list = field(default_factory=list)


def git(repo_path: str, *args) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", "-C", repo_path] + list(args),
        capture_output=True, text=True, timeout=30
    )
    return result.stdout.strip()


def discover_plugins(repo_path: str) -> list[tuple[str, str]]:
    """Find all plugins that have .claude-plugin/plugin.json. Returns [(path, type)]."""
    plugins = []
    for plugin_type in ["external_plugins", "plugins"]:
        type_dir = os.path.join(repo_path, plugin_type)
        if not os.path.isdir(type_dir):
            continue
        for name in sorted(os.listdir(type_dir)):
            plugin_json = os.path.join(type_dir, name, ".claude-plugin", "plugin.json")
            if os.path.isfile(plugin_json):
                plugins.append((f"{plugin_type}/{name}", plugin_type))
    return plugins


def get_plugin_name(repo_path: str, plugin_path: str) -> str:
    """Read the name field from plugin.json."""
    pj = os.path.join(repo_path, plugin_path, ".claude-plugin", "plugin.json")
    try:
        with open(pj) as f:
            data = json.load(f)
        name = data.get("name", plugin_path.split("/")[-1])
        return name[0].upper() + name[1:] if name else plugin_path.split("/")[-1]
    except (json.JSONDecodeError, FileNotFoundError):
        return plugin_path.split("/")[-1]


def get_plugin_description(repo_path: str, plugin_path: str) -> str:
    """Read the description field from plugin.json."""
    pj = os.path.join(repo_path, plugin_path, ".claude-plugin", "plugin.json")
    try:
        with open(pj) as f:
            data = json.load(f)
        return data.get("description", "")
    except (json.JSONDecodeError, FileNotFoundError):
        return ""


def get_plugin_version(repo_path: str, plugin_path: str) -> Optional[str]:
    """Read the current version from plugin.json on disk."""
    pj = os.path.join(repo_path, plugin_path, ".claude-plugin", "plugin.json")
    try:
        with open(pj) as f:
            data = json.load(f)
        return data.get("version")
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def get_version_history(repo_path: str, plugin_path: str) -> list[VersionBoundary]:
    """Walk commits that touched plugin.json and extract version at each commit."""
    log = git(repo_path, "log", "--pretty=format:%H  %h  %ai  %s",
              "--", f"{plugin_path}/.claude-plugin/plugin.json")
    if not log:
        return []

    boundaries = []
    seen_versions = set()

    for line in log.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("  ", 3)
        if len(parts) < 4:
            continue
        full_sha, short_sha, date_str, subject = parts
        date = date_str[:10]

        # Read plugin.json at this commit
        try:
            content = git(repo_path, "show", f"{full_sha}:{plugin_path}/.claude-plugin/plugin.json")
            data = json.loads(content)
            version = data.get("version")
        except (json.JSONDecodeError, subprocess.TimeoutExpired):
            version = None

        if version and version not in seen_versions:
            seen_versions.add(version)
            boundaries.append(VersionBoundary(version=version, sha=full_sha, date=date))

    return boundaries


def get_all_commits(repo_path: str, plugin_path: str) -> list[Commit]:
    """Get all commits that touched the plugin directory."""
    log = git(repo_path, "log", "--pretty=format:%H  %h  %ai  %an  %s",
              "--", plugin_path)
    if not log:
        return []

    commits = []
    for line in log.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("  ", 4)
        if len(parts) < 5:
            continue
        full_sha, short_sha, date_str, author, subject = parts
        date = date_str[:10]

        # Skip pure merge commits
        if subject.startswith("Merge remote-tracking branch") or subject.startswith("Merge branch"):
            continue

        commits.append(Commit(
            full_sha=full_sha,
            short_sha=short_sha,
            date=date,
            author=author,
            subject=subject
        ))

    return commits


def classify_commit(subject: str) -> tuple[str, str, str]:
    """Classify a commit into (category, title, description)."""
    subject_lower = subject.lower()

    # Strip conventional commit prefix
    cleaned = re.sub(r'^(feat|fix|docs|chore|refactor|security|perf|test|ci|build|style)\s*(\([^)]*\))?\s*:\s*', '', subject, flags=re.IGNORECASE)

    # Remove PR reference from end
    cleaned = re.sub(r'\s*\(#\d+\)$', '', cleaned).strip()

    # Determine category
    if subject_lower.startswith("fix") or "bug" in subject_lower or "crash" in subject_lower:
        category = "Fixed"
    elif subject_lower.startswith("docs") or "readme" in subject_lower:
        category = "Docs"
    elif subject_lower.startswith("security") or "permission" in subject_lower.split(":")[0] if ":" in subject_lower else False:
        category = "Security"
    elif subject_lower.startswith("feat") or subject_lower.startswith("add"):
        category = "Added"
    elif any(w in subject_lower for w in ["refactor", "rename", "update", "change", "remove", "migrate", "switch"]):
        category = "Changed"
    else:
        category = "Added"

    # Generate title — first few words, capitalized
    words = cleaned.split()
    title = " ".join(words[:5]) if len(words) > 5 else cleaned
    if len(title) > 60:
        title = title[:57] + "..."
    description = cleaned

    return category, title, description


def group_commits_by_version(
    commits: list[Commit],
    boundaries: list[VersionBoundary]
) -> list[VersionSection]:
    """Group commits into version sections based on version boundaries."""

    if not commits:
        return []

    # boundaries are newest-first from git log; we need them oldest-first for ranging
    boundaries_oldest_first = list(reversed(boundaries))

    # Build a map of sha -> boundary for quick lookup
    boundary_shas = {b.sha: b for b in boundaries}

    # Find the index of each boundary commit in the commit list
    # commits are newest-first
    boundary_positions = {}
    for i, c in enumerate(commits):
        if c.full_sha in boundary_shas:
            boundary_positions[c.full_sha] = i

    sections = []

    if not boundaries:
        # No versions at all — everything is Unreleased
        entries = []
        for c in commits:
            cat, title, desc = classify_commit(c.subject)
            entries.append(ChangeEntry(category=cat, title=title, description=desc, commit=c))
        sections.append(VersionSection(version="Unreleased", date=None, entries=entries))
        return sections

    # Find the newest boundary commit position in the commit list
    # Everything before (newer than) that position is Unreleased
    newest_boundary = boundaries[0]  # newest version
    newest_pos = boundary_positions.get(newest_boundary.sha)

    if newest_pos is not None and newest_pos > 0:
        # There are commits newer than the latest version
        unreleased_commits = commits[:newest_pos]
        entries = []
        for c in unreleased_commits:
            cat, title, desc = classify_commit(c.subject)
            entries.append(ChangeEntry(category=cat, title=title, description=desc, commit=c))
        if entries:
            sections.append(VersionSection(version="Unreleased", date=None, entries=entries))

    # Now group commits for each version
    for i, boundary in enumerate(boundaries):
        pos = boundary_positions.get(boundary.sha)
        if pos is None:
            continue

        # Find the next (older) boundary
        if i + 1 < len(boundaries):
            next_boundary = boundaries[i + 1]
            next_pos = boundary_positions.get(next_boundary.sha)
            if next_pos is not None:
                version_commits = commits[pos:next_pos]
            else:
                version_commits = commits[pos:]
        else:
            # Oldest version — includes all remaining commits
            version_commits = commits[pos:]

        entries = []
        for c in version_commits:
            cat, title, desc = classify_commit(c.subject)
            entries.append(ChangeEntry(category=cat, title=title, description=desc, commit=c))

        if entries:
            sections.append(VersionSection(
                version=boundary.version,
                date=boundary.date,
                entries=entries
            ))

    return sections


def format_changelog(
    plugin_name: str,
    plugin_path: str,
    sections: list[VersionSection]
) -> str:
    """Format version sections into a CHANGELOG.md string."""

    lines = [
        f"# Changelog — {plugin_name}",
        "",
        f"All notable changes to `{plugin_path}` in",
        f"[anthropics/claude-plugins-official]({REPO_URL}).",
        "",
        "Versions refer to the `version` field in `.claude-plugin/plugin.json` where available.",
        "This changelog was compiled from the merged PR and commit history on the `main` branch.",
        "",
        "---",
    ]

    for section in sections:
        lines.append("")
        if section.version == "Unreleased":
            lines.append("## [Unreleased]")
        else:
            date_str = f" — {section.date}" if section.date else ""
            lines.append(f"## [{section.version}]{date_str}")

        # Group entries by category
        by_category = defaultdict(list)
        for entry in section.entries:
            by_category[entry.category].append(entry)

        # Output in standard order
        for category in ["Added", "Changed", "Fixed", "Security", "Docs"]:
            if category not in by_category:
                continue
            lines.append("")
            lines.append(f"### {category}")
            for entry in by_category[category]:
                c = entry.commit
                lines.append(f"- **{entry.title}** — {entry.description}")
                ref = f"  [`{c.short_sha}`]({REPO_URL}/commit/{c.full_sha}) · {c.date}"
                if c.pr_number:
                    ref += f" · ([#{c.pr_number}]({REPO_URL}/pull/{c.pr_number}))"
                lines.append(ref)

    lines.append("")
    return "\n".join(lines)


def format_rollup(plugin_summaries: list[dict]) -> str:
    """Format a repo-level rollup changelog."""
    lines = [
        "# Changelog — Claude Code Plugins",
        "",
        f"Summary of all plugin releases in",
        f"[anthropics/claude-plugins-official]({REPO_URL}).",
        "See each plugin's CHANGELOG.md for full details.",
        "",
        "---",
    ]

    # Group by date
    by_date = defaultdict(list)
    for ps in plugin_summaries:
        for section in ps["sections"]:
            if section.version == "Unreleased":
                # Use the most recent entry's date
                if section.entries:
                    date = section.entries[0].commit.date
                    by_date[date].append({
                        "plugin_path": ps["plugin_path"],
                        "plugin_name": ps["plugin_name"],
                        "version": "Unreleased",
                        "headline": section.entries[0].description[:78],
                    })
            else:
                if section.date:
                    headline = section.entries[0].description[:78] if section.entries else ""
                    by_date[section.date].append({
                        "plugin_path": ps["plugin_path"],
                        "plugin_name": ps["plugin_name"],
                        "version": section.version,
                        "headline": headline,
                    })

    for date in sorted(by_date.keys(), reverse=True):
        lines.append("")
        lines.append(f"## {date}")
        for item in sorted(by_date[date], key=lambda x: x["plugin_name"]):
            version_display = item["version"]
            changelog_path = f"{item['plugin_path']}/CHANGELOG.md"
            lines.append("")
            lines.append(f"### {item['plugin_name']} → [{version_display}]({changelog_path})")
            lines.append(item["headline"])

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate changelogs for Claude Code plugins")
    parser.add_argument("repo_path", help="Path to local clone of claude-plugins-official")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: write into repo clone)")
    parser.add_argument("--plugin", "-p", help="Generate for a single plugin (e.g. external_plugins/telegram)")
    parser.add_argument("--rollup", action="store_true", help="Also generate repo-level rollup changelog")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo_path)
    output_dir = os.path.abspath(args.output_dir) if args.output_dir else repo_path

    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"Error: {repo_path} is not a git repository", file=sys.stderr)
        sys.exit(1)

    # Discover plugins
    if args.plugin:
        plugins = [(args.plugin, args.plugin.split("/")[0])]
    else:
        plugins = discover_plugins(repo_path)

    print(f"Found {len(plugins)} plugins")

    plugin_summaries = []

    for plugin_path, plugin_type in plugins:
        plugin_name = get_plugin_name(repo_path, plugin_path)
        print(f"  Generating: {plugin_name} ({plugin_path})")

        # Get version history
        boundaries = get_version_history(repo_path, plugin_path)
        if boundaries:
            print(f"    Versions: {', '.join(b.version for b in boundaries)}")
        else:
            print(f"    Versions: none found")

        # Get all commits
        commits = get_all_commits(repo_path, plugin_path)
        print(f"    Commits: {len(commits)}")

        if not commits:
            print(f"    Skipping (no commits)")
            continue

        # Group by version
        sections = group_commits_by_version(commits, boundaries)

        # Format
        changelog = format_changelog(plugin_name, plugin_path, sections)

        # Write
        out_path = os.path.join(output_dir, plugin_path, "CHANGELOG.md")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            f.write(changelog)
        print(f"    Wrote: {out_path}")

        plugin_summaries.append({
            "plugin_path": plugin_path,
            "plugin_name": plugin_name,
            "plugin_type": plugin_type,
            "version": get_plugin_version(repo_path, plugin_path),
            "description": get_plugin_description(repo_path, plugin_path),
            "sections": sections,
        })

    # Rollup
    if args.rollup and len(plugin_summaries) > 1:
        rollup = format_rollup(plugin_summaries)
        rollup_path = os.path.join(output_dir, "CHANGELOG.md")
        with open(rollup_path, "w") as f:
            f.write(rollup)
        print(f"\nWrote rollup: {rollup_path}")

    # Write a JSON index for the Jekyll site
    index = []
    for ps in plugin_summaries:
        latest_version = ps["version"] or "unreleased"
        last_updated = None
        if ps["sections"] and ps["sections"][0].entries:
            last_updated = ps["sections"][0].entries[0].commit.date
        index.append({
            "name": ps["plugin_name"],
            "path": ps["plugin_path"],
            "type": ps["plugin_type"],
            "version": latest_version,
            "description": ps["description"],
            "last_updated": last_updated,
            "changelog": f"{ps['plugin_path']}/CHANGELOG.md",
        })

    index_path = os.path.join(output_dir, "_data", "plugins.json")
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
    print(f"\nWrote plugin index: {index_path}")

    print(f"\nDone! Generated {len(plugin_summaries)} changelogs.")


if __name__ == "__main__":
    main()
