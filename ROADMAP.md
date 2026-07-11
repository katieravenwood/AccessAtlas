# AccessAtlas Roadmap

AccessAtlas is evolving from a functional reference application into a polished deployable starter for access-governance teams and data engineering organizations.

The project is intended to remain easy to evaluate, inexpensive to run, and straightforward to adapt. The public demo should demonstrate workflows without persisting tester changes or requiring a paid cloud backend.

This roadmap uses **Now / Next / Later** to describe product direction without committing to calendar dates.

## Product Direction

AccessAtlas is being developed for two primary audiences:

1. data engineering teams looking for a starter architecture for access governance; and
2. small and mid-sized organizations that need a practical access-governance application they can adapt.

AccessAtlas is not intended to become a full identity and access management platform.

Its focus is the governance layer around access:

- catalog users, systems, resources, and permissions
- track system administrator responsibility
- monitor governance requirements
- reconcile source-system access records
- preserve governance action history
- support periodic audits and access-review inputs
- provide extension points for identity, notifications, provisioning, and organization-specific workflows

Formal access approval remains outside the core application for now.

# Now

## Goal: Complete the 1.0.0 Public Reference Baseline

The core starter architecture is materially complete.

### Engineering foundation — Completed

- Dual-distribution modular architecture
- Separate public demo and clean starter runtimes
- Structured application logging
- Governance audit-event model
- Scoped CSV data exports
- Broader automated test coverage
- Ruff linting and formatting baseline
- Repository data-access boundary
- PostgreSQL and Snowflake migration contracts

### Release-readiness work — In progress

Current work is focused on:

- documentation alignment
- documentation information architecture
- application architecture diagrams
- governance and workflow diagrams
- application screenshots
- deployment guidance
- repository readiness files and templates
- final synthetic demo-data presentation review
- v1.0.0 release review

### 1. Align permanent documentation — Completed

Current-state documentation now uses the Generation 3 architecture and task-based application vocabulary.

The permanent documentation set distinguishes:

- product overview
- application architecture
- repository data-access contracts
- deployment guidance
- platform-specific repository implementation guidance
- governance patterns
- role-specific user guides

Historical terminology remains only where appropriate in `CHANGELOG.md`.

### 2. Add architecture and workflow diagrams — Next implementation step

Create version-controlled diagrams for:

- application architecture
- conceptual governance data model
- system access reconciliation
- starter/demo distribution
- repository replacement pattern

Prefer Mermaid source where GitHub rendering is appropriate.

Add exported SVG or PNG assets only where presentation or reuse requires them.

### 3. Capture application screenshots

Capture a restrained synthetic-data screenshot set covering:

- Dashboard
- My Access
- Managed Users
- Managed Systems
- access reconciliation queue
- training reconciliation
- Governance Audit History
- Demo Mode role preview
- direct access management

Feature only a representative subset in the README.

### 4. Complete repository readiness

Add or review:

- `CONTRIBUTING.md`
- `SECURITY.md`
- pull request template
- bug report issue template
- feature request issue template
- repository description and topics
- live demo link
- CI and license badges
- social preview asset
- branch protection and CI requirements

### 5. Perform v1.0.0 release review

Review the repository as a first-time adopter.

Confirm:

- clean installation
- stable entry points
- live demo behavior
- documentation links
- screenshots and diagrams
- CI status
- test suite
- generated root application synchronization
- current CHANGELOG
- current roadmap
- release notes

Then establish the public reference baseline for v1.0.0.

# Next

## Notification module

Notifications are the first functional priority after the 1.0.0 foundation.

The notification capability should be a modular starter component rather than a hard-coded email system.

The application should identify notification-worthy events such as:

- training expiring soon
- expired compliance
- reconciliation items awaiting review
- administrative coverage gaps
- future audit or access-review assignments

The preferred design is:

```text
AccessAtlas identifies notification event
        |
        v
notification record or event
        |
        v
pluggable delivery provider
```

Reference delivery patterns may include:

- email
- Microsoft Power Automate or Logic Apps
- webhook-based delivery
- other organization-specific services

## Lightweight system configuration

Allow authorized administrators to create and maintain governed systems through the application while preserving repository and audit boundaries.

## Access history and periodic review support

Build on inactive-record retention and audit events to support:

- access-history views
- semiannual or organization-defined review periods
- reviewer assignments
- review evidence
- retained-access decisions

Access review should remain conceptually distinct from reconciliation.

## Authentication extension pattern

Provide a pluggable identity integration pattern for deployments replacing `ACCESSATLAS_USER_ID`.

Reference guidance should cover OpenID Connect and enterprise identity concepts without making one provider a mandatory public dependency.

# Later

## Configurable governance model

Allow authorized administrators to configure:

- system categories and types
- resource types
- available permissions
- access models
- reconciliation mappings
- administrator roles

## Configurable compliance requirements

Replace fixed compliance fields with a configurable requirements model.

A future requirement may include:

```text
requirement_id
name
requirement_type
validity_period
warning_period
applicable system or category
applicable user type
record_status
```

This would support organization-defined:

- training
- certifications
- agreements
- acknowledgements
- recurring governance requirements

## Optional access approval module

A future optional module may demonstrate:

- access requests
- configurable reviewers
- approval and denial decisions
- approval history
- handoff to provisioning workflows
- separation of requester, approver, and administrator responsibilities

The module should remain optional so organizations with established approval systems can keep those processes.

## Provisioning integration patterns

Demonstrate how governance decisions can be handed to external provisioning services.

The initial objective is not universal automated provisioning.

Reference patterns should show how an organization could:

- request access enablement
- request access disablement
- send an action to an external service
- record the result
- reconcile the resulting source-system state

Governance state and provisioning execution should remain conceptually separate.

## Expanded source-system cataloging patterns

Continue supporting cataloging and reconciliation patterns for:

- CSV and file-based exports
- Snowflake roles and grants
- PostgreSQL permissions
- dashboard and report platforms
- collaboration platforms
- organization-specific source adapters

Direct provisioning and source-system control remain later concerns.
