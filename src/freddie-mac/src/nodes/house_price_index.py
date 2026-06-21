"""FMHPI: Freddie Mac House Price Index.

Monthly single-family home price index at national (US), state, and metro (CBSA)
levels; not-seasonally-adjusted and seasonally-adjusted; base period Jan 2000 =
100; from 1975. One stable bulk CSV (~16MB), re-pulled in full each run.

Quirks: the date is split across Year + Month columns, and '.' marks a missing
GEO_Code on US / State rows.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_csv, to_float

FMHPI_URL = "https://www.freddiemac.com/fmac-resources/research/docs/fmhpi_master_file.csv"

FMHPI_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("geo_type", pa.string()),
    ("geo_name", pa.string()),
    ("geo_code", pa.string()),
    ("index_nsa", pa.float64()),
    ("index_sa", pa.float64()),
])


def _to_int(value):
    s = (value or "").strip()
    if s == "":
        return None
    return int(float(s))


def fetch_house_price_index(node_id: str) -> None:
    asset = node_id
    reader = csv.DictReader(io.StringIO(fetch_csv(FMHPI_URL)))
    cols = {name: [] for name in FMHPI_SCHEMA.names}
    for row in reader:
        cols["year"].append(_to_int(row.get("Year")))
        cols["month"].append(_to_int(row.get("Month")))
        cols["geo_type"].append((row.get("GEO_Type") or "").strip() or None)
        cols["geo_name"].append((row.get("GEO_Name") or "").strip() or None)
        code = (row.get("GEO_Code") or "").strip()
        cols["geo_code"].append(None if code in ("", ".") else code)
        cols["index_nsa"].append(to_float(row.get("Index_NSA")))
        cols["index_sa"].append(to_float(row.get("Index_SA")))
    table = pa.table(cols, schema=FMHPI_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="freddie-mac-house-price-index", fn=fetch_house_price_index, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freddie-mac-house-price-index-transform",
        deps=["freddie-mac-house-price-index"],
        sql='''
            SELECT
                make_date(year, month, 1)        AS date,
                geo_type,
                geo_name,
                geo_code,
                index_nsa,
                index_sa
            FROM "freddie-mac-house-price-index"
            WHERE index_nsa IS NOT NULL
              AND index_sa IS NOT NULL
        ''',
    ),
]
