"""reddit-subreddit-subscribers — per-subreddit subscriber-count time series.

One precomputed `r/<name>/subscribers` series per enumerated subreddit, written
in raw parquet batches. Isolated per-subreddit failures are skipped (see
utils._check_skips) rather than aborting the whole node.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import (
    BATCH_SUBREDDITS,
    _SKIPPABLE_EXC,
    _check_skips,
    _time_series,
    _walk_subreddits,
)

_SUBSCRIBERS_SCHEMA = pa.schema([
    ("subreddit", pa.string()),
    ("date", pa.int64()),
    ("value", pa.float64()),
])


def fetch_subreddit_subscribers(node_id: str) -> None:
    names = [r["display_name"] for r in _walk_subreddits()]
    print(f"  subscribers: {len(names)} subreddits")
    skipped = 0
    for start in range(0, len(names), BATCH_SUBREDDITS):
        chunk = names[start:start + BATCH_SUBREDDITS]
        rows = []
        for name in chunk:
            try:
                series = _time_series(f"r/{name}/subscribers")
            except _SKIPPABLE_EXC as exc:
                skipped += 1
                print(f"    skip r/{name} subscribers: {type(exc).__name__}: {exc}")
                continue
            for pt in series:
                rows.append({"subreddit": name, "date": pt["date"], "value": pt["value"]})
        if not rows:
            continue
        batch = start // BATCH_SUBREDDITS
        save_raw_parquet(
            pa.Table.from_pylist(rows, schema=_SUBSCRIBERS_SCHEMA),
            f"{node_id}-{batch:04d}",
        )
        print(f"    batch {batch:04d}: {len(rows)} rows")
    _check_skips(skipped, len(names), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="reddit-subreddit-subscribers", fn=fetch_subreddit_subscribers, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="reddit-subreddit-subscribers-transform",
        deps=["reddit-subreddit-subscribers"],
        sql='''
            SELECT
                subreddit,
                CAST(to_timestamp(date) AS DATE)   AS date,
                CAST(round(value) AS BIGINT)       AS subscribers
            FROM "reddit-subreddit-subscribers"
            WHERE value IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY subreddit, CAST(to_timestamp(date) AS DATE) ORDER BY value DESC) = 1
        ''',
    ),
]
