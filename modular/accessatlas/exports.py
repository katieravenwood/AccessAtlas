"""CSV export preparation for AccessAtlas governance datasets."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from accessatlas.logging_config import get_logger, log_exception

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
            column for column in requested_columns if column not in export_frame.columns
        ]
        if missing_columns:
            raise ValueError(
                "Export columns are missing from the dataframe: " + ", ".join(missing_columns)
            )
        export_frame = export_frame[requested_columns]

    if sort_by is not None:
        sort_columns = [column for column in sort_by if column in export_frame.columns]
        if sort_columns:
            export_frame = export_frame.sort_values(
                sort_columns,
                kind="stable",
            )

    object_columns = export_frame.select_dtypes(include=["object", "string"]).columns
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
