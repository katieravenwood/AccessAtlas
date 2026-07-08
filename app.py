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

ROLE_VISIBLE_TABS = {
    "User": ["My Access"],
    "Manager": ["Dashboard", "My Access", "Manage Access", "Review Changes"],
    "System Administrator": [
        "Dashboard",
        "My Access",
        "Manage Access",
        "Review Changes",
    ],
    "Super Administrator": [
        "Dashboard",
        "My Access",
        "Manage Access",
        "Review Changes",
        "Administration",
    ],
}

TAB_LABELS = [
    "Dashboard",
    "My Access",
    "Manage Access",
    "Review Changes",
    "Administration",
]


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


def render_self_service_update_form(selected_user):
    """Render a self-service form for updating training and agreement dates."""
    st.markdown("### Update My Certification and Agreement Dates")
    st.caption(
        "This demo form updates the selected user's compliance dates for the "
        "current Streamlit session. In production, this would write to an approved "
        "database workflow and may require review or approval."
    )

    annual_default = pd.to_datetime(selected_user["annual_training_date"]).date()
    biennial_default = pd.to_datetime(selected_user["biennial_training_date"]).date()
    agreement_default = pd.to_datetime(selected_user["access_agreement_date"]).date()

    with st.form("self_service_compliance_update_form"):
        updated_annual_date = st.date_input(
            "Annual training completion date",
            value=annual_default,
            key="update_annual_training_date",
        )
        updated_biennial_date = st.date_input(
            "Biennial training completion date",
            value=biennial_default,
            key="update_biennial_training_date",
        )
        updated_agreement_date = st.date_input(
            "Access agreement completion date",
            value=agreement_default,
            key="update_access_agreement_date",
        )

        updated_annual_expiration = pd.Timestamp(updated_annual_date) + pd.DateOffset(
            years=ANNUAL_TRAINING_VALID_YEARS
        )
        updated_biennial_expiration = pd.Timestamp(updated_biennial_date) + pd.DateOffset(
            years=BIENNIAL_TRAINING_VALID_YEARS
        )

        st.write(
            f"""
            **Calculated annual training expiration:** {updated_annual_expiration.date()}  
            **Calculated biennial training expiration:** {updated_biennial_expiration.date()}
            """
        )

        submitted = st.form_submit_button("Update My Dates")

    if submitted:
        update_user_compliance_dates(
            selected_user["user_id"],
            updated_annual_date,
            updated_biennial_date,
            updated_agreement_date,
        )
        st.success(
            "Compliance dates updated for this demo session. Refreshing the app "
            "or clearing session state will reset the sample CSV-backed data."
        )
        st.rerun()



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



def get_admin_system_ids(system_admins, user_id):
    """Return system IDs actively administered by the selected user."""
    return system_admins[
        (system_admins["user_id"] == user_id)
        & (system_admins["assignment_status"] == "Active")
    ]["system_id"].dropna().unique().tolist()


def get_manager_report_ids(users, manager_user_id):
    """Return direct report user IDs for the selected manager."""
    return users[
        users["manager_user_id"] == manager_user_id
    ]["user_id"].dropna().unique().tolist()


def get_role_scope(users, systems, access, system_admins, current_user):
    """Return visible user and system IDs for the selected simulated role."""
    role = current_user["application_role"]
    current_user_id = current_user["user_id"]

    if role == "Super Administrator":
        return {
            "user_ids": users["user_id"].dropna().unique().tolist(),
            "system_ids": systems["system_id"].dropna().unique().tolist(),
        }

    if role == "Manager":
        direct_reports = get_manager_report_ids(users, current_user_id)
        visible_user_ids = sorted(set([current_user_id] + direct_reports))
        visible_system_ids = access[
            access["user_id"].isin(visible_user_ids)
        ]["system_id"].dropna().unique().tolist()
        return {
            "user_ids": visible_user_ids,
            "system_ids": visible_system_ids,
        }

    if role == "System Administrator":
        administered_system_ids = get_admin_system_ids(system_admins, current_user_id)
        visible_user_ids = access[
            access["system_id"].isin(administered_system_ids)
        ]["user_id"].dropna().unique().tolist()
        return {
            "user_ids": sorted(set(visible_user_ids)),
            "system_ids": administered_system_ids,
        }

    return {
        "user_ids": [current_user_id],
        "system_ids": access[
            access["user_id"] == current_user_id
        ]["system_id"].dropna().unique().tolist(),
    }


