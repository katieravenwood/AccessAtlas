"""Tests for the governance audit-event model."""

import json

import pandas as pd
from accessatlas.audit import (
    AuditEvent,
    SessionAuditStore,
    create_audit_event,
    get_audit_events,
    record_audit_event,
    reset_audit_actor_context,
    set_audit_actor_context,
)


class MemoryAuditStore:
    """Small in-memory store used to test the audit storage contract."""

    def __init__(self):
        self.events = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)

    def list_events(self) -> list[AuditEvent]:
        return list(self.events)


def setup_function():
    reset_audit_actor_context()


def test_create_audit_event_uses_actor_context():
    set_audit_actor_context("USR00001", "Super Administrator", "starter")

    event = create_audit_event(
        event_type="access_assignment",
        action="create_access",
        entity_type="access_assignment",
        entity_id="A001",
        target_user_id="USR00002",
        system_id="SYS001",
        summary="Access assignment created.",
        changes={"after": {"access_status": "Active"}},
    )

    assert event.audit_event_id.startswith("AUD-")
    assert event.actor_user_id == "USR00001"
    assert event.actor_role == "Super Administrator"
    assert event.runtime == "starter"
    assert event.entity_id == "A001"
    assert event.target_user_id == "USR00002"
    assert event.system_id == "SYS001"


def test_record_audit_event_appends_to_replaceable_store():
    store = MemoryAuditStore()

    event = record_audit_event(
        event_type="user_record",
        action="create_user",
        entity_type="user",
        entity_id="USR00010",
        summary="User governance record created.",
        changes={"after": {"record_status": "Active"}},
        store=store,
    )

    assert store.list_events() == [event]


def test_changes_json_is_deterministic_and_serializable():
    event = create_audit_event(
        event_type="user_compliance",
        action="update_compliance_dates",
        entity_type="user",
        entity_id="USR00003",
        summary="Compliance dates updated.",
        changes={"z": pd.Timestamp("2026-01-01"), "a": "value"},
    )

    payload = json.loads(event.changes_json)
    assert payload["a"] == "value"
    assert payload["z"] == "2026-01-01 00:00:00"


def test_empty_session_audit_history_has_stable_schema():
    state = {}

    events = get_audit_events(SessionAuditStore(state=state))

    assert events.empty
    assert list(events.columns) == [
        "audit_event_id",
        "occurred_at",
        "event_type",
        "action",
        "actor_user_id",
        "actor_role",
        "runtime",
        "entity_type",
        "entity_id",
        "target_user_id",
        "system_id",
        "outcome",
        "source",
        "summary",
        "changes_json",
    ]


def test_session_store_preserves_append_order():
    state = {}
    store = SessionAuditStore(state=state)

    first = record_audit_event(
        event_type="user_record",
        action="create_user",
        entity_type="user",
        entity_id="USR00011",
        summary="First event.",
        store=store,
    )
    second = record_audit_event(
        event_type="access_assignment",
        action="create_access",
        entity_type="access_assignment",
        entity_id="A010",
        summary="Second event.",
        store=store,
    )

    assert [event.audit_event_id for event in store.list_events()] == [
        first.audit_event_id,
        second.audit_event_id,
    ]
