#!/usr/bin/env node

import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

import { installSkills, readCatalogSkillFiles } from "../lib/install-skills.mjs";

function catalogRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
}

function packageRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), "..");
}

async function main() {
  const [targetProject, ...extraArguments] = process.argv.slice(2);
  if (targetProject === undefined || extraArguments.length > 0) {
    throw new Error("Usage: npm run local:init -- TARGET_PROJECT");
  }

  const targetRoot = resolve(process.env.INIT_CWD || process.cwd(), targetProject);
  const result = await installSkills({
    cwd: targetRoot,
    loadCatalogSkillFiles: () => readCatalogSkillFiles(join(catalogRoot(), ".agents", "skills"), {
      localSearchCommand: `npm --prefix ${JSON.stringify(packageRoot())} run local:search --`,
    }),
  });
  process.stdout.write(
    `Installed Genizah skills in ${result.location}: ${result.installedSkillNames.join(", ")}\n` +
      "Next prompt: discover and customize a specification bundle for this project.\n",
  );
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
