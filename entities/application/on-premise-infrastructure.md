---
type: Class
title: On-Premise Infrastructure
description: Computing infrastructure physically located within an organization's own facilities, managed and operated by the organization's own staff.
subtypes_of:
- { type: Software System, resource: /entities/domain/software-system.md }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
tags:
- on-premise-infrastructure
- on-premises
- private-cloud
- data-center
- software-system
status: stable
stale_after: 2027-08-19
---

# On-Premise Infrastructure

Computing infrastructure physically located within an organization's own facilities, managed and operated by the organization's own staff.

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

- On-Premises Infrastructure
- Private Cloud Infrastructure
- Data Center Infrastructure
