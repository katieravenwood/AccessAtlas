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

## Goal: Prepare the 1.0.0 Deployable Starter Application

The current Streamlit application already demonstrates the core AccessAtlas governance model and principal workflows. The immediate roadmap focuses on turning that implementation into a clean starter application that can be evaluated, understood, and adapted without inheriting demo-specific structure.

### Modularize the application

Refactor the current root-level `app.py` into a maintainable application structure.

The target should separate concerns such as:

- application entry point
- configuration
- data loading and repository behavior
- role and scope logic
- compliance calculations
- reconciliation logic
- audit logging
- exports
- reusable UI components
- page or workflow rendering

The modularized structure should remain approachable to developers evaluating the repository. The goal is not to create a framework inside the framework.

### Separate the public demo from the starter application

Retain the current Demo Mode experience for the hosted preview.

Create a clean starter version that removes:

- synthetic persona selection
- demo-specific sidebar content
- Demo Mode warnings and explanatory controls
- assumptions that a selected synthetic user represents the authenticated user

The starter implementation should be placed in a clearly named repository location and be easy to copy or adapt.

The demo and starter versions should share core business logic wherever practical so they do not evolve into two unrelated applications.

### Add data exports

Provide export capability for key governance datasets and review results.

Initial export targets should include:

- users
- systems
- access assignments
- system administrator assignments
- compliance follow-up records
- reconciliation results
- audit history, when available

CSV should remain the baseline export format for portability.

### Add audit logging

Introduce a modular audit-event model capable of recording governance actions.

Initial event types should include:

- user record creation or update
- self-service compliance date update
- access assignment creation or update
- access inactivation
- reconciliation action application
- administrator assignment changes
- system catalog changes, as those workflows are introduced

The reference implementation may keep audit events in session-backed or file-backed demo storage, but the model should be designed for migration to a persistent append-oriented event store.

Audit history should support periodic access review and semiannual audit workflows.

### Expand automated tests

Broaden test coverage beyond the current reconciliation smoke tests.

Priority coverage should include:

- reconciliation matching and action classification
- single-system reconciliation scope
- compliance status calculations
- role and system scope logic
- audit-event generation
- export preparation
- data normalization and validation

Tests should focus first on business logic that can be exercised independently of Streamlit rendering.

### Add linting and formatting

Introduce a lightweight, documented code-quality baseline.

The repository should include automated checks for:

- formatting
- linting
- existing tests

The same checks should run in CI.

### Add structured logging

Replace ad hoc operational logging patterns with structured application logging.

The reference implementation should distinguish between:

- application logs
- governance audit events

Application logs support troubleshooting.

Audit events record meaningful governance actions.

Those concerns should not be treated as the same data stream.

### Define migration support

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

AccessAtlas 1.0.0 will represent the first clean deployable starter application.

The release does **not** require a hosted database or persistent public demo backend.

The public demo should continue to reset tester changes and remain inexpensive to operate.

The 1.0.0 release should include:

- modularized application structure
- clean separation of demo-specific and starter application behavior
- a starter version without the Demo Mode persona selector and demo sidebar structure
- data export capability
- broader automated test coverage
- audit logging and an initial audit-event model
- linting and formatting checks
- structured application logging
- documented migration extension points
- current README, changelog, roadmap, and architecture documentation

Deployment guidance is a stretch goal for 1.0.0.

Authentication integration, persistent production storage, notifications, provisioning, configurable compliance requirements, and complete governance-model configuration are not required for 1.0.0 unless explicitly moved into the release scope later.

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
