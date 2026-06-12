
"""
AccessAtlas

A Streamlit reference implementation for access governance,
compliance tracking, permission cataloging, and access reconciliation
using synthetic CSV-backed data.

This module provides:
- User registry views
- System catalog views
- Compliance monitoring
- System administrator management
- Access reconciliation workflows
"""

import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(page_title="AccessAtlas", layout="wide")

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



def add_expirations(users):
    users = users.copy()
    users["annual_training_expiration"] = users["annual_training_date"] + pd.DateOffset(years=1)
    users["biennial_training_expiration"] = users["biennial_training_date"] + pd.DateOffset(years=2)
    users["compliance_status"] = users.apply(compliance_status, axis=1)
    return users

def reconcile(existing_access, upload_df, selected_system_id=None):
    compare_cols = ["user_id", "system_id", "resource_type", "resource_name", "permission_name"]

    existing = existing_access.copy()
    if selected_system_id and selected_system_id != "All Systems":
        existing = existing[existing["system_id"] == selected_system_id]
        upload_df = upload_df[upload_df["system_id"] == selected_system_id]

    existing_key = existing.set_index(compare_cols)["access_status"].to_dict()
    upload_key = upload_df.set_index(compare_cols)["access_status"].to_dict()

    rows = []
    all_keys = sorted(set(existing_key.keys()) | set(upload_key.keys()))

    for key in all_keys:
        current_status = existing_key.get(key)
        uploaded_status = upload_key.get(key)
        user_id, system_id, resource_type, resource_name, permission_name = key

        if current_status is None:
            change_type = "New Access in Upload"
            recommended_action = "Review and add access record"
        elif uploaded_status is None:
            change_type = "Missing from Upload"
            recommended_action = "Mark inactive after manager confirmation"
        elif current_status != uploaded_status:
            change_type = "Status Changed"
            recommended_action = "Update access status after manager confirmation"
        else:
            change_type = "No Change"
            recommended_action = "No action"

        rows.append({
            "user_id": user_id,
            "system_id": system_id,
            "resource_type": resource_type,
            "resource_name": resource_name,
            "permission_name": permission_name,
            "current_app_status": current_status,
            "uploaded_status": uploaded_status,
            "change_type": change_type,
            "recommended_action": recommended_action
        })

    return pd.DataFrame(rows)

users, systems, access, system_admins = load_data()
users = add_expirations(users)

st.title("AccessAtlas v0.2")
st.caption("Reference implementation for centralized access governance across applications, databases, data platforms, dashboards, and collaboration sites.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Users", "Systems", "System Admins", "Compliance", "Access Reconciliation"
])

with tab1:
    st.subheader("Access Governance Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Users", len(users))
    c2.metric("Tracked Systems", len(systems))
    c3.metric("Access Records", len(access))
    c4.metric("Expired / Expiring", len(users[users["compliance_status"].isin(["Expired", "Expiring Soon"])]))

    joined = access.merge(systems, on="system_id", how="left")
    st.markdown("### Access Records by System Type")
    st.dataframe(joined.groupby("system_type").size().reset_index(name="records"), use_container_width=True)

    st.markdown("### Access Records by Resource Type")
    st.dataframe(joined.groupby("resource_type").size().reset_index(name="records"), use_container_width=True)

    st.markdown("### Use Cases Demonstrated")
    st.write("""
    AccessAtlas shows a generic access governance pattern across several kinds of systems:
    applications, data management systems, cloud data platforms, databases, dashboards,
    and collaboration sites.
    """)

with tab2:
    st.subheader("Central User Registry")
    role_filter = st.multiselect("Filter by application role", sorted(users["application_role"].unique()))
    type_filter = st.multiselect("Filter by user type", sorted(users["user_type"].unique()))
    status_filter = st.multiselect("Filter by record status", sorted(users["record_status"].unique()))
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
        use_container_width=True
    )

with tab3:
    st.subheader("System Catalog")
    st.dataframe(systems, use_container_width=True)

    st.markdown("### Generic Access Model Examples")
    st.info("""
    • Applications can be tracked through periodic user exports.
    • Data management systems can be tracked through role assignments.
    • Cloud data platforms can be tracked through user-to-role metadata.
    • Databases can be tracked through database, schema, and table permissions.
    • Dashboards may require both dashboard access and hosting site access.
    • Collaboration sites can be tracked through site or group membership.
    """)

with tab4:
    st.subheader("System Administrator Assignments")
    admin_view = (
        system_admins
        .merge(users[["user_id", "display_name", "email", "department"]], on="user_id", how="left")
        .merge(systems[["system_id", "system_name", "system_type", "system_category"]], on="system_id", how="left")
    )
    st.dataframe(admin_view, use_container_width=True)

    selected_admin = st.selectbox("Select administrator", sorted(admin_view["display_name"].dropna().unique()))
    st.markdown("### Systems Administered")
    st.dataframe(admin_view[admin_view["display_name"] == selected_admin], use_container_width=True)

with tab5:
    st.subheader("Training & Agreement Compliance")
    compliance_filter = st.multiselect("Filter by compliance status", sorted(users["compliance_status"].unique()))
    comp = users.copy()
    if compliance_filter:
        comp = comp[comp["compliance_status"].isin(compliance_filter)]
    st.dataframe(comp[[
        "user_id", "display_name", "email", "user_type", "record_status",
        "annual_training_date", "annual_training_expiration",
        "biennial_training_date", "biennial_training_expiration",
        "access_agreement_date", "compliance_status"
    ]], use_container_width=True)

    st.markdown("### Reminder Schedule")
    st.write("""
    Reminder logic can be implemented for 30 days before expiration, 7 days before expiration,
    and the date of expiration. In production, notifications would use an approved organizational
    email or orchestration service.
    """)

with tab6:
    st.subheader("Access Reconciliation")
    st.write("Upload an access export or use the included sample file.")
    upload = st.file_uploader(
        "Upload CSV with source_system_record_id, user_id, system_id, resource_type, resource_name, permission_name, access_status",
        type=["csv"]
    )
    if upload:
        uploaded_df = pd.read_csv(upload)
    else:
        uploaded_df = pd.read_csv(DATA_DIR / "sample_access_upload.csv")
        st.caption("Using bundled sample access export.")

    system_options = ["All Systems"] + systems["system_id"].tolist()
    selected_system = st.selectbox("Select reconciliation scope", system_options)

    st.markdown("### Uploaded Access Export")
    st.dataframe(uploaded_df, use_container_width=True)

    result = reconcile(access, uploaded_df, selected_system_id=selected_system)
    st.markdown("### Reconciliation Results")
    st.dataframe(result, use_container_width=True)

    st.markdown("### Reconciliation Summary")
    st.dataframe(result.groupby("change_type").size().reset_index(name="records"), use_container_width=True)

    st.markdown("### Governance Rule Demonstrated")
    st.warning("""
    Users missing from an uploaded access export are recommended for Inactive status rather than deletion,
    preserving access history for audit purposes. Actual access changes remain outside this reference implementation.
    """)
