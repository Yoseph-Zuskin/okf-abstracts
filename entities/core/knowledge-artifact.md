---
type: Class
title: Knowledge Artifact
description: An artifact whose purpose is carrying knowledge. Base of all documentation and instructional genres.
tags:
  - core
  - knowledge
  - artifact
subtype_of:
- { type: Artifact, resource: /entities/core/artifact.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
status: stable
stale_after: 2027-08-19
---
# Knowledge Artifact

An artifact whose purpose is carrying knowledge. Base of all documentation and
instructional genres.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this
  class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

### Required Headers

- Definition
- Sources

Instances of `Knowledge Artifact` MUST:

- state the knowledge claim and its intended audience.

## Implemented by

- Concrete instances in the workspace bundles reference this class via
  `subtype_of`.
