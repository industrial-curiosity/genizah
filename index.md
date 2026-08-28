---
okf_version: "0.2"
---

# Spec bundle repository index

This is a technology-neutral library of specification bundles for people and
AI agents. Read a bundle directly, or discover a suitable one through a small,
generated tag index rather than a monolithic catalog.

## Navigate

* [Bundles](bundles/) - Authoritative, independently distributable bundles.
* [Tags](tags/) - Generated discovery indexes grouped by tag.
* [Bundle format](docs/bundle-format.md) - Authoring and validation contract.
* [Bundle generator](scripts/generate-bundle.py) - Creates an incomplete bundle
  scaffold without overwriting existing content.
* [Customization skill](.agents/skills/customize-spec-bundle/) - Downloadable
  interview and adaptation workflow for a concrete target implementation.

## Format

The repository follows [Open Knowledge Format
0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).
Bundle indexes provide the authoritative discovery metadata; the generated
`tags/` tree is a convenience layer derived from those indexes.