def apply_demo_role_scope(users, systems, access, system_admins, current_user):
    """Return datasets scoped to the selected simulated role.

    Demo Mode scoping is for learning and demonstration only. It is not a
    substitute for production authentication, authorization, or row-level
    security.
    """
    scope = get_role_scope(users, systems, access, system_admins, current_user)
    visible_user_ids = scope["user_ids"]
    visible_system_ids = scope["system_ids"]

    scoped_users = users[users["user_id"].isin(visible_user_ids)].copy()
    scoped_systems = systems[systems["system_id"].isin(visible_system_ids)].copy()
    scoped_access = access[
        access["user_id"].isin(visible_user_ids)
        & access["system_id"].isin(visible_system_ids)
    ].copy()

    if current_user["application_role"] == "System Administrator":
        scoped_system_admins = system_admins[
            system_admins["system_id"].isin(visible_system_ids)
        ].copy()
    else:
        scoped_system_admins = system_admins[
            system_admins["user_id"].isin(visible_user_ids)
            | system_admins["system_id"].isin(visible_system_ids)
        ].copy()

    return scoped_users, scoped_systems, scoped_access, scoped_system_admins


def should_show_user_registry(current_user):
    """Return whether the current simulated role should see the user registry section."""
    return current_user["application_role"] != "User"


def render_demo_scope_summary(users, systems, access, system_admins):
    """Render a sidebar summary of the currently visible demo scope."""
    st.sidebar.markdown("### Visible Demo Scope")
    st.sidebar.write(
        f"""
        **Users:** {len(users)}  
        **Systems:** {len(systems)}  
        **Access Records:** {len(access)}  
        **Admin Assignments:** {len(system_admins)}
        """
    )


def render_sidebar_guidance(selected_section):
    """Render contextual sidebar guidance for selected role-visible sections."""
    guidance = {
        "Dashboard": {
            "title": "Dashboard Guidance",
            "body": """
            The dashboard shows a simplified health summary for your visible scope.

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
            Manage Access combines managed-user review, managed-system review, and scoped edit/add workflows.

            System Administrators see only users and systems in their administered
            scope. Super Administrators see all records.
            """,
        },
        "Review Changes": {
            "title": "Review Changes Guidance",
            "body": """
            Review Changes contains the reconciliation workflow and Action Queue.

            Use it to add, update, or inactivate access assignment records based on
            uploaded access exports.
            """,
        },
        "Administration": {
            "title": "Administration Guidance",
            "body": """
            Administration contains compliance monitoring and administrator coverage
            views for Super Administrators.
            """,
        },
    }

    if selected_section not in guidance:
        return

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {guidance[selected_section]['title']}")
    st.sidebar.info(guidance[selected_section]["body"])


def get_demo_user_options(users):
    """Return formatted demo user options for the sidebar selector."""
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


def get_current_demo_user(users, selected_label):
    """Return the selected demo user row based on the sidebar label."""
    demo_options = get_demo_user_options(users)
    selected_user_id = demo_options[
        demo_options["demo_label"] == selected_label
    ].iloc[0]["user_id"]
    return users[users["user_id"] == selected_user_id].iloc[0]


def get_visible_tabs(application_role):
    """Return the tab labels visible to the selected demo role."""
    return ROLE_VISIBLE_TABS.get(application_role, ["Overview"])


def is_tab_visible(tab_name, visible_tabs):
    """Return whether a tab should be rendered for the selected demo role."""
    return tab_name in visible_tabs


def render_hidden_tab_message(tab_name, current_user):
    """Render a standard message for tabs hidden from the current demo role."""
    st.info(
        f"The {tab_name} section is not visible when viewing the app as "
        f"{current_user['application_role']}. Select a different demo account "
        "from the sidebar to view this functionality."
    )




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


def apply_reconciliation_actions(access_df, selected_rows):
    """Apply selected reconciliation actions and return updated access data plus counts."""
    updated_access = access_df.copy()
    counts = {
        "added": 0,
        "inactivated": 0,
        "updated": 0,
        "skipped": 0,
    }

    for _, row in selected_rows.iterrows():
        updated_access, outcome = apply_reconciliation_action(updated_access, row)
        counts[outcome] += 1

    return updated_access, counts



data = load_data()
initialize_user_update_state()
initialize_editable_user_state(data["users"])
users = get_editable_users(data["users"])
users = apply_user_compliance_updates(users)
users = add_expirations(users)
systems = data["systems"]
access = data["access_assignments"]
system_admins = data["system_admin_assignments"]

initialize_editable_access_state(access)
access = get_editable_access_assignments(access)

all_users = users.copy()
all_systems = systems.copy()
all_access = access.copy()
all_system_admins = system_admins.copy()

