---
name: okf-abstract-lineage
displayName: OKF Abstract Lineage
type: Skill
description: Tracks okf-abstracts entity versions and detects changes since concept verification. Compares concept generated.at/verified[].at timestamps against abstract entity stale_after or git history, warning when abstracts have changed and suggesting version bumps.
title: OKF Abstract Lineage
tags:
- okf
- lineage
- versions
generated: { by: human:yoseph-zuskin, at: '2026-08-29T15:30:00Z' }
user-invocable: true
argument-hint: "[--check-all] [--update-versions] [--abstracts-repo <path>] <bundle-path>"
allowed-tools: Read Write Edit Glob Grep Bash
status: draft
stale_after: 2027-09-05
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
implements:
  - { type: Validator, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/validator.md, version: v0.1.0 }
---

# OKF Abstract Lineage Skill

Tracks okf-abstracts entity versions and detects when abstract definitions have changed since a concept was last verified. This enables proactive compliance maintenance.

## Usage

```text
/okf-abstract-lineage <bundle-path> [--check-all] [--update-versions] [--abstracts-repo <path>]
```

- `--check-all` — Check all concepts in bundle (default: only changed)
- `--update-versions` — Auto-bump `subtype_of[].version` when abstract changed (interactive confirmation)
- `--abstracts-repo <path>` — Path to local okf-abstracts repo (default: auto-detect via GitHub URL)

## What it does

### 1. Version Tracking

Each concept has:

```yaml
generated: { by: "agent/xyz", at: "2026-08-15T10:00:00Z" }
verified:
  - { by: "human:alice", at: "2026-08-20T10:00:00Z" }
  - { by: "agent/xyz", at: "2026-08-22T10:00:00Z" }
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
```

### 2. Change Detection

Compares latest verification timestamp (`verified[-1].at` or `generated.at`) against:

- Abstract entity's `stale_after` date
- Abstract entity's git commit history (if local okf-abstracts repo available)
- GitHub API commit timestamps (if remote)

If abstract changed after concept's latest verification:
> ⚠ Abstract `Skill` (v0.1.0) was updated on 2026-08-25. Your concept was last verified 2026-08-20. Consider re-verifying and bumping `subtype_of[].version` to v0.1.1.

### 3. Version Bump Guidance

When abstract changes:

1. Re-verify concept compliance with new abstract definition
2. If compliant, bump `subtype_of[].version` to next patch (v0.1.0 → v0.1.1)
3. Update concept's `generated.at` or add new `verified` entry
4. Append to `log.md`

### 4. No Forced Updates

- **Never auto-bumps** without explicit confirmation
- Concepts can remain at old version if abstract change doesn't affect them
- Warning only; compliance maintained until next verification

## Dependencies

**REQUIRES okf-skills** (<https://github.com/scaccogatto/okf-skills>) for OKF v0.2 compliance baseline.

## Integration

Run after okf-skills validation:

```bash
# 1. Validate OKF compliance
/okf:validate <bundle> --strict

# 2. Check subtype coherence
/okf-validate-subtype <bundle>

# 3. Check abstract lineage
/okf-abstract-lineage <bundle>
```

## Output

- Exit 0: All concepts up-to-date with abstract versions
- Exit 1: Abstract changes detected (warnings, not errors)
- Exit 2: Errors (missing abstracts repo, invalid timestamps)

## Workflow

1. Accept bundle path and options as arguments
2. Load all concept and skill files from bundle
3. For each concept, extract latest verification timestamp
4. For each subtype_of entry, check abstract entity for changes
5. Compare concept verification timestamp against abstract changes
6. Report warnings for any abstract changes since last verification

## Handoff

Produces: Lineage report with warnings for outdated concepts
Routes to: [okf-validate-subtype](../okf-validate-subtype/SKILL.md) for subtype validation (if not already run)

## Contract

### Preconditions

- Bundle path exists and contains valid OKF v0.2 bundle
- okf-abstracts repo accessible (local or remote)

### Postconditions

- All abstract version changes reported as warnings
- Version bump suggestions provided where applicable

### Invariants

- Never modifies bundle files
- Only reads files, never writes
- Never auto-bumps versions without explicit confirmation

## Verification

- Run: `bash scripts/check_abstract_lineage.sh <bundle-path> --check-all`
- Expected: Exit code 0 for up-to-date bundles
- Expected: Exit code 1 for bundles with abstract changes
