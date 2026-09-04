import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rename, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { installSkills } from "../lib/install-skills.mjs";

const CATALOG_FILES = new Map([
  [
    "/industrial-curiosity/genizah/main/.agents/skills/genizah/SKILL.md",
    "---\nname: genizah\ngenizah_catalog_skill: true\n---\n\n# Catalog discovery skill\n",
  ],
  [
    "/industrial-curiosity/genizah/main/.agents/skills/customize-spec-bundle/SKILL.md",
    "---\nname: customize-spec-bundle\ngenizah_catalog_skill: true\n---\n\n# Catalog customization skill\n",
  ],
  [
    "/industrial-curiosity/genizah/main/.agents/skills/customize-spec-bundle/references/interview-coverage.md",
    "# Catalog interview coverage\n",
  ],
  [
    "/industrial-curiosity/genizah/main/.agents/skills/customize-spec-bundle/references/output-contract.md",
    "# Catalog output contract\n",
  ],
]);

async function catalogFetch(url) {
  const path = new URL(url).pathname;
  const content = CATALOG_FILES.get(path);
  return {
    ok: content !== undefined,
    status: content === undefined ? 404 : 200,
    text: async () => content ?? "Not found",
  };
}

function install(options) {
  return installSkills({ ...options, fetch: catalogFetch });
}

async function withProject(run) {
  const root = await mkdtemp(join(tmpdir(), "genizah-install-"));

  try {
    await run(root);
  } finally {
    await rm(root, { force: true, recursive: true });
  }
}

async function exists(path) {
  try {
    await readFile(path);
    return true;
  } catch {
    return false;
  }
}

test("uses .agents/skills when an interactive user accepts the default", async () => {
  await withProject(async (root) => {
    const output = [];
    const result = await install({
      cwd: root,
      prompt: async () => "",
      write: (message) => output.push(message),
    });

    assert.equal(result.location, ".agents/skills");
    assert.deepEqual(result.installedSkillNames, [
      "genizah",
      "customize-spec-bundle",
    ]);
    assert.equal(
      await readFile(join(root, ".agents/skills/genizah/SKILL.md"), "utf8"),
      CATALOG_FILES.get("/industrial-curiosity/genizah/main/.agents/skills/genizah/SKILL.md"),
    );
    assert.match(output.join("\n"), /\.github\/skills/);
  });
});

test("uses an interactive numbered compatible location without writing the default", async () => {
  await withProject(async (root) => {
    const result = await install({ cwd: root, prompt: async () => "2", write: () => {} });

    assert.equal(result.location, ".github/skills");
    assert.equal(await exists(join(root, ".github/skills/customize-spec-bundle/SKILL.md")), true);
    assert.equal(await exists(join(root, ".agents/skills/customize-spec-bundle/SKILL.md")), false);
  });
});

test("uses an explicit relative location without prompting", async () => {
  await withProject(async (root) => {
    let prompted = false;
    const result = await install({
      cwd: root,
      prompt: async () => {
        prompted = true;
        return "";
      },
      skillsDir: ".claude/skills",
    });

    assert.equal(result.location, ".claude/skills");
    assert.equal(prompted, false);
  });
});

test("reuses the first existing Genizah installation without prompting", async () => {
  await withProject(async (root) => {
    await install({ cwd: root, skillsDir: ".cursor/skills" });
    let prompted = false;

    const result = await install({
      cwd: root,
      prompt: async () => {
        prompted = true;
        return "";
      },
    });

    assert.equal(result.location, ".cursor/skills");
    assert.equal(prompted, false);
    assert.equal(await exists(join(root, ".agents/skills/customize-spec-bundle/SKILL.md")), false);
  });
});

test("rejects absolute and escaping locations before writing files", async () => {
  await withProject(async (root) => {
    for (const skillsDir of ["../outside", "/tmp/outside"]) {
      await assert.rejects(
        () => install({ cwd: root, skillsDir }),
        /inside the current project/,
      );
    }

    await assert.rejects(
      () => install({ cwd: root, prompt: async () => "../outside", write: () => {} }),
      /inside the current project/,
    );
    assert.equal(await exists(join(root, ".agents/skills/customize-spec-bundle/SKILL.md")), false);
  });
});

