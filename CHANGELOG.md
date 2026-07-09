# Changelog

All notable changes to AccessAtlas are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

AccessAtlas has not yet published a tagged release. The dated sections below reconstruct the project's pre-1.0 development history from repository commits and documented design decisions. They are development milestones, not retroactive release versions.

## [Unreleased]

### Added

- Canonical modular application source under `modular/`.
- Shared application core in `modular/accessatlas/app_core.py`.
- `RuntimeContext` contract for resolved identity, role-visible sections, scoped governance datasets, runtime type, and optional runtime-specific guidance.
- Clean starter runtime in `modular/accessatlas/starter_runtime.py`.
- Hosted demo runtime in `modular/accessatlas/demo_runtime.py`.
- Separate modular entry points:
  - `modular/app.py` for the clean starter
  - `modular/demo_app.py` for the hosted role-preview demo
- `ACCESSATLAS_USER_ID` starter identity configuration placeholder.
- `tools/build_single_file.py` for publishing the root single-file starter from canonical modular source.
- `python tools/build_single_file.py --check` synchronization validation.
- Automated tests verifying:
  - generated root `app.py` remains synchronized with modular source
  - generated and modular Python sources compile
  - the starter distribution does not contain Demo Mode controls
  - the hosted demo retains the persona selector and visible-scope preview
  - starter and demo entry points select distinct runtime factories
- `docs/MODULAR_ARCHITECTURE.md` documenting the dual-distribution and starter/demo runtime model.
- Current-state README documentation aligned to the task-based application structure.
- `docs/UI_STYLE_GUIDE.md` documenting current navigation vocabulary, screen hierarchy, table conventions, status semantics, empty states, reconciliation patterns, and Streamlit UI conventions.

### Changed

- Reframed `modular/` as the canonical engineering source while keeping root `app.py` as the easy quick-start distribution.
- Generalized role-scope logic from demo-specific naming to application-level scope behavior.
- Moved synthetic persona selection, Demo Mode warnings, demo-user summaries, visible demo scope, and contextual demo sidebar guidance into the hosted demo runtime.
- Removed Demo Mode controls and demo-specific sidebar structure from the starter runtime and generated root application.
- Updated the single-file build process to publish only the clean starter runtime.
- Updated CI to verify single-file synchronization before running tests.
- Updated data-path discovery so root and modular distributions use the same repository-level `data/` directory.
- Documentation now treats the repository implementation as the source of truth for current application labels and capabilities.
- README navigation and role descriptions remain aligned to:
  - Dashboard
  - My Access
  - Manage Access
  - Access Reconciliation
  - AccessAtlas App Admin
- README now documents the quick-start starter, modular starter, and hosted demo as distinct run paths.
- Repository structure documentation now includes `modular/`, build tooling, runtime-separation tests, roadmap, and modular architecture documentation.
- Future-direction documentation was revised to remove completed modularization and demo/starter separation work.

### Fixed

- Prevented demo-only persona and sidebar behavior from leaking into the generated quick-start starter.
- Added synchronization checks to prevent root `app.py` from silently drifting from canonical modular source.

---

## Pre-1.0 Development History

> The sections below are historical development milestones reconstructed from commit history. They are not tagged releases.

## 2026-07-08 — UI Modernization and Reconciliation Expansion

### Added

- Training certificate date and access agreement reconciliation workflow.
- Training reconciliation queue, action application behavior, and reconciliation results review.
- Additional user-management workflow support, including add-user behavior in Manage Access.
- Managed Systems guidance describing common access-governance patterns across applications, data platforms, databases, dashboards, hosting sites, and collaboration sites.

### Changed

- Limited system access reconciliation to one selected system so missing-record evaluation and inactivation recommendations remain correctly scoped.
- Reorganized Access Reconciliation layout around distinct reconciliation workflows.
- Reformatted Manage Access filters and nested workflows for faster review.
- Refactored the interface to current Streamlit conventions.
- Replaced deprecated `use_container_width` usage with current `width` behavior.
- Standardized read-only dataframe display defaults around `width="stretch"`.
- Improved defensive empty-state handling for administrator and system review selectors.
- Simplified reconciliation session-state initialization.
- Revised Demo Mode warning language to state clearly that simulated role visibility is not authentication.
- Removed Generic Access Model Examples from the System Catalog body and moved the concepts into Managed Systems guidance.
- Continued UI consistency refinements across section titles, nested tabs, captions, filters, tables, and help text.

### Fixed

- Corrected dataframe width behavior and duplicate width-argument issues.
- Added safeguards for empty administrator and system selector option sets.

---

## 2026-07-07 — Dashboard and Task-Based UI Refinement

### Added

- Dashboard visual summaries for:
  - compliance status
  - user record status
  - access records by system type
  - access records by resource type
  - access records by access status
- Dashboard visual-description documentation.
- Nested task-oriented tabs within major application sections.

### Changed

