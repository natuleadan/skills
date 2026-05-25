# Contact CRM — CSV Schema Reference

Three normalized CSV files with UUID-based relational linking.

## Data Model

```
Organization ──1:N──→ Contact ──N:N──→ Product
```

- **Organization**: company or entity (address, industry, contact info)
- **Contact**: person linked to exactly one organization
- **Product**: standalone catalog item, referenced by contacts via `product_ids`

## organizations.csv

| # | Field | Type | Mutable | Example |
|---|-------|------|---------|---------|
| 1 | `id` | UUID | never | `550e8400-e29b-41d4-a716-446655440000` |
| 2 | `num` | string | auto | `"1"` |
| 3 | `name` | string | yes | `"Acme Corp"` |
| 4 | `industry` | string | yes | `"Technology / SaaS"` |
| 5 | `tax_id` | string | yes | `"1234567890001"` |
| 6 | `address` | string | yes | `"123 Main St"` |
| 7 | `city` | string | yes | `"New York"` |
| 8 | `province` | string | yes | `"NY"` |
| 9 | `postal_code` | string | yes | `"10001"` |
| 10 | `country` | string | yes | `"United States"` |
| 11 | `website` | string | yes | `"https://acme.com"` |
| 12 | `email` | string | yes | `"info@acme.com"` |
| 13 | `phone` | string | yes | `"+1 555-0123"` |
| 14 | `linkedin` | string | yes | `"/company/acme"` |
| 15 | `twitter` | string | yes | `"@acme"` |
| 16 | `notes` | string | yes | `"Main supplier for region"` |
| 17 | `tags` | string | yes | `"technology, supplier, nys"` |

## contacts.csv

| # | Field | Type | Mutable | Links to |
|---|-------|------|---------|----------|
| 1 | `num` | string | auto | Display number |
| 2 | `id` | UUID | never | Primary key |
| 3 | `name` | string | yes | First name |
| 4 | `last_name` | string | yes | Last name |
| 5 | `email` | string | yes | |
| 6 | `mobile_phone` | string | yes | |
| 7 | `landline_phone` | string | yes | |
| 8 | `job_title` | string | yes | Job title |
| 9 | `organization_id` | UUID | yes | `organizations.id` |
| 10 | `source` | string | yes | Lead source |
| 11 | `product_ids` | string | yes | Comma-separated `products.id` |
| 12 | `type` | string | yes | `supplier`, `contact`, `organization` |
| 13 | `status` | string | yes | `active`, `inactive` |
| 14 | `priority` | string | yes | `high`, `medium`, `low` |
| 15 | `registration_date` | datetime | auto | |
| 16 | `last_interaction` | datetime | auto | |
| 17 | `notes` | string | yes | |
| 18 | `tags` | string | yes | |

## products.csv

| # | Field | Type | Mutable | Example |
|---|-------|------|---------|---------|
| 1 | `id` | UUID | never | |
| 2 | `num` | string | auto | |
| 3 | `name` | string | yes | `"Widget Pro"` |
| 4 | `category` | string | yes | `"electronics / widgets"` |
| 5 | `presentation` | string | yes | `"box of 12"` |
| 6 | `volume` | string | yes | `"1,000 units/month"` |
| 7 | `reference_price` | string | yes | `"$14.99"` |
| 8 | `coverage` | string | yes | `"nationwide"` |
| 9 | `fleet` | string | yes | `"yes"` |
| 10 | `regulatory` | string | yes | `"ISO 9001"` |
| 11 | `notes` | string | yes | |
| 12 | `tags` | string | yes | |

## Conventions

- `name` with parentheses `(Org Name)` signals organization-only contact (no person attached)
- Tags: comma-separated lowercase keywords for search
- Industry/category: use `/` for hierarchy, e.g. `"Technology / SaaS / CRM"`
- Phone format: `(label) number, (label2) number2`
