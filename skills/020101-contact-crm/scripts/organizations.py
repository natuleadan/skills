#!/usr/bin/env python3
"""CRUD for organizations — companies/entities that group contacts."""

import csv
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path

FIELDS = [
    "id", "num", "nombre", "industria", "ruc", "direccion", "ciudad",
    "provincia", "codigo_postal", "pais", "website", "email", "telefono",
    "linkedin", "twitter", "notas", "tags",
]

CSV_PATH = Path(os.getcwd()) / "organizations.csv"
SKIP_FIELDS = {"id", "num"}


def normalize(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def load():
    if not CSV_PATH.exists():
        print(f"  organizations.csv not found. Run scaffold.py first.")
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
    item = {"id": str(uuid.uuid4()), "num": str(next_num(data))}
    for f in FIELDS:
        if f not in SKIP_FIELDS:
            v = input(f"{f}: ").strip()
            if v:
                item[f] = v
            else:
                item[f] = ""
    data.append(item)
    save(data)
    print(f"  Organization #{item['num']}: {item.get('nombre', '')}")
    return item


def search_items(data, query):
    q = normalize(query)
    return [r for r in data if any(q in normalize(r.get(f, "")) for f in FIELDS)]


def list_items(data):
    print(f"\nOrganizations: {len(data)}\n")
    for r in data:
        print(f"  #{r['num']:>3s} {r['nombre'] or '(no name)':30s} | {r.get('industria', '') or '-'}")


def update_item(data, ident):
    for r in data:
        if r.get("num") == ident or r.get("id") == ident or normalize(r.get("email", "")) == normalize(ident):
            for f in FIELDS:
                if f in SKIP_FIELDS:
                    continue
                v = input(f"{f} [{r.get(f, '')}]: ").strip()
                if v:
                    r[f] = v
            save(data)
            print(f"  Organization #{r['num']} updated")
            return r
    print("  Not found.")
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python organizations.py add|list|search <query>|update <id|email>")
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
            print(f"  #{r['num']} {r.get('nombre', '')} | {r.get('industria', '')}")
    elif cmd == "update":
        if len(sys.argv) < 3:
            print("ID or email required")
            return
        update_item(data, sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
