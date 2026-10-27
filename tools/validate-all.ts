#!/usr/bin/env node
/**
 * Validate every skill in skills/ and the repository metadata.
 *
 * Rules:
 * - each skill has SKILL.md with frontmatter `name` and `description`
 * - each skill has metadata.json with `version`, `abstract`, `references`
 * - every declared reference exists in references/ and has a mermaid diagram
 * - SKILL.md and references stay under 300 lines
 * - no fenced code blocks in any .md file; only mermaid is allowed
 * - no code/ directory, no executable files, no Python under skills/ or tools/
 * - scripts/ only holds .ts or .mjs files and starts at main.ts
 * - every skill is registered in marketplace.json and plugin.json
 * - license and version are consistent across package.json and .claude-plugin
 */
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS = join(ROOT, "skills");
const FRONTMATTER = /^---\s*\n([\s\S]*?)\n---\s*\n/;
const SKIP_DIRS = new Set(["node_modules", ".git", ".changeset", "_old", "dist"]);

type Metadata = {
  version?: string;
  abstract?: string;
  references?: string[];
};

type Catalog = {
  metadata?: { version?: string };
  plugins?: Array<{ version?: string; license?: string; skills?: string[] }>;
};

type Plugin = {
  version?: string;
  license?: string;
  skills?: string[];
};

function walk(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_DIRS.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full));
    else if (entry.isFile()) out.push(full);
  }
  return out;
}

function lineCount(text: string): number {
  const lines = text.split("\n");
  return text.endsWith("\n") ? lines.length - 1 : lines.length;
}

function readFrontmatter(text: string): Record<string, string> | null {
  const match = text.match(FRONTMATTER);
  if (!match) return null;
  const data: Record<string, string> = {};
  for (const line of match[1].split("\n")) {
    const index = line.indexOf(":");
    if (index === -1) continue;
    const key = line.slice(0, index).trim();
    const value = line.slice(index + 1).trim().replace(/^"|"$/g, "");
    data[key] = value;
  }
  return data;
}

function readJson<T>(path: string, label: string): T | null {
  try {
    return JSON.parse(readFileSync(path, "utf8")) as T;
  } catch (error) {
    errors.push(`${label} invalid (${String(error)})`);
    return null;
  }
}

const errors: string[] = [];

if (!existsSync(SKILLS)) {
  console.error("ERROR: no skills directory");
  process.exit(1);
}

const skills = readdirSync(SKILLS, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name)
  .sort();

if (skills.length === 0) {
  console.error("ERROR: no skills found");
  process.exit(1);
}

