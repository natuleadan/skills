#!/usr/bin/env node
// Rejects " - " (space hyphen space) in Markdown prose.
// Allowed: the copyright line "2023 - Present." in README files.
// List markers, tables, frontmatter, inline code and code fences are ignored.
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKIP_DIRS = new Set(["node_modules", ".git", "_old", "dist", ".changeset"]);

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.isFile() && entry.name.endsWith(".md")) out.push(full);
  }
  return out;
}

const findings: string[] = [];

for (const file of walk(ROOT)) {
  const lines = readFileSync(file, "utf8").split("\n");
  let inFence = false;
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;

    // The only allowed spaced hyphen.
    if (line.includes("2023 - Present.")) continue;

    // Ignore table separators such as | --- | or |:---|.
    if (/^\s*\|?[\s:|-]+\|?\s*$/.test(line) && line.includes("|")) {
      continue;
    }

    // Remove inline code spans before checking prose.
    let prose = line.replace(/`[^`]*`/g, "");

    // Remove blockquote and list markers at the start of the line.
    prose = prose.replace(/^(\s*(?:>\s*)*)([-*+]|\d+\.)\s+/, "$1");

    if (prose.includes(" - ")) {
      findings.push(`${relative(ROOT, file)}:${index + 1}: ${line.trim()}`);
    }
  }
}

if (findings.length > 0) {
  for (const finding of findings) console.error(`FAIL: ${finding}`);
  console.error(
    `\n${findings.length} spaced hyphen(s). Use a colon, comma or parentheses instead.`,
  );
  console.error("Allowed exception: 2023 - Present.");
  process.exit(1);
}

console.log("PASS: no spaced hyphens in Markdown prose.");
