---
type: Class
title: Stakeholder
description: A role relating an interested party to a project, product, or organization — one who can influence or be influenced by decisions and outcomes.
subtype_of:
- { type: Role, resource: /entities/core/role.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
tags:
- stakeholder
- governance
- role
- organization
sources:
- id: pmbook-stakeholder
  title: Stakeholder Management (PMBOK)
  resource: https://www.pmi.org/pmbok
  author: org:pmi
status: stable
stale_after: 2027-08-29
---
# Stakeholder

A role relating an interested party to a project, product, or organization — one who can influence or be influenced by decisions and outcomes.

## Stakeholder Categories

- **Internal** — employees, management, board members
- **External** — customers, suppliers, regulators, communities
- **Primary** — directly affected by decisions
- **Secondary** — indirectly affected or influencing

## Contract

Instances of `Stakeholder` MUST:

- Identify the stakeholder's relationship to the subject
- Document their interests, influence, and impact
- Define engagement and communication expectations

## Extensions

- **StakeholderMap** — visualization of stakeholder relationships and influence
- **StakeholderRegister** — Catalog of identified stakeholders with interests and influence

## Sources

This class profile draws on Stakeholder Management (PMBOK)[^pmbook-stakeholder].

[^pmbook-stakeholder]: [Stakeholder Management (PMBOK)](https://www.pmi.org/pmbok) (pmi)

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
