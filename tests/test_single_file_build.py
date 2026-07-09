"""Tests for the quick-start distribution build contract."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_builder_module():
    builder_path = ROOT / "tools" / "build_single_file.py"
    spec = importlib.util.spec_from_file_location("build_single_file", builder_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_generated_app_is_in_sync():
    """Committed root app.py must match the canonical modular source."""
    builder = _load_builder_module()
    expected = builder.build_single_file()
    actual = (ROOT / "app.py").read_text(encoding="utf-8")
    assert actual == expected


def test_generated_app_compiles():
    """The generated quick-start distribution must remain valid Python."""
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    compile(source, str(ROOT / "app.py"), "exec")


def test_reference_architecture_compiles():
    """Canonical modular Python sources must remain syntactically valid."""
    source_paths = [
        ROOT / "modular" / "app.py",
        *(ROOT / "modular" / "accessatlas").glob("*.py"),
    ]
    for source_path in source_paths:
        compile(
            source_path.read_text(encoding="utf-8"),
            str(source_path),
            "exec",
        )
