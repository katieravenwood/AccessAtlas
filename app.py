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

USER_DISPLAY_COLUMNS = [
    "user_id",
    "display_name",
    "email",
    "application_role",
    "manager_user_id",
    "department",
    "user_type",
    "record_status",
    "compliance_status",
]

COMPLIANCE_COLUMNS = [
    "user_id",
    "display_name",
    "email",
    "department",
    "user_type",
    "record_status",
    "annual_training_date",
    "annual_training_expiration",
    "biennial_training_date",
    "biennial_training_expiration",
    "access_agreement_date",
    "compliance_status",
]

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

    warning_date = today_ts + pd.Timedelta(days=EXPIRING_SOON_DAYS)
    if annual_exp <= warning_date or biennial_exp <= warning_date:
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
    **User ID:** {selected_user['user_id']}  
    **Email:** {selected_user['email']}  
    **Department:** {selected_user['department']}  
    **User Type:** {selected_user['user_type']}  
    **Application Role:** {selected_user['application_role']}  
    **Manager:** {manager_name}  
    **Record Status:** {selected_user['record_status']}  
    **Compliance Status:** {selected_user['compliance_status']}
    """


def system_profile_markdown(selected_system):
    """Build the selected system profile markdown block."""
    return f"""
    **System ID:** {selected_system['system_id']}  
    **System Type:** {selected_system['system_type']}  
    **System Category:** {selected_system['system_category']}  
    **Resource Scope:** {selected_system['resource_scope']}  
    **Access Model:** {selected_system['access_model']}  
    **Tracking Method:** {selected_system['tracking_method']}  
    **System Owner:** {selected_system['system_owner']}  
    **Admin Group:** {selected_system['admin_group']}  
    **Record Status:** {selected_system['record_status']}  
    **Notes:** {selected_system['notes']}
    """


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
        raise KeyError(
            "Reconciliation cannot proceed: no matching key columns found in current and uploaded data. "
            f"Expected one of {RECONCILIATION_KEY_COLUMNS} or fallback {fallback}.")

    current_key = current.set_index(key_cols)["access_status"].to_dict()
    upload_key = upload.set_index(key_cols)["access_status"].to_dict()

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


# Load and prepare data.
data = load_data()
users = add_expirations(data["users"])
systems = data["systems"]
access = data["access_assignments"]
system_admins = data["system_admin_assignments"]
access_with_systems = access.merge(systems, on="system_id", how="left")

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
        count_by(users, "record_status", "users"), 
        width="stretch",
    )

    st.markdown("### Compliance Status")
    st.dataframe(
        count_by(users, "compliance_status", "users"), 
        width="stretch",
    )

    st.markdown("### Access Records by System Type")
    st.dataframe(
        count_by(access_with_systems, "system_type"), 
        width="stretch",
    )

    st.markdown("### Access Records by Resource Type")
    st.dataframe(
        count_by(access_with_systems, "resource_type"), 
        width="stretch",
    )

    st.markdown("### Access Records by Access Status")
    st.dataframe(count_by(access, "access_status"), 
        width="stretch",
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
        sorted(users["application_role"].dropna().unique()),
        key="role_filter",
    )
    type_filter = st.multiselect(
        "Filter by user type",
        sorted(users["user_type"].unique()),
        key="type_filter",
    )
    status_filter = st.multiselect(
        "Filter by record status",
        sorted(users["record_status"].dropna().unique()),
        key="status_filter",
    )

    user_view = users.copy()
    user_view = apply_multiselect_filter(user_view, "application_role", role_filter)
    user_view = apply_multiselect_filter(user_view, "user_type", type_filter)
    user_view = apply_multiselect_filter(user_view, "record_status", status_filter)

    st.dataframe(user_view[USER_DISPLAY_COLUMNS], 
                 width="stretch"
                 )

    st.markdown("### Selected User Governance Profile")
    selected_user_id = st.selectbox(
        "Select user ID", 
        users["user_id"],
        key="selected_user_id",
    )
    selected_user = users[users["user_id"] == selected_user_id].iloc[0]
    manager_name = get_display_name(users, selected_user["manager_user_id"])

    selected_access = access[access["user_id"] == selected_user_id].merge(
        systems,
        on="system_id",
        how="left",
    )
    selected_admin_assignments = (
        system_admins[system_admins["user_id"] == selected_user_id]
        .merge(
            systems[["system_id", "system_name", "system_type", "system_category"]],
            on="system_id",
            how="left",
        )
    )

    st.markdown(f"#### {selected_user['display_name']}")
    st.write(user_profile_markdown(selected_user, manager_name))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Systems Accessed", selected_access["system_id"].nunique())
    m2.metric("Access Assignments", len(selected_access))
    m3.metric("Admin Assignments", len(selected_admin_assignments))
    m4.metric("Compliance", selected_user["compliance_status"])

    st.markdown("### Training & Agreement Snapshot")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "requirement": "Annual Training",
                    "completion_date": selected_user["annual_training_date"],
                    "expiration_date": selected_user["annual_training_expiration"],
                },
                {
                    "requirement": "Biennial Training",
                    "completion_date": selected_user["biennial_training_date"],
                    "expiration_date": selected_user["biennial_training_expiration"],
                },
                {
                    "requirement": "Access Agreement",
                    "completion_date": selected_user["access_agreement_date"],
                    "expiration_date": "",
                },
            ]
        ),
        width="stretch",
    )

    st.markdown("### Access by System")
    if selected_access.empty:
        st.info("This user does not currently have access assignments.")
    else:
        st.dataframe(
            count_by(
                selected_access,
                ["system_id", "system_name", "system_type"],
                "access_records",
            ),
            width="stretch",
        )

    st.markdown("### Detailed Access Assignments")
    st.dataframe(selected_access, 
                 width="stretch")

    st.markdown("### Administrative Assignments")
    if selected_admin_assignments.empty:
        st.info("This user is not assigned as an administrator for any tracked systems.")
    else:
        st.dataframe(selected_admin_assignments, 
                     width="stretch")

with tab3:
    st.subheader("System Catalog")

    system_type_filter = st.multiselect(
        "Filter by system type",
        sorted(systems["system_type"].dropna().unique()),
        key="system_type_filter",
    )
    system_category_filter = st.multiselect(
        "Filter by system category",
        sorted(systems["system_category"].dropna().unique()),
        key="system_category_filter",
    )
    system_status_filter = st.multiselect(
        "Filter by system record status",
        sorted(systems["record_status"].dropna().unique()),
        key="system_status_filter",
    )

    system_view = systems.copy()
    system_view = apply_multiselect_filter(system_view, "system_type", system_type_filter)
    system_view = apply_multiselect_filter(
        system_view,
        "system_category",
        system_category_filter,
    )
    system_view = apply_multiselect_filter(system_view, "record_status", system_status_filter)

    st.dataframe(system_view, 
                 width="stretch")

    st.markdown("### Selected System Governance Profile")
    selected_system_id = st.selectbox(
        "Select system ID", 
        systems["system_id"],
        key="selected_system_id",
    )
    selected_system = systems[systems["system_id"] == selected_system_id].iloc[0]

    selected_system_access = access[access["system_id"] == selected_system_id].merge(
        users[["user_id", "display_name", "email", "department", "user_type"]],
        on="user_id",
        how="left",
    )
    selected_system_admins = (
        system_admins[system_admins["system_id"] == selected_system_id]
        .merge(
            users[["user_id", "display_name", "email", "department"]],
            on="user_id",
            how="left",
        )
    )

    st.markdown(f"#### {selected_system['system_name']}")
    st.write(system_profile_markdown(selected_system))

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Unique Users", selected_system_access["user_id"].nunique())
    s2.metric("Access Assignments", len(selected_system_access))
    s3.metric("System Administrators", len(selected_system_admins))
    s4.metric("Resource Types", selected_system_access["resource_type"].nunique())

    st.markdown("### Users with Access")
    if selected_system_access.empty:
        st.info("No access assignments are currently recorded for this system.")
    else:
        st.dataframe(
            selected_system_access[
                [
                    "user_id",
                    "display_name",
                    "email",
                    "department",
                    "user_type",
                    "resource_type",
                    "resource_name",
                    "permission_name",
                    "access_status",
                    "granted_date",
                    "revoked_date",
                    "source",
                ]
            ],
            width="stretch",
        )

    st.markdown("### System Administrators")
    if selected_system_admins.empty:
        st.info("No system administrator assignments are currently recorded for this system.")
    else:
        st.dataframe(selected_system_admins, 
                     width="stretch")

    st.markdown("### Resources and Permissions")
    if selected_system_access.empty:
        st.info("No resources or permissions are currently recorded for this system.")
    else:
        st.dataframe(
            count_by(
                selected_system_access,
                ["resource_type", "resource_name", "permission_name", "access_status"],
                "assigned_users",
            ),
            width="stretch",
        )

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
            systems[
                [
                    "system_id",
                    "system_name",
                    "system_type",
                    "system_category",
                    "record_status",
                ]
            ],
            on="system_id",
            how="left",
        )
    )

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Admin Assignments", len(admin_view))
    a2.metric("Unique Administrators", admin_view["user_id"].nunique())
    a3.metric("Systems with Admins", admin_view["system_id"].nunique())
    a4.metric(
        "Active Assignments",
        len(admin_view[admin_view["assignment_status"] == "Active"]),
    )

    st.markdown("### Filters")
    admin_role_filter = st.multiselect(
        "Filter by admin role",
        sorted(admin_view["admin_role"].dropna().unique()),
        key="admin_role_filter",
    )
    assignment_status_filter = st.multiselect(
        "Filter by assignment status",
        sorted(admin_view["assignment_status"].dropna().unique()),
        key="assignment_status_filter",
    )
    admin_system_type_filter = st.multiselect(
        "Filter by system type",
        sorted(admin_view["system_type"].dropna().unique()),
        key="admin_system_type_filter",
    )
    admin_system_category_filter = st.multiselect(
        "Filter by system category",
        sorted(admin_view["system_category"].dropna().unique()),
        key="admin_system_category_filter",
    )

    filtered_admin_view = admin_view.copy()
    filtered_admin_view = apply_multiselect_filter(
        filtered_admin_view,
        "admin_role",
        admin_role_filter,
    )
    filtered_admin_view = apply_multiselect_filter(
        filtered_admin_view,
        "assignment_status",
        assignment_status_filter,
    )
    filtered_admin_view = apply_multiselect_filter(
        filtered_admin_view,
        "system_type",
        admin_system_type_filter,
    )
    filtered_admin_view = apply_multiselect_filter(
        filtered_admin_view,
        "system_category",
        admin_system_category_filter,
    )

    st.markdown("### All System Administrator Assignments")
    st.dataframe(filtered_admin_view, 
                 width="stretch")

    st.markdown("### Administrator-Centered View")
    selected_admin = st.selectbox(
        "Select administrator",
        sorted(admin_view["display_name"].dropna().unique()),
        key="selected_administrator",
    )
    st.dataframe(
        admin_view[admin_view["display_name"] == selected_admin],
        width="stretch",
    )

    st.markdown("### System-Centered View")
    selected_admin_system = st.selectbox(
        "Select system",
        sorted(systems["system_name"].dropna().unique()),
        key="selected_admin_system",
    )
    selected_admin_system_id = systems[
        systems["system_name"] == selected_admin_system
    ].iloc[0]["system_id"]
    system_admin_detail = admin_view[
        admin_view["system_id"] == selected_admin_system_id
    ]

    if system_admin_detail.empty:
        st.info("No administrator assignments are currently recorded for this system.")
    else:
        st.dataframe(system_admin_detail, 
                     width="stretch")

    st.markdown("### Admin Coverage by System")
    coverage = systems[
        ["system_id", "system_name", "system_type", "system_category", "record_status"]
    ].merge(
        count_by(admin_view, "system_id", "admin_assignment_count"),
        on="system_id",
        how="left",
    )
    coverage["admin_assignment_count"] = (
        coverage["admin_assignment_count"].fillna(0).astype(int)
    )
    coverage["coverage_status"] = coverage["admin_assignment_count"].apply(
        lambda count: "Has Administrator" if count > 0 else "No Administrator Recorded"
    )
    st.dataframe(coverage, 
                 width="stretch")

with tab5:
    st.subheader("Compliance Monitoring")

    current_count = len(users[users["compliance_status"] == "Current"])
    expiring_count = len(users[users["compliance_status"] == "Expiring Soon"])
    expired_count = len(users[users["compliance_status"] == "Expired"])
    follow_up_count = len(
        users[
            (users["compliance_status"] != "Current")
            & (users["record_status"] == "Active")
        ]
    )

    cm1, cm2, cm3, cm4 = st.columns(4)
    cm1.metric("Current", current_count)
    cm2.metric("Expiring Soon", expiring_count)
    cm3.metric("Expired", expired_count)
    cm4.metric("Active Records Requiring Follow-Up", follow_up_count)

    st.markdown("### Filters")
    compliance_filter = st.multiselect(
        "Filter by compliance status",
        sorted(users["compliance_status"].dropna().unique()),
        key="compliance_filter",
    )
    department_filter = st.multiselect(
        "Filter by department",
        sorted(users["department"].dropna().unique()),
        key="department_filter",
    )
    user_type_filter = st.multiselect(
        "Filter by user type",
        sorted(users["user_type"].dropna().unique()),
        key="compliance_user_type_filter",
    )

    comp = users.copy()
    comp = apply_multiselect_filter(comp, "compliance_status", compliance_filter)
    comp = apply_multiselect_filter(comp, "department", department_filter)
    comp = apply_multiselect_filter(comp, "user_type", user_type_filter)

    st.markdown("### Compliance Detail")
    st.dataframe(comp[COMPLIANCE_COLUMNS], 
                 width="stretch")

    st.markdown("### Follow-Up Queue")
    follow_up = users[
        (users["compliance_status"] != "Current")
        & (users["record_status"] == "Active")
    ]
    if follow_up.empty:
        st.success("No active user records currently require compliance follow-up.")
    else:
        st.dataframe(follow_up[COMPLIANCE_COLUMNS], 
                     width="stretch")

    st.markdown("### Compliance by Department")
    st.dataframe(
        count_by(users, ["department", "compliance_status"], "users"),
        width="stretch",
    )

    st.markdown("### Compliance by User Type")
    st.dataframe(
        count_by(users, ["user_type", "compliance_status"], "users"),
        width="stretch",
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
    st.write(
        """
        Upload an access export from a tracked system and compare it against the current
        AccessAtlas access assignment records.
        """
    )

    with st.expander("Expected upload schema"):
        st.write(
            """
            Uploaded reconciliation files should include the following required columns:
            """
        )
        st.dataframe(
            pd.DataFrame(
                {
                    "column_name": RECONCILIATION_REQUIRED_COLUMNS,
                    "description": [
                        "Unique user identifier",
                        "Tracked system identifier",
                        "Type of resource being governed",
                        "Specific resource name",
                        "Permission or role name",
                        "Current access status in the uploaded source",
                    ],
                }
            ),
            width="stretch",
        )
        st.write(
            """
            The optional `source_system_record_id` column can be included to preserve
            traceability back to the source export. First (`first_name`) and last 
            (`last_name`) names may be included in uploads for validation and alignment 
            but are not required for reconciliation, as they may not be identical in 
            the currently present access assignment records. 
            """
        )

    upload = st.file_uploader(
        "Upload CSV with source_system_record_id, user_id, system_id, "
        "resource_type, resource_name, permission_name, access_status",
        type=["csv"],
        key="reconciliation_upload",
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

    st.success("Uploaded file contains all required reconciliation columns.")

    system_options = ["All Systems"] + systems["system_id"].tolist()
    selected_system = st.selectbox("Select reconciliation scope", system_options)

    st.markdown("### Uploaded Access Export")
    st.dataframe(uploaded_df, 
                 width="stretch")

    result = reconcile(access, uploaded_df, selected_system_id=selected_system)
    result_with_system = result.merge(
        systems[["system_id", "system_name"]],
        on="system_id",
        how="left",
    )

    st.markdown("### Reconciliation Summary by Change Type")
    st.dataframe(
        count_by(result_with_system, "change_type"),
        width="stretch",
    )

    st.markdown("### Reconciliation Summary by Resource Type")
    st.dataframe(
        count_by(result_with_system, "resource_type"),
        width="stretch",
    )

    st.markdown("### Action Queue")
    action_queue = result_with_system[
        result_with_system["recommended_action"] != "No action"
    ]
    if action_queue.empty:
        st.success("No reconciliation results currently require follow-up.")
    else:
        st.dataframe(action_queue, 
                     width="stretch")

    st.markdown("### Reconciliation Results")
    change_type_filter = st.multiselect(
        "Filter by change type",
        sorted(result_with_system["change_type"].dropna().unique()),
        key="change_type_filter",
    )

    filtered_results = result_with_system.copy()
    filtered_results = apply_multiselect_filter(
        filtered_results,
        "change_type",
        change_type_filter,
    )

    st.dataframe(filtered_results, 
                 width="stretch")

    st.markdown("### Governance Rule Demonstrated")
    st.warning(
        """
        User access records missing from an uploaded access export are recommended for
        Inactive status review rather than deletion, preserving access history for
        audit purposes. Actual access changes remain outside this reference
        implementation.
        """
    )
