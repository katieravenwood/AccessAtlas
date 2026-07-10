# AccessAtlas Deployment Guidance

AccessAtlas is a reference application and deployable starter. Running the reference app successfully is not the same as completing a production deployment.

This guide identifies the implementation decisions an organization should make before using AccessAtlas with real users, governed systems, or access records.

## Reference Application vs Production Deployment

The reference application provides:

- synthetic data
- CSV-seeded session repositories
- a development identity placeholder
- role-aware UI behavior
- current-session audit history
- structured process logging
- portable CSV exports

A production deployment should replace or harden the reference mechanisms where organizational data, authentication, authorization, persistence, or evidence requirements apply.

## Runtime Selection

AccessAtlas has three stable Streamlit entry points:

```text
/app.py
/modular/app.py
/modular/demo_app.py
```

Use:

- `app.py` for quick evaluation and direct customization
- `modular/app.py` for a modular deployment or engineering extension
- `modular/demo_app.py` only for synthetic role-preview behavior

Do not use the hosted-demo runtime as a production identity model.

## Environment Configuration

Application logging currently supports:

```text
ACCESSATLAS_LOG_LEVEL
ACCESSATLAS_LOG_FORMAT
```

The clean starter currently supports:

```text
ACCESSATLAS_USER_ID
```

as a development identity placeholder.

Production deployments should establish a documented configuration model for:

- environment name
- database or platform connection
- identity provider
- secrets source
- logging level and format
- repository selection
- deployment-specific feature flags

Configuration values that contain credentials or tokens should not be committed to the repository.

## Identity and Authentication

`ACCESSATLAS_USER_ID` is not authentication.

A production deployment should integrate an approved identity mechanism such as:

- enterprise Single Sign-On
- Microsoft Entra ID
- another OpenID Connect-compatible provider
- an organization-approved reverse proxy or platform identity layer

The authenticated identity should resolve to the canonical AccessAtlas user record or to an approved identity-mapping layer.

## Authorization Boundary

Hidden UI controls are not authorization.

The application demonstrates:

- role-aware section visibility
- manager scope
- system administrator scope
- super administrator visibility

A production implementation must enforce equivalent or stronger rules in the backend or repository layer.

Depending on the selected persistence platform, this may include:

- database roles
- row-level policies
- secure views
- stored procedures
- service-layer authorization
- repository-level predicates
- separate read and write credentials

Authorization design should assume that a user may attempt to bypass the normal UI.

## Repository Selection

The default reference path is:

```text
CSV seed data
    ->
session-backed repositories
    ->
disposable current-session changes
```

A production deployment should provide a repository factory appropriate to the persistence platform.

See:

- [`DATA_ACCESS.md`](DATA_ACCESS.md)
- [`integrations/POSTGRESQL.md`](integrations/POSTGRESQL.md)
- [`integrations/SNOWFLAKE.md`](integrations/SNOWFLAKE.md)

The selected repositories should return canonical AccessAtlas DataFrames and implement the current repository contracts.

## Secrets

Do not place database passwords, private keys, OAuth secrets, or access tokens in:

- source code
- CSV files
- committed `.env` files
- screenshots
- application logs
- audit-event change detail

Use an approved secrets mechanism for the deployment environment.

Examples may include:

- hosting-platform secrets
- environment variables injected by a deployment platform
- cloud secrets managers
- enterprise vault products

The exact mechanism is deployment-specific.

## Operational Logging

Application logs support troubleshooting and runtime visibility.

Production deployments should define:

- log destination
- minimum and maximum log level
- retention
- access to logs
- alerting and monitoring
- correlation with hosting or infrastructure logs

AccessAtlas operational logs should not become a second governance history repository.

## Governance Audit Storage

The reference `SessionAuditStore` is disposable.

Production deployments should replace it with a controlled append-oriented repository appropriate to governance and evidence requirements.

Define:

- retention
- immutability expectations
- permitted readers
- permitted writers
- archival
- legal or regulatory evidence requirements
- event correction policy
- time synchronization expectations

Audit-event change detail should remain limited to the governance fields required to understand the action.

## Transaction Considerations

The reference repositories use disposable session-backed DataFrames.

Persistent implementations should decide how to coordinate:

```text
governance record write
        +
audit event write
```

A transactional database may be able to commit both operations in one transaction.

A data-platform implementation may require another consistency pattern.

The repository protocol does not prescribe a universal transaction strategy. The deployment must document the selected behavior, including failure and retry handling.

## Reconciliation Inputs

System access reconciliation assumes a complete comparison set for one selected system.

Production processes should document:

- who produces the source export
- what "complete export" means for the selected system
- export effective time
- reconciliation cadence
- file or staging-table retention
- source-system identifiers
- exception handling
- responsibility for applying recommended actions

An incomplete export can create inappropriate inactivation recommendations.

## Backup and Recovery

Persistent deployments should define recovery objectives for:

- user governance records
- system catalog records
- access assignments
- administrator assignments
- audit events
- reconciliation staging data, where retained

At minimum, document:

- backup mechanism
- backup frequency
- recovery test cadence
- ownership
- restore procedure

## Hosting Patterns

AccessAtlas is a Streamlit application and can be deployed through several organization-specific hosting models.

Common patterns include:

- a managed Streamlit hosting environment
- an internal Python application host
- a container platform
- a cloud application service
- a reverse-proxy deployment

The repository does not prescribe one hosting provider.

A deployment should evaluate:

- network exposure
- identity integration
- TLS termination
- secrets injection
- process scaling
- session behavior
- connection pooling
- outbound connectivity
- monitoring
- patching responsibility

## Reverse Proxy Considerations

Where a reverse proxy or identity-aware gateway is used, document:

- trusted identity headers
- header stripping and spoofing protections
- host and scheme forwarding
- Streamlit WebSocket support
- session affinity, where required
- timeout behavior
- maximum upload size

Do not accept user-supplied identity headers as authenticated identity without a trusted upstream control.

## Monitoring

A production operating model should monitor:

- application availability
- application exceptions
- repository connection failures
- reconciliation processing failures
- export preparation failures
- authentication failures
- unusual authorization failures
- data refresh or source-ingestion issues

Operational monitoring and governance audit history serve different purposes and should remain separate.

## Data Retention

Define retention for:

- active governance records
- inactive governance records
- revoked access history
- audit events
- reconciliation source files or staging records
- application logs
- exports

AccessAtlas demonstrates inactive-not-delete as a governance pattern. A production retention policy must still reflect organizational legal, regulatory, privacy, and records-management requirements.

## Deployment Checklist

Before production use:

1. Replace the development identity placeholder with approved authentication.
2. Enforce role and record scope below the Streamlit UI.
3. Implement persistent repositories.
4. Document canonical source-to-AccessAtlas field mappings.
5. Configure secrets outside the repository.
6. Replace `SessionAuditStore` with controlled audit storage.
7. Define transaction and retry behavior.
8. Establish log retention and monitoring.
9. Validate reconciliation source completeness.
10. Define backup and recovery.
11. Define governance data and audit retention.
12. Run the full quality and test sequence.
13. Perform organization-specific security and accessibility review.
14. Document operational ownership and support procedures.

AccessAtlas provides the application and repository contracts. The deployment team remains responsible for the controls required by its environment.
