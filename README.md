# AccessAtlas

AccessAtlas is a Streamlit-based reference application for centralized access governance, compliance tracking, permission cataloging, and access reconciliation.

It demonstrates how an organization can bring users, systems, permissions, administrator responsibilities, compliance records, and reconciliation workflows into one governance model without tying the design to a single technology platform or identity system.

The current application is intentionally a **reference implementation**. It uses synthetic CSV-backed data and Streamlit session state to demonstrate workflows, role-aware visibility, and a production-oriented data model. It is not a production identity, authentication, or authorization platform.

**Live demo:** [https://accessatlas.streamlit.app/](https://accessatlas.streamlit.app/)

> **Demo Mode simulates role-based visibility and workflow behavior. It is not an authentication or production authorization mechanism.**

---

## Business Case and Reference Application Evolution

AccessAtlas was developed around a common access-governance problem: organizations often manage access to applications, databases, cloud data platforms, dashboards, collaboration sites, and other controlled resources through separate processes and system-specific records.

That fragmentation makes several basic governance questions surprisingly difficult to answer consistently:

- Who currently has access?
- What system, resource, and permission does that access apply to?
- Who is responsible for administering the system?
- Is the user's required training or agreement documentation current?
- Does an external system export still match the organization's governance record?
- What changed, and what action should be taken?

The reference application evolved to demonstrate a centralized, platform-neutral model for those needs.

The current design:

- supports multiple system and resource types rather than a single technology pattern
- tracks user access separately from system administrator responsibility
- models resource-level access as **User → System → Resource → Permission**
- supports upload-based reconciliation when direct source-system integration is unavailable or inappropriate
- limits missing-record evaluation to the system being reconciled
- preserves historical context through inactive records instead of deletion
- separates reconciliation discrepancies from external approval processes
- provides role-aware experiences for Users, Managers, System Administrators, and Super Administrators
- supports self-service compliance date maintenance
- supports system-scoped administration and direct access add/edit workflows
- uses only synthetic users, systems, assignments, and reconciliation data in the public reference implementation

---

## What AccessAtlas Demonstrates

AccessAtlas is designed around five connected governance capabilities.

### 1. Centralized access inventory

The application maintains a common view of:

- users and identity-related governance attributes
- governed systems and resources
- user access assignments
- resource-level permissions
- system administrator assignments
- compliance dates and status

This allows the application to answer both user-centered and system-centered questions from the same underlying model.

### 2. Role-aware governance workflows

Demo Mode uses synthetic personas to show how the same governance data can support different operational responsibilities.

| Demo role | Visible sections | Demonstrated responsibility |
|---|---|---|
| User | My Access | Review own governance record and update personal certification/agreement dates |
| Manager | Dashboard, My Access, Manage Access, Access Reconciliation | Review own record, direct reports, associated systems, and scoped reconciliation information |
| System Administrator | Dashboard, My Access, Manage Access, Access Reconciliation | Review and manage users and access within administered-system scope |
| Super Administrator | All sections | Review the complete synthetic governance dataset and all demo workflows |

Unavailable sections are not rendered for the selected Demo Mode persona.

The application also scopes visible records. For example, System Administrators see only users and systems associated with systems they administer.

### 3. Compliance monitoring

The reference model tracks:

- annual training dates
- biennial training dates
- access agreement dates

The application derives expiration and compliance status from those records and surfaces:

- current records
- records expiring soon
- expired records
- active records requiring follow-up

The current demo uses a 30-day expiring-soon window, one-year validity for annual training, and two-year validity for biennial training.

### 4. Access reconciliation

AccessAtlas compares external access records with the current governance inventory and identifies differences that may require action.

The access reconciliation workflow can identify:

- access present in an uploaded export but missing from AccessAtlas
- active AccessAtlas records missing from the uploaded system export
- status differences between the two datasets

Recommended actions include:

- **Add access record**
- **Inactivate**
- **Update**

The demo applies selected actions only to the current Streamlit session.

### 5. Compliance-date reconciliation

A separate reconciliation workflow compares externally supplied training and agreement dates with current user records.

The workflow evaluates:

- annual training date
- biennial training date
- access agreement date

Differences are presented through the same review-and-apply pattern used for system access reconciliation.

---

## Application Tour

The interface is organized around work users need to perform rather than around database tables.

### Dashboard

The Dashboard provides a role-aware operational summary for the current visible scope.

It includes metrics and visual summaries for:

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

Its purpose is to help a reviewer quickly identify where attention may be needed before moving into a detailed workflow.

### My Access

My Access is the individual governance view.

#### My Record

Shows the selected synthetic user's:

- profile and organizational attributes
- compliance dates and status
- access assignments
- system administrator assignments

#### Update My Certification and Agreement Dates

Demonstrates self-service maintenance of the selected user's compliance dates.

Updates are written only to Streamlit session state. Source CSV files are not changed.

### Manage Access

Manage Access groups user review, system review, and direct access maintenance.

#### Managed Users

Provides a user-centered governance view with:

- User Management Registry
- filters by application role, user type, and record status
- manager lookup
- Selected User Access Profile
- access assignment metrics and details
- administrative assignment details
- training and agreement information
- a session-state-backed add-user workflow

Visible users are limited by the selected Demo Mode role and scope.

#### Managed Systems

Provides a system-centered governance view with:

- System Catalog
- filters by system type, category, and record status
- Selected System Access Profile
- system owner and administrative responsibility
- resource scope and access model
- users with access
- system administrators
- resource and permission details

The section also describes access-governance patterns that may be represented by:

- periodic application user exports
- application roles
- cloud data platform roles
- database, schema, or table permissions
- dashboard access
- hosting-site access
- collaboration-site or group membership

#### Edit / Add Access

Provides a direct single-record workflow for access assignments.

- Super Administrators can manage all visible systems.
- System Administrators can manage only systems they administer and users within that scope.
- Users and Managers do not receive direct access-maintenance controls.

Changes are stored only in the current Streamlit session.

### Access Reconciliation

Access Reconciliation contains two related review workflows.

#### System Access Export File Upload

This workflow compares an external system access export with the current AccessAtlas access inventory.

The process is:

1. Select the system being reconciled.
2. Upload an external access export.
3. Validate required columns and system scope.
4. Preview uploaded records.
5. Compare the export with current access assignments.
6. Review change summaries and the reconciliation queue.
7. Select recommended actions to apply.
8. Review session-state reconciliation results.

The current design reconciles **one system at a time**. This is deliberate: a record should be recommended for inactivation only when it is absent from a complete comparison set for the system being reviewed.

#### Training Certificate Date and Agreement Reconciliation

This workflow compares external user compliance dates with the current user registry.

It follows the same basic pattern:

1. Upload external compliance records.
2. Validate the schema.
3. Compare supplied dates with current user records.
4. Review differences.
5. Select updates to apply.
6. Review reconciliation results.

### AccessAtlas App Admin

This section is visible only to the Super Administrator Demo Mode role.

#### Compliance Monitoring

Provides organization-wide synthetic compliance review, including:

- current, expiring, and expired compliance counts
- active records requiring follow-up
- filters by compliance status, department, and user type
- compliance detail records
- follow-up records
- summary views by department and user type

#### System Administrator Assignments

Provides administrative coverage review, including:

- assignment metrics
- filters by administrator role, assignment status, system type, and system category
- administrator-centered review
- system-centered review
- administrative coverage by system

---

## Core Data Model

The reference implementation uses four primary governance entities.

### Users

Users represent people or identities that may require access to governed resources.

Examples may include:

- employees
- contractors
- vendors
- consultants
- service accounts

Representative fields include:

```text
user_id
display_name
first_name
last_name
email
application_role
manager_user_id
department
user_type
record_status
annual_training_date
biennial_training_date
access_agreement_date
created_date
updated_date
```

`application_role` controls the simulated AccessAtlas persona.

`user_type` describes the identity's relationship to the organization.

`record_status` indicates whether the governance record is active or inactive.

### Systems

Systems represent governed applications, databases, data platforms, dashboards, collaboration resources, and other controlled environments.

Representative fields include:

```text
system_id
system_name
system_type
system_category
resource_scope
access_model
tracking_method
system_owner
admin_group
record_status
```

### Access Assignments

Access assignments connect users to specific permissions within systems.

The conceptual relationship is:

```text
User
  └── System
       └── Resource
            └── Permission
```

Representative fields include:

```text
access_id
user_id
system_id
resource_type
resource_name
permission_name
access_status
granted_date
revoked_date
source
```

This structure allows the same access model to describe a platform role, database permission, dashboard assignment, site membership, or other resource-specific access relationship.

### System Administrator Assignments

System administrator assignments describe responsibility for administering a governed system.

The conceptual relationship is:

```text
User
  └── System
       └── Administrative Role
```

One user may administer multiple systems, and one system may have multiple administrators.

Access to a system and responsibility for administering that system are intentionally modeled as separate relationships.

---

## Reconciliation Models

### System access reconciliation key

Access records are compared using the composite key:

```text
user_id
system_id
resource_type
resource_name
permission_name
```

`access_status` is evaluated after matching records on that key.

The system access upload therefore requires:

```text
user_id
system_id
resource_type
resource_name
permission_name
access_status
```

The optional field:

```text
source_system_record_id
```

is recommended for traceability to the source export.

A sample file is provided in:

```text
data/sample_access_upload.csv
```

### Training and agreement reconciliation key

Compliance-date records are matched on:

```text
user_id
```

The external file must also contain:

```text
annual_training_date
biennial_training_date
access_agreement_date
```

---

## Reference Architecture

The current repository intentionally keeps the implementation simple:

```text
Streamlit UI
    │
    ├── Role-aware demo scoping
    ├── Governance review workflows
    ├── Reconciliation logic
    └── Session-state demo updates
             │
             ▼
      Synthetic CSV datasets
```

The active application is implemented in the root-level `app.py`.

The CSV files act as reference datasets. Streamlit session state provides temporary write behavior for demonstrations such as:

- self-service compliance updates
- adding a synthetic user
- direct access add/edit actions
- reconciliation action application

Refreshing or restarting the session resets those changes to the source data.

This is a deliberate reference-app boundary. Production persistence, authorization, transactions, and audit logging belong in the backend rather than being simulated in the UI.

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
│   ├── user-guides/
│   │   ├── access-reviewer-guide.md
│   │   ├── super-admin-guide.md
│   │   └── system-admin-guide.md
│   └── UI_STYLE_GUIDE.md
├── tests/
│   └── test_reconcile.py
├── .gitignore
├── app.py
├── CHANGELOG.md
├── LICENSE
├── POSTGRES_NOTES.md
├── README.md
├── requirements.txt
└── SNOWFLAKE_NOTES.md
```

The `archive/` directory retains an earlier implementation for historical reference. The current application is the root-level `app.py`.

---

## Technology Stack

The current reference implementation uses:

- Python
- Streamlit
- Pandas
- synthetic CSV datasets
- Pytest
- GitHub Actions

The application is platform-neutral at the governance-model level. A production implementation could use a backend or integrations such as:

- Snowflake
- PostgreSQL
- SQL Server
- Oracle
- Databricks
- REST APIs
- identity management platforms
- notification services

---

## Run AccessAtlas Locally

### 1. Clone the repository

```bash
git clone https://github.com/katieravenwood/AccessAtlas.git
cd AccessAtlas
```

### 2. Create and activate a virtual environment

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the app

```bash
streamlit run app.py
```

### 5. Run tests

```bash
pytest
```

---

## Demo Data and Safety

All data in this repository is synthetic.

The repository contains no:

- production user records
- proprietary organizational data
- credentials
- production system details
- production access exports

The sample records are designed to demonstrate varied governance scenarios, including:

- different application roles
- different user types
- active and inactive records
- current and expired compliance
- different system categories
- resource-level permissions
- multiple administrators
- reconciliation add, update, and inactivation cases

Do not treat Demo Mode as a security boundary.

---

## Production Implementation Considerations

A production deployment should replace the reference application's demo mechanisms with approved enterprise controls.

Typical production requirements include:

- Single Sign-On
- enterprise identity-provider integration
- backend role and scope authorization
- database-backed persistence
- transaction management
- immutable or controlled audit logging
- approval workflows
- notification services
- automated or API-based reconciliation
- row-, object-, or resource-level security where appropriate
- secure secrets management
- monitoring and observability
- backup and recovery
- operational support and data-retention policies

A particularly important architectural principle is that **hidden UI controls are not authorization**. The current app hides and scopes screens to demonstrate intended personas, but a production implementation must enforce the same rules in its backend and data-access layer.

---

## Database Migration Paths

### Snowflake

`SNOWFLAKE_NOTES.md` describes a Snowflake-backed implementation path.

The core reference datasets map naturally to governance tables for:

- users
- systems
- access assignments
- system administrator assignments
- reconciliation inputs

A Snowflake implementation should add approved persistence, authorization, auditing, and transaction patterns rather than copying the demo's session-state behavior.

### PostgreSQL

`POSTGRES_NOTES.md` provides PostgreSQL-oriented guidance for:

- table design
- indexes
- write-back patterns
- transactions
- authorization considerations

The current UI and governance workflows are intended to remain largely independent of the chosen production database.

---

## Design Principles

AccessAtlas follows five design principles.

**Centralized governance**  
Maintain one place to understand users, systems, permissions, administrative responsibility, and compliance posture.

**Platform neutrality**  
Represent access to applications, databases, data platforms, dashboards, collaboration resources, and future system types through a common model.

**Auditability**  
Preserve inactive records and historical access context instead of deleting governance history.

**Transparency**  
Make access relationships, administrator responsibility, compliance status, and reconciliation differences easy to inspect.

**Extensibility**  
Keep the reference implementation understandable while providing a model that can move to enterprise persistence and integration patterns.

---

## Documentation

Additional documentation is available in the repository:

- `CHANGELOG.md` — development history and unreleased changes
- `docs/UI_STYLE_GUIDE.md` — current interface vocabulary and presentation conventions
- `docs/architecture/governance_patterns.md` — governance architecture patterns
- `docs/user-guides/access-reviewer-guide.md` — access review guidance
- `docs/user-guides/system-admin-guide.md` — System Administrator guidance
- `docs/user-guides/super-admin-guide.md` — Super Administrator guidance
- `SNOWFLAKE_NOTES.md` — Snowflake implementation path
- `POSTGRES_NOTES.md` — PostgreSQL implementation path

---

## Current Status and Future Direction

AccessAtlas is currently a functional reference application and public demo, not a production access-management service.

The present implementation demonstrates the core governance model and primary workflows. Future work may include:

- production authentication and authorization
- persistent audit-event logging
- approval workflows
- formal access review campaigns
- notification history and delivery workflows
- user group and team membership management
- automated source-system ingestion
- Snowflake-native role metadata ingestion
- API-based access synchronization
- expanded automated test coverage
- production observability and deployment patterns

See `CHANGELOG.md` for development history.

---

## License

AccessAtlas is licensed under the MIT License. See `LICENSE`.
