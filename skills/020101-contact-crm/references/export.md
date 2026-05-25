# Export Specifications

Auto-generated PDF and XLSX outputs.

## Trigger

Export runs automatically after every `add` or `update` in:

- `python scripts/organizations.py add|update`
- `python scripts/contacts.py add|update`
- `python scripts/products.py add|update`

Manual: `python scripts/export.py`

## Dependencies

Optional — only needed for export:

```bash
pip install reportlab openpyxl
```

Script auto-installs on first run if missing.

## Output Files

All files in `output/`:

| File | Content |
|---|---|
| `organizations.pdf` | Org table: #, Name, Industry, Country, Email, Phone, Website |
| `organizations.xlsx` | 15 columns with headers and totals row |
| `contacts.pdf` | Contact table: #, Name, Role, Email, Phone, Organization, Origin, City, Products |
| `contacts.xlsx` | 16 columns with resolved org name + product names |
| `products.pdf` | Product table: #, Name, Category, Presentation, Volume, Price, Coverage, Fleet, Regulatory, Notes |
| `products.xlsx` | 11 columns with headers and totals row |

## PDF Specs

- Landscape A4, 3mm margins, grey header bar
- 6pt font, edge-to-edge table, alternating row colors
- Products column shows first 2 product names + count if more

## XLSX Specs

- Blue header (#2F5496) with white text
- Last row: "TOTAL" with `=COUNTA()` formula
- Named sheets: "Organizations", "Contacts", "Products"

## Customizing Columns

Edit the header list in the corresponding `_pdf_*` or `_xlsx_all` function in `scripts/export.py`.
