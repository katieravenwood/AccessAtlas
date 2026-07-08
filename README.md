# AccessAtlas

AccessAtlas is a Streamlit-based reference implementation for centralized access governance, compliance tracking, permission cataloging, and access reconciliation.

It demonstrates how organizations can maintain a single inventory of users, systems, permissions, administrator assignments, compliance records, and access review data across applications, databases, cloud platforms, dashboards, and collaboration environments.

The project uses synthetic sample data and generic system examples so it can be adapted to different industries, organizations, and technology stacks.

## Demo Deployment

The demo application is available in Streamlit:

[https://accessatlas.streamlit.app/](https://accessatlas.streamlit.app/)

> Demo Mode simulates role-based visibility and workflow behavior. It is not an authentication or production authorization mechanism.

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
- Training date and agreement reconciliation
- Direct single-record access add/edit workflows
- Audit-friendly inactive record handling
- Role-aware governance summaries
- Scoped access review workflows

---

## Demo Roles and Visible Sections

Demo Mode scopes visible records and top-level application sections based on the selected synthetic user's role.

| Demo Role | Visible Sections | Demonstrated Scope |
| --- | --- | --- |
| User | My Access | Own profile, access, administrative assignments, and self-service certification/agreement date updates |
| Manager | Dashboard, My Access, Manage Access, Access Reconciliation | Own record, visible review scope, associated systems/access, and reconciliation review |
| System Administrator | Dashboard, My Access, Manage Access, Access Reconciliation | Users and systems within administered-system scope; scoped direct access management |
| Super Administrator | Dashboard, My Access, Manage Access, Access Reconciliation, AccessAtlas App Admin | Full synthetic dataset and all demo workflows |

Unavailable sections are not rendered in the application selector.

This behavior demonstrates intended persona-based visibility. Production deployments should enforce access control through real authentication, backend authorization, and database-level security.

---

## Application Structure

AccessAtlas uses task-based top-level navigation.

### Dashboard

Provides role-aware summary metrics and visual detail for the records visible to the selected demo role, including:

- visible users
- visible systems
- access records
- items needing review
- expired or expiring compliance
- pending reconciliation actions
- active compliance follow-up
- compliance status
- user record status
- access records by system type
- access records by resource type
- access records by access status

### My Access

Provides the selected synthetic user's individual governance record.

The section contains:

- **My Record** — profile, compliance dates, access assignments, and administrative assignments
- **Update My Certification and Agreement Dates** — simulated self-service date updates

Self-service changes are stored only in Streamlit session state and do not modify source CSV files.

### Manage Access

Provides scoped user, system, and direct access-management workflows.

#### Managed Users

Includes:

- User Management Registry
- role, user type, and record status filters
- Selected User Access Profile
- manager lookup
- access assignment details
- administrative assignment details
- training and agreement information

System Administrator and Manager demo roles receive scoped user views.

#### Managed Systems

Includes:

- System Catalog
- system type, category, and status filters
- Selected System Access Profile
- system ownership and administrative responsibility
- users with access
- system administrators
- resource and permission details

Managed Systems also explains common governance patterns such as periodic user exports, application roles, data-platform roles, database/schema/table permissions, dashboard access, hosting-site access, and collaboration-site membership.

#### Edit / Add Access

Provides a direct single-record add/edit workflow for access assignments.

- Super Administrators can manage all visible systems.
- System Administrators can manage only systems and users within their administered-system scope.
- Manager and User demo roles cannot perform direct add/edit actions.

Changes are stored only in Streamlit session state.

### Access Reconciliation

Provides two reconciliation workflows.

#### System Access Export File Upload

Demonstrates comparison of a single-system access export against current access assignments.

The workflow includes:

- expected upload schema
- upload validation
- single-system reconciliation scope
- uploaded export preview
- change summaries
- filterable reconciliation queue
- recommended actions
- selectable apply behavior
- source record traceability
- reconciliation results

Supported demo actions include:

- **Add access record**
- **Inactivate**
- **Update**

Inactivation preserves historical governance context rather than deleting access records.

#### Training Certificate Date and Agreement Reconciliation

Demonstrates comparison of external compliance-date records against current user records for:

- annual training date
- biennial training date
- access agreement date

The workflow mirrors the queue-and-apply pattern used for system access reconciliation.

### AccessAtlas App Admin

Available only to the Super Administrator demo role.

#### Compliance Monitoring

Provides:

- current, expiring, and expired compliance counts
- active records requiring follow-up
- compliance detail filters
- follow-up records
- summaries by department and user type

#### System Administrator Assignments

Provides:

- administrator assignment metrics
- filters by admin role, assignment status, system type, and system category
- administrator-centered review
- system-centered review
- administrative coverage by system

---

## Core Data Model

The reference implementation is built around four primary governance entities plus external reconciliation inputs.

### User Records

Individuals, contractors, vendors, consultants, service accounts, or other identities requiring access to managed resources.

Representative attributes include:

- `user_id`
- `display_name`
- `email`
- `application_role`
- `manager_user_id`
- `department`
- `user_type`
- `record_status`
- training and agreement dates

`user_type` describes the user's relationship to the organization.

`record_status` describes whether the user record is active for governance purposes.

### System Records

Applications, databases, cloud platforms, dashboards, collaboration sites, and other governed resources.

Representative attributes include:

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
User -> System -> Resource -> Permission
```

Representative attributes include:

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
User -> System -> Administrative Role
```

One user may administer multiple systems, and one system may have multiple administrators.

### Reconciliation Inputs

External access or compliance exports are compared with current session-state-backed governance records.

The recommended access reconciliation key is:

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
├── .github/
│   └── workflows/
│       └── ci.yml
├── archive/
│   └── data_model_tabbed_single_0_4_12/
├── data/
│   ├── access_assignments.csv
│   ├── sample_access_upload.csv
│   ├── system_admin_assignments.csv
│   ├── systems.csv
│   └── users.csv
├── docs/
│   ├── architecture/
│   │   └── governance_patterns.md
│   └── user-guides/
│       ├── access-reviewer-guide.md
│       ├── super-admin-guide.md
│       └── system-admin-guide.md
├── tests/
│   └── test_reconcile.py
├── .gitignore
├── app.py
├── LICENSE
├── POSTGRES_NOTES.md
├── README.md
├── requirements.txt
└── SNOWFLAKE_NOTES.md
```

The archive contains earlier implementation material retained for historical reference. The current reference application is the root-level `app.py`.

---

## Tech Stack

Included in the reference implementation:

- Streamlit
- Python
- Pandas
- CSV-backed synthetic sample data
- Pytest smoke testing
- GitHub Actions CI

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

Run the current reconciliation smoke test:

```bash
pytest
```

---

## Sample Data

All sample data included in this repository is synthetic.

No proprietary information, organizational data, user records, credentials, or production system details are included.

The sample data is intentionally generic and demonstrates access-governance patterns across multiple system and resource types.

---

## System Access Reconciliation Upload Schema

The sample access upload file uses the following structure:

```text
source_system_record_id
user_id
system_id
resource_type
resource_name
permission_name
access_status
```

Required fields are:

```text
user_id
system_id
resource_type
resource_name
permission_name
access_status
```

`source_system_record_id` is optional but recommended because it preserves traceability to the source export.

The current demo reconciles one system at a time so missing-record evaluation is limited to the selected system scope.

---

## Production Deployment Considerations

A production implementation would typically include:

- Single Sign-On (SSO)
- Active Directory or identity-provider integration
- database-backed storage
- backend authorization
- row- or object-level security where appropriate
- audit logging
- notification services
- approval workflows
- automated reconciliation
- monitoring and observability
- backup and recovery
- secure secrets management

The reference implementation intentionally separates governance concepts from any single production platform.

---

## Snowflake Migration Path

`SNOWFLAKE_NOTES.md` describes a Snowflake-backed implementation path.

The CSV data files map naturally to database tables for users, systems, access assignments, system administrator assignments, and reconciliation inputs.

A production migration should replace session-state/CSV behavior with approved persistence, authorization, transaction, and audit controls.

## PostgreSQL Migration Path

`POSTGRES_NOTES.md` provides PostgreSQL-oriented table definitions, indexing recommendations, write-back patterns, transaction guidance, and production authorization considerations.

---

## Documentation

Additional documentation is available under `docs/`:

- `docs/architecture/governance_patterns.md`
- `docs/user-guides/access-reviewer-guide.md`
- `docs/user-guides/super-admin-guide.md`
- `docs/user-guides/system-admin-guide.md`

The current interface vocabulary and layout conventions are documented in `docs/UI_STYLE_GUIDE.md`.

---

## Future Direction

Potential future work includes:

- production authentication and authorization
- persistent audit event logging
- approval workflows
- access review campaigns
- notification history
- user group and team membership management
- automated source-system ingestion
- Snowflake-native role metadata ingestion
- API-based access synchronization
- expanded automated test coverage
- production observability and deployment patterns

AccessAtlas is intended as a foundation that organizations can extend to fit their own governance, compliance, and operational requirements.

---

## License

MIT License. See `LICENSE`.
