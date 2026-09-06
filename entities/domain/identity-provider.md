---
type: Class
title: Identity Provider
description: A system entity that creates, maintains, and manages identity information for principals and provides authentication services to relying applications.
subtype_of:
- { type: Software System, resource: /entities/domain/software-system.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- identity-provider
- authentication
- authorization
- identity-management
- single-sign-on
status: stable
stale_after: 2027-08-19
---
# Identity Provider

A system entity that creates, maintains, and manages identity information for
principals and provides authentication
services to relying applications.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this
  class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

## Implemented by

- Concrete instances in the workspace bundles reference this class via
  `subtype_of`.

## Aliases

- IdP
- Identity Service
- Authentication Provider
