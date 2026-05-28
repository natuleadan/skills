# Foreign Key Chains for Multi-Currency and Multi-Language

## Multi-currency FK chain

```
sys_currencies.id ← prd_prices.currencyId (FK)
sys_currencies.countryId → sys_countries.id (FK)
sys_taxes.currencyId → sys_currencies.id (FK)
sys_taxes.countryId → sys_countries.id (FK)
```

### Table design

```typescript
// sys_currencies
{ code: string, name: string, symbol: string, countryId: FK→countries, isDefault: bool, isActive: bool }

// sys_taxes
{ countryId: FK→countries, currencyId: FK→currencies, name: string, rate: number, isActive: bool }

// prd_prices
{ productId: FK→products, variantId: FK→variants?, currencyId: FK→currencies, price: decimal, compareAtPrice: decimal?, cost: decimal?, isActive: bool, validFrom: timestamp?, validUntil: timestamp? }
```

Uniqueness constraint: `UNIQUE(product_id, variant_id, currency_id)` with `NULLS NOT DISTINCT` — one price per currency per variant.

## Multi-language FK chain

```
sys_languages.code ← {entity}_translations.language_code (FK RESTRICT)
{entity}.id ← {entity}_translations.{entity}_id (FK CASCADE)
```

### Translation table pattern

Each translatable entity has exactly one `_translations` table:

```sql
CREATE TABLE category_translations (
  id UUID PK,
  category_id UUID FK→categories ON DELETE CASCADE,
  language_code TEXT FK→languages ON DELETE RESTRICT,
  name TEXT NOT NULL,
  description TEXT,
  slug TEXT NOT NULL,
  UNIQUE (category_id, language_code)
);
```

Same for: products, variants, ratings, storehouses.

### Why ON DELETE RESTRICT on language_code?

Prevents deleting a language that still has active translations. The admin must first:
1. Reassign or delete all translations using that language
2. Then delete the language itself

## FK Protection pattern (admin DELETE)

```typescript
function createSysRepo(table, fkChecks?: FkCheck[]) {
  return {
    async remove(id: string) {
      for (const check of (fkChecks ?? [])) {
        const refs = await db.query(check.table)
          .where(eq(check.column, id))
          .limit(1)
        if (refs.length > 0) {
          return { error: `Cannot delete: referenced by ${check.label}` }
        }
      }
      const [row] = await db.delete(table).where(eq(table.id, id)).returning()
      return { data: row }
    }
  }
}
```

This prevents deleting a currency that has prices, or a country used by storehouses.
