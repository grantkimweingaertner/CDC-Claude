"""
Sidebar filter controls.

All filter state lives in st.session_state so "Select All" and "Reset
Filters" buttons can programmatically change widget values (a plain widget
`default=` argument can't be changed after first render).
"""

import pandas as pd
import streamlit as st

from utils.state_mapping import MONTH_ORDER

STATE_KEY = "filter_states"
MONTH_KEY = "filter_months"
SEX_KEY = "filter_sexes"

ALL_SEXES = ["Female", "Male"]


def _init_state(all_states: list[str]) -> None:
    """Populate session_state with default (all-selected) filter values the
    first time the app runs, without overwriting a returning user's choices."""
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = list(all_states)
    if MONTH_KEY not in st.session_state:
        st.session_state[MONTH_KEY] = list(MONTH_ORDER)
    if SEX_KEY not in st.session_state:
        st.session_state[SEX_KEY] = list(ALL_SEXES)


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render all sidebar filter widgets and return the filtered DataFrame."""
    all_states = sorted(df["state_of_residence"].unique())
    _init_state(all_states)

    st.sidebar.header("Filters")

    # --- Geography -------------------------------------------------------
    col_a, col_b = st.sidebar.columns([3, 1])
    col_a.markdown("**States / geographies**")
    if col_b.button("All", key="select_all_states", help="Select all states"):
        st.session_state[STATE_KEY] = list(all_states)
    selected_states = st.sidebar.multiselect(
        "States / geographies", options=all_states, key=STATE_KEY,
        label_visibility="collapsed",
    )

    # --- Month -------------------------------------------------------------
    col_c, col_d = st.sidebar.columns([3, 1])
    col_c.markdown("**Months**")
    if col_d.button("All", key="select_all_months", help="Select all months"):
        st.session_state[MONTH_KEY] = list(MONTH_ORDER)
    selected_months = st.sidebar.multiselect(
        "Months", options=MONTH_ORDER, key=MONTH_KEY,
        label_visibility="collapsed",
    )

    # --- Sex -----------------------------------------------------------
    st.sidebar.markdown("**Infant sex**")
    selected_sexes = st.sidebar.multiselect(
        "Infant sex", options=ALL_SEXES, key=SEX_KEY,
        label_visibility="collapsed",
    )

    st.sidebar.divider()
    if st.sidebar.button("Reset filters", use_container_width=True):
        st.session_state[STATE_KEY] = list(all_states)
        st.session_state[MONTH_KEY] = list(MONTH_ORDER)
        st.session_state[SEX_KEY] = list(ALL_SEXES)
        st.rerun()

    # --- Active filter summary ------------------------------------------
    st.sidebar.divider()
    n_states, n_all_states = len(selected_states), len(all_states)
    n_months = len(selected_months)
    sex_label = (
        "Both" if set(selected_sexes) == set(ALL_SEXES)
        else (selected_sexes[0] if selected_sexes else "None")
    )
    st.sidebar.caption(
        f"**Active filters:** {n_states}/{n_all_states} states · "
        f"{n_months}/12 months · sex: {sex_label}"
    )

    filtered = df[
        df["state_of_residence"].isin(selected_states)
        & df["month"].isin(selected_months)
        & df["sex_of_infant"].isin(selected_sexes)
    ]
    return filtered
