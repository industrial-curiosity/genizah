export function parseInitOptions(options) {
  let skillsDir;
  let force = false;

  for (let index = 0; index < options.length; index += 1) {
    const option = options[index];
    if (option === "--force" || option === "-f") {
      force = true;
      continue;
    }
    if (option !== "--skills-dir") {
      throw new Error(`Unknown option: ${option}`);
    }

    const value = options[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error("--skills-dir requires a relative path");
    }

    skillsDir = value;
    index += 1;
  }

  return { skillsDir, ...(force ? { force } : {}) };
}
