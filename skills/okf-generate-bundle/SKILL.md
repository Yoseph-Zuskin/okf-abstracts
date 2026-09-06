---
name: okf-generate-bundle
displayName: OKF Generate Bundle
type: Skill
description: Generates new OKF v0.2 knowledge bundles with proper abstract lineage to okf-abstracts. Creates bundle structure, index.md, log.md, and scaffolds concepts with proper subtype_of[] linkage to okf-abstracts entities.
title: OKF Generate Bundle
tags:
- okf
- generator
- scaffolding
generated: { by: human:yoseph-zuskin, at: '2026-08-29T15:30:00Z' }
user-invocable: true
argument-hint: "[--title <title>] [--domain <domain>] <output-dir>"
allowed-tools: Read Write Edit Glob Grep Bash
status: draft
stale_after: 2027-09-05
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
implements:
  - { type: Generator, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/generator.md, version: v0.1.0 }
---

# OKF Generate Bundle Skill

Creates new OKF v0.2 knowledge bundles with proper abstract lineage back to okf-abstracts. This skill scaffolds the complete bundle structure including index.md, log.md, and concept templates with correct `subtype_of[]` linkage to okf-abstracts entities.

## Usage

```text
/okf-generate-bundle <output-dir> [--title "My Bundle"] [--domain "my-domain"]
```

Options `--abstracts-url`, `--version`, and `--abstracts-version` override the
default abstracts location and version pins. `--harnesses` selects plugin
configs to emit.

## What it creates

A bare plugin: one starter skill, one starter concept, one starter template,
plus index.md, log.md, VERSION, and the selected harness configs. Grow it by
copying the starter files.

## Abstract Lineage

Every generated concept includes proper `subtype_of[]` linkage:

```yaml
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
```

- First entry matches the concept's `type` (required for validation)
- All entries point to okf-abstracts entities with pinned versions
- Includes `generated` and empty `verified` arrays for compliance tracking

## Dependencies

**REQUIRES okf-skills** (<https://github.com/scaccogatto/okf-skills>) for OKF v0.2 compliance validation. Run okf-skills validation after generation.

## Template Concepts

Generates one starter concept (`getting-started.md`: bundle orientation) with
proper frontmatter. Copy it as the seed for domain concepts.

Each includes proper frontmatter with `subtype_of[]`, `generated`, `verified`, `sources`, `tags`, `status`, `stale_after`.

## How Sections Drive Generation

- **`subtype_of`** is the machine relatedness the generator wires: every generated file links its abstract parent, and generation refuses parents that are git-ignored upstream.
- **`# Contract` sections are read, not written, by generation**: the generator scaffolds static templates and does not inject per-parent required headers (a future enhancement). Run this skill's output through validation to check contract compliance.
- **`Implemented by` / `Related` sections** are never generated or checked. Add them by hand where navigation needs them; explicit body links beat shared tags for the knowledge graph.

## Workflow

1. Accept output directory and options as arguments
2. Create bundle directory structure (index.md, log.md, VERSION, directories)
3. Generate concept templates with proper subtype_of linkage
4. Write harness-specific plugin configs
5. Write VERSION file
6. Run okf-skills validation on generated bundle

## Output

- Complete OKF v0.2 bundle directory: index, log, VERSION, concepts, skills, harness configs.

## Handoff

Produces: Complete OKF v0.2 bundle directory structure
Routes to: [okf-validate-subtype](../okf-validate-subtype/SKILL.md) for linkage validation

## Contract

### Preconditions

- Output directory does not exist or is empty
- okf-abstracts repo accessible for abstract entity definitions

### Postconditions

- Bundle directory created with valid OKF v0.2 structure
- All concepts have proper subtype_of linkage
- okf-skills validation passes on generated bundle

### Invariants

- Never overwrites existing files without --force
- Generated concepts always have proper subtype_of linkage
- Generated bundle passes okf-skills validation

## Verification

- Run: `/okf-generate-bundle ./test-bundle --title "Test" --domain "test"`
- Expected: Bundle created with valid OKF v0.2 structure
- Expected: `python scripts/validate_subtype.py ./test-bundle --strict` passes