- Refactored Dashboard from a table-heavy overview into a visual operational summary.
- Updated the interface for nested workflows and task-based navigation.
- Updated Pandas dependency requirements for the active application environment.
- Continued migration away from entity-first navigation toward day-to-day governance tasks.

---

## 2026-06-24 — Task-Based Application Structure and Direct Access Management

### Added

- Direct single-record access add/edit workflow.
- Scoped access management for System Administrators.
- Additional synthetic administrator examples in sample data.
- Archived copy of the earlier full governance display implementation for historical reference.

### Changed

- Reorganized the application around task-based top-level navigation.
- Consolidated user review, system review, and direct access management under Manage Access.
- Streamlined the interface and user workflows.
- Grouped detailed work surfaces under focused nested sections instead of exposing every governance entity as a top-level screen.
- Updated README documentation for the revised application structure.

---

## 2026-06-19 — Reconciliation Action Queue and PostgreSQL Path

### Added

- Reconciliation Action Queue for access export differences.
- Selectable application of recommended reconciliation actions.
- Session-state-backed handling for:
  - Add access record
  - Inactivate
  - Update
- Reconciliation action results.
- `POSTGRES_NOTES.md` with PostgreSQL-oriented schema, indexing, write-back, transaction, and authorization considerations.

### Changed

- Moved demo guidance into the sidebar where context could follow the selected application section.
- Expanded README documentation to reference the PostgreSQL implementation path.
- Preserved inactive access history rather than deleting reconciled records.

---

## 2026-06-17 — Role-Aware Visibility and My Access Self-Service

### Added

- Role-based top-level section visibility in Demo Mode.
- My Record individual governance profile.
- Self-service training and agreement date update behavior.
- System Administrator scoped user and system views.
- Additional synthetic data supporting administrator-scoping demonstrations.
- Reconciliation smoke-test normalization and stronger assertions.

### Changed

- Demo Mode began scoping visible records by selected synthetic user role.
- User-role visibility was limited to the individual's own governance record.
- System Administrator visibility was limited to users and systems within administered-system scope.
- Self-service updates were kept in Streamlit session state rather than source CSV files.
- Reconciliation testing was made more robust around key-column normalization.

---

## Earlier 2026 — AccessAtlas Generic Reference Implementation

### Added

- Streamlit reference application for centralized access governance.
- Synthetic CSV-backed data model for:
  - users
  - systems
  - access assignments
  - system administrator assignments
  - sample reconciliation exports
- User registry and user-centered governance profiles.
- System catalog and system-centered governance profiles.
- Compliance monitoring for annual training, biennial training, and access agreement dates.
- System administrator assignment review.
- Upload-based access reconciliation.
- Source-system record traceability through optional `source_system_record_id`.
- Snowflake implementation notes and migration guidance.
- MIT license.
- Initial documentation and runnable dependency definition.

### Changed

- Generalized an organization-specific access-governance concept into the platform-neutral AccessAtlas reference application.
- Reframed the project as a platform-neutral reference implementation rather than an organization-specific production application.
- Expanded the governance model beyond a single surveillance environment to support applications, databases, cloud data platforms, dashboards, collaboration sites, and other managed resources.
- Standardized access relationships around:

  `User -> System -> Resource -> Permission`

- Standardized administrative responsibility around:

  `User -> System -> Administrative Role`

- Adopted audit-friendly inactive-record handling for users and access assignments.
- Established system-level administrator assignments, including support for administrators assigned to multiple systems.
- Established a single-file `app.py` as the current reference implementation after exploratory modularization work.

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

### Changed

- Expanded the governance model to support multiple system and resource types rather than a single technology pattern.
- Added separate tracking of user access assignments and system administrator responsibilities.
- Standardized resource-level access relationships around:
  - User
  - System
  - Resource type
  - Resource name
  - Permission
- Added upload-based reconciliation for environments where direct source-system integration is unavailable or inappropriate.
- Scoped missing-record evaluation to the system being reconciled so inactivation recommendations are based on a complete comparison set.
- Adopted inactive-not-delete handling to preserve historical access context.
- Separated reconciliation discrepancy handling from external access approval processes.
- Added role-aware experiences for:
  - User
  - Manager / Access Reviewer
  - System Administrator
  - Super Administrator
- Added self-service compliance date maintenance.
- Added system-scoped administration.
- Added direct access add/edit workflows for authorized administrative roles.
- Added synthetic users, systems, access assignments, administrator assignments, and reconciliation inputs suitable for a public reference implementation.

---

## Changelog Maintenance

Going forward:

- Add user-visible or behaviorally meaningful changes under `[Unreleased]`.
- Use the categories `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security` where applicable.
- Move `[Unreleased]` entries into a versioned section when a release is tagged.
- Use semantic versioning for published releases.
- Do not create retroactive version numbers for the pre-1.0 milestones above.
- Link version headings to GitHub comparisons after the first tagged release exists.
