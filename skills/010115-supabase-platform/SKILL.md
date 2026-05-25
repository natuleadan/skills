---
name: 010115-supabase-platform
description: Supabase platform — Row Level Security, Edge Functions, Realtime patterns, Storage signed URLs, PostgreSQL schema design, and anti-patterns.
---

# Supabase Platform

## Overview

Supabase is an open-source Firebase alternative built on PostgreSQL. This skill covers RLS security, Edge Functions (Deno), Realtime (Broadcast + Postgres Changes), Storage, schema design conventions, and common anti-patterns.

## Quick Reference

### Core Concepts

| Area | Description |
|------|-------------|
| Database | PostgreSQL with UUID v4, snake_case, audit columns |
| RLS | Row Level Security — mandatory on all tables |
| Auth | `auth.uid()` in RLS policies, custom claims in JWT |
| Storage | Private buckets + signed URLs, RLS on `storage.objects` |
| Realtime | Broadcast (low-latency pub-sub) vs Postgres Changes (WAL-based) |
| Edge Functions | Deno runtime, Hono router, service role key |

### Environment Variables
- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_ANON_KEY` — Public anon key for client-side
- `SUPABASE_SERVICE_ROLE_KEY` — Server-side key (bypasses RLS)

## References

- [RLS Security](references/rls-security.md) — Row Level Security policies, null safety, indexes
- [Edge Functions](references/edge-functions.md) — Deno runtime, Hono router, setup
- [Realtime Patterns](references/realtime-patterns.md) — Broadcast vs Postgres Changes, channels
- [Storage](references/storage-implementation.md) — Signed URLs, TUS uploads, bucket RLS
- [Schema Design](references/schema-design.md) — PostgreSQL conventions, constraints, ENUMs
- [Anti-Patterns](references/anti-patterns.md) — Common mistakes to avoid
- [SQL Examples](references/code-examples-sql.md) — RLS, schema, storage, triggers
- [API Examples](references/code-examples-api.md) — Edge Functions, Realtime, client usage
- [Quick Reference](references/reference.md) — Cheat sheet
