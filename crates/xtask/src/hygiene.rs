//! Repository hygiene checks: line limits, pure-Rust tooling, shell syntax, and anti-leak rules.

use std::fs;
use std::path::Path;
use std::process::Command;

const MAX_LINES: usize = 500;
const SKIP_DIRS: &[&str] = &["target", ".git", "dist"];
const CHECK_EXTS: &[&str] = &["rs", "md", "sh", "toml", "yml", "yaml"];
const FORBIDDEN_FILES: &[&str] = &[
    "package.json",
    "pnpm-lock.yaml",
    "package-lock.json",
    ".prettierrc",
    ".prettierrc.json",
];

pub(crate) fn check(root: &Path) -> bool {
    let mut errors = Vec::new();
    for forbidden in FORBIDDEN_FILES {
        if root.join(forbidden).exists() {
            errors.push(format!("forbidden JS/Node artifact '{forbidden}' in Rust repo"));
        }
    }
    walk(root, root, &mut errors);
    if errors.is_empty() {
        println!("PASS hygiene");
        true
    } else {
        println!("FAIL hygiene");
        for err in errors {
            println!("  {err}");
        }
        false
    }
}

fn walk(root: &Path, dir: &Path, errors: &mut Vec<String>) {
    let Ok(entries) = fs::read_dir(dir) else {
        return;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        let name = entry.file_name();
        let name_str = name.to_string_lossy();
        if path.is_dir() {
            if !SKIP_DIRS.contains(&name_str.as_ref()) {
                walk(root, &path, errors);
            }
            continue;
        }
        let ext = path.extension().and_then(|e| e.to_str()).unwrap_or("");
        if !CHECK_EXTS.contains(&ext) {
            continue;
        }
        let Ok(content) = fs::read_to_string(&path) else {
            continue;
        };
        let rel = path.strip_prefix(root).unwrap_or(&path).display();
        let line_count = content.lines().count();
        if line_count > MAX_LINES {
            errors.push(format!("{rel} has {line_count} lines (max {MAX_LINES})"));
        }
        if name_str != "hygiene.rs" && content.contains("/Users/") {
            errors.push(format!("{rel} contains hardcoded '/Users/' path"));
        }
        if ext == "md" {
            check_md_hyphens(&rel.to_string(), &content, errors);
        }
        if ext == "sh" {
            check_shell_syntax(&path, &rel.to_string(), errors);
        }
    }
}

fn check_shell_syntax(path: &Path, rel: &str, errors: &mut Vec<String>) {
    let out = Command::new("sh").arg("-n").arg(path).output();
    if let Ok(res) = out
        && !res.status.success()
    {
        errors.push(format!("{rel} failed 'sh -n' syntax check"));
    }
}

fn check_md_hyphens(rel: &str, content: &str, errors: &mut Vec<String>) {
    let mut in_code = false;
    for (idx, line) in content.lines().enumerate() {
        if line.trim_start().starts_with("```") {
            in_code = !in_code;
            continue;
        }
        if in_code || line.starts_with("- ") || line.starts_with('|') {
            continue;
        }
        let sanitized = line.replace("2023 - Present", "2023PRESENT");
        if sanitized.contains(" - ") {
            errors.push(format!(
                "{rel}:{} contains spaced hyphen ' - ' in prose",
                idx + 1
            ));
        }
    }
}
