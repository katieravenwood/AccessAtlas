# Snowflake Migration Notes

This document explains how the AccessAtlas reference implementation can be migrated from CSV-backed storage to a Snowflake-backed architecture.

The Streamlit application in this repository uses local CSV files for portability and ease of learning. In a production implementation, those CSV files can be replaced by Snowflake tables and queries while preserving the same application workflows.

---

## Migration Concept

The reference implementation separates two concerns:

```text
User Interface and Governance Logic
        ↓
Data Access Layer
        ↓
CSV files today / Snowflake tables in production
```

The goal is to allow the same Streamlit interface to work against either:

- local CSV files for learning and experimentation
- Snowflake tables for production or enterprise deployment

Only the data loading functions need to change.

---

## CSV-to-Snowflake Mapping

The included CSV files map directly to Snowflake tables:

```text
users.csv → ACCESSATLAS.USERS
systems.csv → ACCESSATLAS.SYSTEMS
access_assignments.csv → ACCESSATLAS.ACCESS_ASSIGNMENTS
system_admin_assignments.csv → ACCESSATLAS.SYSTEM_ADMIN_ASSIGNMENTS
sample_access_upload.csv → ACCESSATLAS.ACCESS_RECONCILIATION_UPLOADS
```

---

## Core Schema

```sql
CREATE SCHEMA IF NOT EXISTS ACCESSATLAS;
```

---

## Users

Stores the central user registry.

```sql
CREATE TABLE ACCESSATLAS.USERS (
    user_id STRING PRIMARY KEY,
    display_name STRING,
    first_name STRING,
    last_name STRING,
    email STRING,
    application_role STRING,
    manager_user_id STRING,
    department STRING,
    user_type STRING,
    record_status STRING,
    annual_training_date DATE,
    biennial_training_date DATE,
    access_agreement_date DATE,
    created_date DATE,
    updated_date DATE
);
```

### Notes

- `user_id` is the stable user identifier used throughout the model.
- `user_type` describes the user's relationship to the organization, such as Employee, Contractor, Vendor, Consultant, or Service Account.
- `record_status` describes whether the record is active for governance purposes.
- Inactive records should generally be retained for audit history.

---

## Systems

Stores governed applications, platforms, databases, dashboards, sites, folders, and other managed resources.

```sql
CREATE TABLE ACCESSATLAS.SYSTEMS (
    system_id STRING PRIMARY KEY,
    system_name STRING,
    system_type STRING,
    system_category STRING,
    resource_scope STRING,
    access_model STRING,
    tracking_method STRING,
    system_owner STRING,
    admin_group STRING,
    record_status STRING,
    notes STRING
);
```

### Users Notes

- `system_type` describes the technical type of system.
- `system_category` describes the governance pattern.
- `resource_scope` describes the level at which access is usually governed.
- `system_owner` and `admin_group` support accountability and governance reporting.

---

## Access Assignments

Stores user-to-system access records at the resource and permission level.

```sql
CREATE TABLE ACCESSATLAS.ACCESS_ASSIGNMENTS (
    access_id STRING PRIMARY KEY,
    user_id STRING,
    system_id STRING,
    resource_type STRING,
    resource_name STRING,
    permission_name STRING,
    access_status STRING,
    granted_date DATE,
    revoked_date DATE,
    source STRING
);
```

### Access Model

AccessAtlas models access using the following pattern:

```text
User → System → Resource → Permission
```

Examples:

```text
User → Dashboard Platform → Management Dashboard → Viewer
User → Reporting Database → analytics_schema → Read
User → Enterprise Data Platform → ROLE_DATA_READER → Data Reader
```

---

## System Administrator Assignments

Stores system-level administrative responsibility.

```sql
CREATE TABLE ACCESSATLAS.SYSTEM_ADMIN_ASSIGNMENTS (
    admin_assignment_id STRING PRIMARY KEY,
    user_id STRING,
    system_id STRING,
    admin_role STRING,
    assignment_status STRING,
    granted_date DATE,
    revoked_date DATE,
    assigned_by STRING,
    assignment_source STRING,
    notes STRING
);
```

### Sys Admin Assignments Notes

This table supports the pattern:

```text
User → System → Administrative Role
```

It intentionally models system-level administration only. Resource-level administration can be added later if needed.

---

## Access Reconciliation Runs

Stores metadata for each reconciliation event.

```sql
CREATE TABLE ACCESSATLAS.ACCESS_RECONCILIATION_RUNS (
    reconciliation_run_id STRING PRIMARY KEY,
    system_id STRING,
    reconciliation_type STRING,
    upload_file_name STRING,
    uploaded_by STRING,
    uploaded_at TIMESTAMP_NTZ,
    reconciliation_status STRING
);
```

