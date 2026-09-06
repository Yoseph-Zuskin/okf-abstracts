---
type: Class
title: Process
description: 'An entity that unfolds over time: an activity, an event, a workflow.'
tags:
  - foundational
  - temporal
subtype_of:
- { type: Entity, resource: /entities/foundational/entity.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
status: stable
stale_after: 2027-08-19
---
# Process

An entity that unfolds over time: an activity, an event, a workflow.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this
  class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

### Required Headers

- Definition
- Sources

Instances of `Process` MUST:

- bound the process in time (start/end or ongoing conditions).

## Implemented by

- Concrete instances in the workspace bundles reference this class via
  `subtype_of`.
