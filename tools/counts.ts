#!/usr/bin/env node
// Counts skills, references and scripts, and keeps the README badges in sync.
// Usage: pnpm badges          write the badges
//        pnpm badges:check    fail when the badges are out of date
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");
const README = join(ROOT, "README.md");

type Metadata = { references?: string[] };

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.isFile()) out.push(full);
  }
  return out;
}

const skills = readdirSync(SKILLS, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .filter((name) => {
    try {
      readFileSync(join(SKILLS, name, "metadata.json"), "utf8");
      return true;
    } catch {
      return false;
    }
  })
  .sort();

let references = 0;
let scripts = 0;
for (const name of skills) {
  const metadata = JSON.parse(
    readFileSync(join(SKILLS, name, "metadata.json"), "utf8"),
  ) as Metadata;
  references += metadata.references?.length ?? 0;
  const scriptsDir = join(SKILLS, name, "scripts");
  try {
    scripts += walk(scriptsDir).filter((file) => /\.(ts|mjs)$/.test(file)).length;
  } catch {
    // A skill without scripts contributes zero.
  }
}

const counts = {
  skills: skills.length,
  references,
  scripts,
};

const badges = [
  `  <img src="https://img.shields.io/badge/Skills-${counts.skills}-8B5CF6?style=for-the-badge" alt="${counts.skills} skills" />`,
  `  <img src="https://img.shields.io/badge/References-${counts.references}-blue?style=for-the-badge" alt="${counts.references} references" />`,
  `  <img src="https://img.shields.io/badge/Scripts-${counts.scripts}-green?style=for-the-badge" alt="${counts.scripts} scripts" />`,
].join("\n");

const source = readFileSync(README, "utf8");
const block = /  <img src="https:\/\/img\.shields\.io\/badge\/Skills-\d+-8B5CF6[^>]*\/>\n  <img src="https:\/\/img\.shields\.io\/badge\/References-\d+-blue[^>]*\/>\n  <img src="https:\/\/img\.shields\.io\/badge\/Scripts-\d+-green[^>]*\/>/;
const next = source.replace(block, badges);

if (process.argv.includes("--check")) {
  if (next !== source) {
    console.error(
      `FAIL: README badges are out of date. Run pnpm badges. Expected ${counts.skills} skills, ${counts.references} references and ${counts.scripts} scripts.`,
    );
    process.exit(1);
  }
  console.log(
    `PASS: badges match ${counts.skills} skills, ${counts.references} references and ${counts.scripts} scripts.`,
  );
} else {
  writeFileSync(README, next);
  console.log(
    `Wrote badges: ${counts.skills} skills, ${counts.references} references and ${counts.scripts} scripts.`,
  );
}
