"""Majestic Million connector.

Single-dataset source: one persistent bulk CSV at
https://downloads.majestic.com/majestic_million.csv holding exactly the top
1,000,000 domains by distinct referring subnets, regenerated daily and
overwritten in place. There is no per-entity API and no incremental filter, so
the shape is a stateless full re-pull: fetch the whole ~80MB CSV every run,
parse to parquet, and let the transform publish one Delta table.

Licensed CC-BY 3.0 (attribution to Majestic).
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, get, save_raw_parquet

CSV_URL = "https://downloads.majestic.com/majestic_million.csv"

# Explicit schema is the contract — the CSV header is stable but declaring types
# means a format change (renamed/added column, a count turning non-integer)
# fails loudly at parse time instead of silently mis-typing.
SCHEMA = pa.schema([
    ("GlobalRank", pa.int64()),
    ("TldRank", pa.int64()),
    ("Domain", pa.string()),
    ("TLD", pa.string()),
    ("RefSubNets", pa.int64()),
    ("RefIPs", pa.int64()),
    ("IDN_Domain", pa.string()),
    ("IDN_TLD", pa.string()),
    ("PrevGlobalRank", pa.int64()),
    ("PrevTldRank", pa.int64()),
    ("PrevRefSubNets", pa.int64()),
    ("PrevRefIPs", pa.int64()),
])


def _fetch_csv() -> bytes:
    resp = get(CSV_URL, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def fetch_majestic_million(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    raw = _fetch_csv()
    table = pacsv.read_csv(
        io.BytesIO(raw),
        read_options=pacsv.ReadOptions(column_names=SCHEMA.names, skip_rows=1),
        convert_options=pacsv.ConvertOptions(
            column_types={f.name: f.type for f in SCHEMA}
        ),
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="majestic-million-majestic-million",
        fn=fetch_majestic_million,
        kind="download",
    ),
]