access_with_systems = access.merge(systems, on="system_id", how="left")

st.sidebar.title("Demo Mode")
st.sidebar.warning(
    "Demo Mode is for simulated role-based visibility demonstration purposes only, not a true " \
    "authentication method. "
)
st.sidebar.write(
    "Select an example user account to view the application from that role's perspective."
)

demo_options = get_demo_user_options(users)
selected_demo_label = st.sidebar.selectbox(
    "View app as",
    demo_options["demo_label"].tolist(),
)
current_user = get_current_demo_user(users, selected_demo_label)
visible_tabs = get_visible_tabs(current_user["application_role"])

st.sidebar.markdown("### Current Demo User")
st.sidebar.write(
    f"""
    **Name:** {current_user['display_name']}  
    **Role:** {current_user['application_role']}  
    **User Type:** {current_user['user_type']}  
    **Department:** {current_user['department']}
    """
)

users, systems, access, system_admins = apply_demo_role_scope(
    all_users,
    all_systems,
    all_access,
    all_system_admins,
    current_user,
)
access_with_systems = access.merge(systems, on="system_id", how="left")
render_demo_scope_summary(users, systems, access, system_admins)

st.title("AccessAtlas")
st.caption(
    "Reference implementation for centralized access governance across "
    "applications, databases, data platforms, dashboards, and collaboration sites."
)

st.info(
    f"Viewing as **{current_user['display_name']}** "
    f"with role **{current_user['application_role']}**. "
    "Visible sections and records are controlled by simulated demo-role rules."
)

def render_overview_tab():
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

    st.markdown("### User Record Status")
    st.dataframe(
    count_by(users, "record_status", "users"), 
    use_container_width=True,
    )

    st.markdown("### Compliance Status")
    st.dataframe(
    count_by(users, "compliance_status", "users"), 
    use_container_width=True,
    )

    st.markdown("### Access Records by System Type")
    st.dataframe(
    count_by(access_with_systems, "system_type"), 
    use_container_width=True,
    )

    st.markdown("### Access Records by Resource Type")
    st.dataframe(
    count_by(access_with_systems, "resource_type"), 
    use_container_width=True,
    )

    st.markdown("### Access Records by Access Status")
    st.dataframe(
    count_by(access, "access_status"), 
    use_container_width=True,
    )



def render_selected_user_profile(selected_user_id, user_selection_enabled=True):
    """Render an individual user's governance profile."""
    selected_user = users[users["user_id"] == selected_user_id].iloc[0]
    manager_name = get_display_name(all_users, selected_user["manager_user_id"])

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
        use_container_width=True,
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
            use_container_width=True,
        )

    st.markdown("### Detailed Access Assignments")
    st.dataframe(selected_access, 
                use_container_width=True)

    st.markdown("### Administrative Assignments")
    if selected_admin_assignments.empty:
        st.info("This user is not assigned as an administrator for any tracked systems.")
    else:
        st.dataframe(selected_admin_assignments, 
                    use_container_width=True)


def render_my_record_tab():
    """Render the self-service individual user record tab."""
    st.subheader("My Record")
    st.caption(
        "This view shows the selected user's own governance profile, compliance "
        "dates, access assignments, and administrative assignments."
    )

    current_user_id = current_user["user_id"]
    if current_user_id not in users["user_id"].tolist():
        st.warning(
            "The selected demo user is outside the current scoped user dataset. "
            "Select another demo account or review the role-scoping rules."
        )
        return

    render_selected_user_profile(current_user_id, user_selection_enabled=False)

    selected_user = users[users["user_id"] == current_user_id].iloc[0]
    render_self_service_update_form(selected_user)


def render_users_tab():
    st.subheader("User Management Registry")

    if current_user["application_role"] == "System Administrator":
        st.caption(
            "Showing only users with access to systems administered by the selected "
            "System Administrator demo account."
        )
    elif current_user["application_role"] == "Manager":
        st.caption(
            "Showing users within the selected Manager demo account's visible review scope."
        )

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        role_filter = st.multiselect(
            "Filter by application role",
            sorted(users["application_role"].dropna().unique()),
            key="role_filter",
        )
    with filter_col2:
        type_filter = st.multiselect(
            "Filter by user type",
            sorted(users["user_type"].unique()),
            key="type_filter",
        )
    with filter_col3:
        status_filter = st.multiselect(
            "Filter by record status",
            sorted(users["record_status"].dropna().unique()),
            key="status_filter",
        )

    user_view = users.copy()
    user_view = apply_multiselect_filter(user_view, "application_role", role_filter)
    user_view = apply_multiselect_filter(user_view, "user_type", type_filter)
    user_view = apply_multiselect_filter(user_view, "record_status", status_filter)

    st.dataframe(
        user_view[USER_DISPLAY_COLUMNS],
        use_container_width=True,
    )

    st.markdown("### Selected User Access Profile")
    selected_user_id = st.selectbox(
        "Select user ID",
        users["user_id"],
        key="selected_user_id",
    )
    render_selected_user_profile(selected_user_id)


