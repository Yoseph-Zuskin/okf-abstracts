---
type: Class
title: Role
description: A functional position or capacity that an agent can assume within a context, defining responsibilities, authorities, and expectations.
tags:
  - core
  - role
  - responsibility
  - agent
subtype_of:
- { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }
generated: { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-29T00:00:00Z' }
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
status: stable
stale_after: 2027-08-29
---
# Role

A functional position or capacity that an agent can assume within a context, defining responsibilities, authorities, and expectations. Roles are assumed by agents (persons, organizations, software agents) in specific contexts.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.
- **Played-by pattern**: a Role is played by an Agent, never the other way around. Instances (people, organizations) that fill a role link both the Role subclass and the appropriate Agent subclass (`Person`, `Organization`); the Role link alone never stands in for the Agent link.

## Extensions

- **AssignedRole** — a role assigned to a specific agent in a context, with scope, duration, and delegation rules.
- **RoleAssignment** — the act of assigning a role to an agent, with delegation chains and revocation rules.
- **RoleHierarchy** — parent/child role relationships with inheritance of permissions.
- **RoleConflict** — detection and resolution of conflicting role assignments.
- **RoleLifecycle** — activation, suspension, revocation, and audit trails.

## Sources

- id: role-definition
  title: Role (Abstract Concept)
  resource: <https://en.wikipedia.org/wiki/Role>
  author: wikipedia

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
