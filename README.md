# U.S. Births Dashboard (2025)

A Streamlit dashboard exploring 2025 provisional U.S. natality data by
state, month, and infant sex. Built for undergraduate business analytics
students to practice reading interactive geographic and time-series
visualizations.

## Data

CDC National Center for Health Statistics, provisional 2025 natality data.
Figures are **birth counts**, not birth rates, and are **provisional** —
subject to revision. See the "About the Data" tab in the app for details.

## Project structure

```
natality_dashboard/
├── app.py                      # Entry point
├── data/
│   └── Provisional_Natality_2025_CDC.csv
├── utils/
│   ├── data_loader.py          # Cached CSV loading + validation
│   ├── state_mapping.py        # State name -> USPS abbreviation, month order
│   └── filters.py              # Sidebar filter widgets
├── components/
│   ├── header.py                # Title, attribution, data caveats
│   ├── kpi_cards.py              # Headline KPI metrics
│   ├── charts.py                 # All Plotly chart builders
│   └── data_table.py             # Searchable table + CSV download
└── requirements.txt
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Push this folder to a GitHub repository (keep `data/` alongside `app.py`).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app
   pointing at the repo, branch, and `app.py` as the main file.
3. No secrets or extra configuration are required — the data file is loaded
   locally from the repo and the file path in `utils/data_loader.py` is
   resolved relative to the script, so it works the same way locally and in
   the cloud.

## Notes

- Month ordering is enforced everywhere (charts, groupings, KPIs) via an
  ordered pandas `Categorical`, so nothing ever falls back to alphabetical
  order.
- The choropleth map cannot render the District of Columbia as a filled
  shape (a limitation of Plotly's built-in USA-states base map); DC is
  still included in every other chart, KPI, and the data table.
- Data-validation warnings (unexpected row counts, nulls, out-of-range
  values, etc.) surface as sidebar warnings rather than crashing the app.
