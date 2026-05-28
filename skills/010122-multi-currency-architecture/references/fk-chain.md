# Foreign Key Chain

## Currency → Country → Tax

```
sys_currencies.countryId → sys_countries.id
sys_taxes.currencyId → sys_currencies.id
sys_taxes.countryId → sys_countries.id
```

## Schema

```typescript
const currencies = pgTable("sys_currencies", {
  code: text("code").primaryKey(),
  name: text().notNull(),
  symbol: text().notNull(),
  countryId: text("countryId").references(() => countries.id),
  isDefault: boolean("isDefault").default(false),
  isActive: boolean("isActive").default(true),
})

const taxes = pgTable("sys_taxes", {
  id: id(),
  countryId: text("countryId").notNull().references(() => countries.id),
  currencyId: text("currencyId").notNull().references(() => currencies.code),
  name: text().notNull(),
  rate: numeric({ precision: 5, scale: 2 }).notNull(),
  isActive: boolean("isActive").default(true),
})
```

## FK Protection on DELETE

Before deleting a currency or country, verify no prices or storehouses reference it. Return 409 if referenced.
