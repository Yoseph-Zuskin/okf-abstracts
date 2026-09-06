---
type: Class
title: Generator
description: A skill that generates new OKF v0.2 knowledge bundles with proper abstract lineage, structure, and compliance scaffolding.
subtype_of:
- { type: Skill, resource: /entities/domain/skill.md, version: v0.1.0 }
status: stable
stale_after: 2027-08-29
generated: { by: human:yoseph-zuskin, at: '2026-08-29T15:30:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-29T15:35:00Z' }
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- generator
- bundle-creation
- scaffolding
sources:
- id: okf-generate-bundle-skill
  title: okf-generate-bundle skill
  resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/skills/okf-generate-bundle/SKILL.md
  author: human:yoseph-zuskin
---

# Generator

A **Generator** is a Skill that creates new OKF v0.2 knowledge bundles with proper abstract lineage, structure, and compliance scaffolding.

## Contract

### Preconditions

- Output directory does not exist or is empty (unless --force)
- okf-abstracts repo accessible for abstract entity definitions
- okf-skills available for post-generation validation

### Postconditions

- Bundle directory created with valid OKF v0.2 structure
- All concepts have proper subtype_of linkage to okf-abstracts
- Harness plugin configs generated for target harnesses
- okf-skills validation passes on generated bundle

### Invariants

- Never overwrites existing files without --force
- Generated concepts always have proper subtype_of linkage
- Generated bundle passes okf-skills validation

## Required Headers (from Skill Contract)

- `## Workflow`

- `## Handoff`

- `## Contract`

- `## Verification`

## Generator-Specific Sections

### ## Usage

Command-line interface and options documentation.

### ## What it creates

Bundle structure documentation.

### ## Abstract Lineage

How generated concepts link to okf-abstracts entities.

### ## Intermediate Layers

Support for custom organization-specific layers.

## Dependencies

**REQUIRES okf-skills** for post-generation validation.

## Implemented by

- okf-generate-bundle skill[^okf-generate-bundle-skill]

[^okf-generate-bundle-skill]: [okf-generate-bundle skill](https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/skills/okf-generate-bundle/SKILL.md)
