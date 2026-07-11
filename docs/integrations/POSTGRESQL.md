# PostgreSQL Repository Implementation Guide

This guide describes how a PostgreSQL deployment can implement the AccessAtlas repository contracts.

It is an integration pattern, not a complete production database package.

Start with [`../DATA_ACCESS.md`](../DATA_ACCESS.md) for the canonical repository interfaces and DataFrame schemas.

## Recommended Fit

PostgreSQL is a natural fit when AccessAtlas is used as an interactive operational application with:

- frequent user-driven writes
- transactional record changes
- targeted access-assignment updates
- relational integrity requirements
- persistent audit-event storage
- conventional application connection pooling

## Architecture Pattern

```text
Streamlit workflow
        |
        v
RepositoryContainer
        |
        v
PostgreSQL repository implementations
        |
        v
SQLAlchemy engine
        |
        v
PostgreSQL
```

The Streamlit screens should not contain PostgreSQL SQL or connection logic.

## Repository Factory

A deployment-specific factory may look like:

```python
import os

from sqlalchemy import create_engine

from accessatlas.repositories.container import RepositoryContainer


def build_postgres_repositories() -> RepositoryContainer:
    engine = create_engine(
        os.environ["ACCESSATLAS_DATABASE_URL"],
        pool_pre_ping=True,
    )

    return RepositoryContainer(
        users=PostgresUserRepository(engine),
        systems=PostgresSystemRepository(engine),
        access_assignments=PostgresAccessAssignmentRepository(engine),
        administrator_assignments=(
            PostgresAdministratorAssignmentRepository(engine)
        ),
        audit_events=PostgresAuditStore(engine),
    )
```

The deployment entry point can then supply the factory:

```python
run_app(
    build_starter_runtime,
    repository_factory=build_postgres_repositories,
)
```

## Suggested Relational Model

A baseline schema may contain:

```text
users
systems
access_assignments
system_administrator_assignments
audit_events
```

The physical schema does not need to copy the reference CSV files exactly. Repository implementations may map organization-specific source fields into the canonical AccessAtlas contracts.

## Users

Example:

```sql
create table accessatlas.users (
    user_id text primary key,
    display_name text not null,
    first_name text,
    last_name text,
    email text,
    application_role text not null,
    manager_user_id text,
    department text,
    user_type text,
    record_status text not null,
    annual_training_date date,
    biennial_training_date date,
    access_agreement_date date,
    created_date timestamp not null,
    updated_date timestamp not null
);
```

Consider:

- a self-referencing manager foreign key where appropriate
- unique constraints for approved enterprise identifiers
- check constraints for controlled status values
- indexes for manager and record-status filters

## Systems

A system table should support the canonical fields:

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

Consider indexes on:

- `system_type`
- `system_category`
- `record_status`

## Access Assignments

Access assignments model:

```text
User -> System -> Resource -> Permission
```

A PostgreSQL table should generally include:

- primary key on `access_id`
- foreign keys to users and systems
- indexes on `user_id` and `system_id`
- indexes or a composite index supporting the reconciliation key

The current reconciliation comparison key is:

```text
user_id
system_id
resource_type
resource_name
permission_name
```

A deployment should decide whether this combination is:

- uniquely constrained; or
- allowed to repeat for historical/source-specific reasons

Do not delete revoked assignments merely to represent current state. AccessAtlas uses inactive-not-delete as its reference governance pattern.

## System Administrator Assignments

System administrator assignments are separate from ordinary access assignments.

A baseline key may use:

```text
user_id
system_id
admin_role
```

or a deployment-specific surrogate assignment identifier.

Consider indexes on:

- `user_id`
- `system_id`
- `assignment_status`

## Repository Reads

A repository read should normalize results before returning them.

```python
import pandas as pd

from accessatlas.repositories.schema import normalize_users


class PostgresUserRepository:
    def __init__(self, engine):
        self.engine = engine

    def list_users(self) -> pd.DataFrame:
        dataframe = pd.read_sql(
            "select * from accessatlas.users",
            self.engine,
        )
        return normalize_users(dataframe)
```

Parameterized queries should be used for single-record reads.

## Repository Writes

Use SQLAlchemy Core or parameterized SQL.

A user update should conceptually perform:

```text
validate requested fields
        ->
open transaction
        ->
update targeted user
        ->
verify affected row count
        ->
commit
```

Do not build SQL by concatenating values from Streamlit inputs.

## Reconciliation Writes

The reference session repository supports `replace_all()` because it persists disposable DataFrames.

A PostgreSQL implementation should generally prefer targeted operations for selected reconciliation actions:

```text
Add access record
    -> INSERT

Inactivate
    -> UPDATE access_status and revoked_date

Update
    -> UPDATE changed access fields
```

A production repository may still implement `replace_all()` for contract compatibility, but reconciliation should not require truncating and rewriting the complete access table.

## Transaction Boundaries

Define how governance writes and audit events are coordinated.

A common PostgreSQL design is:

```text
BEGIN
    governance record write
    audit event append
COMMIT
```

The current AccessAtlas workflow calls repository writes and audit recording separately, so a production implementation may introduce a service or unit-of-work layer if atomic write-and-audit behavior is required.

Document:

- rollback behavior
- retry behavior
- duplicate handling
- idempotency expectations
- deadlock or serialization retry strategy

## Audit Events

Implement `AuditStore` with append-oriented storage.

Consider:

- a database-generated or application-generated audit event ID
- immutable event rows
- restricted write role
- restricted read role
- time-zone-aware timestamps
- indexed event type, action, actor, entity, system, and occurrence time
- archival and retention policy

Do not use ordinary application logs as the governance audit repository.

## Connection Pooling

Use an application-appropriate SQLAlchemy connection pool.

`pool_pre_ping=True` is useful for detecting stale connections.

Deployment-specific settings may include:

- pool size
- max overflow
- recycle interval
- connect timeout
- statement timeout

Tune these settings for the hosting platform and expected concurrent Streamlit sessions.

## Migrations

Use a controlled schema migration process.

Common choices include Alembic or an organization-standard database change process.

Migration ownership should cover:

- table creation
- constraints
- indexes
- reference values
- audit schema evolution
- backward compatibility

Do not rely on the Streamlit application to create or mutate production tables implicitly at startup.

## Authorization

The PostgreSQL implementation should enforce authorization below the UI.

Possible patterns include:

- separate read and write database roles
- database views
- row-level security
- stored procedures
- repository-level predicates
- a service layer

The correct pattern depends on the organization's identity and hosting architecture.

## Secrets

Provide connection credentials through the deployment environment.

Do not commit:

```text
DATABASE_URL
passwords
private keys
tokens
```

to the repository.

## Validation Checklist

A PostgreSQL implementation should demonstrate that:

1. all repository protocol methods are implemented;
2. reads return normalized canonical DataFrames;
3. inactive records are preserved as intended;
4. reconciliation actions produce targeted writes;
5. role and record scope are enforced below the UI;
6. audit events use controlled persistent storage;
7. transaction and retry behavior are documented;
8. the AccessAtlas repository and reconciliation tests pass against the implementation or an equivalent integration test suite.
