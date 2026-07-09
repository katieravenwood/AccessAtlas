# AccessAtlas Roadmap

AccessAtlas is evolving from a functional reference application into a deployable starter application for access-governance teams and data engineering organizations.

The project is intended to remain easy to evaluate, inexpensive to run, and straightforward to adapt. The public demo should demonstrate workflows without persisting tester changes or requiring a paid cloud backend. Production-oriented capabilities should be provided as modular components, implementation patterns, and extension points rather than forcing every deployment into a single architecture.

This roadmap uses **Now / Next / Later** to describe product direction without committing to calendar dates.

---

## Product Direction

AccessAtlas is being developed for two primary audiences:

1. **Data engineering teams looking for a starter architecture for access governance**
2. **Small and mid-sized organizations that need a practical access-governance application they can adapt**

The project is not intended to become a full identity and access management platform.

Its focus is the governance layer around access:

- cataloging users, systems, resources, and permissions
- tracking system administrator responsibility
- monitoring compliance requirements
- reconciling source-system access records
- reviewing access history and governance activity
- supporting periodic access audits
- providing clear extension points for notifications, authentication, provisioning, and other organization-specific workflows

Access approval remains outside the core application for now.

---

# Now

## Goal: Complete the 1.0.0 Deployable Starter Foundation

The current application already demonstrates the core AccessAtlas governance model and principal workflows.

The 1.0.0 engineering backlog is focused on making the repository easy to adopt for small and mid-sized organizations while giving data engineering teams clean extension points for broader implementation.

### 1. Dual-distribution modular architecture — Completed

AccessAtlas now maintains one canonical modular source under `modular/` and publishes a generated single-file starter at root `app.py`.

The root application remains the low-friction adoption path.

The modular implementation separates:

- application core
- configuration
- data loading
- role and scope logic
- compliance calculations
- reconciliation logic
- temporary state
- reusable presentation behavior
- runtime identity and guidance behavior

`tools/build_single_file.py` publishes the root starter from modular source.

CI and automated tests verify that the generated file remains synchronized.

### 2. Separate the public demo from the starter application — Completed

The shared application core now supports distinct runtime factories.

The clean starter:

- does not render the synthetic persona selector
- does not render demo-specific sidebar content
- does not display Demo Mode warnings
- resolves a current application identity through a replaceable starter runtime

The hosted demo retains:

- synthetic role/persona selection
- current demo-user details
- visible demo-scope summaries
- contextual demo sidebar guidance
- disposable session-backed changes

The hosted preview should run from:

```text
modular/demo_app.py
```

The root `app.py` and `modular/app.py` remain clean starter paths.

### 3. Add structured application logging — Completed

AccessAtlas now includes structured operational logging through the Python standard `logging` package.

The implementation provides:

- JSON Lines output by default
- optional human-readable text output
- configurable log level
- idempotent handler configuration for Streamlit reruns
- runtime and application-role context
- structured event names and fields
- exception logging with tracebacks
- tests for logging configuration and output contracts

Current operational events cover:

- application run start
- reference-data loading
- runtime and visible-scope resolution
- application-section rendering
- upload schema validation
- reconciliation comparison completion
- reconciliation action processing
- key-resolution failures
- data-load failures

Application logs remain explicitly separate from governance audit events.

### 4. Add audit logging and an audit-event model — Next implementation step

AccessAtlas now includes a modular governance audit-event model and replaceable audit-store contract.

The current reference implementation records meaningful governance actions for:

- user record creation
- self-service compliance date updates
- access assignment creation and update
- access inactivation
- access reconciliation actions
- training and agreement reconciliation actions
- compliance-driven user inactivation

The default `SessionAuditStore` keeps events append-oriented and session-backed so public demo activity remains disposable.

Super Administrators can review current-session governance history in AccessAtlas App Admin.

The event schema and storage contract are designed for migration to controlled persistent audit storage.

Administrator assignment changes and system catalog changes should emit events when those write workflows are introduced.

### 5. Add data exports — Completed

AccessAtlas now provides scoped CSV downloads directly in the workflows where governance datasets are reviewed.

Current exports include:

- filtered users
- filtered systems
- scoped access assignments
- system administrator assignments
- filtered compliance detail
- compliance follow-up records
- system access reconciliation results
- training and agreement reconciliation results
- filtered governance audit history

