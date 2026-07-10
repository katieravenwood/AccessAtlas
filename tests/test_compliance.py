"""Tests for AccessAtlas compliance calculations and normalization."""

from datetime import date

import pandas as pd
from accessatlas.compliance import (
    add_expirations,
    compliance_status,
    get_expired_follow_up_records,
    normalize_date_value,
    uploaded_dates_compliance_status,
)
from accessatlas.config import (
    ANNUAL_TRAINING_VALID_YEARS,
    BIENNIAL_TRAINING_VALID_YEARS,
    EXPIRING_SOON_DAYS,
)


def _row(annual_date, biennial_date):
    return pd.Series(
        {
            "annual_training_date": pd.Timestamp(annual_date),
            "biennial_training_date": pd.Timestamp(biennial_date),
        }
    )


def test_compliance_status_returns_expired_when_annual_training_expired():
    today = pd.Timestamp(date.today())
    annual = today - pd.DateOffset(years=ANNUAL_TRAINING_VALID_YEARS, days=1)
    biennial = today

    assert compliance_status(_row(annual, biennial)) == "Expired"


def test_compliance_status_returns_expiring_soon_at_warning_boundary():
    today = pd.Timestamp(date.today())
    annual_expiration = today + pd.Timedelta(days=EXPIRING_SOON_DAYS)
    annual = annual_expiration - pd.DateOffset(years=ANNUAL_TRAINING_VALID_YEARS)
    biennial = today

    assert compliance_status(_row(annual, biennial)) == "Expiring Soon"


def test_compliance_status_returns_current_for_valid_training_dates():
    today = pd.Timestamp(date.today())

    assert compliance_status(_row(today, today)) == "Current"


def test_add_expirations_does_not_mutate_source_dataframe():
    users = pd.DataFrame(
        [
            {
                "user_id": "USR00001",
                "annual_training_date": pd.Timestamp(date.today()),
                "biennial_training_date": pd.Timestamp(date.today()),
            }
        ]
    )

    result = add_expirations(users)

    assert "annual_training_expiration" not in users.columns
    assert "biennial_training_expiration" not in users.columns
    assert result.iloc[0]["compliance_status"] == "Current"


def test_add_expirations_uses_configured_validity_periods():
    annual = pd.Timestamp("2025-01-15")
    biennial = pd.Timestamp("2024-03-20")
    users = pd.DataFrame(
        [
            {
                "user_id": "USR00001",
                "annual_training_date": annual,
                "biennial_training_date": biennial,
            }
        ]
    )

    result = add_expirations(users)

    assert result.iloc[0]["annual_training_expiration"] == (
        annual + pd.DateOffset(years=ANNUAL_TRAINING_VALID_YEARS)
    )
    assert result.iloc[0]["biennial_training_expiration"] == (
        biennial + pd.DateOffset(years=BIENNIAL_TRAINING_VALID_YEARS)
    )


def test_follow_up_records_return_one_row_per_expired_requirement():
    yesterday = pd.Timestamp(date.today()) - pd.Timedelta(days=1)
    future = pd.Timestamp(date.today()) + pd.Timedelta(days=30)
    users = pd.DataFrame(
        [
            {
                "user_id": "USR00001",
                "display_name": "Alex Example",
                "email": "alex@example.test",
                "annual_training_expiration": yesterday,
                "biennial_training_expiration": yesterday,
            },
            {
                "user_id": "USR00002",
                "display_name": "Casey Example",
                "email": "casey@example.test",
                "annual_training_expiration": future,
                "biennial_training_expiration": future,
            },
        ]
    )

    result = get_expired_follow_up_records(users)

    assert len(result) == 2
    assert set(result["record_type"]) == {"Annual Training", "Biennial Training"}
    assert set(result["user_id"]) == {"USR00001"}


def test_normalize_date_value_handles_blank_null_and_timestamp():
    assert normalize_date_value("") == ""
    assert normalize_date_value(pd.NaT) == ""
    assert normalize_date_value(pd.Timestamp("2026-07-09 15:30:00")) == "2026-07-09"


def test_uploaded_dates_missing_training_date_is_expired():
    result = uploaded_dates_compliance_status(
        {
            "annual_training_date": "",
            "biennial_training_date": pd.Timestamp(date.today()),
        }
    )

    assert result == "Expired"
