#!/usr/bin/env python3
"""CRUD for contacts — linked to one organization, may reference multiple products."""

import csv
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path

FIELDS = [
    "num", "id", "nombre", "apellido", "email", "telefono_movil",
    "telefono_fijo", "cargo", "organization_id", "origen", "product_ids",
    "tipo", "estado", "prioridad", "fecha_registro", "ultima_interaccion",
    "notas", "tags",
]

CSV_PATH = Path(os.getcwd()) / "contacts.csv"
SKIP_FIELDS = {"id", "num", "fecha_registro", "ultima_interaccion"}


def normalize(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def load():
    if not CSV_PATH.exists():
        print(f"  contacts.csv not found. Run scaffold.py first.")
        return []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(data):
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(data)
    _auto_export()


def _auto_export():
    try:
        from export import run_all
        run_all()
    except Exception:
        pass


def next_num(data):
    if not data:
        return 1
    return max(int(r.get("num", 0) or 0) for r in data) + 1


def add_item(data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item = {
        "id": str(uuid.uuid4()),
        "num": str(next_num(data)),
        "fecha_registro": now,
        "ultima_interaccion": now,
        "estado": "activo",
        "prioridad": "media",
    }
    for f in FIELDS:
        if f in SKIP_FIELDS:
            continue
        v = input(f"{f}: ").strip()
        if v:
            item[f] = v
    for f in FIELDS:
        if f not in item:
            item[f] = ""
    data.append(item)
    save(data)
    name = f"{item.get('nombre', '')} {item.get('apellido', '')}".strip()
    print(f"  Contact #{item['num']}: {name or '(org)'}")
    return item


def search_items(data, query):
    q = normalize(query)
    return [r for r in data if any(q in normalize(r.get(f, "")) for f in FIELDS)]


def list_items(data):
    orgs = _load_orgs()
    prods = _load_prods()
    print(f"\nContacts: {len(data)}\n")
    for r in data:
        name = f"{r.get('nombre', '') or '(org)'} {r.get('apellido', '')}".strip()
        org_name = orgs.get(r.get("organization_id", ""), "")
        pids = r.get("product_ids", "")
        prod_names = []
        if pids:
            for pid in pids.split(","):
                pid = pid.strip()
                if pid in prods:
                    prod_names.append(prods[pid])
        print(f"  #{r['num']:>3s} {name:25s} | {r.get('email', ''):25s} | {org_name or '-'}")
        if prod_names:
            print(f"       Products: {', '.join(prod_names)}")


def _load_orgs():
    p = Path(os.getcwd()) / "organizations.csv"
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return {r["id"]: r.get("nombre", "") for r in csv.DictReader(f)}


def _load_prods():
    p = Path(os.getcwd()) / "products.csv"
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return {r["id"]: r.get("nombre", "") for r in csv.DictReader(f)}


def update_item(data, ident):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for r in data:
        if r.get("num") == ident or r.get("id") == ident or normalize(r.get("email", "")) == normalize(ident):
            for f in FIELDS:
                if f in SKIP_FIELDS:
                    continue
                v = input(f"{f} [{r.get(f, '')}]: ").strip()
                if v:
                    r[f] = v
            r["ultima_interaccion"] = now
            save(data)
            print(f"  Contact #{r['num']} updated")
            return r
    print("  Not found.")
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python contacts.py add|list|search <query>|update <id|email>")
        return
    cmd = sys.argv[1]
    data = load()
    if cmd == "add":
        add_item(data)
    elif cmd == "list":
        list_items(data)
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Query required")
            return
        results = search_items(data, " ".join(sys.argv[2:]))
        for r in results:
            name = f"{r.get('nombre', '') or '(org)'} {r.get('apellido', '')}".strip()
            print(f"  #{r['num']} {name} | {r.get('email', '')}")
    elif cmd == "update":
        if len(sys.argv) < 3:
            print("ID or email required")
            return
        update_item(data, sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