def render_systems_tab():
    st.subheader("System Catalog")

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        system_type_filter = st.multiselect(
            "Filter by system type",
            sorted(systems["system_type"].dropna().unique()),
            key="system_type_filter",
        )
    with filter_col2:
        system_category_filter = st.multiselect(
            "Filter by system category",
            sorted(systems["system_category"].dropna().unique()),
            key="system_category_filter",
        )
    with filter_col3:
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
                use_container_width=True)

    st.markdown("### Selected System Access Profile")
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
            all_users[["user_id", "display_name", "email", "department"]],
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
            use_container_width=True,
        )

    st.markdown("### System Administrators")
    if selected_system_admins.empty:
        st.info("No system administrator assignments are currently recorded for this system.")
    else:
        st.dataframe(selected_system_admins, 
                    use_container_width=True)

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
            use_container_width=True,
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


def render_system_admins_tab():
    st.subheader("System Administrator Assignments")

    admin_view = (
        system_admins.merge(
            all_users[["user_id", "display_name", "email", "department"]],
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
                use_container_width=True)

    st.markdown("### Administrator-Centered View")
    selected_admin = st.selectbox(
        "Select administrator",
        sorted(admin_view["display_name"].dropna().unique()),
        key="selected_administrator",
    )
    st.dataframe(
        admin_view[admin_view["display_name"] == selected_admin],
        use_container_width=True,
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
                    use_container_width=True)

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
                use_container_width=True)


def render_compliance_tab():
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
                use_container_width=True)

    st.markdown("### Follow-Up Queue")
    follow_up = users[
        (users["compliance_status"] != "Current")
        & (users["record_status"] == "Active")
    ]
    if follow_up.empty:
        st.success("No active user records currently require compliance follow-up.")
    else:
        st.dataframe(follow_up[COMPLIANCE_COLUMNS], 
                    use_container_width=True)

    st.markdown("### Compliance by Department")
    st.dataframe(
        count_by(users, ["department", "compliance_status"], "users"),
        use_container_width=True,
    )

    st.markdown("### Compliance by User Type")
    st.dataframe(
        count_by(users, ["user_type", "compliance_status"], "users"),
        use_container_width=True,
    )




def get_allowed_management_systems():
    """Return systems available for direct access management for the current role."""
    if current_user["application_role"] == "Super Administrator":
        return systems.copy()

    if current_user["application_role"] == "System Administrator":
        return systems.copy()

    return systems.iloc[0:0].copy()


def get_user_options_for_access_management():
    """Return user records available for access management for the current role."""
    if current_user["application_role"] == "Super Administrator":
        return all_users.copy()

    if current_user["application_role"] == "System Administrator":
        return users.copy()

    return users.iloc[0:0].copy()


def apply_single_access_record_change(
    mode,
    access_id,
    user_id,
    system_id,
    resource_type,
    resource_name,
    permission_name,
    access_status,
    granted_date,
    revoked_date,
    source,
):
    """Add or update one access assignment record in session state."""
    current_access = st.session_state["editable_access_assignments"].copy()

    record = {
        "access_id": access_id,
        "user_id": user_id,
        "system_id": system_id,
        "resource_type": resource_type,
        "resource_name": resource_name,
        "permission_name": permission_name,
        "access_status": access_status,
        "granted_date": pd.Timestamp(granted_date) if granted_date else pd.NaT,
        "revoked_date": pd.Timestamp(revoked_date) if revoked_date else pd.NaT,
        "source": source,
    }

    if mode == "Add new access record":
        st.session_state["editable_access_assignments"] = pd.concat(
            [current_access, pd.DataFrame([record])],
            ignore_index=True,
        )
        return "added"

    match = current_access["access_id"] == access_id
    if not match.any():
        return "not_found"

    for column_name, value in record.items():
        current_access.loc[match, column_name] = value

    st.session_state["editable_access_assignments"] = current_access
    return "updated"


