---
name: okf-adversarial-review
displayName: OKF Adversarial Review
type: Skill
title: Adversarial Review Protocol for OKF Bundles
description: Reviews an OKF v0.2 bundle for logical quality a validator cannot judge (true is-a links, layer discipline, contract quality, IP posture). Read-only; reports BLOCKING vs ADVISORY with a release verdict.
user-invocable: true
argument-hint: "<bundle-path> [--focus ontology|bundle|ip|release]"
allowed-tools: Read Glob Grep
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
implements:
  - { type: Validator, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/validator.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-09-05T18:11:16Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- review
- adversarial
- quality
- release-readiness
- contributions
role_assignments:
- data-owners
- platform-admins-devops
- governance-reps-legal-infosec
- solution-architects
status: draft
stale_after: 2027-09-05
---

# Adversarial Review Protocol for OKF Bundles

A review procedure for an intelligent executor (human or LLM). It judges what
mechanical checks cannot: whether the ontology and bundle are logically right,
not merely well-formed. **Read-only: never write, edit, or commit during a
review.** Every claim must cite file bytes (`path:line`) verified first-hand.

## 0. Mechanical Gates First

Run before judging anything; a red gate is itself a BLOCKING finding:

- `python scripts/validate_subtype.py <bundle> --abstracts-repo <abstracts> --strict`
- `python scripts/check_consistency.py <bundle>`
- `python scripts/check_links.py <bundle>`
- `python scripts/check_newlines.py <bundle>`

Validator-green proves form, never meaning. Say so in the report when relevant.

## 1. Is-a Integrity

For EVERY `subtype_of` entry, apply the OWL test: every instance of the child
must be an instance of the parent. Flag related-to masquerading as is-a
(departments as Concepts, agents as Roles, tasks as siblings of paradigms).
Check entry order (first entry is the most-specific parent) and that no entity
subtypes itself.

## 2. Layer Discipline

No child in a lower-numbered layer than its parent. Flag layer-skips (L3 to L0)
and same-layer subtyping as advisory unless the relationship demands it.
Same-layer children of Skill (Generator, Validator) are acceptable; flattened
taxonomies (paradigms beside tasks) are not.

## 3. Contract Quality

`# Contract` sections must state testable instance requirements, not
boilerplate. Flag tripled/duplicated bodies, missing Contracts on Class files,
and required-headers lists no instance could fail.

## 4. Drift and Counts

Reconcile indexes with disk (entries, counts), prose numbers with reality
("96 concepts" vs actual), manifests with bundle contents (skills, references,
templates arrays), and harness copies with canonical files (TODOs, stale
frontmatter, broken relative-link depth).

## 5. IP and Provenance (public bundles)

Distinguish synthesis from reproduction: verbatim or paywalled-only sourcing,
framework detail exceeding summary, license scope (MIT for code and synthesis;
source materials under their own terms). Flag `status: stable` on unreviewed
or unattributed content; new synthesis ships as `draft`.

## 6. Harness Coherence

Copies must be generated, never forked. Verify regen scripts exist and are
idempotent; symlinks are rejected (Windows privilege, git fragility,
link-depth mismatch).

## Workflow

1. **Run the gates** — Record results; stop judging and report if red. Linkage semantics come from [okf-validate-subtype](../okf-validate-subtype/SKILL.md).
2. **Read the lattice** — Every entity file's parents (dimension 1-2).
3. **Read the bundle** — Concepts, skills executability, references, templates.
4. **Reconcile metadata** — Indexes, manifests, counts, copies (dimension 4, 6).
5. **Judge IP posture** — Sources, licenses, stability claims (dimension 5).
6. **Report** — Flags, counts, verdict, top 5. No fixes applied during review.

## Output

- File-by-file flags as `path: issue` one-liners, grouped BLOCKING vs ADVISORY.
- Counts per dimension.
- Verdict: READY, READY-WITH-FIXES, or NOT-READY, with the top 5 fixes in order.

## Handoff

Produces: adversarial review report with verdict.
Routes to: the bundle owner for fixes; re-run after fixes before release.

## Contract

### Preconditions

- Bundle path supplied; mechanical gates run first with results recorded.

### Postconditions

- Report with file-by-file flags, per-dimension counts, verdict, top 5 fixes.

### Invariants

- Read-only throughout; every claim cites verified file bytes; validator-green never presented as logically right.

## Verification

- Confirm each BLOCKING flag cites a `path:line` that was actually read.
- Confirm the verdict follows from the flags, not from gate output alone.
- Confirm no files were modified during the review.
