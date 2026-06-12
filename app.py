"""
AccessAtlas

A Streamlit reference implementation for access governance,
compliance tracking, permission cataloging, and access reconciliation
using synthetic CSV-backed data.

This module provides:
- User registry views
- System catalog views
- System administrator assignment views
- Compliance monitoring
- Access reconciliation workflows
"""

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path(__file__).parent / "data"

ANNUAL_TRAINING_VALID_YEARS = 1
BIENNIAL_TRAINING_VALID_YEARS = 2
EXPIRING_SOON_DAYS = 30

RECONCILIATION_KEY_COLUMNS = [
    "user_id",
    "system_id",
    "resource_type",
    "resource_name",
    "permission_name",
]
RECONCILIATION_REQUIRED_COLUMNS = RECONCILIATION_KEY_COLUMNS + ["access_status"]

st.set_page_config(page_title="AccessAtlas", layout="wide")


@st.cache_data
def load_csv(filename, date_columns=None):
    """Load a CSV file from the data directory with optional date parsing."""
    return pd.read_csv(
        DATA_DIR / filename,
        parse_dates=date_columns or []
    )


@st.cache_data
def load_data():
    """Load all reference datasets used by the application."""
    users = load_csv(
        "users.csv",
        [
            "annual_training_date",
            "biennial_training_date",
            "access_agreement_date",
            "created_date",
            "updated_date",
        ],
    )
    systems = load_csv("systems.csv")
    access_assignments = load_csv(
        "access_assignments.csv",
        ["granted_date", "revoked_date"],
    )
    system_admin_assignments = load_csv(
        "system_admin_assignments.csv",
        ["granted_date", "revoked_date"],
    )

    return {
        "users": users,
        "systems": systems,
        "access_assignments": access_assignments,
        "system_admin_assignments": system_admin_assignments,
    }


def compliance_status(row):
    """Return compliance status based on training expiration rules."""
    today_ts = pd.Timestamp(date.today())

    annual_exp = row["annual_training_date"] + pd.DateOffset(
        years=ANNUAL_TRAINING_VALID_YEARS
    )
    biennial_exp = row["biennial_training_date"] + pd.DateOffset(
        years=BIENNIAL_TRAINING_VALID_YEARS
    )

    if annual_exp < today_ts or biennial_exp < today_ts:
        return "Expired"

    if (
        annual_exp <= today_ts + pd.Timedelta(days=EXPIRING_SOON_DAYS)
        or biennial_exp <= today_ts + pd.Timedelta(days=EXPIRING_SOON_DAYS)
    ):
        return "Expiring Soon"

    return "Current"


def add_expirations(users):
    """Add expiration dates and compliance status fields to the user dataset."""
    users = users.copy()

    users["annual_training_expiration"] = users["annual_training_date"] + pd.DateOffset(
        years=ANNUAL_TRAINING_VALID_YEARS
    )
    users["biennial_training_expiration"] = users[
        "biennial_training_date"
    ] + pd.DateOffset(years=BIENNIAL_TRAINING_VALID_YEARS)

    users["compliance_status"] = users.apply(compliance_status, axis=1)
    return users


def validate_upload(upload_df, required_columns):
    """Return a list of required columns missing from an uploaded file."""
    return [column for column in required_columns if column not in upload_df.columns]


def reconcile(current_access, upload_df, selected_system_id=None):
    """Compare current access assignments to an uploaded access export."""
    current = current_access.copy()
    upload = upload_df.copy()

    if selected_system_id and selected_system_id != "All Systems":
        current = current[current["system_id"] == selected_system_id]
        upload = upload[upload["system_id"] == selected_system_id]

    current_key = current.set_index(RECONCILIATION_KEY_COLUMNS)["access_status"].to_dict()
    upload_key = upload.set_index(RECONCILIATION_KEY_COLUMNS)["access_status"].to_dict()

    source_record_lookup = {}
    if "source_system_record_id" in upload.columns:
        source_record_lookup = (
            upload.set_index(RECONCILIATION_KEY_COLUMNS)["source_system_record_id"]
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

    return pd.DataFrame(rows)

data = load_data()
users = add_expirations(data["users"])
systems = data["systems"]
access = data["access_assignments"]
system_admins = data["system_admin_assignments"]

st.title("AccessAtlas")
st.caption(
    "Reference implementation for centralized access governance across "
    "applications, databases, data platforms, dashboards, and collaboration sites."
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Overview",
        "Users",
        "Systems",
        "System Admins",
        "Compliance",
        "Access Reconciliation",
    ]
)

with tab1:
    st.subheader("Access Governance Overview")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Users", len(users))
    c2.metric("Tracked Systems", len(systems))
    c3.metric("Access Records", len(access))
    c4.metric("System Admin Assignments", len(system_admins))
    c5.metric(
        "Expired / Expiring",
        len(users[users["compliance_status"].isin(["Expired", "Expiring Soon"])]),
    )

    joined = access.merge(systems, on="system_id", how="left")

    st.markdown("### User Record Status")
    st.dataframe(
        users.groupby("record_status").size().reset_index(name="users"),
        use_container_width=True,
    )

    st.markdown("### Compliance Status")
    st.dataframe(
        users.groupby("compliance_status").size().reset_index(name="users"),
        use_container_width=True,
    )

    st.markdown("### Access Records by System Type")
    st.dataframe(
        joined.groupby("system_type").size().reset_index(name="records"),
        use_container_width=True,
    )

    st.markdown("### Access Records by Resource Type")
    st.dataframe(
        joined.groupby("resource_type").size().reset_index(name="records"),
        use_container_width=True,
    )

    st.markdown("### Access Records by Access Status")
    st.dataframe(
        access.groupby("access_status").size().reset_index(name="records"),
        use_container_width=True,
    )

    st.markdown("### What This Reference Implementation Demonstrates")
    st.write(
        """
        AccessAtlas demonstrates a generic access governance pattern for:

        - Central user registry management
        - Cross-system access cataloging
        - Resource-level permission tracking
        - System administrator assignment tracking
        - Training and agreement compliance monitoring
        - Upload-based access reconciliation
        - Audit-friendly inactive record handling
        """
    )

