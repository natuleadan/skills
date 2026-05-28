# Domain Factory Pattern

## Purpose

Domain factories create reusable CRUD instances parameterized with a Drizzle table. This allows the same code to work with test (`tst_*`) and production (`prd_*` / `sys_*`) tables.

## Pattern

```typescript
import { eq, sql } from "drizzle-orm"
import type { AnyPgTable } from "drizzle-orm/pg-core"
import { db } from "@/app/lib/infra/db"

type P = AnyPgTable & { id: any; name: any }

export function createProductsRepo(table: P) {
  return {
    async listAll() {
      return db.select().from(table).orderBy(sql`${table.name} asc`)
    },

    async getById(id: string) {
      const [row] = await db.select().from(table)
        .where(eq(table.id, id)).limit(1)
      return row ?? null
    },

    async create(data: Record<string, unknown>) {
      const [row] = await db.insert(table)
        .values(data as any).returning()
      return row
    },

    async update(id: string, data: Record<string, unknown>) {
      const [row] = await db.update(table)
        .set(data as any).where(eq(table.id, id)).returning()
      return row ?? null
    },

    async remove(id: string) {
      const [row] = await db.delete(table)
        .where(eq(table.id, id)).returning()
      return row ?? null
    },
  }
}
```

## Usage

```typescript
// Production
const repo = createProductsRepo(prdProducts as any)

// Test  
const testRepo = createProductsRepo(testProducts as any)
```

## `as any` bridging

The `as any` cast on the table parameter is necessary because Drizzle's table types are complex generics that are impractical to type fully in a factory. The cast is safe because the factory only accesses columns declared in the type `P`.

## Factory composition

For related tables, accept multiple tables:

```typescript
export function createCronRepo(tables: {
  jobs: AnyPgTable
  executions: AnyPgTable
}) { /* ... */ }
```
