// Prints the reference map for this skill.
// Run from the repository root with: pnpm skill natuleadan-skills
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

type Metadata = {
  version: string;
  abstract: string;
  references: string[];
};

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const metadata = JSON.parse(
  readFileSync(join(skillDir, "metadata.json"), "utf8"),
) as Metadata;

console.log(`natuleadan-skills ${metadata.version}`);
console.log(metadata.abstract);
console.log("");
console.log("References:");
for (const reference of metadata.references) {
  console.log(`  - references/${reference}`);
}