def render_add_user_form(allowed_systems):
    """Render a demo form for adding one user and optional initial access."""
    st.subheader("Add User")
    st.caption(
        "Add one synthetic user record to the in-session demo user registry. "
        "For System Administrators, an initial access assignment is required so "
        "the new user remains inside the administered-system scope."
    )

    next_user_id = generate_next_user_id(st.session_state["editable_users"])
    manager_options = all_users.copy()
    manager_options["manager_label"] = (
        manager_options["display_name"].astype(str)
        + " ("
        + manager_options["user_id"].astype(str)
        + ")"
    )
    manager_labels = ["Not assigned"] + manager_options["manager_label"].tolist()

    system_options = allowed_systems.copy()
    system_options["system_label"] = (
        system_options["system_name"].astype(str)
        + " ("
        + system_options["system_id"].astype(str)
        + ")"
    )

    with st.form("direct_add_user_form"):
        st.text_input(
            "User ID",
            value=next_user_id,
            key="add_user_id",
            disabled=True,
        )

        first_name = st.text_input("First name", key="add_user_first_name")
        last_name = st.text_input("Last name", key="add_user_last_name")
        email = st.text_input("Email", key="add_user_email")

        application_role = st.selectbox(
            "Application role",
            ["User", "Manager", "System Administrator", "Super Administrator"],
            index=0,
            key="add_user_application_role",
        )
        manager_label = st.selectbox(
            "Manager",
            manager_labels,
            key="add_user_manager",
        )
        department = st.text_input("Department", value="General Operations", key="add_user_department")
        user_type = st.selectbox(
            "User type",
            ["Employee", "Contractor", "Vendor", "Consultant", "Service Account"],
            key="add_user_type",
        )
        record_status = st.selectbox(
            "Record status",
            ["Active", "Leave", "Inactive"],
            key="add_user_record_status",
        )

        annual_training_date = st.date_input(
            "Annual training completion date",
            value=date.today(),
            key="add_user_annual_training_date",
        )
        biennial_training_date = st.date_input(
            "Biennial training completion date",
            value=date.today(),
            key="add_user_biennial_training_date",
        )
        access_agreement_date = st.date_input(
            "Access agreement completion date",
            value=date.today(),
            key="add_user_access_agreement_date",
        )

        st.markdown("### Initial Access Assignment")
        require_initial_access = current_user["application_role"] == "System Administrator"
        add_initial_access = st.checkbox(
            "Create initial access assignment",
            value=require_initial_access,
            disabled=require_initial_access,
            key="add_user_create_initial_access",
        )

        selected_system_label = None
        resource_type = "Application"
        resource_name = ""
        permission_name = ""
        access_status = "Active"
        granted_date = date.today()
        source = "Direct User Entry"

        if add_initial_access:
            selected_system_label = st.selectbox(
                "System",
                system_options["system_label"].tolist(),
                key="add_user_initial_system",
            )
            resource_type = st.selectbox(
                "Resource type",
                ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"],
                key="add_user_initial_resource_type",
            )
            resource_name = st.text_input(
                "Resource name",
                value="General Access",
                key="add_user_initial_resource_name",
            )
            permission_name = st.text_input(
                "Permission name",
                value="Viewer",
                key="add_user_initial_permission_name",
            )
            access_status = st.selectbox(
                "Access status",
                ["Active", "Inactive", "Pending Review"],
                key="add_user_initial_access_status",
            )
            granted_date = st.date_input(
                "Granted date",
                value=date.today(),
                key="add_user_initial_granted_date",
            )
            source = st.text_input(
                "Source",
                value="Direct User Entry",
                key="add_user_initial_source",
            )

        submitted = st.form_submit_button("Add User", type="primary")

    if not submitted:
        return

    if not first_name or not last_name or not email:
        st.error("First name, last name, and email are required.")
        return

    if add_initial_access and (not resource_name or not permission_name):
        st.error("Resource name and permission name are required for the initial access assignment.")
        return

    manager_user_id = ""
    if manager_label != "Not assigned":
        manager_user_id = manager_options[
            manager_options["manager_label"] == manager_label
        ].iloc[0]["user_id"]

    user_outcome = add_user_record(
        next_user_id,
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
    )

    if user_outcome == "duplicate":
        st.error("A user with this generated ID already exists.")
        return

    if add_initial_access:
        selected_system_id = system_options[
            system_options["system_label"] == selected_system_label
        ].iloc[0]["system_id"]

        apply_single_access_record_change(
            "Add new access record",
            generate_next_access_id(st.session_state["editable_access_assignments"]),
            next_user_id,
            selected_system_id,
            resource_type,
            resource_name,
            permission_name,
            access_status,
            granted_date,
            None,
            source,
        )

    st.success("User added for this demo session.")
    st.rerun()


