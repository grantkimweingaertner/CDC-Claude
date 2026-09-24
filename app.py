"""
U.S. Births by State, Month, and Infant Sex (2025) — Streamlit dashboard.

Entry point only: loads data, renders the sidebar filters, and lays out the
tabs. All computation and chart-building logic lives in utils/ and
components/ so this file stays easy to scan.

Run locally with:  streamlit run app.py
"""

import streamlit as st

from components.charts import (
    monthly_trend, sex_comparison, state_ranking,
    state_choropleth, state_month_heatmap, top_bottom_comparison,
)
from components.data_table import render_data_table
from components.header import render_header
from components.kpi_cards import render_kpi_cards
from utils.data_loader import load_data
from utils.filters import render_sidebar_filters

st.set_page_config(
    page_title="U.S. Births Dashboard (2025)",
    page_icon="👶",
    layout="wide",
)


def main() -> None:
    df = load_data()

    # Surface any data-validation issues without stopping the app.
    for warning in df.attrs.get("validation_warnings", []):
        st.sidebar.warning(warning, icon="⚠️")

    render_header()

    filtered = render_sidebar_filters(df)
    render_kpi_cards(filtered)

    st.divider()

    tab_overview, tab_geo, tab_monthly, tab_table, tab_about = st.tabs(
        ["Overview", "Geographic Analysis", "Monthly and Sex Analysis",
         "Data Table and Download", "About the Data"]
    )

    with tab_overview:
        st.markdown(
            "This tab gives a quick headline view. Use the other tabs for "
            "deeper geographic and time-based breakdowns, or the sidebar to "
            "narrow your selection."
        )
        st.plotly_chart(monthly_trend(filtered), use_container_width=True)

    with tab_geo:
        st.plotly_chart(state_choropleth(filtered), use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(state_ranking(filtered), use_container_width=True)
        with col2:
            st.plotly_chart(top_bottom_comparison(filtered), use_container_width=True)

    with tab_monthly:
        st.plotly_chart(sex_comparison(filtered), use_container_width=True)
        st.plotly_chart(state_month_heatmap(filtered), use_container_width=True)

    with tab_table:
        render_data_table(filtered)

    with tab_about:
        st.markdown(
            """
### About this data

**Source:** CDC National Center for Health Statistics — provisional 2025
natality data (births by state of residence, month, and infant sex).

**Provisional status:** These figures are early releases and may be revised
as more complete birth records are processed by the states and finalized by
the CDC.

**Counts vs. rates:** All figures in this dashboard are raw birth *counts*.
They are **not** birth rates and are not adjusted for each state's
population. A state with more births is not necessarily a state with a
higher fertility rate — it may simply have a larger population.

**Column dictionary**

| Column | Description |
|---|---|
| `state_of_residence` | U.S. state (or DC) of maternal residence |
| `month` | Calendar month of birth |
| `sex_of_infant` | Female or Male |
| `births` | Number of births reported for that state/month/sex combination |

**Known limitation:** The choropleth map uses Plotly's built-in USA-states
base map, which does not render the District of Columbia as a filled
polygon. DC's totals are still included in every other chart, KPI, and the
data table.
            """
        )


if __name__ == "__main__":
    main()
