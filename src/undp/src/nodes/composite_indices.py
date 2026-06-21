"""UNDP composite indices — HDRO "Composite indices complete time series" CSV.

A single wide CSV (one row per country/aggregate, columns = <indicator>_<year>)
is fetched and unpivoted to long form (iso3, country, hdicode, region,
indicator, year, value). Covers HDI, IHDI, GDI, GII, PHDI and all their
components, 1990 onward.

Static, versioned bulk artefact (the year stamp in the URL is bumped by HDRO
once a year with each new Human Development Report). Full re-pull every run; the
payload is tiny (~2MB).
"""
import csv
import io
import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_bytes, num

CSV_URL = "https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Composite_indices_complete_time_series.csv"

# Identity columns in the wide composite-indices CSV — everything else is an
# <indicator>_<year> measurement column.
CI_ID_COLS = {"iso3", "country", "hdicode", "region", "hdi_rank_2023"}
_YEAR_COL_RE = re.compile(r"^(?P<stem>.+)_(?P<year>(?:19|20)\d{2})$")

CI_SCHEMA = pa.schema([
    ("iso3", pa.string()),
    ("country", pa.string()),
    ("hdicode", pa.string()),
    ("region", pa.string()),
    ("indicator", pa.string()),
    ("year", pa.int32()),
    ("value", pa.float64()),
])


def fetch_composite_indices(node_id: str) -> None:
    asset = node_id
    # HDRO publishes this CSV in Windows-1252 (accented country names like
    # "Cote d'Ivoire"), not UTF-8 — decoding as UTF-8 raises on byte 0xf4.
    raw = fetch_bytes(CSV_URL)
    text = raw.lstrip(b"\xef\xbb\xbf").decode("cp1252")
    reader = csv.reader(io.StringIO(text))
    header = next(reader)

    # Pre-compute which columns are measurements and split into (stem, year).
    measure_cols = []  # (col_index, stem, year)
    idx = {name: i for i, name in enumerate(header)}
    for i, name in enumerate(header):
        if name in CI_ID_COLS:
            continue
        m = _YEAR_COL_RE.match(name)
        if m:
            measure_cols.append((i, m.group("stem"), int(m.group("year"))))

    rows = []
    for record in reader:
        if not record or len(record) < len(header):
            continue
        iso3 = record[idx["iso3"]].strip() or None
        country = record[idx["country"]].strip() or None
        hdicode = record[idx["hdicode"]].strip() or None
        region = record[idx["region"]].strip() or None
        for col_i, stem, year in measure_cols:
            value = num(record[col_i])
            if value is None:
                continue
            rows.append({
                "iso3": iso3,
                "country": country,
                "hdicode": hdicode,
                "region": region,
                "indicator": stem,
                "year": year,
                "value": value,
            })

    if not rows:
        raise AssertionError(f"{asset}: parsed 0 observations from composite-indices CSV")
    table = pa.Table.from_pylist(rows, schema=CI_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="undp-composite-indices", fn=fetch_composite_indices, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="undp-composite-indices-transform",
        deps=["undp-composite-indices"],
        sql='''
            SELECT
                iso3,
                country,
                hdicode,
                region,
                indicator,
                CAST(year AS INTEGER) AS year,
                CAST(value AS DOUBLE) AS value
            FROM "undp-composite-indices"
            WHERE value IS NOT NULL
        ''',
    ),
]
