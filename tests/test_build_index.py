"""Tests for authoritative bundle-index parsing."""

from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILD_INDEX_PATH = REPOSITORY_ROOT / "scripts" / "build-index.py"


VALID_INDEX = '''---
okf_version: "0.2"
---

# Replayable Maps

Deterministic procedural map generation with version-owned inputs.

## Authors

* Jane Example
* @therightstuff
* industrial-curiosity
* maps@example.com

## Tags

* procedural-maps
* maps

## Specifications

* [Core specification](specification.md) - Normative behavior.
'''


VALID_CONCEPT = '''---
type: Strategy
title: Deterministic replay
description: Freeze every operation that consumes pseudo-random state.
tags:
  - determinism
sources:
  - id: pcg-paper
    resource: https://www.pcg-random.org/paper.html
    title: The PCG Paper
---

# Deterministic replay

The generator must version its random algorithm and consumption order.[^pcg-paper]

[^pcg-paper]: The PCG Paper
'''


class BundleIndexParsingTests(unittest.TestCase):
    """Validate the repository's constrained bundle-index format."""

    def run_parser_fixture(self, bundle_id: str, index_contents: str):
        """Parse one real temporary bundle and return its public metadata."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = root / "bundles" / bundle_id
            bundle_root.mkdir(parents=True)
            index_path = bundle_root / "index.md"
            index_path.write_text(index_contents, encoding="utf-8")
            (bundle_root / "specification.md").write_text("# Specification\n", encoding="utf-8")
            strategy_path = bundle_root / "strategies" / "replay.md"
            strategy_path.parent.mkdir()
            strategy_path.write_text("# Replay strategy\n", encoding="utf-8")

            module = self.load_build_index()
            metadata, issues = module.parse_bundle_index(index_path, bundle_root)

            self.assertEqual(issues, [])
            self.assertIsNotNone(metadata)
            return {
                "bundle_id": metadata.bundle_id,
                "title": metadata.title,
                "description": metadata.description,
                "authors": list(metadata.authors),
                "tags": list(metadata.tags),
                "specification_paths": list(metadata.specification_paths),
                "index_path": metadata.index_path,
                "bundle_root": metadata.bundle_root,
            }

    def assert_fixture_rejected(
        self,
        bundle_id: str,
        index_contents: str,
        message: str,
        expected_line: int | None = None,
    ):
        """Assert a malformed index yields a line-addressed validation error."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = root / "bundles" / bundle_id
            bundle_root.mkdir(parents=True)
            index_path = bundle_root / "index.md"
            index_path.write_text(index_contents, encoding="utf-8")
            (bundle_root / "specification.md").write_text("# Specification\n", encoding="utf-8")

            module = self.load_build_index()
            metadata, issues = module.parse_bundle_index(index_path, bundle_root)

            self.assertIsNone(metadata)
            self.assertTrue(issues)
            matching_issues = [
                issue
                for issue in issues
                if issue.path == index_path and message in issue.message
            ]
            self.assertTrue(
                matching_issues,
                f"Expected a line-addressed issue containing {message!r}, got {issues!r}",
            )
            if expected_line is not None:
                self.assertIn(
                    expected_line,
                    [issue.line for issue in matching_issues],
                    f"Expected {message!r} at line {expected_line}, got {matching_issues!r}",
                )
            else:
                self.assertTrue(all(issue.line > 0 for issue in matching_issues))

    def load_build_index(self):
        """Load the CLI script without giving its hyphenated filename a module name."""
        specification = importlib.util.spec_from_file_location("build_index", BUILD_INDEX_PATH)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        specification.loader.exec_module(module)
        return module

    def test_parses_mixed_authors_and_one_word_tags(self):
        metadata = self.run_parser_fixture("replayable-maps", VALID_INDEX)

        self.assertEqual(metadata["authors"], [
            "Jane Example", "@therightstuff", "industrial-curiosity",
            "maps@example.com",
        ])
        self.assertEqual(metadata["tags"], ["procedural-maps", "maps"])
        self.assertEqual(metadata["title"], "Replayable Maps")
        self.assertEqual(
            metadata["description"],
            "Deterministic procedural map generation with version-owned inputs.",
        )
        self.assertEqual(metadata["specification_paths"], [Path("specification.md")])

    def test_rejects_invalid_directory_identifier(self):
        self.assert_fixture_rejected("Replayable_Maps", VALID_INDEX, "Bundle identifiers")

    def test_rejects_missing_h1(self):
        self.assert_fixture_rejected(
            "replayable-maps", VALID_INDEX.replace("# Replayable Maps\n\n", ""), "H1",
        )

    def test_rejects_blank_description(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace(
                "Deterministic procedural map generation with version-owned inputs.\n\n", "",
            ),
            "description",
        )

    def test_rejects_missing_required_section(self):
        self.assert_fixture_rejected(
            "replayable-maps", VALID_INDEX.replace("## Tags\n\n* procedural-maps\n* maps\n\n", ""), "Tags",
        )

    def test_rejects_reordered_required_sections(self):
        reordered = VALID_INDEX.replace(
            "## Authors\n\n* Jane Example\n* @therightstuff\n* industrial-curiosity\n* maps@example.com\n\n"
            "## Tags\n\n* procedural-maps\n* maps\n\n",
            "## Tags\n\n* procedural-maps\n* maps\n\n"
            "## Authors\n\n* Jane Example\n* @therightstuff\n* industrial-curiosity\n* maps@example.com\n\n",
        )
        self.assert_fixture_rejected("replayable-maps", reordered, "order")

    def test_rejects_empty_authors(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace("* Jane Example\n* @therightstuff\n* industrial-curiosity\n* maps@example.com\n", ""),
            "Authors",
        )

    def test_rejects_exact_duplicate_authors(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace("* maps@example.com\n", "* maps@example.com\n* Jane Example\n"),
            "Duplicate author",
        )

    def test_rejects_invalid_tags(self):
        self.assert_fixture_rejected(
            "replayable-maps", VALID_INDEX.replace("* maps\n", "* Maps\n"), "Tag",
        )

    def test_rejects_duplicate_tags(self):
        self.assert_fixture_rejected(
            "replayable-maps", VALID_INDEX.replace("* maps\n", "* procedural-maps\n"), "Duplicate tag",
        )

    def test_rejects_specification_without_local_markdown_link(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace(
                "* [Core specification](specification.md) - Normative behavior.",
                "* [Core specification](https://example.com/specification) - Normative behavior.",
            ),
            "Specification",
        )

    def test_rejects_missing_required_specification_link_at_its_source_line(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace("specification.md", "missing-specification.md"),
            "Indexed local link does not exist.",
            expected_line=23,
        )

    def test_rejects_missing_optional_local_markdown_link_at_its_source_line(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX + "\n## Strategies\n\n* [Missing strategy](strategies/missing.md) - Preserve stable output.\n",
            "Indexed local link does not exist.",
            expected_line=27,
        )

    def test_rejects_malformed_entries_in_unknown_optional_sections(self):
        malformed_entries = (
            "[Replay strategy](strategies/replay.md) - Preserve stable output.",
            "* [Replay strategy](strategies/replay.md)",
            "* Explain the strategy in prose without an index link.",
        )
        for entry in malformed_entries:
            with self.subTest(entry=entry):
                self.assert_fixture_rejected(
                    "replayable-maps",
                    VALID_INDEX + f"\n## Future material\n\n{entry}\n",
                    "Optional section entries must link",
                )

    def test_rejects_indexed_link_that_escapes_bundle_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = root / "bundles" / "replayable-maps"
            bundle_root.mkdir(parents=True)
            index_path = bundle_root / "index.md"
            index_path.write_text(
                VALID_INDEX.replace("specification.md", "../outside.md"),
                encoding="utf-8",
            )
            (bundle_root.parent / "outside.md").write_text("# Outside\n", encoding="utf-8")

            module = self.load_build_index()
            metadata, issues = module.parse_bundle_index(index_path, bundle_root)

            self.assertIsNone(metadata)
            self.assertTrue(
                any(
                    issue.path == index_path
                    and issue.line == 23
                    and "escapes bundle root" in issue.message
                    for issue in issues
                ),
                f"Expected a path-addressed escape issue, got {issues!r}",
            )

    def test_rejects_symbolic_indexed_markdown_link(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = root / "bundles" / "replayable-maps"
            bundle_root.mkdir(parents=True)
            index_path = bundle_root / "index.md"
            index_path.write_text(VALID_INDEX, encoding="utf-8")
            external = root / "outside.md"
            external.write_text("# Outside\n", encoding="utf-8")
            (bundle_root / "specification.md").symlink_to(external)

            module = self.load_build_index()
            metadata, issues = module.parse_bundle_index(index_path, bundle_root)

            self.assertIsNone(metadata)
            self.assertTrue(
                any(
                    issue.path == index_path
                    and issue.line == 23
                    and "symbolic link" in issue.message
                    for issue in issues
                ),
                f"Expected a path-addressed symbolic-link issue, got {issues!r}",
            )

    def test_rejects_unexpected_frontmatter(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace('okf_version: "0.2"\n', 'okf_version: "0.2"\ntitle: Extra\n'),
            "frontmatter",
            expected_line=3,
        )

    def test_reports_extra_h1_at_its_source_line(self):
        self.assert_fixture_rejected(
            "replayable-maps",
            VALID_INDEX.replace("## Authors", "# Another title\n\n## Authors"),
            "H1",
            expected_line=9,
        )

    def test_allows_additional_sections_with_local_markdown_links(self):
        metadata = self.run_parser_fixture(
            "replayable-maps",
            VALID_INDEX + "\n## Strategies\n\n* [Replay strategy](strategies/replay.md) - Preserve stable output.\n",
        )

        self.assertEqual(
            metadata["specification_paths"],
            [Path("specification.md"), Path("strategies/replay.md")],
        )


class BuildIndexTestCase(unittest.TestCase):
    """Shared helpers for real temporary bundle repositories."""

    def load_build_index(self):
        specification = importlib.util.spec_from_file_location("build_index", BUILD_INDEX_PATH)
        self.assertIsNotNone(specification)
        self.assertIsNotNone(specification.loader)
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        specification.loader.exec_module(module)
        return module

    def write_bundle(
        self,
        root: Path,
        bundle_id: str = "replayable-maps",
        index_contents: str = VALID_INDEX,
        concept_contents: str = VALID_CONCEPT,
    ) -> Path:
        bundle_root = root / "bundles" / bundle_id
        bundle_root.mkdir(parents=True)
        (bundle_root / "index.md").write_text(index_contents, encoding="utf-8")
        (bundle_root / "specification.md").write_text(VALID_CONCEPT, encoding="utf-8")
        (bundle_root / "strategy.md").write_text(concept_contents, encoding="utf-8")
        return bundle_root

    def parse_metadata(self, module, bundle_root: Path):
        metadata, issues = module.parse_bundle_index(bundle_root / "index.md", bundle_root)
        self.assertEqual(issues, [])
        self.assertIsNotNone(metadata)
        return metadata


class ConceptValidationTests(BuildIndexTestCase):
    """Validate constrained OKF concept documents below a bundle."""

    def test_accepts_required_okf_fields_and_external_resource(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            concept_path = bundle_root / "strategy.md"
            concept_path.write_text(
                VALID_CONCEPT + "\n[PCG paper](https://www.pcg-random.org/paper.html)\n",
                encoding="utf-8",
            )

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertEqual(issues, [])

    def test_accepts_unknown_okf_type(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(
                root,
                concept_contents=VALID_CONCEPT.replace("type: Strategy", "type: Experiment"),
            )

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertEqual(issues, [])

    def test_rejects_each_missing_required_frontmatter_field(self):
        expected_fields = ("type", "title", "description", "tags", "sources")
        for field in expected_fields:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                concept = VALID_CONCEPT.replace(f"{field}: ", f"unused-{field}: ", 1)
                if field in ("tags", "sources"):
                    concept = VALID_CONCEPT.replace(f"{field}:\n", f"unused-{field}:\n", 1)
                bundle_root = self.write_bundle(root, concept_contents=concept)

                module = self.load_build_index()
                issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

                self.assertTrue(
                    any(field in issue.message for issue in issues),
                    f"Expected an issue for missing {field!r}, got {issues!r}",
                )

    def test_rejects_missing_local_link(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(
                root,
                concept_contents=VALID_CONCEPT + "\n[Missing](missing.md)\n",
            )

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertTrue(any("does not exist" in issue.message for issue in issues))

    def test_rejects_link_that_escapes_bundle_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(
                root,
                concept_contents=VALID_CONCEPT + "\n[Escape](../../outside.md)\n",
            )

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertTrue(any("escapes bundle root" in issue.message for issue in issues))

    def test_rejects_unresolved_template_markers(self):
        for marker in ("REPLACE_TITLE", "{{TITLE}}"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                bundle_root = self.write_bundle(root, concept_contents=VALID_CONCEPT + f"\n{marker}\n")

                module = self.load_build_index()
                issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

                self.assertTrue(any("template marker" in issue.message for issue in issues))

    def test_requires_at_least_one_https_source_resource(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(
                root,
                concept_contents=VALID_CONCEPT.replace(
                    "resource: https://www.pcg-random.org/paper.html",
                    "resource: local.md",
                ),
            )

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertTrue(any("https://" in issue.message for issue in issues))

    def test_rejects_footnote_reference_without_a_declared_source(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(
                root,
                concept_contents=VALID_CONCEPT.replace("[^pcg-paper]", "[^unknown-source]", 1),
            )

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertTrue(any("unknown-source" in issue.message for issue in issues))

    def test_skips_reserved_log_markdown_at_every_bundle_depth(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            (bundle_root / "log.md").write_text("# Bundle history\n", encoding="utf-8")
            nested_log = bundle_root / "strategies" / "log.md"
            nested_log.parent.mkdir(exist_ok=True)
            nested_log.write_text("# Strategy history\n", encoding="utf-8")

            module = self.load_build_index()
            issues = module.validate_bundle_concepts(self.parse_metadata(module, bundle_root))

            self.assertEqual(issues, [])


class TagGenerationTests(BuildIndexTestCase):
    """Render and safely synchronize the generated distributed tag indexes."""

    def test_write_restores_complete_prior_tree_when_swap_is_interrupted(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            module = self.load_build_index()
            prior = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            module.write_tag_tree(root, prior)
            previous_index = (root / "tags" / "index.md").read_text(encoding="utf-8")
            desired = {Path("index.md"): "new index\n"}
            original_replace = module.os.replace

            def interrupt_swap(source, destination):
                if Path(source).parent.name.startswith(".tags-staging-") and Path(destination).name == "tags":
                    raise KeyboardInterrupt
                return original_replace(source, destination)

            with patch.object(module.os, "replace", side_effect=interrupt_swap), self.assertRaises(KeyboardInterrupt):
                module.write_tag_tree(root, desired)

            self.assertEqual((root / "tags" / "index.md").read_text(encoding="utf-8"), previous_index)

    def test_renders_ordinally_sorted_tag_pages_with_all_authors(self):
        alpha_index = VALID_INDEX.replace("Replayable Maps", "Alpha Maps").replace(
            "procedural-maps\n* maps", "maps",
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            alpha_root = self.write_bundle(root, "alpha-maps", alpha_index)
            replayable_root = self.write_bundle(root)

            module = self.load_build_index()
            desired = module.render_tag_tree([
                self.parse_metadata(module, replayable_root),
                self.parse_metadata(module, alpha_root),
            ])

            self.assertEqual(list(desired), [
                Path("index.md"),
                Path("maps/index.md"),
                Path("procedural-maps/index.md"),
            ])
            self.assertEqual(
                desired[Path("index.md")],
                "<!-- Generated by scripts/build-index.py. Do not edit. -->\n"
                "\n# Tags\n\n"
                "* [maps](maps/)\n"
                "* [procedural-maps](procedural-maps/)\n",
            )
            self.assertEqual(
                desired[Path("maps/index.md")],
                "<!-- Generated by scripts/build-index.py. Do not edit. -->\n"
                "\n# maps\n\n"
                "* [Alpha Maps](../../bundles/alpha-maps/) - Deterministic procedural map generation with version-owned inputs. Authors: Jane Example, @therightstuff, industrial-curiosity, maps@example.com.\n"
                "* [Replayable Maps](../../bundles/replayable-maps/) - Deterministic procedural map generation with version-owned inputs. Authors: Jane Example, @therightstuff, industrial-curiosity, maps@example.com.\n",
            )
            self.assertEqual(
                desired[Path("procedural-maps/index.md")],
                "<!-- Generated by scripts/build-index.py. Do not edit. -->\n"
                "\n# procedural-maps\n\n"
                "* [Replayable Maps](../../bundles/replayable-maps/) - Deterministic procedural map generation with version-owned inputs. Authors: Jane Example, @therightstuff, industrial-curiosity, maps@example.com.\n",
            )

    def test_write_tag_tree_removes_stale_marked_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            tags_root = root / "tags"
            stale_index = tags_root / "obsolete" / "index.md"
            stale_index.parent.mkdir(parents=True)
            stale_index.write_text(
                "<!-- Generated by scripts/build-index.py. Do not edit. -->\n\n# obsolete\n",
                encoding="utf-8",
            )

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            module.write_tag_tree(root, desired)

            self.assertFalse(stale_index.parent.exists())
            self.assertEqual((tags_root / "maps" / "index.md").read_text(encoding="utf-8"), desired[Path("maps/index.md")])

    def test_write_tag_tree_removes_untracked_marked_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            untracked_index = root / "tags" / "new-tag" / "index.md"
            untracked_index.parent.mkdir(parents=True)
            untracked_index.write_text(
                "<!-- Generated by scripts/build-index.py. Do not edit. -->\n\n# new-tag\n",
                encoding="utf-8",
            )

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            module.write_tag_tree(root, desired)

            self.assertFalse(untracked_index.parent.exists())

    def test_refuses_to_replace_unmarked_current_tag_page(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            manual_index = root / "tags" / "maps" / "index.md"
            manual_index.parent.mkdir(parents=True)
            manual_contents = "# Manually maintained maps\n"
            manual_index.write_text(manual_contents, encoding="utf-8")

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            with self.assertRaises(ValueError):
                module.write_tag_tree(root, desired)

            self.assertEqual(manual_index.read_text(encoding="utf-8"), manual_contents)

    def test_refuses_tag_directory_file_without_creating_partial_output(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            blocking_path = root / "tags" / "maps"
            blocking_path.parent.mkdir(parents=True)
            blocking_path.write_text("manual file\n", encoding="utf-8")

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            with self.assertRaises(ValueError):
                module.write_tag_tree(root, desired)

            self.assertFalse((root / "tags" / "index.md").exists())
            self.assertEqual(blocking_path.read_text(encoding="utf-8"), "manual file\n")

    def test_refuses_to_delete_unmarked_stale_tag_page(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)
            manual_index = root / "tags" / "obsolete" / "index.md"
            manual_index.parent.mkdir(parents=True)
            manual_contents = "# Manually maintained obsolete tag\n"
            manual_index.write_text(manual_contents, encoding="utf-8")

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            with self.assertRaises(ValueError):
                module.write_tag_tree(root, desired)

            self.assertEqual(manual_index.read_text(encoding="utf-8"), manual_contents)

    def test_check_reports_drift_without_writing_tags(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_bundle(root)
            error_output = io.StringIO()

            module = self.load_build_index()
            with redirect_stderr(error_output):
                exit_code = module.main(["--root", str(root), "--check"])

            self.assertEqual(exit_code, 1)
            self.assertIn("tags/index.md", error_output.getvalue())
            self.assertFalse((root / "tags").exists())

    def test_compare_rejects_a_symbolic_tags_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "repository"
            external_root = Path(temporary_directory) / "external"
            bundle_root = self.write_bundle(root)

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            module.write_tag_tree(external_root, desired)
            (root / "tags").symlink_to(external_root / "tags", target_is_directory=True)

            self.assertTrue(module.compare_tag_tree(root, desired))

    def test_build_rejects_dangling_tags_root_symbolic_link(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "repository"
            missing_tags = Path(temporary_directory) / "missing" / "tags"
            self.write_bundle(root)
            (root / "tags").symlink_to(missing_tags, target_is_directory=True)
            error_output = io.StringIO()

            module = self.load_build_index()
            with redirect_stderr(error_output):
                exit_code = module.main(["--root", str(root)])

            self.assertEqual(exit_code, 1)
            self.assertIn("tags output location", error_output.getvalue())
            self.assertTrue((root / "tags").is_symlink())

    def test_write_rejects_stale_index_symbolic_links_without_writes(self):
        for target_kind in ("valid", "dangling"):
            with self.subTest(target_kind=target_kind), tempfile.TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory) / "repository"
                external = Path(temporary_directory) / "external.md"
                bundle_root = self.write_bundle(root)
                stale_index = root / "tags" / "stale" / "index.md"
                stale_index.parent.mkdir(parents=True)
                if target_kind == "valid":
                    external.write_text(
                        "<!-- Generated by scripts/build-index.py. Do not edit. -->\n",
                        encoding="utf-8",
                    )
                stale_index.symlink_to(external)

                module = self.load_build_index()
                desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
                with self.assertRaisesRegex(ValueError, "symbolic link"):
                    module.write_tag_tree(root, desired)

                self.assertFalse((root / "tags" / "index.md").exists())
                self.assertTrue(stale_index.is_symlink())

    def test_build_rejects_unmarked_file_directly_under_tags_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            self.write_bundle(root)
            extra = root / "tags" / "notes.md"
            extra.parent.mkdir(parents=True)
            extra.write_text("manual notes\n", encoding="utf-8")
            error_output = io.StringIO()

            module = self.load_build_index()
            with redirect_stderr(error_output):
                exit_code = module.main(["--root", str(root)])

            self.assertEqual(exit_code, 1)
            self.assertIn("notes.md", error_output.getvalue())
            self.assertFalse((root / "tags" / "index.md").exists())
            self.assertEqual(extra.read_text(encoding="utf-8"), "manual notes\n")

    def test_check_reports_extra_file_inside_desired_tag_directory_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            bundle_root = self.write_bundle(root)

            module = self.load_build_index()
            desired = module.render_tag_tree([self.parse_metadata(module, bundle_root)])
            module.write_tag_tree(root, desired)
            extra = root / "tags" / "maps" / "notes.md"
            extra.write_text("manual notes\n", encoding="utf-8")
            generated_before = (root / "tags" / "maps" / "index.md").read_text(encoding="utf-8")
            error_output = io.StringIO()

            with redirect_stderr(error_output):
                exit_code = module.main(["--root", str(root), "--check"])

            self.assertEqual(exit_code, 1)
            self.assertIn("maps/notes.md", error_output.getvalue())
            self.assertEqual((root / "tags" / "maps" / "index.md").read_text(encoding="utf-8"), generated_before)
            self.assertEqual(extra.read_text(encoding="utf-8"), "manual notes\n")


class InputContainmentTests(BuildIndexTestCase):
    """Reject bundle inputs that would cause reads outside the repository root."""

    def test_rejects_symbolic_bundles_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "repository"
            external_root = Path(temporary_directory) / "external"
            self.write_bundle(external_root)
            root.mkdir()
            (root / "bundles").symlink_to(external_root / "bundles", target_is_directory=True)
            error_output = io.StringIO()

            module = self.load_build_index()
            with redirect_stderr(error_output):
                exit_code = module.main(["--root", str(root)])

            self.assertEqual(exit_code, 1)
            self.assertIn("symbolic link", error_output.getvalue())
            self.assertFalse((root / "tags").exists())

    def test_rejects_symbolic_bundle_index(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "repository"
            external_index = Path(temporary_directory) / "external-index.md"
            bundle_root = self.write_bundle(root)
            external_index.write_text(VALID_INDEX, encoding="utf-8")
            (bundle_root / "index.md").unlink()
            (bundle_root / "index.md").symlink_to(external_index)
            error_output = io.StringIO()

            module = self.load_build_index()
            with redirect_stderr(error_output):
                exit_code = module.main(["--root", str(root)])

            self.assertEqual(exit_code, 1)
            self.assertIn("symbolic link", error_output.getvalue())
            self.assertFalse((root / "tags").exists())


if __name__ == "__main__":
    unittest.main()
