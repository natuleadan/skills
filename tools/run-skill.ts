#!/usr/bin/env node
// Runs skills/<name>/scripts/main.ts with node.
// Usage: pnpm skill <name> [args...]
// The script runs with the skill directory as its working directory.
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const NAME = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const [name, ...args] = process.argv.slice(2);

if (!name || !NAME.test(name)) {
  console.error("Usage: pnpm skill <skill-name> [args...]");
  process.exit(2);
}

const skillDir = join(ROOT, "skills", name);
if (!existsSync(skillDir)) {
  console.error(`ERROR: unknown skill '${name}'`);
  process.exit(2);
}

const script = join(skillDir, "scripts", "main.ts");
if (!existsSync(script)) {
  console.error(`ERROR: skill '${name}' has no scripts/main.ts`);
  process.exit(2);
}

const result = spawnSync(process.execPath, [script, ...args], {
  cwd: skillDir,
  stdio: "inherit",
});

if (result.error) {
  console.error(`ERROR: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
