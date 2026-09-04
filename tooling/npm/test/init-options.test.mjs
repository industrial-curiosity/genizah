import assert from "node:assert/strict";
import test from "node:test";

import { parseInitOptions } from "../lib/init-options.mjs";

test("parses the shared skills directory and force options", () => {
  assert.deepEqual(parseInitOptions(["--skills-dir", ".claude/skills", "--force"]), {
    skillsDir: ".claude/skills",
    force: true,
  });
  assert.deepEqual(parseInitOptions(["-f"]), { skillsDir: undefined, force: true });
});

test("rejects an invalid shared skills directory option", () => {
  assert.throws(() => parseInitOptions(["--skills-dir"]), /requires a relative path/);
  assert.throws(() => parseInitOptions(["--unexpected"]), /Unknown option: --unexpected/);
});
