# AccessAtlas Architecture

AccessAtlas is a Streamlit reference application and deployable starter for access-governance workflows. Its architecture is designed to keep the public demo inexpensive and disposable while providing explicit extension points for enterprise identity, persistent storage, notifications, provisioning, and organization-specific governance requirements.

## Architecture Overview

```text
Entry point
    |
    v
Runtime factory
    |
    v
Shared Streamlit application core
    |
    +-------------------+
    |                   |
    v                   v
Governance logic     Presentation helpers
    |
    v
Repository protocols
    |
    +--------------------+--------------------+
    |                    |                    |
    v                    v                    v
Session reference     PostgreSQL           Snowflake
repositories          repositories         repositories
```

Two additional cross-cutting concerns remain intentionally separate:

```text
Application logging  -> process / hosting logs
Governance actions   -> AuditStore
```

## Application Layers

### Entry points

AccessAtlas preserves three stable Streamlit entry points:

```text
/app.py
/modular/app.py
/modular/demo_app.py
```

The root `app.py` is a generated single-file distribution. The canonical source is under `modular/`.

### Runtime layer

Runtime factories resolve the current application experience.

The current runtimes are:

- `build_starter_runtime()` — clean starter behavior
- `build_demo_runtime()` — hosted synthetic role-preview behavior

A runtime resolves:

- current user
- application role
- visible top-level sections
- scoped users
- scoped systems
- scoped access assignments
- scoped system administrator assignments
- runtime name
- demo status
- repository container
- optional section guidance renderer

The shared application core does not own synthetic persona selection.

### Application workflow layer

`modular/accessatlas/app_core.py` owns the shared Streamlit workflows:

- Dashboard
- My Access
- Manage Access
- Access Reconciliation
- AccessAtlas App Admin

The application core coordinates presentation, business logic, repository reads and writes, exports, operational logging, and governance audit events.

It should not contain database-specific SQL, Snowflake session logic, or direct persistence implementation details.

### Governance logic layer

Reusable business logic remains outside the Streamlit workflow wherever practical.

Current modules include:

- `compliance.py` — expiration and compliance calculations
- `scope.py` — role-aware record scope
- `reconciliation.py` — source comparison and action processing
- `navigation.py` — visible-section and label behavior
- `exports.py` — scoped CSV artifact preparation
- `audit.py` — governance audit-event model and store contract
- `logging_config.py` — operational application logging

A key architectural rule is:

> Governance logic decides what a record means or what action is recommended; repositories decide how governed data is read or persisted.

## Role and Scope Resolution

The current application roles are:

```text
User
Manager
System Administrator
Super Administrator
```

Role visibility is task-oriented:

| Role | Visible sections |
| --- | --- |
| User | My Access |
| Manager | Dashboard, My Access, Manage Access, Access Reconciliation |
| System Administrator | Dashboard, My Access, Manage Access, Access Reconciliation |
| Super Administrator | Dashboard, My Access, Manage Access, Access Reconciliation, AccessAtlas App Admin |

Record scope is separate from section visibility.

Examples:

- Users see their own governance record.
- Managers see themselves and direct reports, plus systems associated with that visible scope.
- System Administrators see systems they actively administer and the associated users and access assignments.
- Super Administrators see the complete repository dataset available to the runtime.

These rules demonstrate intended governance behavior. A production implementation must enforce equivalent or stronger authorization below the UI.

## Repository Data-Access Boundary

AccessAtlas workflow code receives persistence dependencies through a `RepositoryContainer`.

```text
Streamlit workflow
        |
        v
governance logic
        |
        v
repository protocol
        |
        +-- session-backed reference implementation
        +-- PostgreSQL implementation
        +-- Snowflake implementation
        +-- other organization-specific implementation
```

Repository modules live under:

```text
modular/accessatlas/repositories/
```

The canonical package contains:

- `schema.py` — canonical tabular contracts and normalization
- `protocols.py` — entity repository interfaces
- `container.py` — runtime repository dependency container
- `session.py` — disposable reference repositories
- `factory.py` — default CSV-seeded session repository factory

Repository protocols cover:

- Users
- Systems
- Access Assignments
- System Administrator Assignments

The existing `AuditStore` remains the persistence contract for governance audit events.

`run_app()` accepts a repository factory. The default factory loads synthetic CSV seed data and constructs session-backed repositories.

The application core does not directly load the governance CSV datasets and does not directly mutate editable user, system, access, or administrator-assignment session-state tables.

See [`DATA_ACCESS.md`](DATA_ACCESS.md) for the complete contract.

## Governance Business Logic

### Compliance

The reference model tracks:

- annual training date
- biennial training date
- access agreement date

The application derives expiration and compliance status from those dates.

The reference configuration uses:

- one-year annual training validity
- two-year biennial training validity
- a 30-day expiring-soon window

These fields are reference examples. A future configurable requirements model is planned.

### Access reconciliation

System access reconciliation compares the governance inventory to one complete source-system export for one selected system.

The comparison may classify records as:

- new access in the upload
- current active access missing from the upload
- access-status difference
- no action

