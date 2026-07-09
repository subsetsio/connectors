"""NWS public forecast zone-codebook correlation file.

Pipe-delimited text published by NWS GIS. It maps public forecast zone codes to
county FIPS/name, office, time zone, feature area, and centroid coordinates.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import save_raw_parquet

from utils import _get_text, _string_table

ZONE_COUNTY_URL = "https://www.weather.gov/source/gis/Shapefiles/County/bp16ap26.dbx"

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


def fetch_nws_public_forecast_zone_codebook(node_id: str) -> None:
    text = _get_text(ZONE_COUNTY_URL, encoding="latin-1")
    reader = csv.reader(io.StringIO(text), delimiter="|")
    schema = pa.schema([(c, pa.string()) for c in HEADER])
    table, dropped = _string_table(HEADER, reader, schema)
    if table.num_rows < 4000:
        raise RuntimeError(f"nws zone codebook: only {table.num_rows} rows")
    if dropped:
        raise RuntimeError(f"nws zone codebook: {dropped} malformed rows")
    save_raw_parquet(table, node_id)
