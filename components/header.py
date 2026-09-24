"""Top-of-page header: title, explainer, and required data caveats."""

import streamlit as st


def render_header() -> None:
    st.title("U.S. Births by State, Month, and Infant Sex (2025)")

    st.markdown(
        "Explore how reported births vary across **states, months, and "
        "infant sex** using 2025 provisional data from the CDC. Use the "
        "filters in the sidebar to narrow the view, then explore the tabs "
        "below for geographic and time-based patterns."
    )

    st.info(
        "**Source:** U.S. Centers for Disease Control and Prevention (CDC), "
        "National Center for Health Statistics — provisional natality data.",
        icon="📊",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.warning(
            "**Provisional data.** These are early, unfinalized 2025 figures "
            "and are subject to revision as more complete records are processed.",
            icon="⚠️",
        )
    with col2:
        st.warning(
            "**Counts, not rates.** Values shown are raw birth *counts*, not "
            "birth *rates*. Larger states will show more births simply because "
            "they have larger populations — this does not imply a higher "
            "fertility rate.",
            icon="⚠️",
        )

    st.divider()
