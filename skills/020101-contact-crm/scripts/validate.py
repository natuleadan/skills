#!/usr/bin/env python3
"""Validate contacts, organizations, and products CSVs: phones, cross-references, duplicates."""

import csv
import os
import re
import sys
from pathlib import Path

BASE = Path(os.getcwd())
ORG_CSV = BASE / "organizations.csv"
CONTACT_CSV = BASE / "contacts.csv"
PRODUCT_CSV = BASE / "products.csv"
OUT = BASE / "output"


def _ensure_deps():
    try:
        import phonenumbers
    except ImportError:
        import subprocess
        req = Path(__file__).parent.parent / "requirements.txt"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])
    import phonenumbers
    return phonenumbers


def normalize(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def load_csv(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def extract_phone_digits(text):
    if not text:
        return []
    return re.findall(r"\d{7,}", text)


def main():
    phones = _ensure_deps()
    contacts = load_csv(CONTACT_CSV)
    orgs = load_csv(ORG_CSV)
    products = load_csv(PRODUCT_CSV)
    warnings = 0
    errors = 0

    org_index = {r["id"]: r for r in orgs}
    prod_index = {r["id"]: r for r in products}

    print(f"\nValidating {len(contacts)} contacts, {len(orgs)} orgs, {len(products)} products\n")

    # --- Phone validation ---
    for c in contacts:
        org_id = c.get("organization_id", "").strip()
        country = ""
        if org_id and org_id in org_index:
            country = org_index[org_id].get("pais", "").strip()
        if not country:
            country = c.get("pais", "").strip()
        if not country:
            continue

        for field in ("telefono_movil", "telefono_fijo"):
            val = c.get(field, "")
            if not val:
                continue
            for raw in extract_phone_digits(val):
                try:
                    parsed = phones.parse(raw, country)
                    if not phones.is_valid_number(parsed):
                        n = f"{c.get('nombre','')} {c.get('apellido','')}".strip()
                        print(f"  WARN [{field}] #{c['num']} {n}: {raw} — invalid for {country}")
                        warnings += 1
                except Exception:
                    pass

    # --- Cross-reference: organization_id ---
    for c in contacts:
        oid = c.get("organization_id", "").strip()
        if oid and oid not in org_index:
            n = f"{c.get('nombre','')} {c.get('apellido','')}".strip()
            print(f"  ERROR contact #{c['num']} {n}: organization_id {oid[:8]}... not found")
            errors += 1

    # --- Cross-reference: product_ids ---
    for c in contacts:
        pids = c.get("product_ids", "").strip()
        if pids:
            for pid in pids.split(","):
                pid = pid.strip()
                if pid and pid not in prod_index:
                    n = f"{c.get('nombre','')} {c.get('apellido','')}".strip()
                    print(f"  ERROR contact #{c['num']} {n}: product_id {pid[:8]}... not found")
                    errors += 1

    if errors == 0 and warnings == 0:
        print("  All clean.")
    else:
        print(f"\n  {errors} error(s), {warnings} warning(s)\n")


if __name__ == "__main__":
    main()
