#!/usr/bin/env python3
"""
Version bump script for okf-abstracts.
Bumps the bundle's own version in VERSION and every manifest carrying it.
Usage: python bump_version.py [major|minor|patch|<explicit>]
"""

import re
import sys
from pathlib import Path

# Every manifest carrying the bundle's own version (plain "0.1.0" form).
MANIFESTS = [
    Path("package.json"),
    Path(".codex-plugin/plugin.json"),
    Path(".claude-plugin/plugin.json"),
    Path(".devin-plugin/plugin.json"),
    Path(".grok-plugin/plugin.json"),
    Path(".qoder-plugin/plugin.json"),
    Path(".openclaw/skills/okf-abstracts/manifest.json"),
    Path(".github/plugin.json"),
]


def bump_version(version: str, part: str) -> str:
    """Bump version string (major.minor.patch)."""
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid version part: {part}")
    return f"{major}.{minor}.{patch}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python bump_version.py [major|minor|patch|<x.y.z>]")
        sys.exit(1)

    part = sys.argv[1]

    # Read current version
    version_file = Path("VERSION")
    if not version_file.exists():
        print("Error: VERSION file not found")
        sys.exit(1)

    current_version = version_file.read_text().strip()
    if re.fullmatch(r"\d+\.\d+\.\d+", part or ""):
        new_version = part
    elif part in ("major", "minor", "patch"):
        new_version = bump_version(current_version, part)
    else:
        print("Error: argument must be major|minor|patch or explicit x.y.z")
        sys.exit(1)

    # Update VERSION file
    Path("VERSION").write_text(new_version + "\n")

    # Update every manifest carrying the bundle version
    changed = ["VERSION"]
    for mf in MANIFESTS:
        if not mf.exists():
            continue
        text = mf.read_text(encoding="utf-8")
        updated, n = re.subn(
            r'"version":\s*"\d+\.\d+\.\d+"', f'"version": "{new_version}"', text
        )
        if n:
            mf.write_text(updated, encoding="utf-8")
            changed.append(str(mf))

    print(f"Bumped version: {current_version} -> {new_version}")
    print("Changed: " + ", ".join(changed))


if __name__ == "__main__":
    main()
