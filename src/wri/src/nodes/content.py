"""WRI NDC / net-zero content (Climate Watch).

  - wri-ndc-content:      structured NDC (Paris pledge) document content.
  - wri-net-zero-content: structured net-zero target content. Same schema as
    ndc_content but a distinct dataset/table.

Both subsets share one parametric fetcher (identical schema); the endpoint is
recovered from the node id.
"""

import csv

import pyarrow as pa

from subsets_utils import save_raw_parquet
from utils import download_zip, open_member

_CONTENT_SCHEMA = pa.schema([
    ("iso_code3", pa.string()),
    ("country", pa.string()),
    ("global_category", pa.string()),
    ("overview_category", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("indicator_id", pa.string()),
    ("value", pa.string()),
    ("source", pa.string()),
    ("indicator_name", pa.string()),
])
# CSV header order -> our column order (the export puts Value before Source).
_CONTENT_HEADER = [
    "iso", "country", "global category", "overview category", "sector",
    "subsector", "indicator id", "value", "source", "indicator name",
]


def fetch_content(node_id: str) -> None:
    """Shared fetcher for ndc_content and net_zero_content (identical schema).
    Recovers the endpoint from the node id."""
    asset = node_id
    endpoint = node_id[len("wri-"):].replace("-", "_")  # ndc-content -> ndc_content
    content = download_zip(endpoint)
    reader = csv.reader(open_member(content, f"{endpoint}.csv"))
    header = [c.strip().lower() for c in next(reader)]
    assert header == _CONTENT_HEADER, f"unexpected {endpoint} header: {header}"

    rows = []
    for row in reader:
        # pad short rows defensively (trailing empty fields can be dropped)
        row = (row + [None] * len(_CONTENT_HEADER))[: len(_CONTENT_HEADER)]
        rows.append({
            "iso_code3": row[0],
            "country": row[1],
            "global_category": row[2],
            "overview_category": row[3],
            "sector": row[4] or None,
            "subsector": row[5] or None,
            "indicator_id": row[6],
            "value": row[7],
            "source": row[8],
            "indicator_name": row[9],
        })

    assert rows, f"{endpoint} produced 0 rows"
    table = pa.Table.from_pylist(rows, schema=_CONTENT_SCHEMA)
    save_raw_parquet(table, asset)
