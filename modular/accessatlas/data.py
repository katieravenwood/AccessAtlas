"""AccessAtlas application module."""

import logging

import pandas as pd
import streamlit as st

from accessatlas.config import DATA_DIR
from accessatlas.logging_config import get_logger, log_event, log_exception

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
        dataset_counts={name: len(dataframe) for name, dataframe in datasets.items()},
    )
    return datasets
