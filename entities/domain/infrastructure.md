---
type: Class
title: Infrastructure
description: 'Computing infrastructure that hosts software systems and models: physical or virtualized compute, storage, and networking, whether on organizational premises or with a cloud provider.'
subtype_of:
- { type: Artifact, resource: /entities/core/artifact.md, version: v0.1.0 }
status: stable
stale_after: 2027-09-05
generated: { by: human:yoseph-zuskin, at: '2026-09-05T18:11:16Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- infrastructure
- hosting
- cloud
---

# Infrastructure

Infrastructure is where software runs: the compute, storage, and networking underneath systems and models. Cloud and on-premise are deployment postures of the same class, discriminated by who operates the physical layer — not by software-vs-hardware, since both postures mix virtualized and physical resources.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

Instances of `Infrastructure` MUST:

- State the hosting location (provider and region, or organizational premises).
- State the managed-vs-self-managed split (what the operator runs vs what the team runs).

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
