# Linking Guide

How the three entities connect via UUIDs.

## Relationship Chain

```
organizations.id ──→ contacts.organization_id ──→ contacts.product_ids ──→ products.id
```

**Organization** has many **Contacts** (1:N via `organization_id`)
**Contact** has many **Products** (N:N via `product_ids` — comma-separated UUIDs)

## Linking Rules

### Organization → Contact

```
organizations.csv:
  id: a1b2c3d4-...
  nombre: "Acme Corp"

contacts.csv:
  organization_id: a1b2c3d4-...  ← matches organizations.id
```

- A contact MUST have a valid `organization_id` (UUID from organizations.csv)
- An organization can have 0 or more contacts
- Deleting an organization should prompt removal of linked contacts

### Contact → Product

```
contacts.csv:
  product_ids: "x1y2z3-..., p4q5r6-..."

products.csv:
  id: x1y2z3-...  (Widget Pro)
  id: p4q5r6-...  (Service Plan)
```

- `product_ids` is a comma-separated string of UUIDs
- A contact can reference 0 or more products
- A product can be referenced by 0 or more contacts
- No cascade delete — removing a product leaves a dangling reference (detected by validation)

## Consistency Validation

Run `python scripts/validate.py` to check:

1. Every `organization_id` in contacts exists in organizations
2. Every UUID in `product_ids` exists in products
3. Phone numbers validated against country from linked organization

## Batch Operations

```python
# Link multiple products to a contact
python scripts/contacts.py update <num>
# At product_ids prompt: uuid1,uuid2,uuid3

# Find all contacts in an organization
python scripts/contacts.py search <org-name>

# List contacts with org name and products
python scripts/contacts.py list
```
