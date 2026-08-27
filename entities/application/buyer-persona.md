---
type: Class
title: Buyer Persona
description: A fictional representation of the decision-maker or purchaser in a
  business-to-business or business-to-consumer context.
subtypes_of:
- { type: Persona, resource: /entities/domain/persona.md }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
tags:
- buyer-persona
- buyer-research
- sales
- decision-maker
- customer-persona
status: stable
stale_after: 2027-08-19
---
# Buyer Persona

A fictional representation of the decision-maker or purchaser in a business-to-business or business-to-consumer context.

## Contract

A concept of this class describes the class itself as a universal — *not* a
concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this
  class, plus a `subtypes_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

## Implemented by

- Concrete instances in the workspace bundles reference this class via
  `subtypes_of`.

## Aliases

- Customer Persona
