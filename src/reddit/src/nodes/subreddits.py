"""reddit-subreddits — per-subreddit metadata reference snapshot.

Current metadata for every subreddit with >= MIN_SUBSCRIBERS, taken from the
subreddits/search enumeration walk.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _walk_subreddits

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


DOWNLOAD_SPECS = [
    NodeSpec(id="reddit-subreddits", fn=fetch_subreddits, kind="download"),
]

TRANSFORM_SPECS = [
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
