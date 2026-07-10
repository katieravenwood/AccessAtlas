"""AccessAtlas application module."""

from datetime import date
import logging

import pandas as pd
import streamlit as st

from accessatlas.audit import record_audit_event

from accessatlas.compliance import normalize_date_value, uploaded_dates_compliance_status
from accessatlas.config import RECONCILIATION_KEY_COLUMNS, TRAINING_RECONCILIATION_DATE_COLUMNS
from accessatlas.logging_config import get_logger, log_event
from accessatlas.state import (
    access_key_mask,
    generate_next_access_id,
    initialize_user_update_state,
    update_user_compliance_dates,
)


logger = get_logger(__name__)

def validate_upload(upload_df, required_columns):
    """Return a list of required columns missing from an uploaded file."""
    missing_columns = [
        column
        for column in required_columns
        if column not in upload_df.columns
    ]
    log_event(
        logger,
        logging.WARNING if missing_columns else logging.INFO,
        "upload_validated",
        "Uploaded reconciliation file schema validated.",
        record_count=len(upload_df),
        required_column_count=len(required_columns),
        missing_columns=missing_columns,
        is_valid=not missing_columns,
    )
    return missing_columns

def reconcile(current_access, upload_df, selected_system_id=None):
    """Compare current access assignments to an uploaded access export."""
    current = current_access.copy()
    upload = upload_df.copy()

    if selected_system_id and selected_system_id != "All Systems":
        current = current[current["system_id"] == selected_system_id]
        upload = upload[upload["system_id"] == selected_system_id]

    # Determine which key columns are available in both dataframes.
    # Some exports include `first_name`/`last_name`, but the canonical
    # access assignments data may not. Use the intersection to avoid
    # KeyError from set_index when columns are missing.
    key_cols = [c for c in RECONCILIATION_KEY_COLUMNS if c in current.columns and c in upload.columns]

    # If no intersection, fall back to the canonical identifier set
    # that the reference data uses (user_id + system + resource + permission).
    if not key_cols:
        fallback = ["user_id", "system_id", "resource_type", "resource_name", "permission_name"]
        key_cols = [c for c in fallback if c in current.columns and c in upload.columns]

    if not key_cols:
        log_event(
            logger,
            logging.ERROR,
            "reconciliation_key_resolution_failed",
            "Reconciliation could not resolve matching key columns.",
            current_columns=list(current.columns),
            upload_columns=list(upload.columns),
        )
        raise KeyError(
            "Reconciliation cannot proceed: no matching key columns found in current and uploaded data. "
            f"Expected one of {RECONCILIATION_KEY_COLUMNS} or fallback {fallback}.")

    current_key = current.set_index(key_cols)["access_status"].to_dict()
    upload_key = upload.set_index(key_cols)["access_status"].to_dict()

    source_record_lookup = {}
    if "source_system_record_id" in upload.columns:
        source_record_lookup = (
            upload.set_index(key_cols)["source_system_record_id"]
            .to_dict()
        )

    rows = []
    all_keys = sorted(set(current_key.keys()) | set(upload_key.keys()))

    for key in all_keys:
        current_status = current_key.get(key)
        uploaded_status = upload_key.get(key)
        user_id, system_id, resource_type, resource_name, permission_name = key

        if current_status is None:
            change_type = "New Access in Upload"
            recommended_action = "Review and add access record"
        elif uploaded_status is None:
            change_type = "Access Not Found in Upload"
            recommended_action = "Review for inactive status"
        elif current_status != uploaded_status:
            change_type = "Status Changed"
            recommended_action = "Review and update access status"
        else:
            change_type = "No Change"
            recommended_action = "No action"

        rows.append(
            {
                "source_system_record_id": source_record_lookup.get(key),
                "user_id": user_id,
                "system_id": system_id,
                "resource_type": resource_type,
                "resource_name": resource_name,
                "permission_name": permission_name,
                "current_access_status": current_status,
                "uploaded_access_status": uploaded_status,
                "change_type": change_type,
                "recommended_action": recommended_action,
            }
        )

    comparison = pd.DataFrame(rows)
    change_counts = (
        comparison["change_type"].value_counts(dropna=False).to_dict()
        if not comparison.empty
        else {}
    )
    log_event(
        logger,
        logging.INFO,
        "access_reconciliation_completed",
        "System access reconciliation comparison completed.",
        selected_system_id=selected_system_id or "All Systems",
        current_record_count=len(current),
        uploaded_record_count=len(upload),
        comparison_record_count=len(comparison),
        change_counts=change_counts,
    )
    return comparison

