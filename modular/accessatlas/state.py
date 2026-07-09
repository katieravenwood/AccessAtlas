"""AccessAtlas application module."""

from datetime import date

import pandas as pd
import streamlit as st

def initialize_user_update_state():
    """Initialize session state used for demo self-service updates."""
    if "user_compliance_updates" not in st.session_state:
        st.session_state["user_compliance_updates"] = {}

def apply_user_compliance_updates(users):
    """Apply in-session user compliance updates to the user dataset."""
    initialize_user_update_state()
    users = users.copy()

    for user_id, updates in st.session_state["user_compliance_updates"].items():
        user_mask = users["user_id"] == user_id
        if not user_mask.any():
            continue

        for column_name, value in updates.items():
            users.loc[user_mask, column_name] = pd.Timestamp(value)

    return users

def update_user_compliance_dates(
    user_id,
    annual_training_date,
    biennial_training_date,
    access_agreement_date,
):
    """Store user-submitted compliance date updates in session state."""
    initialize_user_update_state()
    st.session_state["user_compliance_updates"][user_id] = {
        "annual_training_date": annual_training_date,
        "biennial_training_date": biennial_training_date,
        "access_agreement_date": access_agreement_date,
    }

def initialize_editable_user_state(users):
    """Initialize session-state backed user records for demo user management."""
    if "editable_users" not in st.session_state:
        st.session_state["editable_users"] = users.copy()

def get_editable_users(users):
    """Return session-state user records, initializing them if needed."""
    initialize_editable_user_state(users)
    return st.session_state["editable_users"].copy()

def generate_next_user_id(users_df):
    """Generate the next synthetic user ID."""
    existing_numbers = (
        users_df["user_id"]
        .dropna()
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if existing_numbers.empty else existing_numbers.max() + 1
    return f"USR{next_number:05d}"

def add_user_record(
    user_id,
    first_name,
    last_name,
    email,
    application_role,
    manager_user_id,
    department,
    user_type,
    record_status,
    annual_training_date,
    biennial_training_date,
    access_agreement_date,
):
    """Add one synthetic user record to the session-state user registry."""
    current_users = st.session_state["editable_users"].copy()

    if user_id in current_users["user_id"].tolist():
        return "duplicate"

    display_name = f"{first_name} {last_name}".strip()
    today = pd.Timestamp(date.today())

    new_user = {
        "user_id": user_id,
        "display_name": display_name,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "application_role": application_role,
        "manager_user_id": manager_user_id,
        "department": department,
        "user_type": user_type,
        "record_status": record_status,
        "annual_training_date": pd.Timestamp(annual_training_date),
        "biennial_training_date": pd.Timestamp(biennial_training_date),
        "access_agreement_date": pd.Timestamp(access_agreement_date),
        "created_date": today,
        "updated_date": today,
    }

    st.session_state["editable_users"] = pd.concat(
        [current_users, pd.DataFrame([new_user])],
        ignore_index=True,
    )
    return "added"

def initialize_editable_access_state(access):
    """Initialize session-state backed access assignments for demo CRUD actions."""
    if "editable_access_assignments" not in st.session_state:
        st.session_state["editable_access_assignments"] = access.copy()

def get_editable_access_assignments(access):
    """Return session-state access assignments, initializing them if needed."""
    initialize_editable_access_state(access)
    return st.session_state["editable_access_assignments"].copy()

def generate_next_access_id(access_df):
    """Generate the next synthetic access assignment ID."""
    existing_numbers = (
        access_df["access_id"]
        .dropna()
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if existing_numbers.empty else existing_numbers.max() + 1
    return f"A{next_number:03d}"

def access_key_mask(access_df, row):
    """Return a boolean mask matching an access row by the reconciliation key."""
    return (
        (access_df["user_id"] == row["user_id"])
        & (access_df["system_id"] == row["system_id"])
        & (access_df["resource_type"] == row["resource_type"])
        & (access_df["resource_name"] == row["resource_name"])
        & (access_df["permission_name"] == row["permission_name"])
    )
