"""NOAA NESIS — single Northeast Snowfall Impact Scale CSV (latin-1, stray
bytes). NESIS historical Northeast snowstorm events.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import save_raw_parquet

from utils import NCEI, _get_text, _list_hrefs, _normalize_header, _string_table

NESIS_DIR = f"{NCEI}/data/northeast-snowfall-impact-scale/access/"


def fetch_nesis(node_id: str) -> None:
    files = sorted(h for h in _list_hrefs(NESIS_DIR) if h.endswith(".csv"))
    if not files:
        raise RuntimeError(f"nesis: no CSV found at {NESIS_DIR}")
    text = _get_text(NESIS_DIR + files[-1], encoding="latin-1")
    reader = csv.reader(io.StringIO(text))
    header = _normalize_header(next(reader))
    schema = pa.schema([(c, pa.string()) for c in header])
    table, dropped = _string_table(header, reader, schema)
    if table.num_rows < 10:
        raise RuntimeError(f"nesis: only {table.num_rows} rows in {files[-1]}")
    if dropped:
        raise RuntimeError(f"nesis: {dropped} malformed rows in {files[-1]}")
    save_raw_parquet(table, node_id)

