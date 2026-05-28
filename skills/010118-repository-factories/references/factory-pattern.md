# Factory Pattern

## Structure

```
domain/{module}/repo.ts
```

One factory per domain. The factory accepts the Drizzle table(s) as parameters and returns a CRUD object.

## Type alias

The factory declares a type alias for the table shape it expects:

```typescript
type P = AnyPgTable & {
  id: any
  name: any
  slug: any
  organizationId: any
}
```

Only the columns used by the factory need to be declared. The `any` type is intentional — Drizzle's column types are too complex to replicate.

## Call site

Production and test use the same factory:

```typescript
import { products as prdProducts } from "@/app/db/schema"
import { testProducts } from "@/app/db/schema/test"

// Production
const repo = createProductsRepo(prdProducts as any)

// Test
const testRepo = createProductsRepo(testProducts as any)
```

## When to split into multiple table arguments

If a domain involves multiple related tables, accept them as an options object:

```typescript
export function createCronRepo(tables: {
  jobs: AnyPgTable
  executions: AnyPgTable
}) {
  return {
    async createJob(data) { /* uses tables.jobs */ },
    async createExecution(data) { /* uses tables.executions */ },
  }
}
```
