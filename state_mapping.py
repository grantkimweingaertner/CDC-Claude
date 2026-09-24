"""
Static mapping between full state names (as they appear in the CDC natality
file) and USPS two-letter abbreviations.

A hardcoded dict is used instead of an external package (e.g. `us`) so the
app has no extra dependency and so "District of Columbia" is guaranteed to
resolve correctly for Plotly's choropleth (which expects USPS codes for
locationmode="USA-states").
"""

STATE_TO_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
}

# States that Plotly's built-in USA-states choropleth cannot render as a
# filled polygon (DC has no shape in that basemap; it shows as a point/marker
# only in some Plotly versions). Flag it so the UI can add a caveat.
CHOROPLETH_LIMITED = {"District of Columbia"}

# Chronological month order, used everywhere a month axis or category list
# is built so charts never fall back to alphabetical order.
MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def abbr(state_name: str) -> str:
    """Return the USPS abbreviation for a state name, or the input unchanged
    if it is not recognized (keeps the app from crashing on unexpected data)."""
    return STATE_TO_ABBR.get(state_name, state_name)
