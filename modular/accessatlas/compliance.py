"""AccessAtlas application module."""

from datetime import date

import pandas as pd

from accessatlas.config import ANNUAL_TRAINING_VALID_YEARS, BIENNIAL_TRAINING_VALID_YEARS, EXPIRING_SOON_DAYS

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
