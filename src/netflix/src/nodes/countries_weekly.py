"""Netflix Top 10 — per-country weekly Top 10.

all-weeks-countries.tsv: per-country weekly Top 10 (~482k rows, 94 countries).

season_title is "N/A" for films; the transform maps that to NULL.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import fetch_tsv, s, to_int

_COUNTRIES_SCHEMA = pa.schema([
    ("country_name", pa.string()),
    ("country_iso2", pa.string()),
    ("week", pa.string()),
    ("category", pa.string()),
    ("weekly_rank", pa.int32()),
    ("show_title", pa.string()),
    ("season_title", pa.string()),
    ("cumulative_weeks_in_top_10", pa.int32()),
])


def fetch_countries_weekly(node_id: str) -> None:
    asset = node_id
    rows = fetch_tsv("all-weeks-countries.tsv")
    table = pa.table(
        {
            "country_name": [s(r["country_name"]) for r in rows],
            "country_iso2": [s(r["country_iso2"]) for r in rows],
            "week": [s(r["week"]) for r in rows],
            "category": [s(r["category"]) for r in rows],
            "weekly_rank": [to_int(r["weekly_rank"]) for r in rows],
            "show_title": [s(r["show_title"]) for r in rows],
            "season_title": [s(r["season_title"]) for r in rows],
            "cumulative_weeks_in_top_10": [
                to_int(r["cumulative_weeks_in_top_10"]) for r in rows
            ],
        },
        schema=_COUNTRIES_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="netflix-countries-weekly", fn=fetch_countries_weekly, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="netflix-countries-weekly-transform",
        deps=["netflix-countries-weekly"],
        sql='''
            SELECT
                country_name,
                country_iso2,
                CAST(week AS DATE)                  AS week,
                category,
                weekly_rank,
                show_title,
                NULLIF(season_title, 'N/A')         AS season_title,
                cumulative_weeks_in_top_10
            FROM "netflix-countries-weekly"
            WHERE week IS NOT NULL AND weekly_rank IS NOT NULL
        ''',
    ),
]
