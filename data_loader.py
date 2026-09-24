"""
Loads and validates the CDC provisional natality CSV.

The loader is decorated with st.cache_data so the (small) CSV is only read
and processed once per session, not on every widget interaction/rerun.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.state_mapping import MONTH_ORDER

# Resolved relative to this file, not the current working directory, so the
# app finds its data whether it's run locally (`streamlit run app.py`) or
# deployed on Streamlit Community Cloud (which can have a different CWD).
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Provisional_Natality_2025_CDC.csv"

EXPECTED_COLUMNS = {
    "state_of_residence", "month", "month_code", "year_code",
    "sex_of_infant", "births",
}


@st.cache_data(show_spinner="Loading natality data...")
def load_data() -> pd.DataFrame:
    """Load the natality CSV, enforce types, and return a validated DataFrame.

    Returns a DataFrame with an added 'validation_warnings' attribute (a list
    of strings) so the caller can decide how/whether to surface issues,
    without the loader itself halting the app.
    """
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    warnings = []

    missing_cols = EXPECTED_COLUMNS - set(df.columns)
    if missing_cols:
        warnings.append(f"Missing expected column(s): {sorted(missing_cols)}")

    # Make month an ordered categorical so every groupby/sort/chart respects
    # calendar order instead of falling back to alphabetical.
    if "month" in df.columns:
        df["month"] = pd.Categorical(df["month"], categories=MONTH_ORDER, ordered=True)

    if "births" in df.columns:
        if df["births"].isnull().any():
            warnings.append("Some 'births' values are missing (null).")
        if (df["births"] < 0).any():
            warnings.append("Some 'births' values are negative, which is not valid.")
        if not pd.api.types.is_integer_dtype(df["births"]):
            # Provisional extracts occasionally load as float; coerce safely.
            df["births"] = pd.to_numeric(df["births"], errors="coerce").fillna(0).astype(int)

    if "sex_of_infant" in df.columns:
        unexpected_sexes = set(df["sex_of_infant"].dropna().unique()) - {"Female", "Male"}
        if unexpected_sexes:
            warnings.append(f"Unexpected sex_of_infant value(s): {sorted(unexpected_sexes)}")

    if "state_of_residence" in df.columns and "month" in df.columns and "sex_of_infant" in df.columns:
        n_states = df["state_of_residence"].nunique()
        n_months = df["month"].nunique()
        n_sexes = df["sex_of_infant"].nunique()
        expected_rows = n_states * n_months * n_sexes
        if len(df) != expected_rows:
            warnings.append(
                f"Row count ({len(df)}) does not match the expected "
                f"states x months x sexes combination count ({expected_rows}); "
                "some combinations may be missing or duplicated."
            )
        dup_count = df.duplicated(subset=["state_of_residence", "month", "sex_of_infant"]).sum()
        if dup_count:
            warnings.append(f"{dup_count} duplicate (state, month, sex) row(s) found.")

    df.attrs["validation_warnings"] = warnings
    return df
