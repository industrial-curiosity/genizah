import { lstat, mkdir, mkdtemp, readFile, rename as renameFile, rm, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { createInterface } from "node:readline/promises";

import { PROJECT_SKILL_LOCATIONS, resolveSafeSkillLocation, resolveSkillLocation } from "./skill-locations.mjs";

const SKILL_NAMES = ["genizah", "customize-spec-bundle"];
const CATALOG_RAW_BASE = "https://raw.githubusercontent.com/industrial-curiosity/genizah/main/.agents/skills";
const CATALOG_SKILL_FILES = [
  "genizah/SKILL.md",
  "customize-spec-bundle/SKILL.md",
  "customize-spec-bundle/references/interview-coverage.md",
  "customize-spec-bundle/references/output-contract.md",
];

async function promptForLocation(message) {
  if (!process.stdin.isTTY) {
    throw new Error("Interactive skill location selection requires a terminal or --skills-dir");
  }
  const terminal = createInterface({ input: process.stdin, output: process.stdout });
  try {
    return await terminal.question(`${message} `);
  } finally {
    terminal.close();
  }
}

async function pathExists(path) {
  try {
    await lstat(path);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") {
      return false;
    }
    throw error;
  }
}

async function isOwnedSkill(directory, name) {
  try {
    const metadata = await lstat(directory);
    if (!metadata.isDirectory()) {
      return false;
    }
    const skill = await readFile(join(directory, "SKILL.md"), "utf8");
    const frontmatter = skill.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
    if (frontmatter === undefined) {
      return false;
    }
    const lines = frontmatter.split(/\r?\n/);
    return (
      lines.filter((line) => line === `name: ${name}`).length === 1 &&
      lines.filter((line) => line === "genizah_catalog_skill: true").length === 1
    );
  } catch (error) {
    if (error.code === "ENOENT") {
      return false;
    }
    throw error;
  }
}

async function findPriorLocation(cwd) {
  for (const location of PROJECT_SKILL_LOCATIONS) {
    let destination;
    try {
      ({ destination } = await resolveSafeSkillLocation(cwd, location));
    } catch (error) {
      if (error.message.startsWith("Skill location cannot contain a symbolic link:")) {
        continue;
      }
      throw error;
    }
    if (await isOwnedSkill(join(destination, "genizah"), "genizah")) {
      return location;
    }
  }
  return undefined;
}

async function selectLocation({ cwd, skillsDir, prompt, write }) {
  if (skillsDir !== undefined) {
    return resolveSkillLocation(cwd, skillsDir);
  }

  const priorLocation = await findPriorLocation(cwd);
  if (priorLocation !== undefined) {
    return resolveSkillLocation(cwd, priorLocation);
  }

  write(`Compatible project skill locations:\n${PROJECT_SKILL_LOCATIONS.map((location, index) => `${index + 1}. ${location}`).join("\n")}`);
  const response = (await prompt("Select a skill location (blank for .agents/skills):")).trim();
  if (response === "") {
    return resolveSkillLocation(cwd, PROJECT_SKILL_LOCATIONS[0]);
  }
  if (/^\d+$/.test(response)) {
    const location = PROJECT_SKILL_LOCATIONS[Number(response) - 1];
    if (location === undefined) {
      throw new Error(`Unknown skill location selection: ${response}`);
    }
    return resolveSkillLocation(cwd, location);
  }
  return resolveSkillLocation(cwd, response);
}

async function verifyReplacementTargets(destination) {
  for (const name of SKILL_NAMES) {
    const target = join(destination, name);
    if (await pathExists(target) && !(await isOwnedSkill(target, name))) {
      throw new Error(`Refusing to replace unrelated existing skill directory: ${target}`);
    }
  }
}

async function fetchCatalogSkillFiles(fetch) {
  if (typeof fetch !== "function") {
    throw new Error("A fetch implementation is required to install catalog skills");
  }

  const files = [];
  for (const path of CATALOG_SKILL_FILES) {
    let response;
    try {
      response = await fetch(`${CATALOG_RAW_BASE}/${path}`);
    } catch (error) {
      throw new Error(`Failed to fetch catalog skill ${path}: ${error.message}`, { cause: error });
    }
    if (!response?.ok) {
      throw new Error(`Failed to fetch catalog skill ${path}: HTTP ${response?.status ?? "unknown"}`);
    }
    try {
      files.push({ path, content: await response.text() });
    } catch (error) {
      throw new Error(`Failed to read catalog skill ${path}: ${error.message}`, { cause: error });
    }
  }
  return files;
}

export async function readCatalogSkillFiles(catalogSkillsDirectory, { localSearchCommand } = {}) {
  const files = [];
  for (const path of CATALOG_SKILL_FILES) {
    try {
      let content = await readFile(join(catalogSkillsDirectory, path), "utf8");
      if (path === "genizah/SKILL.md" && localSearchCommand !== undefined) {
        content = content.replace("npx --yes genizah search", localSearchCommand);
      }
      files.push({ path, content });
    } catch (error) {
      throw new Error(`Failed to read local catalog skill ${path}: ${error.message}`, { cause: error });
    }
  }
  return files;
}

async function stageCatalogSkillFiles(staging, files) {
  for (const { path, content } of files) {
    const destination = join(staging, path);
    await mkdir(dirname(destination), { recursive: true });
    await writeFile(destination, content, "utf8");
  }
  for (const name of SKILL_NAMES) {
    if (!(await isOwnedSkill(join(staging, name), name))) {
      throw new Error(`Catalog skill has unexpected identity: ${name}`);
    }
  }
}

export async function installSkills({
  cwd = process.cwd(),
  skillsDir,
  prompt = promptForLocation,
  write = (message) => process.stdout.write(`${message}\n`),
  rename = renameFile,
  fetch = globalThis.fetch,
  loadCatalogSkillFiles = () => fetchCatalogSkillFiles(fetch),
} = {}) {
  const selectedLocation = await selectLocation({ cwd, skillsDir, prompt, write });
  const { location, destination } = await resolveSafeSkillLocation(cwd, selectedLocation.location);
  await verifyReplacementTargets(destination);
  const catalogSkillFiles = await loadCatalogSkillFiles();
  await mkdir(dirname(destination), { recursive: true });

  const staging = await mkdtemp(join(dirname(destination), ".genizah-stage-"));
  const backup = await mkdtemp(join(dirname(destination), ".genizah-backup-"));
  const backedUp = [];
  const installed = [];

  try {
    await stageCatalogSkillFiles(staging, catalogSkillFiles);
    await mkdir(destination, { recursive: true });

    for (const name of SKILL_NAMES) {
      const target = join(destination, name);
      if (await pathExists(target)) {
        await rename(target, join(backup, name));
        backedUp.push(name);
      }
    }
    for (const name of SKILL_NAMES) {
      await rename(join(staging, name), join(destination, name));
      installed.push(name);
    }
  } catch (error) {
    await Promise.all(installed.map((name) => rm(join(destination, name), { force: true, recursive: true })));
    for (const name of backedUp.reverse()) {
      await rename(join(backup, name), join(destination, name));
    }
    throw error;
  } finally {
    await rm(staging, { force: true, recursive: true });
    await rm(backup, { force: true, recursive: true });
  }

  return { location, installedSkillNames: SKILL_NAMES };
}
