"""Tests for session-backed record state and identifier generation."""

import json

import pandas as pd
import streamlit as st

from accessatlas.audit import get_audit_events, set_audit_actor_context
from accessatlas.state import (
    access_key_mask,
    add_user_record,
    apply_user_compliance_updates,
    generate_next_access_id,
    generate_next_user_id,
    get_editable_access_assignments,
    get_editable_users,
    update_user_compliance_dates,
)


def setup_function():
    st.session_state.clear()
    set_audit_actor_context("ACTOR", "Super Administrator", "starter")


def test_generate_next_user_id_handles_mixed_and_missing_identifiers():
    users = pd.DataFrame(
        {"user_id": ["USR00002", "legacy", None, "USR00010"]}
    )

    assert generate_next_user_id(users) == "USR00011"


def test_generate_next_access_id_handles_empty_numeric_suffixes():
    access = pd.DataFrame({"access_id": ["legacy", None]})

    assert generate_next_access_id(access) == "A001"


def test_get_editable_users_returns_copy_of_session_state():
    users = pd.DataFrame([{"user_id": "USR00001", "record_status": "Active"}])

    returned = get_editable_users(users)
    returned.loc[0, "record_status"] = "Inactive"

    assert st.session_state["editable_users"].loc[0, "record_status"] == "Active"


def test_get_editable_access_assignments_returns_copy_of_session_state():
    access = pd.DataFrame([{"access_id": "A001", "access_status": "Active"}])

    returned = get_editable_access_assignments(access)
    returned.loc[0, "access_status"] = "Inactive"

    assert (
        st.session_state["editable_access_assignments"].loc[0, "access_status"]
        == "Active"
    )


def test_update_compliance_dates_applies_override_and_records_audit_event():
    users = pd.DataFrame(
        [
            {
                "user_id": "USR00001",
                "annual_training_date": pd.Timestamp("2025-01-01"),
                "biennial_training_date": pd.Timestamp("2025-01-01"),
                "access_agreement_date": pd.Timestamp("2025-01-01"),
            }
        ]
    )

    event = update_user_compliance_dates(
        "USR00001",
        "2026-01-01",
        "2026-02-01",
        "2026-03-01",
    )
    updated = apply_user_compliance_updates(users)
    audit_events = get_audit_events()

    assert updated.iloc[0]["annual_training_date"] == pd.Timestamp("2026-01-01")
    assert event.action == "update_compliance_dates"
    assert len(audit_events) == 1
    assert audit_events.iloc[0]["target_user_id"] == "USR00001"


def test_add_user_record_rejects_duplicate_without_audit_event():
    st.session_state["editable_users"] = pd.DataFrame(
        [{"user_id": "USR00001"}]
    )

    result = add_user_record(
        "USR00001",
        "Alex",
        "Example",
        "alex@example.test",
        "User",
        "",
        "Operations",
        "Employee",
        "Active",
        "2026-01-01",
        "2026-01-01",
        "2026-01-01",
    )

    assert result == "duplicate"
    assert get_audit_events().empty


def test_add_user_record_creates_display_name_and_audit_event():
    st.session_state["editable_users"] = pd.DataFrame(
        columns=[
            "user_id",
            "display_name",
            "first_name",
            "last_name",
            "email",
            "application_role",
            "manager_user_id",
            "department",
            "user_type",
            "record_status",
            "annual_training_date",
            "biennial_training_date",
            "access_agreement_date",
            "created_date",
            "updated_date",
        ]
    )

    result = add_user_record(
        "USR00001",
        "Alex",
        "Example",
        "alex@example.test",
        "User",
        "",
        "Operations",
        "Employee",
        "Active",
        "2026-01-01",
        "2026-01-01",
        "2026-01-01",
    )

    created = st.session_state["editable_users"].iloc[0]
    audit_events = get_audit_events()

    assert result == "added"
    assert created["display_name"] == "Alex Example"
    assert len(audit_events) == 1
    assert audit_events.iloc[0]["action"] == "create_user"
    changes = json.loads(audit_events.iloc[0]["changes_json"])
    assert changes["after"]["email"] == "alex@example.test"


def test_access_key_mask_matches_full_access_identity():
    access = pd.DataFrame(
        [
            {
                "user_id": "USR00001",
                "system_id": "SYS1",
                "resource_type": "Database",
                "resource_name": "Warehouse",
                "permission_name": "Read",
            },
            {
                "user_id": "USR00001",
                "system_id": "SYS1",
                "resource_type": "Database",
                "resource_name": "Warehouse",
                "permission_name": "Write",
            },
        ]
    )
    row = pd.Series(
        {
            "user_id": "USR00001",
            "system_id": "SYS1",
            "resource_type": "Database",
            "resource_name": "Warehouse",
            "permission_name": "Read",
        }
    )

    mask = access_key_mask(access, row)

    assert mask.tolist() == [True, False]
