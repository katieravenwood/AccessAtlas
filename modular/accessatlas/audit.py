"""Governance audit event model and reference session-backed audit store."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from typing import Any, Protocol
from uuid import uuid4

import pandas as pd


_AUDIT_STATE_KEY = "governance_audit_events"
_AUDIT_ACTOR_USER_ID: ContextVar[str] = ContextVar(
    "accessatlas_audit_actor_user_id",
    default="",
)
_AUDIT_ACTOR_ROLE: ContextVar[str] = ContextVar(
    "accessatlas_audit_actor_role",
    default="",
)
_AUDIT_RUNTIME: ContextVar[str] = ContextVar(
    "accessatlas_audit_runtime",
    default="unknown",
)


@dataclass(frozen=True)
class AuditEvent:
    """One immutable governance action record."""

    audit_event_id: str
    occurred_at: str
    event_type: str
    action: str
    actor_user_id: str
    actor_role: str
    runtime: str
    entity_type: str
    entity_id: str
    target_user_id: str
    system_id: str
    outcome: str
    source: str
    summary: str
    changes_json: str

    def to_record(self) -> dict[str, str]:
        """Return a tabular event record."""
        return asdict(self)


class AuditStore(Protocol):
    """Storage contract for append-oriented governance audit events."""

    def append(self, event: AuditEvent) -> None:
        """Append one immutable audit event."""

    def list_events(self) -> list[AuditEvent]:
        """Return audit events in append order."""


class SessionAuditStore:
    """Streamlit session-backed reference audit store.

    A state mapping may be injected for tests or alternative session containers.
    When omitted, the store resolves Streamlit session state lazily.
    """

    def __init__(
        self,
        state_key: str = _AUDIT_STATE_KEY,
        state: dict[str, Any] | None = None,
    ):
        self.state_key = state_key
        self._state = state

    def _state_mapping(self):
        if self._state is not None:
            return self._state

        import streamlit as st

        return st.session_state

    def _initialize(self) -> None:
        state = self._state_mapping()
        if self.state_key not in state:
            state[self.state_key] = []

    def append(self, event: AuditEvent) -> None:
        self._initialize()
        self._state_mapping()[self.state_key].append(event.to_record())

    def list_events(self) -> list[AuditEvent]:
        self._initialize()
        return [
            AuditEvent(**record)
            for record in self._state_mapping()[self.state_key]
        ]


def set_audit_actor_context(
    actor_user_id: str,
    actor_role: str,
    runtime: str,
) -> None:
    """Set actor and runtime context used by subsequent governance events."""
    _AUDIT_ACTOR_USER_ID.set(str(actor_user_id or ""))
    _AUDIT_ACTOR_ROLE.set(str(actor_role or ""))
    _AUDIT_RUNTIME.set(str(runtime or "unknown"))


def reset_audit_actor_context() -> None:
    """Reset governance audit actor context."""
    _AUDIT_ACTOR_USER_ID.set("")
    _AUDIT_ACTOR_ROLE.set("")
    _AUDIT_RUNTIME.set("unknown")


def _safe_json(value: Any) -> str:
    """Serialize audit change details predictably."""
    return json.dumps(
        value or {},
        default=str,
        sort_keys=True,
        separators=(",", ":"),
    )


def create_audit_event(
    *,
    event_type: str,
    action: str,
    entity_type: str,
    entity_id: str = "",
    target_user_id: str = "",
    system_id: str = "",
    outcome: str = "success",
    source: str = "AccessAtlas",
    summary: str,
    changes: dict[str, Any] | None = None,
) -> AuditEvent:
    """Create one governance audit event from the active actor context."""
    occurred_at = datetime.now(timezone.utc).isoformat()
    event_id = f"AUD-{datetime.now(timezone.utc).year}-{uuid4().hex[:12].upper()}"

    return AuditEvent(
        audit_event_id=event_id,
        occurred_at=occurred_at,
        event_type=str(event_type),
        action=str(action),
        actor_user_id=_AUDIT_ACTOR_USER_ID.get(),
        actor_role=_AUDIT_ACTOR_ROLE.get(),
        runtime=_AUDIT_RUNTIME.get(),
        entity_type=str(entity_type),
        entity_id=str(entity_id or ""),
        target_user_id=str(target_user_id or ""),
        system_id=str(system_id or ""),
        outcome=str(outcome),
        source=str(source),
        summary=str(summary),
        changes_json=_safe_json(changes),
    )


def record_audit_event(
    *,
    event_type: str,
    action: str,
    entity_type: str,
    entity_id: str = "",
    target_user_id: str = "",
    system_id: str = "",
    outcome: str = "success",
    source: str = "AccessAtlas",
    summary: str,
    changes: dict[str, Any] | None = None,
    store: AuditStore | None = None,
) -> AuditEvent:
    """Create and append one governance audit event."""
    audit_store = store or SessionAuditStore()
    event = create_audit_event(
        event_type=event_type,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        target_user_id=target_user_id,
        system_id=system_id,
        outcome=outcome,
        source=source,
        summary=summary,
        changes=changes,
    )
    audit_store.append(event)
    return event


def get_audit_events(store: AuditStore | None = None) -> pd.DataFrame:
    """Return governance audit history as a display/export-ready dataframe."""
    audit_store = store or SessionAuditStore()
    records = [event.to_record() for event in audit_store.list_events()]

    columns = [
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

    if not records:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame(records, columns=columns)
