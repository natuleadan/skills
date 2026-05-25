---
name: 070101-prisma-database
description: Prisma 7 setup with PostgreSQL driver adapters and Better Auth schema models (User, Session, Account, Verification).
---

# Prisma + Database Setup

## Overview

Prisma 7 uses driver adapters instead of traditional database clients. This skill covers setup, configuration, and the required Better Auth schema models.

## Quick Start

```bash
# Install
npm install @prisma/client @prisma/adapter-pg pg dotenv
npm install -D prisma @types/pg

# Configure
# Create prisma.config.ts in project root

# Generate client
npx prisma generate
```

## Key Files

| File | Purpose |
|------|---------|
| `prisma.config.ts` | Prisma configuration with driver adapter |
| `prisma/schema.prisma` | Schema definition (User, Session, Account, Verification) |
| `src/infrastructure/database/prisma.ts` | Client instantiation with PrismaPg adapter |

## Quick Reference

```typescript
// prisma.config.ts
import "dotenv/config"
import { defineConfig, env } from "prisma/config"

export default defineConfig({
  schema: "prisma/schema.prisma",
  datasource: { url: env("DATABASE_URL") },
})
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}

datasource db {
  provider = "postgresql"
}
```

```typescript
// src/infrastructure/database/prisma.ts
import { PrismaPg } from "@prisma/adapter-pg"
import { PrismaClient } from "../../../generated/prisma/client"

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL })
const prisma = new PrismaClient({ adapter })

export default prisma
```

## References

- [Setup Guide](references/setup.md) — Full Prisma 7 installation and config
- [Schema Models](references/schema-models.md) — Better Auth User, Session, Account, Verification
