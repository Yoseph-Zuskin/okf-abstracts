---
type: Class
title: Client
description: A role receiving services, products, or advice from a provider — defining requirements, accepting deliverables, and providing feedback.
subtype_of:
- { type: Role, resource: /entities/core/role.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
tags:
- client
- customer
- service-recipient
- engagement
sources:
- id: client-definition
  title: Client (Business)
  resource: https://en.wikipedia.org/wiki/Client_(business)
  author: org:wikipedia
status: stable
stale_after: 2027-08-29
---
# Client

A role receiving services, products, or advice from a provider — defining requirements, accepting deliverables, and providing feedback.

## Contract

Instances of `Client` MUST:

- Define the scope of engagement (project, retainer, product)
- Specify acceptance criteria and acceptance process
- Define communication cadence and escalation paths
- Clarify intellectual property ownership

## Extensions

- **InternalClient** — A department or team within the same organization
- **ExternalClient** — An individual or organization outside the provider's organization

## Sources

This class profile draws on Client (Business)[^client-definition].

[^client-definition]: [Client (Business)](https://en.wikipedia.org/wiki/Client_(business)) (wikipedia)

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
