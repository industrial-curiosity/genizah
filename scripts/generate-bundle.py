#!/usr/bin/env python3
"""Create an intentionally incomplete, author-owned OKF bundle scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Sequence


BUNDLE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOKEN_PATTERN = re.compile(r"\{\{[^{}]+\}\}")
REPLACEMENTS = ("{{BUNDLE_ID}}", "{{BUNDLE_TITLE}}")
REQUIRED_TEMPLATE_FILES = (
    Path("index.md"),
    Path("specification.md"),
    Path("validation.md"),
    Path("strategies/strategy.md"),
    Path("references/index.md"),
)


def derive_title(bundle_id: str) -> str:
    """Convert a lowercase kebab-case identifier into a display title."""
    return " ".join(part.capitalize() for part in bundle_id.split("-"))


def generate_bundle(root: Path, bundle_id: str, title: str) -> list[Path]:
    """Create one scaffold after every destination and template precondition holds."""
    root = _validate_root(root)
    _validate_bundle_id(bundle_id)
    title = _validate_title(title)
    template = _validate_template(root / "templates" / "bundle")
    destination = _validate_destination(root, bundle_id)

    bundles_root = destination.parent
    bundles_root.mkdir(exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{bundle_id}.", dir=bundles_root))
    created_destination = False
    try:
        staging.rmdir()
        shutil.copytree(template, staging)
        _replace_template_tokens(staging, bundle_id, title)
        try:
            destination.mkdir()
        except FileExistsError as error:
            raise ValueError(
                f"Bundle destination already exists: {destination}. "
                "Choose another ID or remove it yourself.",
            ) from error
        created_destination = True
        shutil.copytree(staging, destination, dirs_exist_ok=True)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        if created_destination:
            shutil.rmtree(destination, ignore_errors=True)
        raise

    shutil.rmtree(staging)

    return sorted(
        path.relative_to(root)
        for path in destination.rglob("*")
        if path.is_file()
    )


def _validate_root(root: Path) -> Path:
    if not isinstance(root, Path):
        raise ValueError("Repository root must be a pathlib.Path.")
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"Repository root must be an existing directory: {root}")
    return root.resolve()


def _validate_bundle_id(bundle_id: str) -> None:
    if not isinstance(bundle_id, str) or not BUNDLE_ID_PATTERN.fullmatch(bundle_id):
        raise ValueError("Bundle identifiers must use lowercase kebab-case.")


def _validate_title(title: str) -> str:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Bundle title must be non-empty.")
    return title.strip()


def _validate_template(template: Path) -> Path:
    if template.is_symlink() or not template.is_dir():
        raise ValueError(f"Bundle template directory does not exist: {template}")
    for relative_path in REQUIRED_TEMPLATE_FILES:
        source = template / relative_path
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Bundle template is missing required file: {source}")
    for source in sorted(template.rglob("*")):
        if source.is_symlink():
            raise ValueError(f"Bundle template must not contain symbolic links: {source}")
        if not source.is_file():
            continue
        for token in TOKEN_PATTERN.findall(source.read_text(encoding="utf-8")):
            if token not in REPLACEMENTS:
                raise ValueError(f"Bundle template contains unsupported replacement token: {token}")
    return template


def _validate_destination(root: Path, bundle_id: str) -> Path:
    bundles_root = root / "bundles"
    if bundles_root.is_symlink() or (bundles_root.exists() and not bundles_root.is_dir()):
        raise ValueError(f"Bundle destination parent must be a directory: {bundles_root}")
    destination = bundles_root / bundle_id
    if destination.exists() or destination.is_symlink():
        raise ValueError(
            f"Bundle destination already exists: {destination}. "
            "Choose another ID or remove it yourself.",
        )
    return destination


def _replace_template_tokens(destination: Path, bundle_id: str, title: str) -> None:
    for path in sorted(path for path in destination.rglob("*") if path.is_file()):
        contents = path.read_text(encoding="utf-8")
        path.write_text(
            contents.replace("{{BUNDLE_ID}}", bundle_id).replace("{{BUNDLE_TITLE}}", title),
            encoding="utf-8",
        )


def main(argv: Sequence[str] | None = None) -> int:
    """Parse CLI arguments, generate a bundle, and report actionable errors."""
    parser = argparse.ArgumentParser(description="Create an incomplete OKF bundle scaffold.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root containing templates/ and bundles/",
    )
    parser.add_argument("bundle_id", metavar="BUNDLE_ID", help="lowercase kebab-case bundle identifier")
    parser.add_argument("--title", metavar="DISPLAY_TITLE", help="display title; defaults to the bundle identifier")
    arguments = parser.parse_args(argv)
    title = arguments.title if arguments.title is not None else derive_title(arguments.bundle_id)
    try:
        created_paths = generate_bundle(arguments.root, arguments.bundle_id, title)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    for path in created_paths:
        print(f"Created: {path.as_posix()}")
    print("Next: replace every REPLACE_ marker, then run python3 scripts/build-index.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
