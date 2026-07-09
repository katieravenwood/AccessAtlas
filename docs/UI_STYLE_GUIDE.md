# AccessAtlas UI Style Guide

AccessAtlas uses a task-based interface for access governance workflows.

This guide records the shared AccessAtlas application's UI vocabulary and presentation conventions. It applies to the quick-start starter, modular starter, and hosted demo unless a rule is explicitly identified as demo-specific.

## Top-Level Navigation

Use the current task-oriented section names exactly:

- `Dashboard`
- `My Access`
- `Manage Access`
- `Access Reconciliation`
- `AccessAtlas App Admin`

The displayed selector may include icons when they improve scanning.

Do not reintroduce older top-level labels such as `Overview`, `Users`, `Systems`, `Review Changes`, or `Administration`.

## Section Vocabulary

Use the following current labels:

| Current Label | Purpose |
|---|---|
| My Record | Individual record view within My Access |
| Update My Certification and Agreement Dates | Self-service date update workflow |
| Managed Users | Scoped user review |
| User Management Registry | User registry table |
| Selected User Access Profile | Selected user detail |
| Managed Systems | Scoped system review |
| System Catalog | System registry table |
| Selected System Access Profile | Selected system detail |
| Edit / Add Access | Direct single-record access management |
| System Access Export File Upload | Access export reconciliation |
| Training Certificate Date and Agreement Reconciliation | Compliance-date reconciliation |
| Compliance Monitoring | Administrative compliance review |
| System Administrator Assignments | Administrative responsibility review |
| Governance Audit History | Current-session governance action review |

Prefer the exact application label when documentation refers to a visible screen or tab.

## Page Structure

Each major top-level section should generally follow this order:

1. Section title
2. One-sentence workflow caption
3. Summary metrics or visual summary, when useful
4. Primary work area
5. Supporting tables, cards, or detail views

Do not add headings solely to create visual weight.

## Heading Hierarchy

Use:

- `st.subheader()` for top-level application section titles
- `###` for major section blocks
- `####` for lower-level record or summary blocks
- `st.caption()` for workflow and filter instructions

Keep heading depth semantic.

## Guidance and Instruction Text

Use one sentence when one sentence will do.

Prefer:

> Filter the records below by compliance status, department, or user type.

Avoid:

> Please use the filters below in order to narrow down the records that are displayed.

Demo-specific language belongs only in the hosted demo runtime and must state clearly that Demo Mode simulates visibility or workflow behavior and is not authentication. The starter runtimes should not render Demo Mode warnings, persona selectors, or demo-only contextual guidance.

## Filters

Place filters directly under the section they affect.

Use horizontal filter rows when three or fewer related controls fit cleanly.

Use specific labels such as:

- `Filter by application role`
- `Filter by user type`
- `Filter by record status`
- `Filter by system type`
- `Filter by system category`

Do not use a standalone `Filters` heading unless the entire screen is a filter-focused workflow.

## Tables

User-facing tables should:

- use friendly display labels where practical
- hide row index values when the index has no user meaning
- use a consistent column order
- use `width="stretch"` for full-width tabular views unless content-width behavior is intentionally required
- remain detailed work surfaces rather than decorative summaries

Use `show_dataframe()` for standard read-only application tables when possible so table defaults remain centralized.

Editable tables may preserve internal field names in code where action logic depends on them.

## Metrics and Summaries

Use `st.metric()` for a small set of operational summary values.

Metrics should answer a clear governance question, such as:

- How many users are visible?
- How many systems are in scope?
- How many records need review?
- How many compliance records are expired or expiring?

Do not turn every count into a metric tile. A wall of tiles is merely a spreadsheet wearing cufflinks.

## Cards

Use selected-record cards for single-entity review.

Card titles should identify the selected record clearly.

Prefer tables or compact grouped summaries when many repeated cards would create excessive vertical length.

## Color Semantics

Use Streamlit status elements consistently:

- Success/green: current, compliant, successfully applied
- Warning/yellow: attention needed or expiring soon
- Error/red: expired, invalid, noncompliant, or blocked
- Info/blue: explanatory, scope, or demo-only guidance
- Neutral/gray: historical or inactive context

Do not rely on color alone to communicate status.

## Empty States

Empty-state text should explain why nothing is shown or what the state means.

Prefer:

> No records require follow-up for the selected filters.

Prefer:

> This system has no recorded administrator assignments.

Avoid:

> No records.

Avoid treating a valid empty state as an error.

## Reconciliation Workflows

Both reconciliation workflows should follow the same mental model:

1. Select or establish reconciliation scope
2. Upload or load external records
3. Validate the input
4. Compare external and current records
5. Summarize change types
6. Review the queue
7. Select applicable actions
8. Apply current-session updates
9. Review results

The queue should make the recommended action and change type easy to scan.

System access reconciliation must preserve single-system scope for missing-record/inactivation evaluation.

Use action language consistently:

- `Add access record`
- `Inactivate`
- `Update`

Historical records should be inactivated rather than deleted.

## Role-Aware Interface Rules

The current shared application section visibility is:

- User: My Access
- Manager: Dashboard, My Access, Manage Access, Access Reconciliation
- System Administrator: Dashboard, My Access, Manage Access, Access Reconciliation
- Super Administrator: all sections

System Administrator views must remain limited to administered-system scope.

User self-service must remain limited to the current user's own record.

The hosted demo uses synthetic personas to preview these rules. The starter runtime resolves a current application identity without rendering the demo selector.

These UI and reference scope rules are not a production authorization boundary. Production authorization belongs in the backend and data-access layer.

## Governance Audit History

Governance Audit History is an administrative review surface, not an operational application-log viewer.

Use it to show:

- event identity and time
- event type and action
- actor identity and role
- affected entity
- target user and system when applicable
- outcome
- source
- concise summary
- structured change detail

Keep the primary table scan-friendly. Detailed `changes_json` belongs in an event-level expander or detail view rather than the main table.

Do not mix structured application logs into Governance Audit History.

The reference UI should state clearly that audit history is session-backed. Production audit storage may require stronger immutability, retention, and access controls.


## Streamlit API Conventions

Use current Streamlit width parameters:

- `width="stretch"` in place of deprecated `use_container_width=True`
- `width="content"` in place of deprecated `use_container_width=False`

Centralize repeated display behavior in helpers where doing so improves consistency without obscuring the workflow.

Prefer small, explicit helpers over broad framework-like abstraction. Shared UI behavior belongs in the modular source; the generated single-file starter should remain readable after publishing.

## Documentation Alignment

When a visible UI label or runtime behavior changes, review at minimum:

- `README.md`
- `CHANGELOG.md`
- `ROADMAP.md` when roadmap status changes
- `docs/MODULAR_ARCHITECTURE.md` when entry points, runtime boundaries, or publishing behavior change
- `docs/UI_STYLE_GUIDE.md`
- user guides under `docs/user-guides/`
- implementation notes when the changed concept is architectural or data-related

The repository implementation is the source of truth for current labels. Historical design discussions explain why choices were made but should not preserve retired vocabulary in current-user documentation.
