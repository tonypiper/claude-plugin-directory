#!/usr/bin/env python3
"""
Gather git history data for one or all Claude Code plugins.

Writes one structured text file per plugin to an output directory
(default: /tmp/claude-changelog-data/). Each file contains:
  - The current plugin.json content
  - Version history (every SHA that touched plugin.json + version at that SHA)
  - All non-merge commits touching the plugin directory, with full bodies

Usage:
  # All plugins
  python3 scripts/gather-plugin-data.py ../claude-plugins-official

  # Single plugin
  python3 scripts/gather-plugin-data.py ../claude-plugins-official --plugin external_plugins/telegram

  # Custom output directory
  python3 scripts/gather-plugin-data.py ../claude-plugins-official --output-dir /tmp/mydata
"""

import argparse
import json
import pathlib
import subprocess
import sys


def get_plugins(repo: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["find", str(repo), "-name", "plugin.json", "-path", "*/.claude-plugin/*"],
        capture_output=True, text=True, check=True,
    )
    paths = []
    for line in result.stdout.strip().splitlines():
        if not line.strip():
            continue
        plugin_path = line.replace(str(repo) + "/", "").replace("/.claude-plugin/plugin.json", "")
        paths.append(plugin_path)
    return sorted(paths)


def gather_plugin(repo: pathlib.Path, plugin: str) -> str:
    out = []

    # --- plugin.json ---
    meta = subprocess.run(
        ["cat", str(repo / plugin / ".claude-plugin" / "plugin.json")],
        capture_output=True, text=True,
    )
    out.append("=== PLUGIN.JSON ===")
    out.append(meta.stdout.strip())

    # --- version history ---
    out.append("\n=== VERSION HISTORY ===")
    out.append("# full_sha  short_sha  version  date  subject")
    vlog = subprocess.run(
        ["git", "-C", str(repo), "log",
         "--pretty=format:%H\t%h\t%ai\t%s",
         "--", f"{plugin}/.claude-plugin/plugin.json"],
        capture_output=True, text=True,
    )
    for line in vlog.stdout.strip().splitlines():
        if not line.strip():
            continue
        try:
            full_sha, short_sha, date, subject = line.split("\t", 3)
        except ValueError:
            continue
        content = subprocess.run(
            ["git", "-C", str(repo), "show", f"{full_sha}:{plugin}/.claude-plugin/plugin.json"],
            capture_output=True, text=True,
        )
        try:
            version = json.loads(content.stdout).get("version", "deleted")
        except (json.JSONDecodeError, AttributeError):
            version = "deleted/parse-error"
        out.append(f"{full_sha}  {short_sha}  {version}  {date[:10]}  {subject}")

    # --- commits ---
    out.append("\n=== COMMITS ===")
    out.append("# Non-merge commits touching the plugin directory, newest first")
    clog = subprocess.run(
        ["git", "-C", str(repo), "log",
         "--pretty=format:COMMIT %H %h %ai%n%s%n%b%n---",
         "--no-merges",
         "--", plugin],
        capture_output=True, text=True,
    )
    out.append(clog.stdout.strip())

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", help="Path to local clone of anthropics/claude-plugins-official")
    parser.add_argument("--plugin", help="Single plugin path (e.g. external_plugins/telegram). Omit for all plugins.")
    parser.add_argument("--output-dir", default="/tmp/claude-changelog-data", help="Directory to write data files (default: /tmp/claude-changelog-data)")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    if not repo.exists():
        print(f"error: repo path not found: {repo}", file=sys.stderr)
        sys.exit(1)

    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plugins = [args.plugin] if args.plugin else get_plugins(repo)
    if not plugins:
        print("error: no plugins found", file=sys.stderr)
        sys.exit(1)

    for plugin in plugins:
        safe_name = plugin.replace("/", "__")
        out_file = output_dir / f"{safe_name}.txt"
        print(f"  gathering: {plugin} ...", end=" ", flush=True)
        try:
            data = gather_plugin(repo, plugin)
            out_file.write_text(data)
            print(f"→ {out_file}")
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)

    print(f"\nDone. {len(plugins)} plugin(s) written to {output_dir}/")
    if len(plugins) > 1:
        print("\nPlugin list:")
        for p in plugins:
            safe = p.replace("/", "__")
            print(f"  {output_dir}/{safe}.txt")


if __name__ == "__main__":
    main()
