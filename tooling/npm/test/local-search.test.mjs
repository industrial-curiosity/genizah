import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

const packageRoot = fileURLToPath(new URL("..", import.meta.url));

test("local:search reads this checkout without npx", () => {
  const result = spawnSync("npm", ["--prefix", packageRoot, "run", "local:search", "--", "maps"], {
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr);
  const output = JSON.parse(result.stdout.slice(result.stdout.indexOf("{")));
  assert.deepEqual(output.terms, ["maps"]);
  assert.equal(output.candidates[0].bundleId, "versioned-procedural-map-generation");
});
