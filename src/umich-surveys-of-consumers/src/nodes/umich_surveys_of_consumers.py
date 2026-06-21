"""University of Michigan Surveys of Consumers — download + transform.

Source: https://data.sca.isr.umich.edu/data-archive/mine.php (data_archive
mechanism). 47 distinct survey tables, each its own publishable subset. One
HTTP POST per table returns the full monthly history as CSV: a title line,
then a header row, then data rows (numeric Month, Year, then table-specific
value columns; a trailing empty column from a dangling comma on each line).

Schemas are heterogeneous across tables (each table has its own value
columns), so the download normalizes every table's wide CSV into a uniform
long shape — (year, month, series, value) — one row per (month, value column).
That keeps a single parquet schema for all 47 raw assets, and each table's
transform publishes a tidy long time series (date, series, value).

Stateless full re-pull: each POST already returns the full history back to
1978, the corpus is a few MB total, so we re-fetch every run and overwrite.
The source revises recent months, which a full re-pull picks up for free.
"""

import csv
import re
from io import StringIO

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    post,
    save_raw_parquet,
    transient_retry,
)

SLUG = "umich-surveys-of-consumers"
ARCHIVE_URL = "https://data.sca.isr.umich.edu/data-archive/mine.php"

# The 47 survey tables — the entity union (table-1 .. table-47).
ENTITY_IDS = [f"table-{n}" for n in range(1, 48)]

# Long-format raw: one row per (month, value column). Uniform across all tables.
SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("month", pa.int32()),
    ("series", pa.string()),
    ("value", pa.float64()),
])


def _clean(col: str) -> str:
    """Strip embedded <br> markup and collapse whitespace in a column name."""
    col = re.sub(r"<br\s*/?>", " ", col, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", col).strip()


def _parse_value(raw: str):
    raw = (raw or "").strip()
    if raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


@transient_retry()
def _fetch_table_csv(table_num: int) -> str:
    resp = post(
        ARCHIVE_URL,
        data={
            "table": str(table_num),
            "year": "1978",
            "qorm": "M",
            "order": "asc",
            "format": "Comma-Separated (CSV)",
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.text


def _table_num(node_id: str) -> int:
    # node_id is "umich-surveys-of-consumers-table-N"
    suffix = node_id[len(SLUG) + 1:]          # "table-N"
    return int(suffix.split("-", 1)[1])


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    table_num = _table_num(node_id)
    text = _fetch_table_csv(table_num)

    rows = list(csv.reader(StringIO(text)))
    # rows[0] = title line, rows[1] = header, rows[2:] = data.
    header = rows[1]
    # Columns after Month/Year are the value series; last col is empty (dangling comma).
    series_cols = [_clean(c) for c in header[2:]]
    # Drop trailing empty-name columns produced by the trailing comma.
    while series_cols and series_cols[-1] == "":
        series_cols.pop()

    out = []
    for row in rows[2:]:
        if len(row) < 2 or not row[0].strip() or not row[1].strip():
            continue
        try:
            month = int(row[0].strip())
            year = int(row[1].strip())
        except ValueError:
            continue
        if not (1 <= month <= 12):
            continue
        for i, series in enumerate(series_cols):
            cell = row[2 + i] if 2 + i < len(row) else ""
            out.append({
                "year": year,
                "month": month,
                "series": series,
                "value": _parse_value(cell),
            })

    if not out:
        raise ValueError(f"{asset}: parsed 0 rows from table {table_num}")

    table = pa.Table.from_pylist(out, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# Each table publishes a tidy long time series. Uniform SQL: build the month
# date and keep observed values (a series may be null in early months).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                make_date(year, month, 1) AS date,
                series,
                CAST(value AS DOUBLE)      AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
            ORDER BY date, series
        ''',
    )
    for s in DOWNLOAD_SPECS
]
