"""Behavior tests for the safe bundle scaffold generator."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPOSITORY_ROOT / "scripts" / "generate-bundle.py"
TEMPLATE_PATH = REPOSITORY_ROOT / "templates" / "bundle"


class GenerateBundleTests(unittest.TestCase):
    """Run the generator against real, isolated temporary repositories."""

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        shutil.copytree(TEMPLATE_PATH, self.root / "templates" / "bundle")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def run_generator(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--root", str(self.root), *arguments],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )

    def test_derives_a_display_title_from_the_bundle_identifier(self):
        result = self.run_generator("sample-bundle")

        self.assertEqual(result.returncode, 0, result.stderr)
        index = self.root / "bundles" / "sample-bundle" / "index.md"
        self.assertIn("# Sample Bundle", index.read_text(encoding="utf-8"))

    def test_generates_named_bundle_without_overwriting(self):
        result = self.run_generator("sample-bundle", "--title", "Sample Bundle")

        self.assertEqual(result.returncode, 0, result.stderr)
        index = self.root / "bundles" / "sample-bundle" / "index.md"
        self.assertIn("# Sample Bundle", index.read_text(encoding="utf-8"))
        self.assertNotIn("{{BUNDLE_ID}}", index.read_text(encoding="utf-8"))
        self.assertNotIn("{{BUNDLE_TITLE}}", index.read_text(encoding="utf-8"))

    def test_rejects_invalid_bundle_identifiers_before_creating_a_destination(self):
        for bundle_id in ("Sample-Bundle", "sample_bundle", "-sample", "sample-", ""):
            with self.subTest(bundle_id=bundle_id):
                arguments = ("--", bundle_id) if bundle_id.startswith("-") else (bundle_id,)
                result = self.run_generator(*arguments)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("lowercase kebab-case", result.stderr)
                self.assertFalse((self.root / "bundles" / bundle_id).exists())

    def test_rejects_an_empty_explicit_title_before_creating_a_destination(self):
        result = self.run_generator("sample-bundle", "--title", "   ")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("title", result.stderr.lower())
        self.assertFalse((self.root / "bundles" / "sample-bundle").exists())

    def test_rejects_a_missing_template_without_leaving_a_partial_bundle(self):
        shutil.rmtree(self.root / "templates" / "bundle")

        result = self.run_generator("sample-bundle")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("template", result.stderr.lower())
        self.assertFalse((self.root / "bundles" / "sample-bundle").exists())

    def test_rejects_a_directory_symbolic_link_in_the_template_before_copying(self):
        external_directory = self.root / "external-template-content"
        external_directory.mkdir()
        (external_directory / "copied-if-unsafe.md").write_text("outside content", encoding="utf-8")
        template_link = self.root / "templates" / "bundle" / "outside"
        template_link.symlink_to(external_directory, target_is_directory=True)

        result = self.run_generator("sample-bundle")

        self.assertNotEqual(result.returncode, 0)
        expected_path = template_link.parent.resolve() / template_link.name
        self.assertIn(f"Bundle template must not contain symbolic links: {expected_path}", result.stderr)
        self.assertFalse((self.root / "bundles" / "sample-bundle").exists())

    def test_refuses_to_overwrite_an_existing_bundle(self):
        destination = self.root / "bundles" / "sample-bundle"
        destination.mkdir(parents=True)
        sentinel = destination / "keep.txt"
        sentinel.write_text("preserve me", encoding="utf-8")

        result = self.run_generator("sample-bundle")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(destination), result.stderr)
        self.assertIn("choose another id or remove it yourself", result.stderr.lower())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve me")

    def test_reports_every_created_file_in_sorted_order(self):
        result = self.run_generator("sample-bundle")

        self.assertEqual(result.returncode, 0, result.stderr)
        destination = self.root / "bundles" / "sample-bundle"
        expected = sorted(
            path.relative_to(self.root).as_posix()
            for path in destination.rglob("*")
            if path.is_file()
        )
        created = [
            line.removeprefix("Created: ")
            for line in result.stdout.splitlines()
            if line.startswith("Created: ")
        ]
        self.assertEqual(created, expected)
        self.assertIn(
            "Next: replace every REPLACE_ marker, then run python3 scripts/build-index.py",
            result.stdout,
        )

    def test_generated_bundle_remains_invalid_until_authored(self):
        result = self.run_generator("sample-bundle")

        self.assertEqual(result.returncode, 0, result.stderr)
        validation = subprocess.run(
            [sys.executable, str(REPOSITORY_ROOT / "scripts" / "build-index.py"), "--root", str(self.root)],
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        self.assertNotEqual(validation.returncode, 0)
        self.assertIn("REPLACE_WITH_TAG", validation.stderr)


if __name__ == "__main__":
    unittest.main()
