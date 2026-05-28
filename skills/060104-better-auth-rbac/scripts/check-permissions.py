#!/usr/bin/env python3
"""Validate that all roles have consistent permissions (no undefined actions)."""
import sys

STATEMENTS = {
    "products": ["create", "read", "read_private", "read_confidential", "update",
                 "delete", "publish", "archive", "set_visibility", "softdelete"],
    "admin": ["manage_system"],
}

ROLES = {
    "admin": {"products": STATEMENTS["products"]},
    "products:editor": {"products": ["create", "read", "read_private", "update",
                                       "publish", "archive", "set_visibility", "softdelete"]},
    "products:operator": {"products": ["create", "read", "read_private", "update"]},
}

def validate():
    errors = []
    for role, perms in ROLES.items():
        for domain, actions in perms.items():
            if domain not in STATEMENTS:
                errors.append(f"{role}: unknown domain '{domain}'")
                continue
            for action in actions:
                if action not in STATEMENTS[domain]:
                    errors.append(f"{role}: undefined action '{action}' in domain '{domain}'")
    return errors

if __name__ == "__main__":
    errs = validate()
    if errs:
        for e in errs:
            print(f"  ERROR: {e}")
        sys.exit(1)
    print("All permissions valid")
