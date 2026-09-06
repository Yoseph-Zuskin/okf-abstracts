#!/usr/bin/env python3
"""
OKF Generate Bundle Skill Implementation

Generates new OKF v0.2 knowledge bundles with proper abstract lineage to okf-abstracts.
Creates bundle structure, index.md, log.md, VERSION, and scaffolds concepts with
proper subtype_of[] linkage to okf-abstracts entities.

Usage: python scripts/generate_bundle.py <output-dir> [--title <title>] [--domain <domain>]
       [--harnesses <list>] [--abstracts-repo <path>] [--abstracts-url <url>]
       [--version <x.y.z>] [--abstracts-version <vX.Y.Z>] [--force]

Dependencies: Python 3.6+, stdlib only (yaml, json, re, pathlib, datetime, argparse)
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from string import Template
from typing import Dict, List, Optional

# =============================================================================
# Template Definitions
# =============================================================================

# Bundle root templates
INDEX_TEMPLATE = Template("""---
okf_version: "0.2"
---
# ${title}

${description}

## Bundle Information

- **Version**: ${version}
- **Created**: ${created_date}
- **OKF Abstracts**: ${okf_abstracts_version}
- **Domain**: ${domain}

## Structure

${structure}

## Navigation

* [Concepts](concepts/)
* [Skills](skills/)
* [Templates](templates/)
* [References](references/)
* [Log](log.md)
""")

LOG_TEMPLATE = Template("""# Change Log

All notable changes to this bundle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [${version}] - ${today}

### Added
- Initial bundle structure
- Core concept definitions
- Skill definitions
- Template definitions
""")

CONCEPT_TEMPLATE = Template("""---
type: ${concept_type}
title: ${title}
description: ${description}
subtype_of:
${subtype_of}
status: draft
stale_after: ${stale_after}
generated: { by: ${generated_by}, at: '${generated_at}' }
verified: []
tags:
${tags}
sources:
${sources}
---

# ${title}

${description}

## Definition

${definition}

## Sources

${source_entries}
""")

SKILL_TEMPLATE = Template("""---
name: ${skill_name}
displayName: ${display_name}
type: Skill
description: ${description}
user-invocable: true
argument-hint: ${argument_hint}
allowed-tools: ${allowed_tools}
subtype_of:
  - { type: Skill, resource: ${abstracts_url}/entities/domain/skill.md, version: ${abstracts_version} }
---

# ${display_name}

${description}

## Workflow

${workflow}

## Output

${output}

## Handoff

Produces: ${output_short}
Routes to: sibling skills as the task requires.

## Contract

### Preconditions
- The task falls within this skill's stated purpose.

### Postconditions
- The output described above is delivered.

### Invariants
- Read-only unless the task explicitly requires writes.

## Verification

- Re-read the output against the Postconditions above.
- Confirm any named bundle paths resolve.
""")

TEMPLATE_TEMPLATE = Template("""---
type: Template
title: ${title}
description: ${description}
subtype_of:
  - { type: Template, resource: ${abstracts_url}/entities/domain/template.md, version: ${abstracts_version} }
status: draft
stale_after: ${stale_after}
generated: { by: ${generated_by}, at: '${generated_at}' }
verified: []
tags:
${tags}
sources:
${sources}
---

# ${title}

${description}

## Structure

${structure}

## Variables

${variables}

## Rendering Rules

${rendering_rules}

## Validation

