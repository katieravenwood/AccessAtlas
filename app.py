from __future__ import annotations

# ---------------------------------------------------------------------------
# AccessAtlas single-file quick-start application
# ---------------------------------------------------------------------------
#
# GENERATED FILE — DO NOT EDIT AS THE ENGINEERING SOURCE OF TRUTH.
#
# Canonical source:
#   modular/app.py
#   modular/accessatlas/
#
# Rebuild after changing canonical source:
#   python tools/build_single_file.py
#
# Verify the committed quick-start file is current:
#   python tools/build_single_file.py --check
#
# This generated distribution publishes the clean starter runtime as one
# directly editable Streamlit file for quick-start adopters.
# Hosted demo controls remain only in modular/demo_app.py and demo_runtime.py.
# ---------------------------------------------------------------------------


# === Shared module: accessatlas/config.py ===
from pathlib import Path

def _find_project_root():
    """Find the nearest parent containing the shared AccessAtlas data directory."""
    current_path = Path(__file__).resolve().parent
    for candidate in (current_path, *current_path.parents):
        if (candidate / "data").is_dir():
            return candidate
    return Path.cwd()


PROJECT_ROOT = _find_project_root()
DATA_DIR = PROJECT_ROOT / "data"

ANNUAL_TRAINING_VALID_YEARS = 1

BIENNIAL_TRAINING_VALID_YEARS = 2

EXPIRING_SOON_DAYS = 30

RECONCILIATION_KEY_COLUMNS = [
    "user_id",
    "system_id",
    "resource_type",
    "resource_name",
    "permission_name",
]

RECONCILIATION_REQUIRED_COLUMNS = RECONCILIATION_KEY_COLUMNS + ["access_status"]

TRAINING_RECONCILIATION_DATE_COLUMNS = [
    "annual_training_date",
    "biennial_training_date",
    "access_agreement_date",
]

TRAINING_RECONCILIATION_REQUIRED_COLUMNS = ["user_id"] + TRAINING_RECONCILIATION_DATE_COLUMNS

ROLE_VISIBLE_TABS = {
    "User": ["My Access"],
    "Manager": ["Dashboard", "My Access", "Manage Access", "Access Reconciliation"],
    "System Administrator": [
        "Dashboard",
        "My Access",
        "Manage Access",
        "Access Reconciliation",
    ],
    "Super Administrator": [
        "Dashboard",
        "My Access",
        "Manage Access",
        "Access Reconciliation",
        "AccessAtlas App Admin",
    ],
}

TAB_LABELS = [
    "Dashboard",
    "My Access",
    "Manage Access",
    "Access Reconciliation",
    "AccessAtlas App Admin",
]

TAB_DISPLAY_LABELS = {
    "Dashboard": "🏠 Dashboard",
    "My Access": "👤 My Access",
    "Manage Access": "🛠️ Manage Access",
    "Access Reconciliation": "🔄 Access Reconciliation",
    "AccessAtlas App Admin": "⚙️ AccessAtlas App Admin",
}

USER_DISPLAY_COLUMNS = [
    "user_id",
    "display_name",
    "email",
    "application_role",
    "manager_user_id",
    "department",
    "user_type",
    "record_status",
    "compliance_status",
]

COMPLIANCE_COLUMNS = [
    "user_id",
    "display_name",
    "email",
    "department",
    "user_type",
    "record_status",
    "annual_training_date",
    "annual_training_expiration",
    "biennial_training_date",
    "biennial_training_expiration",
    "access_agreement_date",
    "compliance_status",
]

COLUMN_LABELS = {
    "access_agreement_date": "Access Agreement Date",
    "access_id": "Access ID",
    "access_model": "Access Model",
    "access_records": "Access Records",
    "access_status": "Access Status",
    "admin_assignment_count": "Admin Assignments",
    "admin_group": "Admin Group",
    "admin_role": "Admin Role",
    "annual_training_date": "Annual Training Date",
    "annual_training_expiration": "Annual Training Expiration",
    "application_role": "Application Role",
    "assignment_source": "Assignment Source",
    "assignment_status": "Assignment Status",
    "assigned_by": "Assigned By",
    "assigned_users": "Assigned Users",
    "audit_event_id": "Audit Event ID",
    "biennial_training_date": "Biennial Training Date",
    "biennial_training_expiration": "Biennial Training Expiration",
    "change_type": "Change Type",
    "changes_identified": "Changes Identified",
    "changes_made": "Changes Made",
    "compliance_status": "Compliance Status",
    "current_access_agreement_date": "Current Access Agreement Date",
    "current_access_status": "Current Access Status",
    "current_annual_training_date": "Current Annual Training Date",
    "current_biennial_training_date": "Current Biennial Training Date",
    "current_record_status": "Current Record Status",
    "department": "Department",
    "display_name": "Display Name",
    "email": "Email",
    "expiration_date": "Expiration Date",
    "expiration_status": "Expiration Status",
    "first_name": "First Name",
    "granted_date": "Granted Date",
    "last_name": "Last Name",
    "manager_user_id": "Manager User ID",
    "notes": "Notes",
    "permission_name": "Permission",
    "record_status": "Record Status",
    "record_type": "Record Type",
    "recommended_action": "Recommended Action",
    "resource_name": "Resource Name",
    "resource_scope": "Resource Scope",
    "resource_type": "Resource Type",
    "revoked_date": "Revoked Date",
    "source": "Source",
    "source_system_record_id": "Source Record ID",
    "system_category": "System Category",
    "system_id": "System ID",
    "system_name": "System Name",
    "system_owner": "System Owner",
    "system_type": "System Type",
    "tracking_method": "Tracking Method",
    "uploaded_access_agreement_date": "Uploaded Access Agreement Date",
    "uploaded_access_status": "Uploaded Access Status",
    "uploaded_annual_training_date": "Uploaded Annual Training Date",
    "uploaded_biennial_training_date": "Uploaded Biennial Training Date",
    "user_id": "User ID",
    "user_type": "User Type",
    "users": "Users",
}


# === Shared module: accessatlas/logging_config.py ===
from contextvars import ContextVar
from datetime import datetime, timezone
import json
import logging
import os
import sys
from typing import Any, Mapping


LOG_LEVEL_ENV = "ACCESSATLAS_LOG_LEVEL"
LOG_FORMAT_ENV = "ACCESSATLAS_LOG_FORMAT"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "json"
LOGGER_NAMESPACE = "accessatlas"

_runtime_name: ContextVar[str] = ContextVar("accessatlas_runtime_name", default="unresolved")
_application_role: ContextVar[str] = ContextVar("accessatlas_application_role", default="unresolved")

_RESERVED_RECORD_FIELDS = set(logging.makeLogRecord({}).__dict__) | {
    "message",
    "asctime",
}


def _normalize_log_level(value: str | None) -> int:
    """Return a valid logging level from configuration."""
    normalized = (value or DEFAULT_LOG_LEVEL).strip().upper()
    level = logging.getLevelName(normalized)
    return level if isinstance(level, int) else logging.INFO


def _normalize_log_format(value: str | None) -> str:
    """Return a supported output format."""
    normalized = (value or DEFAULT_LOG_FORMAT).strip().lower()
    return normalized if normalized in {"json", "text"} else DEFAULT_LOG_FORMAT


def _json_safe(value: Any) -> Any:
    """Return a JSON-serializable representation of a log field."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    return str(value)


class AccessAtlasContextFilter(logging.Filter):
    """Attach runtime context to every AccessAtlas application log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.runtime_name = _runtime_name.get()
        record.application_role = _application_role.get()
        return True


class JsonFormatter(logging.Formatter):
    """Render AccessAtlas application logs as one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created,
                tz=timezone.utc,
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": getattr(record, "event_name", "application_log"),
            "message": record.getMessage(),
            "runtime": getattr(record, "runtime_name", "unresolved"),
            "application_role": getattr(record, "application_role", "unresolved"),
        }

        event_fields = getattr(record, "event_fields", {})
        if event_fields:
            payload["fields"] = _json_safe(event_fields)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, separators=(",", ":"), sort_keys=True)


class TextFormatter(logging.Formatter):
    """Render readable local-development application logs."""

    def format(self, record: logging.LogRecord) -> str:
        event_name = getattr(record, "event_name", "application_log")
        event_fields = getattr(record, "event_fields", {})
        fields_text = ""
        if event_fields:
            fields_text = f" fields={json.dumps(_json_safe(event_fields), sort_keys=True)}"

        message = (
            f"{datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()} "
            f"{record.levelname} {record.name} "
            f"event={event_name} runtime={getattr(record, 'runtime_name', 'unresolved')} "
            f"role={getattr(record, 'application_role', 'unresolved')} "
            f"{record.getMessage()}{fields_text}"
        )

        if record.exc_info:
            message = f"{message}\n{self.formatException(record.exc_info)}"

        return message


def configure_logging(
    *,
    level: str | None = None,
    output_format: str | None = None,
) -> logging.Logger:
    """Configure the AccessAtlas logger namespace once per Python process.

    Repeated calls update the handler level and formatter without adding
    duplicate handlers. This is important in Streamlit, where the app script
    reruns during user interaction.
    """
    logger = logging.getLogger(LOGGER_NAMESPACE)
    logger.setLevel(_normalize_log_level(level or os.getenv(LOG_LEVEL_ENV)))
    logger.propagate = False

    selected_format = _normalize_log_format(
        output_format or os.getenv(LOG_FORMAT_ENV)
    )
    formatter: logging.Formatter = (
        JsonFormatter() if selected_format == "json" else TextFormatter()
    )

    handler = next(
        (
            candidate
            for candidate in logger.handlers
            if getattr(candidate, "_accessatlas_handler", False)
        ),
        None,
    )

    if handler is None:
        handler = logging.StreamHandler(sys.stdout)
        handler._accessatlas_handler = True  # type: ignore[attr-defined]
        handler.addFilter(AccessAtlasContextFilter())
        logger.addHandler(handler)

    handler.setLevel(logger.level)
    handler.setFormatter(formatter)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger inside the AccessAtlas application namespace."""
    if name == LOGGER_NAMESPACE or name.startswith(f"{LOGGER_NAMESPACE}."):
        logger_name = name
    else:
        logger_name = f"{LOGGER_NAMESPACE}.{name}"
    return logging.getLogger(logger_name)


def set_runtime_log_context(
    *,
    runtime_name: str,
    application_role: str,
) -> None:
    """Set low-cardinality runtime context for subsequent application logs."""
    _runtime_name.set(runtime_name)
    _application_role.set(application_role)


def reset_runtime_log_context() -> None:
    """Reset runtime context to its unresolved startup state."""
    _runtime_name.set("unresolved")
    _application_role.set("unresolved")


def log_event(
    logger: logging.Logger,
    level: int,
    event_name: str,
    message: str,
    **fields: Any,
) -> None:
    """Write one structured application event."""
    logger.log(
        level,
        message,
        extra={
            "event_name": event_name,
            "event_fields": fields,
        },
    )


def log_exception(
    logger: logging.Logger,
    event_name: str,
    message: str,
    **fields: Any,
) -> None:
    """Write one structured exception event with the active traceback."""
    logger.exception(
        message,
        extra={
            "event_name": event_name,
            "event_fields": fields,
        },
    )


# === Shared module: accessatlas/audit.py ===
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


# === Shared module: accessatlas/compliance.py ===
from datetime import date

import pandas as pd


def compliance_status(row):
    """Return compliance status based on training expiration rules."""
    today_ts = pd.Timestamp(date.today())

    annual_exp = row["annual_training_date"] + pd.DateOffset(
        years=ANNUAL_TRAINING_VALID_YEARS
    )
    biennial_exp = row["biennial_training_date"] + pd.DateOffset(
        years=BIENNIAL_TRAINING_VALID_YEARS
    )

    if annual_exp < today_ts or biennial_exp < today_ts:
        return "Expired"

    warning_date = today_ts + pd.Timedelta(days=EXPIRING_SOON_DAYS)
    if annual_exp <= warning_date or biennial_exp <= warning_date:
        return "Expiring Soon"

    return "Current"

def add_expirations(users):
    """Add expiration dates and compliance status fields to the user dataset."""
    users = users.copy()
    users["annual_training_expiration"] = users["annual_training_date"] + pd.DateOffset(
        years=ANNUAL_TRAINING_VALID_YEARS
    )
    users["biennial_training_expiration"] = users[
        "biennial_training_date"
    ] + pd.DateOffset(years=BIENNIAL_TRAINING_VALID_YEARS)
    users["compliance_status"] = users.apply(compliance_status, axis=1)
    return users

def get_expired_follow_up_records(user_records):
    """Return individual expired compliance records needing follow-up."""
    follow_up_rows = []
    today_ts = pd.Timestamp(date.today())

    for _, user_row in user_records.iterrows():
        checks = [
            ("Annual Training", user_row.get("annual_training_expiration")),
            ("Biennial Training", user_row.get("biennial_training_expiration")),
        ]

        for record_type, expiration_date in checks:
            if pd.isna(expiration_date):
                continue
            expiration_ts = pd.to_datetime(expiration_date)
            if expiration_ts < today_ts:
                follow_up_rows.append(
                    {
                        "user_id": user_row.get("user_id"),
                        "display_name": user_row.get("display_name"),
                        "email": user_row.get("email"),
                        "record_type": record_type,
                        "expiration_date": expiration_ts.date(),
                        "expiration_status": "Expired",
                    }
                )

    return pd.DataFrame(follow_up_rows)

def normalize_date_value(value):
    """Return a normalized date string for comparison and display."""
    if pd.isna(value) or value == "":
        return ""
    return str(pd.to_datetime(value).date())

def uploaded_dates_compliance_status(uploaded_values):
    """Return compliance status based on uploaded training and agreement dates."""
    today_ts = pd.Timestamp(date.today())

    annual_date = pd.to_datetime(uploaded_values.get("annual_training_date", ""))
    biennial_date = pd.to_datetime(uploaded_values.get("biennial_training_date", ""))

    if pd.isna(annual_date) or pd.isna(biennial_date):
        return "Expired"

    annual_exp = annual_date + pd.DateOffset(years=ANNUAL_TRAINING_VALID_YEARS)
    biennial_exp = biennial_date + pd.DateOffset(years=BIENNIAL_TRAINING_VALID_YEARS)

    if annual_exp < today_ts or biennial_exp < today_ts:
        return "Expired"

    warning_date = today_ts + pd.Timedelta(days=EXPIRING_SOON_DAYS)
    if annual_exp <= warning_date or biennial_exp <= warning_date:
        return "Expiring Soon"

    return "Current"


