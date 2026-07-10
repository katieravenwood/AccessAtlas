# AccessAtlas Data Access and Migration Boundary

AccessAtlas separates Streamlit workflows from persistence through repository protocols.

The application is designed so the same governance workflows can operate against the reference CSV/session implementation or an organization-specific persistent backend without embedding database code in `app_core.py`.

## Architecture

```text
Streamlit workflow
        |
        v
Governance logic
        |
        v
Repository protocols
        |
        +-- session-backed reference repositories
        +-- PostgreSQL repositories
        +-- Snowflake repositories
        +-- other organization-specific implementations
```

The repository layer answers a narrow question:

> How are canonical AccessAtlas governance records read and written?

It does not decide:

- application role visibility
- manager or system administrator scope
- compliance status
- reconciliation classifications
- recommended governance actions
- audit-event meaning

Those remain application and governance rules.

## Repository container

A runtime receives one `RepositoryContainer`:

```python
@dataclass(frozen=True)
class RepositoryContainer:
    users: UserRepository
    systems: SystemRepository
    access_assignments: AccessAssignmentRepository
    administrator_assignments: AdministratorAssignmentRepository
    audit_events: AuditStore
```

The default application path is:

```text
CSV reference files
        |
        v
load_data()
        |
        v
build_session_repositories()
        |
        v
RepositoryContainer
        |
        v
run_app()
```

The CSV files are seeds. Current-session mutations occur behind the session-backed repositories and remain disposable.

## Canonical schemas

Repository reads return pandas DataFrames normalized to AccessAtlas column names.

Canonical schema definitions live in:

```text
modular/accessatlas/repositories/schema.py
```

### Users

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

### Systems

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

### Access assignments

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

### System administrator assignments

```text
user_id
system_id
admin_role
assignment_status
granted_date
revoked_date
```

Audit-event schema remains defined by `AuditEvent` in `audit.py`.

Schema normalization:

- lowercases incoming column names
- adds missing canonical columns as nullable values
- normalizes configured date columns
- retains additional backend-specific columns after the canonical fields

This allows a backend repository to map organization-specific source names to the AccessAtlas contract before returning records.

## Repository protocols

Protocols are defined in:

```text
modular/accessatlas/repositories/protocols.py
```

The current contracts are:

- `UserRepository`
- `SystemRepository`
- `AccessAssignmentRepository`
- `AdministratorAssignmentRepository`
- existing `AuditStore`

Repositories use DataFrames for collection reads because AccessAtlas business logic already uses pandas for filtering, scope, compliance, reconciliation, summaries, and export preparation.

The repository boundary therefore avoids adding a second domain-object conversion layer solely to turn records back into DataFrames.

## Reference session repositories

Reference implementations live in:

```text
modular/accessatlas/repositories/session.py
```

They are:

- `SessionUserRepository`
- `SessionSystemRepository`
- `SessionAccessAssignmentRepository`
- `SessionAdministratorAssignmentRepository`
- `SessionAuditStore`

The session repositories preserve the public demo behavior:

```text
synthetic CSV seed
        |
        v
Streamlit session repository
        |
        v
disposable mutations
        |
        v
session ends or state clears
        |
        v
changes disappear
```

They also support an injected state mapping for unit tests.

## Runtime repository selection

`run_app()` accepts a repository factory:

```python
run_app(
    runtime_factory,
    repository_factory=build_reference_repositories,
)
```

The normal starter and demo entry points do not need to specify it because the reference factory is the default.

A database-backed deployment can supply another factory:

```python
run_app(
    build_starter_runtime,
    repository_factory=build_postgres_repositories,
)
```

or:

```python
run_app(
    build_starter_runtime,
    repository_factory=build_snowflake_repositories,
)
```

The Dashboard, My Access, Manage Access, Access Reconciliation, and AccessAtlas App Admin workflows should not change when the repository factory changes.

## PostgreSQL implementation pattern

PostgreSQL is a natural fit for an interactive operational deployment with frequent transactional updates.

A deployment-specific factory may use SQLAlchemy:

