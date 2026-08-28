"""Repository-level content invariants for the initial specification bundle."""

from __future__ import annotations

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INITIAL_BUNDLE = REPOSITORY_ROOT / "bundles" / "versioned-procedural-map-generation"


class InitialBundleContentTests(unittest.TestCase):
    """Keep the initial bundle technology-neutral and sample-free."""

    def test_initial_bundle_contains_no_implementation_samples(self):
        self.assertFalse(
            (INITIAL_BUNDLE / "references").exists(),
            "The initial bundle must not retain an implementation-sample directory.",
        )
        self.assertEqual(
            list(INITIAL_BUNDLE.rglob("*.cs")),
            [],
            "The initial bundle must not retain C# sample source or tests.",
        )
        index = (INITIAL_BUNDLE / "index.md").read_text(encoding="utf-8")
        self.assertNotIn("## References", index)


if __name__ == "__main__":
    unittest.main()
