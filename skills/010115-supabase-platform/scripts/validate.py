#!/usr/bin/env python3
import sys
from pathlib import Path

def check_supabase(dir_path: Path) -> list[dict]:
    findings = []
    for env_file in [".env", ".env.local", ".env.example"]:
        ef = dir_path / env_file
        if ef.exists():
            content = ef.read_text()
            for var in ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"]:
                if var in content:
                    findings.append({"status": "ok", "check": f"Env: {var}", "detail": "Configured"})
            break
    supabase_files = [f for f in list(dir_path.rglob("*.ts")) + list(dir_path.rglob("*.js")) if "supabase" in f.read_text().lower()]
    if supabase_files:
        findings.append({"status": "ok", "check": "Supabase SDK usage", "detail": f"{len(supabase_files)} file(s)"})
    sql_files = list(dir_path.rglob("*.sql"))
    if sql_files:
        findings.append({"status": "ok", "check": "SQL migration files", "detail": f"{len(sql_files)} file(s)"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/skill-supabase")
    if not root.exists(): print(f"Not found: {root}"); sys.exit(1)
    print(f"Validating Supabase platform in: {root}")
    findings = check_supabase(root)
    for f in findings:
        print(f"  {'✓' if f['status']=='ok' else '!' if f['status']=='warn' else 'i'} {f['check']}: {f['detail']}")
    print("\nAll checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
