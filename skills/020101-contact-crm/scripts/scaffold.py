#!/usr/bin/env python3
"""Generate empty CSV files with correct headers for contact CRM."""

import os
import sys

ORG_FIELDS = [
    "id", "num", "nombre", "industria", "ruc", "direccion", "ciudad",
    "provincia", "codigo_postal", "pais", "website", "email", "telefono",
    "linkedin", "twitter", "notas", "tags",
]

CONTACT_FIELDS = [
    "num", "id", "nombre", "apellido", "email", "telefono_movil",
    "telefono_fijo", "cargo", "organization_id", "origen", "product_ids",
    "tipo", "estado", "prioridad", "fecha_registro", "ultima_interaccion",
    "notas", "tags",
]

PRODUCT_FIELDS = [
    "id", "num", "nombre", "categoria", "presentacion", "volumen",
    "precio_ref", "cobertura", "flota", "regulatorio", "notas", "tags",
]


def write_csv(path, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(",".join(fields) + "\n")
    print(f"  Created: {path}")


def main(target_dir=None):
    if target_dir is None:
        target_dir = os.getcwd()
    else:
        target_dir = os.path.abspath(target_dir)
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(os.path.join(target_dir, "output"), exist_ok=True)

    print(f"\nScaffolding contact CRM in: {target_dir}\n")
    write_csv(os.path.join(target_dir, "organizations.csv"), ORG_FIELDS)
    write_csv(os.path.join(target_dir, "contacts.csv"), CONTACT_FIELDS)
    write_csv(os.path.join(target_dir, "products.csv"), PRODUCT_FIELDS)
    output_dir = os.path.join(target_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nReady. Run scripts from {target_dir}\n")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target)