The reusable export-preparation module provides stable CSV output, optional column selection and sorting, UTF-8 spreadsheet compatibility, and formula-style text sanitization.

Exports inherit the current application role and record scope.

Successful downloads generate an operational application event and a governance audit event without copying exported record contents into either event stream.

### 6. Expand automated tests — Next implementation step

Current automated coverage includes reconciliation behavior, modular/source synchronization, source compilation, and starter/demo runtime-separation contracts.

Broaden coverage for:

- reconciliation matching and action classification
- single-system reconciliation scope
- compliance status calculations
- role and system scope logic
- audit-event generation
- export preparation
- data normalization and validation
- starter identity resolution

Tests should continue to focus first on business logic that can be exercised independently of Streamlit rendering.

### 7. Add linting and formatting — Planned for 1.0.0

Introduce a lightweight, documented code-quality baseline.

The repository should include automated checks for:

- formatting
- linting
- tests
- single-file distribution synchronization

The same checks should run in CI.

### 8. Define migration support — Planned for 1.0.0

Document and establish clear data-layer extension points for moving from synthetic CSV files to persistent storage.

The 1.0.0 application does **not** require a hosted persistent backend.

Migration support should instead provide:

- repository or data-access interfaces
- mapping guidance for the current entities
- migration considerations for identifiers and history
- implementation notes for PostgreSQL and Snowflake
- clear boundaries between UI, business logic, and persistence

### Stretch goal: deployment guidance

Provide practical deployment guidance for organizations adapting the starter application.

The first guidance should focus on architecture and configuration rather than prescribing one hosting provider.

Topics may include:

- environment configuration
- secrets handling
- authentication boundaries
- persistence selection
- logging
- backup considerations
- reverse proxy or hosted Streamlit patterns
- production authorization requirements

---

## First feature after 1.0.0: Notification module

Notifications are the next functional priority.

The notification capability should be implemented as a modular starter component rather than as a hard-coded email system.

The application should be able to identify notification-worthy events such as:

- training expiring soon
- expired compliance
- reconciliation items awaiting review
- administrative coverage gaps
- future audit or access-review assignments

The preferred design is:

1. AccessAtlas determines that a notification event is needed.
2. A notification record or event is generated.
3. A pluggable delivery provider handles transmission.

Reference delivery patterns may include:

- email
- Microsoft Power Automate or Logic Apps
- webhook-based delivery
- other organization-specific services

The core governance application should not depend on one notification vendor.

---

# Next

## Lightweight system catalog creation

Add a basic system-creation workflow to the application.

The initial version should support creation of a governed system with core fields such as:

- system name
- system type
- system category
- resource scope
- access model
- tracking method
- system owner
- administrative group
- record status

This is a near-term step toward configurable governance without attempting to build the complete governance-model designer at once.

---

## Pluggable authentication model

Introduce an authentication abstraction that removes authentication assumptions from page and workflow logic.

The reference implementation should define:

- an authenticated user identity
- application role or governance role mapping
- user-to-governance-record mapping
- scope resolution
- authorization checks

The first implementation may use a simple development or local provider.

Documentation should include production patterns and implementation considerations for:

- OpenID Connect
- Microsoft Entra ID
- Single Sign-On
- Active Directory-backed environments
- other compatible identity providers

Entra ID, SSO, and Active Directory integration are lower-priority reference implementations. The immediate objective is a clean authentication extension point.

---

## Access history and periodic audit support

Build on the audit-event model to support formal access-history review.

The application should be able to show:

- current access
- prior access
- grant and inactivation history
- relevant reconciliation actions
- administrator changes
- governance events affecting a user or system

Add starter workflows for periodic access audits, including semiannual reviews.

A review should distinguish between:

- **reconciliation** — do governance records match the source system?
- **access review** — should the user still retain the access?

Future audit-review structures may include:

- review scope
- review period
- reviewer
- access records in scope
- retain, remove, or update decision
- review completion status
- sign-off history

---

## Modular access enable/disable workflows

Provide starter modules and implementation patterns for integrating governance decisions with actual access-control actions.

The initial objective is not universal automated provisioning.

