---
name: sdk-api
description: "Use this skill when building services with the Go SDK - a YAML-driven framework for event-driven services with entries, auth, databases, events, and OpenAPI."
---

# Go SDK

A Go SDK for building services from **YAML**: entries, REST/CRUD, auth modes,
database drivers, events, and OpenAPI - almost everything is declared, not coded.

## What you get

- Declarative `service.yaml` as the single source of truth.
- CRUD and REST entries generated from YAML.
- Auth modes: `jwt`, `basic`, `oauth`, `session`.
- Pluggable databases: SQLite/libSQL, Turso, PostgreSQL, MySQL/MariaDB, MongoDB.
- Events over NATS (JetStream), with optional token/nkey/creds auth.
- OpenAPI 3 + Scalar docs, driven by the same YAML.

## Conventions

- YAML is ASCII-only.
- Codes and identifiers stay in English/latin.
- Health endpoints (`/healthz`, `/startupz`, `/readyz`, `/livez`) are built in.

## References

- `references/entries.md`
- `references/auth.md`
- `references/database.md`
- `references/events.md`
- `references/openapi.md`
- `references/deployment.md`
