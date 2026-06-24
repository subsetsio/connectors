"""Reddit connector — Arctic Shift precomputed time_series + subreddit metadata.

Four subsets, each a download NodeSpec + a SqlNodeSpec that publishes one Delta
table:

- reddit-global-activity      Reddit-wide monthly posts/comments counts & score sums
- reddit-subreddit-activity   per-subreddit monthly posts/comments counts & score sums
- reddit-subreddit-subscribers per-subreddit monthly subscriber-count series
- reddit-subreddits           current per-subreddit metadata reference snapshot

All HTTP/enumeration/retry policy lives in src/utils.py (shared transport). We
use only the two endpoints of the chosen `arctic_shift_rest` mechanism:
/api/time_series (precomputed series) and /api/subreddits/search (metadata +
enumeration). Stateless full re-pull every run — the series are small
(precision=month) and overwritten downstream.
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

# --------------------------------------------------------------------------
# reddit-global-activity
# --------------------------------------------------------------------------

# Global activity metric -> Arctic Shift time_series key.
GLOBAL_METRICS = {
    "posts_count": "global/posts/count",
    "comments_count": "global/comments/count",
    "posts_sum_score": "global/posts/sum_score",
    "comments_sum_score": "global/comments/sum_score",
}

_GLOBAL_SCHEMA = pa.schema([
    ("metric", pa.string()),
    ("date", pa.int64()),        # epoch seconds (period start)
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


# --------------------------------------------------------------------------
# reddit-subreddit-activity
# --------------------------------------------------------------------------

# Per-subreddit activity metric -> key suffix (prefixed with r/<name>/).
ACTIVITY_METRICS = {
    "posts_count": "posts/count",
    "comments_count": "comments/count",
    "posts_sum_score": "posts/sum_score",
    "comments_sum_score": "comments/sum_score",
}

_ACTIVITY_SCHEMA = pa.schema([
    ("subreddit", pa.string()),
    ("metric", pa.string()),
    ("date", pa.int64()),        # epoch seconds (period start)
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
            pa.Table.from_pylist(rows, schema=_ACTIVITY_SCHEMA),
            f"{node_id}-{batch:04d}",
        )
        print(f"    batch {batch:04d}: {len(rows)} rows")
    _check_skips(skipped, len(names), node_id)


# --------------------------------------------------------------------------
# reddit-subreddit-subscribers
# --------------------------------------------------------------------------

_SUBSCRIBERS_SCHEMA = pa.schema([
    ("subreddit", pa.string()),
    ("date", pa.int64()),        # epoch seconds (period start)
    ("value", pa.float64()),     # subscriber count
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


# --------------------------------------------------------------------------
# reddit-subreddits (metadata snapshot)
# --------------------------------------------------------------------------

_SUBREDDITS_SCHEMA = pa.schema([
    ("subreddit", pa.string()),
    ("subscribers", pa.int64()),
    ("created_utc", pa.int64()),
    ("over18", pa.bool_()),
    ("subreddit_type", pa.string()),
    ("lang", pa.string()),
    ("num_posts", pa.int64()),
    ("num_comments", pa.int64()),
])


def fetch_subreddits(node_id: str) -> None:
    rows = []
    for rec in _walk_subreddits():
        meta = rec.get("_meta") or {}
        rows.append({
            "subreddit": rec.get("display_name"),
            "subscribers": rec.get("subscribers"),
            "created_utc": rec.get("created_utc"),
            "over18": rec.get("over18"),
            "subreddit_type": rec.get("subreddit_type"),
            "lang": rec.get("lang"),
            "num_posts": meta.get("num_posts"),
            "num_comments": meta.get("num_comments"),
        })
    if not rows:
        raise RuntimeError("subreddits: enumeration returned no records")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_SUBREDDITS_SCHEMA), node_id)


# --------------------------------------------------------------------------
# Specs
# --------------------------------------------------------------------------

DOWNLOAD_SPECS = [
    NodeSpec(id="reddit-global-activity", fn=fetch_global_activity, kind="download"),
    NodeSpec(id="reddit-subreddit-activity", fn=fetch_subreddit_activity, kind="download"),
    NodeSpec(id="reddit-subreddit-subscribers", fn=fetch_subreddit_subscribers, kind="download"),
    NodeSpec(id="reddit-subreddits", fn=fetch_subreddits, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="reddit-global-activity-transform",
        deps=["reddit-global-activity"],
        sql='''
            SELECT
                CAST(to_timestamp(date) AS DATE)                          AS date,
                CAST(MAX(value) FILTER (WHERE metric='posts_count')    AS BIGINT) AS posts_count,
                CAST(MAX(value) FILTER (WHERE metric='comments_count') AS BIGINT) AS comments_count,
                MAX(value) FILTER (WHERE metric='posts_sum_score')       AS posts_sum_score,
                MAX(value) FILTER (WHERE metric='comments_sum_score')    AS comments_sum_score
            FROM "reddit-global-activity"
            GROUP BY 1
            ORDER BY 1
        ''',
    ),
    SqlNodeSpec(
        id="reddit-subreddit-activity-transform",
        deps=["reddit-subreddit-activity"],
        sql='''
            SELECT
                subreddit,
                CAST(to_timestamp(date) AS DATE)                          AS date,
                CAST(MAX(value) FILTER (WHERE metric='posts_count')    AS BIGINT) AS posts_count,
                CAST(MAX(value) FILTER (WHERE metric='comments_count') AS BIGINT) AS comments_count,
                MAX(value) FILTER (WHERE metric='posts_sum_score')       AS posts_sum_score,
                MAX(value) FILTER (WHERE metric='comments_sum_score')    AS comments_sum_score
            FROM "reddit-subreddit-activity"
            GROUP BY 1, 2
        ''',
    ),
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
    SqlNodeSpec(
        id="reddit-subreddits-transform",
        deps=["reddit-subreddits"],
        sql='''
            SELECT
                subreddit,
                subscribers,
                CAST(to_timestamp(created_utc) AS DATE) AS created_date,
                over18,
                subreddit_type,
                lang,
                num_posts,
                num_comments
            FROM "reddit-subreddits"
            WHERE subreddit IS NOT NULL
        ''',
    ),
]