Reference patterns should demonstrate how an organization could:

- request access enablement
- request access disablement
- send an action to an external provisioning service
- record the result
- reconcile the resulting source-system state

AccessAtlas should keep governance state and provisioning execution conceptually separate.

---

## Expand source-system cataloging patterns

Continue supporting cataloging and reconciliation patterns for:

- CSV and file-based exports
- Snowflake roles and grants
- PostgreSQL permissions
- dashboard and report platforms
- collaboration platforms

Near-term work should focus on representing and reconciling access from those environments.

Direct provisioning and source-system control may be added later.

---

# Later

## Configurable governance model

Allow authorized administrators to configure more of the governance model through the application.

Potential capabilities include:

- create and edit systems
- manage system categories and types
- define resource types
- define available permissions
- configure access models
- define reconciliation mappings
- configure administrator roles

This work should build on the lightweight system-creation workflow introduced earlier.

---

## Configurable compliance requirements

Replace fixed compliance fields with a configurable requirements model.

A future requirement entity may include:

```text
Requirement
- requirement_id
- name
- requirement_type
- validity_period
- warning_period
- applicable system or category
- applicable user type
- record status
```

This would allow organizations to define their own:

- training
- certifications
- agreements
- acknowledgements
- recurring governance requirements

The current annual training, biennial training, and access agreement fields remain useful reference examples but should not define the long-term architecture.

---

## Optional access approval module

Keep approval workflows outside the core AccessAtlas application for the near term.

A future optional module may demonstrate:

- access requests
- configurable reviewers
- approval and denial decisions
- approval history
- handoff to provisioning workflows
- separation of requester, approver, and administrator responsibilities

The approval module should remain optional so organizations with established request and approval systems can continue using those processes.

---

## Deeper identity integrations

Potential future reference integrations include:

- Microsoft Entra ID
- enterprise Single Sign-On
- Active Directory
- other OpenID Connect-compatible providers

These integrations should build on the pluggable authentication model rather than introducing identity-provider-specific logic throughout the application.

---

## Expanded integration and provisioning patterns

Future reference integrations may demonstrate:

- Snowflake grant metadata ingestion
- PostgreSQL permission metadata ingestion
- dashboard and report platform APIs
- collaboration platform membership APIs
- API-based synchronization
- scheduled ingestion
- access provisioning and deprovisioning adapters

The roadmap does not assume that AccessAtlas should directly control every connected system.

Integrations should be added where they clarify reusable governance patterns.

---

# 1.0.0 Readiness Definition

AccessAtlas 1.0.0 will represent the first clean deployable starter foundation.

The release does **not** require a hosted database or persistent public demo backend.

The public demo should continue to reset tester changes and remain inexpensive to operate.

## Completed foundation

- canonical modular application source
- generated single-file quick-start distribution
- automated starter/source synchronization checks
- shared application core
- separate clean starter and hosted demo runtimes
- starter runtime identity extension point
- role and scope logic shared across starter and demo
- modular architecture documentation

## Remaining release requirements

- broader automated test coverage
- linting and formatting checks
- documented migration extension points
- current README, changelog, roadmap, architecture, and UI documentation

Deployment guidance remains a stretch goal for 1.0.0.

Authentication integration, persistent production storage, notifications, provisioning, configurable compliance requirements, and complete governance-model configuration are not required for 1.0.0 unless explicitly moved into release scope later.

---

# Guiding Constraints

The roadmap follows several deliberate constraints.

### Keep the hosted demo disposable

Tester changes should not persist across sessions or require an always-on paid data service.

### Prefer modules over mandates

Notifications, authentication, audit workflows, and provisioning should be designed as replaceable extension points.

### Keep governance separate from identity infrastructure

AccessAtlas may integrate with identity and provisioning platforms, but it should not attempt to replace a full IAM system.

### Preserve historical context

Inactive access and governance history should remain reviewable.

### Keep the starter application understandable

The project should demonstrate good engineering structure without becoming an abstraction exercise.

### Add integrations to teach a pattern

A small number of well-designed reference integrations are more useful than a long list of shallow connectors.

---

## Roadmap Status

This roadmap describes current product direction and may change as the reference implementation evolves.

Completed work is documented in `CHANGELOG.md`.
