"""Tests for AccessAtlas structured application logging."""

from __future__ import annotations

import json
import logging

from accessatlas.logging_config import (
    LOGGER_NAMESPACE,
    configure_logging,
    get_logger,
    log_event,
    reset_runtime_log_context,
    set_runtime_log_context,
)


def _accessatlas_handlers():
    logger = logging.getLogger(LOGGER_NAMESPACE)
    return [
        handler
        for handler in logger.handlers
        if getattr(handler, "_accessatlas_handler", False)
    ]


def test_configure_logging_does_not_add_duplicate_handlers():
    configure_logging(level="INFO", output_format="json")
    configure_logging(level="DEBUG", output_format="text")

    handlers = _accessatlas_handlers()
    assert len(handlers) == 1
    assert logging.getLogger(LOGGER_NAMESPACE).level == logging.DEBUG


def test_json_log_contains_event_and_runtime_context():
    configure_logging(level="INFO", output_format="json")
    reset_runtime_log_context()
    set_runtime_log_context(
        runtime_name="starter",
        application_role="System Administrator",
    )

    handler = _accessatlas_handlers()[0]
    record = logging.LogRecord(
        name="accessatlas.tests",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Structured test event.",
        args=(),
        exc_info=None,
    )
    record.event_name = "test_event"
    record.event_fields = {"record_count": 7}

    for record_filter in handler.filters:
        assert record_filter.filter(record)

    payload = json.loads(handler.formatter.format(record))

    assert payload["event"] == "test_event"
    assert payload["runtime"] == "starter"
    assert payload["application_role"] == "System Administrator"
    assert payload["fields"]["record_count"] == 7


def test_logging_configuration_falls_back_for_invalid_values():
    configure_logging(level="NOT_A_LEVEL", output_format="not-a-format")

    logger = logging.getLogger(LOGGER_NAMESPACE)
    handlers = _accessatlas_handlers()

    assert logger.level == logging.INFO
    assert handlers[0].formatter.__class__.__name__ == "JsonFormatter"
