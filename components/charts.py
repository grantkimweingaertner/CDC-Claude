"""
Chart-building functions.

Each function takes the already-filtered DataFrame and returns a Plotly
Figure. Keeping figure construction here (separate from where it's rendered
in app.py) keeps each function independently testable and readable.

Shared conventions across all charts:
- Full axes starting at zero (no truncated axes that exaggerate differences).
- Thousands separators in tooltips and axis ticks.
- Colorblind-friendly palettes (Plotly's Viridis / Okabe-Ito-style qualitative set).
- Explicit, descriptive titles rather than defaults.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.state_mapping import CHOROPLETH_LIMITED, MONTH_ORDER, abbr

# Colorblind-safe qualitative palette for the two sex categories.
SEX_COLORS = {"Female": "#D55E00", "Male": "#0072B2"}


def _empty_figure(message: str) -> go.Figure:
    """A blank figure with a centered message, shown when a filter selection
    produces no rows, so a chart area never renders as a confusing blank."""
    fig = go.Figure()
    fig.add_annotation(
        text=message, x=0.5, y=0.5, xref="paper", yref="paper",
        showarrow=False, font=dict(size=16, color="gray"),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(height=350, margin=dict(t=40, b=20))
    return fig


def monthly_trend(df: pd.DataFrame) -> go.Figure:
    """Line chart of total births per month, in calendar order."""
    if df.empty:
        return _empty_figure("No data for the current filter selection.")

    monthly = df.groupby("month", observed=True)["births"].sum().reindex(MONTH_ORDER).dropna()
    fig = px.line(
        x=monthly.index, y=monthly.values, markers=True,
        labels={"x": "Month", "y": "Total births"},
        title="Monthly Birth Trend (Selected Geographies & Sexes)",
    )
    fig.update_traces(hovertemplate="%{x}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    return fig


def sex_comparison(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing female vs. male births by month."""
    if df.empty:
        return _empty_figure("No data for the current filter selection.")

    grouped = (
        df.groupby(["month", "sex_of_infant"], observed=True)["births"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        grouped, x="month", y="births", color="sex_of_infant", barmode="group",
        category_orders={"month": MONTH_ORDER},
        color_discrete_map=SEX_COLORS,
        labels={"month": "Month", "births": "Total births", "sex_of_infant": "Infant sex"},
        title="Female vs. Male Births by Month",
    )
    fig.update_traces(hovertemplate="%{x}<br>Births: %{y:,}<extra></extra>")
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    return fig


def state_ranking(df: pd.DataFrame, top_n: int | None = None) -> go.Figure:
    """Horizontal bar chart ranking geographies by total births (descending).

    Horizontal orientation avoids cramped, unreadable x-axis labels when
    many states are selected.
    """
    if df.empty:
        return _empty_figure("No data for the current filter selection.")

    by_state = df.groupby("state_of_residence", observed=True)["births"].sum().sort_values()
    if top_n:
        by_state = by_state.tail(top_n)

    fig = px.bar(
        x=by_state.values, y=by_state.index, orientation="h",
        labels={"x": "Total births", "y": ""},
        title="Births by Geography (Ranked)",
        height=max(400, 18 * len(by_state)),
    )
    fig.update_traces(hovertemplate="%{y}<br>Births: %{x:,}<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",")
    return fig


def state_choropleth(df: pd.DataFrame) -> go.Figure:
    """US choropleth map of total births by state."""
    if df.empty:
        return _empty_figure("No data for the current filter selection.")

    by_state = df.groupby("state_of_residence", observed=True)["births"].sum().reset_index()
    by_state["abbr"] = by_state["state_of_residence"].apply(abbr)

    fig = px.choropleth(
        by_state, locations="abbr", locationmode="USA-states",
        color="births", scope="usa", color_continuous_scale="Viridis",
        hover_name="state_of_residence",
        labels={"births": "Total births"},
        title="Total Births by State (Selected Filters)",
    )
    fig.update_traces(hovertemplate="%{hovertext}<br>Births: %{z:,}<extra></extra>")
    fig.update_layout(coloraxis_colorbar=dict(tickformat=","))

    if any(s in CHOROPLETH_LIMITED for s in by_state["state_of_residence"]):
        fig.add_annotation(
            text="Note: DC is not rendered as a filled shape on this base map.",
            x=0.5, y=-0.05, xref="paper", yref="paper", showarrow=False,
            font=dict(size=11, color="gray"),
        )
    return fig


def state_month_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap of births with states on one axis and months (in calendar
    order) on the other."""
    if df.empty:
        return _empty_figure("No data for the current filter selection.")

    pivot = (
        df.groupby(["state_of_residence", "month"], observed=True)["births"]
        .sum()
        .unstack("month")
        .reindex(columns=MONTH_ORDER)
    )
    # Order states by total births so the heatmap reads top-to-bottom by magnitude.
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

    fig = px.imshow(
        pivot, color_continuous_scale="Viridis", aspect="auto",
        labels=dict(x="Month", y="", color="Births"),
        title="Births by State and Month",
        height=max(400, 16 * len(pivot)),
    )
    fig.update_traces(hovertemplate="%{y}, %{x}<br>Births: %{z:,}<extra></extra>")
    fig.update_layout(coloraxis_colorbar=dict(tickformat=","))
    return fig


def top_bottom_comparison(df: pd.DataFrame, n: int = 5) -> go.Figure:
    """Side-by-side comparison of the top-N and bottom-N geographies by
    total births within the current selection."""
    if df.empty:
        return _empty_figure("No data for the current filter selection.")

    by_state = df.groupby("state_of_residence", observed=True)["births"].sum().sort_values(ascending=False)
    n = min(n, len(by_state) // 2) if len(by_state) >= 2 else len(by_state)
    n = max(n, 1)

    top = by_state.head(n).reset_index()
    top["group"] = f"Top {n}"
    bottom = by_state.tail(n).reset_index()
    bottom["group"] = f"Bottom {n}"
    combined = pd.concat([top, bottom])

    fig = px.bar(
        combined, x="births", y="state_of_residence", color="group",
        orientation="h",
        labels={"births": "Total births", "state_of_residence": "", "group": ""},
        title=f"Top {n} vs. Bottom {n} Geographies by Total Births",
        color_discrete_sequence=["#0072B2", "#D55E00"],
    )
    fig.update_traces(hovertemplate="%{y}<br>Births: %{x:,}<extra></extra>")
    fig.update_xaxes(rangemode="tozero", tickformat=",")
    fig.update_layout(legend_title_text="")
    return fig
