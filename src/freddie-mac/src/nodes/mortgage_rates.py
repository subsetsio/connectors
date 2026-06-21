"""PMMS: Freddie Mac Primary Mortgage Market Survey.

Weekly average US mortgage rates (30yr fixed, 15yr fixed, 5/1 ARM) from 1971;
the longest-running weekly survey of US mortgage rates. One stable bulk CSV
(~98KB), re-pulled in full each run.

Quirk: PMMS is a ragged CSV — the 9-column header still applies, but rows from
2022-11-17 onward carry only the first 4 columns (date, pmms30, pmms30p, pmms15)
after Freddie Mac discontinued the points/ARM series. Short rows are padded with
nulls positionally; DuckDB's read_csv would reject the inconsistent column
count, which is why parsing happens here. Dates are m/d/YYYY.
"""

import csv
import io
from datetime import datetime

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_csv, to_float

PMMS_URL = "https://www.freddiemac.com/pmms/docs/PMMS_history.csv"

PMMS_SCHEMA = pa.schema([
    ("date", pa.string()),
    ("pmms30", pa.float64()),
    ("pmms30p", pa.float64()),
    ("pmms15", pa.float64()),
    ("pmms15p", pa.float64()),
    ("pmms51", pa.float64()),
    ("pmms51p", pa.float64()),
    ("pmms51m", pa.float64()),
    ("pmms51spread", pa.float64()),
])

_PMMS_HEADER = [
    "date", "pmms30", "pmms30p", "pmms15", "pmms15p",
    "pmms51", "pmms51p", "pmms51m", "pmms51spread",
]


def _parse_pmms_date(value):
    s = (value or "").strip()
    if s == "":
        return None
    try:
        return datetime.strptime(s, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None


def fetch_mortgage_rates(node_id: str) -> None:
    asset = node_id
    reader = csv.reader(io.StringIO(fetch_csv(PMMS_URL)))
    rows = list(reader)
    header = [h.strip() for h in rows[0]]
    if header != _PMMS_HEADER:
        raise AssertionError(f"PMMS header changed: {header}")

    cols = {name: [] for name in PMMS_SCHEMA.names}
    width = len(_PMMS_HEADER)
    for raw in rows[1:]:
        if not raw or all(c.strip() == "" for c in raw):
            continue
        # Ragged: short rows carry only the leading columns; pad with blanks.
        row = (raw + [""] * width)[:width]
        cols["date"].append(_parse_pmms_date(row[0]))
        for i, name in enumerate(_PMMS_HEADER[1:], start=1):
            cols[name].append(to_float(row[i]))
    table = pa.table(cols, schema=PMMS_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="freddie-mac-mortgage-rates", fn=fetch_mortgage_rates, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freddie-mac-mortgage-rates-transform",
        deps=["freddie-mac-mortgage-rates"],
        sql='''
            SELECT
                CAST(date AS DATE)  AS date,
                pmms30              AS rate_30yr_fixed,
                pmms30p             AS points_30yr_fixed,
                pmms15              AS rate_15yr_fixed,
                pmms15p             AS points_15yr_fixed,
                pmms51              AS rate_5yr_arm,
                pmms51p             AS points_5yr_arm,
                pmms51m             AS margin_5yr_arm,
                pmms51spread        AS spread_5yr_arm
            FROM "freddie-mac-mortgage-rates"
            WHERE date IS NOT NULL
              AND pmms30 IS NOT NULL
        ''',
    ),
]
