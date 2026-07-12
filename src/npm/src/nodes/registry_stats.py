"""npm-registry-stats — daily snapshot of registry-wide counters (accumulated).

npm exposes only the current counters, so its raw accumulates one row per
observation date across runs (dedup on date).
"""
from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec, SqlNodeSpec,
    save_raw_parquet, load_raw_parquet, raw_asset_exists,
)

from utils import _get_json

REPLICATE_ROOT = "https://replicate.npmjs.com/"

_STATS_SCHEMA = pa.schema([
    ("observation_date", pa.string()),
    ("doc_count", pa.int64()),
    ("update_seq", pa.int64()),
])


def fetch_registry_stats(node_id: str) -> None:
    meta = _get_json(REPLICATE_ROOT)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = {
        "observation_date": today,
        "doc_count": int(meta["doc_count"]),
        "update_seq": int(meta["update_seq"]),
    }
    # npm exposes only the current counters, so build the time series by
    # accumulating prior observations stored in raw (dedup on date).
    rows = {today: row}
    if raw_asset_exists(node_id, "parquet"):
        for prior in load_raw_parquet(node_id).to_pylist():
            rows.setdefault(prior["observation_date"], prior)
    ordered = [rows[d] for d in sorted(rows)]
    table = pa.Table.from_pylist(ordered, schema=_STATS_SCHEMA)
    save_raw_parquet(table, node_id)
    print(f"  {node_id}: {table.num_rows:,} daily snapshots (latest {today})")


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="npm-registry-stats-transform",
        deps=["npm-registry-stats"],
        sql='''
            SELECT
                CAST(observation_date AS DATE) AS observation_date,
                CAST(doc_count AS BIGINT)      AS doc_count,
                CAST(update_seq AS BIGINT)     AS update_seq
            FROM "npm-registry-stats"
            WHERE observation_date IS NOT NULL
        ''',
    ),
]