${validation}
""")

VERSION_TEMPLATE = Template("${version}\n")


# =============================================================================
# Helper Functions
# =============================================================================


def format_subtype_of(subtypes: List[Dict]) -> str:
    lines = []
    for s in subtypes:
        t = s.get("type", "")
        r = s.get("resource", "")
        v = s.get("version", "v0.1.0")
        lines.append(f"  - {{ type: {t}, resource: {r}, version: {v} }}")
    return "\n".join(lines)


def format_tags(tags: List[str]) -> str:
    return "\n".join(f"  - {t}" for t in tags)


def format_sources(sources: List[Dict]) -> str:
    lines = []
    for s in sources:
        lines.append(f"  - id: {s.get('id', '')}")
        lines.append(f"    title: {s.get('title', '')}")
        lines.append(f"    resource: {s.get('resource', '')}")
        lines.append(f"    author: {s.get('author', '')}")
    return "\n".join(lines)


def clean_frontmatter(content: str) -> str:
    """Drop blank lines inside frontmatter so generated files pass validation."""
    end = content.find("\n---", 4)
    if end == -1 or not content.startswith("---\n"):
        return content
    fm_lines = [line for line in content[4:end].split("\n") if line.strip()]
    return "---\n" + "\n".join(fm_lines) + content[end:]


# =============================================================================
# Main Generator Class
# =============================================================================


class BundleGenerator:
    def __init__(
        self,
        output_dir: Path,
        title: str,
        domain: str,
        okf_abstracts_repo: Path,
        harnesses: List[str] = None,
        abstracts_url: str = "https://www.github.com/Yoseph-Zuskin/okf-abstracts",
        version: str = "0.1.0",
        abstracts_version: str = "v0.1.0",
    ):
        self.output_dir = Path(output_dir).resolve()
        self.title = title
        self.domain = domain
        self.okf_abstracts_repo = okf_abstracts_repo.resolve()
        self.version = version
        self.abstracts_url = abstracts_url.rstrip("/")
        self.abstracts_version = abstracts_version
        self.created_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.stale_after = (
            datetime.now(timezone.utc).date() + timedelta(days=365)
        ).isoformat()
        self.generated_by = "okf-generate-bundle"
        self.generated_at = (
            datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )
        self.okf_abstracts_version = "v0.1.0"
        self.harnesses = harnesses or [
            "codex",
            "claude",
            "devin",
            "grok",
            "qoder",
            "openclaw",
            "copilot",
        ]

    def generate(self) -> None:
        """Generate the complete bundle structure."""
        if self.output_dir.exists() and any(self.output_dir.iterdir()):
            raise FileExistsError(f"Output directory {self.output_dir} is not empty")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create directory structure
        for subdir in ["concepts", "skills", "templates", "references", "scripts"]:
            (self.output_dir / subdir).mkdir(parents=True, exist_ok=True)

        # Generate files
        self._write_index()
        self._write_log()
        self._write_version()
        self._write_concepts()
        self._write_skills()
        self._write_templates()
        self._write_harness_configs()

        print(f"Generated bundle at {self.output_dir}")

    def _write_index(self) -> None:
        structure = "- concepts/ — Domain concepts\n- skills/ — Workflow skills\n- templates/ — Document templates\n- references/ — Reference documents\n- scripts/ — Utility scripts"

        content = INDEX_TEMPLATE.substitute(
            title=self.title,
            description=f"OKF v0.2 knowledge bundle for {self.domain}",
            version=self.version,
            created_date=self.created_date,
            okf_abstracts_version=self.okf_abstracts_version,
            domain=self.domain,
            structure=structure,
        )
        (self.output_dir / "index.md").write_text(content, encoding="utf-8")

    def _write_log(self) -> None:
        content = LOG_TEMPLATE.substitute(
            version=self.version,
            today=self.today,
        )
        (self.output_dir / "log.md").write_text(content, encoding="utf-8")

    def _write_version(self) -> None:
        content = VERSION_TEMPLATE.substitute(version=self.version)
        (self.output_dir / "VERSION").write_text(content, encoding="utf-8")

    def _write_concepts(self) -> None:
        """Generate the single starter concept."""
        concept = {
            "title": "Getting Started",
            "type": "Concept",
            "description": "Orientation guide for this knowledge bundle.",
            "tags": ["orientation", "getting-started"],
            "definition": "This concept provides an overview of the bundle structure, key concepts, and how to navigate the knowledge base.",
            "sources": [],
        }
        subtypes = [
            {
                "type": "Concept",
                "resource": f"{self.abstracts_url}/entities/foundational/concept.md",
                "version": self.abstracts_version,
            },
        ]

        content = CONCEPT_TEMPLATE.substitute(
            concept_type=concept["type"],
            title=concept["title"],
            description=concept["description"],
            subtype_of=format_subtype_of(subtypes),
            stale_after=self.stale_after,
            generated_by="okf-generate-bundle",
            generated_at=self.generated_at,
            tags=format_tags(concept.get("tags", [])),
            sources=format_sources(concept.get("sources", [])),
            definition=concept.get("definition", ""),
            source_entries="",
        )

        safe_title = re.sub(r"[^a-zA-Z0-9-]", "-", concept["title"].lower())
        (self.output_dir / "concepts" / f"{safe_title}.md").write_text(
            clean_frontmatter(content), encoding="utf-8"
        )

    def _write_skills(self) -> None:
        """Generate the single starter skill."""
        skill = {
            "name": "starter",
            "displayName": f"{self.title} Starter",
            "description": (
                f"Orients over the {self.domain} bundle - reads the index, "
                "loads concepts, and answers questions from bundle content."
            ),
            "argument_hint": "[question]",
            "allowed_tools": "Read Glob Grep",
            "workflow": (
                "1. Read index.md for bundle structure\n"
                "2. Load the concepts relevant to the question\n"
                "3. Answer from bundle content, citing sources"
            ),
            "output": "An answer grounded in bundle concepts with source citations.",
            "output_short": "a grounded answer with citations",
        }

        content = SKILL_TEMPLATE.substitute(
            skill_name=skill["name"],
            display_name=skill["displayName"],
            description=skill["description"],
            argument_hint=skill["argument_hint"],
            allowed_tools=skill["allowed_tools"],
            workflow=skill["workflow"],
            output=skill["output"],
            output_short=skill["output_short"],
            abstracts_url=self.abstracts_url,
            abstracts_version=self.abstracts_version,
        )
        skill_dir = self.output_dir / "skills" / skill["name"]
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

    def _write_templates(self) -> None:
        """Generate the single starter template: a template for authoring
        new concepts in this bundle."""
        tmpl = {
            "title": "Concept Template",
            "type": "Template",
            "description": "Fillable template for authoring a new concept in this bundle.",
            "tags": ["template", "concept", "authoring"],
            "structure": "## Definition\n## Sources",
            "variables": "TITLE, TYPE, DESCRIPTION",
            "rendering_rules": "Fill every section; cite every source.",
            "validation": "Frontmatter parses; subtype_of resolves; sources cited",
            "definition": "A blank concept scaffold following this bundle's conventions.",
        }

        subtypes = [
            {
                "type": "Template",
                "resource": f"{self.abstracts_url}/entities/domain/template.md",
                "version": self.abstracts_version,
            },
        ]

        content = TEMPLATE_TEMPLATE.substitute(
            title=tmpl["title"],
            type=tmpl["type"],
            description=tmpl["description"],
            subtype_of=format_subtype_of(subtypes),
            stale_after=self.stale_after,
            generated_by="okf-generate-bundle",
            generated_at=self.generated_at,
            tags=format_tags(tmpl.get("tags", [])),
            sources=format_sources(tmpl.get("sources", [])),
            structure=tmpl["structure"],
            variables=tmpl["variables"],
            rendering_rules=tmpl["rendering_rules"],
            validation=tmpl["validation"],
            definition=tmpl.get("definition", ""),
            abstracts_url=self.abstracts_url,
            abstracts_version=self.abstracts_version,
        )

        safe_title = re.sub(r"[^a-zA-Z0-9-]", "-", tmpl["title"].lower())
        (self.output_dir / "templates" / f"{safe_title}.md").write_text(
            clean_frontmatter(content), encoding="utf-8"
        )

    def _write_harness_configs(self) -> None:
        """Generate harness-specific plugin configurations for specified harnesses."""

        for harness_name in self.harnesses:
            config = self._get_harness_config(harness_name)
            if not config:
                print(f"Warning: Unknown harness '{harness_name}', skipping")
                continue

            harness_dir_path = self.output_dir / config["dir"]
            harness_dir_path.mkdir(parents=True, exist_ok=True)

            if "config" in config:
                config_path = harness_dir_path / "plugin.json"
                config_path.write_text(
                    json.dumps(config["config"], indent=2), encoding="utf-8"
                )

    def _get_harness_config(self, harness_name: str) -> Optional[Dict]:
        """Get harness configuration by name. Returns None if unknown."""
        common_config = {
            "name": "okf-generated-bundle",
            "version": self.version,
            "description": f"Generated OKF bundle for {self.domain}",
            "author": "okf-generate-bundle",
            "license": "MIT",
            "skills": "./skills/",
        }

        configs = {
            "codex": {
                "dir": ".codex-plugin",
                "config": {
                    **common_config,
                    "interface": {
                        "displayName": self.title,
                        "shortDescription": f"OKF bundle for {self.domain}",
                        "longDescription": f"Generated OKF v0.2 knowledge bundle for {self.domain}",
                        "developerName": "okf-generate-bundle",
                        "category": "Productivity",
                        "capabilities": ["Interactive", "Read", "Write"],
                        "websiteURL": "https://github.com/Yoseph-Zuskin/okf-abstracts",
                        "defaultPrompt": [f"Help me with {self.domain}"],
                        "brandColor": "#6E56CF",
                    },
                },
            },
            "claude": {
                "dir": ".claude-plugin",
                "config": {
                    **common_config,
                    "hooks": "./hooks/claude-codex-hooks.json",
                },
            },
            "devin": {
                "dir": ".devin-plugin",
                "config": common_config,
            },
            "grok": {
                "dir": ".grok-plugin",
                "config": common_config,
            },
            "qoder": {
                "dir": ".qoder-plugin",
                "config": common_config,
            },
            "openclaw": {
                "dir": ".openclaw",
                "config": common_config,
            },
            "copilot": {
                "dir": ".github",
                "config": common_config,
            },
        }

        if harness_name not in configs:
            return None

        return configs[harness_name]


# =============================================================================
# CLI Entry Point
# =============================================================================


def main():
    parser = argparse.ArgumentParser(description="Generate OKF v0.2 knowledge bundle")
    parser.add_argument("output_dir", help="Output directory for the new bundle")
    parser.add_argument("--title", default="My Bundle", help="Bundle title")
    parser.add_argument("--domain", default="general", help="Domain name")
    parser.add_argument(
        "--harnesses",
        default="codex,claude,devin,grok,qoder,openclaw,copilot",
        help="Comma-separated list of harnesses to generate (codex,claude,devin,grok,qoder,openclaw,copilot)",
    )
    parser.add_argument(
        "--abstracts-repo",
        default=None,
        help="Path to okf-abstracts repo (default: ../okf-abstracts)",
    )
    parser.add_argument(
        "--abstracts-url",
        default="https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0",
        help="Base URL emitted in subtype_of resources (pinned form)",
    )
    parser.add_argument(
        "--version", default="0.1.0", help="Version stamped on the new bundle"
    )
    parser.add_argument(
        "--abstracts-version",
        default="v0.1.0",
        help="okf-abstracts pin emitted in subtype_of versions",
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing directory"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        print(
            f"Error: Output directory {output_dir} is not empty. Use --force to overwrite."
        )
        return 1

    # Find okf-abstracts repo
    if args.abstracts_repo:
        abstracts_repo = Path(args.abstracts_repo).resolve()
    else:
        # Try to find it relative to this script
        script_dir = Path(__file__).parent.parent
        abstracts_repo = (script_dir / ".." / "okf-abstracts").resolve()
        if not abstracts_repo.exists():
            abstracts_repo = Path.cwd().parent / "okf-abstracts"
            if not abstracts_repo.exists():
                print(
                    "Error: Could not find okf-abstracts repo. Use --abstracts-repo to specify path."
                )
                return 1

    if not abstracts_repo.exists():
        print(f"Error: okf-abstracts repo not found at {abstracts_repo}")
        return 1

    generator = BundleGenerator(
        output_dir=output_dir,
        title=args.title,
        domain=args.domain,
        okf_abstracts_repo=abstracts_repo,
        harnesses=args.harnesses.split(","),
        abstracts_url=args.abstracts_url,
        version=args.version,
        abstracts_version=args.abstracts_version,
    )

    try:
        generator.generate()
        print(f"\nBundle generated successfully at {output_dir}")
        print("Next steps:")
        print(f"  cd {output_dir}")
        print(f"  python {Path(__file__).parent / 'validate_subtype.py'} . --strict")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