def render_add_edit_access_form():
    """Render direct single-record add/edit access management workflow."""
    st.subheader("Add / Edit Access")
    st.caption(
        "Add or edit one user access assignment without uploading a reconciliation file. "
        "Super Administrators can manage all systems. System Administrators can manage "
        "only users and systems within their scoped administered systems."
    )

    allowed_systems = get_allowed_management_systems()
    allowed_users = get_user_options_for_access_management()

    if allowed_systems.empty or allowed_users.empty:
        st.warning("No users or systems are available for management in the current role scope.")
        return

    mode = st.radio(
        "Management action",
        ["Add new access record", "Edit existing access record"],
        horizontal=True,
        key="direct_access_management_mode",
    )

    current_access = st.session_state["editable_access_assignments"].copy()
    scoped_current_access = current_access[
        current_access["system_id"].isin(allowed_systems["system_id"])
    ].copy()

    if current_user["application_role"] == "System Administrator":
        scoped_current_access = scoped_current_access[
            scoped_current_access["user_id"].isin(allowed_users["user_id"])
        ]

    with st.expander("Current manageable access records", expanded=False):
        if scoped_current_access.empty:
            st.info("No existing access records are currently available in this management scope.")
        else:
            st.dataframe(
                scoped_current_access.merge(
                    allowed_systems[["system_id", "system_name"]],
                    on="system_id",
                    how="left",
                ).merge(
                    all_users[["user_id", "display_name", "email"]],
                    on="user_id",
                    how="left",
                ),
                use_container_width=True,
            )

    selected_existing = None
    if mode == "Edit existing access record":
        if scoped_current_access.empty:
            st.warning("There are no existing records available to edit in this scope.")
            return

        access_options = scoped_current_access.copy()
        access_options["access_label"] = (
            access_options["access_id"].astype(str)
            + " — "
            + access_options["user_id"].astype(str)
            + " / "
            + access_options["system_id"].astype(str)
            + " / "
            + access_options["resource_name"].astype(str)
            + " / "
            + access_options["permission_name"].astype(str)
        )

        selected_access_label = st.selectbox(
            "Select access record to edit",
            access_options["access_label"].tolist(),
            key="direct_access_record_select",
        )
        selected_access_id = access_options[
            access_options["access_label"] == selected_access_label
        ].iloc[0]["access_id"]
        selected_existing = scoped_current_access[
            scoped_current_access["access_id"] == selected_access_id
        ].iloc[0]
        default_access_id = selected_existing["access_id"]
    else:
        default_access_id = generate_next_access_id(current_access)

    user_options = allowed_users.copy()
    user_options["user_label"] = (
        user_options["display_name"].astype(str)
        + " ("
        + user_options["user_id"].astype(str)
        + ")"
    )
    system_options = allowed_systems.copy()
    system_options["system_label"] = (
        system_options["system_name"].astype(str)
        + " ("
        + system_options["system_id"].astype(str)
        + ")"
    )

    default_user_index = 0
    default_system_index = 0
    default_resource_type = "Application"
    default_resource_name = ""
    default_permission_name = ""
    default_access_status = "Active"
    default_granted_date = date.today()
    default_revoked_date = None
    default_source = "Direct Entry"

    if selected_existing is not None:
        if selected_existing["user_id"] in user_options["user_id"].tolist():
            default_user_index = user_options["user_id"].tolist().index(selected_existing["user_id"])
        if selected_existing["system_id"] in system_options["system_id"].tolist():
            default_system_index = system_options["system_id"].tolist().index(selected_existing["system_id"])
        default_resource_type = selected_existing["resource_type"]
        default_resource_name = selected_existing["resource_name"]
        default_permission_name = selected_existing["permission_name"]
        default_access_status = selected_existing["access_status"]
        default_granted_date = pd.to_datetime(selected_existing["granted_date"]).date()
        if pd.notna(selected_existing["revoked_date"]):
            default_revoked_date = pd.to_datetime(selected_existing["revoked_date"]).date()
        default_source = selected_existing["source"]

    with st.form("direct_user_access_management_form"):
        st.text_input(
            "Access ID",
            value=default_access_id,
            key="direct_access_id",
            disabled=True,
        )

        selected_user_label = st.selectbox(
            "User",
            user_options["user_label"].tolist(),
            index=default_user_index,
            key="direct_access_user",
        )
        selected_system_label = st.selectbox(
            "System",
            system_options["system_label"].tolist(),
            index=default_system_index,
            key="direct_access_system",
        )

        resource_type = st.selectbox(
            "Resource type",
            ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"],
            index=(
                ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"]
                .index(default_resource_type)
                if default_resource_type in ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"]
                else 7
            ),
            key="direct_resource_type",
        )
        resource_name = st.text_input(
            "Resource name",
            value=default_resource_name,
            key="direct_resource_name",
        )
        permission_name = st.text_input(
            "Permission name",
            value=default_permission_name,
            key="direct_permission_name",
        )
        access_status = st.selectbox(
            "Access status",
            ["Active", "Inactive", "Pending Review"],
            index=(
                ["Active", "Inactive", "Pending Review"].index(default_access_status)
                if default_access_status in ["Active", "Inactive", "Pending Review"]
                else 0
            ),
            key="direct_access_status",
        )
        granted_date = st.date_input(
            "Granted date",
            value=default_granted_date,
            key="direct_granted_date",
        )

        revoked_date_enabled = st.checkbox(
            "Set revoked date",
            value=default_revoked_date is not None,
            key="direct_revoked_date_enabled",
        )
        revoked_date = None
        if revoked_date_enabled:
            revoked_date = st.date_input(
                "Revoked date",
                value=default_revoked_date or date.today(),
                key="direct_revoked_date",
            )

        source = st.text_input(
            "Source",
            value=default_source,
            key="direct_source",
        )

        submitted = st.form_submit_button(
            "Save Access Record",
            type="primary",
        )

    if submitted:
        selected_user_id = user_options[
            user_options["user_label"] == selected_user_label
        ].iloc[0]["user_id"]
        selected_system_id = system_options[
            system_options["system_label"] == selected_system_label
        ].iloc[0]["system_id"]

        if not resource_name or not permission_name:
            st.error("Resource name and permission name are required.")
            return

        outcome = apply_single_access_record_change(
            mode,
            default_access_id,
            selected_user_id,
            selected_system_id,
            resource_type,
            resource_name,
            permission_name,
            access_status,
            granted_date,
            revoked_date,
            source,
        )

        if outcome == "not_found":
            st.error("The selected access record could not be found.")
        else:
            st.success(f"Access record {outcome} for this demo session.")
            st.rerun()


