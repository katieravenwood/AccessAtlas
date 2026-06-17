# AccessAtlas Super Administrator Guide

## Introduction

This guide provides an overview of the responsibilities and workflows available to Super Administrators within AccessAtlas.

Super Administrators are responsible for maintaining the governance platform itself. They oversee user records, system records, administrator assignments, compliance monitoring, and reconciliation activities across all tracked systems.

Unlike System Administrators, whose responsibilities are limited to specific systems, Super Administrators have visibility across the entire governance environment.

---

## Responsibilities

Typical Super Administrator responsibilities include:

* Maintaining the central user registry
* Maintaining the systems catalog
* Managing administrative assignments
* Monitoring compliance status
* Reviewing reconciliation results
* Coordinating governance reporting
* Supporting governance audits
* Monitoring overall platform data quality

---

## AccessAtlas Navigation

The application is organized into six primary sections:

1. Overview
2. Users
3. Systems
4. System Admins
5. Compliance
6. Access Reconciliation

Each section supports a different governance workflow.

---

## Overview Dashboard

The Overview dashboard provides a high-level summary of governance activity across the platform.

The dashboard displays:

* Total users
* Tracked systems
* Access assignments
* System administrator assignments
* Compliance status summaries
* User record status summaries
* Access assignment summaries

### Typical Uses

Super Administrators may use the dashboard to:

* Monitor overall governance activity
* Identify compliance issues
* Review access growth trends
* Verify administrative coverage

---

## User Registry Management

The Users section provides access to the Central User Registry.

### Typical Activities

#### Review User Information

Administrators can review:

* User identifiers
* Contact information
* Departments
* Managers
* User types
* Compliance status

#### Review User Access

Administrators can:

* View all access assignments for a user
* Review systems accessed
* Review assigned permissions
* Review administrator assignments

#### Review User Governance Profile

The User Governance Profile provides a consolidated view of:

* User information
* Access metrics
* Compliance status
* Administrative responsibilities

### Common Super Admin Questions

Examples include:

* What systems does a user have access to?
* Is the user compliant with required training?
* Who manages the user?
* Which systems does the user administer?

---

## Systems Catalog Management

The Systems section provides access to the Systems Catalog.

### Typical Systems Catalog Management Activities

#### Review System Information

Administrators can review:

* System type
* System category
* Access model
* Tracking method
* System owner
* Administrative group

#### Review Access Assignments

Administrators can:

* View all users with access
* Review permissions assigned
* Review resource-level access

#### Review Administrative Coverage

Administrators can:

* Identify assigned administrators
* Verify ownership coverage
* Review governance accountability

### Common Questions

Examples include:

* Who has access to this system?
* Which permissions exist within this system?
* Who administers the system?
* Does the system have assigned ownership?

---

## Administrative Assignment Management

The System Admins section provides visibility into administrative responsibility.

### Typical Administrative Assignment Management Activities

#### Review Administrator Assignments

Administrators can:

* View administrator assignments
* Review assignment status
* Review assignment history

#### Review Coverage

Administrators can:

* Identify systems with assigned administrators
* Identify systems lacking administrative coverage

### Common Administrator Assignment Review Questions

Examples include:

* Who administers a specific system?
* Which systems are managed by a specific administrator?
* Are there systems without administrative coverage?

---

## Compliance Monitoring

The Compliance section provides visibility into governance-related compliance requirements.

### Compliance Statuses

AccessAtlas supports:

* Current
* Expiring Soon
* Expired

### Typical Administrator Assignment Review Activities

#### Monitor Compliance

Administrators can:

* Review compliance summaries
* Monitor upcoming expirations
* Identify overdue requirements

#### Review Follow-Up Queue

Administrators can:

* Identify active users requiring attention
* Prioritize remediation activities

#### Analyze Trends

Administrators can review compliance summaries by:

* Department
* User Type

### Common Administrator Compliance Review Questions

Examples include:

* Which users require follow-up?
* Which departments have the most compliance issues?
* How many users have expired requirements?

---

## Access Reconciliation

The Access Reconciliation section supports comparison of governance records against authoritative access sources.

### Purpose

Over time, governance records may diverge from operational systems.

Reconciliation helps identify:

* Missing access records
* New access assignments
* Status changes
* Potential governance discrepancies

### Typical Workflow

#### Step 1: Obtain an Authoritative Access Export

Examples include:

* Application user exports
* Platform role exports
* Database permission exports
* Dashboard access exports

#### Step 2: Upload the Export

Upload a CSV file using the expected schema.

#### Step 3: Validate the File

AccessAtlas validates:

* Required columns
* Data structure

#### Step 4: Review Reconciliation Results

Results are classified into categories such as:

* New Access in Upload
* Access Not Found in Upload
* Status Changed
* No Change

#### Step 5: Review the Action Queue

The Action Queue highlights records requiring review.

#### Step 6: Coordinate Remediation

Remediation actions are typically performed in source systems rather than within AccessAtlas itself.

---

## Governance Reporting

Super Administrators often use AccessAtlas as a reporting platform.

Examples include:

* User access inventories
* System access inventories
* Compliance reports
* Administrative coverage reports
* Reconciliation reports

Reports can support:

* Governance reviews
* Internal audits
* Compliance audits
* Access certification activities

---

## Data Governance Best Practices

Super Administrators should follow several governance practices.

### Maintain Historical Records

Avoid deleting records when possible.

Use inactive status designations to preserve audit history.

### Review Administrative Coverage of Tracked Systems

Ensure all tracked systems have assigned administrators.

### Monitor Compliance Regularly

Review compliance metrics and follow-up queues on a regular schedule.

### Perform Reconciliation Routinely

Regular reconciliation helps maintain confidence in governance data.

### Document Governance Decisions

Maintain documentation for governance processes, ownership assignments, and remediation decisions.

---

## Troubleshooting

### Missing User Information

Verify that the user exists within the Central User Registry.

### Missing System Information

Verify that the system exists within the Systems Catalog.

### Missing Administrator Assignments

Review the System Admins section and verify assignment records.

### Reconciliation Upload Errors

Verify that uploaded files contain all required reconciliation columns.

### Unexpected Reconciliation Results

Verify:

* User identifiers
* System identifiers
* Resource names
* Permission names
* Access status values

Discrepancies in any of these values may produce unexpected reconciliation results.

---

## Summary

Super Administrators oversee the governance environment as a whole.

Their responsibilities include:

* User governance
* System governance
* Administrative accountability
* Compliance monitoring
* Access reconciliation
* Governance reporting

Together, these activities help organizations maintain accurate, auditable, and trustworthy access governance records across their technology landscape.
