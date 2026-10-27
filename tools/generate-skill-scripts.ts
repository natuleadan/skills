#!/usr/bin/env node
// Generates skills/<name>/scripts/main.ts from tools/skill-script-template.txt.
// The generated script is self-contained: it does not read metadata.json at
// runtime because the skills installer does not copy that file.
// Usage: pnpm scripts:generate
//        pnpm scripts:generate --check
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");
const TEMPLATE = readFileSync(
  join(ROOT, "tools", "skill-script-template.txt"),
  "utf8",
);
const CHECK = process.argv.includes("--check");

type Metadata = {
  version?: string;
  abstract?: string;
  references?: string[];
};

const skills = readdirSync(SKILLS, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .filter((name) => existsSync(join(SKILLS, name, "metadata.json")))
  .sort();

if (skills.length === 0) {
  console.error("FAIL: no skills found");
  process.exit(1);
}

let changed = 0;
for (const name of skills) {
  const metaPath = join(SKILLS, name, "metadata.json");
  const metadata = JSON.parse(readFileSync(metaPath, "utf8")) as Metadata;
  const commands = (metadata.references ?? []).map((reference) =>
    reference.replace(/\.md$/, ""),
  );

  const content = TEMPLATE.replaceAll(
    "__NAME_LITERAL__",
    JSON.stringify(name),
  )
    .replaceAll("__VERSION_LITERAL__", JSON.stringify(metadata.version ?? ""))
    .replaceAll("__ABSTRACT_LITERAL__", JSON.stringify(metadata.abstract ?? ""))
    .replaceAll("__COMMANDS_LITERAL__", JSON.stringify(commands))
    .replaceAll("__NAME__", name);

  const target = join(SKILLS, name, "scripts", "main.ts");
  const current = existsSync(target) ? readFileSync(target, "utf8") : "";
  if (current === content) continue;
  if (CHECK) {
    console.error(`FAIL: skills/${name}/scripts/main.ts is out of date`);
    changed += 1;
    continue;
  }
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, content);
  console.log(`Wrote skills/${name}/scripts/main.ts`);
}

if (CHECK) {
  if (changed > 0) {
    console.error(
      `FAIL: ${changed} script(s) out of date. Run pnpm scripts:generate.`,
    );
    process.exit(1);
  }
  console.log(`PASS: ${skills.length} skill scripts are up to date.`);
} else {
  console.log(`Generated ${skills.length} skill scripts.`);
}
