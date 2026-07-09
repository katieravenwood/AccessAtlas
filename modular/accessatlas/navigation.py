"""AccessAtlas application module."""

from accessatlas.config import ROLE_VISIBLE_TABS, TAB_DISPLAY_LABELS

def section_label(tab_name):
    """Return the display label for a top-level section."""
    return TAB_DISPLAY_LABELS.get(tab_name, tab_name)

def section_name_from_label(display_label):
    """Return the internal section name for a top-level display label."""
    reverse_labels = {
        display_value: internal_name
        for internal_name, display_value in TAB_DISPLAY_LABELS.items()
    }
    return reverse_labels.get(display_label, display_label)

def get_visible_tabs(application_role):
    """Return the tab labels visible to the selected demo role."""
    return ROLE_VISIBLE_TABS.get(application_role, ["Overview"])

def is_tab_visible(tab_name, visible_tabs):
    """Return whether a tab should be rendered for the selected demo role."""
    return tab_name in visible_tabs
