"""Shared HTTP + parse helpers for the US Drought Monitor connector.

Source: USDM Data Services REST API (https://usdmdataservices.unl.edu/api).
Public domain, no auth. Weekly data since 2000-01-04.

The full history is retrieved in a single request per (measure, scope) using a
wide startdate/enddate window — there is no pagination, so a stateless full
re-pull each run is cheap. State-level data has no all-states endpoint, so we
iterate the 52 FIPS codes.
"""

from subsets_utils import get, transient_retry

API_BASE = "https://usdmdataservices.unl.edu/api"

# Wide window covering the full USDM history (starts 2000-01-04) through a
# comfortable future bound; the date range IS the full pull (no pagination).
START_DATE = "1/1/2000"
END_DATE = "12/31/2030"

# All US state FIPS codes including DC (11) and Puerto Rico (72).
STATE_FIPS = [
    "01", "02", "04", "05", "06", "08", "09", "10", "11", "12",
    "13", "15", "16", "17", "18", "19", "20", "21", "22", "23",
    "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
    "34", "35", "36", "37", "38", "39", "40", "41", "42", "44",
    "45", "46", "47", "48", "49", "50", "51", "53", "54", "55",
    "56", "72",
]

REGION_CODES = {
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL",
    "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA",
    "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
    "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "PR",
    "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY",
}


@transient_retry()
def fetch(path: str, aoi: str) -> list[dict]:
    resp = get(
        f"{API_BASE}/{path}",
        params={
            "aoi": aoi,
            "startdate": START_DATE,
            "enddate": END_DATE,
            "statisticsType": "1",
        },
        headers={"Accept": "application/json"},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def iso_to_date(value: str) -> str:
    """Slice an ISO-8601 datetime down to YYYY-MM-DD."""
    return value[:10]