def render_user_access_management_tab():
    """Render direct add/edit workflows for users and access assignments."""
    st.subheader("Edit / Add Access")
    st.caption(
        "Add users and manage individual access assignments without uploading a reconciliation file."
    )

    allowed_systems = get_allowed_management_systems()

    access_tab, user_tab = st.tabs(["Add / Edit Access", "Add User"])
    with access_tab:
        render_add_edit_access_form()

    with user_tab:
        render_add_user_form(allowed_systems)


def render_access_reconciliation_tab():
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
            use_container_width=True,
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
    selected_system = st.selectbox(
        "Select reconciliation scope",
        system_options,
        key="reconciliation_scope",
    )

    st.markdown("### Uploaded Access Export")
    st.dataframe(uploaded_df, 
                use_container_width=True)

    result = reconcile(access, uploaded_df, selected_system_id=selected_system)
    result_with_system = result.merge(
        systems[["system_id", "system_name"]],
        on="system_id",
        how="left",
    )

    st.markdown("### Reconciliation Summary by Change Type")
    st.dataframe(
        count_by(result_with_system, "change_type"),
        use_container_width=True,
    )

    st.markdown("### Reconciliation Summary by Resource Type")
    st.dataframe(
        count_by(result_with_system, "resource_type"),
        use_container_width=True,
    )

    st.markdown("### Action Queue")
    action_queue = result_with_system[
        result_with_system["recommended_action"] != "No action"
    ].copy()

    if action_queue.empty:
        st.success("No reconciliation results currently require follow-up.")
    else:
        action_queue.insert(0, "apply_action", False)
        editable_action_queue = st.data_editor(
            action_queue,
            use_container_width=True,
            hide_index=True,
            key="reconciliation_action_queue_editor",
            column_config={
                "apply_action": st.column_config.CheckboxColumn(
                    "Apply?",
                    help="Select rows to apply the recommended reconciliation action.",
                    default=False,
                )
            },
            disabled=[
                column for column in action_queue.columns if column != "apply_action"
            ],
        )

        selected_actions = editable_action_queue[
            editable_action_queue["apply_action"] == True
        ].drop(columns=["apply_action"])

        st.caption(
            "Recommended actions update the canonical access assignment table for "
            "this demo session. They do not modify source CSV files."
        )

        if st.button(
            "Apply Recommended Actions",
            key="apply_reconciliation_actions_button",
            disabled=selected_actions.empty,
        ):
            updated_access, action_counts = apply_reconciliation_actions(
                st.session_state["editable_access_assignments"],
                selected_actions,
            )
            st.session_state["editable_access_assignments"] = updated_access
            st.success(
                "Applied reconciliation actions: "
                f"{action_counts['added']} added, "
                f"{action_counts['inactivated']} inactivated, "
                f"{action_counts['updated']} updated, "
                f"{action_counts['skipped']} skipped."
            )
            st.rerun()

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
                use_container_width=True)





