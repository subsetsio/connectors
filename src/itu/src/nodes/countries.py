"""ITU DataHub — countries subset.

Reference table of ~236 economies + their classifications, sourced from
GET /v2/country/all. Stateless full re-pull each refresh.
"""

import json

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import _get_json

_COUNTRIES_SCHEMA = pa.schema([
    ("country_id", pa.int64()),
    ("iso", pa.string()),
    ("short_name", pa.string()),
    ("long_name", pa.string()),
    ("classifications", pa.string()),  # JSON array of the economy's regions
])


def fetch_countries(node_id: str) -> None:
    asset = node_id
    rows = _get_json("country/all")
    cols = {k: [] for k in _COUNTRIES_SCHEMA.names}
    for r in rows:
        cols["country_id"].append(r.get("CountryID"))
        cols["iso"].append(r.get("IsoCode"))
        cols["short_name"].append(r.get("ShortName"))
        cols["long_name"].append(r.get("LongName"))
        cols["classifications"].append(json.dumps(r.get("Regions", []), ensure_ascii=False))
    table = pa.table(cols, schema=_COUNTRIES_SCHEMA)
    save_raw_parquet(table, asset)
