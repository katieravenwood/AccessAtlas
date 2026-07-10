"""Hosted demo runtime for AccessAtlas."""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st

from accessatlas.logging_config import get_logger, log_event, set_runtime_log_context
from accessatlas.navigation import get_visible_tabs
from accessatlas.runtime import RuntimeContext
from accessatlas.scope import apply_role_scope

logger = get_logger(__name__)


def _demo_user_options(users: pd.DataFrame) -> pd.DataFrame:
    """Return formatted synthetic user options for the demo selector."""
    demo_users = users.sort_values(["application_role", "display_name"]).copy()
    demo_users["demo_label"] = (
        demo_users["display_name"]
        + " — "
        + demo_users["application_role"]
        + " ("
        + demo_users["user_id"]
        + ")"
    )
    return demo_users[["user_id", "demo_label"]]


def _current_demo_user(users: pd.DataFrame, selected_label: str) -> pd.Series:
    """Return the synthetic user selected in the demo sidebar."""
    options = _demo_user_options(users)
    selected_user_id = options.loc[
        options["demo_label"] == selected_label,
        "user_id",
    ].iloc[0]
    return users[users["user_id"] == selected_user_id].iloc[0]


def _render_scope_summary(
    users: pd.DataFrame,
    systems: pd.DataFrame,
    access: pd.DataFrame,
    system_admins: pd.DataFrame,
) -> None:
    """Render the currently visible synthetic demo scope."""
    st.sidebar.markdown("### Visible Demo Scope")
    st.sidebar.write(
        f"""
        **Users:** {len(users)}  
        **Systems:** {len(systems)}  
        **Access Records:** {len(access)}  
        **Admin Assignments:** {len(system_admins)}
        """
    )


def render_demo_section_guidance(selected_section: str) -> None:
    """Render contextual sidebar guidance for the selected demo section."""
    guidance = {
        "Dashboard": {
            "title": "Dashboard Guidance",
            "body": """
            The dashboard shows a simplified health summary for the visible scope.

            Use it to spot compliance issues, access records, system coverage, and
            items that may need review.
            """,
        },
        "My Access": {
            "title": "My Access Guidance",
            "body": """
            My Access shows the selected user's own governance record, compliance
            dates, access assignments, and administrative assignments.

            Individual users see only this section.
            """,
        },
        "Manage Access": {
            "title": "Manage Access Guidance",
            "body": """
            Manage Access combines managed-user review, managed-system review, and
            scoped edit/add workflows.

            System Administrators see only users and systems in their administered
            scope. Super Administrators see all records.
            """,
        },
        "Access Reconciliation": {
            "title": "Access Reconciliation Guidance",
            "body": """
            Access Reconciliation contains system access and training-date
            reconciliation workflows.

            Use it to add, update, or inactivate access assignment records based on
            uploaded access exports.
            """,
        },
        "AccessAtlas App Admin": {
            "title": "AccessAtlas App Admin Guidance",
            "body": """
            AccessAtlas App Admin contains compliance monitoring and system
            administrator assignment views for Super Administrators.
            """,
        },
    }

    selected_guidance = guidance.get(selected_section)
    if selected_guidance is None:
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {selected_guidance['title']}")
    st.sidebar.info(selected_guidance["body"])


def build_demo_runtime(
    users: pd.DataFrame,
    systems: pd.DataFrame,
    access: pd.DataFrame,
    system_admins: pd.DataFrame,
) -> RuntimeContext:
    """Build the hosted synthetic demo runtime and render its sidebar controls."""
    st.sidebar.title("Demo Mode")
    st.sidebar.warning(
        "Demo Mode simulates role-based visibility and workflow behavior. "
        "It is not authentication or a production authorization mechanism."
    )
    st.sidebar.write(
        "Select an example user account to view the application from that role's perspective."
    )

    options = _demo_user_options(users)
    labels = options["demo_label"].tolist()
    default_index = next(
        (index for index, label in enumerate(labels) if label.startswith("Casey Rivera")),
        0,
    )
    selected_label = st.sidebar.selectbox(
        "View app as",
        labels,
        index=default_index,
    )
    current_user = _current_demo_user(users, selected_label)
    set_runtime_log_context(
        runtime_name="demo",
        application_role=str(current_user["application_role"]),
    )
    visible_tabs = get_visible_tabs(current_user["application_role"])

    st.sidebar.markdown("### Current Demo User")
    st.sidebar.write(
        f"""
        **Name:** {current_user["display_name"]}  
        **Role:** {current_user["application_role"]}  
        **User Type:** {current_user["user_type"]}  
        **Department:** {current_user["department"]}
        """
    )

    scoped_users, scoped_systems, scoped_access, scoped_system_admins = apply_role_scope(
        users,
        systems,
        access,
        system_admins,
        current_user,
    )
    _render_scope_summary(
        scoped_users,
        scoped_systems,
        scoped_access,
        scoped_system_admins,
    )

    st.info(
        f"Viewing as **{current_user['display_name']}** "
        f"with role **{current_user['application_role']}**. "
        "Visible sections and records are controlled by simulated demo-role rules."
    )

    log_event(
        logger,
        logging.INFO,
        "runtime_scope_resolved",
        "Demo runtime scope resolved.",
        visible_section_count=len(visible_tabs),
        visible_user_count=len(scoped_users),
        visible_system_count=len(scoped_systems),
        visible_access_count=len(scoped_access),
        visible_admin_assignment_count=len(scoped_system_admins),
    )

    return RuntimeContext(
        current_user=current_user,
        visible_tabs=visible_tabs,
        users=scoped_users,
        systems=scoped_systems,
        access=scoped_access,
        system_admins=scoped_system_admins,
        runtime_name="demo",
        is_demo=True,
        section_guidance_renderer=render_demo_section_guidance,
    )
