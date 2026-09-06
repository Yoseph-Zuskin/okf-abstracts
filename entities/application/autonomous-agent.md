---
type: Class
title: Autonomous Agent
description: A software agent that pursues goals on behalf of a principal with
  limited or no step-by-step direction.
tags:
- application
- agent
- autonomous
subtype_of:
- { type: Software Agent, resource: /entities/core/software-agent.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
status: stable
stale_after: 2027-08-19
---
# Autonomous Agent

A software agent that pursues goals on behalf of a principal with limited or no step-by-step direction.

## Contract

A concept of this class describes the class itself as a universal — *not* a
concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this
  class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

## Implemented by

- Concrete instances in the workspace bundles reference this class via
  `subtype_of`.
