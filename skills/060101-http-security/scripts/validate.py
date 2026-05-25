#!/usr/bin/env python3
"""Validate security configuration in a project."""
import sys
from pathlib import Path


def check_security(dir_path: Path) -> list[dict]:
    findings = []

    # Check for security headers in proxy/middleware
    for proxy_file in ["proxy.ts", "middleware.ts", "middleware.js"]:
        pf = dir_path / proxy_file
        if pf.exists():
            findings.append({"status": "ok", "check": f"{proxy_file} found", "detail": "Exists"})
            content = pf.read_text()
            for header in ["X-Content-Type-Options", "X-Frame-Options", "Strict-Transport-Security",
                           "X-XSS-Protection", "Referrer-Policy", "Permissions-Policy"]:
                if header in content:
                    findings.append({"status": "ok", "check": f"  Security header: {header}", "detail": "Found"})
            if "CSP" in content or "Content-Security-Policy" in content:
                findings.append({"status": "ok", "check": "  CSP configuration", "detail": "Found"})
            else:
                findings.append({"status": "info", "check": "  CSP configuration", "detail": "Not found"})
            if "ratelimit" in content.lower():
                findings.append({"status": "ok", "check": "  Rate limiting", "detail": "Found"})
            break

    # CORS config
    cors_files = list(dir_path.rglob("*.ts"))
    cors_found = False
    for f in cors_files:
        if "cors(" in f.read_text() and "origin" in f.read_text():
            cors_found = True
            break
    if cors_found:
        findings.append({"status": "ok", "check": "CORS configuration", "detail": "Found"})
    else:
        findings.append({"status": "info", "check": "CORS configuration", "detail": "Not found"})

    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-dummy")
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    print(f"Validating security patterns in: {root}")
    findings = check_security(root)
    errors = 0
    for f in findings:
        icon = {"ok": "\u2713", "warn": "!", "info": "i"}.get(f["status"], "?")
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