Recommended actions are:

- Add access record
- Inactivate
- Update

The one-system scope is deliberate: absence can support an inactivation recommendation only when the comparison set is complete for the system being reviewed.

### Training and agreement reconciliation

A separate workflow compares:

- annual training date
- biennial training date
- access agreement date

against current user records.

This workflow uses the same general pattern:

```text
validate
    ->
compare
    ->
review differences
    ->
select actions
    ->
persist selected changes
    ->
record audit events
```

### Access review is distinct

Reconciliation asks:

> Does the governance record match the source?

Access review asks:

> Should the user still retain access?

Formal access-review workflows remain outside the current core application.

## Operational Application Logging

`modular/accessatlas/logging_config.py` configures structured operational logging using the Python standard `logging` package.

Configuration is controlled through:

```text
ACCESSATLAS_LOG_LEVEL
ACCESSATLAS_LOG_FORMAT
```

Supported formats:

```text
json
text
```

The default is JSON Lines at `INFO` level.

Operational logs support:

- startup visibility
- data-loading diagnostics
- runtime and scope resolution
- upload validation
- reconciliation processing
- export activity
- exception troubleshooting

Application logs deliberately avoid automatically recording user display names, email addresses, compliance dates, or governance change detail.

## Governance Audit Events

Application logs and audit events answer different questions:

```text
Application logs
    How is the software behaving?

Governance audit events
    What governance action happened to a governed record?
```

`modular/accessatlas/audit.py` defines:

- immutable `AuditEvent`
- replaceable `AuditStore` protocol
- session-backed `SessionAuditStore`
- audit actor/runtime context
- deterministic change-detail serialization

Current audited actions include:

- user creation
- self-service compliance-date updates
- access assignment creation and update
- access reconciliation actions
- training and agreement reconciliation actions
- compliance-driven user inactivation
- scoped data exports

The runtime repository container supplies the active audit store.

The reference `SessionAuditStore` is disposable and append-oriented. It is not a production immutable audit repository.

## Starter and Demo Distribution

The canonical source and published distributions are:

```text
modular/accessatlas/
        |
        +-- shared application and business logic
        |
        +--> modular/app.py
        |       clean modular starter
        |
        +--> modular/demo_app.py
        |       hosted demo
        |
        +--> tools/build_single_file.py
                |
                v
              app.py
              generated quick-start starter
```

### Clean starter

The starter:

- does not render Demo Mode persona selection
- does not render demo warnings
- does not render Current Demo User or Visible Demo Scope panels
- uses the `ACCESSATLAS_USER_ID` development identity extension point
- uses the default repository factory unless another is supplied

`ACCESSATLAS_USER_ID` is not authentication.

### Hosted demo

The demo:

- renders a synthetic persona selector
- resolves the selected synthetic user
- shows current demo-user and visible-scope context
- renders demo-only guidance
- uses the same shared workflows and role-scope rules
- keeps tester changes disposable

### Generated quick-start

The root `app.py` is generated from canonical modular source.

Build:

```bash
python tools/build_single_file.py
```

Verify synchronization:

```bash
python tools/build_single_file.py --check
```

Shared application changes belong under `modular/`. The generated root application should not be edited as the canonical source.

## Testing Boundaries

The test strategy emphasizes deterministic business rules and architectural contracts rather than reproducing Streamlit rendering behavior.

Coverage includes:

- compliance calculations
- role and record scope
- navigation visibility
- starter identity resolution
- session repository behavior
- canonical data normalization
- reconciliation edge cases
- audit-event storage and audited writes
- CSV export safeguards
- operational logging configuration
- starter/demo separation
- repository runtime boundary
- generated single-file synchronization and compilation

The intended flow is:

```text
UI workflow
    |
    v
tested business function
    |
    v
tested repository / audit / export boundary
```

## Code Quality Boundary

Ruff is the shared formatter and linter for:

```text
modular/
tests/
tools/
```

The generated root `app.py` is excluded from direct Ruff checks because it is a bundled build artifact. The synchronization check protects the generated distribution.

CI runs:

```bash
ruff format --check modular tests tools
ruff check modular tests tools
python tools/build_single_file.py --check
pytest -q
```

## Security and Authorization Boundary

AccessAtlas is not an identity and access management enforcement product.

The reference application demonstrates governance workflows and intended role-aware visibility. It does not provide production authentication or backend authorization.

A production deployment must define:

- enterprise identity and authentication
- backend role and scope authorization
- repository-level or database-level access controls
- secrets handling
- audit retention and immutability
- transaction behavior
- deployment monitoring and support

Hidden Streamlit controls are not a security boundary.

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for deployment considerations.

## Extension Points

The current architecture intentionally supports future modules and deployment-specific implementations.

Near-term extension points include:

- notification providers
- PostgreSQL repositories
- Snowflake repositories
- enterprise identity integration
- configurable systems and governance metadata
- configurable compliance requirements
- access review workflows
- provisioning adapters

The public reference application should remain platform-neutral. Organization-specific implementations should extend these contracts rather than embedding private operational assumptions into the reference core.
