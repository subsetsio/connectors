"""Park directory subset.

park-attendance-parks : the park directory from queue-times.com/parks.json
(one row per park: id, name, company, country, continent, lat/long, timezone).
Stateless — re-pulled in full every run (the corpus is tiny).
"""
import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _load_parks

PARKS_SCHEMA = pa.schema([
    ("park_id", pa.int64()),
    ("park_name", pa.string()),
    ("company", pa.string()),
    ("country", pa.string()),
    ("continent", pa.string()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("timezone", pa.string()),
])


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_parks(node_id: str) -> None:
    """Download the full park directory."""
    asset = node_id
    rows = []
    for park in _load_parks():
        rows.append({
            "park_id": int(park["id"]),
            "park_name": park.get("name"),
            "company": park.get("company"),
            "country": park.get("country"),
            "continent": park.get("continent"),
            "latitude": _to_float(park.get("latitude")),
            "longitude": _to_float(park.get("longitude")),
            "timezone": park.get("timezone"),
        })
    table = pa.Table.from_pylist(rows, schema=PARKS_SCHEMA)
    save_raw_parquet(table, asset)
