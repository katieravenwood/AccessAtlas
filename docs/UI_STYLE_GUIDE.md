# AccessAtlas UX and UI Design Guide

AccessAtlas uses a task-based interface designed to make access-governance work understandable to users who may not think in terms of database entities or application architecture.

This guide catalogs the visual and interaction patterns used in the reference application, the vocabulary applied to key work areas, and the design rationale behind those choices. It is intended for UX/UI designers, product owners, and developers extending the application.

## Design Principles

### Organize around user tasks

The interface groups work by what the user is trying to accomplish rather than by the names of underlying tables.

For example, `Manage Access` groups user review, system review, and direct access maintenance because these activities support one operational objective. This replaces an entity-first navigation model such as `Users`, `Systems`, and `Access`.

The task-based structure reduces the need for users to understand the physical data model before they can navigate the application.

### Keep scope visible

AccessAtlas is role-aware and record-scope-aware. A user may see only their own record, themselves and direct reports, systems they actively administer, or the complete governance dataset.

The interface should help users understand the context of the records shown without presenting role mechanics as a technical security model.

### Prefer direct review surfaces

Governance work often requires scanning, filtering, comparing, and confirming records. AccessAtlas therefore favors compact metrics, visible summary tables, filterable registries, detail profiles, review queues, and explicit action controls.

Decorative visualization is secondary to readable operational data.

### Separate review from action

Where possible, AccessAtlas visually distinguishes reviewing current state from applying a governance change.

Examples include User Management Registry versus Edit / Add Access, reconciliation comparison versus Apply current-session updates, and Governance Audit History versus the workflow that originally created the event.

This reduces accidental changes and makes workflow intent clearer.

### Use explicit governance language

Labels describe the governance action being taken. Examples include `Inactivate`, `Add access record`, `Update`, `Access Reconciliation`, and `Governance Audit History`.

The application avoids softer or ambiguous action labels when the governance meaning is important.

## Information Architecture

The current top-level navigation is:

| Section | User question answered | Design purpose |
| --- | --- | --- |
| Dashboard | What needs attention in my current scope? | Summary and orientation |
| My Access | What does AccessAtlas know about me and my access? | Individual self-service |
| Manage Access | Which users, systems, and access assignments am I responsible for? | Operational access management |
| Access Reconciliation | Does the governance inventory match an external source? | Comparison and corrective action |
| AccessAtlas App Admin | How is the governance model administered and evidenced? | Super Administrator functions |

The current navigation deliberately avoids using `Users`, `Systems`, or `Administration` as top-level destinations. Those labels describe data entities; the current structure describes user goals.

## Application Vocabulary

### Personal access

| Visible label | Meaning |
| --- | --- |
| My Access | Individual access-governance area |
| My Record | Current user's profile, compliance, access, and administrator assignments |
| Update My Certification and Agreement Dates | Self-service compliance-date maintenance |

### Access management

| Visible label | Meaning |
| --- | --- |
| Manage Access | Task area for scoped access-governance work |
| Managed Users | User review area within the current role scope |
| User Management Registry | Filterable user table |
| Selected User Access Profile | Detailed view of one user |
| Managed Systems | System review area within the current role scope |
| System Catalog | Filterable governed-system table |
| Selected System Access Profile | Detailed view of one system |
| Edit / Add Access | Direct maintenance area |
| Add / Edit Access | Access-assignment maintenance workflow |
| Add User | User-record creation workflow |

### Reconciliation

| Visible label | Meaning |
| --- | --- |
| Access Reconciliation | Comparison and corrective-action area |
| System Access Export File Upload | One-system access export comparison |
| Training Certificate Date and Agreement Reconciliation | Compliance-date comparison |
| Reconciliation Queue | Review surface for identified differences |
| Recommended Action | Suggested governance response |
| Reconciliation Results | Record of actions applied in the current workflow |

### Administration

| Visible label | Meaning |
| --- | --- |
| AccessAtlas App Admin | Super Administrator governance area |
| Compliance Monitoring | Organization-wide compliance review |
| System Administrator Assignments | Administrative responsibility review |
| Governance Audit History | Governance action history |

### Governance actions and states

