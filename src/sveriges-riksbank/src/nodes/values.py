"""Sveriges Riksbank — SWEA observations (long format).

`values` — long-format observations across all series (one row per
(series_id, date)). Built by enumerating /Series, then pulling each series'
FULL history in one request via /Observations/{seriesId}/{min}/{max}. (The bulk
/Observations/ByGroup endpoint is capped at 1-year windows, so it is useless for
full history; the per-series endpoint has no span cap.)

Strategy is stateless full re-pull each run: there is no incremental query
parameter on the API, and re-pulling picks up revisions/backfills for free.
"""

import pyarrow as pa

from subsets_utils import raw_parquet_writer
from utils import BASE, fetch_series_catalog, get_json

VALUES_SCHEMA = pa.schema([
    ("series_id", pa.string()),
    ("group_id", pa.int64()),
    ("date", pa.string()),
    ("value", pa.float64()),
])


def fetch_values(node_id: str) -> None:
    asset = node_id
    series = fetch_series_catalog()

    total = 0
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for s in series:
            sid = s.get("seriesId")
            gid = s.get("groupId")
            mn = s.get("observationMinDate")
            mx = s.get("observationMaxDate")
            if not sid or not mn or not mx:
                continue
            obs = get_json(f"{BASE}/Observations/{sid}/{mn}/{mx}")
            if not obs:
                continue
            n = len(obs)
            batch = pa.table(
                {
                    "series_id": pa.array([sid] * n, pa.string()),
                    "group_id": pa.array([gid] * n, pa.int64()),
                    "date": pa.array([o.get("date") for o in obs], pa.string()),
                    "value": pa.array([o.get("value") for o in obs], pa.float64()),
                },
                schema=VALUES_SCHEMA,
            )
            writer.write_table(batch)
            total += n

    if total == 0:
        raise AssertionError("fetched 0 observations across all series — API shape likely changed")
