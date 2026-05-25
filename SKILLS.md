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
| | | `010107-code-quality` | Testing (vitest) and security rules (secrets, XSS, injection, CORS) |
| | | `010112-typescript-rules` | TypeScript 5.7+ strict mode, generics, mapped types, Zod, migration |
| | `0104-git` | `010108-version-control` | Conventional commits, safe staging, disaster recovery via git reflog |
| | | `010109-release-automation` | Semantic-release, version bump mapping, post-release sync |
| | `0105-architecture` | `010110-clean-architecture` | Clean Architecture layer ordering and strict inward dependency flow |
| | | `010111-http-caching` | Three-tier caching strategy: browser/CDN, runtime cache, distributed cache |
| | `0106-integrations` | `010113-polar-integration` | Polar.sh payment integration: sync, checkout, webhooks, MoR |
| | | `010114-stripe-integration` | Stripe payments, billing, connect platforms, treasury, CLI tools |
| | | `010115-supabase-platform` | PostgreSQL RLS, Edge Functions, Realtime, Storage, schema design |
| | `0107-i18n` | `010116-i18n-patterns` | RTL support, safe translations, LangProvider, language tables |
| `02-business` | `0201-crm` | `020101-contact-crm` | CSV contact management with UUID linking, phone validation, auto-export |
| `03-artificial` | `0301-lancedb` | `030101-lancedb-search` | Vector search fundamentals: distance metrics, ANN, embeddings |
| | | `030102-lancedb-index` | Vector index types (IVF, HNSW, PQ), quantization, reindexing |
| | | `030103-lancedb-fulltext` | Full-text search with BM25: FTS indexing, fuzzy, boolean queries |
| | | `030104-lancedb-hybrid` | Hybrid search (vector+FTS), multivector (ColBERT), filtering |
| `04-devops` | `0401-docker` | `040101-docker-deploy` | Docker multi-stage builds, env mgmt, CI/CD integration |
| `05-web` | `0501-frameworks` | `050101-elysia-framework` | Elysia API framework: plugins, controllers, auto-routing, auth macros |
| | | `050102-nextjs-framework` | Next.js 16 async APIs, Compiler, App Router, caching, SEO, anti-patterns |
| | `0502-patterns` | `050103-tailwind-implement` | Tailwind v4 CSS-first config, shadcn component composition, CVA patterns, styling rules |
| | `0503-seo` | `050104-seo-optimization` | XML Sitemaps protocol, robots.txt, metadata, Open Graph, canonical URLs, JSON-LD structured data |
| | | `060102-zero-trust` | Zero Trust auth: single validation, role propagation, no client trust |
| | | `060103-better-auth` | Better Auth integration: setup, API endpoints, client SDK, session |
| `07-data` | `0701-database` | `070101-prisma-database` | Prisma 7 setup with PostgreSQL adapter and Better Auth schema models |
| `08-design` | `0801-foundations` | `080101-design-foundations` | Color theory, design tokens, brand vs product register, OKLCH, absolute bans |
| | | `080102-design-typography` | Type selection, modular scale, spacing systems, grid theory, visual hierarchy |
| | `0802-ux` | `080103-ux-standards` | WCAG accessibility, touch interaction, form UX, navigation, UX writing |
| | `0803-motion` | `080104-motion-animation` | Animation timing and easing, spring physics, micro-interactions, reduced motion |
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