| Term | Use |
| --- | --- |
| Active | Current governance record or assignment |
| Inactive | Retained record that is no longer current |
| Current | Compliance requirement is within validity period |
| Expiring Soon | Compliance requirement is approaching expiration |
| Expired | Compliance requirement is outside the validity period |
| Add access record | Create a governance access assignment |
| Inactivate | Retain the assignment while ending current access status |
| Update | Change an existing governance record |
| No action | Difference does not require a governance change |

`Inactivate` is used instead of `Delete`, `Remove`, or `Terminate` because the reference governance model preserves historical context.

## Page Composition

AccessAtlas uses a consistent page rhythm:

```text
Section title
    ↓
Short workflow explanation
    ↓
Summary metrics or source summaries
    ↓
Primary work surface
    ↓
Selected-record or result detail
```

This structure is intentionally simple. The application is designed for operational review rather than dashboard storytelling.

### Section titles

Top-level application sections use `st.subheader()`. Major content blocks use third-level headings, and lower-level record or summary areas use fourth-level headings.

The heading hierarchy should communicate information structure rather than visual emphasis alone.

### Captions and guidance

Short captions are used immediately above the controls or data they explain.

Example:

> Filter the records below by compliance status, department, or user type.

Guidance text is kept brief and procedural. Demo-only explanatory text is reserved for the hosted demo runtime.

## Dashboard Style

The Dashboard is an orientation and exception-awareness surface.

### Metric tiles

`st.metric()` is used for a small set of high-value counts. Current examples include Visible Users, Visible Systems, Access Records, Items Needing Review, Expired / Expiring Compliance, Pending Reconciliation Actions, and Active Compliance Follow-Up.

Metrics are not intended to repeat every table count.

### Access Management Summary Stats

The supporting source summaries appear directly under `Access Management Summary Stats`.

Current tables are:

- User Record Status
- Compliance Status
- Access Records by System Type
- Access Records by Resource Type
- Access Records by Access Status

These are shown as compact tables rather than bar charts. The design choice is intentional: exact category values are more useful to governance reviewers than decorative visual comparison.

## Table and Registry Style

Tables are the primary AccessAtlas work surface.

### Standard presentation

Read-only tables generally use the shared `show_dataframe()` presentation helper.

Current table conventions include full-width display where appropriate, hidden technical row indexes, stable column order, friendly display labels where practical, and compact, readable record density.

### Registries

A registry is a filterable master review table.

Current registries are `User Management Registry` and `System Catalog`.

Registries support broad scanning and selection. The detailed profile for the selected record is presented separately below the table. This avoids forcing every available field into one oversized grid.

### Filters

Filters appear close to the table or workflow they affect. Related filters are placed in a horizontal row when the page width supports it.

Examples include `Filter by application role`, `Filter by user type`, and `Filter by record status`.

Labels identify the field or concept being filtered rather than using generic labels such as `Filter 1`.

## Selected Record Profiles

AccessAtlas uses selected-record profiles to move from broad review to detailed governance context.

### Selected User Access Profile

The user profile consolidates governance identity information, organizational context, compliance dates, compliance status, access assignment metrics, detailed access assignments, and system administrator assignments.

The profile is intended to answer:

> What is the full governance context for this user?

### Selected System Access Profile

The system profile consolidates system type and category, ownership and administrator group, resource scope, access model, tracking method, users with access, system administrators, and resources and permissions.

The profile is intended to answer:

> How is this system governed and who currently has access?

## Reconciliation Workflow Style

Reconciliation is presented as a review-and-apply workflow.

```text
Select scope
    ↓
Upload source data
    ↓
Validate
    ↓
Compare
    ↓
Review queue
    ↓
Select actions
    ↓
Apply updates
    ↓
Review results
```

### Scope first

For system access reconciliation, the system is selected before upload. This makes the comparison boundary explicit and supports correct inactivation evaluation.

### Summary before queue

Compact summary information is shown before the detailed Reconciliation Queue. The user first understands the scale of the comparison, then reviews individual differences.

### Reconciliation Queue

The queue is a dense operational table. Key columns are ordered to support action review:

```text
Apply?
Recommended Action
Change Type
User identifiers and names
System identifiers and name
Change detail
```

The exact table contains additional comparison fields where needed. Recommended Action is intentionally placed near the action-selection control.

### Action labels

Reconciliation uses governance verbs:

```text
Add access record
Inactivate
Update
No action
```

### Results

After selected actions are applied, Reconciliation Results explain what happened to each reviewed record. The results surface is distinct from the original comparison queue.

