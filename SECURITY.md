# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, use GitHub's private vulnerability reporting (the repository's
Security tab → "Report a vulnerability"). Solo-maintainer project: there is
no bug bounty program and no SLA, but every private report is reviewed;
fix, release, and credit follow coordinated disclosure.

Please include as much as you can:

- Type of issue (e.g. path traversal, injection, exfiltration, vulnerable dependency)
- Full paths of involved source files
- Tag, branch, or commit (or direct URL) of the affected code
- Any special configuration required to reproduce
- Step-by-step instructions to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact, including how an attacker might exploit the issue

## Automated Scanning

Repository scanned 2026-09-12 with [SkillSpector](https://github.com/NVIDIA/SkillSpector)
2.11.2, static analysis only (no LLM provider credentials on the scanning
machine; semantic stage unavailable, so this is pattern evidence, not a
conclusive verdict).

- **Scope:** whole repository (124 Markdown, 13 Python, manifests, workflows).
- **Result:** score 81/100, severity CRITICAL, recommendation DO_NOT_INSTALL,
  on 42 static-pattern hits.
- **Triage:** all 42 verified false positives against file content: 14 HIGH
  hits are git-ignored, untracked `__pycache__`/`.pyc` test artifacts (never
  shipped; cleaned before scan); 2 MEDIUM "MCP Rug Pull" hits are
  `markdownlint-cli2` lint invocations (`npx markdownlint-cli2`), not MCP
  servers; 21 MEDIUM "Skill Enumeration" hits are documentation citations
  and links to local skill docs (OKF `sources[].id` footnotes, `subtype_of`
  cross-repo URLs, `index.md` manifest links) — the scanner flags any URL-
  like string as "skill reference," but these are static knowledge-bundle
  metadata, not dynamic skill loads; 5 MEDIUM `subprocess` hits are
  fixed-argument `git` (log/status/diff) and `pytest` calls in validators
  with no shell, no untrusted input, and no network.
- **Attack surface:** this repo contains no MCP server, no hooks, no network
  services, and no credentials. Executable code is stdlib-plus-pyyaml
  validators with no exec/eval/network sinks (verified by grep).
- **Residual hygiene (not vulnerabilities):** delete `__pycache__` dirs;
  consider pinning the `npx markdownlint-cli2` version.
- **Prior differing scores** (e.g. a reported 15/100 elsewhere) were not
  reproduced and are inconsistent with this evidence; they reflect a
  different scan mode or scope, not a different repo.

Scores measure pattern hits, not exploitability. Re-run with LLM semantic
analysis available before treating any future scan as conclusive.

## Semantic Scan Addendum (2026-09-12)

Repository re-scanned 2026-09-12 with SkillSpector 2.11.2, `opencode_cli`
provider (Nemotron 3 Ultra Free), LLM semantic analysis enabled.

- **Scope:** whole repository (124 Markdown, 13 Python, manifests, workflows).
- **Result:** score 83/100, severity CRITICAL, recommendation DO_NOT_INSTALL,
  on 0 semantic findings (4 semantic analyzers attempted, 3 succeeded, 1
  degraded).
- **Triage:** 0 semantic findings — no delta vs static baseline.
- **Verdict:** No actionable security issues; the CRITICAL score is a
  static-pattern artifact (all 81 static hits previously triaged as FP).
  Semantic scan adds no new risks. Posture unchanged.

## Semantic Re-scan Addendum (2026-09-13)

Repository re-scanned 2026-09-13 with SkillSpector 2.11.2, `opencode_cli`
provider, model `opencode/nemotron-3-ultra-free`, LLM semantic
analysis requested.

- **Result:** score 83/100, severity CRITICAL, recommendation DO_NOT_INSTALL,
  unchanged vs the 2026-09-12 semantic baseline (still +2 vs the static 81).
- **Caveat:** 0/4 LLM calls succeeded — the shared runtime budget expired
  before any model inference, so the model was never invoked and this run
  is static-only, same as the Nemotron run.
- **Triage:** 0 new true positives — finding content identical to the
  prior semantic baseline, no delta vs static baseline. Posture unchanged.

## Semantic Re-scan Addendum (2026-09-19)

Repository `skills/` re-scanned 2026-09-19 with SkillSpector 2.11.2,
`copilot_cli` provider (local fork branch, Copilot Free CLI-default
model), LLM semantic analysis enabled — every skill executed
successfully (prior whole-repo semantic baselines above still stand
for non-skill content).

- **Scope:** `skills/` only, recursive (5 `SKILL.md`).
- **Result:** max risk 34/100, severity MEDIUM, recommendation CAUTION,
  on 4 semantic findings.
- **Triage:** 2 HIGH purpose-mismatch (TP4) hits on
  `okf-abstract-lineage` and `okf-intermediate-layers` are analyzer
  misfires — both skills are markdown-only workflows with no executable
  code, so there is no "supplied code" to mismatch the description
  against (FP). 1 MEDIUM (SDI-4) on `okf-abstract-lineage` is a real
  doc inconsistency: the usage section documents `--update-versions`
  auto-bumping `subtype_of[].version` while the contract claims the
  skill never modifies bundle files — logged as doc-clarity backlog
  (clarify default read-only vs explicitly confirmed writes). 1 MEDIUM
  (SQP-2) on `okf-intermediate-layers` is advisory: add a mutation
  warning near the workflow (writes entity files, linkages, indexes).
  A single-skill probe the same day surfaced one further MEDIUM
  (allowed-tools Write/Edit/Bash vs read-only invariant on
  `okf-validate-subtype`) that the full run did not reproduce —
  LLM variance, same doc-clarity class, also backlog.
- **Environment note:** the `opencode_cli`/Nemotron route delivered 0/4
  LLM calls today — Zen now answers 403 ("free tier can only be used
  from within OpenCode") whenever the provider's isolation env
  (`OPENCODE_CONFIG_CONTENT` or `OPENCODE_PERMISSION` alone suffices)
  is present. Bisected and fork tree left clean; upstream issue
  material. Unrelated to this repo's posture.
- **Verdict:** No exploitable issues; no code changes required.
  Posture unchanged: doc-clarity backlog only.
