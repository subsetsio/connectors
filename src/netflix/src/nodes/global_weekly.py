"""Netflix Top 10 — global weekly Top 10.

all-weeks-global.tsv: global weekly Top 10 (~10k rows, 259 weeks).

The global file leaves runtime/weekly_views empty for pre-2023 weeks (views were
added later); those parse to NULL. season_title is "N/A" for films; the transform
maps that to NULL.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_tsv, s, to_float, to_int

_GLOBAL_SCHEMA = pa.schema([
    ("week", pa.string()),
    ("category", pa.string()),
    ("weekly_rank", pa.int32()),
    ("show_title", pa.string()),
    ("season_title", pa.string()),
    ("weekly_hours_viewed", pa.int64()),
    ("runtime", pa.float64()),
    ("weekly_views", pa.int64()),
    ("cumulative_weeks_in_top_10", pa.int32()),
])


def fetch_global_weekly(node_id: str) -> None:
    asset = node_id
    rows = fetch_tsv("all-weeks-global.tsv")
    table = pa.table(
        {
            "week": [s(r["week"]) for r in rows],
            "category": [s(r["category"]) for r in rows],
            "weekly_rank": [to_int(r["weekly_rank"]) for r in rows],
            "show_title": [s(r["show_title"]) for r in rows],
            "season_title": [s(r["season_title"]) for r in rows],
            "weekly_hours_viewed": [to_int(r["weekly_hours_viewed"]) for r in rows],
            "runtime": [to_float(r["runtime"]) for r in rows],
            "weekly_views": [to_int(r["weekly_views"]) for r in rows],
            "cumulative_weeks_in_top_10": [
                to_int(r["cumulative_weeks_in_top_10"]) for r in rows
            ],
        },
        schema=_GLOBAL_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="netflix-global-weekly", fn=fetch_global_weekly, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="netflix-global-weekly-transform",
        deps=["netflix-global-weekly"],
        sql='''
            SELECT
                CAST(week AS DATE)                  AS week,
                category,
                weekly_rank,
                show_title,
                NULLIF(season_title, 'N/A')         AS season_title,
                weekly_hours_viewed,
                runtime                             AS runtime_hours,
                weekly_views,
                cumulative_weeks_in_top_10
            FROM "netflix-global-weekly"
            WHERE week IS NOT NULL AND weekly_rank IS NOT NULL
        ''',
    ),
]
