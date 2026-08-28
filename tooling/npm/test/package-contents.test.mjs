import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import test from "node:test";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));

test("package declares local init but does not package catalog skill copies", async () => {
  const manifest = JSON.parse(await readFile(new URL("../package.json", import.meta.url), "utf8"));

  assert.equal(manifest.scripts["local:init"], "node bin/local-init.mjs");
  assert.equal(manifest.scripts["local:search"], "node bin/local-search.mjs");
  assert.equal(manifest.author, "Industrial Curiosity");
  assert.deepEqual(manifest.repository, {
    type: "git",
    url: "git+https://github.com/industrial-curiosity/genizah.git",
  });
  assert.equal(manifest.homepage, "https://github.com/industrial-curiosity/genizah#readme");
  assert.deepEqual(manifest.bugs, {
    url: "https://github.com/industrial-curiosity/genizah/issues",
  });
  assert.equal(manifest.files.includes("LICENSE"), true);
  await access(new URL("../LICENSE", import.meta.url));
  assert.equal(manifest.files.includes("skills/"), false);
  await assert.rejects(access(new URL("../skills", import.meta.url)));
  assert.equal(packageRoot.endsWith("tooling/npm/"), true);
});