def render_dashboard_section():
    """Render a streamlined role-aware dashboard."""
    st.subheader("Dashboard")

    pending_reconciliation = 0
    try:
        uploaded_df = pd.read_csv(DATA_DIR / "sample_access_upload.csv")
        pending_reconciliation = len(
            reconcile(access, uploaded_df)[lambda df: df["recommended_action"] != "No action"]
        )
    except Exception:
        pending_reconciliation = 0

    active_follow_up = len(
        users[
            (users["compliance_status"] != "Current")
            & (users["record_status"] == "Active")
        ]
    )

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Visible Users", len(users))
    d2.metric("Visible Systems", len(systems))
    d3.metric("Access Records", len(access))
    d4.metric("Items Needing Review", pending_reconciliation + active_follow_up)

    if current_user["application_role"] == "User":
        st.info(
            "Use My Access to review your profile, access assignments, and compliance dates."
        )
    elif current_user["application_role"] == "System Administrator":
        st.info(
            "Use Manage Access to review users and systems in your administered scope. "
            "Use Review Changes to process reconciliation exceptions."
        )
    elif current_user["application_role"] == "Manager":
        st.info(
            "Use Manage Access to review users in your visible scope and Review Changes "
            "to inspect access exceptions."
        )
    else:
        st.info(
            "Use Manage Access for user/system records, Review Changes for reconciliation, "
            "and Administration for compliance and administrative coverage."
        )

    with st.expander("View dashboard details"):
        st.markdown("### User Record Status")
        st.dataframe(count_by(users, "record_status", "users"), use_container_width=True)

        st.markdown("### Compliance Status")
        st.dataframe(count_by(users, "compliance_status", "users"), use_container_width=True)

        st.markdown("### Access Records by System Type")
        st.dataframe(count_by(access_with_systems, "system_type"), use_container_width=True)

        st.markdown("### Access Records by Resource Type")
        st.dataframe(count_by(access_with_systems, "resource_type"), use_container_width=True)

        st.markdown("### Access Records by Access Status")
        st.dataframe(count_by(access, "access_status"), use_container_width=True)


def render_manage_access_section():
    """Render user/system access workflows in a streamlined task section."""
    st.subheader("Manage Access")
    st.caption(
        "Review managed users and systems, and perform scoped add/edit workflows "
        "where permitted by the selected demo role."
    )

    managed_users_tab, managed_systems_tab, edit_access_tab = st.tabs(
        ["Managed Users", "Managed Systems", "Edit / Add Access"]
    )

    with managed_users_tab:
        render_users_tab()

    with managed_systems_tab:
        render_systems_tab()

    with edit_access_tab:
        if current_user["application_role"] in ["System Administrator", "Super Administrator"]:
            render_user_access_management_tab()
        else:
            st.info(
                "Direct add/edit access management is available to System Administrator "
                "and Super Administrator demo roles."
            )


def render_review_changes_section():
    """Render reconciliation and action queue workflows."""
    st.subheader("Review Changes")
    st.caption(
        "Upload or review access exports, inspect differences, and apply recommended "
        "session-state updates from the reconciliation action queue."
    )
    render_access_reconciliation_tab()


def render_administration_section():
    """Render administrative and compliance workflows for Super Administrators."""
    st.subheader("Administration")
    st.caption(
        "Review administrative coverage and compliance monitoring details."
    )

    with st.expander("Compliance Monitoring", expanded=True):
        render_compliance_tab()

    with st.expander("System Administrator Assignments"):
        render_system_admins_tab()

TAB_RENDERERS = {
    "Dashboard": render_dashboard_section,
    "My Access": render_my_record_tab,
    "Manage Access": render_manage_access_section,
    "Review Changes": render_review_changes_section,
    "Administration": render_administration_section,
}

active_tabs = [tab_name for tab_name in TAB_LABELS if tab_name in visible_tabs]

selected_section = st.radio(
    "Application section",
    active_tabs,
    horizontal=True,
    key="active_application_section",
)

render_sidebar_guidance(selected_section)

TAB_RENDERERS[selected_section]()
