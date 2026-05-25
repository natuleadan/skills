#!/usr/bin/env python3
"""Validate Better Auth configuration in a project."""
import sys
from pathlib import Path


def check_auth_config(dir_path: Path) -> list[dict]:
    findings = []

    # Check env vars in .env or .env.local
    for env_file in [".env", ".env.local", ".env.example"]:
        ef = dir_path / env_file
        if ef.exists():
            content = ef.read_text()
            checks = [
                ("BETTER_AUTH_SECRET", "Better Auth secret configured"),
                ("BETTER_AUTH_URL", "Better Auth URL configured"),
                ("NEXT_PUBLIC_APP_URL", "Public app URL configured"),
            ]
            for var, label in checks:
                if any(line.strip().startswith(var) for line in content.split("\n")):
                    findings.append({"status": "ok", "check": f"Env var: {var}", "detail": label})
            break

    src = dir_path / "src"

    # Auth config file
    auth_config = src / "lib" / "auth.ts"
    if not auth_config.exists():
        auth_config = src / "infrastructure" / "external" / "auth.ts"
    if auth_config.exists():
        findings.append({"status": "ok", "check": "Auth config file", "detail": str(auth_config.relative_to(dir_path))})
        content = auth_config.read_text()
        if "betterAuth(" in content:
            findings.append({"status": "ok", "check": "  betterAuth() instance", "detail": "Found"})
        if "emailAndPassword" in content:
            findings.append({"status": "ok", "check": "  emailAndPassword config", "detail": "Found"})
    else:
        findings.append({"status": "warn", "check": "Auth config file", "detail": "Not found in src/lib/ or src/infrastructure/external/"})

    # API route
    api_route = src / "app" / "api" / "auth" / "[...all]" / "route.ts"
    if api_route.exists():
        findings.append({"status": "ok", "check": "API route", "detail": "src/app/api/auth/[...all]/route.ts"})
        content = api_route.read_text()
        if "toNextJsHandler" in content:
            findings.append({"status": "ok", "check": "  toNextJsHandler()", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "API route", "detail": "src/app/api/auth/[...all]/route.ts not found"})

    # Auth client
    client_file = src / "lib" / "auth-client.ts"
    if client_file.exists():
        findings.append({"status": "ok", "check": "Auth client", "detail": "src/lib/auth-client.ts"})
        content = client_file.read_text()
        if "createAuthClient" in content:
            findings.append({"status": "ok", "check": "  createAuthClient()", "detail": "Found"})
        if "baseURL" in content:
            findings.append({"status": "ok", "check": "  baseURL configured", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "Auth client", "detail": "src/lib/auth-client.ts not found"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-dummy-auth")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating Better Auth configuration in: {root}")
    findings = check_auth_config(root)
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
