"""Edge-case and outcome tests for AccessAtlas reconciliation."""

import json

import pandas as pd
import pytest
import streamlit as st
from accessatlas.audit import get_audit_events, set_audit_actor_context
from accessatlas.reconciliation import (
    apply_reconciliation_action,
    apply_reconciliation_actions,
    apply_training_date_actions,
    reconcile,
    reconcile_training_dates,
    validate_upload,
)

ACCESS_COLUMNS = [
    "access_id",
    "user_id",
    "system_id",
    "resource_type",
    "resource_name",
    "permission_name",
    "access_status",
    "granted_date",
    "revoked_date",
    "source",
]


def setup_function():
    st.session_state.clear()
    set_audit_actor_context("ADMIN", "System Administrator", "starter")


def _access(records):
    return pd.DataFrame(records, columns=ACCESS_COLUMNS)


def _access_row(
    *,
    access_id="A001",
    user_id="USR1",
    system_id="SYS1",
    permission_name="Read",
    access_status="Active",
):
    return {
        "access_id": access_id,
        "user_id": user_id,
        "system_id": system_id,
        "resource_type": "Database",
        "resource_name": "Warehouse",
        "permission_name": permission_name,
        "access_status": access_status,
        "granted_date": pd.Timestamp("2026-01-01"),
        "revoked_date": pd.NaT,
        "source": "Seed",
    }


def test_validate_upload_returns_required_columns_in_requested_order():
    upload = pd.DataFrame(columns=["user_id"])

    missing = validate_upload(
        upload,
        ["system_id", "user_id", "permission_name"],
    )

    assert missing == ["system_id", "permission_name"]


def test_reconcile_preserves_source_record_id_when_optional_name_columns_absent():
    current = _access([_access_row()])
    upload = pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "system_id": "SYS1",
                "resource_type": "Database",
                "resource_name": "Warehouse",
                "permission_name": "Read",
                "access_status": "Inactive",
                "source_system_record_id": "SRC-101",
            }
        ]
    )

    result = reconcile(current, upload, selected_system_id="SYS1")

    assert result.iloc[0]["source_system_record_id"] == "SRC-101"
    assert result.iloc[0]["change_type"] == "Status Changed"


def test_reconcile_selected_system_does_not_inactivate_other_system_records():
    current = _access(
        [
            _access_row(system_id="SYS1"),
            _access_row(
                access_id="A002",
                system_id="SYS2",
                permission_name="Write",
            ),
        ]
    )
    upload = pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "system_id": "SYS1",
                "resource_type": "Database",
                "resource_name": "Warehouse",
                "permission_name": "Read",
                "access_status": "Active",
            }
        ]
    )

    result = reconcile(current, upload, selected_system_id="SYS1")

    assert set(result["system_id"]) == {"SYS1"}
    assert "Access Not Found in Upload" not in set(result["change_type"])


def test_reconcile_raises_when_no_compatible_key_columns_exist():
    current = pd.DataFrame([{"alpha": "one", "access_status": "Active"}])
    upload = pd.DataFrame([{"beta": "two", "access_status": "Active"}])

    with pytest.raises(KeyError, match="no matching key columns"):
        reconcile(current, upload)


def test_apply_new_access_generates_next_id_without_mutating_source():
    source = _access([_access_row(access_id="A009")])
    row = pd.Series(
        {
            "user_id": "USR2",
            "system_id": "SYS1",
            "resource_type": "Dashboard",
            "resource_name": "Metrics",
            "permission_name": "View",
            "uploaded_access_status": "Active",
            "change_type": "New Access in Upload",
        }
    )

    updated, outcome = apply_reconciliation_action(source, row)

    assert outcome == "added"
    assert len(source) == 1
    assert len(updated) == 2
    assert updated.iloc[-1]["access_id"] == "A010"


def test_apply_missing_access_sets_inactive_and_revoked_date():
    source = _access([_access_row()])
    row = pd.Series(
        {
            **_access_row(),
            "change_type": "Access Not Found in Upload",
            "current_access_status": "Active",
            "uploaded_access_status": None,
        }
    )

    updated, outcome = apply_reconciliation_action(source, row)

    assert outcome == "inactivated"
    assert updated.iloc[0]["access_status"] == "Inactive"
    assert pd.notna(updated.iloc[0]["revoked_date"])


def test_apply_status_change_to_active_clears_revoked_date():
    source = _access([_access_row(access_status="Inactive")])
    source.loc[0, "revoked_date"] = pd.Timestamp("2026-05-01")
    row = pd.Series(
        {
            **_access_row(access_status="Inactive"),
            "change_type": "Status Changed",
            "current_access_status": "Inactive",
            "uploaded_access_status": "Active",
        }
    )

    updated, outcome = apply_reconciliation_action(source, row)

    assert outcome == "updated"
    assert updated.iloc[0]["access_status"] == "Active"
    assert pd.isna(updated.iloc[0]["revoked_date"])