# === Shared module: accessatlas/exports.py ===
from dataclasses import dataclass
import re
from typing import Iterable

import pandas as pd



logger = get_logger(__name__)

_FORMULA_PREFIXES = ("=", "+", "-", "@")


@dataclass(frozen=True)
class CsvExportArtifact:
    """Prepared CSV download artifact."""

    export_name: str
    filename: str
    data: bytes
    mime_type: str
    record_count: int
    column_count: int


def _safe_export_name(export_name: str) -> str:
    """Return a filesystem-friendly export name."""
    normalized = re.sub(r"[^A-Za-z0-9_-]+", "_", str(export_name).strip())
    normalized = normalized.strip("_")
    return normalized or "accessatlas_export"


def _sanitize_csv_value(value):
    """Protect spreadsheet consumers from formula-style CSV cell execution."""
    if not isinstance(value, str):
        return value

    stripped = value.lstrip()
    if stripped.startswith(_FORMULA_PREFIXES):
        return "'" + value

    return value


def prepare_export_dataframe(
    dataframe: pd.DataFrame,
    *,
    columns: Iterable[str] | None = None,
    sort_by: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Return a stable, sanitized dataframe for CSV export."""
    export_frame = dataframe.copy()

    if columns is not None:
        requested_columns = list(columns)
        missing_columns = [
            column for column in requested_columns
            if column not in export_frame.columns
        ]
        if missing_columns:
            raise ValueError(
                "Export columns are missing from the dataframe: "
                + ", ".join(missing_columns)
            )
        export_frame = export_frame[requested_columns]

    if sort_by is not None:
        sort_columns = [
            column for column in sort_by
            if column in export_frame.columns
        ]
        if sort_columns:
            export_frame = export_frame.sort_values(
                sort_columns,
                kind="stable",
            )

    object_columns = export_frame.select_dtypes(
        include=["object", "string"]
    ).columns
    for column in object_columns:
        export_frame[column] = export_frame[column].map(_sanitize_csv_value)

    return export_frame.reset_index(drop=True)


def prepare_csv_export(
    dataframe: pd.DataFrame,
    *,
    export_name: str,
    columns: Iterable[str] | None = None,
    sort_by: Iterable[str] | None = None,
) -> CsvExportArtifact:
    """Prepare one portable UTF-8 CSV download artifact."""
    try:
        export_frame = prepare_export_dataframe(
            dataframe,
            columns=columns,
            sort_by=sort_by,
        )
        safe_name = _safe_export_name(export_name)
        csv_text = export_frame.to_csv(
            index=False,
            lineterminator="\n",
        )
        return CsvExportArtifact(
            export_name=safe_name,
            filename=f"{safe_name}.csv",
            data=csv_text.encode("utf-8-sig"),
            mime_type="text/csv",
            record_count=len(export_frame),
            column_count=len(export_frame.columns),
        )
    except Exception:
        log_exception(
            logger,
            "export_preparation_failed",
            "CSV export preparation failed.",
            export_name=export_name,
        )
        raise


# === Shared module: accessatlas/data.py ===
import logging

import pandas as pd
import streamlit as st



logger = get_logger(__name__)

@st.cache_data
def load_csv(filename, date_columns=None):
    """Load a CSV file from the data directory with optional date parsing."""
    source_path = DATA_DIR / filename
    try:
        dataframe = pd.read_csv(
            source_path,
            parse_dates=date_columns or [],
        )
    except Exception:
        log_exception(
            logger,
            "data_load_failed",
            "Reference dataset could not be loaded.",
            dataset=filename,
            source_path=str(source_path),
        )
        raise

    log_event(
        logger,
        logging.INFO,
        "data_loaded",
        "Reference dataset loaded.",
        dataset=filename,
        record_count=len(dataframe),
        column_count=len(dataframe.columns),
    )
    return dataframe

@st.cache_data
def load_data():
    """Load all reference datasets used by the application."""
    users = load_csv(
        "users.csv",
        [
            "annual_training_date",
            "biennial_training_date",
            "access_agreement_date",
            "created_date",
            "updated_date",
        ],
    )
    systems = load_csv("systems.csv")
    access_assignments = load_csv(
        "access_assignments.csv",
        ["granted_date", "revoked_date"],
    )
    system_admin_assignments = load_csv(
        "system_admin_assignments.csv",
        ["granted_date", "revoked_date"],
    )

    datasets = {
        "users": users,
        "systems": systems,
        "access_assignments": access_assignments,
        "system_admin_assignments": system_admin_assignments,
    }
    log_event(
        logger,
        logging.INFO,
        "reference_data_ready",
        "Reference datasets are ready for the application.",
        dataset_counts={
            name: len(dataframe)
            for name, dataframe in datasets.items()
        },
    )
    return datasets


# === Shared module: accessatlas/navigation.py ===
def section_label(tab_name):
    """Return the display label for a top-level section."""
    return TAB_DISPLAY_LABELS.get(tab_name, tab_name)

def section_name_from_label(display_label):
    """Return the internal section name for a top-level display label."""
    reverse_labels = {
        display_value: internal_name
        for internal_name, display_value in TAB_DISPLAY_LABELS.items()
    }
    return reverse_labels.get(display_label, display_label)

def get_visible_tabs(application_role):
    """Return the tab labels visible to the selected demo role."""
    return ROLE_VISIBLE_TABS.get(application_role, ["Overview"])

def is_tab_visible(tab_name, visible_tabs):
    """Return whether a tab should be rendered for the selected demo role."""
    return tab_name in visible_tabs


# === Shared module: accessatlas/presentation.py ===
import pandas as pd
import streamlit as st


def section_caption(text):
    """Render standard section-level instruction text."""
    st.caption(text)

def filter_caption(text):
    """Render standard filter instruction text."""
    st.caption(text)

def apply_multiselect_filter(dataframe, column_name, selected_values):
    """Filter a DataFrame by selected values from a multiselect widget."""
    if not selected_values:
        return dataframe
    return dataframe[dataframe[column_name].isin(selected_values)]

def count_by(dataframe, columns, count_name="records"):
    """Return grouped counts for one or more columns."""
    if isinstance(columns, str):
        columns = [columns]
    return dataframe.groupby(columns).size().reset_index(name=count_name)

def display_table(dataframe):
    """Return a copy of a dataframe with user-friendly column labels."""
    return dataframe.rename(columns=COLUMN_LABELS)

def show_dataframe(dataframe, **kwargs):
    """Render a dataframe with user-friendly column labels and clean defaults."""
    kwargs.setdefault("hide_index", True)
    kwargs.setdefault("width", "stretch")
    st.dataframe(
        display_table(dataframe),
        **kwargs,
    )

def get_display_name(users, user_id):
    """Return a display name for a user ID when available."""
    if pd.isna(user_id) or user_id == "":
        return "Not assigned"
    match = users[users["user_id"] == user_id]
    if match.empty:
        return "Not assigned"
    return match.iloc[0]["display_name"]

def user_profile_markdown(selected_user, manager_name):
    """Build the selected user profile markdown block."""
    return f"""
    **User ID:** {selected_user['user_id']}  
    **Email:** {selected_user['email']}  
    **Department:** {selected_user['department']}  
    **User Type:** {selected_user['user_type']}  
    **Application Role:** {selected_user['application_role']}  
    **Manager:** {manager_name}  
    **Record Status:** {selected_user['record_status']}  
    **Compliance Status:** {selected_user['compliance_status']}
    """

def system_profile_markdown(selected_system):
    """Build the selected system profile markdown block."""
    return f"""
    **System ID:** {selected_system['system_id']}  
    **System Type:** {selected_system['system_type']}  
    **System Category:** {selected_system['system_category']}  
    **Resource Scope:** {selected_system['resource_scope']}  
    **Access Model:** {selected_system['access_model']}  
    **Tracking Method:** {selected_system['tracking_method']}  
    **System Owner:** {selected_system['system_owner']}  
    **Admin Group:** {selected_system['admin_group']}  
    **Record Status:** {selected_system['record_status']}  
    **Notes:** {selected_system['notes']}
    """


# === Shared module: accessatlas/scope.py ===
def get_admin_system_ids(system_admins, user_id):
    """Return system IDs actively administered by the selected user."""
    return system_admins[
        (system_admins["user_id"] == user_id)
        & (system_admins["assignment_status"] == "Active")
    ]["system_id"].dropna().unique().tolist()

def get_manager_report_ids(users, manager_user_id):
    """Return direct report user IDs for the selected manager."""
    return users[
        users["manager_user_id"] == manager_user_id
    ]["user_id"].dropna().unique().tolist()

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
        visible_system_ids = access[
            access["user_id"].isin(visible_user_ids)
        ]["system_id"].dropna().unique().tolist()
        return {
            "user_ids": visible_user_ids,
            "system_ids": visible_system_ids,
        }

    if role == "System Administrator":
        administered_system_ids = get_admin_system_ids(system_admins, current_user_id)
        visible_user_ids = access[
            access["system_id"].isin(administered_system_ids)
        ]["user_id"].dropna().unique().tolist()
        return {
            "user_ids": sorted(set(visible_user_ids)),
            "system_ids": administered_system_ids,
        }

    return {
        "user_ids": [current_user_id],
        "system_ids": access[
            access["user_id"] == current_user_id
        ]["system_id"].dropna().unique().tolist(),
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
        access["user_id"].isin(visible_user_ids)
        & access["system_id"].isin(visible_system_ids)
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


# === Shared module: accessatlas/state.py ===
from datetime import date

import pandas as pd
import streamlit as st


def initialize_user_update_state():
    """Initialize session state used for demo self-service updates."""
    if "user_compliance_updates" not in st.session_state:
        st.session_state["user_compliance_updates"] = {}

def apply_user_compliance_updates(users):
    """Apply in-session user compliance updates to the user dataset."""
    initialize_user_update_state()
    users = users.copy()

    for user_id, updates in st.session_state["user_compliance_updates"].items():
        user_mask = users["user_id"] == user_id
        if not user_mask.any():
            continue

        for column_name, value in updates.items():
            users.loc[user_mask, column_name] = pd.Timestamp(value)

    return users

def update_user_compliance_dates(
    user_id,
    annual_training_date,
    biennial_training_date,
    access_agreement_date,
    *,
    audit_action="update_compliance_dates",
    audit_source="Self Service",
):
    """Store user-submitted compliance date updates and record the governance action."""
    initialize_user_update_state()

    previous_values = st.session_state["user_compliance_updates"].get(user_id, {}).copy()
    new_values = {
        "annual_training_date": annual_training_date,
        "biennial_training_date": biennial_training_date,
        "access_agreement_date": access_agreement_date,
    }
    st.session_state["user_compliance_updates"][user_id] = new_values

    return record_audit_event(
        event_type="user_compliance",
        action=audit_action,
        entity_type="user",
        entity_id=user_id,
        target_user_id=user_id,
        source=audit_source,
        summary="User compliance dates updated.",
        changes={
            "before": previous_values,
            "after": new_values,
        },
    )

def initialize_editable_user_state(users):
    """Initialize session-state backed user records for demo user management."""
    if "editable_users" not in st.session_state:
        st.session_state["editable_users"] = users.copy()

def get_editable_users(users):
    """Return session-state user records, initializing them if needed."""
    initialize_editable_user_state(users)
    return st.session_state["editable_users"].copy()

def generate_next_user_id(users_df):
    """Generate the next synthetic user ID."""
    existing_numbers = (
        users_df["user_id"]
        .dropna()
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if existing_numbers.empty else existing_numbers.max() + 1
    return f"USR{next_number:05d}"

def add_user_record(
    user_id,
    first_name,
    last_name,
    email,
    application_role,
    manager_user_id,
    department,
    user_type,
    record_status,
    annual_training_date,
    biennial_training_date,
    access_agreement_date,
):
    """Add one synthetic user record to the session-state user registry."""
    current_users = st.session_state["editable_users"].copy()

    if user_id in current_users["user_id"].tolist():
        return "duplicate"

    display_name = f"{first_name} {last_name}".strip()
    today = pd.Timestamp(date.today())

    new_user = {
        "user_id": user_id,
        "display_name": display_name,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "application_role": application_role,
        "manager_user_id": manager_user_id,
        "department": department,
        "user_type": user_type,
        "record_status": record_status,
        "annual_training_date": pd.Timestamp(annual_training_date),
        "biennial_training_date": pd.Timestamp(biennial_training_date),
        "access_agreement_date": pd.Timestamp(access_agreement_date),
        "created_date": today,
        "updated_date": today,
    }

    st.session_state["editable_users"] = pd.concat(
        [current_users, pd.DataFrame([new_user])],
        ignore_index=True,
    )
    record_audit_event(
        event_type="user_record",
        action="create_user",
        entity_type="user",
        entity_id=user_id,
        target_user_id=user_id,
        source="Direct User Entry",
        summary="User governance record created.",
        changes={"after": new_user},
    )
    return "added"

def initialize_editable_access_state(access):
    """Initialize session-state backed access assignments for demo CRUD actions."""
    if "editable_access_assignments" not in st.session_state:
        st.session_state["editable_access_assignments"] = access.copy()

def get_editable_access_assignments(access):
    """Return session-state access assignments, initializing them if needed."""
    initialize_editable_access_state(access)
    return st.session_state["editable_access_assignments"].copy()

def generate_next_access_id(access_df):
    """Generate the next synthetic access assignment ID."""
    existing_numbers = (
        access_df["access_id"]
        .dropna()
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if existing_numbers.empty else existing_numbers.max() + 1
    return f"A{next_number:03d}"

def access_key_mask(access_df, row):
    """Return a boolean mask matching an access row by the reconciliation key."""
    return (
        (access_df["user_id"] == row["user_id"])
        & (access_df["system_id"] == row["system_id"])
        & (access_df["resource_type"] == row["resource_type"])
        & (access_df["resource_name"] == row["resource_name"])
        & (access_df["permission_name"] == row["permission_name"])
    )


# === Shared module: accessatlas/reconciliation.py ===
from datetime import date
import logging

import pandas as pd
import streamlit as st




logger = get_logger(__name__)

def validate_upload(upload_df, required_columns):
    """Return a list of required columns missing from an uploaded file."""
    missing_columns = [
        column
        for column in required_columns
        if column not in upload_df.columns
    ]
    log_event(
        logger,
        logging.WARNING if missing_columns else logging.INFO,
        "upload_validated",
        "Uploaded reconciliation file schema validated.",
        record_count=len(upload_df),
        required_column_count=len(required_columns),
        missing_columns=missing_columns,
        is_valid=not missing_columns,
    )
    return missing_columns

def reconcile(current_access, upload_df, selected_system_id=None):
    """Compare current access assignments to an uploaded access export."""
    current = current_access.copy()
    upload = upload_df.copy()

    if selected_system_id and selected_system_id != "All Systems":
        current = current[current["system_id"] == selected_system_id]
        upload = upload[upload["system_id"] == selected_system_id]

    # Determine which key columns are available in both dataframes.
    # Some exports include `first_name`/`last_name`, but the canonical
    # access assignments data may not. Use the intersection to avoid
    # KeyError from set_index when columns are missing.
    key_cols = [c for c in RECONCILIATION_KEY_COLUMNS if c in current.columns and c in upload.columns]

    # If no intersection, fall back to the canonical identifier set
    # that the reference data uses (user_id + system + resource + permission).
    if not key_cols:
        fallback = ["user_id", "system_id", "resource_type", "resource_name", "permission_name"]
        key_cols = [c for c in fallback if c in current.columns and c in upload.columns]

    if not key_cols:
        log_event(
            logger,
            logging.ERROR,
            "reconciliation_key_resolution_failed",
            "Reconciliation could not resolve matching key columns.",
            current_columns=list(current.columns),
            upload_columns=list(upload.columns),
        )
        raise KeyError(
            "Reconciliation cannot proceed: no matching key columns found in current and uploaded data. "
            f"Expected one of {RECONCILIATION_KEY_COLUMNS} or fallback {fallback}.")

    current_key = current.set_index(key_cols)["access_status"].to_dict()
    upload_key = upload.set_index(key_cols)["access_status"].to_dict()

    source_record_lookup = {}
    if "source_system_record_id" in upload.columns:
        source_record_lookup = (
            upload.set_index(key_cols)["source_system_record_id"]
            .to_dict()
        )

    rows = []
    all_keys = sorted(set(current_key.keys()) | set(upload_key.keys()))

    for key in all_keys:
        current_status = current_key.get(key)
        uploaded_status = upload_key.get(key)
        user_id, system_id, resource_type, resource_name, permission_name = key

        if current_status is None:
            change_type = "New Access in Upload"
            recommended_action = "Review and add access record"
        elif uploaded_status is None:
            change_type = "Access Not Found in Upload"
            recommended_action = "Review for inactive status"
        elif current_status != uploaded_status:
            change_type = "Status Changed"
            recommended_action = "Review and update access status"
        else:
            change_type = "No Change"
            recommended_action = "No action"

        rows.append(
            {
                "source_system_record_id": source_record_lookup.get(key),
                "user_id": user_id,
                "system_id": system_id,
                "resource_type": resource_type,
                "resource_name": resource_name,
                "permission_name": permission_name,
                "current_access_status": current_status,
                "uploaded_access_status": uploaded_status,
                "change_type": change_type,
                "recommended_action": recommended_action,
            }
        )

    comparison = pd.DataFrame(rows)
    change_counts = (
        comparison["change_type"].value_counts(dropna=False).to_dict()
        if not comparison.empty
        else {}
    )
    log_event(
        logger,
        logging.INFO,
        "access_reconciliation_completed",
        "System access reconciliation comparison completed.",
        selected_system_id=selected_system_id or "All Systems",
        current_record_count=len(current),
        uploaded_record_count=len(upload),
        comparison_record_count=len(comparison),
        change_counts=change_counts,
    )
    return comparison

def apply_reconciliation_action(access_df, row):
    """Apply one reconciliation recommendation to the canonical access table."""
    access_df = access_df.copy()
    change_type = row["change_type"]
    today = pd.Timestamp(date.today())

    if change_type == "New Access in Upload":
        new_record = {
            "access_id": generate_next_access_id(access_df),
            "user_id": row["user_id"],
            "system_id": row["system_id"],
            "resource_type": row["resource_type"],
            "resource_name": row["resource_name"],
            "permission_name": row["permission_name"],
            "access_status": row["uploaded_access_status"] or "Active",
            "granted_date": today,
            "revoked_date": pd.NaT,
            "source": "Reconciliation Action",
        }
        return pd.concat([access_df, pd.DataFrame([new_record])], ignore_index=True), "added"

    mask = access_key_mask(access_df, row)

    if not mask.any():
        return access_df, "skipped"

    if change_type == "Access Not Found in Upload":
        access_df.loc[mask, "access_status"] = "Inactive"
        access_df.loc[mask, "revoked_date"] = today
        return access_df, "inactivated"

    if change_type == "Status Changed":
        access_df.loc[mask, "access_status"] = row["uploaded_access_status"]
        if row["uploaded_access_status"] == "Inactive":
            access_df.loc[mask, "revoked_date"] = today
        elif row["uploaded_access_status"] == "Active":
            access_df.loc[mask, "revoked_date"] = pd.NaT
        return access_df, "updated"

    return access_df, "skipped"


def build_reconciliation_change_summary(row, outcome):
    """Return a human-readable summary of what changed for a reconciliation row."""
    if outcome == "added":
        return (
            "Added new access assignment "
            f"({row.get('resource_type')} / {row.get('resource_name')} / "
            f"{row.get('permission_name')}) with status "
            f"{row.get('uploaded_access_status')}."
        )

    if outcome == "inactivated":
        return (
            "Access Status: "
            f"{row.get('current_access_status')} → Inactive."
        )

    if outcome == "updated":
        return (
            "Access Status: "
            f"{row.get('current_access_status')} → {row.get('uploaded_access_status')}."
        )

    if outcome == "skipped":
        return "No record was changed. The action was skipped."

    return "No change summary available."

def build_reconciliation_action_result(row, outcome):
    """Return a display-friendly action result and record a successful governance event."""
    result_labels = {
        "added": "Success",
        "inactivated": "Success",
        "updated": "Success",
        "skipped": "Skipped",
    }
    change_summary = build_reconciliation_change_summary(row, outcome)
    audit_event_id = ""

    if outcome != "skipped":
        event = record_audit_event(
            event_type="access_reconciliation",
            action=f"reconciliation_{outcome}",
            entity_type="access_assignment",
            target_user_id=row.get("user_id", ""),
            system_id=row.get("system_id", ""),
            source="System Access Reconciliation",
            summary=change_summary,
            changes={
                "recommended_action": row.get("recommended_action"),
                "change_type": row.get("change_type"),
                "resource_type": row.get("resource_type"),
                "resource_name": row.get("resource_name"),
                "permission_name": row.get("permission_name"),
                "before_status": row.get("current_access_status"),
                "after_status": row.get("uploaded_access_status"),
                "source_system_record_id": row.get("source_system_record_id"),
            },
        )
        audit_event_id = event.audit_event_id

    return {
        "audit_event_id": audit_event_id,
        "action_result": result_labels.get(outcome, "Unknown"),
        "changes_made": change_summary,
        "recommended_action": row.get("recommended_action"),
        "change_type": row.get("change_type"),
        "user_id": row.get("user_id"),
        "first_name": row.get("first_name"),
        "last_name": row.get("last_name"),
        "system_id": row.get("system_id"),
        "system_name": row.get("system_name"),
        "resource_type": row.get("resource_type"),
        "resource_name": row.get("resource_name"),
        "permission_name": row.get("permission_name"),
        "current_access_status": row.get("current_access_status"),
        "uploaded_access_status": row.get("uploaded_access_status"),
        "source_system_record_id": row.get("source_system_record_id"),
    }

def apply_reconciliation_actions(access_df, selected_rows):
    """Apply selected reconciliation actions and return updated access data, counts, and result rows."""
    updated_access = access_df.copy()
    counts = {
        "added": 0,
        "inactivated": 0,
        "updated": 0,
        "skipped": 0,
    }
    action_results = []

    action_value_map = {
        "Add access record": "Review and add access record",
        "Inactivate": "Review for inactive status",
        "Update access status": "Review and update access status",
    }

    for _, row in selected_rows.iterrows():
        row = row.copy()
        if row.get("recommended_action") in action_value_map:
            row["recommended_action"] = action_value_map[row["recommended_action"]]

        updated_access, outcome = apply_reconciliation_action(updated_access, row)
        counts[outcome] += 1

        display_row = row.copy()
        display_row["recommended_action"] = display_recommended_action(
            row.get("recommended_action")
        )
        action_results.append(build_reconciliation_action_result(display_row, outcome))

    result_dataframe = pd.DataFrame(action_results)
    log_event(
        logger,
        logging.INFO,
        "access_reconciliation_actions_applied",
        "Selected system access reconciliation actions were processed.",
        selected_action_count=len(selected_rows),
        outcome_counts=counts,
        resulting_access_record_count=len(updated_access),
    )
    return updated_access, counts, result_dataframe

def inactivate_user_record(user_id):
    """Mark one user record inactive in the session-state user registry."""
    current_users = st.session_state["editable_users"].copy()
    user_mask = current_users["user_id"] == user_id

    if not user_mask.any():
        return "skipped"

    current_users.loc[user_mask, "record_status"] = "Inactive"
    current_users.loc[user_mask, "updated_date"] = pd.Timestamp(date.today())
    st.session_state["editable_users"] = current_users
    return "inactivated"

def reconcile_training_dates(current_users, upload_df):
    """Compare current user compliance dates to an uploaded date export."""
    current = current_users.copy()
    upload = upload_df.copy()

    for column in TRAINING_RECONCILIATION_DATE_COLUMNS:
        current[column] = current[column].apply(normalize_date_value)
        upload[column] = upload[column].apply(normalize_date_value)

    current_lookup = current.set_index("user_id")[TRAINING_RECONCILIATION_DATE_COLUMNS].to_dict("index")
    upload_lookup = upload.set_index("user_id")[TRAINING_RECONCILIATION_DATE_COLUMNS].to_dict("index")
    current_status_lookup = current.set_index("user_id")["record_status"].to_dict()

    rows = []
    all_user_ids = sorted(set(current_lookup.keys()) | set(upload_lookup.keys()))

    for user_id in all_user_ids:
        current_values = current_lookup.get(user_id)
        uploaded_values = upload_lookup.get(user_id)

        if current_values is None:
            change_type = "User Not Found in AccessAtlas"
            recommended_action = "Review user record"
            changes = "Uploaded user is not present in the current user registry."
        elif uploaded_values is None:
            change_type = "User Not Found in Upload"
            recommended_action = "No action"
            changes = "No uploaded date record was provided for this user."
        else:
            uploaded_compliance = uploaded_dates_compliance_status(uploaded_values)
            changed_fields = []

            for column in TRAINING_RECONCILIATION_DATE_COLUMNS:
                current_value = current_values.get(column, "")
                uploaded_value = uploaded_values.get(column, "")
                if current_value != uploaded_value:
                    changed_fields.append(
                        f"{column}: {current_value or 'Blank'} → {uploaded_value or 'Blank'}"
                    )

            if uploaded_compliance == "Expired":
                change_type = "User Remains Out of Compliance"
                recommended_action = "Inactivate user record"
                changes = (
                    "Uploaded dates confirm the user remains out of compliance. "
                    + ("; ".join(changed_fields) if changed_fields else "No date changes provided.")
                )
            elif changed_fields:
                change_type = "Date Changed"
                recommended_action = "Update date records"
                changes = "; ".join(changed_fields)
            else:
                change_type = "No Change"
                recommended_action = "No action"
                changes = "No date changes detected."

        row = {
            "user_id": user_id,
            "current_record_status": current_status_lookup.get(user_id, ""),
            "change_type": change_type,
            "recommended_action": recommended_action,
            "changes_identified": changes,
        }

        for column in TRAINING_RECONCILIATION_DATE_COLUMNS:
            row[f"current_{column}"] = (
                current_values.get(column, "") if current_values else ""
            )
            row[f"uploaded_{column}"] = (
                uploaded_values.get(column, "") if uploaded_values else ""
            )

        rows.append(row)

    comparison = pd.DataFrame(rows)
    change_counts = (
        comparison["change_type"].value_counts(dropna=False).to_dict()
        if not comparison.empty
        else {}
    )
    log_event(
        logger,
        logging.INFO,
        "training_reconciliation_completed",
        "Training and agreement reconciliation comparison completed.",
        current_user_count=len(current),
        uploaded_user_count=len(upload),
        comparison_record_count=len(comparison),
        change_counts=change_counts,
    )
    return comparison

def apply_training_date_actions(selected_rows):
    """Apply selected training date reconciliation actions to session state."""
    initialize_user_update_state()

    results = []
    counts = {"updated": 0, "inactivated": 0, "skipped": 0}

    for _, row in selected_rows.iterrows():
        if row["recommended_action"] == "Update date records":
            audit_event = update_user_compliance_dates(
                row["user_id"],
                row["uploaded_annual_training_date"],
                row["uploaded_biennial_training_date"],
                row["uploaded_access_agreement_date"],
                audit_action="reconcile_compliance_dates",
                audit_source="Training and Agreement Reconciliation",
            )
            counts["updated"] += 1
            results.append(
                {
                    "audit_event_id": audit_event.audit_event_id,
                    "action_result": "Success",
                    "changes_made": row.get("changes_identified", "Date records updated."),
                    "recommended_action": row["recommended_action"],
                    "change_type": row["change_type"],
                    "user_id": row["user_id"],
                    "first_name": row.get("first_name", ""),
                    "last_name": row.get("last_name", ""),
                    "changes_identified": row.get("changes_identified", ""),
                }
            )
            continue

        if row["recommended_action"] == "Inactivate user record":
            outcome = inactivate_user_record(row["user_id"])
            counts["inactivated" if outcome == "inactivated" else "skipped"] += 1
            audit_event_id = ""
            if outcome == "inactivated":
                audit_event_id = record_audit_event(
                    event_type="user_record",
                    action="inactivate_user",
                    entity_type="user",
                    entity_id=row["user_id"],
                    target_user_id=row["user_id"],
                    source="Training and Agreement Reconciliation",
                    summary="User record status set to Inactive.",
                    changes={"record_status": {"before": row.get("current_record_status"), "after": "Inactive"}},
                ).audit_event_id
            results.append(
                {
                    "audit_event_id": audit_event_id,
                    "action_result": "Success" if outcome == "inactivated" else "Skipped",
                    "changes_made": "User record status set to Inactive." if outcome == "inactivated" else "User record was not changed.",
                    "recommended_action": row["recommended_action"],
                    "change_type": row["change_type"],
                    "user_id": row["user_id"],
                    "first_name": row.get("first_name", ""),
                    "last_name": row.get("last_name", ""),
                    "changes_identified": row.get("changes_identified", ""),
                }
            )
            continue

        counts["skipped"] += 1
        results.append(
            {
                "audit_event_id": "",
                "action_result": "Skipped",
                "changes_made": "No date or user status update was applied.",
                "recommended_action": row["recommended_action"],
                "change_type": row["change_type"],
                "user_id": row["user_id"],
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "changes_identified": row.get("changes_identified", ""),
            }
        )

    result_dataframe = pd.DataFrame(results)
    log_event(
        logger,
        logging.INFO,
        "training_reconciliation_actions_applied",
        "Selected training and agreement reconciliation actions were processed.",
        selected_action_count=len(selected_rows),
        outcome_counts=counts,
    )
    return counts, result_dataframe


def display_recommended_action(action):
    """Return a concise display label for a reconciliation recommended action."""
    action_labels = {
        "Review and add access record": "Add access record",
        "Review for inactive status": "Inactivate",
        "Review and update access status": "Update access status",
        "No action": "No action",
    }
    return action_labels.get(action, action)


# === Shared module: accessatlas/runtime.py ===
from dataclasses import dataclass
from typing import Callable

import pandas as pd


SectionGuidanceRenderer = Callable[[str], None]


@dataclass(frozen=True)
class RuntimeContext:
    """Resolved identity, scope, and optional runtime-specific UI behavior."""

    current_user: pd.Series
    visible_tabs: list[str]
    users: pd.DataFrame
    systems: pd.DataFrame
    access: pd.DataFrame
    system_admins: pd.DataFrame
    runtime_name: str
    is_demo: bool = False
    section_guidance_renderer: SectionGuidanceRenderer | None = None


# === Shared module: accessatlas/starter_runtime.py ===
import logging
import os

import pandas as pd



STARTER_USER_ID_ENV = "ACCESSATLAS_USER_ID"


logger = get_logger(__name__)


def _resolve_starter_user(users: pd.DataFrame) -> pd.Series:
    """Resolve the configured starter identity without providing a demo selector."""
    configured_user_id = os.getenv(STARTER_USER_ID_ENV, "").strip()

    if configured_user_id:
        matching_users = users[users["user_id"] == configured_user_id]
        if matching_users.empty:
            raise ValueError(
                f"{STARTER_USER_ID_ENV}={configured_user_id!r} does not match a user_id "
                "in the current user dataset."
            )
        log_event(
            logger,
            logging.INFO,
            "starter_identity_resolved",
            "Starter identity resolved from configuration.",
            resolution_method="environment",
        )
        return matching_users.iloc[0]

    super_admins = users[
        (users["application_role"] == "Super Administrator")
        & (users["record_status"] == "Active")
    ]
    if not super_admins.empty:
        log_event(
            logger,
            logging.WARNING,
            "starter_identity_fallback",
            "Starter identity configuration was not provided; using the active Super Administrator fallback.",
            resolution_method="super_administrator_fallback",
        )
        return super_admins.sort_values("user_id").iloc[0]

    active_users = users[users["record_status"] == "Active"]
    if not active_users.empty:
        log_event(
            logger,
            logging.WARNING,
            "starter_identity_fallback",
            "Starter identity configuration was not provided; using the first active user fallback.",
            resolution_method="active_user_fallback",
        )
        return active_users.sort_values("user_id").iloc[0]

    if users.empty:
        raise ValueError("The user dataset is empty; AccessAtlas cannot resolve a starter identity.")

    log_event(
        logger,
        logging.WARNING,
        "starter_identity_fallback",
        "No active users were available; using the first user record fallback.",
        resolution_method="first_user_fallback",
    )
    return users.sort_values("user_id").iloc[0]


def build_starter_runtime(
    users: pd.DataFrame,
    systems: pd.DataFrame,
    access: pd.DataFrame,
    system_admins: pd.DataFrame,
) -> RuntimeContext:
    """Build the clean starter runtime from a configured application identity."""
    current_user = _resolve_starter_user(users)
    set_runtime_log_context(
        runtime_name="starter",
        application_role=str(current_user["application_role"]),
    )
    visible_tabs = get_visible_tabs(current_user["application_role"])

    scoped_users, scoped_systems, scoped_access, scoped_system_admins = apply_role_scope(
        users,
        systems,
        access,
        system_admins,
        current_user,
    )

    log_event(
        logger,
        logging.INFO,
        "runtime_scope_resolved",
        "Starter runtime scope resolved.",
        visible_section_count=len(visible_tabs),
        visible_user_count=len(scoped_users),
        visible_system_count=len(scoped_systems),
        visible_access_count=len(scoped_access),
        visible_admin_assignment_count=len(scoped_system_admins),
    )

    return RuntimeContext(
        current_user=current_user,
        visible_tabs=visible_tabs,
        users=scoped_users,
        systems=scoped_systems,
        access=scoped_access,
        system_admins=scoped_system_admins,
        runtime_name="starter",
        is_demo=False,
    )


# === Shared module: accessatlas/app_core.py ===
from datetime import date
import logging

import pandas as pd
import streamlit as st



logger = get_logger(__name__)


def run_app(runtime_factory):
    """Run AccessAtlas using the supplied runtime-context factory."""
    configure_logging()
    reset_runtime_log_context()
    reset_audit_actor_context()
    log_event(
        logger,
        logging.INFO,
        "application_run_started",
        "AccessAtlas application run started.",
        runtime_factory=getattr(runtime_factory, "__name__", type(runtime_factory).__name__),
    )
    st.set_page_config(page_title="AccessAtlas", layout="wide")

    def render_csv_export_button(
        dataframe,
        *,
        export_name,
        label,
        key,
        columns=None,
        sort_by=None,
        help_text=None,
    ):
        """Render a scoped CSV download and record successful export activity."""
        artifact = prepare_csv_export(
            dataframe,
            export_name=export_name,
            columns=columns,
            sort_by=sort_by,
        )

        downloaded = st.download_button(
            label,
            data=artifact.data,
            file_name=artifact.filename,
            mime=artifact.mime_type,
            key=key,
            help=help_text,
            disabled=artifact.record_count == 0,
        )

        if downloaded:
            log_event(
                logger,
                logging.INFO,
                "data_export_downloaded",
                "Governance data export downloaded.",
                export_name=artifact.export_name,
                record_count=artifact.record_count,
                column_count=artifact.column_count,
            )
            record_audit_event(
                event_type="data_export",
                action="export_dataset",
                entity_type="governance_dataset",
                entity_id=artifact.export_name,
                source="CSV Export",
                summary=f"Governance dataset exported: {artifact.export_name}.",
                changes={
                    "record_count": artifact.record_count,
                    "column_count": artifact.column_count,
                    "filename": artifact.filename,
                },
            )

        return artifact














    def render_self_service_update_form(selected_user):
        """Render a self-service form for updating training and agreement dates."""
        st.markdown("### Update My Certification and Agreement Dates")
        st.caption(
            "This demo form updates the selected user's compliance dates for the "
            "current Streamlit session. In a persistent deployment, this would write to an approved "
            "database workflow and may require review or approval."
        )

        annual_default = pd.to_datetime(selected_user["annual_training_date"]).date()
        biennial_default = pd.to_datetime(selected_user["biennial_training_date"]).date()
        agreement_default = pd.to_datetime(selected_user["access_agreement_date"]).date()

        with st.form("self_service_compliance_update_form"):
            updated_annual_date = st.date_input(
                "Annual training completion date",
                value=annual_default,
                key="update_annual_training_date",
            )
            updated_biennial_date = st.date_input(
                "Biennial training completion date",
                value=biennial_default,
                key="update_biennial_training_date",
            )
            updated_agreement_date = st.date_input(
                "Access agreement completion date",
                value=agreement_default,
                key="update_access_agreement_date",
            )

            updated_annual_expiration = pd.Timestamp(updated_annual_date) + pd.DateOffset(
                years=ANNUAL_TRAINING_VALID_YEARS
            )
            updated_biennial_expiration = pd.Timestamp(updated_biennial_date) + pd.DateOffset(
                years=BIENNIAL_TRAINING_VALID_YEARS
            )

            st.write(
                f"""
                **Calculated annual training expiration:** {updated_annual_expiration.date()}  
                **Calculated biennial training expiration:** {updated_biennial_expiration.date()}
                """
            )

            submitted = st.form_submit_button("Update My Dates")

        if submitted:
            update_user_compliance_dates(
                selected_user["user_id"],
                updated_annual_date,
                updated_biennial_date,
                updated_agreement_date,
            )
            st.success(
                "Compliance dates updated for this current session. Refreshing the app "
                "or clearing session state will reset the sample CSV-backed data."
            )
            st.rerun()
















































































    data = load_data()
    initialize_user_update_state()
    initialize_editable_user_state(data["users"])
    users = get_editable_users(data["users"])
    users = apply_user_compliance_updates(users)
    users = add_expirations(users)
    systems = data["systems"]
    access = data["access_assignments"]
    system_admins = data["system_admin_assignments"]

    initialize_editable_access_state(access)
    access = get_editable_access_assignments(access)
    for session_key in [
        "reconciliation_action_results",
        "training_reconciliation_action_results",
    ]:
        if session_key not in st.session_state:
            st.session_state[session_key] = pd.DataFrame()

    all_users = users.copy()
    all_systems = systems.copy()
    all_access = access.copy()
    all_system_admins = system_admins.copy()

    runtime = runtime_factory(
        all_users,
        all_systems,
        all_access,
        all_system_admins,
    )
    set_runtime_log_context(
        runtime_name=runtime.runtime_name,
        application_role=str(runtime.current_user["application_role"]),
    )
    set_audit_actor_context(
        actor_user_id=str(runtime.current_user["user_id"]),
        actor_role=str(runtime.current_user["application_role"]),
        runtime=runtime.runtime_name,
    )
    log_event(
        logger,
        logging.INFO,
        "runtime_initialized",
        "Application runtime initialized.",
        is_demo=runtime.is_demo,
        visible_section_count=len(runtime.visible_tabs),
        visible_user_count=len(runtime.users),
        visible_system_count=len(runtime.systems),
        visible_access_count=len(runtime.access),
        visible_admin_assignment_count=len(runtime.system_admins),
    )
    current_user = runtime.current_user
    visible_tabs = runtime.visible_tabs
    users = runtime.users
    systems = runtime.systems
    access = runtime.access
    system_admins = runtime.system_admins
    access_with_systems = access.merge(systems, on="system_id", how="left")

    st.title("AccessAtlas")
    st.caption(
        "Reference implementation for centralized access governance across "
        "applications, databases, data platforms, dashboards, and collaboration sites."
    )

    def render_overview_tab():
        st.subheader("Access Governance Overview")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Users", len(users))
        c2.metric("Tracked Systems", len(systems))
        c3.metric("Access Records", len(access))
        c4.metric("System Admin Assignments", len(system_admins))
        c5.metric(
        "Expired / Expiring",
        len(users[users["compliance_status"].isin(["Expired", "Expiring Soon"])]),
        )

        st.markdown("### User Record Status")
        st.dataframe(
        count_by(users, "record_status", "users"), 
        width='stretch',
        )

        st.markdown("### Compliance Status")
        st.dataframe(
        count_by(users, "compliance_status", "users"), 
        width='stretch',
        )

        st.markdown("### Access Records by System Type")
        st.dataframe(
        count_by(access_with_systems, "system_type"), 
        width='stretch',
        )

        st.markdown("### Access Records by Resource Type")
        st.dataframe(
        count_by(access_with_systems, "resource_type"), 
        width='stretch',
        )

        st.markdown("### Access Records by Access Status")
        st.dataframe(
        count_by(access, "access_status"), 
        width='stretch',
        )



    def render_selected_user_profile(selected_user_id, user_selection_enabled=True):
        """Render an individual user's governance profile."""
        selected_user = users[users["user_id"] == selected_user_id].iloc[0]
        manager_name = get_display_name(all_users, selected_user["manager_user_id"])

        selected_access = access[access["user_id"] == selected_user_id].merge(
            systems,
            on="system_id",
            how="left",
        )
        selected_admin_assignments = (
            system_admins[system_admins["user_id"] == selected_user_id]
            .merge(
                systems[["system_id", "system_name", "system_type", "system_category"]],
                on="system_id",
                how="left",
            )
        )

        st.markdown(f"#### {selected_user['display_name']}")
        st.write(user_profile_markdown(selected_user, manager_name))

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Systems Accessed", selected_access["system_id"].nunique())
        m2.metric("Access Assignments", len(selected_access))
        m3.metric("Admin Assignments", len(selected_admin_assignments))
        m4.metric("Compliance", selected_user["compliance_status"])

        st.markdown("### Training & Agreement Snapshot")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "requirement": "Annual Training",
                        "completion_date": selected_user["annual_training_date"],
                        "expiration_date": selected_user["annual_training_expiration"],
                    },
                    {
                        "requirement": "Biennial Training",
                        "completion_date": selected_user["biennial_training_date"],
                        "expiration_date": selected_user["biennial_training_expiration"],
                    },
                    {
                        "requirement": "Access Agreement",
                        "completion_date": selected_user["access_agreement_date"],
                        "expiration_date": "",
                    },
                ]
            ),
            width='stretch',
        )

        st.markdown("### Access by System")
        if selected_access.empty:
            st.info("This user does not currently have access assignments.")
        else:
            show_dataframe(
                count_by(
                    selected_access,
                    ["system_id", "system_name", "system_type"],
                    "access_records",
                ),
                width='stretch',
            )

        st.markdown("### Detailed Access Assignments")
        show_dataframe(selected_access, 
                    width='stretch')

        st.markdown("### Administrative Assignments")
        if selected_admin_assignments.empty:
            st.info("This user is not assigned as an administrator for any tracked systems.")
        else:
            show_dataframe(selected_admin_assignments, 
                        width='stretch')


    def render_my_record_tab():
        """Render the self-service individual user record tab."""
        st.subheader("My Access")
        st.caption(
            "Review your access record and update your own certification and agreement dates."
        )

        current_user_id = current_user["user_id"]
        if current_user_id not in users["user_id"].tolist():
            st.warning(
                "The current user is outside the current scoped user dataset. "
                "Select another demo account or review the role-scoping rules."
            )
            return

        my_record_tab, update_dates_tab = st.tabs(
            ["My Record", "Update My Certification and Agreement Dates"]
        )

        with my_record_tab:
            render_selected_user_profile(current_user_id, user_selection_enabled=False)

        with update_dates_tab:
            selected_user = users[users["user_id"] == current_user_id].iloc[0]
            render_self_service_update_form(selected_user)


    def render_users_tab():
        st.subheader("User Management Registry")

        if current_user["application_role"] == "System Administrator":
            st.caption(
                "Showing only users with access to systems administered by the selected "
                "System Administrator demo account."
            )
        elif current_user["application_role"] == "Manager":
            st.caption(
                "Showing users within the current Manager review scope."
            )

        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            role_filter = st.multiselect(
                "Filter by application role",
                sorted(users["application_role"].dropna().unique()),
                key="role_filter",
            )
        with filter_col2:
            type_filter = st.multiselect(
                "Filter by user type",
                sorted(users["user_type"].unique()),
                key="type_filter",
            )
        with filter_col3:
            status_filter = st.multiselect(
                "Filter by record status",
                sorted(users["record_status"].dropna().unique()),
                key="status_filter",
            )

        user_view = users.copy()
        user_view = apply_multiselect_filter(user_view, "application_role", role_filter)
        user_view = apply_multiselect_filter(user_view, "user_type", type_filter)
        user_view = apply_multiselect_filter(user_view, "record_status", status_filter)

        st.dataframe(
            user_view[USER_DISPLAY_COLUMNS],
            width='stretch',
        )
        render_csv_export_button(
            user_view,
            export_name="accessatlas_users",
            label="Download Filtered Users CSV",
            key="export_users_csv",
            sort_by=["display_name", "user_id"],
            help_text="Exports the currently filtered user records visible in your application scope.",
        )

        st.markdown("### Selected User Access Profile")
        selected_user_id = st.selectbox(
            "Select user ID",
            users["user_id"],
            key="selected_user_id",
        )
        render_selected_user_profile(selected_user_id)


    def render_systems_tab():
        st.subheader("System Catalog")

        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            system_type_filter = st.multiselect(
                "Filter by system type",
                sorted(systems["system_type"].dropna().unique()),
                key="system_type_filter",
            )
        with filter_col2:
            system_category_filter = st.multiselect(
                "Filter by system category",
                sorted(systems["system_category"].dropna().unique()),
                key="system_category_filter",
            )
        with filter_col3:
            system_status_filter = st.multiselect(
                "Filter by system record status",
                sorted(systems["record_status"].dropna().unique()),
                key="system_status_filter",
            )

        system_view = systems.copy()
        system_view = apply_multiselect_filter(system_view, "system_type", system_type_filter)
        system_view = apply_multiselect_filter(
            system_view,
            "system_category",
            system_category_filter,
        )
        system_view = apply_multiselect_filter(system_view, "record_status", system_status_filter)

        show_dataframe(system_view, 
                    width='stretch')
        render_csv_export_button(
            system_view,
            export_name="accessatlas_systems",
            label="Download Filtered Systems CSV",
            key="export_systems_csv",
            sort_by=["system_name", "system_id"],
            help_text="Exports the currently filtered system records visible in your application scope.",
        )

        st.markdown("### Selected System Access Profile")
        selected_system_id = st.selectbox(
            "Select system ID", 
            systems["system_id"],
            key="selected_system_id",
        )
        selected_system = systems[systems["system_id"] == selected_system_id].iloc[0]

        selected_system_access = access[access["system_id"] == selected_system_id].merge(
            users[["user_id", "display_name", "email", "department", "user_type"]],
            on="user_id",
            how="left",
        )
        selected_system_admins = (
            system_admins[system_admins["system_id"] == selected_system_id]
            .merge(
                all_users[["user_id", "display_name", "email", "department"]],
                on="user_id",
                how="left",
            )
        )

        st.markdown(f"#### {selected_system['system_name']}")
        st.write(system_profile_markdown(selected_system))

        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Unique Users", selected_system_access["user_id"].nunique())
        s2.metric("Access Assignments", len(selected_system_access))
        s3.metric("System Administrators", len(selected_system_admins))
        s4.metric("Resource Types", selected_system_access["resource_type"].nunique())

        st.markdown("### Users with Access")
        if selected_system_access.empty:
            st.info("No access assignments are currently recorded for this system.")
        else:
            st.dataframe(
                selected_system_access[
                    [
                        "user_id",
                        "display_name",
                        "email",
                        "department",
                        "user_type",
                        "resource_type",
                        "resource_name",
                        "permission_name",
                        "access_status",
                        "granted_date",
                        "revoked_date",
                        "source",
                    ]
                ],
                width='stretch',
            )

        st.markdown("### System Administrators")
        if selected_system_admins.empty:
            st.info("No system administrator assignments are currently recorded for this system.")
        else:
            st.dataframe(selected_system_admins, 
                        width='stretch')

        st.markdown("### Resources and Permissions")
        if selected_system_access.empty:
            st.info("No resources or permissions are currently recorded for this system.")
        else:
            show_dataframe(
                count_by(
                    selected_system_access,
                    ["resource_type", "resource_name", "permission_name", "access_status"],
                    "assigned_users",
                ),
                width='stretch',
            )


    def compliance_detail_styler(dataframe):
        """Return a styled compliance dataframe with readable noncompliance highlighting."""
        def style_row(row):
            status = row.get("Compliance Status", row.get("compliance_status"))
            if status in ["Expired", "Expiring Soon"]:
                return [
                    "background-color: #fff7bf; color: #111111;"
                    for _ in row
                ]
            return ["" for _ in row]

        def style_date(value):
            if pd.isna(value) or value == "":
                return ""
            try:
                date_value = pd.to_datetime(value)
            except Exception:
                return ""

            today_ts = pd.Timestamp(date.today())
            if date_value < today_ts:
                return "background-color: #fff7bf; color: #b3261e; font-weight: 800;"
            return ""

        date_columns = [
            column
            for column in [
                "Annual Training Expiration",
                "Biennial Training Expiration",
                "annual_training_expiration",
                "biennial_training_expiration",
            ]
            if column in dataframe.columns
        ]

        return (
            dataframe.style
            .apply(style_row, axis=1)
            .map(style_date, subset=date_columns)
        )


    def render_labeled_metric_card(title, subtitle=None, metric_label=None, metric_value=None, detail_rows=None):
        """Render a compact card using Streamlit-native bordered containers."""
        with st.container(border=True):
            st.markdown(f"### {title}")
            if subtitle:
                st.caption(str(subtitle))
            if metric_label is not None and metric_value is not None:
                st.metric(metric_label, metric_value)
            if detail_rows:
                for label, value in detail_rows:
                    st.write(f"**{label}:** {value}")


    def render_compliance_summary_cards(group_column, title):
        """Render compact compliance summaries by department or user type."""
        st.markdown(f"### {title}")

        summary_rows = []
        for group_value, group_df in users.groupby(group_column):
            compliant_count = len(group_df[group_df["compliance_status"] == "Current"])
            noncompliant_count = len(group_df[group_df["compliance_status"] != "Current"])
            summary_rows.append(
                {
                    group_column: group_value,
                    "compliant": compliant_count,
                    "noncompliant": noncompliant_count,
                }
            )

        if not summary_rows:
            st.info("No compliance summary records are available for this scope.")
            return

        summary_df = display_table(pd.DataFrame(summary_rows))

        def style_summary(dataframe):
            styles = pd.DataFrame("", index=dataframe.index, columns=dataframe.columns)
            if "Compliant" in dataframe.columns:
                styles["Compliant"] = "color: #137333; font-weight: 800;"
            if "Noncompliant" in dataframe.columns:
                styles["Noncompliant"] = "color: #b3261e; font-weight: 800;"
            return styles

        st.dataframe(
            summary_df.style.apply(style_summary, axis=None),
            hide_index=True,
            width='stretch',
        )


    def render_admin_coverage_cards(coverage):
        """Render admin coverage by system as a compact summary table."""
        st.markdown("### Admin Coverage by System")

        if coverage.empty:
            st.info("No system administrator coverage records are available.")
            return

        coverage_view = coverage[
            ["system_id", "system_name", "admin_assignment_count"]
        ].rename(
            columns={
                "admin_assignment_count": "active_admin_assignments",
            }
        )

        st.dataframe(
            display_table(coverage_view),
            hide_index=True,
            width='stretch',
        )


    def render_record_summary_card(title, subtitle, rows):
        """Render a compact single-record style summary card using native containers."""
        render_labeled_metric_card(
            title=title,
            subtitle=subtitle,
            detail_rows=rows,
        )


    def build_system_admin_view():
        """Return the joined system administrator assignment view."""
        return (
            system_admins.merge(
                all_users[["user_id", "display_name", "email", "department"]],
                on="user_id",
                how="left",
            )
            .merge(
                systems[
                    [
                        "system_id",
                        "system_name",
                        "system_type",
                        "system_category",
                        "record_status",
                    ]
                ],
                on="system_id",
                how="left",
            )
        )


    def render_system_admin_assignments_overview(admin_view):
        """Render assignment overview, coverage cards, filters, and assignment table."""
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Admin Assignments", len(admin_view))
        a2.metric("Unique Administrators", admin_view["user_id"].nunique())
        a3.metric("Systems with Admins", admin_view["system_id"].nunique())
        a4.metric(
            "Active Assignments",
            len(admin_view[admin_view["assignment_status"] == "Active"]),
        )

        coverage = systems[
            ["system_id", "system_name", "system_type", "system_category", "record_status"]
        ].merge(
            count_by(
                admin_view[admin_view["assignment_status"] == "Active"],
                "system_id",
                "admin_assignment_count",
            ),
            on="system_id",
            how="left",
        )
        coverage["admin_assignment_count"] = (
            coverage["admin_assignment_count"].fillna(0).astype(int)
        )
        render_admin_coverage_cards(coverage)

        st.markdown("### All System Administrator Assignments")
        filter_caption(
            "Filter the records below by admin role, assignment status, system type, or system category."
        )

        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        with filter_col1:
            admin_role_filter = st.multiselect(
                "Filter by admin role",
                sorted(admin_view["admin_role"].dropna().unique()),
                key="admin_role_filter",
            )
        with filter_col2:
            assignment_status_filter = st.multiselect(
                "Filter by assignment status",
                sorted(admin_view["assignment_status"].dropna().unique()),
                key="assignment_status_filter",
            )
        with filter_col3:
            admin_system_type_filter = st.multiselect(
                "Filter by system type",
                sorted(admin_view["system_type"].dropna().unique()),
                key="admin_system_type_filter",
            )
        with filter_col4:
            admin_system_category_filter = st.multiselect(
                "Filter by system category",
                sorted(admin_view["system_category"].dropna().unique()),
                key="admin_system_category_filter",
            )

        filtered_admin_view = admin_view.copy()
        filtered_admin_view = apply_multiselect_filter(
            filtered_admin_view,
            "admin_role",
            admin_role_filter,
        )
        filtered_admin_view = apply_multiselect_filter(
            filtered_admin_view,
            "assignment_status",
            assignment_status_filter,
        )
        filtered_admin_view = apply_multiselect_filter(
            filtered_admin_view,
            "system_type",
            admin_system_type_filter,
        )
        filtered_admin_view = apply_multiselect_filter(
            filtered_admin_view,
            "system_category",
            admin_system_category_filter,
        )

        show_dataframe(filtered_admin_view, width='stretch')



    def render_admin_assignment_cards(records, card_title_field):
        """Render administrator assignment records as stacked cards."""
        if records.empty:
            st.info("No assignment records are available.")
            return

        display_columns = [
            "admin_role",
            "assignment_status",
            "system_id",
            "system_name",
            "system_type",
            "system_category",
            "user_id",
            "display_name",
            "email",
            "department",
            "granted_date",
            "revoked_date",
            "assigned_by",
            "assignment_source",
            "notes",
        ]

        label_map = {
            "admin_role": "Admin Role",
            "assignment_status": "Assignment Status",
            "system_id": "System ID",
            "system_name": "System Name",
            "system_type": "System Type",
            "system_category": "System Category",
            "user_id": "User ID",
            "display_name": "Administrator",
            "email": "Email",
            "department": "Department",
            "granted_date": "Granted Date",
            "revoked_date": "Revoked Date",
            "assigned_by": "Assigned By",
            "assignment_source": "Assignment Source",
            "notes": "Notes",
        }

        for index, (_, record) in enumerate(records.iterrows(), start=1):
            title = record.get(card_title_field, f"Assignment {index}")
            with st.container(border=True):
                st.markdown(f"#### {title}")
                field_col1, field_col2 = st.columns(2)

                visible_fields = [
                    column
                    for column in display_columns
                    if column in records.columns
                    and column != card_title_field
                    and pd.notna(record.get(column))
                    and str(record.get(column)) != ""
                    and str(record.get(column)) != "NaT"
                ]

                midpoint = (len(visible_fields) + 1) // 2
                for column in visible_fields[:midpoint]:
                    field_col1.write(f"**{label_map.get(column, column)}:** {record.get(column)}")
                for column in visible_fields[midpoint:]:
                    field_col2.write(f"**{label_map.get(column, column)}:** {record.get(column)}")


    def render_admin_record_review(admin_view):
        """Render administrator-centered record review."""
        st.subheader("Admin Record Review")

        admin_options = sorted(admin_view["display_name"].dropna().unique())
        if not admin_options:
            st.info("No administrator records are available for review.")
            return

        selected_admin = st.selectbox(
            "Select administrator",
            admin_options,
            key="selected_administrator",
        )
        admin_detail = admin_view[admin_view["display_name"] == selected_admin]

        if admin_detail.empty:
            st.info("This administrator has no recorded system administrator assignments.")
            return

        first_admin_row = admin_detail.iloc[0]
        render_record_summary_card(
            selected_admin,
            first_admin_row.get("email", ""),
            [
                ("Department", first_admin_row.get("department", "")),
                ("Assignments", len(admin_detail)),
                (
                    "Active Assignments",
                    len(admin_detail[admin_detail["assignment_status"] == "Active"]),
                ),
                ("Systems Administered", admin_detail["system_id"].nunique()),
            ],
        )
        render_admin_assignment_cards(
            admin_detail,
            card_title_field="system_name",
        )


    def render_system_record_review(admin_view):
        """Render system-centered administrator assignment review."""
        st.subheader("System Record Review")

        system_options = sorted(systems["system_name"].dropna().unique())
        if not system_options:
            st.info("No system records are available for review.")
            return

        selected_admin_system = st.selectbox(
            "Select system",
            system_options,
            key="selected_admin_system",
        )
        selected_admin_system_id = systems[
            systems["system_name"] == selected_admin_system
        ].iloc[0]["system_id"]
        system_admin_detail = admin_view[
            admin_view["system_id"] == selected_admin_system_id
        ]

        selected_system_record = systems[
            systems["system_id"] == selected_admin_system_id
        ].iloc[0]
        render_record_summary_card(
            selected_system_record["system_name"],
            selected_system_record["system_id"],
            [
                ("System Type", selected_system_record.get("system_type", "")),
                ("System Category", selected_system_record.get("system_category", "")),
                ("Record Status", selected_system_record.get("record_status", "")),
                ("Admin Assignments", len(system_admin_detail)),
            ],
        )

        if system_admin_detail.empty:
            st.info("This system has no recorded system administrator assignments.")
        else:
            render_admin_assignment_cards(
                system_admin_detail,
                card_title_field="display_name",
            )


    def render_system_admins_tab():
        st.subheader("System Administrator Assignments")

        admin_view = build_system_admin_view()

        assignments_tab, admin_record_tab, system_record_tab = st.tabs(
            [
                "System Administrator Assignments",
                "Admin Record Review",
                "System Record Review",
            ]
        )

        with assignments_tab:
            render_system_admin_assignments_overview(admin_view)
            render_csv_export_button(
                admin_view,
                export_name="accessatlas_system_administrator_assignments",
                label="Download System Administrator Assignments CSV",
                key="export_system_admin_assignments_csv",
                sort_by=["system_name", "display_name"],
                help_text="Exports administrator assignments within the current application scope.",
            )

        with admin_record_tab:
            render_admin_record_review(admin_view)

        with system_record_tab:
            render_system_record_review(admin_view)


    def render_compliance_tab():
        st.subheader("Compliance Monitoring")

        current_count = len(users[users["compliance_status"] == "Current"])
        expiring_count = len(users[users["compliance_status"] == "Expiring Soon"])
        expired_count = len(users[users["compliance_status"] == "Expired"])
        follow_up_count = len(
            users[
                (users["compliance_status"] != "Current")
                & (users["record_status"] == "Active")
            ]
        )

        cm1, cm2, cm3, cm4 = st.columns(4)
        cm1.metric("Current", current_count)
        cm2.metric("Expiring Soon", expiring_count)
        cm3.metric("Expired", expired_count)
        cm4.metric("Active Records Requiring Follow-Up", follow_up_count)

        summary_col1, summary_col2 = st.columns(2)
        with summary_col1:
            render_compliance_summary_cards("user_type", "Compliance by User Type")
        with summary_col2:
            render_compliance_summary_cards("department", "Compliance by Department")

        st.markdown("### Compliance Detail")
        filter_caption(
            "Filter the records below by compliance status, department, or user type."
        )
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            compliance_filter = st.multiselect(
                "Filter by compliance status",
                sorted(users["compliance_status"].dropna().unique()),
                key="compliance_filter",
            )
        with filter_col2:
            department_filter = st.multiselect(
                "Filter by department",
                sorted(users["department"].dropna().unique()),
                key="department_filter",
            )
        with filter_col3:
            user_type_filter = st.multiselect(
                "Filter by user type",
                sorted(users["user_type"].dropna().unique()),
                key="compliance_user_type_filter",
            )

        comp = users.copy()
        comp = apply_multiselect_filter(comp, "compliance_status", compliance_filter)
        comp = apply_multiselect_filter(comp, "department", department_filter)
        comp = apply_multiselect_filter(comp, "user_type", user_type_filter)

        st.dataframe(
            compliance_detail_styler(display_table(comp[COMPLIANCE_COLUMNS])),
            width='stretch',
        )
        render_csv_export_button(
            comp,
            export_name="accessatlas_compliance_detail",
            label="Download Filtered Compliance Detail CSV",
            key="export_compliance_detail_csv",
            columns=COMPLIANCE_COLUMNS,
            sort_by=["display_name", "user_id"],
            help_text="Exports the currently filtered compliance detail records.",
        )

        st.markdown("### Compliance Follow-Up Queue")
        st.caption(
            "This queue lists each expired compliance item separately so follow-up is tied to the specific record requiring action."
        )
        follow_up = get_expired_follow_up_records(
            users[users["record_status"] == "Active"]
        )
        if follow_up.empty:
            st.success("No expired active user compliance records currently require follow-up.")
        else:
            st.dataframe(
                display_table(follow_up),
                hide_index=True,
                width='stretch',
            )
            render_csv_export_button(
                follow_up,
                export_name="accessatlas_compliance_follow_up",
                label="Download Compliance Follow-Up CSV",
                key="export_compliance_follow_up_csv",
                sort_by=["display_name", "user_id", "compliance_item"],
                help_text="Exports active compliance records that currently require follow-up.",
            )



    def get_allowed_management_systems():
        """Return systems available for direct access management for the current role."""
        if current_user["application_role"] == "Super Administrator":
            return systems.copy()

        if current_user["application_role"] == "System Administrator":
            return systems.copy()

        return systems.iloc[0:0].copy()


    def get_user_options_for_access_management():
        """Return user records available for access management for the current role."""
        if current_user["application_role"] == "Super Administrator":
            return all_users.copy()

        if current_user["application_role"] == "System Administrator":
            return users.copy()

        return users.iloc[0:0].copy()


    def apply_single_access_record_change(
        mode,
        access_id,
        user_id,
        system_id,
        resource_type,
        resource_name,
        permission_name,
        access_status,
        granted_date,
        revoked_date,
        source,
    ):
        """Add or update one access assignment record in session state."""
        current_access = st.session_state["editable_access_assignments"].copy()

        record = {
            "access_id": access_id,
            "user_id": user_id,
            "system_id": system_id,
            "resource_type": resource_type,
            "resource_name": resource_name,
            "permission_name": permission_name,
            "access_status": access_status,
            "granted_date": pd.Timestamp(granted_date) if granted_date else pd.NaT,
            "revoked_date": pd.Timestamp(revoked_date) if revoked_date else pd.NaT,
            "source": source,
        }

        if mode == "Add new access record":
            st.session_state["editable_access_assignments"] = pd.concat(
                [current_access, pd.DataFrame([record])],
                ignore_index=True,
            )
            record_audit_event(
                event_type="access_assignment",
                action="create_access",
                entity_type="access_assignment",
                entity_id=access_id,
                target_user_id=user_id,
                system_id=system_id,
                source="Direct Access Entry",
                summary="Access assignment created.",
                changes={"after": record},
            )
            return "added"

        match = current_access["access_id"] == access_id
        if not match.any():
            return "not_found"

        before_record = current_access.loc[match].iloc[0].to_dict()
        for column_name, value in record.items():
            current_access.loc[match, column_name] = value

        st.session_state["editable_access_assignments"] = current_access
        record_audit_event(
            event_type="access_assignment",
            action="update_access",
            entity_type="access_assignment",
            entity_id=access_id,
            target_user_id=user_id,
            system_id=system_id,
            source="Direct Access Entry",
            summary="Access assignment updated.",
            changes={"before": before_record, "after": record},
        )
        return "updated"


    def render_add_user_form(allowed_systems):
        """Render a demo form for adding one user and optional initial access."""
        st.subheader("Add User")
        st.caption(
            "Add one synthetic user record to the in-session demo user registry. "
            "For System Administrators, an initial access assignment is required so "
            "the new user remains inside the administered-system scope."
        )

        next_user_id = generate_next_user_id(st.session_state["editable_users"])
        manager_options = all_users.copy()
        manager_options["manager_label"] = (
            manager_options["display_name"].astype(str)
            + " ("
            + manager_options["user_id"].astype(str)
            + ")"
        )
        manager_labels = ["Not assigned"] + manager_options["manager_label"].tolist()

        system_options = allowed_systems.copy()
        system_options["system_label"] = (
            system_options["system_name"].astype(str)
            + " ("
            + system_options["system_id"].astype(str)
            + ")"
        )

        with st.form("direct_add_user_form"):
            st.text_input(
                "User ID",
                value=next_user_id,
                key="add_user_id",
                disabled=True,
            )

            first_name = st.text_input("First name", key="add_user_first_name")
            last_name = st.text_input("Last name", key="add_user_last_name")
            email = st.text_input("Email", key="add_user_email")

            application_role = st.selectbox(
                "Application role",
                ["User", "Manager", "System Administrator", "Super Administrator"],
                index=0,
                key="add_user_application_role",
            )
            manager_label = st.selectbox(
                "Manager",
                manager_labels,
                key="add_user_manager",
            )
            department = st.text_input("Department", value="General Operations", key="add_user_department")
            user_type = st.selectbox(
                "User type",
                ["Employee", "Contractor", "Vendor", "Consultant", "Service Account"],
                key="add_user_type",
            )
            record_status = st.selectbox(
                "Record status",
                ["Active", "Leave", "Inactive"],
                key="add_user_record_status",
            )

            annual_training_date = st.date_input(
                "Annual training completion date",
                value=date.today(),
                key="add_user_annual_training_date",
            )
            biennial_training_date = st.date_input(
                "Biennial training completion date",
                value=date.today(),
                key="add_user_biennial_training_date",
            )
            access_agreement_date = st.date_input(
                "Access agreement completion date",
                value=date.today(),
                key="add_user_access_agreement_date",
            )

            st.markdown("### Initial Access Assignment")
            require_initial_access = current_user["application_role"] == "System Administrator"
            add_initial_access = st.checkbox(
                "Create initial access assignment",
                value=require_initial_access,
                disabled=require_initial_access,
                key="add_user_create_initial_access",
            )

            selected_system_label = None
            resource_type = "Application"
            resource_name = ""
            permission_name = ""
            access_status = "Active"
            granted_date = date.today()
            source = "Direct User Entry"

            if add_initial_access:
                selected_system_label = st.selectbox(
                    "System",
                    system_options["system_label"].tolist(),
                    key="add_user_initial_system",
                )
                resource_type = st.selectbox(
                    "Resource type",
                    ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"],
                    key="add_user_initial_resource_type",
                )
                resource_name = st.text_input(
                    "Resource name",
                    value="General Access",
                    key="add_user_initial_resource_name",
                )
                permission_name = st.text_input(
                    "Permission name",
                    value="Viewer",
                    key="add_user_initial_permission_name",
                )
                access_status = st.selectbox(
                    "Access status",
                    ["Active", "Inactive", "Pending Review"],
                    key="add_user_initial_access_status",
                )
                granted_date = st.date_input(
                    "Granted date",
                    value=date.today(),
                    key="add_user_initial_granted_date",
                )
                source = st.text_input(
                    "Source",
                    value="Direct User Entry",
                    key="add_user_initial_source",
                )

            submitted = st.form_submit_button("Add User", type="primary")

        if not submitted:
            return

        if not first_name or not last_name or not email:
            st.error("First name, last name, and email are required.")
            return

        if add_initial_access and (not resource_name or not permission_name):
            st.error("Resource name and permission name are required for the initial access assignment.")
            return

        manager_user_id = ""
        if manager_label != "Not assigned":
            manager_user_id = manager_options[
                manager_options["manager_label"] == manager_label
            ].iloc[0]["user_id"]

        user_outcome = add_user_record(
            next_user_id,
            first_name,
            last_name,
            email,
            application_role,
            manager_user_id,
            department,
            user_type,
            record_status,
            annual_training_date,
            biennial_training_date,
            access_agreement_date,
        )

        if user_outcome == "duplicate":
            st.error("A user with this generated ID already exists.")
            return

        if add_initial_access:
            selected_system_id = system_options[
                system_options["system_label"] == selected_system_label
            ].iloc[0]["system_id"]

            apply_single_access_record_change(
                "Add new access record",
                generate_next_access_id(st.session_state["editable_access_assignments"]),
                next_user_id,
                selected_system_id,
                resource_type,
                resource_name,
                permission_name,
                access_status,
                granted_date,
                None,
                source,
            )

        st.success("User added for this current session.")
        st.rerun()


    def render_add_edit_access_form():
        """Render direct single-record add/edit access management workflow."""
        st.subheader("Add / Edit Access")
        st.caption(
            "Add or edit one user access assignment without uploading a reconciliation file. "
            "Super Administrators can manage all systems. System Administrators can manage "
            "only users and systems within their scoped administered systems."
        )

        allowed_systems = get_allowed_management_systems()
        allowed_users = get_user_options_for_access_management()

        if allowed_systems.empty or allowed_users.empty:
            st.warning("No users or systems are available for management in the current role scope.")
            return

        mode = st.radio(
            "Management action",
            ["Add new access record", "Edit existing access record"],
            horizontal=True,
            key="direct_access_management_mode",
        )

        current_access = st.session_state["editable_access_assignments"].copy()
        scoped_current_access = current_access[
            current_access["system_id"].isin(allowed_systems["system_id"])
        ].copy()

        if current_user["application_role"] == "System Administrator":
            scoped_current_access = scoped_current_access[
                scoped_current_access["user_id"].isin(allowed_users["user_id"])
            ]

        render_csv_export_button(
            scoped_current_access,
            export_name="accessatlas_access_assignments",
            label="Download Scoped Access Assignments CSV",
            key="export_access_assignments_csv",
            sort_by=["system_id", "user_id", "resource_type", "resource_name", "permission_name"],
            help_text="Exports access assignments available in the current direct-management scope.",
        )

        with st.expander("Current manageable access records", expanded=False):
            if scoped_current_access.empty:
                st.info("No access records are currently available in this management scope.")
            else:
                st.dataframe(
                    scoped_current_access.merge(
                        allowed_systems[["system_id", "system_name"]],
                        on="system_id",
                        how="left",
                    ).merge(
                        all_users[["user_id", "display_name", "email"]],
                        on="user_id",
                        how="left",
                    ),
                    width='stretch',
                )

        selected_existing = None
        if mode == "Edit existing access record":
            if scoped_current_access.empty:
                st.warning("There are no existing records available to edit in this scope.")
                return

            access_options = scoped_current_access.copy()
            access_options["access_label"] = (
                access_options["access_id"].astype(str)
                + " — "
                + access_options["user_id"].astype(str)
                + " / "
                + access_options["system_id"].astype(str)
                + " / "
                + access_options["resource_name"].astype(str)
                + " / "
                + access_options["permission_name"].astype(str)
            )

            selected_access_label = st.selectbox(
                "Select access record to edit",
                access_options["access_label"].tolist(),
                key="direct_access_record_select",
            )
            selected_access_id = access_options[
                access_options["access_label"] == selected_access_label
            ].iloc[0]["access_id"]
            selected_existing = scoped_current_access[
                scoped_current_access["access_id"] == selected_access_id
            ].iloc[0]
            default_access_id = selected_existing["access_id"]
        else:
            default_access_id = generate_next_access_id(current_access)

        user_options = allowed_users.copy()
        user_options["user_label"] = (
            user_options["display_name"].astype(str)
            + " ("
            + user_options["user_id"].astype(str)
            + ")"
        )
        system_options = allowed_systems.copy()
        system_options["system_label"] = (
            system_options["system_name"].astype(str)
            + " ("
            + system_options["system_id"].astype(str)
            + ")"
        )

        default_user_index = 0
        default_system_index = 0
        default_resource_type = "Application"
        default_resource_name = ""
        default_permission_name = ""
        default_access_status = "Active"
        default_granted_date = date.today()
        default_revoked_date = None
        default_source = "Direct Entry"

        if selected_existing is not None:
            if selected_existing["user_id"] in user_options["user_id"].tolist():
                default_user_index = user_options["user_id"].tolist().index(selected_existing["user_id"])
            if selected_existing["system_id"] in system_options["system_id"].tolist():
                default_system_index = system_options["system_id"].tolist().index(selected_existing["system_id"])
            default_resource_type = selected_existing["resource_type"]
            default_resource_name = selected_existing["resource_name"]
            default_permission_name = selected_existing["permission_name"]
            default_access_status = selected_existing["access_status"]
            default_granted_date = pd.to_datetime(selected_existing["granted_date"]).date()
            if pd.notna(selected_existing["revoked_date"]):
                default_revoked_date = pd.to_datetime(selected_existing["revoked_date"]).date()
            default_source = selected_existing["source"]

        with st.form("direct_user_access_management_form"):
            st.text_input(
                "Access ID",
                value=default_access_id,
                key="direct_access_id",
                disabled=True,
            )

            selected_user_label = st.selectbox(
                "User",
                user_options["user_label"].tolist(),
                index=default_user_index,
                key="direct_access_user",
            )
            selected_system_label = st.selectbox(
                "System",
                system_options["system_label"].tolist(),
                index=default_system_index,
                key="direct_access_system",
            )

            resource_type = st.selectbox(
                "Resource type",
                ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"],
                index=(
                    ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"]
                    .index(default_resource_type)
                    if default_resource_type in ["Application", "Role", "Schema", "Table", "Dashboard", "Site", "Folder", "Other"]
                    else 7
                ),
                key="direct_resource_type",
            )
            resource_name = st.text_input(
                "Resource name",
                value=default_resource_name,
                key="direct_resource_name",
            )
            permission_name = st.text_input(
                "Permission name",
                value=default_permission_name,
                key="direct_permission_name",
            )
            access_status = st.selectbox(
                "Access status",
                ["Active", "Inactive", "Pending Review"],
                index=(
                    ["Active", "Inactive", "Pending Review"].index(default_access_status)
                    if default_access_status in ["Active", "Inactive", "Pending Review"]
                    else 0
                ),
                key="direct_access_status",
            )
            granted_date = st.date_input(
                "Granted date",
                value=default_granted_date,
                key="direct_granted_date",
            )

            revoked_date_enabled = st.checkbox(
                "Set revoked date",
                value=default_revoked_date is not None,
                key="direct_revoked_date_enabled",
            )
            revoked_date = None
            if revoked_date_enabled:
                revoked_date = st.date_input(
                    "Revoked date",
                    value=default_revoked_date or date.today(),
                    key="direct_revoked_date",
                )

            source = st.text_input(
                "Source",
                value=default_source,
                key="direct_source",
            )

            submitted = st.form_submit_button(
                "Save Access Record",
                type="primary",
            )

        if submitted:
            selected_user_id = user_options[
                user_options["user_label"] == selected_user_label
            ].iloc[0]["user_id"]
            selected_system_id = system_options[
                system_options["system_label"] == selected_system_label
            ].iloc[0]["system_id"]

            if not resource_name or not permission_name:
                st.error("Resource name and permission name are required.")
                return

            outcome = apply_single_access_record_change(
                mode,
                default_access_id,
                selected_user_id,
                selected_system_id,
                resource_type,
                resource_name,
                permission_name,
                access_status,
                granted_date,
                revoked_date,
                source,
            )

            if outcome == "not_found":
                st.error("The selected access record could not be found.")
            else:
                st.success(f"Access record {outcome} for this current session.")
                st.rerun()


    def render_user_access_management_tab():
        """Render direct add/edit workflows for users and access assignments."""
        st.subheader("Edit / Add Access")
        st.caption(
            "Add users and manage individual access assignments without uploading a reconciliation file."
        )

        allowed_systems = get_allowed_management_systems()

        access_tab, user_tab = st.tabs(["Add / Edit Access", "Add User"])
        with access_tab:
            render_add_edit_access_form()

        with user_tab:
            render_add_user_form(allowed_systems)















    def render_system_access_export_reconciliation_tab():
        st.subheader("System Access Export File Upload")
        st.write(
            """
            Upload an access export from a tracked system and compare it against the current
            AccessAtlas access assignment records.
            """
        )

        with st.expander("Expected upload schema"):
            st.write(
                """
                Uploaded reconciliation files should include the following required columns:
                """
            )
            st.dataframe(
                pd.DataFrame(
                    {
                        "column_name": RECONCILIATION_REQUIRED_COLUMNS,
                        "description": [
                            "Unique user identifier",
                            "Tracked system identifier",
                            "Type of resource being governed",
                            "Specific resource name",
                            "Permission or role name",
                            "Current access status in the uploaded source",
                        ],
                    }
                ),
                width='stretch',
            )
            st.write(
                """
                The optional `source_system_record_id` column can be included to preserve
                traceability back to the source export. First (`first_name`) and last 
                (`last_name`) names may be included in uploads for validation and alignment 
                but are not required for reconciliation, as they may not be identical in 
                the currently present access assignment records. 
                """
            )

        upload = st.file_uploader(
            "Upload CSV with source_system_record_id, user_id, system_id, "
            "resource_type, resource_name, permission_name, access_status",
            type=["csv"],
            key="reconciliation_upload",
        )

        if upload:
            uploaded_df = pd.read_csv(upload)
        else:
            uploaded_df = pd.read_csv(DATA_DIR / "sample_access_upload.csv")
            st.caption("Using bundled sample access export.")

        missing_columns = validate_upload(uploaded_df, RECONCILIATION_REQUIRED_COLUMNS)
        if missing_columns:
            st.error(
                "Uploaded file is missing required columns: "
                + ", ".join(missing_columns)
            )
            st.stop()

        st.success("Uploaded file contains all required reconciliation columns.")

        system_options = systems["system_id"].tolist()
        selected_system = st.selectbox(
            "Select system for reconciliation",
            system_options,
            key="reconciliation_scope",
        )
        selected_system_name = systems[
            systems["system_id"] == selected_system
        ].iloc[0]["system_name"]

        st.caption(
            f"Access export uploads are evaluated for one system at a time. "
            f"This run is scoped to **{selected_system_name} ({selected_system})**."
        )

        scoped_uploaded_df = uploaded_df[
            uploaded_df["system_id"] == selected_system
        ].copy()

        if scoped_uploaded_df.empty:
            st.warning(
                "The uploaded export does not contain records for the selected system. "
                "Choose a different system or upload a file for this system."
            )
            st.stop()

        other_system_count = len(uploaded_df[uploaded_df["system_id"] != selected_system])
        if other_system_count > 0:
            st.info(
                f"{other_system_count} uploaded records for other systems are excluded "
                "from this reconciliation run."
            )

        st.markdown("### Uploaded Access Export")
        st.dataframe(
            scoped_uploaded_df,
            width='stretch',
        )

        result = reconcile(access, scoped_uploaded_df, selected_system_id=selected_system)
        result_with_system = (
            result.merge(
                all_users[["user_id", "first_name", "last_name"]],
                on="user_id",
                how="left",
            )
            .merge(
                systems[["system_id", "system_name"]],
                on="system_id",
                how="left",
            )
        )
        result_with_system["recommended_action"] = result_with_system[
            "recommended_action"
        ].apply(display_recommended_action)

        st.markdown("### Reconciliation Summary")
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

        change_counts = result_with_system["change_type"].value_counts().to_dict()
        summary_col1.metric(
            "Add Access",
            change_counts.get("New Access in Upload", 0),
        )
        summary_col2.metric(
            "Inactivate",
            change_counts.get("Access Not Found in Upload", 0),
        )
        summary_col3.metric(
            "Update Status",
            change_counts.get("Status Changed", 0),
        )
        summary_col4.metric(
            "No Change",
            change_counts.get("No Change", 0),
        )

        with st.expander("View reconciliation summary tables"):
            st.markdown("#### Summary by Change Type")
            show_dataframe(
                count_by(result_with_system, "change_type"),
                width='stretch',
            )

            st.markdown("#### Summary by Resource Type")
            show_dataframe(
                count_by(result_with_system, "resource_type"),
                width='stretch',
            )

        st.markdown("### Reconciliation Queue")
        st.caption(
            "All record changes should be reviewed before applying recommended actions. "
            "This demo updates only the in-session access assignment table."
        )
        action_queue = result_with_system[
            result_with_system["recommended_action"] != "No action"
        ].copy()

        queue_change_type_filter = st.multiselect(
            "Filter reconciliation queue by change type",
            sorted(action_queue["change_type"].dropna().unique()),
            key="reconciliation_queue_change_type_filter",
        )
        action_queue = apply_multiselect_filter(
            action_queue,
            "change_type",
            queue_change_type_filter,
        )

        if action_queue.empty:
            st.success("No reconciliation records require follow-up for the selected filters.")
        else:
            action_queue.insert(0, "apply_action", False)
            queue_column_order = [
                "apply_action",
                "recommended_action",
                "change_type",
                "user_id",
                "first_name",
                "last_name",
                "system_id",
                "system_name",
                "resource_type",
                "resource_name",
                "permission_name",
                "current_access_status",
                "uploaded_access_status",
                "source_system_record_id",
            ]
            queue_columns = [
                column for column in queue_column_order if column in action_queue.columns
            ] + [
                column for column in action_queue.columns if column not in queue_column_order
            ]
            action_queue = action_queue[queue_columns]
            editable_action_queue = st.data_editor(
                action_queue,
                width='stretch',
                hide_index=True,
                key="reconciliation_action_queue_editor",
                column_config={
                    "apply_action": st.column_config.CheckboxColumn(
                        "Apply?",
                        help="Select rows to apply the recommended reconciliation action.",
                        default=False,
                    )
                },
                disabled=[
                    column for column in action_queue.columns if column != "apply_action"
                ],
            )

            selected_actions = editable_action_queue[
                editable_action_queue["apply_action"] == True
            ].drop(columns=["apply_action"])

            st.caption(
                "Recommended actions update the canonical access assignment table for "
                "this current session. They do not modify source CSV files."
            )

            if st.button(
                "Apply Recommended Actions",
                key="apply_reconciliation_actions_button",
                disabled=selected_actions.empty,
            ):
                updated_access, action_counts, action_results = apply_reconciliation_actions(
                    st.session_state["editable_access_assignments"],
                    selected_actions,
                )
                st.session_state["editable_access_assignments"] = updated_access
                st.session_state["reconciliation_action_results"] = action_results
                st.success(
                    "Applied reconciliation actions: "
                    f"{action_counts['added']} added, "
                    f"{action_counts['inactivated']} inactivated, "
                    f"{action_counts['updated']} updated, "
                    f"{action_counts['skipped']} skipped."
                )
                st.rerun()

        st.markdown("### Reconciliation Results")
        st.caption(
            "After Apply Recommended Actions is pressed, this section shows the action "
            "outcomes for records changed from the Reconciliation Queue. In production, "
            "these action results would be displayed after the action completes and "
            "written to an audit log."
        )

        action_results = st.session_state.get("reconciliation_action_results", pd.DataFrame())
        if not action_results.empty:
            st.markdown("#### Applied Action Results")
            st.caption(
                "These rows summarize what changed during the most recent reconciliation "
                "action run in this current session."
            )
            action_result_columns = [
                "audit_event_id",
                "action_result",
                "changes_made",
                "recommended_action",
                "change_type",
                "user_id",
                "first_name",
                "last_name",
                "system_id",
                "system_name",
                "resource_type",
                "resource_name",
                "permission_name",
                "current_access_status",
                "uploaded_access_status",
                "source_system_record_id",
            ]
            visible_action_result_columns = [
                column for column in action_result_columns if column in action_results.columns
            ]
            st.dataframe(
                action_results[visible_action_result_columns],
                width='stretch',
            )
            render_csv_export_button(
                action_results,
                export_name="accessatlas_access_reconciliation_results",
                label="Download Reconciliation Results CSV",
                key="export_access_reconciliation_results_csv",
                columns=visible_action_result_columns,
                sort_by=["system_id", "user_id", "audit_event_id"],
                help_text="Exports action results from the most recent system access reconciliation run.",
            )
        else:
            st.info(
                "No reconciliation actions have been applied yet in this current session. "
                "Select records in the Reconciliation Queue and click Apply Recommended Actions "
                "to populate action results."
            )





    def render_training_date_reconciliation_tab():
        """Render training certificate and agreement date reconciliation workflow."""
        st.subheader("Training Certificate Date and Agreement Reconciliation")
        st.write(
            """
            Upload a training or agreement date export and compare it against the current
            AccessAtlas user compliance date records.
            """
        )

        with st.expander("Expected upload schema"):
            st.write("Uploaded files should include the following required columns:")
            st.dataframe(
                pd.DataFrame(
                    {
                        "column_name": TRAINING_RECONCILIATION_REQUIRED_COLUMNS,
                        "description": [
                            "Unique user identifier",
                            "Annual training completion date",
                            "Biennial training completion date",
                            "Access agreement completion date",
                        ],
                    }
                ),
                width='stretch',
            )

        uploaded_training_file = st.file_uploader(
            "Upload CSV with user_id, annual_training_date, biennial_training_date, access_agreement_date",
            type=["csv"],
            key="training_reconciliation_upload",
        )

        if uploaded_training_file:
            training_upload_df = pd.read_csv(
                uploaded_training_file,
                parse_dates=TRAINING_RECONCILIATION_DATE_COLUMNS,
            )
        else:
            training_upload_df = pd.read_csv(
                DATA_DIR / "sample_training_reconciliation_upload.csv",
                parse_dates=TRAINING_RECONCILIATION_DATE_COLUMNS,
            )
            st.caption("Using bundled sample training date reconciliation export.")

        missing_columns = validate_upload(
            training_upload_df,
            TRAINING_RECONCILIATION_REQUIRED_COLUMNS,
        )
        if missing_columns:
            st.error(
                "Uploaded file is missing required columns: "
                + ", ".join(missing_columns)
            )
            st.stop()

        scoped_training_upload_df = training_upload_df[
            training_upload_df["user_id"].isin(users["user_id"])
        ].copy()
        excluded_count = len(training_upload_df) - len(scoped_training_upload_df)
        if excluded_count > 0:
            st.info(
                f"{excluded_count} uploaded records outside the current visible user scope "
                "are excluded from this reconciliation run."
            )

        st.markdown("### Uploaded Training Date Export")
        show_dataframe(scoped_training_upload_df, width='stretch')

        training_result = reconcile_training_dates(users, scoped_training_upload_df)
        training_result = training_result.merge(
            all_users[["user_id", "first_name", "last_name", "display_name"]],
            on="user_id",
            how="left",
        )

        st.markdown("### Training Date Reconciliation Summary")
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        change_counts = training_result["change_type"].value_counts().to_dict()
        summary_col1.metric("Date Changes", change_counts.get("Date Changed", 0))
        summary_col2.metric("Review Inactivation", change_counts.get("User Remains Out of Compliance", 0))
        summary_col3.metric("No Change", change_counts.get("No Change", 0))
        summary_col4.metric("Missing in Registry", change_counts.get("User Not Found in AccessAtlas", 0))

        st.markdown("### Training Date Reconciliation Queue")
        st.caption(
            "All date changes should be reviewed before applying recommended updates. "
            "This demo updates only the in-session user compliance date records."
        )

        training_queue = training_result[
            training_result["recommended_action"] != "No action"
        ].copy()

        queue_change_type_filter = st.multiselect(
            "Filter training reconciliation queue by change type",
            sorted(training_queue["change_type"].dropna().unique()),
            key="training_reconciliation_queue_change_type_filter",
        )
        training_queue = apply_multiselect_filter(
            training_queue,
            "change_type",
            queue_change_type_filter,
        )

        if training_queue.empty:
            st.success("No training date reconciliation records require follow-up for the selected filters.")
        else:
            training_queue.insert(0, "apply_action", False)
            queue_column_order = [
                "apply_action",
                "recommended_action",
                "change_type",
                "user_id",
                "first_name",
                "last_name",
                "current_record_status",
                "changes_identified",
                "current_annual_training_date",
                "uploaded_annual_training_date",
                "current_biennial_training_date",
                "uploaded_biennial_training_date",
                "current_access_agreement_date",
                "uploaded_access_agreement_date",
            ]
            queue_columns = [
                column for column in queue_column_order if column in training_queue.columns
            ] + [
                column for column in training_queue.columns if column not in queue_column_order
            ]

            editable_training_queue = st.data_editor(
                training_queue[queue_columns],
                width='stretch',
                hide_index=True,
                key="training_reconciliation_queue_editor",
                column_config={
                    "apply_action": st.column_config.CheckboxColumn(
                        "Apply?",
                        help="Select rows to update training and agreement dates.",
                        default=False,
                    )
                },
                disabled=[
                    column for column in queue_columns if column != "apply_action"
                ],
            )

            selected_training_actions = editable_training_queue[
                editable_training_queue["apply_action"] == True
            ].drop(columns=["apply_action"])

            if st.button(
                "Apply Training Date Updates",
                key="apply_training_reconciliation_actions_button",
                disabled=selected_training_actions.empty,
            ):
                action_counts, action_results = apply_training_date_actions(
                    selected_training_actions,
                )
                st.session_state["training_reconciliation_action_results"] = action_results
                st.success(
                    "Applied training date reconciliation actions: "
                    f"{action_counts['updated']} updated, "
                    f"{action_counts['inactivated']} inactivated, "
                    f"{action_counts['skipped']} skipped."
                )
                st.rerun()

        st.markdown("### Training Date Reconciliation Results")
        st.caption(
            "After Apply Training Date Updates is pressed, this section shows the action "
            "outcomes for records changed from the Training Date Reconciliation Queue."
        )

        training_action_results = st.session_state.get(
            "training_reconciliation_action_results",
            pd.DataFrame(),
        )
        if training_action_results.empty:
            st.info(
                "No training date reconciliation actions have been applied yet in this current session."
            )
        else:
            show_dataframe(training_action_results, width='stretch')
            render_csv_export_button(
                training_action_results,
                export_name="accessatlas_training_reconciliation_results",
                label="Download Training Reconciliation Results CSV",
                key="export_training_reconciliation_results_csv",
                sort_by=["user_id", "audit_event_id"],
                help_text="Exports action results from the most recent training and agreement reconciliation run.",
            )


    def render_access_reconciliation_tab():
        """Render access and training reconciliation workflow tabs."""
        access_export_tab, training_dates_tab = st.tabs(
            [
                "System Access Export File Upload",
                "Training Certificate Date and Agreement Reconciliation",
            ]
        )

        with access_export_tab:
            render_system_access_export_reconciliation_tab()

        with training_dates_tab:
            render_training_date_reconciliation_tab()



    def render_dashboard_section():
        """Render a streamlined role-aware dashboard."""
        st.subheader("Dashboard")

        pending_reconciliation = 0
        try:
            uploaded_df = pd.read_csv(DATA_DIR / "sample_access_upload.csv")
            pending_reconciliation = len(
                reconcile(access, uploaded_df)[lambda df: df["recommended_action"] != "No action"]
            )
        except Exception:
            pending_reconciliation = 0

        active_follow_up = len(
            users[
                (users["compliance_status"] != "Current")
                & (users["record_status"] == "Active")
            ]
        )

        expired_or_expiring = len(
            users[users["compliance_status"].isin(["Expired", "Expiring Soon"])]
        )

        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Visible Users", len(users))
        d2.metric("Visible Systems", len(systems))
        d3.metric("Access Records", len(access))
        d4.metric("Items Needing Review", pending_reconciliation + active_follow_up)

        h1, h2, h3 = st.columns(3)
        h1.metric("Expired / Expiring Compliance", expired_or_expiring)
        h2.metric("Pending Reconciliation Actions", pending_reconciliation)
        h3.metric("Active Compliance Follow-Up", active_follow_up)

        if current_user["application_role"] == "User":
            st.info(
                "Use My Access to review your profile, access assignments, and compliance dates."
            )
        elif current_user["application_role"] == "System Administrator":
            st.info(
                "Use Manage Access to review users and systems in your administered scope. "
                "Use Access Reconciliation to process reconciliation exceptions."
            )
        elif current_user["application_role"] == "Manager":
            st.info(
                "Use Manage Access to review users in your visible scope and Access Reconciliation "
                "to inspect access exceptions."
            )
        else:
            st.info(
                "Use Manage Access for user/system records, Access Reconciliation for reconciliation, "
                "and AccessAtlas App Admin for compliance and administrative coverage."
            )

        with st.expander("View dashboard details", expanded=True):
            st.caption("Visual summaries for the records visible to the current application role.")

            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.markdown("### Compliance Status")
                st.bar_chart(
                    count_by(users, "compliance_status", "users"),
                    x="compliance_status",
                    y="users",
                )

            with chart_col2:
                st.markdown("### User Record Status")
                st.bar_chart(
                    count_by(users, "record_status", "users"),
                    x="record_status",
                    y="users",
                )

            chart_col3, chart_col4 = st.columns(2)
            with chart_col3:
                st.markdown("### Access Records by System Type")
                st.bar_chart(
                    count_by(access_with_systems, "system_type", "records"),
                    x="system_type",
                    y="records",
                )

            with chart_col4:
                st.markdown("### Access Records by Resource Type")
                st.bar_chart(
                    count_by(access_with_systems, "resource_type", "records"),
                    x="resource_type",
                    y="records",
                )

            st.markdown("### Access Records by Access Status")
            st.bar_chart(
                count_by(access, "access_status", "records"),
                x="access_status",
                y="records",
            )

            with st.expander("View source summary tables"):
                st.markdown("#### User Record Status")
                show_dataframe(
                    count_by(users, "record_status", "users"),
                    width='stretch',
                )

                st.markdown("#### Compliance Status")
                show_dataframe(
                    count_by(users, "compliance_status", "users"),
                    width='stretch',
                )

                st.markdown("#### Access Records by System Type")
                show_dataframe(
                    count_by(access_with_systems, "system_type"),
                    width='stretch',
                )

                st.markdown("#### Access Records by Resource Type")
                show_dataframe(
                    count_by(access_with_systems, "resource_type"),
                    width='stretch',
                )

                st.markdown("#### Access Records by Access Status")
                show_dataframe(
                    count_by(access, "access_status"),
                    width='stretch',
                )


    def render_manage_access_section():
        """Render user/system access workflows in a streamlined task section."""
        st.subheader("Manage Access")
        section_caption(
            "Review managed users and systems, and perform scoped add/edit workflows where permitted by the current application role."
        )

        managed_users_tab, managed_systems_tab, edit_access_tab = st.tabs(
            ["Managed Users", "Managed Systems", "Edit / Add Access"]
        )

        with managed_users_tab:
            render_users_tab()

        with managed_systems_tab:
            st.info(
                """
                Managed Systems shows tracked systems within the current application role scope.

                Access can be governed through different patterns, including periodic user exports,
                application roles, data platform roles, database/schema/table permissions,
                dashboard access, hosting-site access, and collaboration-site membership.
                """
            )
            render_systems_tab()

        with edit_access_tab:
            if current_user["application_role"] in ["System Administrator", "Super Administrator"]:
                render_user_access_management_tab()
            else:
                st.info(
                    "Direct add/edit access management is available to System Administrator "
                    "and Super Administrator application roles."
                )


    def render_review_changes_section():
        """Render reconciliation and action queue workflows."""
        st.subheader("Access Reconciliation")
        section_caption(
            "Review uploaded access and compliance exports, inspect differences, and apply recommended current-session updates."
        )
        render_access_reconciliation_tab()


    def render_audit_history_tab():
        """Render session-backed governance audit history for Super Administrators."""
        st.subheader("Governance Audit History")
        st.caption(
            "Review governance actions recorded during the current Streamlit session. "
            "The reference audit store is append-oriented and session-backed; production "
            "deployments should use controlled persistent audit storage."
        )

        audit_events = get_audit_events()

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Audit Events", len(audit_events))
        metric_col2.metric(
            "Event Types",
            audit_events["event_type"].nunique() if not audit_events.empty else 0,
        )
        metric_col3.metric(
            "Actors",
            audit_events["actor_user_id"].replace("", pd.NA).nunique()
            if not audit_events.empty
            else 0,
        )

        if audit_events.empty:
            st.info(
                "No governance actions have been recorded in the current session. "
                "Create or update a user, update compliance dates, change an access "
                "assignment, or apply a reconciliation action to generate audit history."
            )
            return

        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            event_type_filter = st.multiselect(
                "Filter by event type",
                sorted(audit_events["event_type"].dropna().unique()),
                key="audit_event_type_filter",
            )
        with filter_col2:
            action_filter = st.multiselect(
                "Filter by action",
                sorted(audit_events["action"].dropna().unique()),
                key="audit_action_filter",
            )
        with filter_col3:
            outcome_filter = st.multiselect(
                "Filter by outcome",
                sorted(audit_events["outcome"].dropna().unique()),
                key="audit_outcome_filter",
            )

        filtered_events = audit_events.copy()
        if event_type_filter:
            filtered_events = filtered_events[
                filtered_events["event_type"].isin(event_type_filter)
            ]
        if action_filter:
            filtered_events = filtered_events[
                filtered_events["action"].isin(action_filter)
            ]
        if outcome_filter:
            filtered_events = filtered_events[
                filtered_events["outcome"].isin(outcome_filter)
            ]

        display_columns = [
            "audit_event_id",
            "occurred_at",
            "event_type",
            "action",
            "actor_user_id",
            "actor_role",
            "entity_type",
            "entity_id",
            "target_user_id",
            "system_id",
            "outcome",
            "source",
            "summary",
        ]
        show_dataframe(
            filtered_events[display_columns].sort_values(
                "occurred_at",
                ascending=False,
            ),
            width="stretch",
        )
        render_csv_export_button(
            filtered_events,
            export_name="accessatlas_governance_audit_history",
            label="Download Filtered Audit History CSV",
            key="export_audit_history_csv",
            sort_by=["occurred_at", "audit_event_id"],
            help_text="Exports the currently filtered governance audit history, including structured change detail.",
        )

        with st.expander("View selected audit event details"):
            event_options = filtered_events.copy()
            event_options["event_label"] = (
                event_options["audit_event_id"].astype(str)
                + " — "
                + event_options["action"].astype(str)
                + " — "
                + event_options["summary"].astype(str)
            )
            selected_event_label = st.selectbox(
                "Select audit event",
                event_options["event_label"].tolist(),
                key="selected_audit_event",
            )
            selected_event = event_options[
                event_options["event_label"] == selected_event_label
            ].iloc[0]

            st.write(
                f"""
                **Audit Event ID:** {selected_event['audit_event_id']}  
                **Occurred At:** {selected_event['occurred_at']}  
                **Actor User ID:** {selected_event['actor_user_id'] or 'Not resolved'}  
                **Actor Role:** {selected_event['actor_role'] or 'Not resolved'}  
                **Runtime:** {selected_event['runtime']}  
                **Entity:** {selected_event['entity_type']} / {selected_event['entity_id'] or 'Not supplied'}  
                **Target User ID:** {selected_event['target_user_id'] or 'Not supplied'}  
                **System ID:** {selected_event['system_id'] or 'Not supplied'}  
                **Source:** {selected_event['source']}  
                **Outcome:** {selected_event['outcome']}
                """
            )
            st.markdown("#### Change Detail")
            st.code(selected_event["changes_json"], language="json")


    def render_administration_section():
        """Render administrative and compliance workflows for Super Administrators."""
        st.subheader("AccessAtlas App Admin")
        section_caption(
            "Review compliance monitoring, system administrator assignment coverage, "
            "and governance audit history."
        )

        compliance_tab, admins_tab, audit_tab = st.tabs(
            [
                "Compliance Monitoring",
                "System Administrator Assignments",
                "Governance Audit History",
            ]
        )

        with compliance_tab:
            render_compliance_tab()

        with admins_tab:
            render_system_admins_tab()

        with audit_tab:
            render_audit_history_tab()


    TAB_RENDERERS = {
        "Dashboard": render_dashboard_section,
        "My Access": render_my_record_tab,
        "Manage Access": render_manage_access_section,
        "Access Reconciliation": render_review_changes_section,
        "AccessAtlas App Admin": render_administration_section,
    }

    active_tabs = [tab_name for tab_name in TAB_LABELS if tab_name in visible_tabs]
    active_tab_labels = [section_label(tab_name) for tab_name in active_tabs]

    selected_section_label = st.radio(
        "Application section",
        active_tab_labels,
        horizontal=True,
        key="active_application_section",
    )

    selected_section = section_name_from_label(selected_section_label)

    if runtime.section_guidance_renderer is not None:
        runtime.section_guidance_renderer(selected_section)

    log_event(
        logger,
        logging.INFO,
        "section_rendered",
        "Application section selected for rendering.",
        section=selected_section,
    )
    TAB_RENDERERS[selected_section]()


# === Streamlit application entry point ===
run_app(build_starter_runtime)