test("preserves unrelated skills and refuses to replace an unrelated target skill", async () => {
  await withProject(async (root) => {
    const location = join(root, ".agents/skills");
    await mkdir(join(location, "unrelated"), { recursive: true });
    await writeFile(join(location, "unrelated/SKILL.md"), "keep", "utf8");
    await mkdir(join(location, "customize-spec-bundle"), { recursive: true });
    await writeFile(join(location, "customize-spec-bundle/SKILL.md"), "not Genizah", "utf8");

    await assert.rejects(
      () => install({ cwd: root, skillsDir: ".agents/skills" }),
      /unrelated existing skill directory[\s\S]*--force \(or -f\)/,
    );
    assert.equal(await readFile(join(location, "unrelated/SKILL.md"), "utf8"), "keep");
    assert.equal(await readFile(join(location, "customize-spec-bundle/SKILL.md"), "utf8"), "not Genizah");
  });
});

test("replaces an unrelated target skill only when forced", async () => {
  await withProject(async (root) => {
    const location = join(root, ".agents/skills");
    const target = join(location, "customize-spec-bundle/SKILL.md");
    await mkdir(join(location, "customize-spec-bundle"), { recursive: true });
    await writeFile(target, "not Genizah", "utf8");

    await install({ cwd: root, skillsDir: ".agents/skills", force: true });

    assert.equal(
      await readFile(target, "utf8"),
      CATALOG_FILES.get("/industrial-curiosity/genizah/main/.agents/skills/customize-spec-bundle/SKILL.md"),
    );
  });
});

test("restores owned skills when moving a staged skill fails", async () => {
  await withProject(async (root) => {
    await install({ cwd: root, skillsDir: ".agents/skills" });
    const location = join(root, ".agents/skills");
    const original = await readFile(join(location, "customize-spec-bundle/SKILL.md"), "utf8");
    let stagedMoves = 0;

    await assert.rejects(
      () => install({
        cwd: root,
        skillsDir: ".agents/skills",
        rename: async (from, to) => {
          if (from.includes(".genizah-stage-") && to.endsWith(join(".agents/skills", "customize-spec-bundle"))) {
            stagedMoves += 1;
            throw new Error("simulated move failure");
          }
          await rename(from, to);
        },
      }),
      /simulated move failure/,
    );

    assert.equal(stagedMoves, 1);
    assert.equal(await readFile(join(location, "customize-spec-bundle/SKILL.md"), "utf8"), original);
    assert.equal(
      await exists(join(location, "genizah/SKILL.md")),
      true,
    );
  });
});

test("fails before destination writes when a catalog skill cannot be fetched", async () => {
  await withProject(async (root) => {
    const fetch = async () => ({ ok: false, status: 503, text: async () => "Unavailable" });

    await assert.rejects(
      () => installSkills({ cwd: root, skillsDir: ".agents/skills", fetch }),
      /Failed to fetch catalog skill .*503/,
    );
    assert.equal(await exists(join(root, ".agents/skills/customize-spec-bundle/SKILL.md")), false);
  });
});

test("fetches only the four catalog files needed for the two skill trees", async () => {
  await withProject(async (root) => {
    const requestedPaths = [];
    const fetch = async (url) => {
      const path = new URL(url).pathname;
      requestedPaths.push(path);
      return catalogFetch(url);
    };

    await installSkills({ cwd: root, skillsDir: ".agents/skills", fetch });

    assert.deepEqual(requestedPaths, [...CATALOG_FILES.keys()]);
  });
});

test("rejects a symlinked destination ancestor before fetching or writing", async () => {
  await withProject(async (root) => {
    const external = await mkdtemp(join(tmpdir(), "genizah-external-"));
    try {
      await symlink(external, join(root, ".agents"));
      let fetched = false;

      await assert.rejects(
        () => installSkills({
          cwd: root,
          skillsDir: ".agents/skills",
          fetch: async () => {
            fetched = true;
            return catalogFetch();
          },
        }),
        /cannot contain a symbolic link/,
      );

      assert.equal(fetched, false);
      assert.equal(await exists(join(external, "skills/customize-spec-bundle/SKILL.md")), false);
    } finally {
      await rm(external, { force: true, recursive: true });
    }
  });
});

test("refuses a third-party skill that mentions a Genizah name only in prose", async () => {
  await withProject(async (root) => {
    const skillPath = join(root, ".agents/skills/customize-spec-bundle/SKILL.md");
    const thirdPartySkill = "---\nname: third-party-skill\n---\n\nThis mentions name: customize-spec-bundle in prose.\n";
    await mkdir(join(root, ".agents/skills/customize-spec-bundle"), { recursive: true });
    await writeFile(skillPath, thirdPartySkill, "utf8");

    await assert.rejects(
      () => install({ cwd: root, skillsDir: ".agents/skills" }),
      /unrelated existing skill directory/,
    );
    assert.equal(await readFile(skillPath, "utf8"), thirdPartySkill);
  });
});
