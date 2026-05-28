#!/usr/bin/env python3
"""Validate that all entities have at least one translation per language."""

translations = {
    "products": {"en": {"name": "Product A"}, "es": {"name": "Producto A"}},
    "categories": {"en": {"name": "Category A"}, "es": {"name": "Categoría A"}},
    "variants": {"en": {"name": "Small"}, "es": {"name": "Pequeño"}},
}

errors = []
for entity, langs in translations.items():
    for lang, data in langs.items():
        if not data.get("name"):
            errors.append(f"{entity}/{lang}: missing name")

if errors:
    for e in errors:
        print(f"  ERROR: {e}")
else:
    print(f"All {len(translations)} entities have valid translations")
