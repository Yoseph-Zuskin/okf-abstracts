#!/usr/bin/env python3
"""Check every .md file ends with exactly one trailing newline.

Usage: python scripts/check_newlines.py <bundle-root> [<bundle-root> ...]
Exit 1 on any violation. Byte-level: counts trailing LF bytes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_bundle_mds  # noqa: E402


def check_bundle(root: Path) -> list:
    bad = []
    root = root.resolve()
    for f in iter_bundle_mds(root, skip_local_only=True):
        data = f.read_bytes()
        nl = 0
        i = len(data) - 1
        while i >= 0 and data[i] in (10, 13):
            if data[i] == 10:
                nl += 1
            i -= 1
        if nl != 1:
            bad.append(f"{f} : {nl} trailing newlines")
    return bad


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_newlines.py <bundle-root> [...]")
        return 2
    bad = []
    checked = 0
    for arg in sys.argv[1:]:
        root = Path(arg)
        checked += sum(1 for _ in root.rglob("*.md"))
        bad += check_bundle(Path(arg))
    if bad:
        for b in bad:
            print(b)
        return 1
    print(f"ALL OK - every .md file ends with exactly one newline ({checked} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
