#!/usr/bin/env python3
"""Validate Prisma database setup in a project."""
import sys
from pathlib import Path


def check_prisma(dir_path: Path) -> list[dict]:
    findings = []

    # Check prisma.config.ts
    prisma_config = dir_path / "prisma.config.ts"
    if prisma_config.exists():
        findings.append({"status": "ok", "check": "prisma.config.ts", "detail": "Found"})
        content = prisma_config.read_text()
        if "defineConfig" in content:
            findings.append({"status": "ok", "check": "  defineConfig()", "detail": "Found"})
        if "env(" in content and "DATABASE_URL" in content:
            findings.append({"status": "ok", "check": "  DATABASE_URL from env", "detail": "Configured"})
    else:
        findings.append({"status": "warn", "check": "prisma.config.ts", "detail": "Not found"})

    # Check schema.prisma
    schema = dir_path / "prisma" / "schema.prisma"
    if schema.exists():
        findings.append({"status": "ok", "check": "prisma/schema.prisma", "detail": "Found"})
        content = schema.read_text()
        if "prisma-client" in content:
            findings.append({"status": "ok", "check": "  prisma generator", "detail": "provider: prisma-client"})
        if "postgresql" in content:
            findings.append({"status": "ok", "check": "  PostgreSQL datasource", "detail": "Configured"})
        if "model User" in content:
            findings.append({"status": "ok", "check": "  Better Auth models", "detail": "User model found"})
    else:
        findings.append({"status": "warn", "check": "prisma/schema.prisma", "detail": "Not found"})

    # Check .env has DATABASE_URL
    for env_file in [".env", ".env.local", ".env.example"]:
        ef = dir_path / env_file
        if ef.exists() and "DATABASE_URL" in ef.read_text():
            findings.append({"status": "ok", "check": "DATABASE_URL in env", "detail": "Configured"})
            break

    # Check prisma client instantiation
    prisma_client_files = list(dir_path.rglob("prisma.ts"))
    if prisma_client_files:
        findings.append({"status": "ok", "check": "Prisma client file", "detail": str(prisma_client_files[0].relative_to(dir_path))})
        content = prisma_client_files[0].read_text()
        if "PrismaPg" in content:
            findings.append({"status": "ok", "check": "  PrismaPg adapter", "detail": "Found"})
        if "PrismaClient" in content:
            findings.append({"status": "ok", "check": "  PrismaClient", "detail": "Instantiated"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-prisma")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Prisma database setup in: {root}")
    findings = check_prisma(root)
    errors = 0
    for f in findings:
        icon = {"ok": "✓", "warn": "!", "info": "i"}.get(f["status"], "?")
        print(f"  {icon} {f['check']}: {f['detail']}")
        if f["status"] == "warn":
            errors += 1

    if errors:
        print(f"\n{errors} warning(s) found")
    else:
        print("\nAll checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
