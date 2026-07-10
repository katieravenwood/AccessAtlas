# AccessAtlas

AccessAtlas is a Streamlit-based reference application for centralized access governance, compliance tracking, permission cataloging, and access reconciliation.

It demonstrates how an organization can bring users, systems, permissions, administrator responsibilities, compliance records, and reconciliation workflows into one governance model without tying the design to a single technology platform or identity system.

AccessAtlas is published in two forms from one canonical modular codebase:

- a **single-file quick-start starter** for organizations that want to inspect, edit, and run the application with minimal application-architecture overhead; and
- a **modular implementation** for teams extending authentication, persistence, notifications, audit workflows, provisioning, or automated tests.

A separate hosted demo runtime preserves the synthetic role-preview experience. All reference data is synthetic, and demo changes remain session-backed rather than persistent.

**Live demo:** [https://accessatlas-demo.streamlit.app/](https://accessatlas-demo.streamlit.app/)

> **The hosted Demo Mode simulates role-based visibility and workflow behavior. It is not authentication or a production authorization mechanism.**

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
- append-oriented governance audit events

This allows the application to answer both user-centered and system-centered questions from the same underlying model.

### 2. Role-aware governance workflows

The hosted demo uses synthetic personas to show how the same governance data can support different operational responsibilities. The starter runtimes use the same role and scope rules without rendering the demo persona selector.

| Demo role | Visible sections | Demonstrated responsibility |
| --- | --- | --- |
| User | My Access | Review own governance record and update personal certification/agreement dates |
| Manager | Dashboard, My Access, Manage Access, Access Reconciliation | Review own record, direct reports, associated systems, and scoped reconciliation information |
| System Administrator | Dashboard, My Access, Manage Access, Access Reconciliation | Review and manage users and access within administered-system scope |
| Super Administrator | All sections | Review the complete synthetic governance dataset and all demo workflows |

Unavailable sections are not rendered for the current application role.

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

The reference implementation applies selected actions only to the current Streamlit session.

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

Shows the current user's:

- profile and organizational attributes
- compliance dates and status
- access assignments
- system administrator assignments

#### Update My Certification and Agreement Dates

Demonstrates self-service maintenance of the current user's compliance dates.

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

Visible users are limited by the current application role and resolved scope.

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

This section is visible only to the Super Administrator application role.

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

`application_role` drives the current reference role and scope model. In the hosted demo, it also controls the synthetic persona preview.

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

### System Administrator Roles

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

## Code Quality Checks

AccessAtlas uses Ruff as the shared linting and formatting baseline for canonical source, tests, and build tooling.

Install development dependencies with:

```bash
pip install -r requirements-dev.txt
```

Run the formatter:

```bash
ruff format modular tests tools
```

Run lint checks:

```bash
ruff check modular tests tools
```

Verify formatting without changing files:

```bash
ruff format --check modular tests tools
```

The generated root `app.py` is intentionally excluded from direct Ruff formatting and linting. It is rebuilt from the canonical modular source and protected by the single-file synchronization check.

The CI quality job runs, in order:

1. Ruff format check
2. Ruff lint check
3. generated single-file synchronization check
4. pytest

Run the full local validation sequence with:

```bash
ruff format --check modular tests tools
ruff check modular tests tools
python tools/build_single_file.py --check
pytest -q
```

---

## Automated Test Coverage

The AccessAtlas test suite now covers the principal non-UI business rules and distribution contracts.

Current coverage includes:

- compliance status, expiration, follow-up, and date normalization rules
- role-based user, system, access, and administrator assignment scope
- navigation label and visibility helpers
- starter identity configuration and fallback behavior
- session-backed user and access state helpers
- identifier generation and access-key matching
- access reconciliation comparison and action edge cases
- training and agreement reconciliation outcomes
- governance audit-event creation and storage contracts
- CSV export preparation and spreadsheet safeguards
- structured application logging configuration
- starter/demo runtime separation
- generated single-file synchronization and Python compilation

The suite intentionally emphasizes deterministic business logic and architectural contracts. The Streamlit UI remains a thin workflow layer around these tested functions.

Run the full suite with:

```bash
pytest -q
```

---

## Data Exports

AccessAtlas provides scoped CSV downloads from the workflow where each dataset is reviewed.

Available exports include:

- filtered users
- filtered systems
- scoped access assignments
- system administrator assignments
- filtered compliance detail
- compliance follow-up records
- system access reconciliation results
- training and agreement reconciliation results
- filtered governance audit history

Exports use the current role and record scope. A System Administrator therefore exports only records available within that administrator's application scope; the export helper does not bypass the shared scope model.

CSV is the baseline export format for portability.

The export preparation module is:

```text
modular/accessatlas/exports.py
```

It provides:

- stable column selection
- stable sorting when requested
- UTF-8 CSV output with a byte-order mark for spreadsheet compatibility
- no dataframe index column
- filesystem-friendly export filenames
- protection against formula-style CSV cell execution for text values beginning with `=`, `+`, `-`, or `@`

Successful downloads generate:

- an operational `data_export_downloaded` application log event; and
- a governance `data_export / export_dataset` audit event containing the export name, record count, column count, and filename.

The exported governance records themselves are not copied into the application log or export audit event.

---

## Governance Audit History

AccessAtlas maintains a separate governance audit-event model for meaningful record actions.

Application logs and governance audit events serve different purposes:

```text
Application logs
    └── How is the software behaving?

Governance audit events
    └── What governance action happened to a record?
```

The reference implementation records events for:

- user record creation
- self-service compliance date updates
- training and agreement reconciliation updates
- user inactivation through compliance reconciliation
- direct access assignment creation or update
- system access reconciliation additions, updates, and inactivations

Audit events include:

```text
audit_event_id
occurred_at
event_type
action
actor_user_id
actor_role
runtime
entity_type
entity_id
target_user_id
system_id
outcome
source
summary
changes_json
```

The modular contract is defined in:

```text
modular/accessatlas/audit.py
```

The default `SessionAuditStore` is append-oriented and uses Streamlit session state. This keeps the hosted demo disposable and avoids persistent public test data.

Super Administrators can review current-session events in:

```text
AccessAtlas App Admin
    └── Governance Audit History
```

The UI provides event counts, filters, a chronological event table, and event-level change detail.

The reference audit store is not intended as a production immutable audit repository. Production implementations should replace it with controlled persistent storage appropriate to the organization's retention, security, and evidence requirements.

---

## Application Architecture and Distribution Model

AccessAtlas uses one shared modular application core with separate starter and demo runtimes.

```text
                         modular/accessatlas/app_core.py
                                      |
                         shared UI and workflows
                                      |
                   +------------------+------------------+
                   |                                     |
                   v                                     v
      build_starter_runtime()                build_demo_runtime()
                   |                                     |
                   v                                     v
          modular/app.py                       modular/demo_app.py
                   |                                     |
                   | clean modular starter                | hosted demo
                   v                                     v
      tools/build_single_file.py              role-preview deployment
                   |
                   v
              root app.py
```

### Quick-start single-file starter

The root-level `app.py` is a generated, self-contained Streamlit application intended for rapid evaluation and direct customization.

```bash
streamlit run app.py
```

This is the recommended starting point for small and mid-sized organizations that want a readable one-file application without first learning the modular package structure.

The root `app.py` is a published distribution, not the canonical engineering source. Shared application changes should be made under `modular/` and then republished with the build script.

### Clean modular starter

The canonical engineering source is under:

```text
modular/
```

Run the modular starter with:

```bash
streamlit run modular/app.py
```

The modular version separates the shared application core from configuration, compliance logic, data loading, scope rules, temporary state, presentation helpers, reconciliation behavior, and runtime identity resolution.

The starter runtime does not include:

- a Demo Mode persona selector
- demo-specific sidebar warnings
- the Current Demo User panel
- the Visible Demo Scope panel
- demo-only contextual sidebar guidance

Until a pluggable authentication module is added, the starter can resolve its current application identity from:

```text
ACCESSATLAS_USER_ID
```

For example:

```bash
ACCESSATLAS_USER_ID=USR-0001 streamlit run app.py
```

This is a development and configuration placeholder, not authentication. Production implementations must replace it with an approved identity mechanism and enforce equivalent authorization in the backend and data-access layer.

### Hosted demo

The public preview uses the demo runtime:

```bash
streamlit run modular/demo_app.py
```

The demo retains the synthetic persona selector, current-user summary, visible-scope summary, contextual guidance, and role-aware preview experience.

Tester changes use Streamlit session state and reset with the session. The demo therefore remains inexpensive to host and does not require a persistent public backend.

### One application core, two runtimes

`modular/accessatlas/app_core.py` owns the shared AccessAtlas interface and workflows.

The starter and demo entry points supply different runtime factories:

```python
run_app(build_starter_runtime)
```

```python
run_app(build_demo_runtime)
```

The runtime resolves the current identity, visible sections, scoped records, and optional runtime-specific guidance. The application core does not own demo persona selection.

This keeps the starter and demo from becoming separate implementations.

### Publishing the quick-start application

Build the root single-file starter from the canonical modular source:

```bash
python tools/build_single_file.py
```

Verify that the committed quick-start distribution is synchronized:

```bash
python tools/build_single_file.py --check
```

CI runs the synchronization check before the test suite.

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
│   ├── MODULAR_ARCHITECTURE.md
│   └── UI_STYLE_GUIDE.md
├── modular/
│   ├── accessatlas/
│   │   ├── app_core.py
│   │   ├── compliance.py
│   │   ├── config.py
│   │   ├── data.py
│   │   ├── demo_runtime.py
│   │   ├── navigation.py
│   │   ├── presentation.py
│   │   ├── reconciliation.py
│   │   ├── runtime.py
│   │   ├── scope.py
│   │   ├── starter_runtime.py
│   │   └── state.py
│   ├── app.py
│   └── demo_app.py
├── tests/
│   ├── test_reconcile.py
│   ├── test_runtime_separation.py
│   └── test_single_file_build.py
├── tools/
│   └── build_single_file.py
├── .gitignore
├── app.py
├── CHANGELOG.md
├── LICENSE
├── POSTGRES_NOTES.md
├── README.md
├── requirements.txt
├── ROADMAP.md
└── SNOWFLAKE_NOTES.md
```

The root `app.py` is the generated quick-start distribution.

The canonical application source is under `modular/`. The hosted demo uses `modular/demo_app.py`.

The `archive/` directory retains an earlier implementation for historical reference.

---

## Technology Stack

The current reference implementation uses:

- Python
- Streamlit
- Pandas
- synthetic CSV datasets
- Pytest
- GitHub Actions
- Python standard-library structured logging

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

### 4. Choose a run path

#### Run the quick-start single-file starter

```bash
streamlit run app.py
```

#### Run the modular app version

```bash
streamlit run modular/app.py
```

#### Run the demo version

```bash
streamlit run modular/demo_app.py
```

The demo runtime retains the synthetic role selector and demo sidebar. The starter runtimes do not.

### 5. Optionally select a starter identity

The starter currently supports a development identity placeholder through `ACCESSATLAS_USER_ID`.

macOS or Linux:

```bash
ACCESSATLAS_USER_ID=USR-0001 streamlit run app.py
```

Windows PowerShell:

```powershell
$env:ACCESSATLAS_USER_ID = "USR-0001"
streamlit run app.py
```

When the variable is not set, the reference dataset falls back to the first active Super Administrator, then the first active user.

This behavior is intended only to keep the starter immediately runnable. It is not authentication.

### 6. Run tests

```bash
pytest
```

### 7. Rebuild the quick-start distribution after modular changes

```bash
python tools/build_single_file.py
```

Verify synchronization with:

```bash
python tools/build_single_file.py --check
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

Do not treat the hosted Demo Mode, starter identity placeholder, hidden UI controls, or client-visible scope logic as a security boundary.

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

### Application logging

AccessAtlas uses structured operational logging for troubleshooting and runtime visibility.

JSON logs are enabled by default and can be configured with:

```text
ACCESSATLAS_LOG_LEVEL
ACCESSATLAS_LOG_FORMAT
```

For example:

```bash
ACCESSATLAS_LOG_LEVEL=DEBUG ACCESSATLAS_LOG_FORMAT=text streamlit run modular/app.py
```

Application logs and governance audit events are intentionally separate. Operational logs describe application behavior and processing outcomes. Governance actions will be recorded through the audit-event model.

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
- `ROADMAP.md` — Now / Next / Later product direction and 1.0.0 readiness
- `docs/MODULAR_ARCHITECTURE.md` — single-file publishing, starter/demo runtime architecture, and structured logging configuration
- `docs/UI_STYLE_GUIDE.md` — current interface vocabulary and presentation conventions
- `docs/architecture/governance_patterns.md` — governance architecture patterns
- `docs/user-guides/access-reviewer-guide.md` — access review guidance
- `docs/user-guides/system-admin-guide.md` — System Administrator guidance
- `docs/user-guides/super-admin-guide.md` — Super Administrator guidance
- `SNOWFLAKE_NOTES.md` — Snowflake implementation path
- `POSTGRES_NOTES.md` — PostgreSQL implementation path

---

## Current Status and Future Direction

AccessAtlas is currently a functional reference application, quick-start starter, modular implementation, and public demo. It is not a production identity or access-management service.

The current 1.0.0 engineering work has established:

- a canonical modular source under `modular/`
- a generated root-level single-file starter
- automated synchronization checks between the two distributions
- a shared application core
- separate starter and hosted demo runtimes
- a starter identity extension point
- disposable, session-backed demo changes
- structured application logging with JSON or text output
- a governance audit-event model and current-session audit history
- scoped CSV data exports
- broader automated test coverage
- Ruff linting and formatting checks enforced in CI

The remaining 1.0.0 engineering priority is migration support, with deployment guidance retained as a stretch goal.

Notifications remain the first planned functional module after the 1.0.0 foundation.

See `ROADMAP.md` for product direction and `CHANGELOG.md` for development history.

---

## License

AccessAtlas is licensed under the MIT License. See `LICENSE`.
