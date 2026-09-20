# Natuleadan Skills - Agent Guide

This repository contains installable agent skills for AI coding agents.

## Quick Links

- **[README.md](README.md)** - Full documentation and installation
- **[SKILLS.md](SKILLS.md)** - The complete skill catalog
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Skill format, naming, and validation

## Skills

Skills are installed via `npx skills add natuleadan/skills`. Each skill lives in
`skills/<skill-name>/` with a `SKILL.md` containing instructions for the agent.

### Platform Skills (4)

- `platform` - Platform APIs (agents, robots, toolsets, scheduling, HIL)
- `sdk-api` - Go SDK for YAML-driven services
- `sdk-ops` - CLI for provisioning and operating infrastructure
- `neural-db` - Enhanced SQL engine with native vector search

### Industry AI Tools (16)

`healthcare` · `biology` · `agriculture` · `food-and-beverage` · `energy` ·
`manufacturing` · `logistics` · `environment` · `education` · `commerce` ·
`entertainment` · `technology` · `construction` · `security` · `space` ·
`government`

Each ends in `-ai-tools` (e.g. `healthcare-ai-tools`).

The industry skills are **provider-agnostic**: they describe AI tooling for an
area and work with a platform API or any compatible backend.

## Format

```
skills/<name>/
  SKILL.md          # frontmatter (name, description) + short instructions
  metadata.json     # version, abstract, references
  references/*.md   # prose notes; no embedded code
  code/*            # optional code, separated by language
```

- **No code inside `.md`** - code lives under `code/<language>/`.
- Industry skills stay neutral: no provider-specific detail.

## Validation

Run `python3 tools/validate-all.py` before committing. Husky runs it on pre-commit.
