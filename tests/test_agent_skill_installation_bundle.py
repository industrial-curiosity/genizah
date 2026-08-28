"""Regression checks for the agent skill installation bundle."""

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = REPOSITORY_ROOT / "bundles" / "ai-agent-skill-installation"


class AgentSkillInstallationBundleTests(unittest.TestCase):
    """Ensure the portable installer contract remains discoverable."""

    def test_skill_installation_bundle_indexes_its_reference(self):
        """The bundle must expose the compatibility evidence it relies on."""
        index = (BUNDLE_ROOT / "index.md").read_text(encoding="utf-8")

        self.assertIn("references/agentskills-support.md", index)
        self.assertTrue((BUNDLE_ROOT / "references" / "agentskills-support.md").is_file())

    def test_bundle_preserves_the_portable_location_invariants(self):
        """The installer must retain its choice and containment guarantees."""
        specification = (BUNDLE_ROOT / "specification.md").read_text(encoding="utf-8")

        for phrase in (
            "before writing skill files",
            "one selected destination",
            "noninteractive override",
            "default project-level location",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, specification)


if __name__ == "__main__":
    unittest.main()
