"""reddit-global-activity — Reddit-wide posts/comments counts & score sums.

Sourced from Arctic Shift's precomputed `global/...` time_series keys.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _time_series

# Global activity metric -> Arctic Shift time_series key.
GLOBAL_METRICS = {
    "posts_count": "global/posts/count",
    "comments_count": "global/comments/count",
    "posts_sum_score": "global/posts/sum_score",
    "comments_sum_score": "global/comments/sum_score",
}

_GLOBAL_SCHEMA = pa.schema([
    ("metric", pa.string()),
    ("date", pa.int64()),
    ("value", pa.float64()),
])


def fetch_global_activity(node_id: str) -> None:
    rows = []
    for metric, key in GLOBAL_METRICS.items():
        for pt in _time_series(key):
            rows.append({"metric": metric, "date": pt["date"], "value": pt["value"]})
    if not rows:
        raise RuntimeError("global activity: all time_series keys returned empty")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_GLOBAL_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="reddit-global-activity", fn=fetch_global_activity, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="reddit-global-activity-transform",
        deps=["reddit-global-activity"],
        sql='''
            SELECT
                CAST(to_timestamp(date) AS DATE)                         AS date,
                CAST(MAX(value) FILTER (WHERE metric='posts_count')    AS BIGINT) AS posts_count,
                CAST(MAX(value) FILTER (WHERE metric='comments_count') AS BIGINT) AS comments_count,
                MAX(value) FILTER (WHERE metric='posts_sum_score')      AS posts_sum_score,
                MAX(value) FILTER (WHERE metric='comments_sum_score')   AS comments_sum_score
            FROM "reddit-global-activity"
            GROUP BY 1
            ORDER BY 1
        ''',
    ),
]
