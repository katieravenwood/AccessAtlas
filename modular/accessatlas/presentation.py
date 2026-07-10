"""AccessAtlas application module."""

import pandas as pd
import streamlit as st

from accessatlas.config import COLUMN_LABELS


def section_caption(text):
    """Render standard section-level instruction text."""
    st.caption(text)


def filter_caption(text):
    """Render standard filter instruction text."""
    st.caption(text)


def apply_multiselect_filter(dataframe, column_name, selected_values):
    """Filter a DataFrame by selected values from a multiselect widget."""
    if not selected_values:
        return dataframe
    return dataframe[dataframe[column_name].isin(selected_values)]


def count_by(dataframe, columns, count_name="records"):
    """Return grouped counts for one or more columns."""
    if isinstance(columns, str):
        columns = [columns]
    return dataframe.groupby(columns).size().reset_index(name=count_name)


def display_table(dataframe):
    """Return a copy of a dataframe with user-friendly column labels."""
    return dataframe.rename(columns=COLUMN_LABELS)


def show_dataframe(dataframe, **kwargs):
    """Render a dataframe with user-friendly column labels and clean defaults."""
    kwargs.setdefault("hide_index", True)
    kwargs.setdefault("width", "stretch")
    st.dataframe(
        display_table(dataframe),
        **kwargs,
    )


def get_display_name(users, user_id):
    """Return a display name for a user ID when available."""
    if pd.isna(user_id) or user_id == "":
        return "Not assigned"
    match = users[users["user_id"] == user_id]
    if match.empty:
        return "Not assigned"
    return match.iloc[0]["display_name"]


def user_profile_markdown(selected_user, manager_name):
    """Build the selected user profile markdown block."""
    return f"""
    **User ID:** {selected_user["user_id"]}  
    **Email:** {selected_user["email"]}  
    **Department:** {selected_user["department"]}  
    **User Type:** {selected_user["user_type"]}  
    **Application Role:** {selected_user["application_role"]}  
    **Manager:** {manager_name}  
    **Record Status:** {selected_user["record_status"]}  
    **Compliance Status:** {selected_user["compliance_status"]}
    """


def system_profile_markdown(selected_system):
    """Build the selected system profile markdown block."""
    return f"""
    **System ID:** {selected_system["system_id"]}  
    **System Type:** {selected_system["system_type"]}  
    **System Category:** {selected_system["system_category"]}  
    **Resource Scope:** {selected_system["resource_scope"]}  
    **Access Model:** {selected_system["access_model"]}  
    **Tracking Method:** {selected_system["tracking_method"]}  
    **System Owner:** {selected_system["system_owner"]}  
    **Admin Group:** {selected_system["admin_group"]}  
    **Record Status:** {selected_system["record_status"]}  
    **Notes:** {selected_system["notes"]}
    """
