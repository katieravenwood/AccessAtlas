# AccessAtlas System Administrator Guide

## Introduction

This guide provides an overview of the responsibilities and workflows available to System Administrators within AccessAtlas.

System Administrators are responsible for one or more governed systems that are tracked within AccessAtlas. They use the platform to review user access, monitor administrative coverage, support compliance activities, and participate in access reconciliation processes.

Unlike Super Administrators, System Administrators focus only on systems assigned to them and are not responsible for managing the overall governance platform.

---

## Responsibilities

Typical System Administrator responsibilities include:

* Reviewing access assignments within assigned systems
* Monitoring administrative coverage
* Supporting access reviews
* Participating in reconciliation activities
* Supporting compliance and audit requests
* Maintaining awareness of governance issues affecting assigned systems

System Administrators are generally not responsible for:

* Maintaining the Central User Registry
* Managing the Systems Catalog
* Managing platform-wide configuration
* Managing governance policies
* Administering the AccessAtlas application itself

---

## AccessAtlas Navigation

System Administrators primarily interact with the following sections:

1. Systems
2. System Admins
3. Compliance
4. Access Reconciliation

The Overview dashboard may also be used for general monitoring.

---

## Overview Dashboard

The Overview dashboard provides a summary of governance activity across the environment.

System Administrators may use the dashboard to:

* Monitor overall governance activity
* Review compliance summaries
* Review access assignment counts
* Monitor reconciliation activity

While useful for situational awareness, most day-to-day work occurs in the Systems and Access Reconciliation sections.

---

## Reviewing Assigned Systems

The Systems section is the primary workspace for System Administrators.

### Locate Your System

Select a system from the Systems Catalog.

Review:

* System Name
* System Type
* Access Model
* Resource Scope
* System Owner
* Administrative Group

### Review Users with Access

The Users with Access section displays:

* Users assigned to the system
* Resource-level assignments
* Permission assignments
* Access status information

Typical review questions include:

* Who currently has access?
* What permissions have been assigned?
* Are permissions appropriate for current business needs?

### Review Resources and Permissions

The Resources and Permissions section provides a summary of governed resources.

Examples include:

* Application roles
* Database permissions
* Platform roles
* Dashboards
* Collaboration sites

This view helps administrators understand how access is distributed within a system.

---

## Administrative Coverage

The System Admins section helps administrators verify governance accountability.

### Review Assigned Administrators

Administrators can review:

* Assigned administrators
* Administrative roles
* Assignment status

### Confirm Administrative Coverage

Administrative coverage should be reviewed periodically to ensure that:

* All systems have assigned administrators
* Administrative assignments remain current
* Responsibility is clearly defined

### Common Questions

Examples include:

* Who administers this system?
* Are there backup administrators?
* Are administrative assignments still valid?

---

## Supporting Access Reviews

Organizations often conduct periodic access reviews to validate user access.

AccessAtlas supports these reviews by providing:

* User inventories
* Permission inventories
* Resource-level access visibility
* Administrative accountability information

### Typical Access Review Activities

Review:

* Users with access
* Permissions assigned
* Resource assignments
* Access status

Identify:

* Access that is no longer required
* Access that appears inconsistent with business needs
* Missing governance records

Access changes are typically performed within source systems rather than within AccessAtlas.

---

## Compliance Monitoring

System Administrators may be asked to support compliance-related reviews.

### Review Compliance Status

Compliance information may include:

* Training completion
* Policy acknowledgement
* Agreement completion

### Monitor Follow-Up Items

Users with compliance issues may appear in follow-up queues.

Common statuses include:

* Current
* Expiring Soon
* Expired

### Supporting Compliance Activities

System Administrators may:

* Verify user assignments
* Assist with follow-up communications
* Support audit requests

Compliance enforcement processes vary by organization.

---

## Access Reconciliation

Access Reconciliation is one of the most important governance activities for System Administrators.

### Purpose

Over time, governance records may differ from actual system access.

Reconciliation identifies discrepancies between:

* Governance records
* Authoritative system exports

### Typical Workflow

#### Step 1: Obtain a Current Access Export

Examples include:

* Application user exports
* Platform role exports
* Database permission exports
* Dashboard access exports

#### Step 2: Upload the Export

Upload the export file using the expected reconciliation schema.

#### Step 3: Review Validation Results

Verify that:

* Required fields are present
* Records are loaded successfully

#### Step 4: Review Reconciliation Results

Results may include:

* New Access in Upload
* Access Not Found in Upload
* Status Changed
* No Change

#### Step 5: Review the Action Queue

Focus first on records requiring review.

Common follow-up activities include:

* Investigating unexpected access
* Confirming access removals
* Validating role changes
* Coordinating updates with governance teams

#### Step 6: Coordinate Remediation

AccessAtlas identifies discrepancies but does not directly modify source systems.

Any required changes should be performed through approved organizational processes.

---

## Supporting Audits

System Administrators frequently support:

* Internal audits
* Compliance reviews
* Access certification activities
* Governance assessments

AccessAtlas can assist by providing:

* Access inventories
* Permission inventories
* Administrative assignment records
* Reconciliation history

### Best Practices

When supporting audits:

* Review data before sharing
* Verify administrative assignments
* Validate system ownership information
* Ensure reconciliation activities are up to date

---

## Governance Best Practices

### Review Access Regularly

Periodically review users, permissions, and resource assignments.

### Maintain Administrative Coverage

Ensure systems have assigned administrators and backup coverage where appropriate.

### Participate in Reconciliation Activities

Regular reconciliation improves governance accuracy and reduces access drift.

### Escalate Governance Concerns

Report:

* Missing ownership
* Inactive administrative coverage
* Significant reconciliation discrepancies
* Potential compliance concerns

### Preserve Governance History

When access is no longer required, organizations should generally retain historical governance records rather than deleting them.

Inactive records provide important audit and reporting value.

---

## Troubleshooting

### Missing Users

Verify that the user exists within the Central User Registry.

### Missing Permissions

Verify that the permission exists within the authoritative source system.

### Missing Administrator Assignments

Review assignment records within the System Admins section.

### Upload Validation Errors

Verify that uploaded reconciliation files contain all required columns.

### Unexpected Reconciliation Results

Verify:

* User IDs
* System IDs
* Resource Names
* Permission Names
* Access Status Values

Differences in these values may cause reconciliation discrepancies.

---

## Summary

System Administrators use AccessAtlas to govern the systems for which they are responsible.

Their primary activities include:

* Reviewing user access
* Monitoring administrative coverage
* Supporting compliance reviews
* Participating in reconciliation activities
* Supporting governance and audit processes

These activities help maintain accurate, auditable, and trustworthy access records within the systems they administer.
