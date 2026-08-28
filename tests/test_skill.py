"""Structural tests for the portable specification-customization skill."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPOSITORY_ROOT / ".agents" / "skills" / "customize-spec-bundle"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
EXPECTED_DESCRIPTION = (
    "Use when a user asks to apply, adapt, or customize a specification bundle "
    "for a concrete implementation, or explicitly invokes this skill."
)
REQUIRED_REFERENCES = (
    "references/interview-coverage.md",
    "references/output-contract.md",
)
FORBIDDEN_HOST_DETAILS = ("/Users/", "~/.agents/", ".cursor/", "Composer")


class CustomizeSpecBundleSkillTests(unittest.TestCase):
    """Verify the skill is complete, discoverable, and portable."""

    def read_skill(self) -> tuple[dict[str, str], str]:
        """Return the simple scalar frontmatter and Markdown body."""
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"), "SKILL.md must start with YAML frontmatter")
        _, frontmatter_text, body = text.split("---", maxsplit=2)
        frontmatter = {}
        for line in frontmatter_text.strip().splitlines():
            key, separator, value = line.partition(":")
            self.assertTrue(separator, f"Invalid frontmatter line: {line!r}")
            frontmatter[key.strip()] = value.strip()
        return frontmatter, body

    def test_skill_has_required_frontmatter(self):
        frontmatter, _ = self.read_skill()

        self.assertEqual(frontmatter.get("type"), "Agent Skill")
        self.assertEqual(frontmatter.get("name"), "customize-spec-bundle")
        self.assertEqual(frontmatter.get("description"), EXPECTED_DESCRIPTION)
        for field in ("type", "name", "description"):
            self.assertTrue(frontmatter.get(field), f"Missing non-empty {field!r} frontmatter")

    def test_skill_description_covers_every_entry_point(self):
        frontmatter, body = self.read_skill()
        description = frontmatter["description"].lower()

        for trigger in ("apply", "adapt", "customize"):
            self.assertIn(trigger, description)
        self.assertIn("explicit", body.lower())

    def test_skill_has_no_machine_or_host_specific_paths(self):
        paths = [SKILL_PATH, *(
            SKILL_ROOT / relative_path for relative_path in REQUIRED_REFERENCES
        )]
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8")
                for forbidden in FORBIDDEN_HOST_DETAILS:
                    self.assertNotIn(forbidden, text)

    def test_skill_body_enforces_the_customization_workflow(self):
        _, body = self.read_skill()
        normalized = " ".join(body.lower().split())

        required_phrases = (
            "read the bundle index first",
            "load only",
            "inspect discoverable",
            "one unresolved question per turn",
            "discovered facts",
            "user decisions",
            "deliberate deviation",
            "unresolved blocker",
            "unknown optional concept types",
            "conversation by default",
            "user review",
            "explicit path",
            "explicit request",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, normalized)

    def test_skill_treats_implementation_samples_as_optional_and_illustrative(self):
        _, body = self.read_skill()
        normalized = " ".join(body.lower().split())

        for phrase in (
            "implementation samples are optional",
            "illustrative and non-normative",
            "do not run or port sample tests",
            "validation concepts define conformance",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, normalized)

    def test_required_references_exist_and_are_okf_guides(self):
        for relative_path in REQUIRED_REFERENCES:
            with self.subTest(relative_path=relative_path):
                reference_path = SKILL_ROOT / relative_path
                self.assertTrue(reference_path.is_file(), f"Missing {relative_path}")
                text = reference_path.read_text(encoding="utf-8")
                self.assertRegex(text, r"(?m)^type: Guide$")
                self.assertRegex(text, r"(?m)^# .+")

    def test_skill_has_no_missing_local_markdown_links(self):
        text = SKILL_PATH.read_text(encoding="utf-8")
        local_links = [
            target
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
            if "://" not in target and not target.startswith("#")
        ]

        self.assertEqual(sorted(local_links), sorted(REQUIRED_REFERENCES))
        for target in local_links:
            self.assertTrue((SKILL_ROOT / target).is_file(), f"Missing linked resource: {target}")

    def test_output_contract_defines_exact_section_order(self):
        output_contract = (SKILL_ROOT / "references" / "output-contract.md").read_text(
            encoding="utf-8",
        )
        headings = re.findall(r"(?m)^#{1,3} .+$", output_contract)

        self.assertEqual(headings, [
            "# Customization output contract",
            "## Target implementation profile",
            "### Discovered facts",
            "### User decisions",
            "### Bundle invariants retained",
            "### Deliberate deviations",
            "### Unresolved questions",
            "## Customized specification draft",
            "### Purpose",
            "### Target environment",
            "### Requirements",
            "### Selected strategies",
            "### Failure behavior",
            "### Acceptance scenarios",
            "### Provenance",
        ])

    def test_interview_coverage_defines_domains_and_completion_criteria(self):
        interview_coverage = " ".join((
            SKILL_ROOT / "references" / "interview-coverage.md"
        ).read_text(encoding="utf-8").lower().split())

        for domain in (
            "domain",
            "language and runtime",
            "integration",
            "data and persistence",
            "determinism and compatibility",
            "security",
            "scale and performance",
            "operations",
            "failure policy",
            "testing",
            "excluded scope",
        ):
            with self.subTest(domain=domain):
                self.assertIn(domain, interview_coverage)
        for outcome in (
            "recorded fact",
            "user decision",
            "explicit deviation",
            "unresolved blocker",
        ):
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, interview_coverage)

    def test_eval_inventory_covers_required_scenarios(self):
        eval_path = SKILL_ROOT / "evals" / "evals.json"
        payload = json.loads(eval_path.read_text(encoding="utf-8"))
        evals = payload["evals"]

        self.assertGreaterEqual(len(evals), 6)
        self.assertEqual(len({case["id"] for case in evals}), len(evals))
        required_ids = {
            "new-project",
            "existing-repository",
            "conflicting-requirements",
            "rejected-invariant",
            "user-stops-answering",
            "unknown-optional-concept-type",
            "illustrative-implementation-sample",
        }
        self.assertTrue(required_ids.issubset({case["id"] for case in evals}))
        for case in evals:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"].strip())
                self.assertGreaterEqual(len(case["assertions"]), 2)
                self.assertTrue(all(assertion.strip() for assertion in case["assertions"]))

    def test_eval_assertions_cover_each_baseline_failure(self):
        eval_path = SKILL_ROOT / "evals" / "evals.json"
        cases = {
            case["id"]: " ".join(case["assertions"]).lower()
            for case in json.loads(eval_path.read_text(encoding="utf-8"))["evals"]
        }
        expected_terms = {
            "new-project": ("one", "question", "invent"),
            "existing-repository": ("inspect", "before", "question"),
            "conflicting-requirements": ("tradeoff", "decision"),
            "rejected-invariant": ("deliberate deviation", "provenance"),
            "user-stops-answering": ("unresolved", "invent"),
            "unknown-optional-concept-type": ("tolerate", "progressive"),
        }
        for case_id, terms in expected_terms.items():
            with self.subTest(case_id=case_id):
                assertions = cases[case_id]
                for term in terms:
                    self.assertIn(term, assertions)


if __name__ == "__main__":
    unittest.main()
