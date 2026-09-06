#!/usr/bin/env python3
"""
OKF Abstracts Subtype Validation Script

Validates subtype_of[] linkage in OKF v0.2 bundles:
1. First entry matches concept type (warning if other entry matches)
2. Header matching against abstract subtypes' required headers
3. Missing version warnings

Abstract version change detection lives in check_abstract_lineage.sh.

Usage: python scripts/validate_subtype.py <bundle-path> [--strict] [--abstracts-repo <path>]

Dependencies: Python 3.6+, stdlib plus pyyaml (pip install -r requirement.txt)
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    RESERVED_FILES,
    _ignored_set,
    _is_local_only,
    parse_frontmatter,
)

# =============================================================================
# Abstract Entity Loading
# =============================================================================


def load_abstract_entities(
    bundle_path: Path, abstracts_repo: Optional[Path] = None
) -> Dict[str, Dict]:
    """
    Load abstract entity definitions from the bundle being validated and optionally
    from the okf-abstracts repo. Returns a dict mapping entity type to its metadata
    including required headers from the # Contract section.
    """
    entities = {}

    # Load from the bundle's own entities/ directory first (custom subtypes)
    bundle_entities_path = bundle_path / "entities"
    if bundle_entities_path.exists():
        entities.update(_load_entities_from_dir(bundle_entities_path))

    # Then load from okf-abstracts repo (base ontology)
    if abstracts_repo and abstracts_repo.exists():
        abstracts_entities_path = abstracts_repo / "entities"
        if abstracts_entities_path.exists():
            entities.update(_load_entities_from_dir(abstracts_entities_path))

    return entities


def _load_entities_from_dir(entities_dir: Path) -> Dict[str, Dict]:
    """
    Load abstract entity definitions from an entities/ directory.
    Scans all .md files in subdirectories for type: Class definitions.
    """
    entities = {}

    for md_file in entities_dir.rglob("*.md"):
        if entities_dir.name == "entities" and md_file.parent == entities_dir:
            continue  # Skip root entities/ files like index.md

        content = md_file.read_text(encoding="utf-8")
        try:
            fm, body = parse_frontmatter(content)
        except ValueError:
            continue

        if not fm or fm.get("type") != "Class":
            continue

        entity_type = fm.get("title") or fm.get("name") or md_file.stem
        if not entity_type:
            continue

        # Extract required headers from # Contract section
        required_headers = _extract_required_headers(body)

        # Extract required_tags from frontmatter
        required_tags = fm.get("required_tags", [])
        if not isinstance(required_tags, list):
            required_tags = []

        entities[entity_type] = {
            "required_headers": required_headers,
            "required_tags": set(required_tags),
            "description": fm.get("description", ""),
            "source_file": str(md_file),
        }

    return entities


def _extract_required_headers(body: str) -> Set[str]:
    """
    Extract required headers from the # Contract section of an abstract entity.
    Looks for lines like '### Required Headers' or bullet points under ## Contract.
    """
    headers = set()
    in_contract = False
    in_required = False

    for line in body.split("\n"):
        stripped = line.strip()

        if stripped.startswith("## Contract"):
            in_contract = True
            continue
        elif stripped.startswith("## ") and in_contract:
            in_contract = False
            in_required = False
            continue

        if in_contract:
            if re.match(r"^###\s+Required\s+Headers?", stripped, re.IGNORECASE):
                in_required = True
                continue
            elif stripped.startswith("### ") and in_required:
                in_required = False
                continue

            if in_required:
                # Only the contiguous bullet list right under the heading counts.
                # A prose paragraph ends the list (otherwise trailing MUST
                # bullets elsewhere in ## Contract leak in as requirements).
                if stripped == "":
                    continue
                match = re.match(r"^[-*]\s*(.+)$", stripped)
                if match:
                    header_text = match.group(1).strip()
                    # Extract header name (remove markdown formatting)
                    header_text = re.sub(r"`([^`]+)`", r"\1", header_text)
                    header_text = re.sub(r"\*\*([^*]+)\*\*", r"\1", header_text)
                    headers.add(header_text)
                else:
                    in_required = False

    return headers


# =============================================================================
# Header Extraction
# =============================================================================

# Header level mapping (header text -> level)
# Note: Placeholder variants like [text], (text), {text}, <text> are normalized for matching
# Ponytail: broad pattern is intentional — humans/agents use [], (), {}, <> inconsistently;
# strict validation would reject valid files. Accept all four, normalize to bare text.
HEADER_LEVEL_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")
PLACEHOLDER_PATTERN = re.compile(r"\[.*?\]|\(.*?\)|\{.*?\}|<.*?>")


def extract_headers(body: str) -> Dict[int, Set[str]]:
    """Extract headers grouped by level."""
    headers_by_level = defaultdict(set)
    for line in body.split("\n"):
        match = HEADER_LEVEL_PATTERN.match(line.strip())
        if match:
            level = len(match.group(1))
            header_text = match.group(2).strip()
            headers_by_level[level].add(header_text)
    return dict(headers_by_level)


# =============================================================================
# Frontmatter Helpers
# =============================================================================

# Canonical subtype-linkage key plus accepted aliases.
# Canonical `subtype_of` reads correctly ("I am a subtype of X"); the legacy
# plural `subtypes_of` reads backwards (children, not parents) but is accepted
# with warnings, as are `subclass_of` (OWL term) and `subconcept_of` (OKF term).
SUBTYPE_KEY_CANONICAL = "subtype_of"
SUBTYPE_KEY_ALIASES = ("subtypes_of", "subclass_of", "subconcept_of")
# Plural aliases read backwards (children, not parents); singular ones do not.
# (Explicit set: "subclass_of" ends in s_of but is singular.)
SUBTYPE_KEY_PLURALS = {"subtypes_of"}


def get_subtype_of(fm: Dict) -> Tuple[List[Dict], Optional[str]]:
    """Get subtype linkage list from frontmatter. Returns (entries, key_used)."""
    if isinstance(fm.get(SUBTYPE_KEY_CANONICAL), list):
        return fm[SUBTYPE_KEY_CANONICAL], SUBTYPE_KEY_CANONICAL
    for alias in SUBTYPE_KEY_ALIASES:
        if isinstance(fm.get(alias), list):
            return fm[alias], alias
    return [], None


# =============================================================================
# Concept Validation
# =============================================================================


def validate_concept(
    filepath: Path,
    abstract_entities: Dict[str, Dict],
) -> List[Tuple[str, str]]:
    """
    Validate a single concept file.
    Returns list of (level, message) where level is "ERROR" or "WARNING".
    """
    issues = []
    content = filepath.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(content)
    except ValueError as e:
        issues.append(("ERROR", str(e)))
        return issues

    if not fm:
        issues.append(("ERROR", "No valid frontmatter"))
        return issues

    concept_type = fm.get("type")
    if not concept_type:
        issues.append(("ERROR", "Missing 'type' in frontmatter"))
        return issues

    subtype_of, subtype_key = get_subtype_of(fm)
    if not subtype_of:
        issues.append(("WARNING", "No 'subtype_of' entries"))
    else:
        if subtype_key != SUBTYPE_KEY_CANONICAL:
            issues.append(
                (
                    "WARNING",
                    f"Non-canonical subtype key '{subtype_key}' (expected '{SUBTYPE_KEY_CANONICAL}')",
                )
            )
            if subtype_key in SUBTYPE_KEY_PLURALS:
                issues.append(
                    (
                        "WARNING",
                        f"Plural subtype key '{subtype_key}' reads as children-not-parents; use '{SUBTYPE_KEY_CANONICAL}'",
                    )
                )
        # Check 1: First entry matches concept type
        # Special case: Abstract entity definitions (type: Class) with subtype_of: Concept are valid
        # (Thing root uses Spec parent: lattice root is a subtype of the OKF spec itself)
        first_type = subtype_of[0].get("type") if subtype_of else None
        if concept_type == "Class" and first_type == "Concept":
            # Abstract entity definition - valid
            pass
        elif concept_type == "Class":
            # Abstract entity definition: parent must be a known abstract class
            # (or the Spec anchor), and an entity cannot subtype itself.
            own_title = fm.get("title")
            if first_type == "Spec":
                pass
            elif first_type not in abstract_entities:
                issues.append(
                    (
                        "ERROR",
                        f"Parent class '{first_type}' is not a known abstract entity",
                    )
                )
            elif first_type == own_title:
                issues.append(("ERROR", f"Entity '{own_title}' cannot subtype itself"))
        elif first_type != concept_type:
            # Check if any other entry matches
            other_matches = any(s.get("type") == concept_type for s in subtype_of[1:])
            if other_matches:
                issues.append(
                    (
                        "WARNING",
                        f"First subtype_of entry type '{first_type}' doesn't match concept type '{concept_type}' (another entry does match)",
                    )
                )
            else:
                issues.append(
                    (
                        "ERROR",
                        f"First subtype_of entry type '{first_type}' doesn't match concept type '{concept_type}' and no other entry matches",
                    )
                )

        # Check 2: Version presence
        if any("version" not in entry for entry in subtype_of):
            issues.append(("WARNING", "subtype_of entry missing 'version' field"))

    # Check 3: Header matching
    # Only validate headers for known abstract types (not Class definitions)
    if concept_type in abstract_entities:
        required_headers = abstract_entities[concept_type].get(
            "required_headers", set()
        )
        headers_by_level = extract_headers(body)
        # Check level 2 headers (##)
        level2_headers = headers_by_level.get(2, set())
        # Normalize headers by removing placeholder variants for matching
        normalized_level2 = {
            PLACEHOLDER_PATTERN.sub("", h).strip() for h in level2_headers
        }
        normalized_level2.update(level2_headers)  # Keep original for exact match too
        normalized_required = {
            PLACEHOLDER_PATTERN.sub("", h).strip() for h in required_headers
        }
        normalized_required.update(
            required_headers
        )  # Keep original for exact match too
        missing = normalized_required - normalized_level2
        if missing:
            for h in sorted(missing):
                issues.append(
                    (
                        "ERROR",
                        f"Missing required header '## {h}' (required by {concept_type})",
                    )
                )

    return issues


def validate_bundle(
    bundle_path: Path,
    abstracts_repo: Optional[Path] = None,
    strict: bool = False,
) -> Tuple[int, List[Tuple[str, str, str]]]:
    """
    Validate all concepts in a bundle.
    Returns (exit_code, list of (file, level, message))
    """
    # Load abstract entities from bundle and okf-abstracts repo
    abstract_entities = load_abstract_entities(bundle_path, abstracts_repo)

    all_issues = []
    checked = 0

    ignored = _ignored_set(bundle_path)

    # Find all concept files: bundle root, concepts/, skills/, references/,
    # templates/, agents/, entities/ (the lattice itself), and program modules/lessons.
    for pattern in [
        "*.md",
        "**/concepts/*.md",
        "**/skills/**/SKILL.md",
        "references/*.md",
        "templates/*.md",
        "agents/*.md",
        "entities/*/*.md",
        "module-*/lessons/*.md",
        "module-*/*.md",
    ]:
        for filepath in bundle_path.glob(pattern):
            if any(
                part in ("node_modules", ".git", ".venv", "__pycache__", ".openclaw")
                for part in filepath.parts
            ):
                continue
            if _is_local_only(filepath, bundle_path, ignored):
                continue
            if filepath.name in RESERVED_FILES:
                continue
            # okf-spec.md is the external Spec anchor, not a lattice class
            if filepath.name == "okf-spec.md":
                continue
            issues = validate_concept(
                filepath,
                abstract_entities=abstract_entities,
            )
            checked += 1
            for level, msg in issues:
                all_issues.append((str(filepath.relative_to(bundle_path)), level, msg))

    # Print results
    errors = [i for i in all_issues if i[1] == "ERROR"]
    warnings = [i for i in all_issues if i[1] == "WARNING"]

    for filepath, level, msg in all_issues:
        print(f"{filepath}: {level}: {msg}")

    print(
        f"\nChecked {checked} files. Total: {len(errors)} errors, {len(warnings)} warnings"
    )

    if strict and (errors or warnings):
        return 1, all_issues
    if errors:
        return 1, all_issues
    return 0, all_issues


def main():
    parser = argparse.ArgumentParser(description="Validate OKF v0.2 subtype_of linkage")
    parser.add_argument("bundle_path", help="Path to OKF bundle root")
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )
    parser.add_argument(
        "--abstracts-repo", help="Path to okf-abstracts repo for base ontology"
    )
    args = parser.parse_args()

    bundle_path = Path(args.bundle_path).resolve()
    if not bundle_path.exists():
        print(f"Error: Bundle path does not exist: {bundle_path}")
        return 2

    abstracts_repo = (
        Path(args.abstracts_repo).resolve() if args.abstracts_repo else None
    )
    if abstracts_repo and not abstracts_repo.exists():
        print(f"Error: Abstracts repo not found: {abstracts_repo}")
        return 2

    exit_code, _ = validate_bundle(
        bundle_path,
        abstracts_repo=abstracts_repo,
        strict=args.strict,
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
