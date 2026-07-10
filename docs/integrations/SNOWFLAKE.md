# Snowflake Repository Implementation Guide

This guide describes how a Snowflake deployment can implement the AccessAtlas repository contracts.

It is an integration pattern, not a complete production Snowflake package.

Start with [`../DATA_ACCESS.md`](../DATA_ACCESS.md) for the canonical repository interfaces and DataFrame schemas.

## Recommended Fit

Snowflake is a strong fit when:

- governed inventories already exist in a centralized data platform
- source-system access exports are staged in Snowflake
- governance reporting and analytics are important
- access data spans multiple source systems
- an organization already operates approved Snowflake authentication, role, and cost controls

Snowflake and PostgreSQL can satisfy the same AccessAtlas repository protocols without being operationally identical.

## Architecture Pattern

```text
Streamlit workflow
        |
        v
RepositoryContainer
        |
        v
Snowflake repository implementations
        |
        v
Snowpark or Snowflake connector
        |
        v
Snowflake governance database/schema
```

The Streamlit screens should not contain Snowflake SQL, warehouse selection, or session construction logic.

## Repository Factory

A deployment-specific factory may look like:

```python
from snowflake.snowpark import Session

from accessatlas.repositories.container import RepositoryContainer


def build_snowflake_repositories() -> RepositoryContainer:
    session = (
        Session.builder
        .configs(load_snowflake_config())
        .create()
    )

    return RepositoryContainer(
        users=SnowflakeUserRepository(session),
        systems=SnowflakeSystemRepository(session),
        access_assignments=SnowflakeAccessAssignmentRepository(session),
        administrator_assignments=(
            SnowflakeAdministratorAssignmentRepository(session)
        ),
        audit_events=SnowflakeAuditStore(session),
    )
```

A deployment entry point can then supply:

```python
run_app(
    build_starter_runtime,
    repository_factory=build_snowflake_repositories,
)
```

## Suggested Object Organization

A deployment may use an organization-specific structure such as:

```text
ACCESSATLAS database
    |
    +-- GOVERNANCE schema
    |       USERS
    |       SYSTEMS
    |       ACCESS_ASSIGNMENTS
    |       SYSTEM_ADMINISTRATOR_ASSIGNMENTS
    |       AUDIT_EVENTS
    |
    +-- STAGING schema
            ACCESS_EXPORT_*
            COMPLIANCE_EXPORT_*
```

This is an example only.

An enterprise implementation may instead place AccessAtlas objects in an existing governed database or separate schemas by environment.

## Canonical Schema Mapping

Snowflake often returns unquoted identifiers in uppercase.

Repository implementations should normalize results before returning them.

```python
from accessatlas.repositories.schema import normalize_users


class SnowflakeUserRepository:
    def __init__(self, session):
        self.session = session

    def list_users(self):
        dataframe = (
            self.session
            .table("ACCESSATLAS.GOVERNANCE.USERS")
            .to_pandas()
        )
        return normalize_users(dataframe)
```

The AccessAtlas normalization helpers lowercase incoming column names and normalize configured date fields.

A repository may also explicitly map organization-specific source names.

Example:

```text
EMPLOYEE_GUID    -> user_id
PREFERRED_NAME   -> display_name
EMPLOYMENT_STATE -> record_status
```

The physical Snowflake schema does not need to use the exact reference CSV column names.

## Repository Reads

Snowflake repositories should consider whether each read should:

- materialize a full table to pandas
- filter in Snowflake first
- use a secure view
- use a role-scoped view
- use a stored procedure or service layer

The reference repository protocols currently return DataFrames because AccessAtlas uses pandas for scope, compliance, reconciliation, summaries, and exports.

For large deployments, push selective filters to Snowflake before calling `to_pandas()` where practical.

The repository implementation should still return the canonical AccessAtlas contract.

## Repository Writes

Write behavior may use:

```text
INSERT
UPDATE
MERGE
```

