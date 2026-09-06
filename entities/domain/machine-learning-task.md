---
type: Class
title: Machine Learning Task
description: 'A well-defined problem type solved by training or prompting a model (classification, regression, clustering). Tasks are not paradigms: a paradigm is how learning happens, a task is what gets solved.'
subtype_of:
- { type: Concept, resource: /entities/foundational/concept.md, version: v0.1.0 }
status: stable
stale_after: 2027-09-05
generated: { by: human:yoseph-zuskin, at: '2026-09-05T18:11:16Z' }
verified:
- { by: opencode/muse-spark-1.3-free, at: '2026-09-05T18:11:16Z' }
tags:
- machine-learning
- tasks
---

# Machine Learning Task

A machine learning task names WHAT gets solved (predict a label, estimate a value, group similar items). A paradigm (`Supervised Learning`, `Unsupervised Learning`) names HOW learning happens (from labeled data, from unlabeled structure). Classification is a task performed under the supervised paradigm — tasks are never paradigms, and paradigms are never tasks.

## Contract

A concept of this class describes the class itself as a universal — *not* a concrete instance. Its body defines the contract for instances:

- **What it is** (definition above).
- **Frontmatter** an instance must carry: a distinct `type` value naming this class, plus a `subtype_of` entry `{ type: <Class>, resource: <href>, version: <tag> }` pointing here.
- **Body conventions** expected of instances.

Instances of `Machine Learning Task` MUST:

- Name the task type and its input/output contract.
- State the evaluation metric the task is judged by.
- Name the paradigm family the task is performed under, without claiming to BE the paradigm.

## Related Concepts

- [Learning Paradigm](/entities/domain/learning-paradigm.md) - defines the paradigms (supervised, unsupervised, reinforcement) tasks are performed under.
- [Supervised Learning](/entities/application/supervised-learning.md) - paradigm for classification and regression tasks.
- [Unsupervised Learning](/entities/application/unsupervised-learning.md) - paradigm for clustering tasks.

## Implemented by

- Concrete instances in the workspace bundles reference this class via `subtype_of`.
