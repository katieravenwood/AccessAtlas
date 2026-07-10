"""AccessAtlas application module."""

from pathlib import Path


def _find_project_root():
    """Find the nearest parent containing the shared AccessAtlas data directory."""
    current_path = Path(__file__).resolve().parent
    for candidate in (current_path, *current_path.parents):
        if (candidate / "data").is_dir():
            return candidate
    return Path.cwd()


PROJECT_ROOT = _find_project_root()
DATA_DIR = PROJECT_ROOT / "data"

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

TRAINING_RECONCILIATION_DATE_COLUMNS = [
    "annual_training_date",
    "biennial_training_date",
    "access_agreement_date",
]

TRAINING_RECONCILIATION_REQUIRED_COLUMNS = [
    "user_id"
] + TRAINING_RECONCILIATION_DATE_COLUMNS

ROLE_VISIBLE_TABS = {
    "User": ["My Access"],
    "Manager": ["Dashboard", "My Access", "Manage Access", "Access Reconciliation"],
    "System Administrator": [
        "Dashboard",
        "My Access",
        "Manage Access",
        "Access Reconciliation",
    ],
    "Super Administrator": [
        "Dashboard",
        "My Access",
        "Manage Access",
        "Access Reconciliation",
        "AccessAtlas App Admin",
    ],
}

TAB_LABELS = [
    "Dashboard",
    "My Access",
    "Manage Access",
    "Access Reconciliation",
    "AccessAtlas App Admin",
]

TAB_DISPLAY_LABELS = {
    "Dashboard": "🏠 Dashboard",
    "My Access": "👤 My Access",
    "Manage Access": "🛠️ Manage Access",
    "Access Reconciliation": "🔄 Access Reconciliation",
    "AccessAtlas App Admin": "⚙️ AccessAtlas App Admin",
}

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

COLUMN_LABELS = {
    "access_agreement_date": "Access Agreement Date",
    "access_id": "Access ID",
    "access_model": "Access Model",
    "access_records": "Access Records",
    "access_status": "Access Status",
    "admin_assignment_count": "Admin Assignments",
    "admin_group": "Admin Group",
    "admin_role": "Admin Role",
    "annual_training_date": "Annual Training Date",
    "annual_training_expiration": "Annual Training Expiration",
    "application_role": "Application Role",
    "assignment_source": "Assignment Source",
    "assignment_status": "Assignment Status",
    "assigned_by": "Assigned By",
    "assigned_users": "Assigned Users",
    "audit_event_id": "Audit Event ID",
    "biennial_training_date": "Biennial Training Date",
    "biennial_training_expiration": "Biennial Training Expiration",
    "change_type": "Change Type",
    "changes_identified": "Changes Identified",
    "changes_made": "Changes Made",
    "compliance_status": "Compliance Status",
    "current_access_agreement_date": "Current Access Agreement Date",
    "current_access_status": "Current Access Status",
    "current_annual_training_date": "Current Annual Training Date",
    "current_biennial_training_date": "Current Biennial Training Date",
    "current_record_status": "Current Record Status",
    "department": "Department",
    "display_name": "Display Name",
    "email": "Email",
    "expiration_date": "Expiration Date",
    "expiration_status": "Expiration Status",
    "first_name": "First Name",
    "granted_date": "Granted Date",
    "last_name": "Last Name",
    "manager_user_id": "Manager User ID",
    "notes": "Notes",
    "permission_name": "Permission",
    "record_status": "Record Status",
    "record_type": "Record Type",
    "recommended_action": "Recommended Action",
    "resource_name": "Resource Name",
    "resource_scope": "Resource Scope",
    "resource_type": "Resource Type",
    "revoked_date": "Revoked Date",
    "source": "Source",
    "source_system_record_id": "Source Record ID",
    "system_category": "System Category",
    "system_id": "System ID",
    "system_name": "System Name",
    "system_owner": "System Owner",
    "system_type": "System Type",
    "tracking_method": "Tracking Method",
    "uploaded_access_agreement_date": "Uploaded Access Agreement Date",
    "uploaded_access_status": "Uploaded Access Status",
    "uploaded_annual_training_date": "Uploaded Annual Training Date",
    "uploaded_biennial_training_date": "Uploaded Biennial Training Date",
    "user_id": "User ID",
    "user_type": "User Type",
    "users": "Users",
}
