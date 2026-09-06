#!/usr/bin/env python3
"""Shared helpers for the okf-abstracts scripts (stdlib + pyyaml only).

Import with:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _common import parse_frontmatter  # noqa: E402
"""

from pathlib import Path
from typing import Any, Dict, Iterator, Optional, Set, Tuple

# Spec-reserved (index, log) and repo scaffolding: never OKF concepts.
# Ontology checks skip them always; hygiene checks (links, newlines) still
# cover them.
RESERVED_FILES = frozenset(
    {
        "index.md",
        "log.md",
        "README.md",
        "CHANGELOG.md",
        "AGENTS.md",
        "privacy.md",
        "terms.md",
    }
)

SKIP_DIRS = frozenset({"node_modules", ".git", ".venv", "__pycache__"})


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content. Returns (frontmatter_dict, body).
    Raises ValueError if frontmatter contains empty lines (not allowed per OKF spec)."""
    import yaml

    if not content.startswith("---\n"):
        return {}, content
    end = content.find("\n---", 4)
    if end == -1:
        return {}, content
    fm_text = content[4:end]

    # Check for empty lines in frontmatter (not allowed per OKF spec)
    for i, line in enumerate(fm_text.split("\n"), 1):
        if not line.strip():
            raise ValueError(
                f"Empty line at line {i} in frontmatter (empty lines not allowed in frontmatter)"
            )

    body = content[end + 4 :]
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")
    return fm or {}, body


def _ignored_set(root):
    """Root-relative posix paths that are git-ignored AND untracked, i.e.
    absent post-push. Empty set outside git work trees (fail-open)."""
    import subprocess

    try:
        out = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "--others",
                "--ignored",
                "--exclude-standard",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if out.returncode != 0:
            return set()
        ignored = set(out.stdout.splitlines())
        tr = subprocess.run(
            ["git", "-C", str(root), "ls-files"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return ignored - set(tr.stdout.splitlines())
    except (OSError, ValueError):
        return set()


def _under_gitkeep(path, root):
    """True if path sits under a directory holding a .gitkeep marker:
    explicitly preserved content stays in scope even when ignored."""
    root = Path(root).resolve()
    d = Path(path).resolve().parent
    while d != root and root in d.parents:
        if (d / ".gitkeep").exists():
            return True
        d = d.parent
    return False


def _is_local_only(path, root, ignored):
    r = Path(root).resolve()
    p = Path(path)
    try:
        rel = (
            ((r / p) if not p.is_absolute() else p).resolve().relative_to(r).as_posix()
        )
    except ValueError:
        return False
    return rel in ignored and not _under_gitkeep(path, root)


def iter_bundle_mds(root, skip_local_only=False, skip_dirs=None):
    """Yield .md files under root, skipping tooling dirs and (optionally)
    git-ignored local-only files. Pass skip_dirs to extend SKIP_DIRS
    (e.g. check_consistency adds '.openclaw')."""
    ignored = _ignored_set(root) if skip_local_only else set()
    skip = SKIP_DIRS if skip_dirs is None else skip_dirs
    for f in Path(root).rglob("*.md"):
        if any(p in skip for p in f.parts) or f.name == ".gitkeep":
            continue
        if skip_local_only and _is_local_only(f, root, ignored):
            continue
        yield f
