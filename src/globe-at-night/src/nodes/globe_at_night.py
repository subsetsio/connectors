"""GLOBE at Night — citizen-science night-sky-brightness observations.

Single homogeneous corpus published as one CSV per calendar year at
https://globeatnight.org/documents/{doc_id}/GaN{YEAR}.csv. The {doc_id} per
year is arbitrary and not derivable, so we scrape the maps-data landing page
(which lists every year's CSV link in its HTML) to discover the full year set
dynamically — picking up new years for free, no hardcoded year range. All years
share one schema, so they merge into one raw asset and one published table.

Shape: stateless full re-pull. The whole corpus is ~250k-300k rows / a few tens
of MB — cheap to re-fetch in full every run, which also picks up late
corrections to prior years for free. No incremental query is supported by the
source anyway (no date/cursor params; granularity is the whole-year file).
"""
import csv
import io
import re

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    configure_http,
    get,
    save_raw_parquet,
)

MAPS_DATA_URL = "https://globeatnight.org/maps-data/"
DOC_URL = "https://globeatnight.org/documents/{doc_id}/GaN{year}.csv"
# The landing page 403s to non-browser user agents; the /documents/ file URLs
# serve fine to any client, but we set a browser-like UA once so both work.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# Source CSV header -> our snake_case raw column name. Order is the raw schema.
COLUMN_MAP = [
    ("ID", "id"),
    ("ObsType", "obs_type"),
    ("Latitude", "latitude"),
    ("Longitude", "longitude"),
    ("Elevation(m)", "elevation_m"),
    ("LocalDate", "local_date"),
    ("LocalTime", "local_time"),
    ("UTDate", "ut_date"),
    ("UTTime", "ut_time"),
    ("LimitingMag", "limiting_mag"),
    ("SQMReading", "sqm_reading"),
    ("SQMSerial", "sqm_serial"),
    ("CloudCover", "cloud_cover"),
    ("Constellation", "constellation"),
    ("SkyComment", "sky_comment"),
    ("LocationComment", "location_comment"),
    ("Country", "country"),
]

# Raw is kept faithful to the source: every column a string (many fields are
# blank, e.g. SQMReading). The transform does the typing.
RAW_SCHEMA = pa.schema(
    [(dst, pa.string()) for _src, dst in COLUMN_MAP] + [("file_year", pa.string())]
)


def _get(url: str) -> "object":
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp


def _discover_year_urls() -> dict:
    """Scrape the maps-data page for every GaN{year}.csv link. Returns
    {year: full_url}. Raises if none are found — never silently empty."""
    html = _get(MAPS_DATA_URL).text
    found = {}
    for doc_id, year in re.findall(r"/documents/(\d+)/GaN(\d{4})\.csv", html):
        # If a year appears twice, keep the first (page lists each once).
        found.setdefault(year, DOC_URL.format(doc_id=doc_id, year=year))
    if not found:
        raise RuntimeError(
            f"no GaN CSV links discovered at {MAPS_DATA_URL}; page format changed"
        )
    return found


def fetch_observations(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    configure_http(headers={"User-Agent": BROWSER_UA})

    year_urls = _discover_year_urls()
    cols = {dst: [] for _src, dst in COLUMN_MAP}
    cols["file_year"] = []

    for year, url in sorted(year_urls.items()):
        text = _get(url).text
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            for src, dst in COLUMN_MAP:
                val = row.get(src)
                cols[dst].append(val if val not in ("", None) else None)
            cols["file_year"].append(year)

    table = pa.table(
        {name: pa.array(cols[name], type=pa.string()) for name in cols},
        schema=RAW_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="globe-at-night-observations", fn=fetch_observations, kind="download"),
]
