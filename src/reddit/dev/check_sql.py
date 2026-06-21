"""Validate transform SQL against small live samples (no raw writes)."""
import duckdb
import pyarrow as pa  # noqa
from subsets_utils import get

API = "https://arctic-shift.photon-reddit.com/api"


def ts(key):
    d = get(f"{API}/time_series", params={"key": key, "precision": "month"}, timeout=(10, 60)).json()
    return d.get("data") or []


# global-activity sample
g_rows = []
for metric, key in [("posts_count", "global/posts/count"), ("comments_count", "global/comments/count"),
                    ("posts_sum_score", "global/posts/sum_score"), ("comments_sum_score", "global/comments/sum_score")]:
    for pt in ts(key):
        g_rows.append({"metric": metric, "date": pt["date"], "value": pt["value"]})
glob = pa.Table.from_pylist(g_rows)
con = duckdb.connect()
con.register("g", glob)
r = con.execute('''
    SELECT CAST(to_timestamp(date) AS DATE) AS date,
        CAST(MAX(value) FILTER (WHERE metric='posts_count') AS BIGINT) AS posts_count,
        CAST(MAX(value) FILTER (WHERE metric='comments_count') AS BIGINT) AS comments_count,
        MAX(value) FILTER (WHERE metric='posts_sum_score') AS posts_sum_score,
        MAX(value) FILTER (WHERE metric='comments_sum_score') AS comments_sum_score
    FROM g GROUP BY 1 ORDER BY 1''').fetch_arrow_table()
print("GLOBAL rows", r.num_rows, "cols", r.column_names)
print(r.slice(r.num_rows - 2).to_pylist())

# subscribers sample
s_rows = []
for name in ["AskReddit", "funny", "science"]:
    for pt in ts(f"r/{name}/subscribers"):
        s_rows.append({"subreddit": name, "date": pt["date"], "value": pt["value"]})
con.register("s", pa.Table.from_pylist(s_rows))
r = con.execute('''
    SELECT subreddit, CAST(to_timestamp(date) AS DATE) AS date, CAST(round(value) AS BIGINT) AS subscribers
    FROM s WHERE value IS NOT NULL
    QUALIFY row_number() OVER (PARTITION BY subreddit, CAST(to_timestamp(date) AS DATE) ORDER BY value DESC) = 1''').fetch_arrow_table()
print("SUBS rows", r.num_rows, "uniq check", con.execute("SELECT count(*), count(distinct (subreddit,date)) FROM r").fetch_arrow_table().to_pylist() if False else "")
print(r.slice(0, 2).to_pylist())

# activity sample
a_rows = []
for name in ["AskReddit", "science"]:
    for metric, suf in [("posts_count", "posts/count"), ("comments_count", "comments/count"),
                        ("posts_sum_score", "posts/sum_score"), ("comments_sum_score", "comments/sum_score")]:
        for pt in ts(f"r/{name}/{suf}"):
            a_rows.append({"subreddit": name, "metric": metric, "date": pt["date"], "value": pt["value"]})
con.register("a", pa.Table.from_pylist(a_rows))
r = con.execute('''
    SELECT subreddit, CAST(to_timestamp(date) AS DATE) AS date,
        CAST(MAX(value) FILTER (WHERE metric='posts_count') AS BIGINT) AS posts_count,
        CAST(MAX(value) FILTER (WHERE metric='comments_count') AS BIGINT) AS comments_count,
        MAX(value) FILTER (WHERE metric='posts_sum_score') AS posts_sum_score,
        MAX(value) FILTER (WHERE metric='comments_sum_score') AS comments_sum_score
    FROM a GROUP BY 1,2''').fetch_arrow_table()
print("ACTIVITY rows", r.num_rows, "cols", r.column_names)
print(r.slice(0, 2).to_pylist())
print("OK")