def apply_reconciliation_action(access_df, row):
    """Apply one reconciliation recommendation to the canonical access table."""
    access_df = access_df.copy()
    change_type = row["change_type"]
    today = pd.Timestamp(date.today())

    if change_type == "New Access in Upload":
        new_record = {
            "access_id": generate_next_access_id(access_df),
            "user_id": row["user_id"],
            "system_id": row["system_id"],
            "resource_type": row["resource_type"],
            "resource_name": row["resource_name"],
            "permission_name": row["permission_name"],
            "access_status": row["uploaded_access_status"] or "Active",
            "granted_date": today,
            "revoked_date": pd.NaT,
            "source": "Reconciliation Action",
        }
        return pd.concat([access_df, pd.DataFrame([new_record])], ignore_index=True), "added"

    mask = access_key_mask(access_df, row)

    if not mask.any():
        return access_df, "skipped"

    if change_type == "Access Not Found in Upload":
        access_df.loc[mask, "access_status"] = "Inactive"
        access_df.loc[mask, "revoked_date"] = today
        return access_df, "inactivated"

    if change_type == "Status Changed":
        access_df.loc[mask, "access_status"] = row["uploaded_access_status"]
        if row["uploaded_access_status"] == "Inactive":
            access_df.loc[mask, "revoked_date"] = today
        elif row["uploaded_access_status"] == "Active":
            access_df.loc[mask, "revoked_date"] = pd.NaT
        return access_df, "updated"

    return access_df, "skipped"


def build_reconciliation_change_summary(row, outcome):
    """Return a human-readable summary of what changed for a reconciliation row."""
    if outcome == "added":
        return (
            "Added new access assignment "
            f"({row.get('resource_type')} / {row.get('resource_name')} / "
            f"{row.get('permission_name')}) with status "
            f"{row.get('uploaded_access_status')}."
        )

    if outcome == "inactivated":
        return (
            "Access Status: "
            f"{row.get('current_access_status')} → Inactive."
        )

    if outcome == "updated":
        return (
            "Access Status: "
            f"{row.get('current_access_status')} → {row.get('uploaded_access_status')}."
        )

    if outcome == "skipped":
        return "No record was changed. The action was skipped."

    return "No change summary available."

def build_reconciliation_action_result(row, outcome):
    """Return a display-friendly action result and record a successful governance event."""
    result_labels = {
        "added": "Success",
        "inactivated": "Success",
        "updated": "Success",
        "skipped": "Skipped",
    }
    change_summary = build_reconciliation_change_summary(row, outcome)
    audit_event_id = ""

    if outcome != "skipped":
        event = record_audit_event(
            event_type="access_reconciliation",
            action=f"reconciliation_{outcome}",
            entity_type="access_assignment",
            target_user_id=row.get("user_id", ""),
            system_id=row.get("system_id", ""),
            source="System Access Reconciliation",
            summary=change_summary,
            changes={
                "recommended_action": row.get("recommended_action"),
                "change_type": row.get("change_type"),
                "resource_type": row.get("resource_type"),
                "resource_name": row.get("resource_name"),
                "permission_name": row.get("permission_name"),
                "before_status": row.get("current_access_status"),
                "after_status": row.get("uploaded_access_status"),
                "source_system_record_id": row.get("source_system_record_id"),
            },
        )
        audit_event_id = event.audit_event_id

    return {
        "audit_event_id": audit_event_id,
        "action_result": result_labels.get(outcome, "Unknown"),
        "changes_made": change_summary,
        "recommended_action": row.get("recommended_action"),
        "change_type": row.get("change_type"),
        "user_id": row.get("user_id"),
        "first_name": row.get("first_name"),
        "last_name": row.get("last_name"),
        "system_id": row.get("system_id"),
        "system_name": row.get("system_name"),
        "resource_type": row.get("resource_type"),
        "resource_name": row.get("resource_name"),
        "permission_name": row.get("permission_name"),
        "current_access_status": row.get("current_access_status"),
        "uploaded_access_status": row.get("uploaded_access_status"),
        "source_system_record_id": row.get("source_system_record_id"),
    }