def test_apply_reconciliation_actions_records_audit_only_for_changed_rows():
    access = _access([_access_row()])
    selected_rows = pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "system_id": "SYS1",
                "resource_type": "Database",
                "resource_name": "Warehouse",
                "permission_name": "Read",
                "current_access_status": "Active",
                "uploaded_access_status": "Inactive",
                "change_type": "Status Changed",
                "recommended_action": "Update access status",
                "source_system_record_id": "SRC-1",
            },
            {
                "user_id": "USR1",
                "system_id": "SYS1",
                "resource_type": "Database",
                "resource_name": "Warehouse",
                "permission_name": "Read",
                "current_access_status": "Inactive",
                "uploaded_access_status": "Inactive",
                "change_type": "No Change",
                "recommended_action": "No action",
                "source_system_record_id": "SRC-1",
            },
        ]
    )

    updated, counts, results = apply_reconciliation_actions(access, selected_rows)
    audit_events = get_audit_events()

    assert counts == {"added": 0, "inactivated": 0, "updated": 1, "skipped": 1}
    assert len(results) == 2
    assert results.iloc[0]["audit_event_id"].startswith("AUD-")
    assert results.iloc[1]["audit_event_id"] == ""
    assert len(audit_events) == 1
    assert audit_events.iloc[0]["action"] == "reconciliation_updated"
    changes = json.loads(audit_events.iloc[0]["changes_json"])
    assert changes["source_system_record_id"] == "SRC-1"
    assert updated.iloc[0]["access_status"] == "Inactive"


def _training_users():
    return pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "record_status": "Active",
                "annual_training_date": pd.Timestamp("2026-01-01"),
                "biennial_training_date": pd.Timestamp("2026-01-01"),
                "access_agreement_date": pd.Timestamp("2026-01-01"),
            }
        ]
    )


def test_training_reconcile_identifies_user_missing_from_registry():
    upload = pd.DataFrame(
        [
            {
                "user_id": "USR2",
                "annual_training_date": "2026-01-01",
                "biennial_training_date": "2026-01-01",
                "access_agreement_date": "2026-01-01",
            }
        ]
    )

    result = reconcile_training_dates(_training_users(), upload)
    missing = result[result["user_id"] == "USR2"].iloc[0]

    assert missing["change_type"] == "User Not Found in AccessAtlas"
    assert missing["recommended_action"] == "Review user record"


def test_training_reconcile_identifies_date_change_for_compliant_upload():
    upload = pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "annual_training_date": pd.Timestamp.today().normalize(),
                "biennial_training_date": pd.Timestamp.today().normalize(),
                "access_agreement_date": "2026-02-01",
            }
        ]
    )

    result = reconcile_training_dates(_training_users(), upload)

    assert result.iloc[0]["change_type"] == "Date Changed"
    assert result.iloc[0]["recommended_action"] == "Update date records"


def test_training_actions_update_dates_and_emit_compliance_audit_event():
    st.session_state["editable_users"] = _training_users()
    selected_rows = pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "current_record_status": "Active",
                "change_type": "Date Changed",
                "recommended_action": "Update date records",
                "changes_identified": "annual_training_date changed",
                "uploaded_annual_training_date": "2026-05-01",
                "uploaded_biennial_training_date": "2026-05-01",
                "uploaded_access_agreement_date": "2026-05-01",
            }
        ]
    )

    counts, results = apply_training_date_actions(selected_rows)
    audit_events = get_audit_events()

    assert counts == {"updated": 1, "inactivated": 0, "skipped": 0}
    assert results.iloc[0]["audit_event_id"].startswith("AUD-")
    assert len(audit_events) == 1
    assert audit_events.iloc[0]["action"] == "reconcile_compliance_dates"


def test_training_actions_inactivate_user_and_emit_user_record_event():
    st.session_state["editable_users"] = _training_users()
    selected_rows = pd.DataFrame(
        [
            {
                "user_id": "USR1",
                "current_record_status": "Active",
                "change_type": "User Remains Out of Compliance",
                "recommended_action": "Inactivate user record",
                "changes_identified": "Expired training remains expired.",
            }
        ]
    )

    counts, results = apply_training_date_actions(selected_rows)
    audit_events = get_audit_events()

    assert counts == {"updated": 0, "inactivated": 1, "skipped": 0}
    assert results.iloc[0]["audit_event_id"].startswith("AUD-")
    assert st.session_state["editable_users"].iloc[0]["record_status"] == "Inactive"
    assert audit_events.iloc[0]["action"] == "inactivate_user"
