import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { main } from "../lib/cli.mjs";

test("dispatches init to the installer", async () => {
  let received;

  const code = await main(["init"], {
    install: async (options) => {
      received = options;
    },
  });

  assert.equal(code, 0);
  assert.deepEqual(received, { skillsDir: undefined });
});

test("passes an init skills directory to the installer", async () => {
  let received;

  await main(["init", "--skills-dir", ".claude/skills"], {
    install: async (options) => {
      received = options;
    },
  });

  assert.deepEqual(received, { skillsDir: ".claude/skills" });
});

test("passes either force option to the installer", async () => {
  for (const option of ["--force", "-f"]) {
    let received;

    await main(["init", option], {
      install: async (options) => {
        received = options;
      },
    });

    assert.deepEqual(received, { skillsDir: undefined, force: true });
  }
});

test("dispatches search terms to the catalog search", async () => {
  let received;

  const code = await main(["search", "procedural", "maps"], {
    search: async (terms) => {
      received = terms;
    },
  });

  assert.equal(code, 0);
  assert.deepEqual(received, ["procedural", "maps"]);
});

test("rejects init options it does not support", async () => {
  await assert.rejects(
    () => main(["init", "--unexpected"], { install: async () => {} }),
    /Unknown option: --unexpected/,
  );
});

test("rejects init without a skills directory value", async () => {
  await assert.rejects(
    () => main(["init", "--skills-dir"], { install: async () => {} }),
    /requires a relative path/,
  );
});

test("rejects search without terms", async () => {
  await assert.rejects(() => main(["search"], {}), /requires at least one term/);
});

test("rejects search options", async () => {
  await assert.rejects(() => main(["search", "--limit"], {}), /Unknown option: --limit/);
});

test("rejects an unknown command", async () => {
  await assert.rejects(() => main(["unknown"], {}), /Unknown command/);
});

test("bin wrapper writes one error message and exits unsuccessfully", () => {
  const binPath = fileURLToPath(new URL("../bin/genizah.mjs", import.meta.url));
  const result = spawnSync(process.execPath, [binPath, "unknown"], {
    encoding: "utf8",
  });

  assert.notEqual(result.status, 0);
  assert.deepEqual(result.stdout, "");
  assert.deepEqual(result.stderr.trim().split("\n"), ["Unknown command: unknown"]);
});
