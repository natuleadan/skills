---
name: 010110-clean-architecture
description: Clean Architecture layer ordering and strict inward dependency flow for web applications. Domain → Application → Infrastructure → Actions → UI.
---

# Clean Architecture

## Core Principle

> Dependencies flow inward. Inner layers know nothing about outer layers.

## Layer Order (Outer to Inner)

1. **UI/Components** — Presentation components
2. **Hooks** — React hooks (if applicable)
3. **App/Pages** — Route pages and layouts
4. **Actions** — Entry points (Server Actions, controllers)
5. **Infrastructure** — External integrations (DB, cache, APIs)
6. **Application** — Use cases and services
7. **Domain** — Business entities (pure, no dependencies)

## Layer Responsibilities

### Domain Layer (Innermost)

- Pure business logic
- No external dependencies
- Entities, value objects, interfaces
- Zero imports from any other layer

### Application Layer

- Use cases and service orchestration
- Depends only on domain interfaces (ports)
- DTOs for data transfer
- No framework or infrastructure imports

### Infrastructure Layer

- Implements application interfaces (adapters)
- Database clients, external API clients, cache, file storage
- Vendor SDKs live here
- Cookie I/O, authentication providers

### Actions Layer

- Entry points: Server Actions, API route handlers, CLI commands
- Validate authentication and authorization
- Call application services
- Thin — no business logic

### UI Layer (Outermost)

- Components, pages, layouts
- Calls actions (not services/repositories directly)
- Read-only data fetching via dedicated hooks

## Clean Architecture Checklist

- [ ] Domain has no imports from infrastructure or UI
- [ ] Application uses interfaces (ports), not concrete implementations
- [ ] Infrastructure implements application interfaces (adapters)
- [ ] Actions call services, not repositories directly
- [ ] All external dependencies are in infrastructure layer
- [ ] UI calls actions, not services or repositories
- [ ] Dependency direction: UI → Actions → App → Infra → Domain
- [ ] No circular dependencies between layers

## Migration Pattern

For legacy modules without clear layering:

1. Identify module boundaries
2. Create domain entities first (pure types + logic)
3. Extract infrastructure concerns
4. Define application service interfaces
5. Wire up actions as entry points
6. Remove legacy code when migration is complete

## Quick Reference

| Layer | Can import from | Cannot import from |
|-------|----------------|-------------------|
| Domain | Nothing | Everything |
| Application | Domain | Infrastructure, UI |
| Infrastructure | Domain | UI, Actions |
| Actions | App, Infra, Domain | UI |
| UI | Actions | Domain (directly), Infrastructure |

## References

- [Layers](references/layers.md)
- [Service Layering](references/service-layering.md) — Repository → Service → Action layer pattern with userRole propagation
