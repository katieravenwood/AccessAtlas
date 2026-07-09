"""Tests for starter/demo runtime separation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_generated_starter_contains_no_demo_sidebar_controls():
    """The root quick-start distribution must not publish Demo Mode UI."""
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'st.sidebar.title("Demo Mode")' not in source
    assert '"View app as"' not in source
    assert "Current Demo User" not in source
    assert "Visible Demo Scope" not in source


def test_demo_runtime_retains_demo_controls():
    """The modular hosted demo must keep the persona selector and scope preview."""
    source = (
        ROOT / "modular" / "accessatlas" / "demo_runtime.py"
    ).read_text(encoding="utf-8")
    assert 'st.sidebar.title("Demo Mode")' in source
    assert '"View app as"' in source
    assert "Current Demo User" in source
    assert "Visible Demo Scope" in source


def test_entry_points_select_distinct_runtime_factories():
    """Starter and demo entry points must use separate runtime factories."""
    starter_source = (ROOT / "modular" / "app.py").read_text(encoding="utf-8")
    demo_source = (ROOT / "modular" / "demo_app.py").read_text(encoding="utf-8")

    assert "build_starter_runtime" in starter_source
    assert "build_demo_runtime" not in starter_source
    assert "build_demo_runtime" in demo_source
    assert "build_starter_runtime" not in demo_source
