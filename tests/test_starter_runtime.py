"""Tests for starter identity resolution and runtime scoping."""

import pandas as pd
import pytest
from accessatlas.starter_runtime import (
    STARTER_USER_ID_ENV,
    _resolve_starter_user,
    build_starter_runtime,
)


def _users():
    return pd.DataFrame(
        [
            {
                "user_id": "USR00003",
                "application_role": "User",
                "record_status": "Active",
                "manager_user_id": "",
            },
            {
                "user_id": "USR00002",
                "application_role": "Super Administrator",
                "record_status": "Active",
                "manager_user_id": "",
            },
            {
                "user_id": "USR00001",
                "application_role": "Super Administrator",
                "record_status": "Active",
                "manager_user_id": "",
            },
        ]
    )


def test_environment_identity_takes_precedence(monkeypatch):
    users = _users()
    monkeypatch.setenv(STARTER_USER_ID_ENV, "USR00003")

    selected = _resolve_starter_user(users)

    assert selected["user_id"] == "USR00003"


def test_invalid_environment_identity_raises_clear_error(monkeypatch):
    monkeypatch.setenv(STARTER_USER_ID_ENV, "MISSING")

    with pytest.raises(ValueError, match="does not match a user_id"):
        _resolve_starter_user(_users())


def test_fallback_selects_lowest_active_super_administrator(monkeypatch):
    monkeypatch.delenv(STARTER_USER_ID_ENV, raising=False)

    selected = _resolve_starter_user(_users())

    assert selected["user_id"] == "USR00001"


def test_fallback_selects_first_active_user_when_no_active_super_admin(monkeypatch):
    monkeypatch.delenv(STARTER_USER_ID_ENV, raising=False)
    users = _users()
    users.loc[
        users["application_role"] == "Super Administrator",
        "record_status",
    ] = "Inactive"

    selected = _resolve_starter_user(users)

    assert selected["user_id"] == "USR00003"


def test_fallback_selects_first_record_when_no_active_users(monkeypatch):
    monkeypatch.delenv(STARTER_USER_ID_ENV, raising=False)
    users = _users()
    users["record_status"] = "Inactive"

    selected = _resolve_starter_user(users)

    assert selected["user_id"] == "USR00001"


def test_empty_user_dataset_raises_clear_error(monkeypatch):
    monkeypatch.delenv(STARTER_USER_ID_ENV, raising=False)
    users = pd.DataFrame(
        columns=["user_id", "application_role", "record_status", "manager_user_id"]
    )

    with pytest.raises(ValueError, match="user dataset is empty"):
        _resolve_starter_user(users)


def test_build_starter_runtime_returns_scoped_non_demo_context(monkeypatch):
    monkeypatch.setenv(STARTER_USER_ID_ENV, "USR00003")
    users = _users()
    systems = pd.DataFrame([{"system_id": "SYS1"}, {"system_id": "SYS2"}])
    access = pd.DataFrame(
        [
            {"user_id": "USR00003", "system_id": "SYS2"},
            {"user_id": "USR00001", "system_id": "SYS1"},
        ]
    )
    system_admins = pd.DataFrame(columns=["user_id", "system_id", "assignment_status"])

    runtime = build_starter_runtime(users, systems, access, system_admins)

    assert runtime.current_user["user_id"] == "USR00003"
    assert runtime.runtime_name == "starter"
    assert runtime.is_demo is False
    assert set(runtime.users["user_id"]) == {"USR00003"}
    assert set(runtime.systems["system_id"]) == {"SYS2"}
    assert set(runtime.access["system_id"]) == {"SYS2"}
