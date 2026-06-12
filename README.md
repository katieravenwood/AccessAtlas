# AccessAtlas

A Streamlit-based reference implementation for centralized access governance, compliance tracking, permission cataloging, and access reconciliation.

AccessAtlas demonstrates how organizations can maintain a single inventory of users, systems, permissions, certifications, and access reviews across applications, databases, cloud platforms, dashboards, and collaboration environments.

The project uses synthetic sample data and generic system examples so it can be adapted to virtually any industry, organization, or technology stack.

## Design Principles

AccessAtlas is built around five core principles:

1. Centralized governance
2. Platform neutrality
3. Auditability
4. Transparency
5. Extensibility

## Purpose

Organizations frequently manage access information across multiple systems, often using disconnected spreadsheets, exports, ticketing systems, and administrative tools.

AccessAtlas demonstrates a practical architecture for consolidating access governance activities into a single platform that can:

- Maintain centralized user inventories
- Catalog managed systems and resources
- Track permissions and access assignments
- Track system administrator assignments
- Monitor compliance requirements
- Support access reviews and audits
- Reconcile authoritative access exports
- Provide governance reporting and oversight

## Key Capabilities

### User Registry

Maintain a centralized inventory of users including identifiers, names, contact information, user type, application role, manager relationship, training records, and governance record status.

### System Catalog

Track applications, databases, cloud data platforms, dashboards, collaboration sites, shared folders, and data management systems.

### Access Governance

Maintain relationships between users and systems including permission assignments, role assignments, access status, access history, and administrative ownership.

### System Administrator Assignments

Assign users as administrators for one or more specific systems without storing comma-separated roles in a user record. This supports a clean many-to-many relationship between users and systems.

### Compliance Tracking

Monitor recurring training, certifications, acknowledgements, and governance obligations.

### Access Reconciliation

Compare authoritative access exports against existing records to identify new users, removed users, permission changes, and status changes.

### Audit Support

Support governance and compliance activities through historical record retention, inactive-user management, access review workflows, reconciliation reporting, and compliance monitoring.

## Example Use Cases

AccessAtlas can be adapted to support:

- Application access inventories
- Database and schema permission tracking
- Dashboard and reporting access reviews
- Collaboration site governance
- User certification management
- Periodic access audits
- Role-based access reviews
- System administrator assignment tracking
- Access reconciliation workflows
- Internal compliance programs
- Data governance initiatives

## Example Architecture

```text
                           AccessAtlas
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
         Users              Systems          Permissions
            │                   │                   │
            └───────────────────┼───────────────────┘
                                ▼
                      Governance Services
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
      Compliance         Reconciliation         Audit
```

## Technology Stack

- Streamlit
- Python
- Pandas
- CSV Data Sources

Common production backends include Snowflake, PostgreSQL, SQL Server, Oracle, Databricks, REST APIs, and identity management platforms.

## Core Data Model

### Users

Individuals or service identities requiring access to systems and resources.

Key fields include:

- `user_id`
- `display_name`
- `email`
- `application_role`
- `manager_user_id`
- `department`
- `user_type`
- `record_status`

`user_type` describes the user's relationship to the organization, such as Employee, Contractor, Vendor, Consultant, or Service Account.

`record_status` describes whether the user record is active for governance purposes.

### Systems

Applications, databases, cloud platforms, dashboards, and collaboration environments.

### Access Assignments

Relationships between users and systems that define permissions and access levels.

### System Administrator Assignments

Relationships between users and systems that define which users administer which systems.

## Repository Structure

```text
/
├── app.py
├── README.md
├── requirements.txt
├── SNOWFLAKE_NOTES.md
└── data/
    ├── users.csv
    ├── systems.csv
    ├── access_assignments.csv
    ├── system_admin_assignments.csv
    └── sample_access_upload.csv
```

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```

## Sample Data

All sample data included in this repository is synthetic.

No proprietary information, organizational data, user records, credentials, or production system details are included.

## Production Deployment Considerations

A production implementation would typically include:

- Single Sign-On (SSO)
- Active Directory or identity provider integration
- Database-backed storage
- Audit logging
- Notification services
- Role-based administration
- Approval workflows
- Automated reconciliation processes
- Monitoring and observability
- Backup and recovery processes

## Snowflake Example

The included `SNOWFLAKE_NOTES.md` document demonstrates how the same architecture can be migrated from CSV-backed storage to a Snowflake-backed implementation.

Only the data access layer needs to change; the user interface and governance workflows remain largely unchanged.
