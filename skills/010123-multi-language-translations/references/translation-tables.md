# Per-Entity Translation Tables

## Pattern

Each translatable entity gets its own `_translations` table:

```typescript
// products + product_translations
const productTranslations = pgTable("prd_product_translations", {
  id: id(),
  productId: text("productId").notNull().references(() => products.id, { onDelete: "cascade" }),
  languageCode: text("languageCode").notNull().references(() => languages.code, { onDelete: "restrict" }),
  name: text().notNull(),
  description: text(),
  longDescription: text("longDescription"),
  slug: text().notNull(),
  badge: text(),
  sellerTitle: text("sellerTitle"),
  sellerInfo: text("sellerInfo"),
  shippingTitle: text("shippingTitle"),
  shippingInfo: text("shippingInfo"),
  warrantyTitle: text("warrantyTitle"),
  warrantyInfo: text("warrantyInfo"),
  supportTitle: text("supportTitle"),
  supportInfo: text("supportInfo"),
  returnsTitle: text("returnsTitle"),
  returnsInfo: text("returnsInfo"),
  specsOnPdf: text("specsOnPdf"),
})

// Same pattern for: category_translations, variant_translations, storehouse_translations, rating_translations
```

## Constraints

```sql
-- One translation per language per entity
UNIQUE (product_id, language_code)
UNIQUE (slug, language_code)  -- each language has its own URL namespace

-- Prevent deleting languages with active translations
FOREIGN KEY (language_code) REFERENCES languages(code) ON DELETE RESTRICT
```

## Languages table

```typescript
const languages = pgTable("sys_languages", {
  code: text().primaryKey(),
  name: text().notNull(),
  direction: text().notNull().default("ltr"),  -- "ltr" | "rtl"
  isActive: boolean("isActive").default(false),
  isDefault: boolean("isDefault").default(false),
})
```
