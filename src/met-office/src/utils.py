"""Shared HTTP + station-discovery helpers for the Met Office connector.

Source: Met Office 'Historic Station Data' — monthly climate observations for
~37 long-running UK weather stations, one fixed-width plain-text file per
station at
https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/<name>data.txt

The station directory is not browsable, so the station list is discovered by
scraping anchor links on the HTML index page each run.
"""
import re

from subsets_utils import get, transient_retry

INDEX_URL = "https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data"
STATION_BASE = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata"
STATION_HREF = re.compile(r"stationdata/([a-z]+)data\.txt", re.IGNORECASE)

# Data row: 4-digit year, 1-2 digit month, then the rest of the line.
ROW_RE = re.compile(r"^\s*(\d{4})\s+(\d{1,2})\b(.*)$")


@transient_retry()
def fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def discover_station_slugs() -> list:
    html = fetch_text(INDEX_URL)
    slugs = sorted(set(m.group(1).lower() for m in STATION_HREF.finditer(html)))
    if len(slugs) < 30:
        raise AssertionError(
            f"index scrape found only {len(slugs)} stations (expected ~37); "
            "the index page layout or href pattern likely changed"
        )
    return slugs
