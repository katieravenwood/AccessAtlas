"""Tests for AccessAtlas CSV export preparation."""

from io import BytesIO

import pandas as pd
import pytest
from accessatlas.exports import (
    prepare_csv_export,
    prepare_export_dataframe,
)


def test_prepare_csv_export_uses_utf8_bom_and_no_index():
    dataframe = pd.DataFrame(
        [
            {"user_id": "USR00002", "display_name": "Zoë Example"},
            {"user_id": "USR00001", "display_name": "Alex Example"},
        ]
    )

    artifact = prepare_csv_export(
        dataframe,
        export_name="AccessAtlas Users",
        sort_by=["user_id"],
    )

    assert artifact.filename == "AccessAtlas_Users.csv"
    assert artifact.mime_type == "text/csv"
    assert artifact.record_count == 2
    assert artifact.column_count == 2
    assert artifact.data.startswith(b"\xef\xbb\xbf")

    exported = pd.read_csv(BytesIO(artifact.data))
    assert exported["user_id"].tolist() == ["USR00001", "USR00002"]
    assert "Unnamed: 0" not in exported.columns


def test_export_preserves_requested_column_order():
    dataframe = pd.DataFrame(
        [{"user_id": "USR00001", "email": "user@example.test", "status": "Active"}]
    )

    export_frame = prepare_export_dataframe(
        dataframe,
        columns=["status", "user_id"],
    )

    assert list(export_frame.columns) == ["status", "user_id"]


def test_export_rejects_missing_requested_columns():
    dataframe = pd.DataFrame([{"user_id": "USR00001"}])

    with pytest.raises(ValueError, match="missing from the dataframe"):
        prepare_export_dataframe(
            dataframe,
            columns=["user_id", "system_id"],
        )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("=1+1", "'=1+1"),
        ("+SUM(A1:A2)", "'+SUM(A1:A2)"),
        ("-10+20", "'-10+20"),
        ("@cmd", "'@cmd"),
        ("Normal value", "Normal value"),
    ],
)
def test_export_sanitizes_formula_style_text(value, expected):
    dataframe = pd.DataFrame([{"resource_name": value}])

    export_frame = prepare_export_dataframe(dataframe)

    assert export_frame.iloc[0]["resource_name"] == expected


def test_prepare_export_does_not_mutate_source_dataframe():
    dataframe = pd.DataFrame([{"resource_name": "=1+1"}])

    prepare_export_dataframe(dataframe)

    assert dataframe.iloc[0]["resource_name"] == "=1+1"
