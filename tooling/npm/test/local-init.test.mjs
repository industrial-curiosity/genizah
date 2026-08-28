import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { mkdtemp } from "node:fs/promises";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));
const sourceSkill = "---\nname: genizah\ngenizah_catalog_skill: true\n---\n";

test("local:init installs from this checkout into the invoking project", async () => {
  const targetProject = await mkdtemp(join(tmpdir(), "genizah-local-init-"));
  try {
    const priorSkillDirectory = join(targetProject, ".agents/skills/genizah");
    await mkdir(priorSkillDirectory, { recursive: true });
    await writeFile(join(priorSkillDirectory, "SKILL.md"), sourceSkill, "utf8");

    const result = spawnSync("npm", ["--prefix", packageRoot, "run", "local:init", "--", "."], {
      cwd: targetProject,
      encoding: "utf8",
    });

    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /Installed Genizah skills in \.agents\/skills/);
    const installedSkill = await readFile(
      join(targetProject, ".agents/skills/customize-spec-bundle/SKILL.md"),
      "utf8",
    );
    assert.match(installedSkill, /genizah_catalog_skill: true/);
    const installedGenizahSkill = await readFile(join(targetProject, ".agents/skills/genizah/SKILL.md"), "utf8");
    assert.match(installedGenizahSkill, /npm --prefix .* run local:search -- TERM\.\.\./);
    assert.doesNotMatch(installedGenizahSkill, /npx --yes genizah search/);
    assert.match(installedGenizahSkill, /Candidates with equal scores are tied/);
  } finally {
    await rm(targetProject, { force: true, recursive: true });
  }
});