### Example reconciliation types

- Application Access
- Role Assignment
- Database Permission
- Dashboard Access
- Site Membership

---

## Access Reconciliation Uploads

Stores raw uploaded access export records before reconciliation processing.

```sql
CREATE TABLE ACCESSATLAS.ACCESS_RECONCILIATION_UPLOADS (
    upload_id STRING PRIMARY KEY,
    reconciliation_run_id STRING,
    source_system_record_id STRING,
    user_id STRING,
    system_id STRING,
    resource_type STRING,
    resource_name STRING,
    permission_name STRING,
    access_status STRING
);
```

### Access Reconciliation Uploads Notes

The optional `source_system_record_id` field preserves traceability back to the source export.

---

## Access Reconciliation Results

Stores comparison results generated from a reconciliation run.

```sql
CREATE TABLE ACCESSATLAS.ACCESS_RECONCILIATION_RESULTS (
    reconciliation_result_id STRING PRIMARY KEY,
    reconciliation_run_id STRING,
    source_system_record_id STRING,
    user_id STRING,
    system_id STRING,
    resource_type STRING,
    resource_name STRING,
    permission_name STRING,
    current_access_status STRING,
    uploaded_access_status STRING,
    change_type STRING,
    recommended_action STRING,
    reviewed_by STRING,
    reviewed_at TIMESTAMP_NTZ,
    review_status STRING
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

This key allows reconciliation at the resource-permission level rather than only at the user or system level.

---

## Supported Reconciliation Patterns

The same structure can support multiple access review patterns:

### Application access reconciliation

```text
User → Application → Application Role
```

### Role assignment reconciliation

```text
User → Cloud Platform → Platform Role
```

### Database permission reconciliation

```text
User → Database → Schema/Table → Permission
```

### Dashboard access reconciliation

```text
User → Dashboard Platform → Dashboard → Viewer/Admin Role
```

### Site membership reconciliation

```text
User → Collaboration Site → Site/Folder → Membership Role
```

---

## Streamlit Data Loading Pattern

The reference implementation currently loads CSV files with a cached data-loading function.

A Snowflake-backed implementation would replace the CSV loader with Snowflake queries.

### CSV pattern

```python
@st.cache_data
def load_csv(filename, date_columns=None):
    return pd.read_csv(
        DATA_DIR / filename,
        parse_dates=date_columns or []
    )
```

### Snowflake connection pattern

```python
from snowflake.connector import connect
import pandas as pd
import streamlit as st


@st.cache_resource
def get_connection():
    return connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
    )


@st.cache_data
def run_query(sql):
    conn = get_connection()
    return pd.read_sql(sql, conn)
```

---

## Why Caching Matters

Streamlit reruns the application script when users interact with filters, dropdowns, upload controls, or tabs.

Without caching, each interaction could trigger repeated Snowflake queries.

Recommended pattern:

- use `@st.cache_resource` for Snowflake connections
- use `@st.cache_data` for query results and lookup tables

This improves performance and reduces unnecessary warehouse usage.

---

## Example Snowflake-Backed Loader

```python
@st.cache_data
def load_data():
    return {
        "users": run_query("SELECT * FROM ACCESSATLAS.USERS"),
        "systems": run_query("SELECT * FROM ACCESSATLAS.SYSTEMS"),
        "access_assignments": run_query(
            "SELECT * FROM ACCESSATLAS.ACCESS_ASSIGNMENTS"
        ),
        "system_admin_assignments": run_query(
            "SELECT * FROM ACCESSATLAS.SYSTEM_ADMIN_ASSIGNMENTS"
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

## Production Considerations

A production Snowflake implementation should consider:

- role-based Snowflake access controls
- least-privilege database roles
- secure secrets management
- separation of development and production schemas
- scheduled ingestion of source access exports
- audit logging
- reconciliation run history
- notification history
- data retention rules
- warehouse usage monitoring
- backup and recovery expectations

---

## Future Schema Extensions

Common production extensions include:

- `ENVIRONMENTS`
- `RESOURCES`
- `RESOURCE_GROUPS`
- `APPROVAL_WORKFLOWS`
- `NOTIFICATION_HISTORY`
- `AUDIT_EVENTS`
- `USER_GROUPS`
- `TEAM_MEMBERSHIPS`
- `ACCESS_REVIEW_CAMPAIGNS`
- `DATA_QUALITY_CHECKS`

These extensions are intentionally excluded from the starter model to keep the reference implementation understandable and easy to adapt.
