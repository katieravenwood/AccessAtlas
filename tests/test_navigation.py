"""Tests for top-level navigation and role visibility."""

from accessatlas.navigation import (
    get_visible_tabs,
    is_tab_visible,
    section_label,
    section_name_from_label,
)


def test_section_label_round_trip_for_known_sections():
    internal_name = "Overview"
    display_label = section_label(internal_name)

    assert section_name_from_label(display_label) == internal_name


def test_unknown_section_labels_pass_through_unchanged():
    assert section_label("Custom Section") == "Custom Section"
    assert section_name_from_label("Custom Section") == "Custom Section"


def test_unknown_role_falls_back_to_overview():
    assert get_visible_tabs("Unknown Role") == ["Overview"]


def test_is_tab_visible_uses_exact_internal_tab_name():
    visible_tabs = ["Overview", "Manage Access"]

    assert is_tab_visible("Manage Access", visible_tabs) is True
    assert is_tab_visible("My Access", visible_tabs) is False
