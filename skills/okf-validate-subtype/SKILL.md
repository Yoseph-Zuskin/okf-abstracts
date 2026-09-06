---
name: okf-validate-subtype
displayName: OKF Validate Subtype
type: Skill
description: Validates subtype_of[] linkage in OKF v0.2 bundles against okf-abstracts classes. Checks first entry matches concept type, header matching against abstract class required headers, version warnings, and abstract version change detection.
title: OKF Validate Subtype
tags:
- okf
- validation
- subtype
generated: { by: human:yoseph-zuskin, at: '2026-08-29T15:30:00Z' }
user-invocable: true
argument-hint: "[--strict] [--abstracts-repo <path>] <bundle-path>"
allowed-tools: Read Write Edit Glob Grep Bash
status: draft
stale_after: 2027-09-05
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
implements:
  - { type: Validator, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/validator.md, version: v0.1.0 }
---

# OKF Validate Subtype Skill

Validates `subtype_of[]` linkage in OKF v0.2 knowledge bundles against okf-abstracts class definitions. This skill runs **after** okf-skills validation — run okf-skills first for full OKF v0.2 spec compliance, then use this for subtype coherence against okf-abstracts classes.

## What it checks

1. **First entry matches concept `type`** — The first `subtype_of[]` entry's `type` must match the concept's own `type` field. If not, but another entry does, raises a warning.

2. **Header matching** — Concept must include all headers (at same level) as the union of its abstract subtypes' required headers. Missing headers = error.

3. **Version warnings** — Missing `subtype_of[].version` raises warning (not error).

4. **Abstract version change detection** — If `generated.at` or latest `verified[].by` timestamp is older than the abstract's latest change, warn to re-verify compliance.

5. **Key flexibility** — The canonical linkage key is `subtype_of`. Aliases `subtypes_of`, `subclass_of`, and `subconcept_of` are accepted: a non-canonical key raises a warning, and a plural `*s_of` key raises a second warning (plural reads as children, not parents).

## Usage

```text
/okf-validate-subtype <bundle-path> [--strict] [--warn-on-missing-version] [--check-abstract-versions] [--abstracts-repo <path>]
```

- `--strict` — Treat warnings as errors
- `--warn-on-missing-version` — Explicitly warn on missing subtype versions (default: on)
- `--check-abstract-versions` — Check if abstract definitions have changed since concept verification (requires okf-abstracts repo)
- `--abstracts-repo <path>` — Path to local okf-abstracts repo for base ontology

## Validation Logic

### 1. First Entry Type Match

```yaml
# Concept
type: Skill
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }  # ✓ First entry matches
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
```

### 2. Header Matching

Each abstract class defines required headers in its `# Contract` section. The concept must have all distinct headers (at same level) from the union of all subtypes.

### 3. Version Warnings

```yaml
subtype_of:
  - { type: Skill, resource: ..., version: v0.1.0 }  # ✓ Has version
  - { type: Concept, resource: ... }                 # ⚠ Warning: missing version
```

### 4. Abstract Version Change Detection

Compares concept's `generated.at` / latest `verified[].at` against abstract's `stale_after` or git history. If abstract changed after concept verification, warn. See [okf-abstract-lineage](../okf-abstract-lineage/SKILL.md) for proactive change detection across a bundle.

> ⚠ Abstract `Skill` (v0.1.0) was updated on 2026-08-25. Your concept was last verified 2026-08-15. Consider re-verifying compliance and bumping `subtype_of[].version` to v0.1.1.

## Skill→Class Mapping

The `implements` field in skill frontmatter declares which abstract class this skill implements:

```yaml
implements:
  - { type: Validator, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/validator.md, version: v0.1.0 }
```

This enables:

- Automatic validation that skill implements required headers from the abstract class
- Tooling to discover all skills implementing a given abstract class
- Cross-repo skill discovery

## How Sections Drive This Skill

- **`# Contract` (+ Required Headers)** on an abstract class is the machine-readable part: checks 2 and 3b enforce its headers and tags on every instance. Everything else in the section body is guidance for authors.
- **`subtype_of`** is the machine relatedness between instance and class; it is what checks 1-2 traverse.
- **`Implemented by` / `Related` sections** are never machine-checked. They exist for human and agent navigation (which instances exist, what to read next). Keep them truthful by hand; no script verifies them.

## Dependencies

**REQUIRES okf-skills** (<https://github.com/scaccogatto/okf-skills>) for:

- OKF v0.2 spec compliance validation
- Frontmatter parsing and schema validation
- Basic concept structure validation

Run `/okf:validate <bundle> --strict` first, then `/okf-validate-subtype <bundle>`.

## Workflow

1. **Parse frontmatter** — Load each concept's YAML; reject empty lines and invalid syntax.
2. **Check linkage** — First `subtype_of` entry matches `type`; versions pinned; canonical key preferred.
3. **Match headers and tags** — Required headers and tags from abstract Contracts enforced.
4. **Report** — Per-file diagnostics with ERROR/WARNING levels and exit code.

## Output

- Exit code 0: All validations passed
- Exit code 1: Errors found (missing headers, type mismatches)
- Exit code 2: Warnings only (with `--strict` treats warnings as errors)

## Handoff

Produces: validation report with per-file diagnostics and exit code.
Routes to: [okf-abstract-lineage](../okf-abstract-lineage/SKILL.md) for abstract-change review when version warnings appear.

## Contract

### Preconditions

- Bundle path supplied; abstracts repo available for base ontology.

### Postconditions

- Every concept judged; diagnostics carry file, level, and message.

### Invariants

- Read-only: never modifies bundle files; warnings never fail unless `--strict`.

## Verification

- Run against a fixture with a bad parent, a missing header, and a missing version; confirm ERROR, ERROR, WARNING respectively.
- Confirm `--strict` exits non-zero on warnings alone.
- Confirm a clean bundle exits 0 with no output beyond the total.
