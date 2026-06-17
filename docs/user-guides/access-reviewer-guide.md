# AccessAtlas Access Reviewer Guide

## Introduction

This guide provides an overview of the responsibilities and workflows available to Access Reviewers within AccessAtlas.

Access Reviewers are responsible for periodically reviewing and validating user access to systems, resources, and permissions. They help ensure that access remains appropriate, necessary, and aligned with business responsibilities.

Access Reviewers are often:

* Managers
* Supervisors
* Team Leads
* Data Owners
* Business Owners
* Department Representatives

Unlike Super Administrators and System Administrators, Access Reviewers are generally responsible for evaluating access decisions rather than administering systems or maintaining governance records.

---

## Responsibilities

Typical Access Reviewer responsibilities include:

* Reviewing user access assignments
* Validating access appropriateness
* Participating in access certification activities
* Supporting compliance reviews
* Identifying unnecessary access
* Escalating governance concerns
* Documenting review decisions

Access Reviewers are generally not responsible for:

* Managing systems
* Modifying source system permissions
* Maintaining governance data
* Managing administrative assignments
* Configuring the AccessAtlas platform

---

## Why Access Reviews Matter

Over time, users change roles, responsibilities, departments, and projects.

Without periodic review, organizations may accumulate:

* Unnecessary access
* Excessive permissions
* Orphaned accounts
* Outdated assignments
* Governance inaccuracies

Access reviews help ensure that access remains:

* Appropriate
* Justified
* Current
* Auditable

---

## Access Review Process

The typical review process follows five steps.

```text
Access Inventory
        ↓
Review Access
        ↓
Validate Business Need
        ↓
Record Decision
        ↓
Remediate if Needed
```

AccessAtlas supports the review and validation portions of this process.

---

## AccessAtlas Navigation

Access Reviewers primarily use:

1. Users
2. Systems
3. Compliance
4. Access Reconciliation

The Overview dashboard may also be used to understand overall governance status.

---

## Reviewing Individual Users

The Users section provides a user-centered governance view.

### User Governance Profile

The profile includes:

* User information
* Department
* Manager
* User type
* Compliance status
* Access metrics
* Administrative assignments

### Questions to Consider

When reviewing a user:

* Does the user still require access?
* Are assigned permissions appropriate?
* Does the user still perform the associated business function?
* Does the user require all assigned resources?

### Reviewing Access Assignments

Review:

* Systems accessed
* Resource assignments
* Permission assignments
* Access status

Look for:

* Excessive permissions
* Unused access
* Duplicate assignments
* Access inconsistent with responsibilities

---

## Reviewing Systems

The Systems section provides a system-centered view of access.

### Users with Access

Review:

* Users assigned to the system
* Permission levels
* Resource assignments

### Resources and Permissions

Review:

* Resource types
* Permission structures
* Access distribution

### Questions to Consider During Review

Examples include:

* Do all users require access?
* Are permissions appropriate?
* Are elevated permissions justified?
* Are there users whose access should be removed?

---

## Access Certification Activities

Many organizations conduct periodic access certification reviews.

Examples include:

* Quarterly reviews
* Semiannual reviews
* Annual reviews
* Regulatory reviews

AccessAtlas can support these activities by providing a centralized inventory of:

* Users
* Systems
* Permissions
* Administrative assignments

### Typical Certification Questions

Reviewers may be asked:

* Does this user still require access?
* Is the assigned permission appropriate?
* Is access consistent with job responsibilities?
* Should access be retained or removed?

---

## Compliance Review Support

Access Reviewers may also participate in compliance-related reviews.

### Reviewing Compliance Status

Compliance information may include:

* Training completion
* Agreement acknowledgements
* Policy attestations

Common statuses include:

* Current
* Expiring Soon
* Expired

### Review Considerations

Examples include:

* Does the user have active access while non-compliant?
* Should follow-up occur before access is renewed?
* Are compliance records accurate?

Compliance decisions should follow organizational policy.

---

## Reviewing Reconciliation Results

Access Reconciliation helps identify differences between governance records and authoritative systems.

Reviewers may be asked to help validate reconciliation findings.

### Common Reconciliation Outcomes

#### New Access in Upload

Access exists in the source system but not in governance records.

Review Questions:

* Is the access legitimate?
* Should governance records be updated?

#### Access Not Found in Upload

Access exists in governance records but not in the source system.

Review Questions:

* Was access intentionally removed?
* Should governance records be updated?

#### Status Changed

Access status differs between records.

Review Questions:

* Which source is correct?
* Has access changed recently?

#### No Change

No action required.

---

## Documenting Review Decisions

Organizations often require documentation of review outcomes.

Typical decisions include:

* Access Approved
* Access Requires Modification
* Access Removal Recommended
* Further Investigation Required

AccessAtlas supports the review process, while final decision documentation may occur within organizational workflows.

---

## Escalation Guidelines

Escalate concerns when you identify:

* Unnecessary access
* Excessive permissions
* Missing ownership
* Compliance concerns
* Unexplained reconciliation discrepancies
* Potential security risks

Escalation paths vary by organization.

---

## Governance Best Practices

### Review Access Carefully

Validate access based on actual business need rather than historical assignments.

### Focus on Least Privilege

Users should have only the access necessary to perform their responsibilities.

### Review Elevated Permissions Closely

Administrative and privileged access should receive additional scrutiny.

### Consider Business Context

Access requirements vary across roles and departments.

Review decisions should reflect business responsibilities.

### Participate Consistently

Regular participation in access reviews improves governance quality and reduces long-term risk.

---

## Common Review Questions

### Does the User Still Need Access?

Confirm current job responsibilities and business need.

### Is the Permission Appropriate?

Validate that permission levels match responsibilities.

### Is the User Still Active?

Review employment and record status information.

### Is Compliance Current?

Review compliance status and follow-up requirements.

### Are There Any Outstanding Governance Issues?

Review reconciliation findings and administrative coverage information.

---

## Summary

Access Reviewers play an important role in maintaining accurate and appropriate access governance.

Their primary responsibilities include:

* Reviewing user access
* Validating business need
* Supporting access certification activities
* Participating in compliance reviews
* Evaluating reconciliation findings
* Escalating governance concerns

By performing regular access reviews, organizations can improve security, strengthen compliance, reduce unnecessary access, and maintain confidence in their governance data.
