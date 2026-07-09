"""Starter runtime for the quick-start and modular application."""

from __future__ import annotations

import os

import pandas as pd
import streamlit as st

from accessatlas.navigation import get_visible_tabs
from accessatlas.runtime import RuntimeContext
from accessatlas.scope import apply_role_scope


STARTER_USER_ID_ENV = "ACCESSATLAS_USER_ID"


def _resolve_starter_user(users: pd.DataFrame) -> pd.Series:
    """Resolve the configured starter identity without providing a demo selector."""
    configured_user_id = os.getenv(STARTER_USER_ID_ENV, "").strip()

    if configured_user_id:
        matching_users = users[users["user_id"] == configured_user_id]
        if matching_users.empty:
            raise ValueError(
                f"{STARTER_USER_ID_ENV}={configured_user_id!r} does not match a user_id "
                "in the current user dataset."
            )
        return matching_users.iloc[0]

    super_admins = users[
        (users["application_role"] == "Super Administrator")
        & (users["record_status"] == "Active")
    ]
    if not super_admins.empty:
        return super_admins.sort_values("user_id").iloc[0]

    active_users = users[users["record_status"] == "Active"]
    if not active_users.empty:
        return active_users.sort_values("user_id").iloc[0]

    if users.empty:
        raise ValueError("The user dataset is empty; AccessAtlas cannot resolve a starter identity.")

    return users.sort_values("user_id").iloc[0]


def build_starter_runtime(
    users: pd.DataFrame,
    systems: pd.DataFrame,
    access: pd.DataFrame,
    system_admins: pd.DataFrame,
) -> RuntimeContext:
    """Build the clean starter runtime from a configured application identity."""
    current_user = _resolve_starter_user(users)
    visible_tabs = get_visible_tabs(current_user["application_role"])

    scoped_users, scoped_systems, scoped_access, scoped_system_admins = apply_role_scope(
        users,
        systems,
        access,
        system_admins,
        current_user,
    )

    return RuntimeContext(
        current_user=current_user,
        visible_tabs=visible_tabs,
        users=scoped_users,
        systems=scoped_systems,
        access=scoped_access,
        system_admins=scoped_system_admins,
        runtime_name="starter",
        is_demo=False,
    )
