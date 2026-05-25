#!/usr/bin/env python3
"""CRUD for products — standalone catalog referenced by contacts via product_ids."""

import csv
import os
import re
import sys
import uuid
from pathlib import Path

FIELDS = [
    "id", "num", "nombre", "categoria", "presentacion", "volumen",
    "precio_ref", "cobertura", "flota", "regulatorio", "notas", "tags",
]

CSV_PATH = Path(os.getcwd()) / "products.csv"
SKIP_FIELDS = {"id", "num"}


def normalize(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).lower().strip())


def load():
    if not CSV_PATH.exists():
        print(f"  products.csv not found. Run scaffold.py first.")
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
    print(f"  Product #{item['num']}: {item.get('nombre', '')}")
    return item


def search_items(data, query):
    q = normalize(query)
    return [r for r in data if any(q in normalize(r.get(f, "")) for f in FIELDS)]


def list_items(data):
    print(f"\nProducts: {len(data)}\n")
    for r in data:
        print(f"  #{r['num']:>3s} {r['nombre']:30s} | {r.get('categoria', ''):20s} | {r.get('precio_ref', '') or '-'}")


def update_item(data, ident):
    for r in data:
        if r.get("num") == ident or r.get("id") == ident:
            for f in FIELDS:
                if f in SKIP_FIELDS:
                    continue
                v = input(f"{f} [{r.get(f, '')}]: ").strip()
                if v:
                    r[f] = v
            save(data)
            print(f"  Product #{r['num']} updated")
            return r
    print("  Not found.")
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python products.py add|list|search <query>|update <num|id>")
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
            print(f"  #{r['num']} {r['nombre']} | {r.get('categoria', '')} | {r.get('precio_ref', '')}")
    elif cmd == "update":
        if len(sys.argv) < 3:
            print("ID required")
            return
        update_item(data, sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
