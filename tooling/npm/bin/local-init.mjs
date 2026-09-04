#!/usr/bin/env node

import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

import { parseInitOptions } from "../lib/init-options.mjs";
import { installSkills, readCatalogSkillFiles } from "../lib/install-skills.mjs";

function catalogRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
}

function packageRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), "..");
}

async function main() {
  const [targetProject, ...options] = process.argv.slice(2);
  if (targetProject === undefined) {
    throw new Error("Usage: npm run local:init -- TARGET_PROJECT [--skills-dir RELATIVE_PATH] [--force|-f]");
  }

  const { force, skillsDir } = parseInitOptions(options);

  const targetRoot = resolve(process.env.INIT_CWD || process.cwd(), targetProject);
  const result = await installSkills({
    cwd: targetRoot,
    force,
    skillsDir,
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
