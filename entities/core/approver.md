---
type: Class
title: Approver
description: A role holding formal authority to approve or reject decisions, documents, expenditures, or changes within a defined scope of authority.
subtype_of:
- { type: Role, resource: /entities/core/role.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
tags:
- approval
- authority
- governance
- workflow
sources:
- id: approval-patterns
  title: Approval Workflow Patterns
  resource: https://martinfowler.com/articles/approval-patterns.html
  author: human:martin-fowler
status: stable
stale_after: 2027-08-29
---
# Approver

A role holding formal authority to approve or reject decisions, documents, expenditures, or changes within a defined scope of authority.

## Contract

Instances of `Approver` MUST:

- Define the scope of approval authority (budget limits, decision types, organizational scope)
- Specify delegation rules and escalation paths
- Define approval criteria and required documentation
- Establish audit-trail requirements (what is recorded, by whom, for how long)

## Extensions

- **DelegatedApprover** — Approver with delegated authority from a primary approver

## Sources

This class profile draws on Approval Workflow Patterns[^approval-patterns].

[^approval-patterns]: [Approval Workflow Patterns](https://martinfowler.com/articles/approval-patterns.html) (martin-fowler)

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
