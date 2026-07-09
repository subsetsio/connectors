"""NOAA Regional Snowfall Index (RSI) event table — pick the newest dated CSV
in access/.
"""

import csv
import io
import re

import pyarrow as pa

from subsets_utils import save_raw_parquet

from utils import (
    NCEI,
    _get_text,
    _iso_date_columns,
    _list_hrefs,
    _normalize_header,
    _string_table,
)

RSI_DIR = f"{NCEI}/data/regional-snowfall-index/access/"
_RSI_RE = re.compile(r"regional-snowfall-index_c\d+\.csv$")


def fetch_rsi(node_id: str) -> None:
    files = sorted(h for h in _list_hrefs(RSI_DIR) if _RSI_RE.match(h))
    if not files:
        raise RuntimeError(f"rsi: no dated CSV found at {RSI_DIR}")
    text = _get_text(RSI_DIR + files[-1])
    reader = csv.reader(io.StringIO(text))
    header = _normalize_header(next(reader))
    schema = pa.schema([(c, pa.string()) for c in header])
    table, dropped = _string_table(header, reader, schema)
    if table.num_rows < 50:
        raise RuntimeError(f"rsi: only {table.num_rows} rows in {files[-1]}")
    # A few upstream rows omit `End` entirely (22 of 23 fields); they are dropped
    # rather than misaligned. More than a handful means the layout moved.
    if dropped > 10:
        raise RuntimeError(f"rsi: {dropped} malformed rows in {files[-1]}")
    table = _iso_date_columns(table, ["Start", "End"])
    save_raw_parquet(table, node_id)

