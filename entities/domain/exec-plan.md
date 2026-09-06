---
type: Class
title: ExecPlan
description: A structured implementation plan with discrete, verifiable tasks and review checkpoints. Based on Superpowers' executing-plans and subagent-driven-development skills. Each task has exact file paths, complete code, and verification steps. Supports both batch execution with human checkpoints and subagent-driven parallel execution.
subtype_of:
- { type: Operational Artifact, resource: /entities/core/operational-artifact.md, version: v0.1.0 }
status: stable
stale_after: 2027-08-29
generated: { by: human:yoseph-zuskin, at: '2026-08-29T14:30:00Z' }
verified:
- { by: human:yoseph-zuskin, at: '2026-08-29T14:35:00Z' }
- { by: opencode/deepseek-v4-flash-free, at: '2026-08-29T14:36:00Z' }
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- planning
- execution
- project-management
sources:
- id: superpowers-executing-plans
  title: Superpowers executing-plans skill
  resource: https://github.com/obra/superpowers/skills/executing-plans/SKILL.md
  author: human:jesse-vincent
- id: superpowers-subagent-driven
  title: Superpowers subagent-driven-development skill
  resource: https://github.com/obra/superpowers/skills/subagent-driven-development/SKILL.md
  author: human:jesse-vincent
- id: superpowers-writing-plans
  title: Superpowers writing-plans skill
  resource: https://github.com/obra/superpowers/skills/writing-plans/SKILL.md
  author: human:jesse-vincent
- id: superpowers-git-worktrees
  title: Superpowers using-git-worktrees skill
  resource: https://github.com/obra/superpowers/skills/using-git-worktrees/SKILL.md
  author: human:jesse-vincent
- id: superpowers-finishing-branch
  title: Superpowers finishing-a-development-branch skill
  resource: https://github.com/obra/superpowers/skills/finishing-a-development-branch/SKILL.md
  author: human:jesse-vincent
---

# ExecPlan

An **ExecPlan** is a structured implementation plan that breaks work into discrete, verifiable tasks. Each task specifies exact file paths, complete code, and verification steps. The plan supports two execution modes:

1. **Batch execution with human checkpoints** (`executing-plans`) — Tasks grouped into batches; human reviews at checkpoints
2. **Subagent-driven parallel execution** (`subagent-driven-development`) — Fresh subagent per task with two-stage review (spec compliance, then code quality)

## Contract

An ExecPlan instance MUST:

- List discrete tasks, each with exact file paths and complete code or an explicit human review checkpoint.
- State verification steps per task with expected outcomes.
- Declare its execution mode: batch with human checkpoints, or subagent-driven parallel execution.

## Core Principles

### True Red/Green/Refactor TDD

- Write failing test first
- Watch it fail
- Write minimal code to pass
- Watch it pass
- Refactor
- Commit

### YAGNI (You Aren't Gonna Need It)

- No speculative abstractions
- No boilerplate "for later"
- One line before fifty

### Complexity Reduction

- Simplicity as primary goal
- Stdlib before dependencies
- Native platform features before libraries

## Structure

An ExecPlan consists of:

### 1. Phase Overview

High-level phases with clear deliverables and acceptance criteria.

### 2. Task List

Each task contains:

- **Task ID** — Unique identifier
- **Objective** — What this task accomplishes
- **Files to Modify/Create** — Exact paths
- **Complete Code** — Full implementation (not pseudocode)
- **Verification Steps** — Commands to run, expected outputs
- **Dependencies** — Other task IDs this depends on

### 3. Review Checkpoints

- **Spec Compliance Review** — Does implementation match plan?
- **Code Quality Review** — Over-engineering, security, testing
- **Human Gate** — Explicit approval before next phase

## Execution Modes

### Mode A: Batch Execution with Checkpoints

```text
Phase 1 → [Task 1, Task 2, Task 3] → Checkpoint 1 (human review)
Phase 2 → [Task 4, Task 5] → Checkpoint 2
Phase 3 → [Task 6] → Done
```

Human reviews at each checkpoint before proceeding.

### Mode B: Subagent-Driven Development

```text
Task 1 → Subagent 1 → Spec Review → Code Quality Review → Commit
Task 2 → Subagent 2 → Spec Review → Code Quality Review → Commit
...
```

Fresh subagent per task. Two-stage review per task.

## Verification Standards

Every task must include runnable verification:

- Unit tests (pytest, jest, etc.)
- Lint/typecheck commands
- Integration test if applicable
- Manual verification steps if automated not feasible

## Source Attribution

Based on Superpowers skills:

- `executing-plans` — Batch execution with human checkpoints[^superpowers-executing-plans]
- `subagent-driven-development` — Parallel subagent execution with two-stage review[^superpowers-subagent-driven]
- `writing-plans` — Plan creation from approved design[^superpowers-writing-plans]
- `using-git-worktrees` — Isolated workspace per task[^superpowers-git-worktrees]
- `finishing-a-development-branch` — Merge/PR decision workflow[^superpowers-finishing-branch]

[^superpowers-executing-plans]: [Superpowers executing-plans skill](https://github.com/obra/superpowers/skills/executing-plans/SKILL.md)
[^superpowers-subagent-driven]: [Superpowers subagent-driven-development skill](https://github.com/obra/superpowers/skills/subagent-driven-development/SKILL.md)
[^superpowers-writing-plans]: [Superpowers writing-plans skill](https://github.com/obra/superpowers/skills/writing-plans/SKILL.md)
[^superpowers-git-worktrees]: [Superpowers using-git-worktrees skill](https://github.com/obra/superpowers/skills/using-git-worktrees/SKILL.md)
[^superpowers-finishing-branch]: [Superpowers finishing-a-development-branch skill](https://github.com/obra/superpowers/skills/finishing-a-development-branch/SKILL.md)
