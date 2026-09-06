---
type: Class
title: Decision Maker
description: A role representing an individual with authority to approve purchases or strategic decisions within an organization. Distinct from a persona — this is a functional role, not a fictional representation.
subtype_of:
- { type: Approver, resource: /entities/core/approver.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- decision-maker
- authority
- stakeholder
- executive
- role
status: stable
stale_after: 2027-08-29
---
# Decision Maker

A role representing an individual with authority to approve purchases or strategic decisions within an organization. Distinct from a persona — this is a functional role, not a fictional representation.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.

## Related Terms

- Stakeholder
- Executive Sponsor
