# Validation Rules

Phone validation and duplicate detection for the contact CRM.

## Phone Validation

Uses the `phonenumbers` library. Country is resolved from the contact's linked organization:

```
contact.organization_id → lookup organization.pais
```

- If `pais` is empty → **skip** phone validation for that contact
- If `pais` has a value → validate using that country code
- Validated fields: `telefono_movil`, `telefono_fijo`
- Multi-number strings supported: `(label1) num1, (label2) num2`

## Cross-CSV Consistency

| Check | Rule |
|---|---|
| `organization_id` | Must exist in `organizations.id` |
| `product_ids` | Every UUID must exist in `products.id` |

Broken references are reported as errors (not warnings).

## Fuzzy Duplicate Detection

When adding a contact via `contacts.py add`:

| Criterion | Weight | Match |
|---|---|---|
| Email | 100% | Exact (case-insensitive) |
| Phone | 90% | Exact (normalized digits) |
| Name | 80% | Partial substring (A in B) |
| Organization | 70% | Partial org name match |

If any match scores ≥ 70, the script prompts for confirmation.

## Running Validation

```bash
python scripts/validate.py
```

Output:
```
Validating 42 contacts, 15 orgs, 108 products

  WARN [telefono_movil] #12 Jane Doe: 12345 — invalid for US
  ERROR contact #7 Acme Corp: organization_id not found

  1 error(s), 1 warning(s)
```
