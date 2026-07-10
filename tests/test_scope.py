"""Tests for AccessAtlas role and record-scope rules."""

import pandas as pd

from accessatlas.scope import (
    apply_role_scope,
    get_admin_system_ids,
    get_manager_report_ids,
    get_role_scope,
    should_show_user_registry,
)


def _datasets():
    users = pd.DataFrame(
        [
            {"user_id": "SUPER", "application_role": "Super Administrator", "manager_user_id": ""},
            {"user_id": "MGR", "application_role": "Manager", "manager_user_id": ""},
            {"user_id": "REPORT1", "application_role": "User", "manager_user_id": "MGR"},
            {"user_id": "REPORT2", "application_role": "User", "manager_user_id": "MGR"},
            {"user_id": "ADMIN", "application_role": "System Administrator", "manager_user_id": ""},
            {"user_id": "OTHER", "application_role": "User", "manager_user_id": ""},
        ]
    )
    systems = pd.DataFrame(
        [
            {"system_id": "SYS1"},
            {"system_id": "SYS2"},
            {"system_id": "SYS3"},
        ]
    )
    access = pd.DataFrame(
        [
            {"user_id": "MGR", "system_id": "SYS1"},
            {"user_id": "REPORT1", "system_id": "SYS1"},
            {"user_id": "REPORT2", "system_id": "SYS2"},
            {"user_id": "OTHER", "system_id": "SYS3"},
            {"user_id": "ADMIN", "system_id": "SYS2"},
        ]
    )
    system_admins = pd.DataFrame(
        [
            {"user_id": "ADMIN", "system_id": "SYS1", "assignment_status": "Active"},
            {"user_id": "ADMIN", "system_id": "SYS2", "assignment_status": "Inactive"},
            {"user_id": "SUPER", "system_id": "SYS3", "assignment_status": "Active"},
        ]
    )
    return users, systems, access, system_admins


def _user(users, user_id):
    return users[users["user_id"] == user_id].iloc[0]


def test_admin_system_ids_include_only_active_assignments():
    _, _, _, system_admins = _datasets()

    assert get_admin_system_ids(system_admins, "ADMIN") == ["SYS1"]


def test_manager_report_ids_return_direct_reports_only():
    users, _, _, _ = _datasets()

    assert set(get_manager_report_ids(users, "MGR")) == {"REPORT1", "REPORT2"}


def test_super_administrator_scope_contains_all_users_and_systems():
    users, systems, access, system_admins = _datasets()

    scope = get_role_scope(
        users, systems, access, system_admins, _user(users, "SUPER")
    )

    assert set(scope["user_ids"]) == set(users["user_id"])
    assert set(scope["system_ids"]) == set(systems["system_id"])


def test_manager_scope_contains_self_direct_reports_and_their_systems():
    users, systems, access, system_admins = _datasets()

    scope = get_role_scope(
        users, systems, access, system_admins, _user(users, "MGR")
    )

    assert set(scope["user_ids"]) == {"MGR", "REPORT1", "REPORT2"}
    assert set(scope["system_ids"]) == {"SYS1", "SYS2"}


def test_system_administrator_scope_is_limited_to_active_administered_systems():
    users, systems, access, system_admins = _datasets()

    scope = get_role_scope(
        users, systems, access, system_admins, _user(users, "ADMIN")
    )

    assert scope["system_ids"] == ["SYS1"]
    assert set(scope["user_ids"]) == {"MGR", "REPORT1"}


def test_user_scope_contains_only_self_and_own_systems():
    users, systems, access, system_admins = _datasets()

    scope = get_role_scope(
        users, systems, access, system_admins, _user(users, "OTHER")
    )

    assert scope["user_ids"] == ["OTHER"]
    assert scope["system_ids"] == ["SYS3"]


def test_apply_role_scope_filters_all_four_datasets_for_system_admin():
    users, systems, access, system_admins = _datasets()

    scoped_users, scoped_systems, scoped_access, scoped_admins = apply_role_scope(
        users, systems, access, system_admins, _user(users, "ADMIN")
    )

    assert set(scoped_users["user_id"]) == {"MGR", "REPORT1"}
    assert set(scoped_systems["system_id"]) == {"SYS1"}
    assert set(scoped_access["system_id"]) == {"SYS1"}
    assert set(scoped_access["user_id"]) == {"MGR", "REPORT1"}
    assert set(scoped_admins["system_id"]) == {"SYS1"}


def test_user_registry_hidden_only_for_user_role():
    assert should_show_user_registry(pd.Series({"application_role": "User"})) is False
    assert should_show_user_registry(pd.Series({"application_role": "Manager"})) is True
    assert should_show_user_registry(
        pd.Series({"application_role": "System Administrator"})
    ) is True
    assert should_show_user_registry(
        pd.Series({"application_role": "Super Administrator"})
    ) is True
