---
type: Class
title: Decision
description: A formal choice made between alternatives to resolve uncertainty, commit resources, or direct action. Decisions have context, criteria, alternatives, and consequences.
subtype_of:
- { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
tags:
- decision
- decision-making
- choice
- governance
sources:
- id: decision-making
  title: Decision Making (Management)
  resource: https://en.wikipedia.org/wiki/Decision-making
  author: org:wikipedia
- id: adr
  title: Architecture Decision Records
  resource: https://adr.github.io/
  author: org:adr-community
status: stable
stale_after: 2027-08-29
---
# Decision

A formal choice made between alternatives to resolve uncertainty, commit resources, or direct action. Decisions have context, criteria, alternatives, and consequences.

## Contract

Instances of `Decision` MUST:

- Document the decision context and problem statement
- Identify alternatives considered and evaluation criteria
- Record the rationale for the chosen alternative
- Document assumptions, constraints, and risks
- Specify the decision owner and stakeholders
- Define success criteria and review triggers

## Decision Types

- **StrategicDecision** — Long-term, high-impact, irreversible
- **TacticalDecision** — Operational, reversible, shorter timeframe
- **OperationalDecision** — Routine, delegated, procedural
- **ArchitecturalDecision** — Technical structure, technology selection, and constraints

## Sources

This class profile draws on Decision Making (Management)[^decision-making], Architecture Decision Records[^adr].

[^decision-making]: [Decision Making (Management)](https://en.wikipedia.org/wiki/Decision-making) (wikipedia)
[^adr]: [Architecture Decision Records](https://adr.github.io/) (adr-community)

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
