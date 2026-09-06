---
type: Class
title: Skill
description: A reusable, self-contained capability that encapsulates a specific workflow, methodology, or expertise domain — composable with other skills to form complex agent behaviors.
subtype_of:
- { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
tags:
- skill
- capability
- agent-workflow
- composability
- reusable-methodology
required_tags:
- displayName
- argument-hint
- allowed-tools
- user-invocable
- implements
status: stable
stale_after: 2027-08-19
---
# Skill

A reusable, self-contained capability that encapsulates a specific workflow,
methodology, or expertise domain —
composable with other skills to form complex agent behaviors.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this
  class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances:
  - Must define a `name` and `description` in frontmatter.
  - Must declare a `workflow` section describing the step-by-step execution model.
  - Must define an `output` protocol for user selection/handoff.
  - Must declare required frontmatter tags: `displayName`, `argument-hint`, `allowed-tools`, `user-invocable`, `implements`.
  - May declare `critical-overrides`, `user-context`, `feedback-loop`, `output` protocols.
- May reference other skills via `$skill-name` syntax in body.

### Required Headers

- Workflow
- Output
- Handoff
- Contract
- Verification

## Implemented by

- Concrete skill files in Codex plugins reference this class via `subtype_of`.
