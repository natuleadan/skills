# Prisma 7 Setup

## Prisma 7.x Configuration

> Prisma 7 uses driver adapters instead of traditional database clients.

### Installation

- Install production: `@prisma/client`, `@prisma/adapter-pg`, `pg`, `dotenv`
- Install dev: `prisma`, `@types/pg`

### Configuration File

Create `prisma.config.ts` in project root:

```typescript
import "dotenv/config";
import { defineConfig, env } from "prisma/config";

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations" },
  datasource: { url: env("DATABASE_URL") },
});
```

## Schema Configuration

### Generator Setup

```prisma
generator client {
  provider = "prisma-client"
  output   = "../generated/prisma"
}
```

- Use `provider = "prisma-client"` (not prisma-client-js)
- Set output path for generated client
- Generate with: `npx prisma generate`

### Database Connection

```prisma
datasource db {
  provider = "postgresql"
}
```

- Do not include URL in schema (use prisma.config.ts)
- URL comes from environment variable

## Client Instantiation

Create `src/infrastructure/database/prisma.ts`:

```typescript
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../../../generated/prisma/client";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

export default prisma;
```

## Commands

- `npx prisma generate` — Generate Prisma Client
- `npx prisma db:push` — Push schema to database
- `npx prisma db:migrate` — Create and apply migrations
- `npx prisma studio` — Open Prisma Studio
