#!/usr/bin/env python3
"""
Install the Claude Code status line:
  1. Copy statusline.py to ~/.claude/statusline.py
  2. Merge the JSON below into ~/.claude/settings.json
"""

import json
import os
import shutil

SETTINGS_OVERRIDE = {
    "statusLine": {
        "type": "command",
        "command": "python3 ~/.claude/statusline.py",
        "padding": 0,
        "refreshInterval": 1,
    },
    "verbose": True,
}


def main():
    claude_dir = os.path.expanduser("~/.claude")
    os.makedirs(claude_dir, exist_ok=True)

    statusline_dst = os.path.join(claude_dir, "statusline.py")
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "statusline.py")
    shutil.copy2(src, statusline_dst)
    print(f"Copied statusline.py -> {statusline_dst}")

    settings_path = os.path.join(claude_dir, "settings.json")
    settings = {}
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, OSError):
            settings = {}

    def deep_merge(base, override):
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                deep_merge(base[k], v)
            else:
                base[k] = v

    deep_merge(settings, SETTINGS_OVERRIDE)

    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Updated settings: {settings_path}")
    print("Done. Restart Claude Code to apply the status line.")


if __name__ == "__main__":
    main()
