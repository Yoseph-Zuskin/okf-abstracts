---
type: Class
title: Decision Maker
description: A persona representing an individual with authority to approve purchases or strategic decisions within an organization.
subtypes_of:
- { type: Persona, resource: /entities/domain/persona.md }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
tags:
- decision-maker
- buyer-persona
- authority
- stakeholder
- executive
status: stable
stale_after: 2027-08-19
---

# Decision Maker

A persona representing an individual with authority to approve purchases or strategic decisions within an organization.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete
instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this class, plus a
  `subtypes_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtypes_of`.

## Aliases

- Stakeholder
- Approver
- Executive Sponsor
