# Claude Agent Guide

This repository uses one agent guide. Read [AGENTS.md](AGENTS.md) for the
catalog, the format rules and the commands.

Quick reference:

- Validate everything with `pnpm validate`.
- Run a skill script with `pnpm skill <name>`.
- Never edit versions by hand; use `pnpm changeset` and `pnpm run version`.
- Skills are instructions, not programs: the only code allowed is an optional
  `scripts/main.ts`, executed explicitly.
- No code blocks in markdown except mermaid.
