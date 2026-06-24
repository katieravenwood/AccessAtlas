# PostgreSQL Migration Notes

This document explains how AccessAtlas can be migrated from CSV-backed storage to a PostgreSQL-backed architecture.

The reference implementation uses local CSV files for portability and ease of learning. A production implementation can replace those CSV files with PostgreSQL tables and queries while preserving the same application workflows.

---

## Migration Concept

```text
Streamlit User Interface
        ↓
Governance Logic
        ↓
Data Access Layer
        ↓
CSV files today / PostgreSQL tables in production
```

Only the data loading and write-back functions need to change. The role views, compliance calculations, reconciliation workflow, and governance concepts can remain largely the same.

---

## CSV-to-PostgreSQL Mapping

```text
users.csv → accessatlas.users
systems.csv → accessatlas.systems
access_assignments.csv → accessatlas.access_assignments
system_admin_assignments.csv → accessatlas.system_admin_assignments
sample_access_upload.csv → accessatlas.access_reconciliation_uploads
```

---

## Schema Setup

```sql
CREATE SCHEMA IF NOT EXISTS accessatlas;
```

---

## Users Table

```sql
CREATE TABLE IF NOT EXISTS accessatlas.users (
    user_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    application_role TEXT NOT NULL,
    manager_user_id TEXT REFERENCES accessatlas.users(user_id),
    department TEXT,
    user_type TEXT,
    record_status TEXT NOT NULL,
    annual_training_date DATE,
    biennial_training_date DATE,
    access_agreement_date DATE,
    created_date DATE,
    updated_date DATE
);
```

### Notes

- `user_id` is the stable user identifier.
- `manager_user_id` supports manager and access reviewer workflows.
- `record_status` should generally be updated instead of deleting user records.
- Inactive records should be retained for audit history.

---

## Systems Table

```sql
CREATE TABLE IF NOT EXISTS accessatlas.systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT,
    system_category TEXT,
    resource_scope TEXT,
    access_model TEXT,
    tracking_method TEXT,
    system_owner TEXT,
    admin_group TEXT,
    record_status TEXT NOT NULL,
    notes TEXT
);
```

### Systems Table Notes

- `system_type` describes the technical type of system.
- `system_category` describes the governance pattern.
- `resource_scope` describes the level at which access is usually governed.
- `system_owner` and `admin_group` support accountability and governance reporting.

---

## Access Assignments Table

