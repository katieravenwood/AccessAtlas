"""Build the root-level single-file AccessAtlas starter application.

The modular implementation under ``modular/`` is the engineering
source of truth. This script publishes a readable, self-contained ``app.py`` at
the repository root for quick-start users.

Run from the repository root:

    python tools/build_single_file.py

Use ``--check`` in CI to fail when the committed root ``app.py`` is out of sync.
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULAR_ROOT = ROOT / "modular"
PACKAGE_ROOT = MODULAR_ROOT / "accessatlas"
OUTPUT_PATH = ROOT / "app.py"

MODULE_ORDER = [
    "config.py",
    "logging_config.py",
    "compliance.py",
    "data.py",
    "navigation.py",
    "presentation.py",
    "scope.py",
    "state.py",
    "reconciliation.py",
    "runtime.py",
    "starter_runtime.py",
    "app_core.py",
]

HEADER = """\
from __future__ import annotations

# ---------------------------------------------------------------------------
# AccessAtlas single-file quick-start application
# ---------------------------------------------------------------------------
#
# GENERATED FILE — DO NOT EDIT AS THE ENGINEERING SOURCE OF TRUTH.
#
# Canonical source:
#   modular/app.py
#   modular/accessatlas/
#
# Rebuild after changing canonical source:
#   python tools/build_single_file.py
#
# Verify the committed quick-start file is current:
#   python tools/build_single_file.py --check
#
# This generated distribution publishes the clean starter runtime as one
# directly editable Streamlit file for quick-start adopters.
# Hosted demo controls remain only in modular/demo_app.py and demo_runtime.py.
# ---------------------------------------------------------------------------

"""


def _excluded_line_numbers(source: str) -> set[int]:
    """Return source lines to omit from a bundled module."""
    tree = ast.parse(source)
    excluded: set[int] = set()

    for index, node in enumerate(tree.body):
        is_module_docstring = (
            index == 0
            and isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )
        is_internal_import = (
            isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module.startswith("accessatlas")
        )
        is_future_import = (
            isinstance(node, ast.ImportFrom)
            and node.module == "__future__"
        )

        if is_module_docstring or is_internal_import or is_future_import:
            excluded.update(range(node.lineno, node.end_lineno + 1))

    return excluded


def _clean_source(path: Path) -> str:
    """Strip package-internal imports and module docstrings while preserving layout."""
    source = path.read_text(encoding="utf-8")
    excluded = _excluded_line_numbers(source)
    lines = [
        line
        for line_number, line in enumerate(source.splitlines(), start=1)
        if line_number not in excluded
    ]
    return "\n".join(lines).strip()


def build_single_file() -> str:
    """Return the generated single-file starter source."""
    sections = [HEADER.rstrip()]

    for module_name in MODULE_ORDER:
        module_path = PACKAGE_ROOT / module_name
        sections.append(
            "\n".join(
                [
                    f"# === Shared module: accessatlas/{module_name} ===",
                    _clean_source(module_path),
                ]
            )
        )

    sections.append(
        "\n".join(
            [
                "# === Streamlit application entry point ===",
                _clean_source(MODULAR_ROOT / "app.py"),
            ]
        )
    )

    return "\n\n\n".join(sections).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if root app.py differs from generated canonical source.",
    )
    args = parser.parse_args()

    generated = build_single_file()

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"{OUTPUT_PATH} does not exist.")
            return 1
        if OUTPUT_PATH.read_text(encoding="utf-8") != generated:
            print(
                "Root app.py is out of sync with modular/. "
                "Run: python tools/build_single_file.py"
            )
            return 1
        print("Root app.py is in sync with the canonical modular source.")
        return 0

    OUTPUT_PATH.write_text(generated, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
