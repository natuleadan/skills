---
name: 010104-skill-creator
license: MIT
description: Guide for creating AI agent skills from scratch. Covers SKILL.md frontmatter, directory structure, progressive disclosure, writing patterns, bundled resources, testing with evals, benchmarking, packaging, distribution, and repo-level architecture. Use this skill whenever the user asks about creating a new skill, writing a SKILL.md, structuring a skill directory, setting up eval tests for a skill, packaging a skill for distribution, or understanding the skill format. Also trigger when the user says "turn this into a skill", "make a skill for X", or "how do I create a skill". Do NOT trigger for using existing skills — only for creating new ones.
---

# Skill Creator Guide

This skill teaches you how to create, test, package, and distribute AI agent skills following the standard Agent Skills format.

## How to use this skill

1. If the user asks about **basic concepts or structure** → read `references/structure.md`
2. If the user asks about **frontmatter or description** → read `references/frontmatter.md`
3. If the user asks about **writing style or patterns** → read `references/writing.md`
4. If the user asks about **testing, evals, or iteration** → read `references/testing.md`
5. If the user asks about **packaging or distribution** → read `references/distribution.md`
6. If the user asks about **repo architecture or marketplace** → read `references/repo-architecture.md`
7. If the user asks to **scaffold a new skill** → run `python scripts/scaffold.py <skill-name> --category <category/subcategory>`

## Quick reference checklist

- [ ] Choose a kebab-case name matching the directory (max 64 chars, lowercase + hyphens only)
- [ ] Write frontmatter with `name` and `description` (include trigger contexts, desc ≤ 1024)
- [ ] Optionally add `compatibility` (≤ 500 chars), `license`, `metadata`, `allowed-tools`
- [ ] Keep SKILL.md under 100 lines — use `references/` for detailed content
- [ ] Write in imperative tone, explain the why, include examples
- [ ] Add at least one Python script to `scripts/` (no external deps)
- [ ] Create `evals/evals.json` with test prompts
- [ ] Run validation: `python3 tools/validate-all.py` from repo root

## References

- `references/structure.md` — Directory layout, progressive disclosure, size limits
- `references/frontmatter.md` — Name rules, description rules, optimization
- `references/writing.md` — Tone, examples, explaining reasoning, keeping lean
- `references/testing.md` — Evals, assertions, grading, benchmarking, iteration
- `references/distribution.md` — Marketplace.json, packaging, install
- `references/repo-architecture.md` — Multi-category repo structure, validate-all.py, hierarchy
- `scripts/scaffold.py` — Creates a new skill skeleton with --category support
