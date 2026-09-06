---
type: Class
title: Validator
description: A skill that validates OKF v0.2 knowledge bundles against the abstract class ontology. Checks subtype_of[] linkage, header matching against abstract class contracts, version pinning, and abstract version change detection.
subtype_of:
- { type: Skill, resource: /entities/domain/skill.md, version: v0.1.0 }
status: stable
stale_after: 2027-08-29
generated: { by: human:yoseph-zuskin, at: '2026-08-29T15:30:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-29T15:35:00Z' }
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- validator
- compliance
- subtype-validation
sources:
- id: okf-validate-subtype-skill
  title: okf-validate-subtype skill
  resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/skills/okf-validate-subtype/SKILL.md
  author: human:yoseph-zuskin
---

# Validator

A **Validator** is a Skill that validates OKF v0.2 knowledge bundles against the okf-abstracts class ontology. It ensures subtype_of[] linkage coherence, header matching against abstract class contracts, version pinning compliance, and abstract version change detection.

## Contract

### Preconditions

- Bundle path exists and contains valid OKF v0.2 bundle
- okf-skills validation has passed (or --strict implies it)
- okf-abstracts repo accessible for abstract entity definitions

### Postconditions

- All subtype_of[] linkage errors reported
- All header matching violations reported
- Version warnings reported
- Abstract version changes detected and reported

### Invariants

- Never modifies bundle files
- Only reads files, never writes
- Deterministic validation results

## Validation Checks

### 1. First Entry Type Match

First `subtype_of[]` entry's `type` must match the concept's `type` field.

### 2. Header Matching

Concept must include all distinct headers (at same level) from the union of its abstract subtypes' required headers.

### 3. Version Warnings

Missing `subtype_of[].version` raises warning.

### 4. Abstract Version Change Detection

Warns if abstract entity changed since concept's last verification.

## Required Headers (from Skill Contract)

- `## Workflow`

- `## Output`

- `## Handoff`

- `## Contract`

- `## Verification`

## Dependencies

**REQUIRES okf-skills** (<https://github.com/scaccogatto/okf-skills>) for:

- OKF v0.2 spec compliance validation
- Frontmatter parsing and schema validation
- Basic concept structure validation

Run `/okf:validate <bundle> --strict` first, then `/okf-validate-subtype <bundle>`.

## Implemented by

- The `okf-validate-subtype` skill (`skills/okf-validate-subtype/SKILL.md`) references this class via `implements`[^okf-validate-subtype-skill].

[^okf-validate-subtype-skill]: [okf-validate-subtype skill](https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/skills/okf-validate-subtype/SKILL.md)
