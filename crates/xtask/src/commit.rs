//! Conventional commit message and author policy validator.

use std::fs;
use std::path::Path;
use std::process::{Command, ExitCode};

const TYPES: &[&str] = &[
    "feat", "fix", "upgrade", "docs", "style", "refactor", "perf", "test", "chore", "ci", "revert",
];
const SCOPES: &[&str] = &[
    "core", "api", "cli", "domain", "math", "tools", "ui", "config", "docs", "ci", "workflow", "hooks", "release", "license", "deps", "security",
];
// Organization noreply email domain enforced for all commits.
const NOREPLY_SUFFIX: &str = "@users.noreply.github.com";

pub(crate) fn validate_message(msg: &str) -> Result<(), String> {
    let normalized = msg.replace("\r\n", "\n");
    let trimmed = normalized.trim_end_matches('\n');
    let lines: Vec<&str> = trimmed.lines().collect();
    let Some(header) = lines.first().copied() else {
        return Err("empty commit message".to_string());
    };
    if header.starts_with("Merge ") || header.starts_with("Revert ") || trimmed.contains("dependabot[bot]") {
        return Ok(());
    }
    validate_header(header)?;
    validate_body(&lines[1..], trimmed)?;
    Ok(())
}

fn validate_header(header: &str) -> Result<(), String> {
    if header.len() > 100 {
        return Err(format!("header exceeds 100 chars ({})", header.len()));
    }
    if header.ends_with('.') {
        return Err("header must not end with a period".to_string());
    }
    let Some((prefix, desc)) = header.split_once(": ") else {
        return Err("header must match type(scope): description".to_string());
    };
    let Some((commit_type, scope_part)) = prefix.split_once('(') else {
        return Err("header missing scope in parentheses".to_string());
    };
    let Some(scope) = scope_part.strip_suffix(')') else {
        return Err("header scope must end with ')'".to_string());
    };
    if !TYPES.contains(&commit_type) {
        return Err(format!("invalid commit type '{commit_type}'"));
    }
    if !SCOPES.contains(&scope) {
        return Err(format!("invalid commit scope '{scope}'"));
    }
    let desc_words = desc.split_whitespace().count();
    if !(3..=6).contains(&desc_words) {
        return Err(format!(
            "description has {desc_words} words (expected 3..=6)"
        ));
    }
    Ok(())
}

fn validate_body(rest: &[&str], full: &str) -> Result<(), String> {
    let lower = full.to_ascii_lowercase();
    for forbidden in [
        "co-authored-by:",
        "signed-off-by:",
        "generated-by:",
        "assisted-by:",
    ] {
        if lower.contains(forbidden) {
            return Err(format!("forbidden trailer '{forbidden}' present"));
        }
    }
    if rest.is_empty() || !rest[0].is_empty() {
        return Err("expected a single blank line after header".to_string());
    }
    let body_lines: Vec<&str> = rest[1..]
        .iter()
        .copied()
        .filter(|line| !line.starts_with('#'))
        .collect();
    if body_lines.iter().any(|line| line.is_empty()) {
        return Err("body bullets must not contain blank lines".to_string());
    }
    if body_lines.len() < 3 {
        return Err(format!("body has {} bullets (minimum 3)", body_lines.len()));
    }
    for line in body_lines {
        let Some(after_dash) = line.strip_prefix("- **") else {
            return Err(format!("bullet must start with '- **Label**: ': {line}"));
        };
        let Some((_, text)) = after_dash.split_once("**: ") else {
            return Err(format!("bullet missing '**: ' separator: {line}"));
        };
        let words = text.split_whitespace().count();
        if !(3..=10).contains(&words) {
            return Err(format!(
                "bullet has {words} words (expected 3..=10): {line}"
            ));
        }
    }
    Ok(())
}

fn check_git_identity(root: &Path) -> Result<(), String> {
    let name = git_config(root, "user.name")?;
    let email = git_config(root, "user.email")?;
    if name.is_empty() {
        return Err("git user.name must be configured".to_string());
    }
    if !email.ends_with(NOREPLY_SUFFIX) {
        return Err(format!(
            "git user.email must end with '{NOREPLY_SUFFIX}', got '{email}'"
        ));
    }
    Ok(())
}

fn git_config(root: &Path, key: &str) -> Result<String, String> {
    let out = Command::new("git")
        .args(["config", key])
        .current_dir(root)
        .output()
        .map_err(|e| format!("failed to run git config: {e}"))?;
    Ok(String::from_utf8_lossy(&out.stdout).trim().to_string())
}

pub(crate) fn run(root: &Path, args: &[String]) -> ExitCode {
    if let Some(pos) = args.iter().position(|a| a == "--range") {
        let Some(range) = args.get(pos + 1) else {
            eprintln!("FAIL commit-check: missing range argument");
            return ExitCode::FAILURE;
        };
        let out = Command::new("git")
            .args(["rev-list", range])
            .current_dir(root)
            .output();
        let Ok(res) = out else {
            eprintln!("FAIL commit-check: could not list range {range}");
            return ExitCode::FAILURE;
        };
        let shas = String::from_utf8_lossy(&res.stdout);
        for sha in shas.lines().filter(|s| !s.is_empty()) {
            let msg_out = Command::new("git")
                .args(["log", "-1", "--format=%B", sha])
                .current_dir(root)
                .output();
            let Ok(mres) = msg_out else {
                eprintln!("FAIL commit-check: could not read {sha}");
                return ExitCode::FAILURE;
            };
            let msg = String::from_utf8_lossy(&mres.stdout);
            if let Err(err) = validate_message(&msg) {
                eprintln!("FAIL commit-check ({sha}): {err}");
                return ExitCode::FAILURE;
            }
        }
        println!("PASS commit-check");
        return ExitCode::SUCCESS;
    }

    let Some(file) = args.first() else {
        eprintln!("FAIL commit-check: pass <msg-file> or --range <rev-range>");
        return ExitCode::FAILURE;
    };
    if let Err(err) = check_git_identity(root) {
        eprintln!("FAIL commit-check: {err}");
        return ExitCode::FAILURE;
    }
    let Ok(msg) = fs::read_to_string(file) else {
        eprintln!("FAIL commit-check: cannot read {file}");
        return ExitCode::FAILURE;
    };
    if let Err(err) = validate_message(&msg) {
        eprintln!("FAIL commit-check: {err}");
        return ExitCode::FAILURE;
    }
    println!("PASS commit-check");
    ExitCode::SUCCESS
}

#[cfg(test)]
mod tests {
    use super::validate_message;

    #[test]
    fn accepts_valid_commit_message() {
        let msg = "feat(core): ship native skills core\n\
            \n\
            - **Core**: add clean workspace crate structure\n\
            - **Checks**: verify commit rules in pure Rust\n\
            - **Docs**: align guides with repository standards";
        assert!(validate_message(msg).is_ok());
    }

    #[test]
    fn rejects_double_blank_lines_and_excess_words() {
        let msg = "feat(core): this header has way too many words here\n\
            \n\
            - **Core**: valid bullet text here\n\n\
            - **Checks**: second valid bullet text\n\
            - **Docs**: third valid bullet text";
        assert!(validate_message(msg).is_err());
    }
}
