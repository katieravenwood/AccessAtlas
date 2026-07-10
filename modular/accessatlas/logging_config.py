"""Structured application logging for AccessAtlas.

Application logs support troubleshooting and runtime observability. They are
deliberately separate from governance audit events, which record user and
administrative actions.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any, Mapping

LOG_LEVEL_ENV = "ACCESSATLAS_LOG_LEVEL"
LOG_FORMAT_ENV = "ACCESSATLAS_LOG_FORMAT"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "json"
LOGGER_NAMESPACE = "accessatlas"

_runtime_name: ContextVar[str] = ContextVar("accessatlas_runtime_name", default="unresolved")
_application_role: ContextVar[str] = ContextVar(
    "accessatlas_application_role", default="unresolved"
)

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

    selected_format = _normalize_log_format(output_format or os.getenv(LOG_FORMAT_ENV))
    formatter: logging.Formatter = JsonFormatter() if selected_format == "json" else TextFormatter()

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
