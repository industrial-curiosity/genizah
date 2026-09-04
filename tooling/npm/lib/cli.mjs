import { searchCatalog } from "./catalog-search.mjs";
import { parseInitOptions } from "./init-options.mjs";
import { installSkills } from "./install-skills.mjs";

function parseSearchTerms(terms) {
  if (terms.length === 0) {
    throw new Error("search requires at least one term");
  }

  for (const term of terms) {
    if (term.startsWith("--")) {
      throw new Error(`Unknown option: ${term}`);
    }
  }

  return terms;
}

export async function main(commandArguments, dependencies = {}) {
  const [command, ...options] = commandArguments;

  switch (command) {
    case "init": {
      const installOptions = parseInitOptions(options);
      const install = dependencies.install ?? installSkills;
      const result = await install(installOptions);
      if (dependencies.install === undefined) {
        process.stdout.write(
          `Installed Genizah skills in ${result.location}: ${result.installedSkillNames.join(", ")}\n` +
          "Next prompt: discover and customize a specification bundle for this project.\n",
        );
      }
      return 0;
    }
    case "search": {
      const terms = parseSearchTerms(options);
      const search = dependencies.search ?? searchCatalog;
      const result = await search(terms);
      if (dependencies.search === undefined) {
        process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
      }
      return 0;
    }
    default:
      throw new Error(`Unknown command: ${command ?? ""}`.trim());
  }
}
