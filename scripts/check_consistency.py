#!/usr/bin/env python3
"""Consistency checks for OKF bundles: manifests, indexes, placeholders,
sources/footnotes, skill naming, subtype graph, URL form.

Usage: python scripts/check_consistency.py <bundle-root> [...]
Exit 1 on any ERROR (warnings never fail).
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    RESERVED_FILES,
    _ignored_set,
    _is_local_only,
    iter_bundle_mds,
    parse_frontmatter,
)
from _common import (
    SKIP_DIRS as _BASE_SKIP_DIRS,
)

try:
    import yaml
except ImportError:
    yaml = None

SKIP_DIRS = _BASE_SKIP_DIRS | {".openclaw"}
JSONC_ALLOW = {"qoder-hooks.json"}
PLACEHOLDERS = [
    r"\[Step \d+\]",
    r"\[Precondition \d+\]",
    r"\[Postcondition \d+\]",
    r"\[Invariant \d+\]",
    r"\[verification command\]",
    r"\[Expected (outcome|output)",
    r"\[Output artifact\]",
    r"\[Next skill",
    r"\bTODO\b",
    r"\bFIXME\b",
    r"\[planned\]",
]
ABSTRACTS_RE = re.compile(r"https://(?:www\.)?github\.com/Yoseph-Zuskin/okf-abstracts")


def find_manifests(root):
    return list(root.rglob("plugin.json")) + list(root.rglob("manifest.json"))


def push_completeness(root, issues):
    """Index/manifest entries must resolve post-push: flag entries pointing
    at git-ignored, untracked files. Skipped outside git work trees."""
    import subprocess

    try:
        r = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            timeout=30,
        )
    except (OSError, ValueError):
        return
    if r.returncode != 0:
        return
    ignored = _ignored_set(root)
    targets = []
    for idx in list(root.rglob("index.md")):
        if any(p in SKIP_DIRS for p in idx.parts):
            continue
        text = idx.read_text(encoding="utf-8")
        for m in re.finditer(r"\((/[^)]+?\.md)\)", text):
            targets.append((str(idx.relative_to(root)), m.group(1)[1:]))
    for mf in find_manifests(root) + [
        root / "gemini-extension.json",
        root / "plugin.json",
        root / "package.json",
    ]:
        if not mf.exists() or any(p in SKIP_DIRS for p in mf.parts):
            continue
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for key in ("references", "templates", "agents"):
            for entry in data.get(key) or []:
                targets.append((str(mf.relative_to(root)), entry))
    seen = set()
    for src, target in targets:
        if target in seen:
            continue
        seen.add(target)
        tp = root / target
        if _is_local_only(tp, root, ignored):
            issues.append(
                ("ERROR", f"{src}: {target} is git-ignored (dangles post-push)")
            )


def strip_code(text):
    text = re.sub(r"(?s)```.*?```", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def check_manifests(root, issues):
    version = None
    vf = root / "VERSION"
    if vf.exists():
        version = vf.read_text(encoding="utf-8").strip()
    for mf in find_manifests(root) + [
        root / "gemini-extension.json",
        root / "plugin.json",
        root / "package.json",
        root / "ai-pm-mcp" / "package.json",
        root / "pi-extension" / "package.json",
    ]:
        if not mf.exists() or any(p in SKIP_DIRS for p in mf.parts):
            continue
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
        except ValueError as e:
            if mf.name not in JSONC_ALLOW:
                issues.append(("ERROR", f"{mf.relative_to(root)}: invalid JSON: {e}"))
            continue
        rel = str(mf.relative_to(root))
        if (
            isinstance(data.get("version"), str)
            and version
            and data["version"] != version
        ):
            issues.append(
                ("ERROR", f"{rel}: version {data['version']} != VERSION {version}")
            )
        skills = data.get("skills")
        if isinstance(skills, list):
            on_disk = (
                sorted(d.name for d in (root / "skills").iterdir() if d.is_dir())
                if (root / "skills").is_dir()
                else []
            )
            for s in skills:
                if s not in on_disk:
                    issues.append(("ERROR", f"{rel}: skill {s} not on disk"))
            for s in on_disk:
                if s not in skills:
                    issues.append(
                        ("ERROR", f"{rel}: skill {s} on disk, missing from manifest")
                    )
        elif isinstance(skills, str):
            if not (root / skills).is_dir():
                issues.append(("ERROR", f"{rel}: skills dir {skills} missing"))
        for key in ("references", "templates", "agents"):
            for entry in data.get(key) or []:
                if not (root / entry).exists():
                    issues.append(("ERROR", f"{rel}: {key} entry {entry} missing"))


def check_indexes(root, issues):
    ignored = _ignored_set(root)
    for idx in (
        (root / "entities").rglob("index.md") if (root / "entities").is_dir() else []
    ):
        layer = idx.parent
        linked = set(
            re.findall(r"\((/entities/[^)]+?\.md)\)", idx.read_text(encoding="utf-8"))
        )
        on_disk = set(
            "/entities/" + layer.name + "/" + f.name
            for f in layer.glob("*.md")
            if f.name != "index.md"
        )
        for missing in sorted(on_disk - linked):
            # git-ignored local-only files are exempt from indexing
            if _is_local_only(root / missing[1:], root, ignored):
                continue
            issues.append(
                ("ERROR", f"{idx.relative_to(root)}: {missing} on disk, not indexed")
            )
        for stale in sorted(linked - on_disk):
            issues.append(
                ("ERROR", f"{idx.relative_to(root)}: indexed {stale} missing on disk")
            )
    bidx = root / "index.md"
    if bidx.exists():
        text = bidx.read_text(encoding="utf-8")
        for sub in ["concepts", "templates"]:
            for f in (root / sub).glob("*.md"):
                if f.name not in text:
                    issues.append(
                        ("WARNING", f"index.md: {sub}/{f.name} not mentioned")
                    )
        skills_dir = root / "skills"
        if skills_dir.is_dir():
            mentioned = set()
            for d in skills_dir.iterdir():
                if d.is_dir() and d.name in text:
                    mentioned.add(d.name)
            if mentioned:
                for d in skills_dir.iterdir():
                    if d.is_dir() and d.name not in text:
                        issues.append(
                            ("WARNING", f"index.md: skill {d.name} not mentioned")
                        )


def check_placeholders(root, issues):
    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        if f.name in RESERVED_FILES:
            continue
        text = strip_code(f.read_text(encoding="utf-8"))
        for pat in PLACEHOLDERS:
            if re.search(pat, text):
                issues.append(("ERROR", f"{f.relative_to(root)}: placeholder {pat}"))
                break


def check_sources(root, issues):
    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        if f.name in RESERVED_FILES:
            continue
        text = f.read_text(encoding="utf-8")
        try:
            fm, _ = parse_frontmatter(text)
        except ValueError:
            continue
        if not fm:
            continue
        src = fm.get("sources")
        entries = src if isinstance(src, list) else []
        ids = set(
            str(e["id"])
            for e in entries
            if isinstance(e, dict) and e.get("id") is not None
        )
        body = strip_code(text.split("---", 2)[-1] if text.startswith("---") else text)
        cites = set(m.group(1) for m in re.finditer(r"\[\^([^\]]+)\](?!:)", body))
        for c in sorted(cites - ids):
            issues.append(
                ("ERROR", f"{f.relative_to(root)}: footnote [^{c}] has no sources id")
            )
        for sid in sorted(ids - cites):
            if f"[^{sid}]" not in body:
                issues.append(
                    ("ERROR", f"{f.relative_to(root)}: sources id {sid} never cited")
                )


def check_skills(root, issues):
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return
    ignored = _ignored_set(root)
    for d in sorted(skills_dir.iterdir()):
        if not d.is_dir():
            continue
        if _is_local_only(d / "SKILL.md", root, ignored):
            continue
        sf = d / "SKILL.md"
        if not sf.exists():
            issues.append(("ERROR", f"skills/{d.name}: SKILL.md missing"))
            continue
        try:
            fm, _ = parse_frontmatter(sf.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if fm.get("name") != d.name:
            issues.append(("ERROR", f"skills/{d.name}: name != dirname"))
        if len(str(fm.get("description") or "")) > 1024:
            issues.append(("ERROR", f"skills/{d.name}: description over 1024 chars"))
        if not fm.get("displayName"):
            issues.append(("ERROR", f"skills/{d.name}: displayName missing"))


def check_graph(root, issues):
    ent = root / "entities"
    if not ent.is_dir():
        return
    titles = {}
    edges = {}
    for f in ent.rglob("*.md"):
        if f.name == "index.md":
            continue
        try:
            fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not str(fm.get("type") or "").startswith("Class"):
            continue
        title = fm.get("title")
        if not title:
            continue
        title = str(title).strip()
        titles[title] = f
        sub = fm.get("subtype_of")
        entries = sub if isinstance(sub, list) else []
        edges[title] = [
            str(e.get("type")).strip()
            for e in entries
            if isinstance(e, dict) and e.get("type")
        ]
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {t: WHITE for t in titles}
    stack = []

    def visit(t):
        color[t] = GRAY
        stack.append(t)
        for p in edges.get(t, []):
            if p not in titles:
                continue
            if color[p] == GRAY:
                issues.append(("ERROR", "subtype cycle: " + " -> ".join(stack + [p])))
            elif color[p] == WHITE:
                visit(p)
        stack.pop()
        color[t] = BLACK

    for t in titles:
        if color[t] == WHITE:
            visit(t)


def check_provenance(root, issues):
    if yaml is None:
        return

    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        if f.name in RESERVED_FILES:
            continue
        try:
            fm, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        rel = str(f.relative_to(root))
        gen = fm.get("generated")
        if gen is not None:
            if not isinstance(gen, dict) or not gen.get("by") or not gen.get("at"):
                issues.append(("ERROR", f"{rel}: generated must carry by and at only"))
            elif set(gen) - {"by", "at"}:
                issues.append(("ERROR", f"{rel}: generated carries extra keys"))
        ver = fm.get("verified")
        if ver is None:
            continue
        entries = ver if isinstance(ver, list) else [ver]
        for entry in entries:
            if (
                not isinstance(entry, dict)
                or not entry.get("by")
                or not entry.get("at")
            ):
                issues.append(
                    ("ERROR", f"{rel}: verified entries must carry by and at only")
                )
            elif set(entry) - {"by", "at"}:
                issues.append(("ERROR", f"{rel}: verified entry carries extra keys"))


def check_tables(root, issues):
    """No empty lines inside markdown tables (header, separator, and data
    rows stay consecutive). Fenced code blocks are not tables."""
    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        if f.name in RESERVED_FILES:
            continue
        lines = f.read_text(encoding="utf-8").splitlines()
        in_fence = False
        in_table = False
        for i, line in enumerate(lines):
            s = line.strip()
            if s.startswith("```"):
                in_fence = not in_fence
                in_table = False
                continue
            if in_fence:
                continue
            if "|" in line and "---" in line:
                in_table = True
                continue
            if in_table:
                if "|" in line:
                    continue
                if s == "":
                    # Peek ahead: a fresh header+separator block means a NEW
                    # table (blank correctly separates them); bare rows mean
                    # this table was split.
                    k = i + 1
                    while k < len(lines) and lines[k].strip() == "":
                        k += 1
                    group = []
                    while k < len(lines) and "|" in lines[k]:
                        group.append(lines[k])
                        k += 1
                    if any("---" in g for g in group):
                        in_table = False
                    elif group:
                        issues.append(
                            (
                                "ERROR",
                                f"{f.relative_to(root)}:{i + 1}: empty line inside table",
                            )
                        )
                    else:
                        in_table = False
                else:
                    in_table = False


def check_fences(root, issues):
    """Every fenced code block must close: an odd fence count means the
    rest of the file renders as code."""
    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        n = sum(
            1
            for line in f.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("```")
        )
        if n % 2:
            issues.append(
                ("ERROR", f"{f.relative_to(root)}: unclosed fenced code block")
            )


def check_connectivity(root, issues):
    """Instance content (concepts, skills, lessons, agents, root program
    files) should link explicitly to related concepts — tags alone do not
    make the knowledge graph. References/, templates/, and entities/ are
    exempt by design (self-contained forms; lattice links live in
    frontmatter). WARNING only."""
    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        if f.name in RESERVED_FILES:
            continue
        rel = f.relative_to(root).as_posix()
        parts = Path(rel).parts
        in_scope = (
            parts[0] in ("concepts", "skills", "agents")
            or "lessons" in parts
            or (len(parts) == 1 and rel.endswith(".md"))
        )
        if not in_scope:
            continue
        text = f.read_text(encoding="utf-8")
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        body = strip_code(body)
        linked = any(
            m.group(1).endswith(".md")
            or "/entities/" in m.group(1)
            or "/concepts/" in m.group(1)
            for m in re.finditer(r"\]\(([^)]+)\)", body)
        )
        if not linked:
            issues.append(
                ("WARNING", f"{rel}: no explicit cross-concept links (tags only)")
            )


def check_urls(root, issues):
    for f in iter_bundle_mds(root, skip_local_only=True, skip_dirs=SKIP_DIRS):
        if f.name in RESERVED_FILES:
            continue
        text = f.read_text(encoding="utf-8")
        for m in ABSTRACTS_RE.finditer(text):
            if not m.group(0).startswith("https://www.github.com/"):
                issues.append(
                    ("WARNING", f"{f.relative_to(root)}: non-www abstracts URL")
                )
                break


def main():
    if len(sys.argv) < 2:
        print("Usage: check_consistency.py <bundle-root> [...]")
        return 2
    issues = []
    multi = len(sys.argv[1:]) > 1
    checked = 0
    for arg in sys.argv[1:]:
        root = Path(arg)
        if multi:
            print(f"=== {root}")
        checked += sum(
            1 for f in root.rglob("*.md") if not any(p in SKIP_DIRS for p in f.parts)
        )
        check_manifests(root, issues)
        check_indexes(root, issues)
        check_placeholders(root, issues)
        check_sources(root, issues)
        check_skills(root, issues)
        check_graph(root, issues)
        check_urls(root, issues)
        check_provenance(root, issues)
        check_connectivity(root, issues)
        check_fences(root, issues)
        check_tables(root, issues)
        push_completeness(root, issues)
    errs = [i for i in issues if i[0] == "ERROR"]
    for level, msg in issues:
        print(f"{level}: {msg}")
    print(
        f"Checked {checked} files. Total: {len(errs)} errors, {len(issues) - len(errs)} warnings"
    )
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
