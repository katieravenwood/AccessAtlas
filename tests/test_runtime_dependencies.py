"""Runtime dependency regression tests for UI-adjacent library features."""

import pandas as pd


def test_pandas_styler_is_available_for_compliance_tables():
    """Accessing DataFrame.style should work in the declared app environment."""
    dataframe = pd.DataFrame([{"compliance_status": "Current", "users": 1}])

    styler = dataframe.style.apply(
        lambda frame: pd.DataFrame(
            "",
            index=frame.index,
            columns=frame.columns,
        ),
        axis=None,
    )

    assert styler.data.equals(dataframe)
