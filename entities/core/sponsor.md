---
type: Class
title: Sponsor
description: A role providing resources, authority, and advocacy for a project, initiative, or product.
subtype_of:
- { type: Role, resource: /entities/core/role.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
tags:
- sponsor
- executive
- governance
- project-management
sources:
- id: pmi-sponsor
  title: Project Sponsor Role (PMBOK)
  resource: https://www.pmi.org/pmbok
  author: org:pmi
status: stable
stale_after: 2027-08-29
---
# Sponsor

A role providing resources, authority, and advocacy for a project, initiative, or product.

## Contract

Instances of `Sponsor` MUST:

- Identify the scope of sponsorship (project, program, portfolio)
- Define the sponsor's authority level and decision rights
- Specify escalation paths and decision-making authority
- Document resource commitment (budget, people, political capital)

## Extensions

- **ExecutiveSponsor** — C-level or senior leadership sponsor with organizational authority
- **ProjectSponsor** — Sponsor accountable for a specific project or initiative

## Sources

This class profile draws on Project Sponsor Role (PMBOK)[^pmi-sponsor].

[^pmi-sponsor]: [Project Sponsor Role (PMBOK)](https://www.pmi.org/pmbok) (pmi)

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