```sql
CREATE TABLE IF NOT EXISTS accessatlas.access_assignments (
    access_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES accessatlas.users(user_id),
    system_id TEXT NOT NULL REFERENCES accessatlas.systems(system_id),
    resource_type TEXT NOT NULL,
    resource_name TEXT NOT NULL,
    permission_name TEXT NOT NULL,
    access_status TEXT NOT NULL,
    granted_date DATE,
    revoked_date DATE,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Recommended natural key

```sql
CREATE UNIQUE INDEX IF NOT EXISTS uq_access_assignments_access_key
ON accessatlas.access_assignments (
    user_id,
    system_id,
    resource_type,
    resource_name,
    permission_name
);
```

If historical duplicate records are required, use effective dating or an `is_current` flag instead of enforcing the unique index directly.

---

## System Administrator Assignments Table

```sql
CREATE TABLE IF NOT EXISTS accessatlas.system_admin_assignments (
    admin_assignment_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES accessatlas.users(user_id),
    system_id TEXT NOT NULL REFERENCES accessatlas.systems(system_id),
    admin_role TEXT NOT NULL,
    assignment_status TEXT NOT NULL,
    granted_date DATE,
    revoked_date DATE,
    assigned_by TEXT REFERENCES accessatlas.users(user_id),
    assignment_source TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

This table supports:

```text
User → System → Administrative Role
```

---

## Access Reconciliation Runs

```sql
CREATE TABLE IF NOT EXISTS accessatlas.access_reconciliation_runs (
    reconciliation_run_id TEXT PRIMARY KEY,
    system_id TEXT REFERENCES accessatlas.systems(system_id),
    reconciliation_type TEXT,
    upload_file_name TEXT,
    uploaded_by TEXT REFERENCES accessatlas.users(user_id),
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    reconciliation_status TEXT
);
```

---

## Access Reconciliation Uploads

```sql
CREATE TABLE IF NOT EXISTS accessatlas.access_reconciliation_uploads (
    upload_id TEXT PRIMARY KEY,
    reconciliation_run_id TEXT REFERENCES accessatlas.access_reconciliation_runs(reconciliation_run_id),
    source_system_record_id TEXT,
    user_id TEXT,
    system_id TEXT,
    resource_type TEXT,
    resource_name TEXT,
    permission_name TEXT,
    access_status TEXT
);
```

The optional `source_system_record_id` field preserves traceability back to the source export.

---

## Access Reconciliation Results

```sql
CREATE TABLE IF NOT EXISTS accessatlas.access_reconciliation_results (
    reconciliation_result_id TEXT PRIMARY KEY,
    reconciliation_run_id TEXT REFERENCES accessatlas.access_reconciliation_runs(reconciliation_run_id),
    source_system_record_id TEXT,
    user_id TEXT,
    system_id TEXT,
    resource_type TEXT,
    resource_name TEXT,
    permission_name TEXT,
    current_access_status TEXT,
    uploaded_access_status TEXT,
    change_type TEXT,
    recommended_action TEXT,
    reviewed_by TEXT REFERENCES accessatlas.users(user_id),
    reviewed_at TIMESTAMPTZ,
    review_status TEXT
);
```

### Recommended comparison key

```text
user_id
system_id
resource_type
resource_name
permission_name
```

This allows reconciliation at the resource-permission level rather than only at the user or system level.

---

## Optional Audit Events Table

```sql
CREATE TABLE IF NOT EXISTS accessatlas.audit_events (
    audit_event_id TEXT PRIMARY KEY,
    event_timestamp TIMESTAMPTZ DEFAULT NOW(),
    actor_user_id TEXT REFERENCES accessatlas.users(user_id),
    event_type TEXT NOT NULL,
    target_table TEXT,
    target_record_id TEXT,
    event_summary TEXT,
    before_value JSONB,
    after_value JSONB
);
```

This table can capture:

- user self-service updates
- reconciliation actions
- access assignment changes
- administrative assignment changes
- review decisions

---

## Useful Indexes

```sql
CREATE INDEX IF NOT EXISTS idx_access_assignments_user_id
ON accessatlas.access_assignments(user_id);

CREATE INDEX IF NOT EXISTS idx_access_assignments_system_id
ON accessatlas.access_assignments(system_id);

CREATE INDEX IF NOT EXISTS idx_access_assignments_status
ON accessatlas.access_assignments(access_status);

CREATE INDEX IF NOT EXISTS idx_system_admin_assignments_user_id
ON accessatlas.system_admin_assignments(user_id);

CREATE INDEX IF NOT EXISTS idx_system_admin_assignments_system_id
ON accessatlas.system_admin_assignments(system_id);

CREATE INDEX IF NOT EXISTS idx_reconciliation_results_run_id
ON accessatlas.access_reconciliation_results(reconciliation_run_id);

CREATE INDEX IF NOT EXISTS idx_audit_events_actor_user_id
ON accessatlas.audit_events(actor_user_id);
```

---

## Streamlit Connection Pattern

A PostgreSQL-backed implementation can use SQLAlchemy.

```python
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


@st.cache_resource
def get_engine():
    return create_engine(st.secrets["postgres"]["connection_url"])


@st.cache_data
def run_query(sql, params=None):
    engine = get_engine()
    with engine.connect() as connection:
        return pd.read_sql(text(sql), connection, params=params)
```

Example `.streamlit/secrets.toml` pattern:

```toml
[postgres]
connection_url = "postgresql+psycopg2://username:password@host:5432/database"
```

Do not commit real credentials to a repository. Put them in an approved secrets store.

---

## PostgreSQL-Backed Loader

```python
@st.cache_data
def load_data():
    return {
        "users": run_query("SELECT * FROM accessatlas.users"),
        "systems": run_query("SELECT * FROM accessatlas.systems"),
        "access_assignments": run_query(
            "SELECT * FROM accessatlas.access_assignments"
        ),
        "system_admin_assignments": run_query(
            "SELECT * FROM accessatlas.system_admin_assignments"
        ),
    }
```

The rest of the app can continue using:

```python
data = load_data()
users = data["users"]
systems = data["systems"]
access = data["access_assignments"]
system_admins = data["system_admin_assignments"]
```

---

## Write-Back Pattern

Unlike the CSV reference implementation, PostgreSQL can persist user updates and reconciliation actions.

### User self-service update

```python
def update_user_compliance_dates(
    user_id,
    annual_training_date,
    biennial_training_date,
    access_agreement_date,
):
    sql = '''
        UPDATE accessatlas.users
        SET
            annual_training_date = :annual_training_date,
            biennial_training_date = :biennial_training_date,
            access_agreement_date = :access_agreement_date,
            updated_date = CURRENT_DATE
        WHERE user_id = :user_id
    '''

    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(
            text(sql),
            {
                "user_id": user_id,
                "annual_training_date": annual_training_date,
                "biennial_training_date": biennial_training_date,
                "access_agreement_date": access_agreement_date,
            },
        )
```

### Reconciliation inactivation

```python
def inactivate_access_assignment(row):
    sql = '''
        UPDATE accessatlas.access_assignments
        SET
            access_status = 'Inactive',
            revoked_date = CURRENT_DATE,
            updated_at = NOW()
        WHERE user_id = :user_id
          AND system_id = :system_id
          AND resource_type = :resource_type
          AND resource_name = :resource_name
          AND permission_name = :permission_name
    '''

    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(text(sql), row)
```

---

## Transaction Handling

Use transactions for multi-row reconciliation actions.

```python
engine = get_engine()

with engine.begin() as connection:
    for row in selected_rows:
        connection.execute(text(sql), row)
```

If any statement fails, PostgreSQL can roll back the transaction.

This matters because partial reconciliation updates can create more governance confusion than doing nothing. A half-fixed access catalog is a tiny compliance horror movie.

---

## Production Authorization Considerations

Demo Mode is not production security. In production, authorization must be enforced outside the visual interface.

Recommended controls include:

- Single Sign-On or identity provider integration
- backend authorization checks before writes
- least-privilege database roles
- PostgreSQL Row-Level Security where appropriate
- audit logging for updates
- separation of read and write permissions
- approval controls for reconciliation actions

---

## PostgreSQL Row-Level Security Option

PostgreSQL Row-Level Security can enforce scoped data access at the database layer.

```sql
ALTER TABLE accessatlas.access_assignments ENABLE ROW LEVEL SECURITY;
```

A production implementation would usually map application users to database session context or application-managed authorization filters.

For many Streamlit applications, backend application authorization may be simpler than direct per-user database accounts. The important point is not to rely only on hidden UI elements.

---

## Caching Considerations

Streamlit reruns the application script when users interact with widgets.

Recommended pattern:

- use `@st.cache_resource` for PostgreSQL engines or connection pools
- use `@st.cache_data` for query results and lookup tables
- clear or refresh cached data after write operations

Example:

```python
st.cache_data.clear()
```

---

## Production Considerations

A production PostgreSQL implementation should consider:

- schema migrations
- database backups
- point-in-time recovery
- least-privilege database roles
- secure secrets management
- development and production database separation
- audit logging
- reconciliation run history
- notification history
- data retention rules
- performance monitoring
- connection pooling
- application-level and database-level authorization

---

## Future Schema Extensions

Common production extensions include:

- `environments`
- `resources`
- `resource_groups`
- `approval_workflows`
- `notification_history`
- `audit_events`
- `user_groups`
- `team_memberships`
- `access_review_campaigns`
- `data_quality_checks`

These extensions are intentionally excluded from the starter model to keep the reference implementation understandable and easy to adapt.
