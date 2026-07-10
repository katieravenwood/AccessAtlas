# AccessAtlas Manager Guide

This guide describes the current AccessAtlas experience for the **Manager** application role.

AccessAtlas does not currently implement a formal retained-access review module. The Manager experience provides governance inventory and reconciliation context that may support an organization's separate access-review process.

## Manager Role Scope

A Manager can access:

```text
Dashboard
My Access
Manage Access
Access Reconciliation
```

The current role-scope model provides visibility to:

- the Manager's own user record
- direct reports
- access assignments associated with visible users
- systems associated with the visible user and access scope
- administrator assignments associated with the visible scope

The Manager role does not receive direct access-maintenance controls.

## Dashboard

![AccessAtlas Dashboard](docs/images/screenshots/01-dashboard.png)

The Dashboard summarizes the current visible scope.

Metrics include:

- Visible Users
- Visible Systems
- Access Records
- Items Needing Review
- Expired / Expiring Compliance
- Pending Reconciliation Actions
- Active Compliance Follow-Up

`Access Management Summary Stats` provides source summary tables for:

- User Record Status
- Compliance Status
- Access Records by System Type
- Access Records by Resource Type
- Access Records by Access Status

## My Access

My Access provides the Manager's own governance record.

Use:

- **My Record** to review profile, compliance, access, and administrator assignments.
- **Update My Certification and Agreement Dates** to maintain the current user's reference compliance dates.

See the [User Guide](user-guide.md) for the My Access self-service workflow.

## Manage Access

### Managed Users

![Managed Users](docs/images/screenshots/05-managed-users.png)

Managed Users provides the scoped User Management Registry.

Use the filters to narrow records by:

- application role
- user type
- record status

Select a visible user to review the Selected User Access Profile.

The profile includes:

- user governance information
- training and agreement information
- access assignment metrics
- detailed access assignments
- system administrator assignments

### Managed Systems

![Managed Systems](docs/images/screenshots/04-managed-systems.png)

Managed Systems provides the scoped System Catalog.

Select a visible system to review the Selected System Access Profile, including:

- system attributes
- owner and administrator group
- resource scope
- access model
- users with access
- system administrators
- resources and permissions

### Edit / Add Access

Direct add/edit access management is not available to the Manager role.

The section is intended for System Administrators and Super Administrators.

## Access Reconciliation

![Access Reconciliation](docs/images/screenshots/06-access-reconciliation-queue.png)

The Manager role can inspect scoped reconciliation information.

### System Access Export File Upload

This workflow compares a complete export for one selected system with current AccessAtlas access assignments.

The comparison may identify:

- access in the source but not in AccessAtlas
- active AccessAtlas access missing from the source
- access-status differences

Recommended actions are:

```text
Add access record
Inactivate
Update
No action
```

### Training Certificate Date and Agreement Reconciliation

This workflow compares external compliance dates with current user records.

It evaluates:

- annual training date
- biennial training date
- access agreement date

## Supporting Access Review Activities

Reconciliation and access review are different.

```text
Reconciliation
    Does the governance record match the source?

Access review
    Should the user still retain the access?
```

AccessAtlas currently implements reconciliation.

A Manager may use:

- user access profiles
- system profiles
- compliance status
- access history retained through inactive records
- reconciliation results

as input to an organization's separate access-review process.

Formal retained-access decisions and approval workflows remain outside the current core application.

## Manager Limitations

The current Manager role cannot:

- create or edit access assignments
- add users through direct maintenance controls
- access AccessAtlas App Admin
- administer system administrator assignments
- review Governance Audit History

## Demo Mode Note

The hosted demo simulates Manager scope and visibility with synthetic data.

It is not authentication or backend authorization.
