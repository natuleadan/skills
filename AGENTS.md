# Natuleadan Skills — Agent Guide

This repository contains installable agent skills for AI coding agents.

## Quick Links

- **[README.md](README.md)** — Full documentation, installation, and project structure
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Skill creation conventions, naming, and validation

## Skills

Skills are installed via `npx skills add natuleadan/skills`. Each skill lives in `skills/<domain>/<category>/<skill-code>/` with a `SKILL.md` containing instructions for the agent.

## Validation

Run `python3 tools/validate-all.py` before committing. Husky runs it automatically on pre-commit.
