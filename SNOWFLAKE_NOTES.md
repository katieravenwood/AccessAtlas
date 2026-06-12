# Snowflake Migration Notes

This reference implementation uses CSV files for portability. In a Snowflake-backed implementation, the same model can be implemented using a small governance schema.

The CSV files used by the reference implementation correspond directly to Snowflake tables. A production implementation can replace local CSV loading with Snowflake queries while preserving the user interface and governance workflow patterns.

## Core Schema

```sql
CREATE SCHEMA IF NOT EXISTS ACCESSATLAS;
```

## Users

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

## Systems

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

## Access Assignments

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

## System Administrator Assignments

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

## Access Reconciliation Runs

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

## Access Reconciliation Uploads

This optional staging table preserves raw uploaded access data before reconciliation results are generated.

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

## Access Reconciliation Results

```sql
CREATE TABLE ACCESSATLAS.ACCESS_RECONCILIATION_RESULTS (
    reconciliation_result_id STRING PRIMARY KEY,
    reconciliation_run_id STRING,
    user_id STRING,
    system_id STRING,
    resource_type STRING,
    resource_name STRING,
    permission_name STRING,
    current_app_status STRING,
    uploaded_status STRING,
    change_type STRING,
    recommended_action STRING,
    reviewed_by STRING,
    reviewed_at TIMESTAMP_NTZ,
    review_status STRING
);
```

## Supported Reconciliation Examples

The reference model can support multiple reconciliation patterns:

- Application Access Reconciliation
- Role Assignment Reconciliation
- Database Permission Reconciliation
- Dashboard Access Reconciliation
- Site Membership Reconciliation

The recommended comparison key is:

```text
user_id
system_id
resource_type
resource_name
permission_name
```

## Streamlit Replacement Pattern

Replace local CSV loading with a Snowflake query function:

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

In production, credentials should be managed using approved secrets management and organizational security standards.

## Future Schema Extensions

Common production extensions include:

- Environments
- Resources
- Resource Groups
- Approval Workflows
- Notification History
- Audit Events
- User Groups
- Team Memberships
- Access Review Campaigns
- Data Quality Checks