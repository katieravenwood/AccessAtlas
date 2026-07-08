# AccessAtlas

AccessAtlas is a Streamlit-based reference implementation for centralized access governance, compliance tracking, permission cataloging, and access reconciliation.

It demonstrates how organizations can maintain a single inventory of users, systems, permissions, administrator assignments, compliance records, and access review data across applications, databases, cloud platforms, dashboards, and collaboration environments.

The project uses synthetic sample data and generic system examples so it can be adapted to different industries, organizations, and technology stacks.

## Demo Deployment

The demo version of the app can be accessed here: [AccessAtlas In Streamlit](https://accessatlas.streamlit.app/)

---

## Design Principles

AccessAtlas is built around five core principles:

1. **Centralized governance** — maintain one place to understand users, systems, permissions, and compliance posture.
2. **Platform neutrality** — support applications, databases, dashboards, cloud platforms, sites, folders, and future system types.
3. **Auditability** — preserve inactive records and historical access context rather than deleting governance history.
4. **Transparency** — make access relationships, administrative responsibility, and compliance status easy to inspect.
5. **Extensibility** — keep the reference implementation simple while allowing migration to enterprise backends and workflows.

---

## What This Project Demonstrates

AccessAtlas demonstrates practical patterns for:

- Central user registry management
- Cross-system access cataloging
- Resource-level permission tracking
- System administrator assignment tracking
- Training and agreement compliance monitoring
- Upload-based access reconciliation
- Audit-friendly inactive record handling
- Governance reporting summaries

---

## Simulated Role-Based Data Scoping

Demo Mode scopes visible records based on the selected synthetic user's role.

- **User** accounts see only the Users tab, beginning with their own selected governance profile; the broader registry/filter section and Overview tab are hidden.
- **Manager** accounts see their own record, direct reports, and systems/access records associated with that group.
- **System Administrator** accounts can view the Users tab, but it is scoped to users with access to systems they administer. They can also view only information about systems they administer.
- **Super Administrator** accounts see all synthetic records.

This feature is for demonstration only. Production deployments should enforce access control through real authentication, backend authorization, and database-level security.

---

## Dynamic Role-Based Tabs

AccessAtlas only renders tabs available to the selected Demo Mode role.

Unavailable sections are not shown in the tab bar. This keeps the demo interface closer to the intended user experience for each persona:

- User: My Record self-service tab only
- Manager: review-oriented views
- System Administrator: administered-system views plus scoped Users tab
- Super Administrator: full application

This is still simulated UI behavior only; production applications should enforce authorization on the backend as well as in the interface.

---

## Self-Service Date Updates

The **My Record** tab includes a simulated self-service form that allows the selected demo user to update their own training and agreement completion dates.

The app recalculates expiration dates based on the configured validity periods:

- annual training: 1 year
- biennial training: 2 years

These updates are stored only in Streamlit session state for demonstration purposes. They do not modify the source CSV files. In a production implementation, this workflow would write to an approved database table and may require review, approval, document upload, or audit logging.

---

## System Administrator Users Tab Scope

System Administrator demo accounts can access the **Users** tab, but the table and selected user access profile options are filtered to users who have access to systems administered by that System Administrator.

This allows System Administrators to review relevant users without exposing the full user registry.

---

## Contextual Sidebar Guidance and Tab Selection Considerations

The Overview, Compliance, and Access Reconciliation explanatory sections are displayed in the Demo Mode sidebar when the corresponding section is selected.

Because native Streamlit tabs do not expose the active tab to Python, this version uses a role-aware horizontal section selector instead of `st.tabs()`. This keeps unavailable sections hidden and allows sidebar guidance to update based on the selected section. In non-demo implementations, use of `st.tabs()` would likely be a more standard implementation.

---

## Reconciliation Queue Updates

The System Access Export File Upload section includes a selectable Reconciliation Queue.

Super Administrator and System Administrator demo users can select reconciliation exceptions and apply recommended actions to the session-state-backed access assignment table.

Supported actions include:

- **Add** records for access found in an uploaded export but missing from AccessAtlas
- **Inactivate** records for access retained in AccessAtlas but missing from the uploaded export
- **Update** records when access status differs between AccessAtlas and the uploaded export

These actions update only the in-session demo dataset. They do not modify the source CSV files. In production, this workflow would write to an approved database table and should include authorization checks, audit logging, and approval controls.

---

## Direct User Access Management

The **User Access Management** section allows Super Administrator and System Administrator demo users to add or edit a single access assignment without uploading a reconciliation file.

Role scope is enforced in the demo interface:

- Super Administrators can manage access assignments for all systems.
- System Administrators can manage access assignments only for systems they administer and users visible within that administered-system scope.

Changes are written to the session-state-backed access assignment table and do not modify the source CSV files.

---

## Streamlined Task-Based Interface

AccessAtlas now organizes the demo around day-to-day workflows rather than database entities.

Primary sections are:

- **Dashboard** — role-aware summary and key indicators
- **My Access** — individual user profile, compliance dates, and access assignments
- **Manage Access** — user and system review workflows, with manual single-record add/edit where permitted
- **Access Reconciliation** — reconciliation workflow and reconciliation queue
- **AccessAtlas App Admin** — compliance monitoring and system administrator coverage for Super Administrators

Detailed tables are available, but many are grouped under expanders so the main interface stays focused.

---

## Application Tabs

The application includes a dedicated **My Record** tab for individual self-service access review. The broader **Users** tab remains available only to roles that need registry or review functionality.

The application is organized into role-aware tabs.

### Overview

Provides a dashboard-style summary of the governance dataset, including:

- total users
- tracked systems
- access records
- system administrator assignments
- expired or expiring compliance records
- user record status summaries
- compliance status summaries
- access records by system type, resource type, and access status

### My Record

Provides an individual self-service view of the selected user's governance record, including profile information, compliance dates, access assignments, and administrative assignments.

### Manage Access

The Manage Access tab provides collapsible user and system review sections which are filtered by the scope of the current user's administrative assignments.

#### Users In Scope

Provides a user-centered governance profile including:

- user registry filters
- selected user access profile
- manager lookup
- access assignment metrics
- administrative assignment metrics
- training and agreement snapshot
- access by system
- detailed access records
- systems administered by the selected user

#### Systems In Scope

Provides a system-centered governance profile including:

- system catalog filters
- selected system access details
- system owner and administrative group
- resource scope and access model
- users with access
- system administrators
- resources and permissions assigned within the system

#### User Access Management

Provides a direct single-record add/edit workflow for user access assignments. This section is available to Super Administrator and System Administrator demo roles.

### Access Reconciliation Tab

#### Access Reconciliation

Demonstrates upload-based reconciliation of external access exports against current access assignment records, including:

- expected upload schema
- upload validation
- reconciliation scope selection
- uploaded export preview
- summary by change type
- summary by resource type
- reconciliation queue
- source record traceability
- audit-friendly inactive status recommendations

### AccessAtlas App Admin Tab

Allows Super Admins users to review Compliance monitorinig metrics and details and manage system administrator roles.

#### Compliance

Provides compliance monitoring and follow-up reporting, including:

- current, expiring, and expired compliance counts
- active records requiring follow-up
- filters by compliance status, department, and user type
- follow-up queue
- compliance summaries by department and user type

#### System Admins

Shows administrative responsibility across systems, including:

- administrator assignment metrics
- filters by admin role, status, system type, and system category
- administrator-centered view
- system-centered view
- admin coverage by system

### Access Reconciliation

Allows administrators to Upload or review access list exports from other systems, inspect differences, and apply recommended session-state updates from the reconciliation Reconciliation Queue.

#### Access Reconciliation Section

Demonstrates upload-based reconciliation of external access exports against current access assignment records, including:

- expected upload schema
- upload validation
- reconciliation scope selection
- uploaded export preview
- summary by change type
- summary by resource type
- reconciliation queue
- source record traceability
- audit-friendly inactive status recommendations

---

## Core Data Model

The AccessAtlas reference implementation is built around five primary entities.

### User Records

Individuals, contractors, vendors, consultants, service accounts, or other identities requiring access to managed resources.

Key attributes include:

- `user_id`
- `display_name`
- `email`
- `application_role`
- `manager_user_id`
- `department`
- `user_type`
- `record_status`
- training and agreement dates

`user_type` describes the user's relationship to the organization, such as Employee, Contractor, Vendor, Consultant, or Service Account.

`record_status` describes whether the user record is active for governance purposes.

### Systems Records

Applications, databases, cloud platforms, dashboards, collaboration sites, and other governed resources.

Key attributes include:

- `system_id`
- `system_name`
- `system_type`
- `system_category`
- `resource_scope`
- `access_model`
- `tracking_method`
- `system_owner`
- `admin_group`
- `record_status`

### Access Assignments

Relationships between users and systems that define access permissions to specific resources.

The model supports:

```text
User → System → Resource → Permission
```

Key attributes include:

- `user_id`
- `system_id`
- `resource_type`
- `resource_name`
- `permission_name`
- `access_status`
- `granted_date`
- `revoked_date`
- `source`

### System Administrator Assignments

Relationships between users and systems that define administrative responsibility.

The model supports:

```text
User → System → Administrative Role
```

This allows one user to administer multiple systems and one system to have multiple administrators.

### Access Reconciliation Uploads

Authoritative access exports used to compare current access records against external systems.

Uploads may represent:

- application access
- role-based platform access
- database permissions
- dashboard access
- site membership
- other governed resources

The recommended reconciliation key is:

```text
user_id
system_id
resource_type
resource_name
permission_name
```

---

## Repository Structure

```text
/
├── app.py
├── README.md
├── requirements.txt
├── SNOWFLAKE_NOTES.md
└── data/
    ├── users.csv
    ├── systems.csv
    ├── access_assignments.csv
    ├── system_admin_assignments.csv
    └── sample_access_upload.csv
```

---

## Tech Stack

Included in this reference implementation:

- Streamlit
- Python
- Pandas
- CSV data sources

Common production backends or integrations may include:

- Snowflake
- PostgreSQL
- SQL Server
- Oracle
- Databricks
- REST APIs
- identity management platforms
- notification services

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```

---

## Sample Data

All sample data included in this repository is synthetic.

No proprietary information, organizational data, user records, credentials, or production system details are included.

The sample data is intentionally generic and demonstrates access governance patterns across multiple system and resource types.

---

## Access Reconciliation Upload Schema

The sample upload file uses the following structure:

```text
source_system_record_id
user_id
system_id
resource_type
resource_name
permission_name
access_status
```

Required fields for reconciliation are:

```text
user_id
system_id
resource_type
resource_name
permission_name
access_status
```

The `source_system_record_id` field is optional but recommended because it preserves traceability back to the source export.

---

## Production Deployment Considerations

A production implementation would typically include:

- Single Sign-On (SSO)
- Active Directory or identity provider integration
- Database-backed storage
- Audit logging
- Notification services
- Role-based administration
- Approval workflows
- Automated reconciliation processes
- Monitoring and observability
- Backup and recovery processes
- Secure secrets management

The architecture is intentionally designed so the CSV-based data layer can be replaced with enterprise databases or identity platforms with limited changes to the application layer.

---

## Snowflake Migration Path

The included `SNOWFLAKE_NOTES.md` document demonstrates how the same architecture can be migrated from CSV-backed storage to a Snowflake-backed implementation.

The CSV files map naturally to Snowflake tables:

```text
users.csv → ACCESSATLAS.USERS
systems.csv → ACCESSATLAS.SYSTEMS
access_assignments.csv → ACCESSATLAS.ACCESS_ASSIGNMENTS
system_admin_assignments.csv → ACCESSATLAS.SYSTEM_ADMIN_ASSIGNMENTS
sample_access_upload.csv → ACCESSATLAS.ACCESS_RECONCILIATION_UPLOADS
```

Only the data access layer needs to change; the user interface and governance workflows remain largely unchanged.

## PostgreSQL Migration Path

The included `POSTGRES_NOTES.md` document provides PostgreSQL table definitions, indexing recommendations, write-back examples, transaction guidance, and production authorization considerations.

---

## Future Enhancements

Potential enhancements include:

- resource and environment dimension tables
- notification history
- approval workflows
- access review campaigns
- audit event logging
- user group management
- team membership management
- Snowflake-native role metadata ingestion
- API-based access synchronization
- dashboard visualizations
- test suite and CI workflow

AccessAtlas is intended as a foundation that organizations can extend to fit their own governance, compliance, and operational requirements.
