#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

import { CATALOG_OWNER, CATALOG_REF, CATALOG_REPOSITORY, searchCatalog } from "../lib/catalog-search.mjs";

function catalogRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
}

function localCatalogFetch(root) {
  const basePath = `/${CATALOG_OWNER}/${CATALOG_REPOSITORY}/${CATALOG_REF}/`;
  const resolvedRoot = resolve(root);

  return async (url) => {
    const pathname = new URL(url).pathname;
    if (!pathname.startsWith(basePath)) {
      return { ok: false, status: 404, text: async () => "Not found" };
    }
    const target = resolve(resolvedRoot, pathname.slice(basePath.length));
    const pathRelativeToRoot = relative(resolvedRoot, target);
    if (
      pathRelativeToRoot === ".." ||
      pathRelativeToRoot.startsWith(`..${sep}`) ||
      target === resolvedRoot
    ) {
      return { ok: false, status: 404, text: async () => "Not found" };
    }
    try {
      return { ok: true, status: 200, text: async () => readFile(target, "utf8") };
    } catch (error) {
      if (error.code === "ENOENT") {
        return { ok: false, status: 404, text: async () => "Not found" };
      }
      throw error;
    }
  };
}

async function main() {
  const terms = process.argv.slice(2);
  if (terms.length === 0) {
    throw new Error("Usage: npm run local:search -- TERM...");
  }
  const result = await searchCatalog(terms, { fetch: localCatalogFetch(catalogRoot()) });
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
