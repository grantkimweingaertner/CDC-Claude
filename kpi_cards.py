"""Top KPI row: five headline metrics computed from the filtered DataFrame."""

import pandas as pd
import streamlit as st


def render_kpi_cards(filtered: pd.DataFrame) -> None:
    if filtered.empty:
        st.warning("No data matches the current filters. Adjust your selections to see KPIs.")
        return

    total_births = int(filtered["births"].sum())
    n_geographies = filtered["state_of_residence"].nunique()

    by_month = filtered.groupby("month", observed=True)["births"].sum()
    avg_births_per_month = by_month.mean() if not by_month.empty else 0
    top_month = by_month.idxmax() if not by_month.empty else "N/A"
    top_month_value = by_month.max() if not by_month.empty else 0

    by_state = filtered.groupby("state_of_residence", observed=True)["births"].sum()
    top_state = by_state.idxmax() if not by_state.empty else "N/A"
    top_state_value = by_state.max() if not by_state.empty else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total births", f"{total_births:,}")
    c2.metric("Geographies selected", f"{n_geographies:,}")
    c3.metric("Avg births / month", f"{avg_births_per_month:,.0f}")
    c4.metric("Top geography", top_state, f"{top_state_value:,} births")
    c5.metric("Top month", str(top_month), f"{top_month_value:,} births")
