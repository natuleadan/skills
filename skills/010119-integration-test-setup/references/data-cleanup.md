# Data Cleanup Patterns

## Golden rule

**Never delete seed data.** All cleanup must target `test-%` / `TEST-%` prefixed records only.

## Product cleanup

```typescript
const pool = new Pool({ connectionString: DATABASE_URL })
await pool.execute(`
  DELETE FROM prd_variants
  WHERE product_id IN (SELECT id FROM prd_products WHERE name LIKE 'test-%')
`)
await pool.execute("DELETE FROM prd_products WHERE name LIKE 'test-%'")
await pool.end()
```

## Sub-resource cleanup (cascading)

```typescript
const ids = await pool.query("SELECT id FROM prd_products WHERE name LIKE 'test-%'")
const idList = ids.rows.map(r => `'${r.id}'`).join(",")
if (!idList) return

const tables = [
  "prd_inventory", "prd_prices", "prd_medias",
  "prd_ratings", "prd_variants",
]
for (const table of tables) {
  await pool.execute(`DELETE FROM ${table} WHERE product_id IN (${idList})`)
}
await pool.execute("DELETE FROM prd_products WHERE name LIKE 'test-%'")
```

## KV cache cleanup

```typescript
// Never use FLUSHALL — delete targeted keys only
const keys = await kv.send("KEYS", ["cache:tags:*"])
if (keys?.length) await kv.send("DEL", [keys.join(" ")])
```

## Full cleanup in afterAll

```typescript
afterAll(async () => {
  const pool = new Pool({ connectionString: DATABASE_URL })
  await cascadeCleanup(pool)
  await pool.end()
})
```
