"""NWS public forecast zone-codebook correlation file.

Pipe-delimited text published by NWS GIS. It maps public forecast zone codes to
county FIPS/name, office, time zone, feature area, and centroid coordinates.
"""

import csv
import io
import re
from datetime import datetime

import pyarrow as pa

from subsets_utils import save_raw_parquet

from utils import _get_text, _string_table

# NWS republishes the correlation file under a new dated name (`bpDDmonYY.dbx`)
# on every zone revision and drops the old one from this index, so the URL has
# to be resolved from the listing page rather than pinned.
ZONE_COUNTY_INDEX = "https://www.weather.gov/gis/ZoneCounty"
ZONE_COUNTY_BASE = "https://www.weather.gov"
_DBX_HREF = re.compile(r'href="(/source/gis/Shapefiles/County/bp(\d{2})([a-z]{3})(\d{2})\.dbx)"')

HEADER = [
    "STATE",
    "ZONE",
    "CWA",
    "NAME",
    "STATE_ZONE",
    "COUNTY",
    "FIPS",
    "TIME_ZONE",
    "FE_AREA",
    "LAT",
    "LON",
]


def _latest_zone_county_url() -> str:
    """Newest `bpDDmonYY.dbx` linked from the NWS ZoneCounty index."""
    matches = _DBX_HREF.findall(_get_text(ZONE_COUNTY_INDEX))
    if not matches:
        raise RuntimeError(f"nws zone codebook: no .dbx link at {ZONE_COUNTY_INDEX}")
    dated = []
    for href, day, mon, year in matches:
        try:
            stamp = datetime.strptime(f"{day}{mon}{year}", "%d%b%y").date()
        except ValueError:
            continue
        dated.append((stamp, href))
    if not dated:
        raise RuntimeError(f"nws zone codebook: no parseable .dbx date at {ZONE_COUNTY_INDEX}")
    return ZONE_COUNTY_BASE + max(dated)[1]


def fetch_nws_public_forecast_zone_codebook(node_id: str) -> None:
    text = _get_text(_latest_zone_county_url(), encoding="latin-1")
    reader = csv.reader(io.StringIO(text), delimiter="|")
    schema = pa.schema([(c, pa.string()) for c in HEADER])
    table, dropped = _string_table(HEADER, reader, schema)
    if table.num_rows < 4000:
        raise RuntimeError(f"nws zone codebook: only {table.num_rows} rows")
    if dropped:
        raise RuntimeError(f"nws zone codebook: {dropped} malformed rows")
    save_raw_parquet(table, node_id)
