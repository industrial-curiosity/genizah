"""Contract tests for the pull-request bundle-validation workflow."""

from __future__ import annotations

from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import re
import sys
import tempfile
import textwrap
from types import ModuleType
import unittest
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "validate-bundles.yml"


class ValidateBundlesWorkflowTests(unittest.TestCase):
    """Assert the safeguards that make the CI check authoritative and read-only."""

    def setUp(self):
        self.text = WORKFLOW_PATH.read_text(encoding="utf-8")

    def inline_python_script(self, step_name):
        step_marker = f"      - name: {step_name}\n"
        self.assertIn(step_marker, self.text)
        step_text = self.text.split(step_marker, maxsplit=1)[1]
        marker = "        run: |\n"
        self.assertIn(marker, step_text)
        return textwrap.dedent(step_text.split(marker, maxsplit=1)[1].split("\n      - name:", maxsplit=1)[0])

    def load_inline_python_step(self, step_name, module_name):
        script = self.inline_python_script(step_name)
        module = ModuleType(module_name)
        sys.modules[module_name] = module
        exec(compile(script, str(WORKFLOW_PATH), "exec"), module.__dict__)
        return module.__dict__

    def load_inline_python(self):
        return self.load_inline_python_step(
            "Test and validate bundle indexes",
            "validate_bundles_workflow_test",
        )

    def test_runs_for_each_pull_request_update_without_a_path_filter(self):
        self.assertIn("pull_request:", self.text)
        for event in ("opened", "reopened", "synchronize", "ready_for_review"):
            self.assertIn(event, self.text)
        workflow_header = self.text.split("permissions:", maxsplit=1)[0]
        self.assertNotRegex(workflow_header, r"(?m)^\s+paths:")
        self.assertIn("github.event.pull_request.number", self.text)

    def test_uses_the_exact_pull_request_head_with_read_only_checkout(self):
        self.assertIn("contents: read", self.text)
        self.assertIn("actions/checkout@v7.0.1", self.text)
        self.assertIn("actions/setup-python@v7.0.0", self.text)
        self.assertIn("python-version: '3.13'", self.text)
        self.assertIn("actions/setup-node@v6.4.0", self.text)
        self.assertIn("node-version: '18'", self.text)
        self.assertIn("ref: ${{ github.event.pull_request.head.sha }}", self.text)
        self.assertIn("fetch-depth: 0", self.text)
        self.assertIn("persist-credentials: false", self.text)
        self.assertNotIn("git push", self.text)
        self.assertNotIn("secrets.", self.text)

    def test_runs_repository_tests_before_selective_or_full_index_validation(self):
        self.assertIn("node --test tooling/npm/test/*.test.mjs", self.text)
        self.assertIn('["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]', self.text)
        self.assertIn('builder_arguments = ("python3", "scripts/build-index.py")', self.text)
        self.assertIn('"--bundles",', self.text)
        self.assertIn("list(plan.builder_arguments)", self.text)

    def test_reports_npm_test_failures_with_an_actionable_summary(self):
        self.assertIn("id: npm_tests", self.text)
        self.assertIn("continue-on-error: true", self.text)
        self.assertIn("if: always()", self.text)
        self.assertIn("steps.npm_tests.outcome", self.text)
        self.assertIn("GITHUB_STEP_SUMMARY", self.text)
        self.assertIn("::error::npm package tests failed.", self.text)

    def test_npm_failure_report_writes_annotation_and_summary(self):
        script = self.inline_python_script("Report npm package test result")
        with tempfile.TemporaryDirectory() as temporary_directory:
            summary_path = Path(temporary_directory) / "summary.md"
            output = io.StringIO()
            with patch.dict(
                os.environ,
                {
                    "NPM_TEST_OUTCOME": "failure",
                    "GITHUB_STEP_SUMMARY": str(summary_path),
                },
                clear=False,
            ), self.assertRaises(SystemExit), redirect_stdout(output):
                module = ModuleType("npm_failure_report_workflow_test")
                module.__dict__["__name__"] = "npm_failure_report_workflow_test"
                exec(compile(script, str(WORKFLOW_PATH), "exec"), module.__dict__)

            self.assertEqual(output.getvalue().strip(), "::error::npm package tests failed.")
            self.assertIn("Run `node --test tooling/npm/test/*.test.mjs`", summary_path.read_text(encoding="utf-8"))

    def test_compares_base_and_head_and_parses_nul_delimited_name_status(self):
        self.assertIn("github.event.pull_request.base.sha", self.text)
        self.assertIn("github.event.pull_request.head.sha", self.text)
        self.assertIn('"diff", "--name-status", "-z", base_sha, head_sha', self.text)
        self.assertIn("split(b\"\\0\")", self.text)
        self.assertIn("status.startswith", self.text)

    def test_uses_full_diff_to_detect_contract_changes_and_existing_bundles_for_selection(self):
        diff_calls = re.findall(r'\["git", "diff"[^\n]+', self.text)
        self.assertTrue(diff_calls, self.text)
        self.assertTrue(
            any("bundles/" not in diff_call for diff_call in diff_calls),
            "Contract/tool change detection must examine the whole repository diff.",
        )
        self.assertIn('root / "bundles" / bundle_id', self.text)
        self.assertIn("make_validation_plan", self.text)
        self.assertIn("scripts/", self.text)
        self.assertIn("templates/", self.text)
        self.assertIn("tests/", self.text)
        self.assertIn(".agents/skills/", self.text)
        self.assertIn("docs/bundle-format.md", self.text)
        self.assertIn(".github/workflows/validate-bundles.yml", self.text)

    def test_rebuilds_full_indexes_and_fails_for_any_tracked_or_untracked_tag_drift(self):
        self.assertIn('"status", "--porcelain=v1", "--untracked-files=all", "--", "tags/"', self.text)
        self.assertIn("GITHUB_STEP_SUMMARY", self.text)
        self.assertIn("::error::", self.text)
        self.assertIn("write_failure_summary", self.text)
        self.assertIn("current indexes", self.text.lower())

    def test_parses_status_records_and_selects_only_changed_targets(self):
        workflow = self.load_inline_python()
        payload = (
            b"A\0bundles/added/index.md\0"
            b"C100\0bundles/source/specification.md\0bundles/copied/specification.md\0"
            b"M\0bundles/modified/specification.md\0"
            b"R095\0bundles/old/index.md\0bundles/renamed/index.md\0"
            b"T\0bundles/type-changed/index.md\0"
            b"D\0bundles/deleted/old.md\0"
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for bundle_id in (
                "added",
                "source",
                "copied",
                "modified",
                "old",
                "renamed",
                "type-changed",
                "deleted",
            ):
                (root / "bundles" / bundle_id).mkdir(parents=True)

            changes = workflow["parse_name_status"](payload)
            plan = workflow["make_validation_plan"](changes, root)

        self.assertEqual(plan.selected_bundle_ids, (
            "added",
            "copied",
            "modified",
            "renamed",
            "type-changed",
        ))
        self.assertEqual(plan.deleted_paths, ("bundles/deleted/old.md",))
        self.assertNotIn("source", plan.selected_bundle_ids)
        self.assertNotIn("old", plan.selected_bundle_ids)
        self.assertNotIn("deleted", plan.selected_bundle_ids)

    def test_switches_between_selective_and_full_validation_plans(self):
        workflow = self.load_inline_python()
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            for bundle_id in ("alpha", "beta"):
                (root / "bundles" / bundle_id).mkdir(parents=True)

            selective = workflow["make_validation_plan"](
                [("M", "bundles/alpha/specification.md", "bundles/alpha/specification.md")],
                root,
            )
            full = workflow["make_validation_plan"](
                [("M", "scripts/build-index.py", "scripts/build-index.py")],
                root,
            )

        self.assertEqual(
            selective.builder_arguments,
            ("python3", "scripts/build-index.py", "--bundles", "alpha"),
        )
        self.assertEqual(selective.validated_bundle_ids, ("alpha",))
        self.assertEqual(full.builder_arguments, ("python3", "scripts/build-index.py"))
        self.assertEqual(full.validated_bundle_ids, ("alpha", "beta"))

    def test_failure_writes_annotation_and_actionable_summary(self):
        workflow = self.load_inline_python()
        with tempfile.TemporaryDirectory() as temporary_directory:
            summary_path = Path(temporary_directory) / "summary.md"
            workflow["summary_path"] = str(summary_path)
            output = io.StringIO()

            with self.assertRaises(SystemExit), redirect_stdout(output):
                workflow["fail"]("Validation broke.", ["bundles/alpha"])

            summary = summary_path.read_text(encoding="utf-8")

        self.assertIn("::error::Validation broke.", output.getvalue())
        self.assertIn("bundles/alpha", summary)
        self.assertIn("python3 scripts/build-index.py", summary)

    def test_tracked_and_untracked_tag_drift_each_fail(self):
        workflow = self.load_inline_python()
        for status_output in (
            " M tags/index.md\n",
            "?? tags/new-tag/index.md\n",
        ):
            with self.subTest(status_output=status_output), tempfile.TemporaryDirectory() as temporary_directory:
                summary_path = Path(temporary_directory) / "summary.md"
                workflow["summary_path"] = str(summary_path)
                with self.assertRaises(SystemExit), redirect_stdout(io.StringIO()):
                    workflow["fail_if_tag_drift"](status_output)
                self.assertIn("python3 scripts/build-index.py", summary_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
