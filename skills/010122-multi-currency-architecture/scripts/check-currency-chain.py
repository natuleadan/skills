#!/usr/bin/env python3
"""Validate currency FK chain consistency."""

currencies = {"USD": "US", "EUR": "FR", "GBP": "GB", "BRL": "BR"}
countries = {"US": "United States", "FR": "France", "GB": "United Kingdom", "BR": "Brazil"}
taxes = {"US": {"name": "Sales Tax", "rate": 8.5}, "FR": {"name": "VAT", "rate": 20.0}}

errors = []
for code, country_code in currencies.items():
    if country_code not in countries:
        errors.append(f"{code}: country '{country_code}' not found")
    if country_code not in taxes:
        errors.append(f"{code}: no tax for country '{country_code}'")
    else:
        if taxes[country_code]["rate"] <= 0:
            errors.append(f"{code}: tax rate must be > 0")

if errors:
    for e in errors:
        print(f"  ERROR: {e}")
else:
    print(f"All {len(currencies)} currencies have valid FK chains")
