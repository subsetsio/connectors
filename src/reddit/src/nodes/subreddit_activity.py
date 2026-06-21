"""reddit-subreddit-activity — per-subreddit posts/comments counts & score sums.

Four precomputed `r/<name>/<metric>` series per enumerated subreddit, written in
raw parquet batches. A subreddit's rows are committed only on full success of
all four metrics; isolated failures are skipped (see utils._check_skips).
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

# Per-subreddit activity metric -> key suffix (prefixed with r/<name>/).
ACTIVITY_METRICS = {
    "posts_count": "posts/count",
    "comments_count": "comments/count",
    "posts_sum_score": "posts/sum_score",
    "comments_sum_score": "comments/sum_score",
}

_TIMESERIES_SCHEMA = pa.schema([
    ("subreddit", pa.string()),
    ("metric", pa.string()),
    ("date", pa.int64()),       # epoch seconds (period start)
    ("value", pa.float64()),
])


def fetch_subreddit_activity(node_id: str) -> None:
    names = [r["display_name"] for r in _walk_subreddits()]
    print(f"  activity: {len(names)} subreddits")
    skipped = 0
    for start in range(0, len(names), BATCH_SUBREDDITS):
        chunk = names[start:start + BATCH_SUBREDDITS]
        rows = []
        for name in chunk:
            try:
                sub_rows = []
                for metric, suffix in ACTIVITY_METRICS.items():
                    for pt in _time_series(f"r/{name}/{suffix}"):
                        sub_rows.append({
                            "subreddit": name, "metric": metric,
                            "date": pt["date"], "value": pt["value"],
                        })
            except _SKIPPABLE_EXC as exc:
                skipped += 1
                print(f"    skip r/{name} activity: {type(exc).__name__}: {exc}")
                continue
            rows.extend(sub_rows)  # only on full success of all metrics
        if not rows:
            continue
        batch = start // BATCH_SUBREDDITS
        save_raw_parquet(
            pa.Table.from_pylist(rows, schema=_TIMESERIES_SCHEMA),
            f"{node_id}-{batch:04d}",
        )
        print(f"    batch {batch:04d}: {len(rows)} rows")
    _check_skips(skipped, len(names), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="reddit-subreddit-activity", fn=fetch_subreddit_activity, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="reddit-subreddit-activity-transform",
        deps=["reddit-subreddit-activity"],
        sql='''
            SELECT
                subreddit,
                CAST(to_timestamp(date) AS DATE)                         AS date,
                CAST(MAX(value) FILTER (WHERE metric='posts_count')    AS BIGINT) AS posts_count,
                CAST(MAX(value) FILTER (WHERE metric='comments_count') AS BIGINT) AS comments_count,
                MAX(value) FILTER (WHERE metric='posts_sum_score')      AS posts_sum_score,
                MAX(value) FILTER (WHERE metric='comments_sum_score')   AS comments_sum_score
            FROM "reddit-subreddit-activity"
            GROUP BY 1, 2
        ''',
    ),
]
