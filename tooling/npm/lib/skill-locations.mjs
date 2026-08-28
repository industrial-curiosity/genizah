import { lstat, realpath } from "node:fs/promises";
import { isAbsolute, join, relative, resolve } from "node:path";

export const PROJECT_SKILL_LOCATIONS = [
  ".agents/skills",
  ".github/skills",
  ".claude/skills",
  ".cursor/skills",
  ".codex/skills",
  ".opencode/skills",
  ".pi/skills",
];

export function resolveSkillLocation(cwd, location) {
  if (typeof location !== "string" || location.trim() === "") {
    throw new Error("A skill location is required");
  }
  if (isAbsolute(location)) {
    throw new Error("Skill location must be inside the current project");
  }

  const projectRoot = resolve(cwd);
  const destination = resolve(projectRoot, location);
  const destinationRelativeToProject = relative(projectRoot, destination);
  if (
    destinationRelativeToProject === "" ||
    destinationRelativeToProject === ".." ||
    destinationRelativeToProject.startsWith(`..${process.platform === "win32" ? "\\" : "/"}`) ||
    isAbsolute(destinationRelativeToProject)
  ) {
    throw new Error("Skill location must be inside the current project");
  }

  return {
    location: destinationRelativeToProject.split("\\").join("/"),
    destination,
  };
}

export async function resolveSafeSkillLocation(cwd, location) {
  const resolvedLocation = resolveSkillLocation(cwd, location);
  const projectRoot = await realpath(resolve(cwd));
  const destination = resolve(projectRoot, resolvedLocation.location);
  let ancestor = projectRoot;

  for (const segment of resolvedLocation.location.split("/")) {
    ancestor = join(ancestor, segment);
    try {
      const metadata = await lstat(ancestor);
      if (metadata.isSymbolicLink()) {
        throw new Error(`Skill location cannot contain a symbolic link: ${ancestor}`);
      }
    } catch (error) {
      if (error.code === "ENOENT") {
        break;
      }
      throw error;
    }
  }

  return {
    location: resolvedLocation.location,
    destination,
  };
}
