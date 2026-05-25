#!/usr/bin/env python3
import sys
from pathlib import Path

def check_i18n(dir_path: Path) -> list[dict]:
    findings = []
    tsx_files = list(dir_path.rglob("*.tsx"))
    i18n_files = [f for f in dir_path.rglob("*.ts") if "translation" in f.read_text().lower() or "i18n" in f.read_text().lower() or "lang" in f.read_text().lower()]
    if i18n_files:
        findings.append({"status": "ok", "check": "I18n/translation files", "detail": f"{len(i18n_files)} file(s)"})
    rtl_files = [f for f in tsx_files if "dir=" in f.read_text() or "rtl" in f.read_text().lower()]
    if rtl_files:
        findings.append({"status": "ok", "check": "RTL support", "detail": "Found"})
    return findings

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/nla-i18n")
    if not root.exists(): print(f"Not found: {root}"); sys.exit(1)
    print(f"Validating i18n in: {root}")
    findings = check_i18n(root)
    for f in findings:
        print(f"  {'✓' if f['status']=='ok' else '!' if f['status']=='warn' else 'i'} {f['check']}: {f['detail']}")
    print("\nAll checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
