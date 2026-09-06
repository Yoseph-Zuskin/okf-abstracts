---
type: Class
title: Product Department
description: A business department responsible for product strategy, development, lifecycle management, and customer value delivery.
subtype_of:
- { type: Business Department, resource: /entities/domain/business-department.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-19T12:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-19T12:05:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-19T12:06:00Z' }
- { by: opencode/nemotron-3-ultra-free, at: '2026-08-23T16:40:30Z' }
tags:
- product-department
- product-management
- product-strategy
- product-development
- product-lifecycle
status: stable
stale_after: 2027-08-19
---
# Product Department

A business department responsible for product strategy, development, lifecycle management, and customer value delivery.

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

- Product Management
- Product Organization
- Product Team
