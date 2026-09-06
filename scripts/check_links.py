#!/usr/bin/env python3
"""Check that internal markdown links resolve inside OKF bundles.

Usage: python scripts/check_links.py <bundle-root> [<bundle-root> ...]

Rules: http(s) links skipped (external). Leading '/' resolves against the
bundle root (bundle-relative convention). Otherwise relative to the file.
Links escaping the bundle root or pointing at missing files are reported.
Exit 1 on any broken link.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import iter_bundle_mds  # noqa: E402

LINK_RE = re.compile(r"\]\(([^)#]+?\.md)(?:#[^)]*)?\)")


def check_bundle(root: Path) -> list:
    bad = []
    checked = 0
    root = root.resolve()
    for f in iter_bundle_mds(root, skip_local_only=True):
        try:
            t = f.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in LINK_RE.finditer(t):
            target = m.group(1)
            if target.startswith(("http://", "https://")):
                continue
            checked += 1
            resolved = (
                (root / target[1:]) if target.startswith("/") else (f.parent / target)
            ).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                bad.append(f"{f.relative_to(root)} -> {target} (escapes bundle)")
                continue
            if not resolved.exists():
                bad.append(f"{f.relative_to(root)} -> {target} (missing)")
    return checked, bad


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_links.py <bundle-root> [...]")
        return 2
    total_bad = []
    total_checked = 0
    for arg in sys.argv[1:]:
        checked, bad = check_bundle(Path(arg))
        total_checked += checked
        total_bad += bad
    print(f"checked {total_checked} internal links; {len(total_bad)} broken")
    for b in total_bad:
        print(b)
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
