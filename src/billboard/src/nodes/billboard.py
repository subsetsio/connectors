"""Billboard Hot 100 weekly chart connector.

Single dataset: the complete Billboard Hot 100 weekly singles ranking
(1958-08-04 to present), sourced from the auto-updated community GitHub mirror
`mhollingshead/billboard-hot-100`. The mirror publishes `all.json` — one
persistent ~44MB JSON array of weekly chart objects
`{date, data:[{song, artist, this_week, last_week, peak_position, weeks_on_chart}]}`.

Strategy: stateless full re-pull. The corpus is small (~44MB / ~354k rows) and
the source carries no incremental filter, so every run fetches the whole file
and overwrites. Revisions and late corrections are picked up for free.
"""
import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

ALL_URL = "https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/all.json"

# last_week is null on new entries; chart_date stored as string (ISO date),
# cast to DATE in the transform. All chart positions are 1-100.
SCHEMA = pa.schema([
    ("chart_date", pa.string()),
    ("rank", pa.int64()),
    ("song", pa.string()),
    ("artist", pa.string()),
    ("last_week", pa.int64()),
    ("peak_position", pa.int64()),
    ("weeks_on_chart", pa.int64()),
])


@transient_retry()
def _fetch_all() -> list:
    # The whole history is one static file on a CDN; (connect, read) timeout
    # generous for the ~44MB body.
    resp = get(ALL_URL, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


def fetch_hot_100(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    charts = _fetch_all()

    rows = []
    for chart in charts:
        chart_date = chart["date"]
        for entry in chart["data"]:
            rows.append({
                "chart_date": chart_date,
                "rank": entry["this_week"],
                "song": entry["song"],
                "artist": entry["artist"],
                "last_week": entry["last_week"],
                "peak_position": entry["peak_position"],
                "weeks_on_chart": entry["weeks_on_chart"],
            })

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="billboard-hot-100", fn=fetch_hot_100, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="billboard-hot-100-transform",
        deps=["billboard-hot-100"],
        sql='''
            SELECT
                CAST(chart_date AS DATE)        AS chart_date,
                CAST(rank AS INTEGER)           AS rank,
                song,
                artist,
                CAST(last_week AS INTEGER)      AS last_week,
                CAST(peak_position AS INTEGER)  AS peak_position,
                CAST(weeks_on_chart AS INTEGER) AS weeks_on_chart
            FROM "billboard-hot-100"
            WHERE chart_date IS NOT NULL
              AND rank IS NOT NULL
              AND song IS NOT NULL
              AND artist IS NOT NULL
              AND rank BETWEEN 1 AND 100
        ''',
    ),
]
