# Skills Index

Skills use numeric codes to encode a three-level hierarchy: domain, category, and skill. Each skill lives at `skills/<skill-code>-<name>/` with a `SKILL.md` file.

Format: `DDCCSS-word-word` (6 digits, exactly 2 words after the code, each ≥4 characters).

## Complete Skill List

| Domain | Category | Skill | Description |
|---|---|---|---|
| `01-programming` | `0101-tools` | `010101-package-security` | Hardens npm, pnpm, and bun against supply chain attacks |
| | | `010102-install-toolchain` | Installs and configures the JS/TS toolchain from scratch |
| | | `010103-package-operations` | Day-to-day package management: install, update, audit, publish |
| | `0102-agents` | `010104-skill-creator` | Guides creation of new Agent Skills |
| | `0103-standards` | `010105-frontend-coding` | React, accessibility, and frontend performance best practices |
| | | `010106-backend-architecture` | Error handling, module structure, env management, API patterns |
| | | `010107-code-quality` | TypeScript strict patterns, testing (vitest), and security rules |
| | `0104-git` | `010108-version-control` | Conventional commits, safe staging, disaster recovery via git reflog |
| | | `010109-release-automation` | Semantic-release, version bump mapping, post-release sync |
| | `0105-architecture` | `010110-clean-architecture` | Clean Architecture layer ordering and strict inward dependency flow |
| | | `010111-http-caching` | Three-tier caching strategy: browser/CDN, runtime cache, distributed cache |
| `02-business` | `0201-crm` | `020101-contact-crm` | CSV contact management with UUID linking, phone validation, auto-export |
| `03-artificial` | `0301-lancedb` | `030101-lancedb-search` | Vector search fundamentals: distance metrics, ANN, embeddings |
| | | `030102-lancedb-index` | Vector index types (IVF, HNSW, PQ), quantization, reindexing |
| | | `030103-lancedb-fulltext` | Full-text search with BM25: FTS indexing, fuzzy, boolean queries |
| | | `030104-lancedb-hybrid` | Hybrid search (vector+FTS), multivector (ColBERT), filtering |
| `04-devops` | `0401-docker` | `040101-docker-deploy` | Docker multi-stage builds, env mgmt, CI/CD integration |
| `05-devices` | `0501-web` | `050101-elysia-patterns` | Elysia API framework: plugins, controllers, auto-routing, auth macros |
| | | `050102-nextjs-compiler` | SWC compiler optimization: removeConsole, tree-shaking, bundle size |
| | | `050103-server-actions` | Server Actions: form handling, auth, typed returns, error patterns |
| `06-security` | `0601-auth` | `060101-http-security` | Multi-layer security: rate limiting, CSP, security headers, CORS |
| | | `060102-zero-trust` | Zero Trust auth: single validation, role propagation, no client trust |
| | | `060103-better-auth` | Better Auth integration: setup, API endpoints, client SDK, session |
| `07-data` | `0701-database` | `070101-prisma-database` | Prisma 7 setup with PostgreSQL adapter and Better Auth schema models |
| `08-design` | — | — | UX, UI, accessibility (future) |
| `09-science` | — | — | Biology, chemistry, physics (future) |
| `10-education` | — | — | Learning platforms, courses (future) |
| `11-health` | — | — | Healthcare, medical apps (future) |
| `12-finance` | — | — | Fintech, payments, banking (future) |
| `13-legal` | — | — | Legal compliance, contracts (future) |
| `14-media` | — | — | Audio, video, image processing (future) |
| `15-gaming` | — | — | Game development (future) |
| `16-automation` | — | — | Process automation, RPA (future) |
| `17-networking` | — | — | Networks, protocols, APIs (future) |
| `18-embedded` | — | — | IoT, hardware, firmware (future) |
| `19-productivity` | — | — | Methodologies, documentation, project mgmt (future) |
| `20-social` | — | — | Social media, communication platforms (future) |
