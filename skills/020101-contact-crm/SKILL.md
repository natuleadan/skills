---
name: 020101-contact-crm
license: MIT
compatibility: Requires Python 3.8+ with pandas
description: "Pattern for building a contact-product-organization database using CSV files with UUID-based relational linking. Use this skill whenever the user needs to manage business contacts, suppliers, organizations, and products with a lightweight relational pattern using only CSV files (no SQL database), implement phone validation (via phonenumbers), validate cross-CSV references (organization_id, product_ids), detect fuzzy duplicates, or auto-export to PDF and XLSX. Also trigger when the user asks for a CRM in Python, contact management system, product catalog linked to contacts, or organization hierarchy with multiple contacts per org. Do NOT trigger for general database design unrelated to CSV contact management."
---

# Contact CRM

This skill provides a complete contact-product-organization management system using CSV files with relational linking via UUIDs. Three normalized entities with auto-export to PDF and XLSX.

## Data model

```
Organization ──1:N──→ Contact ──N:N──→ Product
```

- **Organization**: company or entity with address, industry, tax info
- **Contact**: person linked to one organization
- **Product**: catalog item referenced by contacts via `product_ids`

## When to install dependencies

If you only need the CSV schema or pattern, no installation needed. If you need validation, CRUD operations, or export, install dependencies:

```bash
pip install -r requirements.txt
```

Scripts auto-detect missing dependencies and install them on first run.

## How to use this skill

1. **Scaffold**: `python scripts/scaffold.py` — generates empty CSVs with correct headers
2. **Organizations**: `python scripts/organizations.py add|list|search|update`
3. **Contacts**: `python scripts/contacts.py add|list|search|update`
4. **Products**: `python scripts/products.py add|list|search|update`
5. **Validate**: `python scripts/validate.py` — checks phone numbers + cross-CSV references
6. **Export**: `python scripts/export.py` — generates PDF and XLSX

All CRUD operations auto-trigger export after every save.

## Quick reference

```bash
# Scaffold empty CSVs
python scripts/scaffold.py

# Create an organization
python scripts/organizations.py add

# Create a contact (note the org UUID from previous step)
python scripts/contacts.py add

# Create a product (note the product UUID)
python scripts/products.py add

# Link product to contact via update
python scripts/contacts.py update <contact-num>

# Validate everything
python scripts/validate.py

# Export to PDF + XLSX
python scripts/export.py
```

## References

- `references/schema.md` — Full schema for all three CSVs
- `references/linking.md` — UUID-based cross-CSV linking, consistency rules
- `references/validation.md` — Phone validation, fuzzy duplicate detection
- `references/export.md` — PDF and XLSX output specifications
