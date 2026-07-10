# AccessAtlas Super Administrator Guide

This guide describes the current AccessAtlas experience for the **Super Administrator** application role.

The Super Administrator can review the complete governance dataset available to the active repository container and can access all application sections.

## Super Administrator Role Scope

The Super Administrator can access:

```text
Dashboard
My Access
Manage Access
Access Reconciliation
AccessAtlas App Admin
```

The reference role-scope model does not limit the Super Administrator to a specific manager or administered-system assignment.

A production deployment should still enforce Super Administrator authorization below the UI.

## Dashboard

The Dashboard provides an organization-wide summary of the repository data available to the current runtime.

Metrics include:

- Visible Users
- Visible Systems
- Access Records
- Items Needing Review
- Expired / Expiring Compliance
- Pending Reconciliation Actions
- Active Compliance Follow-Up

`Access Management Summary Stats` contains:

- User Record Status
- Compliance Status
- Access Records by System Type
- Access Records by Resource Type
- Access Records by Access Status

## My Access

My Access provides the Super Administrator's own governance record.

Use:

- **My Record** to review profile, compliance, access, and administrative assignments.
- **Update My Certification and Agreement Dates** to update the current user's reference compliance dates.

## Manage Access

### Managed Users

Managed Users provides the complete visible User Management Registry.

Use filters for:

- application role
- user type
- record status

Select a user to review the Selected User Access Profile.

The profile includes:

- user governance information
- training and agreement dates
- access metrics
- detailed access assignments
- system administrator assignments

The filtered user dataset can be exported as CSV.

### Managed Systems

Managed Systems provides the complete visible System Catalog.

Use filters for:

- system type
- system category
- record status

Select a system to review the Selected System Access Profile.

The profile includes:

- system owner and administrator group
- resource scope
- access model
- tracking method
- users with access
- system administrators
- resources and permissions

The filtered system dataset can be exported as CSV.

### Edit / Add Access

This work area contains:

```text
Add / Edit Access
Add User
```

#### Add / Edit Access

Create a new access assignment or edit an existing assignment.

Access assignments model:

```text
User -> System -> Resource -> Permission
```

Successful creates and updates are persisted through the active Access Assignment repository and recorded as governance audit events.

Scoped access assignments can be exported as CSV.

#### Add User

Create a new user governance record and, where applicable, an initial access assignment.

User creation is persisted through the active User repository and recorded as a governance audit event.

## Access Reconciliation

### System Access Export File Upload

The Super Administrator can reconcile any visible governed system.

The workflow is:

1. Select one system.
2. Upload a complete source-system access export.
3. Validate required fields and selected-system scope.
4. Review uploaded records.
5. Generate the comparison.
6. Review summary statistics and the Reconciliation Queue.
7. Select actions.
8. Apply selected actions.
9. Review action results.

Recommended actions are:

```text
Add access record
Inactivate
Update
No action
```

Reconciliation results can be exported as CSV.

### Training Certificate Date and Agreement Reconciliation

This workflow compares external user compliance dates with the current user repository.

It evaluates:

- annual training date
- biennial training date
- access agreement date

Selected actions may update compliance dates or inactivate user records.

Training reconciliation results can be exported as CSV.

## AccessAtlas App Admin

AccessAtlas App Admin contains three administrative work areas.

### Compliance Monitoring

Compliance Monitoring provides organization-wide compliance review.

Use it to review:

- current, expiring, and expired compliance counts
- active records requiring follow-up
- filtered compliance detail
- follow-up records
- summary views by department and user type

Available exports include filtered compliance detail and compliance follow-up records.

### System Administrator Assignments

This work area reviews administrative responsibility.

Use filters for:

- administrator role
- assignment status
- system type
- system category

The current UI supports:

- System Administrator Assignments
- Admin Record Review
- System Record Review
- Admin Coverage by System
- All System Administrator Assignments

Administrator assignment data can be exported as CSV.

### Governance Audit History

Governance Audit History reviews meaningful governance actions recorded through the active AuditStore.

The current reference view includes:

- Audit Events
- Event Types
- Actors

Filters are available for:

- event type
- action
- outcome

The event table is newest-first.

Select an event to review Change Detail.

Governance audit history can be exported as CSV.

The reference `SessionAuditStore` is disposable and is not a production immutable audit repository.

## Operational Logging vs Audit Events

These records have different purposes.

```text
Application logging
    How is the software behaving?

Governance audit events
    What governance action happened to a governed record?
```

Super Administrators review governance audit events in the application.

Operational logs remain in the Streamlit process or hosting environment.

## Data Exports

AccessAtlas places exports in the workflow where each governed dataset is reviewed.

Current export surfaces include:

- filtered users
- filtered systems
- scoped access assignments
- administrator assignments
- compliance detail
- compliance follow-up
- access reconciliation results
- training reconciliation results
- governance audit history

Exports preserve current role scope and active filters.

Successful exports generate an operational application event and a governance audit event without copying exported row contents into those event streams.

## Reference Repository Behavior

The default public reference repositories are:

```text
CSV-seeded
session-backed
disposable
```

Current-session changes do not modify the source CSV files.

A persistent deployment can replace the repository factory with PostgreSQL, Snowflake, or another implementation.

## Production Administration Note

The Super Administrator role is powerful.

Production deployments should define:

- approved identity and authentication
- explicit assignment of Super Administrator authority
- backend authorization
- persistent repository permissions
- audit-event retention
- operational monitoring

Do not rely on the visible Streamlit role selector or hidden controls as a production security boundary.
