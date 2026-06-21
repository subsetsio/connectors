"""Netflix Top 10 — all-time most popular (first 91 days).

most-popular.tsv: all-time most popular (91d) (~40 rows).

season_title is "N/A" for films; the transform maps that to NULL.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_tsv, s, to_float, to_int

_POPULAR_SCHEMA = pa.schema([
    ("category", pa.string()),
    ("rank", pa.int32()),
    ("show_title", pa.string()),
    ("season_title", pa.string()),
    ("hours_viewed_first_91_days", pa.int64()),
    ("runtime", pa.float64()),
    ("views_first_91_days", pa.int64()),
])


def fetch_most_popular(node_id: str) -> None:
    asset = node_id
    rows = fetch_tsv("most-popular.tsv")
    table = pa.table(
        {
            "category": [s(r["category"]) for r in rows],
            "rank": [to_int(r["rank"]) for r in rows],
            "show_title": [s(r["show_title"]) for r in rows],
            "season_title": [s(r["season_title"]) for r in rows],
            "hours_viewed_first_91_days": [
                to_int(r["hours_viewed_first_91_days"]) for r in rows
            ],
            "runtime": [to_float(r["runtime"]) for r in rows],
            "views_first_91_days": [to_int(r["views_first_91_days"]) for r in rows],
        },
        schema=_POPULAR_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="netflix-most-popular", fn=fetch_most_popular, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="netflix-most-popular-transform",
        deps=["netflix-most-popular"],
        sql='''
            SELECT
                category,
                rank,
                show_title,
                NULLIF(season_title, 'N/A')         AS season_title,
                hours_viewed_first_91_days,
                runtime                             AS runtime_hours,
                views_first_91_days
            FROM "netflix-most-popular"
            WHERE rank IS NOT NULL
        ''',
    ),
]