## Compliance Presentation

Compliance uses three text statuses:

```text
Current
Expiring Soon
Expired
```

The interface does not rely on color alone. Status text remains visible in tables and summary content.

The reference application uses styling to support rapid scanning, but the status label carries the meaning.

Compliance Monitoring combines summary metrics, filtered detail, follow-up records, department summaries, and user-type summaries. The design favors operational follow-up rather than compliance visualization for its own sake.

## Audit History Presentation

Governance Audit History is a review surface for meaningful governance actions.

The current design includes Audit Events, Event Types, and Actors metrics; event type, action, and outcome filters; a newest-first event table; and selected-event Change Detail.

The primary table presents human-readable event context. Serialized change detail is shown only when a specific event is selected. This prevents raw change payloads from overwhelming the main review surface.

## Export Controls

Exports appear in the context of the data being reviewed.

Examples include `Download Filtered Users CSV`, `Download Filtered Systems CSV`, and `Download Scoped Access Assignments CSV`.

This pattern communicates both what will be exported and which current scope or filters apply.

AccessAtlas does not use a generic `Export Everything` page. The placement of export controls reinforces the principle that data portability should follow the same governance context as on-screen review.

## Empty States and Exceptions

Valid empty results are explained in plain language.

Examples:

> No systems are available in the current application scope.

> No governance actions have been recorded in the current session.

The interface distinguishes a valid empty state from an application error. A missing record or out-of-scope result should not look like a traceback or technical failure.

## Demo and Starter Presentation

The public demo and clean starter share the same application workflows but use different presentation context.

### Hosted demo

The hosted demo includes a Demo Mode explanation, synthetic persona selector, Current Demo User context, Visible Demo Scope context, and contextual demo guidance.

These elements help a reviewer understand role and scope behavior.

### Clean starter

The starter omits Demo Mode warnings, the persona selector, Current Demo User panel, Visible Demo Scope panel, and demo-only contextual guidance.

This distinction keeps the starter suitable for adaptation while preserving a clear public demonstration experience.

## Accessibility and Interaction Standards

AccessAtlas uses native Streamlit controls and semantic heading hierarchy wherever practical.

The interface should provide text labels for status and action meaning, avoid communicating state through color alone, use explicit control labels, keep controls close to the records they affect, preserve readable table column names, provide meaningful empty-state text, and maintain predictable section order.

Where styling is used, it supports scanning rather than replacing text meaning.

## Screenshot and Documentation Presentation

Reference screenshots should use the hosted demo or `modular/demo_app.py`.

Screenshots should contain synthetic data only, use a stable persona appropriate to the screen, use desktop-width presentation, show the complete section title and main work surface, omit browser chrome when it adds no explanatory value, avoid debug or traceback states, and avoid local filesystem paths, secrets, tokens, or private organization information.

The planned reference set is:

```text
01-dashboard.png
02-my-access.png
03-managed-users.png
04-managed-systems.png
05-access-reconciliation-queue.png
06-training-reconciliation.png
07-governance-audit-history.png
08-demo-role-preview.png
09-direct-access-management.png
```

The README should use only a representative subset.

## Design System Summary

| Design element | AccessAtlas pattern |
| --- | --- |
| Navigation | Task-based |
| Primary work surface | Filterable tables and registries |
| Detail pattern | Selected record profile |
| Summary pattern | Metric tiles and compact source tables |
| Action pattern | Explicit governance verbs |
| Review pattern | Queue before apply |
| History pattern | Inactive records plus governance audit events |
| Export pattern | Contextual and scope-aware |
| Demo pattern | Synthetic persona and visible scope context |
| Starter pattern | Clean task-based workflow without demo framing |
| Status communication | Text-first; styling supports scanning |
| Persistence language | Repository-backed; reference repositories are session-backed |
| Security language | UI scope demonstrates behavior but is not authorization |

## Design Evolution

The current interface evolved from an entity-oriented design toward a task-oriented model.

Earlier concepts such as `Overview`, `Users`, `Systems`, `Review Changes`, and `Administration` were replaced because they reflected the application's underlying records more than the user's work.

The current vocabulary groups related governance activities into `Dashboard`, `My Access`, `Manage Access`, `Access Reconciliation`, and `AccessAtlas App Admin`.

This task-based structure is the current reference point for future UX work unless user research or a major workflow change supports a different information architecture.