depending on the entity and workflow.

Examples:

```text
create user
    -> INSERT

update compliance dates
    -> targeted UPDATE

create access assignment
    -> INSERT

inactivate access assignment
    -> UPDATE access_status and revoked_date
```

Do not use wholesale table replacement as the default production write strategy merely because the reference session repository supports `replace_all()`.

## Reconciliation Staging

Snowflake is particularly well suited to staged reconciliation inputs.

A deployment may load source exports into:

```text
STAGING.ACCESS_EXPORT_<SOURCE>
```

with metadata such as:

```text
source_system_id
source_export_id
loaded_at
effective_at
source_filename
source_record_id
```

The AccessAtlas comparison workflow currently expects a complete export for one selected system.

A Snowflake implementation may:

1. identify the selected system and approved export batch;
2. query the complete staged batch;
3. normalize the result to the expected reconciliation input;
4. run the shared AccessAtlas comparison logic;
5. persist selected governance actions through repository methods.

This keeps reconciliation classification in the application business logic while using Snowflake for durable source staging.

## MERGE Patterns

`MERGE` may be useful for source-ingestion or repository maintenance workflows.

Use it carefully.

The AccessAtlas reconciliation queue presents recommended governance actions for human review. A production implementation should not automatically convert every source difference into an unreviewed `MERGE` against governance state unless the organization's operating model explicitly allows that behavior.

A reviewed action can map to a targeted `INSERT` or `UPDATE`.

## Role and Warehouse Selection

Document:

- authentication method
- Snowflake role
- secondary role behavior, if any
- warehouse
- database
- schema
- query tag
- session lifetime

Use least-privilege roles appropriate to the application.

Consider separate roles for:

- application reads
- governance writes
- audit-event append
- administrative maintenance

## Cost Controls

The public AccessAtlas demo intentionally does not require Snowflake.

A Snowflake deployment should define:

- warehouse size
- auto-suspend
- auto-resume
- resource monitors
- statement timeouts
- query filters
- application concurrency expectations

Repository methods should avoid repeatedly materializing large unfiltered tables when a narrower query is sufficient.

## Session Lifecycle

Streamlit reruns can execute application code frequently.

Do not create an uncontrolled Snowflake session for every minor widget interaction without understanding the connection and authentication impact.

A deployment should define:

- session creation strategy
- session caching or reuse
- expiry handling
- reconnect behavior
- thread/concurrency behavior
- cleanup

The selected pattern depends on the Snowflake client and hosting environment.

## Audit Events

Implement `AuditStore` as an append-oriented Snowflake repository or another controlled event store.

A Snowflake audit table may support:

- append-only application role
- read-only governance review role
- clustering or search optimization only where justified
- time-based retention and archival
- downstream governance reporting

Audit-event storage should remain separate from operational application logs.

## Authorization

A Snowflake-backed implementation should enforce authorization below the Streamlit UI.

Possible controls include:

- Snowflake roles
- secure views
- row access policies
- masking policies
- stored procedures
- repository queries scoped to the authenticated identity
- a service layer

UI section visibility is not sufficient authorization.

## Deployment-Specific Packages

The public reference app should not add Snowpark or the Snowflake connector as mandatory runtime dependencies.

A Snowflake implementation should maintain deployment-specific dependencies, for example:

```text
requirements-snowflake.txt
```

or an organization-specific application package.

This preserves the lightweight public starter.

## Validation Checklist

A Snowflake implementation should demonstrate that:

1. all repository protocol methods are implemented;
2. repository reads return normalized canonical DataFrames;
3. Snowflake sessions and roles use approved authentication and least privilege;
4. warehouse and cost controls are documented;
5. source reconciliation batches are complete and traceable;
6. selected reconciliation actions produce controlled writes;
7. audit events use controlled persistent storage;
8. role and record scope are enforced below the UI;
9. integration tests cover schema mapping, writes, and source-staging behavior.
