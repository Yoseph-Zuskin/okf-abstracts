# Pull Request

## Overview & Motivation

<!-- What is this change and why is it needed? Link issues with `Fixes #NNN`. -->

## What Changed

<!-- Bundle content (concepts/skills/templates/references/entities), tooling
(scripts, workflows), or metadata (manifests, indexes, versions). Note any
convention changes (AGENTS.md / OKF_STYLE_GUIDE.md) and new `draft` files. -->

## How It Was Tested

<!-- Check every box that applies. CI must be green before merge. -->

- [ ] `validate_subtype.py --strict`: 0 errors, 0 warnings
- [ ] `check_consistency.py`: 0 errors, 0 warnings
- [ ] `check_links.py` / `check_newlines.py`: clean
- [ ] Unit tests (`python -m unittest discover tests`): pass
- [ ] `pre-commit run --all-files`: green
- [ ] `okf-adversarial-review` skill: no BLOCKING findings (or they are listed above with justification)
- [ ] CHANGELOG `Unreleased` section updated (for user-facing changes)
- [ ] Generated copies re-ran (`regen_*.ps1`) with no unexpected diff
