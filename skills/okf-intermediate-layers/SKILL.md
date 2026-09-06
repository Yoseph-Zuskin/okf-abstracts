---
name: okf-intermediate-layers
displayName: OKF Intermediate Layers
type: Skill
description: Supports custom organization-specific abstract layers between okf-abstracts and domain concepts. Creates and manages intermediate abstract entities (e.g., org-specific policies, industry-specific patterns) that sit between okf-abstracts foundational classes and domain concepts.
title: OKF Intermediate Layers
tags:
- okf
- layers
- ontology
generated: { by: human:yoseph-zuskin, at: '2026-08-29T15:30:00Z' }
user-invocable: true
argument-hint: "[--create <layer-name>] [--parent <parent-abstract>] [--concepts <list>] [--bundle <path>]"
allowed-tools: Read Write Edit Glob Grep Bash
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
---

# OKF Intermediate Layers Skill

Enables custom organization-specific abstract layers between okf-abstracts foundational classes and your domain concepts. This allows organizations to define their own abstract policies, industry patterns, or domain-specific abstract entities that form a coherent lineage.

## The Layer Model

OKF v0.2 defines four standard layers (see `entities/*/index.md` for truth):

1. **Foundational** (L0) — `Thing`, `Concept`, `Agent`, `Process`, `Entity`, etc.
2. **Core** (L1) — `Artifact`, `Person`, `Organization`, `Role`, `Workflow`, etc.
3. **Domain** (L2) — `Skill`, `Template`, `Reference`, `Persona`, `Product`, etc.
4. **Application** (L3) — `Online Program`, `SaaS Product`, `Startup`, `Treaty`, etc.

This skill lets you insert **custom intermediate layers** between any standard layers.

## Usage

```text
/okf-intermediate-layers <bundle-path> [--create <layer-name>] [--parent <parent-abstract>] [--concepts <concept1,concept2>] [--list]
```

### Create a new intermediate layer

```bash
/okf-intermediate-layers ./my-bundle --create "acme-corp" --parent "Skill" --concepts "MLModelGovernance,ProductDiscovery,ReleaseProcess"
```

This creates:

1. New abstract entity `AcmeCorpSkill` in okf-abstracts style (L1.5)
2. Links it as subtype of `Skill` (parent)
3. Makes listed concepts subtype of `AcmeCorpSkill`
4. Adds to bundle's layer index

### List existing layers

```bash
/okf-intermediate-layers ./my-bundle --list
```

Output:

```text
Layer hierarchy:
L0 Foundational: thing → Concept, Agent, Template
L1 Core: Skill, Reference, Service
L1.5 AcmeCorp: AcmeCorpSkill → MLModelGovernance, ProductDiscovery
L2 Domain: MLModel, API
L3 Application: MyMLModel, PaymentAPI
```

## Abstract Entity Format

Each intermediate layer gets an abstract entity file:

```markdown
---
type: Class
title: AcmeCorp Skill
description: Organization-specific skill pattern extending base Skill with Acme Corp governance requirements.
title: OKF Intermediate Layers
tags:
- okf
- layers
- ontology
generated: { by: human:yoseph-zuskin }
subtype_of:
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
status: stable
stale_after: 2027-08-29
generated: { by: "human:alice", at: "2026-08-29T10:00:00Z" }
verified: []
---

# Contract

Instances of `AcmeCorpSkill` MUST:

1. Include all base Skill requirements (## Workflow, ## Handoff)
2. Add Acme Corp governance section (## Governance)
3. Reference Acme Corp policy registry (## PolicyRefs)
4. Specify compliance officer (## ComplianceOfficer)

## Required Headers (Union)

- ## Workflow (from Skill)
- ## Handoff (from Skill)
- ## Governance (AcmeCorp-specific)
- ## PolicyRefs (AcmeCorp-specific)
- ## ComplianceOfficer (AcmeCorp-specific)

## Extensions

Organizations may extend with additional constraints in ## Extensions.
```

## Concept Linkage

Domain concepts then link to the intermediate layer:

```yaml
subtype_of:
  - { type: AcmeCorpSkill, resource: ./entities/acme-corp/skill.md, version: v0.1.0 }
  - { type: Skill, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/domain/skill.md, version: v0.1.0 }
  - { type: Concept, resource: https://www.github.com/Yoseph-Zuskin/okf-abstracts/blob/v0.1.0/entities/foundational/concept.md, version: v0.1.0 }
```

- First entry matches concept's `type` (AcmeCorpSkill)
- Chain traces back to okf-abstracts

## Validation

The [okf-validate-subtype](../okf-validate-subtype/SKILL.md) skill validates intermediate layers:

- First `subtype_of[]` entry matches concept `type`
- Headers include union of all subtype abstracts' required headers
- Version warnings for missing `subtype_of[].version`

## Dependencies

**REQUIRES okf-skills** (<https://github.com/scaccogatto/okf-skills>) for base compliance.
Run okf-skills validation first, then intermediate layer validation.

## Use Cases

- **Org policies**: Security, compliance, data handling patterns
- **Industry patterns**: Healthcare HIPAA skills, FinTech audit skills
- **Team conventions**: Frontend patterns, API design patterns
- **Product lines**: Platform skills vs. Feature skills

## Workflow

1. Accept bundle path and options as arguments
2. If --create: generate new intermediate layer abstract entity
3. If --list: display current layer hierarchy
4. Write intermediate layer abstract entity file
5. Update concept subtype_of to include new layer
6. Update bundle layer index

## Output

- New intermediate layer abstract entity file with updated concept linkages.

## Handoff

Produces: Intermediate layer abstract entity file
Routes to: okf-validate-subtype for linkage validation

## Contract

### Preconditions

- Bundle path exists and contains valid OKF v0.2 bundle
- Parent abstract entity exists in okf-abstracts

### Postconditions

- Intermediate layer abstract entity created
- Concepts updated with new subtype_of linkage
- Layer hierarchy updated in bundle index

### Invariants

- Never modifies existing abstract entities
- New layer always traces back to okf-abstracts root
- Concepts maintain complete lineage chain

## Verification

- Run: `/okf-intermediate-layers ./my-bundle --create "test" --parent "Skill" --concepts "TestConcept"`
- Expected: New layer entity created
- Expected: `python scripts/validate_subtype.py ./my-bundle --strict` passes
