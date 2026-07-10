"""AccessAtlas application module."""


def get_admin_system_ids(system_admins, user_id):
    """Return system IDs actively administered by the selected user."""
    return (
        system_admins[
            (system_admins["user_id"] == user_id) & (system_admins["assignment_status"] == "Active")
        ]["system_id"]
        .dropna()
        .unique()
        .tolist()
    )


def get_manager_report_ids(users, manager_user_id):
    """Return direct report user IDs for the selected manager."""
    return users[users["manager_user_id"] == manager_user_id]["user_id"].dropna().unique().tolist()


def get_role_scope(users, systems, access, system_admins, current_user):
    """Return visible user and system IDs for the current application role."""
    role = current_user["application_role"]
    current_user_id = current_user["user_id"]

    if role == "Super Administrator":
        return {
            "user_ids": users["user_id"].dropna().unique().tolist(),
            "system_ids": systems["system_id"].dropna().unique().tolist(),
        }

    if role == "Manager":
        direct_reports = get_manager_report_ids(users, current_user_id)
        visible_user_ids = sorted(set([current_user_id] + direct_reports))
        visible_system_ids = (
            access[access["user_id"].isin(visible_user_ids)]["system_id"].dropna().unique().tolist()
        )
        return {
            "user_ids": visible_user_ids,
            "system_ids": visible_system_ids,
        }

    if role == "System Administrator":
        administered_system_ids = get_admin_system_ids(system_admins, current_user_id)
        visible_user_ids = (
            access[access["system_id"].isin(administered_system_ids)]["user_id"]
            .dropna()
            .unique()
            .tolist()
        )
        return {
            "user_ids": sorted(set(visible_user_ids)),
            "system_ids": administered_system_ids,
        }

    return {
        "user_ids": [current_user_id],
        "system_ids": access[access["user_id"] == current_user_id]["system_id"]
        .dropna()
        .unique()
        .tolist(),
    }


def apply_role_scope(users, systems, access, system_admins, current_user):
    """Return datasets scoped to the current application role.

    This function expresses application scope rules. Production implementations
    must enforce equivalent authorization in the backend and data-access layer.
    """
    scope = get_role_scope(users, systems, access, system_admins, current_user)
    visible_user_ids = scope["user_ids"]
    visible_system_ids = scope["system_ids"]

    scoped_users = users[users["user_id"].isin(visible_user_ids)].copy()
    scoped_systems = systems[systems["system_id"].isin(visible_system_ids)].copy()
    scoped_access = access[
        access["user_id"].isin(visible_user_ids) & access["system_id"].isin(visible_system_ids)
    ].copy()

    if current_user["application_role"] == "System Administrator":
        scoped_system_admins = system_admins[
            system_admins["system_id"].isin(visible_system_ids)
        ].copy()
    else:
        scoped_system_admins = system_admins[
            system_admins["user_id"].isin(visible_user_ids)
            | system_admins["system_id"].isin(visible_system_ids)
        ].copy()

    return scoped_users, scoped_systems, scoped_access, scoped_system_admins


def should_show_user_registry(current_user):
    """Return whether the current application role should see the user registry section."""
    return current_user["application_role"] != "User"


# Backward-compatible alias retained for downstream examples created before 1.0.0.
apply_demo_role_scope = apply_role_scope
