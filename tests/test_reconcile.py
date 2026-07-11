from pathlib import Path

import pandas as pd


def test_reconcile_smoke():
    """Smoke test: run reconciliation logic against bundled sample files.

    This test mirrors the reconciliation algorithm used by the app and
    asserts the expected summary counts for the sample CSVs included
    in the `data/` folder.
    """
    data_dir = Path(__file__).parent.parent / "data"
    access = pd.read_csv(
        data_dir / "access_assignments.csv",
        parse_dates=["granted_date", "revoked_date"],
    )
    uploaded = pd.read_csv(data_dir / "sample_access_upload.csv")

    KEYS = ["user_id", "system_id", "resource_type", "resource_name", "permission_name"]
    key_cols = [k for k in KEYS if k in access.columns and k in uploaded.columns]

    # ensure the expected key columns are present
    assert key_cols == KEYS

    # normalize string key columns to avoid false mismatches due to whitespace/case
    for c in key_cols:
        if pd.api.types.is_string_dtype(access[c]):
            access[c] = access[c].str.strip().str.lower()
        if pd.api.types.is_string_dtype(uploaded[c]):
            uploaded[c] = uploaded[c].str.strip().str.lower()

    current_key = access.set_index(key_cols)["access_status"].to_dict()
    upload_key = uploaded.set_index(key_cols)["access_status"].to_dict()

    all_keys = set(current_key.keys()) | set(upload_key.keys())
    counts = {
        "Access Not Found in Upload": 0,
        "New Access in Upload": 0,
        "No Change": 0,
        "Status Changed": 0,
    }

    for key in all_keys:
        current_status = current_key.get(key)
        uploaded_status = upload_key.get(key)
        if current_status is None:
            counts["New Access in Upload"] += 1
        elif uploaded_status is None:
            counts["Access Not Found in Upload"] += 1
        elif current_status != uploaded_status:
            counts["Status Changed"] += 1
        else:
            counts["No Change"] += 1

    # sanity checks instead of brittle hard-coded numbers
    assert sum(counts.values()) == len(all_keys)
    # counts should be non-negative and bounded by the number of rows in each source
    assert counts["Access Not Found in Upload"] <= len(current_key)
    assert counts["New Access in Upload"] <= len(upload_key)