def apply_reconciliation_actions(access_df, selected_rows):
    """Apply selected reconciliation actions and return updated access data, counts, and result rows."""
    updated_access = access_df.copy()
    counts = {
        "added": 0,
        "inactivated": 0,
        "updated": 0,
        "skipped": 0,
    }
    action_results = []

    action_value_map = {
        "Add access record": "Review and add access record",
        "Inactivate": "Review for inactive status",
        "Update access status": "Review and update access status",
    }

    for _, row in selected_rows.iterrows():
        row = row.copy()
        if row.get("recommended_action") in action_value_map:
            row["recommended_action"] = action_value_map[row["recommended_action"]]

        updated_access, outcome = apply_reconciliation_action(updated_access, row)
        counts[outcome] += 1

        display_row = row.copy()
        display_row["recommended_action"] = display_recommended_action(
            row.get("recommended_action")
        )
        action_results.append(build_reconciliation_action_result(display_row, outcome))

    result_dataframe = pd.DataFrame(action_results)
    log_event(
        logger,
        logging.INFO,
        "access_reconciliation_actions_applied",
        "Selected system access reconciliation actions were processed.",
        selected_action_count=len(selected_rows),
        outcome_counts=counts,
        resulting_access_record_count=len(updated_access),
    )
    return updated_access, counts, result_dataframe

def inactivate_user_record(user_id):
    """Mark one user record inactive in the session-state user registry."""
    current_users = st.session_state["editable_users"].copy()
    user_mask = current_users["user_id"] == user_id

    if not user_mask.any():
        return "skipped"

    current_users.loc[user_mask, "record_status"] = "Inactive"
    current_users.loc[user_mask, "updated_date"] = pd.Timestamp(date.today())
    st.session_state["editable_users"] = current_users
    return "inactivated"

def reconcile_training_dates(current_users, upload_df):
    """Compare current user compliance dates to an uploaded date export."""
    current = current_users.copy()
    upload = upload_df.copy()

    for column in TRAINING_RECONCILIATION_DATE_COLUMNS:
        current[column] = current[column].apply(normalize_date_value)
        upload[column] = upload[column].apply(normalize_date_value)

    current_lookup = current.set_index("user_id")[TRAINING_RECONCILIATION_DATE_COLUMNS].to_dict("index")
    upload_lookup = upload.set_index("user_id")[TRAINING_RECONCILIATION_DATE_COLUMNS].to_dict("index")
    current_status_lookup = current.set_index("user_id")["record_status"].to_dict()

    rows = []
    all_user_ids = sorted(set(current_lookup.keys()) | set(upload_lookup.keys()))

    for user_id in all_user_ids:
        current_values = current_lookup.get(user_id)
        uploaded_values = upload_lookup.get(user_id)

        if current_values is None:
            change_type = "User Not Found in AccessAtlas"
            recommended_action = "Review user record"
            changes = "Uploaded user is not present in the current user registry."
        elif uploaded_values is None:
            change_type = "User Not Found in Upload"
            recommended_action = "No action"
            changes = "No uploaded date record was provided for this user."
        else:
            uploaded_compliance = uploaded_dates_compliance_status(uploaded_values)
            changed_fields = []

            for column in TRAINING_RECONCILIATION_DATE_COLUMNS:
                current_value = current_values.get(column, "")
                uploaded_value = uploaded_values.get(column, "")
                if current_value != uploaded_value:
                    changed_fields.append(
                        f"{column}: {current_value or 'Blank'} → {uploaded_value or 'Blank'}"
                    )

            if uploaded_compliance == "Expired":
                change_type = "User Remains Out of Compliance"
                recommended_action = "Inactivate user record"
                changes = (
                    "Uploaded dates confirm the user remains out of compliance. "
                    + ("; ".join(changed_fields) if changed_fields else "No date changes provided.")
                )
            elif changed_fields:
                change_type = "Date Changed"
                recommended_action = "Update date records"
                changes = "; ".join(changed_fields)
            else:
                change_type = "No Change"
                recommended_action = "No action"
                changes = "No date changes detected."

        row = {
            "user_id": user_id,
            "current_record_status": current_status_lookup.get(user_id, ""),
            "change_type": change_type,
            "recommended_action": recommended_action,
            "changes_identified": changes,
        }

        for column in TRAINING_RECONCILIATION_DATE_COLUMNS:
            row[f"current_{column}"] = (
                current_values.get(column, "") if current_values else ""
            )
            row[f"uploaded_{column}"] = (
                uploaded_values.get(column, "") if uploaded_values else ""
            )

        rows.append(row)

    comparison = pd.DataFrame(rows)
    change_counts = (
        comparison["change_type"].value_counts(dropna=False).to_dict()
        if not comparison.empty
        else {}
    )
    log_event(
        logger,
        logging.INFO,
        "training_reconciliation_completed",
        "Training and agreement reconciliation comparison completed.",
        current_user_count=len(current),
        uploaded_user_count=len(upload),
        comparison_record_count=len(comparison),
        change_counts=change_counts,
    )
    return comparison

