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
| 3 | `nombre` | string | yes | `"Acme Corp"` |
| 4 | `industria` | string | yes | `"Technology / SaaS"` |
| 5 | `ruc` | string | yes | `"1234567890001"` |
| 6 | `direccion` | string | yes | `"123 Main St"` |
| 7 | `ciudad` | string | yes | `"New York"` |
| 8 | `provincia` | string | yes | `"NY"` |
| 9 | `codigo_postal` | string | yes | `"10001"` |
| 10 | `pais` | string | yes | `"United States"` |
| 11 | `website` | string | yes | `"https://acme.com"` |
| 12 | `email` | string | yes | `"info@acme.com"` |
| 13 | `telefono` | string | yes | `"+1 555-0123"` |
| 14 | `linkedin` | string | yes | `"/company/acme"` |
| 15 | `twitter` | string | yes | `"@acme"` |
| 16 | `notas` | string | yes | `"Main supplier for region"` |
| 17 | `tags` | string | yes | `"technology, supplier, nys"` |

## contacts.csv

| # | Field | Type | Mutable | Links to |
|---|-------|------|---------|----------|
| 1 | `num` | string | auto | Display number |
| 2 | `id` | UUID | never | Primary key |
| 3 | `nombre` | string | yes | First name |
| 4 | `apellido` | string | yes | Last name |
| 5 | `email` | string | yes | |
| 6 | `telefono_movil` | string | yes | |
| 7 | `telefono_fijo` | string | yes | |
| 8 | `cargo` | string | yes | Job title |
| 9 | `organization_id` | UUID | yes | `organizations.id` |
| 10 | `origen` | string | yes | Lead source |
| 11 | `product_ids` | string | yes | Comma-separated `products.id` |
| 12 | `tipo` | string | yes | `proveedor`, `contacto`, `organización` |
| 13 | `estado` | string | yes | `activo`, `inactivo` |
| 14 | `prioridad` | string | yes | `alta`, `media`, `baja` |
| 15 | `fecha_registro` | datetime | auto | |
| 16 | `ultima_interaccion` | datetime | auto | |
| 17 | `notas` | string | yes | |
| 18 | `tags` | string | yes | |

## products.csv

| # | Field | Type | Mutable | Example |
|---|-------|------|---------|---------|
| 1 | `id` | UUID | never | |
| 2 | `num` | string | auto | |
| 3 | `nombre` | string | yes | `"Widget Pro"` |
| 4 | `categoria` | string | yes | `"electronics / widgets"` |
| 5 | `presentacion` | string | yes | `"box of 12"` |
| 6 | `volumen` | string | yes | `"1,000 units/month"` |
| 7 | `precio_ref` | string | yes | `"$14.99"` |
| 8 | `cobertura` | string | yes | `"nationwide"` |
| 9 | `flota` | string | yes | `"yes"` |
| 10 | `regulatorio` | string | yes | `"ISO 9001"` |
| 11 | `notas` | string | yes | |
| 12 | `tags` | string | yes | |

## Conventions

- `nombre` with parentheses `(Org Name)` signals organization-only contact (no person attached)
- Tags: comma-separated lowercase keywords for search
- Industry/category: use `/` for hierarchy, e.g. `"Technology / SaaS / CRM"`
- Phone format: `(label) number, (label2) number2`
