---
type: Class
title: Approval
description: A formal authorization granted by an approver to proceed with an action, expenditure, decision, or change. Approvals are recorded with the approver, timestamp, scope, and conditions.
subtype_of:
- { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
tags:
- approval
- authorization
- workflow
- governance
sources:
- id: approval-patterns
  title: Approval Workflow Patterns
  resource: https://martinfowler.com/articles/approval-patterns.html
  author: human:martin-fowler
status: stable
stale_after: 2027-08-29
---
# Approval

A formal authorization granted by an approver to proceed with an action, expenditure, decision, or change. Approvals are recorded with the approver, timestamp, scope, and conditions.

## Contract

Instances of `Approval` MUST:

- Identify the approver (individual or role)
- Specify the scope of approval (what is being approved)
- Record timestamp and authentication of approver
- Specify any conditions or limitations
- Reference the artifact being approved (document, expenditure, change, decision)

## Types of Approval

- **ExplicitApproval** — Explicit sign-off by named approver
- **ImplicitApproval** — Approval by lack of objection within timeframe
- **ConditionalApproval** — Approval subject to conditions
- **DelegatedApproval** — Approval by delegated authority
- **EscalatedApproval** — Approval requiring escalation to higher authority

## Sources

This class profile draws on Approval Workflow Patterns[^approval-patterns].

[^approval-patterns]: [Approval Workflow Patterns](https://martinfowler.com/articles/approval-patterns.html) (martin-fowler)

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