def apply_training_date_actions(selected_rows):
    """Apply selected training date reconciliation actions to session state."""
    initialize_user_update_state()

    results = []
    counts = {"updated": 0, "inactivated": 0, "skipped": 0}

    for _, row in selected_rows.iterrows():
        if row["recommended_action"] == "Update date records":
            audit_event = update_user_compliance_dates(
                row["user_id"],
                row["uploaded_annual_training_date"],
                row["uploaded_biennial_training_date"],
                row["uploaded_access_agreement_date"],
                audit_action="reconcile_compliance_dates",
                audit_source="Training and Agreement Reconciliation",
            )
            counts["updated"] += 1
            results.append(
                {
                    "audit_event_id": audit_event.audit_event_id,
                    "action_result": "Success",
                    "changes_made": row.get("changes_identified", "Date records updated."),
                    "recommended_action": row["recommended_action"],
                    "change_type": row["change_type"],
                    "user_id": row["user_id"],
                    "first_name": row.get("first_name", ""),
                    "last_name": row.get("last_name", ""),
                    "changes_identified": row.get("changes_identified", ""),
                }
            )
            continue

        if row["recommended_action"] == "Inactivate user record":
            outcome = inactivate_user_record(row["user_id"])
            counts["inactivated" if outcome == "inactivated" else "skipped"] += 1
            audit_event_id = ""
            if outcome == "inactivated":
                audit_event_id = record_audit_event(
                    event_type="user_record",
                    action="inactivate_user",
                    entity_type="user",
                    entity_id=row["user_id"],
                    target_user_id=row["user_id"],
                    source="Training and Agreement Reconciliation",
                    summary="User record status set to Inactive.",
                    changes={"record_status": {"before": row.get("current_record_status"), "after": "Inactive"}},
                ).audit_event_id
            results.append(
                {
                    "audit_event_id": audit_event_id,
                    "action_result": "Success" if outcome == "inactivated" else "Skipped",
                    "changes_made": "User record status set to Inactive." if outcome == "inactivated" else "User record was not changed.",
                    "recommended_action": row["recommended_action"],
                    "change_type": row["change_type"],
                    "user_id": row["user_id"],
                    "first_name": row.get("first_name", ""),
                    "last_name": row.get("last_name", ""),
                    "changes_identified": row.get("changes_identified", ""),
                }
            )
            continue

        counts["skipped"] += 1
        results.append(
            {
                "audit_event_id": "",
                "action_result": "Skipped",
                "changes_made": "No date or user status update was applied.",
                "recommended_action": row["recommended_action"],
                "change_type": row["change_type"],
                "user_id": row["user_id"],
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "changes_identified": row.get("changes_identified", ""),
            }
        )

    result_dataframe = pd.DataFrame(results)
    log_event(
        logger,
        logging.INFO,
        "training_reconciliation_actions_applied",
        "Selected training and agreement reconciliation actions were processed.",
        selected_action_count=len(selected_rows),
        outcome_counts=counts,
    )
    return counts, result_dataframe


def display_recommended_action(action):
    """Return a concise display label for a reconciliation recommended action."""
    action_labels = {
        "Review and add access record": "Add access record",
        "Review for inactive status": "Inactivate",
        "Review and update access status": "Update access status",
        "No action": "No action",
    }
    return action_labels.get(action, action)
