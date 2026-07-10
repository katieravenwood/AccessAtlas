# AccessAtlas Modular Architecture

AccessAtlas publishes a quick-start single-file application from one canonical modular codebase and keeps the hosted demo as a separate runtime.

## Distribution and runtime model

```text
                         modular/accessatlas/app_core.py
                                      |
                     shared workflows and application UI
                                      |
                   +------------------+------------------+
                   |                                     |
                   v                                     v
      build_starter_runtime()                build_demo_runtime()
                   |                                     |
                   v                                     v
          modular/app.py                       modular/demo_app.py
                   |                                     |
                   | canonical starter                    | hosted demo
                   v                                     v
      tools/build_single_file.py              Streamlit demo deployment
                   |
                   v
              root app.py
```

The application UI and business logic are shared.

The runtime determines:

- the current application identity
- role-visible sections
- visible user, system, access, and administrator records
- optional runtime-specific guidance

## Root `app.py`: quick-start starter

The root application is generated from the modular starter runtime.

It contains no:

- Demo Mode persona selector
- Demo Mode sidebar warning
- Current Demo User panel
- Visible Demo Scope panel
- demo-only contextual sidebar guidance

Run it with:

```bash
streamlit run app.py
```

The starter resolves its current application identity from the `ACCESSATLAS_USER_ID` environment variable.

Example:

```bash
ACCESSATLAS_USER_ID=USR-0001 streamlit run app.py
```

When the variable is not set, the reference dataset resolves the first active Super Administrator, then the first active user, as a development-friendly fallback.

This is an application identity placeholder, not authentication. Production implementations should replace the starter runtime with an approved authentication provider and enforce authorization in the backend and data-access layer.

## `modular/demo_app.py`: hosted demo

The hosted demo retains the synthetic persona selector and role-scoped preview experience.

Run it with:

```bash
streamlit run modular/demo_app.py
```

The demo includes:

- Demo Mode explanation
- synthetic user/persona selector
- current demo user summary
- visible demo scope summary
- contextual sidebar guidance
- role-aware record and section scoping

Tester changes continue to use Streamlit session state and reset with the demo session.

## Shared application core

`modular/accessatlas/app_core.py` owns the shared Streamlit workflows and rendering logic.

It receives a runtime factory:

```python
run_app(build_starter_runtime)
```

or:

```python
run_app(build_demo_runtime)
```

The core does not own identity selection or demo controls.

This prevents the starter and demo from becoming separate application implementations.

## Runtime context

`modular/accessatlas/runtime.py` defines `RuntimeContext`.

A runtime context supplies:

```text
current_user
visible_tabs
users
systems
access
system_admins
runtime_name
is_demo
section_guidance_renderer
```

Future authentication modules can resolve the same context contract without rewriting workflow pages.

## Runtime implementations

### `starter_runtime.py`

Provides the clean starter behavior.

It:

1. resolves the configured application identity;
2. determines visible sections from the application role;
3. applies the current role-scope rules; and
4. returns a runtime context without demo UI.

### `demo_runtime.py`

Provides the hosted preview behavior.

It:

1. renders the persona selector;
2. resolves the selected synthetic user;
3. determines visible sections;
4. applies the same role-scope rules used by the starter;
5. renders demo scope information; and
6. attaches demo-only contextual guidance.


## Structured application logging

`modular/accessatlas/logging_config.py` configures AccessAtlas operational logs.

Application logs are separate from governance audit events:

- **application logs** support troubleshooting, runtime visibility, data-loading diagnostics, and processing failures;
- **audit events** record meaningful governance actions and belong to the separate audit-event model.

The logging module uses the Python standard `logging` package and emits JSON lines by default.

Configuration is controlled through:

```text
ACCESSATLAS_LOG_LEVEL
ACCESSATLAS_LOG_FORMAT
```

Supported log formats are:

```text
json
text
```

The default is:

```text
ACCESSATLAS_LOG_LEVEL=INFO
ACCESSATLAS_LOG_FORMAT=json
```

The logger is configured idempotently so Streamlit reruns do not add duplicate handlers.

Runtime context is attached after the starter or demo runtime resolves. Current structured fields include:

```text
event
runtime
application_role
fields
```

Application logs deliberately avoid display names, email addresses, and governance action details that belong in the audit model.

Initial operational events cover:

- application run start
- reference-data loading
- runtime and visible-scope resolution
- application-section rendering
- upload schema validation
- reconciliation comparison completion
- reconciliation action processing
- reconciliation key-resolution failures
- reference-data load failures


## Single-file publishing

The modular implementation remains the canonical engineering source.

Build the root starter with:

```bash
python tools/build_single_file.py
```

Verify synchronization with:

```bash
python tools/build_single_file.py --check
```

The generated root `app.py` bundles:

- shared application modules
- runtime context
- starter runtime
- shared application core
- starter entry point

The demo runtime is deliberately excluded from the generated root application.

## Hosted demo deployment

The Streamlit-hosted preview should use:

```text
modular/demo_app.py
```

The root `app.py` should remain the recommended quick-start path in the README.

## Code quality boundary

Ruff is the shared formatter and linter for canonical Python source, tests, and build tooling.

Configuration is defined in:

```text
pyproject.toml
```

Development dependencies are defined in:

```text
requirements-dev.txt
```

The quality boundary is:

```text
modular/
tests/
tools/
```

The generated root `app.py` is intentionally excluded from direct Ruff checks because module bundling places repeated imports after executable module content. Formatting and linting the generated artifact would therefore create noise around the bundling mechanism rather than improve the canonical source.

The generated distribution remains protected by:

```bash
python tools/build_single_file.py --check
```

CI runs formatter checks, lint checks, the distribution synchronization check, and the full automated test suite.


## Test strategy

The test suite protects business-rule and architecture boundaries rather than reproducing Streamlit rendering.

```text
UI workflow
    ↓
tested business function
    ↓
tested state / audit / export boundary
```

Coverage is organized by concern:

```text
test_compliance.py
test_scope.py
test_navigation.py
test_starter_runtime.py
test_state.py
test_reconcile.py
test_reconciliation_edges.py
test_audit.py
test_exports.py
test_logging.py
test_runtime_separation.py
test_single_file_build.py
```

`tests/conftest.py` adds the canonical `modular/` package to the test path.

When Streamlit is unavailable, the test bootstrap provides a minimal session-state adapter for pure unit tests. This does not emulate Streamlit rendering; it only supports testing modules whose reference state adapter uses `st.session_state`.

The full suite should run with:

```bash
pytest -q
```

Distribution checks remain part of the same suite so modular-source changes cannot silently drift from the generated root starter.


## Data export boundary

CSV export preparation is centralized in:

```text
modular/accessatlas/exports.py
```

The module does not decide which records a user may export.

Role and record scope are resolved before a workflow passes a dataframe to the export helper:

```text
runtime scope
    ↓
workflow dataframe
    ↓
prepare_csv_export()
    ↓
CSV download artifact
```

This keeps export serialization separate from authorization and scope resolution.

The reference export artifact contains:

```text
export_name
filename
data
mime_type
record_count
column_count
```

CSV preparation supports explicit column ordering and stable sorting.

Text fields beginning with spreadsheet formula prefixes are escaped before CSV serialization. This protects users who open exported governance data in spreadsheet software from formula-style cell execution.

Successful downloads emit:

```text
Operational log
    └── data_export_downloaded

Governance audit history
    └── data_export / export_dataset
```

The application log and audit event record export metadata, not the exported row contents.

CSV is the baseline reference format. Additional formats should be added only when they clarify a reusable governance or interoperability pattern.


## Governance audit events

Governance audit history is implemented separately from structured application logging.

```text
Operational event
    └── logging_config.py
        └── runtime/process troubleshooting

Governance action
    └── audit.py
        └── append-oriented audit event
```

`modular/accessatlas/audit.py` defines:

- `AuditEvent`
- `AuditStore`
- `SessionAuditStore`
- audit actor/runtime context
- event creation and recording helpers
- dataframe access for review and future export

The shared application core sets audit actor context after the starter or demo runtime resolves the current user.

The default session-backed store is deliberate for the reference application:

- hosted demo actions do not persist
- no public test activity accumulates
- no hosted database is required
- the event model remains demonstrable

The `AuditStore` protocol is the production extension point. A persistent implementation may write to an append-oriented database table, governed event store, or another controlled audit repository.

Production implementations should define retention, immutability, access control, evidence requirements, and archival behavior according to their own governance and regulatory context.

Audit event change detail is serialized into `changes_json`. The reference model records actor, target, entity, system, outcome, source, summary, and runtime context without using the operational log stream as governance history.


## Maintenance rule

Shared application changes belong in:

```text
modular/accessatlas/
```

Starter runtime behavior belongs in:

```text
modular/accessatlas/starter_runtime.py
```

Demo-only behavior belongs in:

```text
modular/accessatlas/demo_runtime.py
```

After shared or starter changes:

```bash
python tools/build_single_file.py
```

Commit the modular source and generated root `app.py` together.

Demo-only changes do not require rebuilding root `app.py` unless shared application behavior also changed.
