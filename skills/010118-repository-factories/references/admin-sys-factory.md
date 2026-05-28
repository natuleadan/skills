# Generic Admin System Factory

## Purpose

A single factory `createSysRepo(table, fkChecks?)` that provides full CRUD for any admin-managed system table (currencies, countries, languages, taxes).

## Implementation

```typescript
export function createSysRepo(table: AnyPgTable, fkChecks?: FkCheck[]) {
  return {
    list()       { return db.select().from(table) }
    getById(id)  { /* SELECT + LIMIT 1 */ }
    create(data) { /* INSERT RETURNING * */ }
    update(id, data) { /* UPDATE RETURNING * */ }
    remove(id) {
      // Verifica FK checks antes de borrar
      if (fkChecks) {
        for (const fk of fkChecks) {
          const [row] = await db.execute(sql`
            SELECT 1 FROM ${sql.raw(fk.table)} WHERE ${sql.raw(fk.column)} = ${id} LIMIT 1
          `)
          if (row) return { error: `Referenced by ${fk.label}` }
        }
      }
      return db.delete(table).where(eq(table.id, id)).returning()
    }
  }
}
```

## Adding a new admin table

One line in the controller:

```typescript
const resources = [
  { name: "payment-methods", table: sysPaymentMethods },
  // → Full CRUD endpoint at /v1/admin/payment-methods
]
```