for (const name of skills) {
  const skill = join(SKILLS, name);

  const skillMd = join(skill, "SKILL.md");
  if (!existsSync(skillMd)) {
    errors.push(`${name}: missing SKILL.md`);
  } else {
    const fm = readFrontmatter(readFileSync(skillMd, "utf8"));
    if (!fm) {
      errors.push(`${name}: SKILL.md has no frontmatter`);
    } else {
      for (const key of ["name", "description"]) {
        if (!fm[key]) errors.push(`${name}: SKILL.md missing '${key}'`);
      }
      if (fm.name !== name) {
        errors.push(`${name}: frontmatter name '${fm.name}' != folder`);
      }
    }
  }

  const metaPath = join(skill, "metadata.json");
  if (!existsSync(metaPath)) {
    errors.push(`${name}: missing metadata.json`);
  } else {
    const metadata = readJson<Metadata>(metaPath, `${name}: metadata.json`);
    if (metadata) {
      for (const key of ["version", "abstract"] as const) {
        if (!metadata[key]) {
          errors.push(`${name}: metadata.json missing '${key}'`);
        }
      }
      if ((metadata.abstract ?? "").length > 200) {
        errors.push(`${name}: metadata.json abstract over 200 characters`);
      }
      if (metadata.references === undefined) {
        errors.push(`${name}: metadata.json missing 'references'`);
      } else {
        for (const reference of metadata.references) {
          const refPath = join(skill, "references", reference);
          if (!existsSync(refPath)) {
            errors.push(`${name}: missing reference '${reference}'`);
            continue;
          }
          const text = readFileSync(refPath, "utf8");
          if (!text.includes("```mermaid") || !text.includes("sequenceDiagram")) {
            errors.push(
              `${name}: reference '${reference}' needs a mermaid sequenceDiagram`,
            );
          }
        }
      }
    }
  }

  const mdFiles = walk(skill).filter((file) => file.endsWith(".md"));
  for (const file of mdFiles) {
    const text = readFileSync(file, "utf8");
    const lines = lineCount(text);
    if (lines > 300) {
      errors.push(
        `${name}: ${relative(skill, file)} has ${lines} lines (max 300)`,
      );
    }
    for (const match of text.matchAll(/```(\w+)/g)) {
      if (match[1] !== "mermaid") {
        errors.push(
          `${name}: non-mermaid code block in ${relative(skill, file)} (only mermaid is allowed)`,
        );
      }
    }
  }

  if (existsSync(join(skill, "code"))) {
    errors.push(`${name}: code/ directory is not allowed in skills`);
  }

  const scriptsDir = join(skill, "scripts");
  if (existsSync(scriptsDir)) {
    if (!existsSync(join(scriptsDir, "main.ts"))) {
      errors.push(`${name}: scripts/ requires main.ts as the entry point`);
    }
    for (const file of walk(scriptsDir)) {
      const rel = relative(skill, file);
      if (!/\.(ts|mjs)$/.test(file)) {
        errors.push(`${name}: scripts/ only allows .ts or .mjs (${rel})`);
      }
      if (statSync(file).size === 0) {
        errors.push(`${name}: empty script file (${rel})`);
      }
    }
  }

  for (const file of walk(skill)) {
    if ((statSync(file).mode & 0o111) !== 0) {
      errors.push(
        `${name}: executable file not allowed (${relative(skill, file)})`,
      );
    }
    if (file.endsWith(".py")) {
      errors.push(`${name}: Python is not allowed (${relative(skill, file)})`);
    }
  }
}

// Root markdown: same rule as skills, no code blocks except mermaid.
for (const file of walk(ROOT).filter((path) => path.endsWith(".md"))) {
  if (file.startsWith(SKILLS)) continue;
  const text = readFileSync(file, "utf8");
  for (const match of text.matchAll(/```(\w+)/g)) {
    if (match[1] !== "mermaid") {
      errors.push(
        `${relative(ROOT, file)}: non-mermaid code block (only mermaid is allowed)`,
      );
    }
  }
}

// Tooling stays in Node.
for (const file of walk(join(ROOT, "tools"))) {
  if (file.endsWith(".py")) {
    errors.push(`tools: Python is not allowed (${relative(ROOT, file)})`);
  }
}

const marketplacePath = join(ROOT, ".claude-plugin", "marketplace.json");
const pluginPath = join(ROOT, ".claude-plugin", "plugin.json");
const packagePath = join(ROOT, "package.json");

const packageJson = readJson<{ version?: string; license?: string }>(
  packagePath,
  "package.json",
);
const catalog = readJson<Catalog>(marketplacePath, "marketplace.json");
const plugin = readJson<Plugin>(pluginPath, "plugin.json");

const catalogSkills =
  catalog?.plugins?.flatMap((entry) => entry.skills ?? []) ?? [];
for (const entry of catalogSkills) {
  if (!existsSync(join(ROOT, entry))) {
    errors.push(`marketplace.json: missing path '${entry}'`);
  }
}

const normalize = (path: string) => path.replace(/^\.\//, "").replace(/\/$/, "");
const registered = new Set(catalogSkills.map(normalize));
for (const name of skills) {
  if (!registered.has(`skills/${name}`)) {
    errors.push(`marketplace.json: skill '${name}' is not registered`);
  }
}
if (registered.size !== skills.length) {
  errors.push(
    `marketplace.json: ${registered.size} paths for ${skills.length} skills`,
  );
}

const pluginSkills = new Set((plugin?.skills ?? []).map(normalize));
for (const name of skills) {
  if (!pluginSkills.has(`skills/${name}`)) {
    errors.push(`plugin.json: skill '${name}' is not registered`);
  }
}

if (packageJson?.license !== "Apache-2.0") {
  errors.push(`package.json: license must be Apache-2.0`);
}
if (plugin?.license !== "Apache-2.0") {
  errors.push(`plugin.json: license must be Apache-2.0`);
}
for (const entry of catalog?.plugins ?? []) {
  if (entry.license !== "Apache-2.0") {
    errors.push(`marketplace.json: plugin license must be Apache-2.0`);
  }
}

const versions = [
  ["package.json", packageJson?.version],
  ["plugin.json", plugin?.version],
  ["marketplace.json metadata", catalog?.metadata?.version],
  ["marketplace.json plugin", catalog?.plugins?.[0]?.version],
] as const;
for (const [label, version] of versions) {
  if (version !== packageJson?.version) {
    errors.push(
      `${label}: version ${version ?? "missing"} != package.json ${packageJson?.version}`,
    );
  }
}

if (errors.length > 0) {
  for (const error of errors) console.error(`ERROR: ${error}`);
  console.error(`\n${errors.length} error(s)`);
  process.exit(1);
}

console.log(`All ${skills.length} skills valid.`);