with tab2:
    st.subheader("Central User Registry")
    role_filter = st.multiselect(
        "Filter by application role",
        sorted(users["application_role"].unique()),
    )
    type_filter = st.multiselect(
        "Filter by user type",
        sorted(users["user_type"].unique()),
    )
    status_filter = st.multiselect(
        "Filter by record status",
        sorted(users["record_status"].unique()),
    )

    view = users.copy()
    if role_filter:
        view = view[view["application_role"].isin(role_filter)]
    if type_filter:
        view = view[view["user_type"].isin(type_filter)]
    if status_filter:
        view = view[view["record_status"].isin(status_filter)]

    st.dataframe(view, use_container_width=True)

    st.markdown("### User Access Detail")
    selected = st.selectbox("Select user ID", users["user_id"])
    st.dataframe(
        access[access["user_id"] == selected].merge(systems, on="system_id", how="left"),
        use_container_width=True,
    )

with tab3:
    st.subheader("System Catalog")
    st.dataframe(systems, use_container_width=True)

    st.markdown("### Generic Access Model Examples")
    st.info(
        """
        • Applications can be tracked through periodic user exports.
        • Data management systems can be tracked through role assignments.
        • Cloud data platforms can be tracked through user-to-role metadata.
        • Databases can be tracked through database, schema, and table permissions.
        • Dashboards may require both dashboard access and hosting site access.
        • Collaboration sites can be tracked through site or group membership.
        """
    )

with tab4:
    st.subheader("System Administrator Assignments")
    admin_view = (
        system_admins.merge(
            users[["user_id", "display_name", "email", "department"]],
            on="user_id",
            how="left",
        )
        .merge(
            systems[["system_id", "system_name", "system_type", "system_category"]],
            on="system_id",
            how="left",
        )
    )

    st.dataframe(admin_view, use_container_width=True)

    selected_admin = st.selectbox(
        "Select administrator",
        sorted(admin_view["display_name"].dropna().unique()),
    )
    st.markdown("### Systems Administered")
    st.dataframe(
        admin_view[admin_view["display_name"] == selected_admin],
        use_container_width=True,
    )

with tab5:
    st.subheader("Training & Agreement Compliance")
    compliance_filter = st.multiselect(
        "Filter by compliance status",
        sorted(users["compliance_status"].unique()),
    )

    comp = users.copy()
    if compliance_filter:
        comp = comp[comp["compliance_status"].isin(compliance_filter)]

    st.dataframe(
        comp[
            [
                "user_id",
                "display_name",
                "email",
                "user_type",
                "record_status",
                "annual_training_date",
                "annual_training_expiration",
                "biennial_training_date",
                "biennial_training_expiration",
                "access_agreement_date",
                "compliance_status",
            ]
        ],
        use_container_width=True,
    )

    st.markdown("### Reminder Schedule")
    st.write(
        f"""
        Reminder logic can be implemented for {EXPIRING_SOON_DAYS} days before
        expiration, 7 days before expiration, and the date of expiration.
        In production, notifications would use an approved organizational
        email or orchestration service.
        """
    )

with tab6:
    st.subheader("Access Reconciliation")
    st.write("Upload an access export or use the included sample file.")
    upload = st.file_uploader(
        "Upload CSV with source_system_record_id, user_id, system_id, "
        "resource_type, resource_name, permission_name, access_status",
        type=["csv"],
    )

    if upload:
        uploaded_df = pd.read_csv(upload)
    else:
        uploaded_df = pd.read_csv(DATA_DIR / "sample_access_upload.csv")
        st.caption("Using bundled sample access export.")

    missing_columns = validate_upload(uploaded_df, RECONCILIATION_REQUIRED_COLUMNS)
    if missing_columns:
        st.error(
            "Uploaded file is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    system_options = ["All Systems"] + systems["system_id"].tolist()
    selected_system = st.selectbox("Select reconciliation scope", system_options)

    st.markdown("### Uploaded Access Export")
    st.dataframe(uploaded_df, use_container_width=True)

    result = reconcile(access, uploaded_df, selected_system_id=selected_system)

    st.markdown("### Reconciliation Results")
    st.dataframe(result, use_container_width=True)

    st.markdown("### Reconciliation Summary")
    st.dataframe(
        result.groupby("change_type").size().reset_index(name="records"),
        use_container_width=True,
    )

    st.markdown("### Governance Rule Demonstrated")
    st.warning(
        """
        Users missing from an uploaded access export are recommended for
        Inactive status rather than deletion, preserving access history for
        audit purposes. Actual access changes remain outside this reference
        implementation.
        """
    )
