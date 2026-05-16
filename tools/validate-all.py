#!/usr/bin/env python3
"""validate-all.py — Validate all registered skills against the Agent Skills format."""

import json
import re
import sys
import unicodedata
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

ALLOWED_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
    "user-invocable",
    "argument-hint",
}


def load_marketplace() -> dict:
    if not MARKETPLACE.exists():
        print(f"  marketplace.json not found at {MARKETPLACE}")
        sys.exit(1)
    return json.loads(MARKETPLACE.read_text())


def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter into a flat dict.

    Handles top-level key:value pairs and a single-level nested metadata: block.
    """
    result = {}
    lines = text.split("\n")
    current_key = None
    current_val_parts = []
    metadata_lines = []
    in_metadata = False

    for line in lines:
        stripped = line.rstrip()

        if in_metadata:
            if stripped == "" or not stripped[0].isspace():
                in_metadata = False
                if metadata_lines:
                    meta = {}
                    for ml in metadata_lines:
                        m = re.match(r"^\s+(\S+):\s*(.*)", ml)
                        if m:
                            meta[m.group(1)] = m.group(2)
                    result[current_key] = meta
                    metadata_lines = []
                current_key = None
                current_val_parts = []
            else:
                metadata_lines.append(stripped)
                continue

        m = re.match(r"^(\S[\w-]*):\s*(.*)", stripped)
        if m:
            if current_key is not None:
                val = " ".join(v.rstrip() for v in current_val_parts).strip()
                result[current_key] = val

            new_key = m.group(1)
            val_part = m.group(2)

            if new_key == "metadata":
                current_key = new_key
                current_val_parts = []
                if val_part.strip():
                    metadata_lines = []
                    in_metadata = False
                    meta = {}
                    meta_line = re.match(r"\{(.+)\}", val_part.strip())
                    if meta_line:
                        for pair in meta_line.group(1).split(","):
                            kv = pair.split(":", 1)
                            if len(kv) == 2:
                                meta[kv[0].strip()] = kv[1].strip()
                    else:
                        meta[val_part.strip()] = ""
                    result[new_key] = meta
                else:
                    in_metadata = True
                    metadata_lines = []
                continue

            current_key = new_key
            current_val_parts = [val_part] if val_part else []
            continue

        if current_key is not None:
            current_val_parts.append(stripped)

    if current_key is not None:
        if in_metadata and metadata_lines:
            meta = {}
            for ml in metadata_lines:
                m = re.match(r"^\s+(\S+):\s*(.*)", ml)
                if m:
                    meta[m.group(1)] = m.group(2)
            result[current_key] = meta
        else:
            val = " ".join(v.rstrip() for v in current_val_parts).strip()
            result[current_key] = val

    return result


def check_name(name, skill_dir):
    errs = []

    if not name or not isinstance(name, str) or not name.strip():
        errs.append("Field 'name' must be a non-empty string")
        return errs

    name = unicodedata.normalize("NFKC", name.strip())

    if len(name) > 64:
        errs.append(f"Skill name exceeds 64 character limit ({len(name)} chars): {name}")

    if name != name.lower():
        errs.append(f"Skill name must be lowercase: {name}")

    if name.startswith("-") or name.endswith("-"):
        errs.append("Skill name cannot start or end with a hyphen")

    if "--" in name:
        errs.append("Skill name cannot contain consecutive hyphens")

    for c in name:
        if not (c.isalpha() or c.isdigit() or c == "-"):
            errs.append(f"Skill name contains invalid character '{c}'. Only letters, digits, and hyphens allowed: {name}")
            break

    dir_name = unicodedata.normalize("NFKC", skill_dir.name)
    if dir_name != name:
        errs.append(f"Directory name '{skill_dir.name}' must match skill name '{name}'")

    return errs


def check_description(value, raw_line=None):
    errs = []
    if not value or not isinstance(value, str) or not value.strip():
        errs.append("Field 'description' must be a non-empty string")
        return errs
    if len(value) > 1024:
        errs.append(f"Description exceeds 1024 character limit ({len(value)} chars)")
    if raw_line and ": " in raw_line:
        val_part = raw_line.split(":", 1)[1].strip()
        is_quoted = val_part.startswith('"') or val_part.startswith("'")
        if not is_quoted and ": " in value:
            errs.append("Description contains ': ' — must be quoted in YAML frontmatter to avoid parser issues")
    return errs


def check_compatibility(value):
    errs = []
    if not isinstance(value, str):
        errs.append("Field 'compatibility' must be a string")
        return errs
    if len(value) > 500:
        errs.append(f"Compatibility exceeds 500 character limit ({len(value)} chars)")
    return errs


def validate_skill(path_str):
    results = []
    skill_dir = (REPO_ROOT / path_str).resolve()

    if not skill_dir.exists():
        results.append({"type": "error", "msg": f"Directory not found: {skill_dir}"})
        return results

    sk = skill_dir / "SKILL.md"
    if not sk.exists():
        results.append({"type": "error", "msg": f"Missing required file: SKILL.md in {skill_dir}"})
        return results

    content = sk.read_text()

    if not content.startswith("---"):
        results.append({"type": "error", "msg": f"SKILL.md must start with YAML frontmatter (---) in {sk}"})
        return results

    parts = content.split("---", 2)
    if len(parts) < 3:
        results.append({"type": "error", "msg": f"Frontmatter not properly closed with --- in {sk}"})
        return results

    metadata = parse_frontmatter(parts[1])

    if not isinstance(metadata, dict) or not metadata:
        results.append({"type": "error", "msg": f"Frontmatter must contain key-value pairs in {sk}"})
        return results

    unknown = set(metadata.keys()) - ALLOWED_FIELDS
    if unknown:
        results.append({"type": "error", "msg": f"Unexpected frontmatter fields: {', '.join(sorted(unknown))}. Allowed: {sorted(ALLOWED_FIELDS)}"})

    name = metadata.get("name")
    if name is None:
        results.append({"type": "error", "msg": f"Missing required field 'name' in {sk}"})
    else:
        for e in check_name(name, skill_dir):
            results.append({"type": "error", "msg": e})

    desc = metadata.get("description")
    if desc is None:
        results.append({"type": "error", "msg": f"Missing required field 'description' in {sk}"})
    else:
        raw_desc = ""
        for line in parts[1].split("\n"):
            if line.strip().startswith("description:"):
                raw_desc = line
                break
        for e in check_description(desc, raw_desc):
            results.append({"type": "error", "msg": e})

    compat = metadata.get("compatibility")
    if compat is not None:
        for e in check_compatibility(compat):
            results.append({"type": "error", "msg": e})

    meta_file = skill_dir / "metadata.json"
    if not meta_file.exists():
        results.append({"type": "error", "msg": f"Missing required file: metadata.json in {skill_dir}"})
    else:
        try:
            meta_data = json.loads(meta_file.read_text())
            if not isinstance(meta_data, dict):
                results.append({"type": "error", "msg": f"metadata.json must contain a JSON object in {skill_dir}"})
            else:
                if "version" not in meta_data:
                    results.append({"type": "error", "msg": f"metadata.json missing required field 'version' in {skill_dir}"})
                if "abstract" not in meta_data:
                    results.append({"type": "error", "msg": f"metadata.json missing required field 'abstract' in {skill_dir}"})
                if "references" not in meta_data:
                    results.append({"type": "error", "msg": f"metadata.json missing required field 'references' in {skill_dir}"})
                elif not isinstance(meta_data["references"], list):
                    results.append({"type": "error", "msg": f"metadata.json 'references' must be an array in {skill_dir}"})
        except json.JSONDecodeError:
            results.append({"type": "error", "msg": f"metadata.json is not valid JSON in {skill_dir}"})

    refs_dir = skill_dir / "references"
    if refs_dir.exists():
        for f in refs_dir.iterdir():
            if f.suffix == ".md" and f.stat().st_size == 0:
                results.append({"type": "warning", "msg": f"Empty reference file: {f}"})

    scripts_dir = skill_dir / "scripts"
    py_files = list(scripts_dir.glob("*.py")) if scripts_dir.exists() else []
    if not py_files:
        results.append({"type": "warning", "msg": f"No Python scripts in {scripts_dir} — every skill should have at least one .py"})

    return results


def main():
    print("=== Skills Validation ===")
    print()

    data = load_marketplace()

    all_errors = []
    all_warnings = []
    skill_count = 0

    for plugin in data.get("plugins", []):
        sources = [REPO_ROOT / (plugin.get("source") or ".")]
        explicit = plugin.get("skills", [])
        if explicit:
            skill_paths = explicit
        else:
            skill_paths = []
            for src in sources:
                src = src.resolve()
                for f in sorted(src.rglob("SKILL.md")):
                    parent = f.parent
                    rel = parent.relative_to(REPO_ROOT)
                    parts = rel.parts
                    if any(p.startswith(".") or p in ("node_modules", ".husky", "_") for p in parts):
                        continue
                    skill_paths.append(f"./{rel}")

        for skill_path in skill_paths:
            skill_count += 1
            print(f"--- {skill_path} ---")
            results = validate_skill(skill_path)
            if not results:
                print("  Valid")
            else:
                for r in results:
                    icon = "  !" if r["type"] == "warning" else "  X"
                    print(f"{icon} {r['msg']}")
                    if r["type"] == "error":
                        all_errors.append(r)
                    else:
                        all_warnings.append(r)
            print()

    if skill_count == 0:
        print("No skills found in marketplace.json")
        sys.exit(1)

    print(f"Results: {len(all_errors)} error(s), {len(all_warnings)} warning(s) across {skill_count} skill(s)")
    print()

    if all_errors:
        sys.exit(1)

    if all_warnings:
        print("All skills pass. Review warnings for optional improvements.")
        sys.exit(0)

    print("All skills pass.")
    sys.exit(0)


if __name__ == "__main__":
    main()