```python
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

A user repository can map database rows to the canonical AccessAtlas schema:

```python
class PostgresUserRepository:
    def __init__(self, engine):
        self.engine = engine

    def list_users(self) -> pd.DataFrame:
        dataframe = pd.read_sql(
            "select * from accessatlas.users",
            self.engine,
        )
        return normalize_users(dataframe)

    def get_user(self, user_id: str) -> pd.Series | None:
        users = self.list_users()
        matches = users[users["user_id"] == user_id]
        return None if matches.empty else matches.iloc[0]

    def create_user(self, record: dict) -> str:
        # Use a parameterized INSERT or SQLAlchemy Core statement.
        ...

    def update_user(self, user_id: str, changes: dict) -> bool:
        # Use a transaction and parameterized UPDATE.
        ...

    def replace_all(self, dataframe: pd.DataFrame) -> None:
        # Optional for bulk-oriented workflows. Production implementations
        # may instead translate reconciliation actions to targeted statements.
        ...
```

Production PostgreSQL implementations should define:

- table constraints and foreign keys
- transaction boundaries
- connection pooling
- secrets handling
- migration tooling
- authorization enforcement below the Streamlit UI
- audit retention and immutability requirements

The repository protocol is an application contract, not a substitute for backend authorization.

## Snowflake implementation pattern

Snowflake is useful when governance inventories, source-system exports, and analytical reporting already live in a centralized data platform.

A deployment-specific factory may use Snowpark:

```python
from snowflake.snowpark import Session

from accessatlas.repositories.container import RepositoryContainer


def build_snowflake_repositories() -> RepositoryContainer:
    session = Session.builder.configs(load_snowflake_config()).create()

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

A repository read can normalize Snowflake results:

```python
class SnowflakeUserRepository:
    def __init__(self, session):
        self.session = session

    def list_users(self) -> pd.DataFrame:
        dataframe = (
            self.session
            .table("ACCESSATLAS.GOVERNANCE.USERS")
            .to_pandas()
        )
        return normalize_users(dataframe)
```

Write implementations may use `INSERT`, `UPDATE`, or `MERGE` depending on the deployment's governance and workload model.

A Snowflake implementation should explicitly define:

- authentication and role selection
- warehouse selection and cost controls
- session lifecycle
- write permissions
- schema ownership
- reconciliation staging patterns
- audit retention
- backend authorization

PostgreSQL and Snowflake can satisfy the same AccessAtlas repository protocols without being operationally identical systems.

## Reconciliation and repositories

Reconciliation remains business logic.

```text
reconciliation.py
        |
        | determines:
        | - new access
        | - missing access
        | - status change
        | - no change
        v
repository
        |
        | persists:
        | - create assignment
        | - update assignment
        | - inactivate assignment
        v
audit event
```

The repository should not decide whether a source-system discrepancy represents an inactivation recommendation.

For the reference implementation, reconciliation functions may still produce an updated DataFrame and the application persists that result through `replace_all()`.

A production repository may optimize this by translating selected reconciliation outcomes into targeted statements while preserving the same workflow contract.

## Audit events

`AuditStore` remains the audit persistence contract.

The application sets the repository container's audit store as the active audit-event store after runtime initialization.

This means:

```text
record_audit_event()
        |
        v
active repository audit store
```

The reference runtime uses `SessionAuditStore`.

A persistent deployment can provide `PostgresAuditStore`, `SnowflakeAuditStore`, or another controlled append-oriented event store without changing the governance workflow code.

## Migration checklist

A deployment replacing the reference repositories should:

1. map source fields to the canonical AccessAtlas schemas;
2. implement the four repository protocols and `AuditStore`;
3. construct a `RepositoryContainer`;
4. provide a repository factory with no required Streamlit arguments;
5. pass that factory to `run_app`;
6. enforce equivalent or stronger authorization in the backend;
7. define transaction and audit consistency behavior;
8. run the AccessAtlas repository, scope, reconciliation, audit, and distribution tests.

The success criterion is:

> Changing the repository factory should not require changing a Streamlit workflow screen.
