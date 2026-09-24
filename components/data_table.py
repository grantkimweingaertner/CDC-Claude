"""Searchable data table and CSV download for the currently filtered data."""

import pandas as pd
import streamlit as st


def render_data_table(filtered: pd.DataFrame) -> None:
    if filtered.empty:
        st.warning("No data matches the current filters.")
        return

    st.markdown(f"**{len(filtered):,} rows** match the current filters.")

    search = st.text_input(
        "Search by state name",
        placeholder="e.g. Texas",
        help="Filters the table below to states containing this text.",
    )

    display_df = filtered.sort_values(["state_of_residence", "month"])
    if search:
        display_df = display_df[
            display_df["state_of_residence"].str.contains(search, case=False, na=False)
        ]

    display_df = display_df[
        ["state_of_residence", "month", "sex_of_infant", "births"]
    ].rename(columns={
        "state_of_residence": "State",
        "month": "Month",
        "sex_of_infant": "Sex",
        "births": "Births",
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Births": st.column_config.NumberColumn("Births", format="%d"),
        },
    )

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_bytes,
        file_name="filtered_natality_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
